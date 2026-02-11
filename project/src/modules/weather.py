"""
Módulo de previsão do tempo: CEP → Brasil API → WeatherAPI.com.
Formato: <ícone> <temp>°C. Cache com weather_interval_seconds (ex.: 3600).
Em erro: Tempo: N/A.
"""
import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from .base import BaseModule

logger = logging.getLogger(__name__)
FALLBACK = "Tempo: N/A"
REQUEST_TIMEOUT = 10

# Ícones por condição (WeatherAPI condition code)
# https://www.weatherapi.com/docs/weather_conditions.json
ICON_SUNNY = "\u2600\ufe0f"      # ☀️
ICON_PARTLY_CLOUDY = "\u26c5"    # ⛅
ICON_CLOUDY = "\u2601\ufe0f"     # ☁️
ICON_RAIN = "\U0001f327\ufe0f"   # 🌧️
ICON_THUNDER = "\u26c8\ufe0f"    # ⛈️
ICON_SNOW = "\u2744\ufe0f"       # ❄️
ICON_FOG = "\U0001f32b\ufe0f"    # 🌫️
ICON_DEFAULT = ICON_SUNNY


def _condition_icon(code: int) -> str:
    """Mapeia código de condição da WeatherAPI para emoji."""
    if code == 1000:
        return ICON_SUNNY
    if code == 1003:
        return ICON_PARTLY_CLOUDY
    if code in (1006, 1009):
        return ICON_CLOUDY
    if code in (1030, 1135, 1147):
        return ICON_FOG
    if code in (1087, 1273, 1276, 1279, 1282):
        return ICON_THUNDER
    if code in (
        1066, 1069, 1072, 1114, 1117, 1204, 1207, 1210, 1213, 1216, 1219,
        1222, 1225, 1249, 1252, 1255, 1258, 1261, 1264, 1237,
    ):
        return ICON_SNOW
    # Chuva e variantes (drizzle, rain, freezing rain, etc.)
    if code in (
        1063, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195,
        1198, 1201, 1240, 1243, 1246,
    ):
        return ICON_RAIN
    return ICON_DEFAULT


def _http_get(url: str) -> dict[str, Any] | None:
    """GET JSON com timeout; retorna None em falha."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "linux-stats-statusbar/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as e:
        logger.debug("HTTP GET %s failed: %s", url[:50], e)
        return None


def _cep_to_location(cep: str) -> tuple[str, str] | None:
    """Brasil API: CEP → (city, state). CEP pode ter ou não hífen."""
    cep_clean = cep.strip().replace("-", "").replace(" ", "")
    if len(cep_clean) != 8 or not cep_clean.isdigit():
        return None
    url = f"https://brasilapi.com.br/api/cep/v1/{cep_clean}"
    data = _http_get(url)
    if not data or not isinstance(data, dict):
        return None
    city = data.get("city") or data.get("localidade")
    state = data.get("state") or data.get("estado")
    if not city or not state:
        return None
    return (str(city).strip(), str(state).strip())


def _weather_current(api_key: str, query: str) -> tuple[float, int] | None:
    """
    WeatherAPI current: retorna (temp_c, condition_code) ou None.
    query: cidade, estado ou 'city,state'.
    """
    if not api_key or not query:
        return None
    base = "https://api.weatherapi.com/v1/current.json"
    params = urllib.parse.urlencode({"key": api_key, "q": query})
    url = f"{base}?{params}"
    data = _http_get(url)
    if not data or not isinstance(data, dict):
        return None
    current = data.get("current")
    if not current or not isinstance(current, dict):
        return None
    try:
        temp = float(current.get("temp_c", 0))
    except (TypeError, ValueError):
        return None
    cond = current.get("condition") or {}
    code = int(cond.get("code", 1000)) if isinstance(cond, dict) else 1000
    return (temp, code)


# Cache: (output_string, timestamp); invalida após weather_interval_seconds
_weather_cache: tuple[str, float] | None = None


def _get_weather_interval(config: dict[str, Any] | None) -> int:
    """Intervalo em segundos para atualizar dados do tempo (default 3600)."""
    if not config:
        return 3600
    try:
        sec = int(config.get("weather_interval_seconds", 3600))
        return max(60, min(sec, 86400))
    except (TypeError, ValueError):
        return 3600


class WeatherModule(BaseModule):
    """Módulo de previsão do tempo para a barra do sistema."""

    @property
    def name(self) -> str:
        return "weather"

    @property
    def fallback_label(self) -> str:
        return "Tempo"

    def get_output(self, config: dict[str, Any] | None = None) -> str:
        global _weather_cache
        config = config or {}
        cep = config.get("cep") or config.get("weather_cep")
        api_key = config.get("weather_api_key") or config.get("weatherapi_key")
        if not cep or not api_key:
            return FALLBACK

        cep_str = str(cep).strip()
        key_str = str(api_key).strip()
        if not cep_str or not key_str:
            return FALLBACK

        interval = _get_weather_interval(config)
        now = time.monotonic()

        if _weather_cache is not None:
            cached_out, cached_ts = _weather_cache
            if now - cached_ts < interval:
                return cached_out

        location = _cep_to_location(cep_str)
        if not location:
            logger.debug("CEP invalid or Brasil API failed")
            return FALLBACK

        city, state = location
        query = f"{city},{state}"
        result = _weather_current(key_str, query)
        if result is None:
            return FALLBACK

        temp_c, code = result
        icon = _condition_icon(code)
        out = f"{icon} {int(round(temp_c))}°C"
        _weather_cache = (out, now)
        return out
