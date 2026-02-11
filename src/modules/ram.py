"""
Módulo de telemetria da RAM: uso percentual da memória.
Formato: RAM: <uso>%. Em falha: RAM: N/A.
"""
import logging
from typing import Any

import psutil

from .base import BaseModule

logger = logging.getLogger(__name__)
FALLBACK = "RAM: N/A"


class RamModule(BaseModule):
    """Módulo RAM para a barra de status."""

    @property
    def name(self) -> str:
        return "ram"

    def get_output(self, config: dict[str, Any] | None = None) -> str:
        try:
            percent = psutil.virtual_memory().percent
            return f"RAM: {int(percent)}%"
        except Exception as e:
            logger.debug("virtual_memory failed: %s", e)
            return FALLBACK
