"""
Core engine: carrega a configuração, invoca os módulos ativos em loop
e imprime uma única linha em stdout a cada intervalo.
"""
import logging
import sys
import time

from src.config import get_interval_seconds, is_module_enabled, load_config
from src.modules.battery import BatteryModule
from src.modules.cpu import CpuModule
from src.modules.disk import DiskModule
from src.modules.gpu import GpuModule
from src.modules.ram import RamModule
from src.modules.weather import WeatherModule

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s:%(name)s:%(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

DELIMITER = " | "

# Ordem fixa: CPU, RAM, Bateria, Disco, GPU, Tempo
MODULES = [
    ("cpu", CpuModule()),
    ("ram", RamModule()),
    ("battery", BatteryModule()),
    ("disk", DiskModule()),
    ("gpu", GpuModule()),
    ("weather", WeatherModule()),
]


def _collect_outputs(config: dict) -> list[str]:
    """Chama cada módulo ativo e retorna lista de strings; falhas viram N/A por módulo."""
    outputs: list[str] = []
    for key, mod in MODULES:
        if not is_module_enabled(config, key):
            continue
        try:
            out = mod.get_output(config)
            outputs.append(out)
        except Exception as e:
            logger.debug("module %s failed: %s", key, e)
            outputs.append(f"{mod.fallback_label}: N/A")
    return outputs


def run_loop() -> None:
    """Loop principal: a cada interval_seconds, coleta módulos ativos e imprime uma linha."""
    config = load_config()
    interval = get_interval_seconds(config)

    while True:
        parts = _collect_outputs(config)
        line = DELIMITER.join(parts)
        print(line, flush=True)
        time.sleep(interval)


def main() -> None:
    run_loop()


if __name__ == "__main__":
    main()
