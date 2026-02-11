"""
Módulo de uso do Disco (SSD/HD): uso percentual do disco principal e temperatura se disponível.
Formato: SSD: <uso>% 🌡️<temp>°C. Caminho configurável via config (disk_path, ex.: /).
"""
import logging
from typing import Any

import psutil

from .base import BaseModule

logger = logging.getLogger(__name__)
TEMP_ICON = "\N{thermometer}"
DEFAULT_DISK_PATH = "/"
FALLBACK = "SSD: N/A"


def _disk_usage(path: str) -> float | None:
    try:
        usage = psutil.disk_usage(path)
        return usage.percent
    except Exception as e:
        logger.debug("disk_usage(%s) failed: %s", path, e)
        return None


def _disk_temperature() -> float | None:
    """Temperatura de disco se disponível em sensors (nvme, drivetemp, etc.)."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        for key in ("nvme", "drivetemp", "samsung", "sdd", "hdd"):
            if key in temps:
                for entry in temps[key]:
                    if entry.current and entry.current > 0:
                        return round(entry.current, 0)
        for name, sensor_list in temps.items():
            if "drive" in name.lower() or "nvme" in name.lower() or "ssd" in name.lower():
                for entry in sensor_list:
                    if entry.current and entry.current > 0:
                        return round(entry.current, 0)
    except Exception:
        pass
    return None


class DiskModule(BaseModule):
    """Módulo Disco para a barra de status."""

    @property
    def name(self) -> str:
        return "disk"

    @property
    def fallback_label(self) -> str:
        return "SSD"

    def get_output(self, config: dict[str, Any] | None = None) -> str:
        path = DEFAULT_DISK_PATH
        if config:
            disk_config = config.get("disk") if isinstance(config.get("disk"), dict) else None
            if disk_config and isinstance(disk_config.get("path"), str):
                path = disk_config["path"]
            elif isinstance(config.get("disk_path"), str):
                path = config["disk_path"]
        percent = _disk_usage(path)
        if percent is None:
            return FALLBACK
        temp = _disk_temperature()
        if temp is not None:
            return f"SSD: {int(percent)}% {TEMP_ICON}{int(temp)}°C"
        return f"SSD: {int(percent)}%"
