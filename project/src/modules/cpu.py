"""
Módulo de telemetria da CPU: uso percentual e temperatura.
Formato: CPU: <uso>% 🌡️<temp>°C. Em falha: CPU: N/A.
Temperatura em Linux pode exigir lm-sensors (psutil.sensors_temperatures).
"""
import logging
from typing import Any

import psutil

from .base import BaseModule

logger = logging.getLogger(__name__)
TEMP_ICON = "\N{thermometer}"
FALLBACK = "CPU: N/A"


def _cpu_usage() -> float | None:
    """Uso da CPU em percentual (intervalo curto para amostra)."""
    try:
        return psutil.cpu_percent(interval=0.1)
    except Exception as e:
        logger.debug("cpu_percent failed: %s", e)
        return None


def _cpu_temperature() -> float | None:
    """
    Temperatura da CPU em °C.
    Em Linux usa psutil.sensors_temperatures(); pode exigir lm-sensors.
    """
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        # Preferir coretemp (Intel) ou k10temp (AMD), senão primeiro sensor
        for key in ("coretemp", "k10temp", "zenpower"):
            if key in temps:
                for entry in temps[key]:
                    if entry.current and entry.current > 0:
                        return round(entry.current, 0)
        # Fallback: primeira temperatura válida
        for sensor_list in temps.values():
            for entry in sensor_list:
                if entry.current and entry.current > 0:
                    return round(entry.current, 0)
    except Exception as e:
        logger.debug("sensors_temperatures failed: %s", e)
    return None


class CpuModule(BaseModule):
    """Módulo CPU para a barra do sistema."""

    @property
    def name(self) -> str:
        return "cpu"

    def get_output(self, config: dict[str, Any] | None = None) -> str:
        usage = _cpu_usage()
        if usage is None:
            return FALLBACK
        temp = _cpu_temperature()
        if temp is not None:
            return f"CPU: {int(usage)}% {TEMP_ICON}{int(temp)}°C"
        return f"CPU: {int(usage)}% {TEMP_ICON}N/A"
