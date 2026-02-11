"""
Módulo de telemetria da GPU (NVIDIA via GPUtil).
Formato: GPU: <uso>% 🌡️<temp>°C. Em ausência de GPU NVIDIA ou falha: GPU: N/A.
Suporte a AMD está fora do escopo nesta fase (melhoria futura).
"""
import logging
from typing import Any

from .base import BaseModule

logger = logging.getLogger(__name__)
TEMP_ICON = "\N{thermometer}"
FALLBACK = "GPU: N/A"


def _nvidia_gpu_stats() -> tuple[float, float] | None:
    """Retorna (load_percent, temp_c) da primeira GPU NVIDIA ou None."""
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if not gpus:
            return None
        g = gpus[0]
        load = (g.load or 0) * 100
        temp = g.temperature
        if temp is None:
            temp = 0
        return (load, float(temp))
    except Exception as e:
        logger.debug("GPUtil failed: %s", e)
        return None


class GpuModule(BaseModule):
    """Módulo GPU (NVIDIA) para a barra do sistema."""

    @property
    def name(self) -> str:
        return "gpu"

    def get_output(self, config: dict[str, Any] | None = None) -> str:
        stats = _nvidia_gpu_stats()
        if stats is None:
            return FALLBACK
        load, temp = stats
        return f"GPU: {int(load)}% {TEMP_ICON}{int(temp)}°C"
