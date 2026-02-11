"""
Módulo de status da Bateria: carga, estado (carregando/descarregando/cheia) e temperatura.
Formato: <ícone> <carga>% 🌡️<temp>°C. Ícones: ⚡ carregando, 🔋 descarregando, 🔌 cheia.
Em sistema sem bateria ou falha: Bateria: N/A.
"""
import logging
from typing import Any

import psutil

from .base import BaseModule

logger = logging.getLogger(__name__)
TEMP_ICON = "\N{thermometer}"
ICON_CHARGING = "\u26a1"      # ⚡
ICON_DISCHARGING = "\U0001f50b"  # 🔋
ICON_FULL = "\U0001f50c"     # 🔌
FALLBACK = "Bateria: N/A"


def _battery_icon(plugged: bool | None, percent: float) -> str:
    if plugged is None:
        return ICON_DISCHARGING
    if plugged and percent >= 100:
        return ICON_FULL
    if plugged:
        return ICON_CHARGING
    return ICON_DISCHARGING


def _battery_temp() -> float | None:
    """Temperatura da bateria se disponível via sensores (comum em notebooks)."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        for key in ("BAT0", "BAT1", "battery", "acpitz"):
            if key in temps:
                for entry in temps[key]:
                    if entry.current and entry.current > 0:
                        return round(entry.current, 0)
        for sensor_list in temps.values():
            for entry in sensor_list:
                if entry.current and entry.current > 0 and "battery" in str(entry.label).lower():
                    return round(entry.current, 0)
    except Exception:
        pass
    return None


class BatteryModule(BaseModule):
    """Módulo Bateria para a barra do sistema."""

    @property
    def name(self) -> str:
        return "battery"

    @property
    def fallback_label(self) -> str:
        return "Bateria"

    def get_output(self, config: dict[str, Any] | None = None) -> str:
        try:
            bat = psutil.sensors_battery()
            if bat is None:
                return FALLBACK
            percent = bat.percent
            plugged = bat.power_plugged
            icon = _battery_icon(plugged, percent)
            temp = _battery_temp()
            if temp is not None:
                return f"{icon} {int(percent)}% {TEMP_ICON}{int(temp)}°C"
            return f"{icon} {int(percent)}%"
        except Exception as e:
            logger.debug("sensors_battery failed: %s", e)
            return FALLBACK
