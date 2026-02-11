"""
Carregamento e validação do arquivo de configuração (config.json).
Procura em: diretório atual, depois ~/.config/linux-stats/
"""
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_INTERVAL_SECONDS = 60
DEFAULT_MODULES = {"cpu": True}


def _config_paths() -> list[Path]:
    """Ordem de busca do config.json."""
    cwd = Path.cwd()
    xdg = Path.home() / ".config" / "linux-stats"
    return [
        cwd / "config.json",
        xdg / "config.json",
    ]


def _find_config_path() -> Path | None:
    """Retorna o primeiro path existente de config ou None."""
    for p in _config_paths():
        if p.is_file():
            return p
    return None


def load_config() -> dict[str, Any]:
    """
    Carrega config.json. Se não existir ou for inválido, retorna valores padrão.
    Padrões: modules.cpu = True, interval_seconds = 60.
    """
    path = _find_config_path()
    if path is None:
        return _default_config()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return _default_config()

    return _normalize_config(data)


def _default_config() -> dict[str, Any]:
    """Configuração padrão quando arquivo não existe ou é inválido."""
    return {
        "modules": dict(DEFAULT_MODULES),
        "interval_seconds": DEFAULT_INTERVAL_SECONDS,
    }


def _normalize_config(data: dict[str, Any]) -> dict[str, Any]:
    """Preenche campos faltantes e garante tipos."""
    if not isinstance(data, dict):
        return _default_config()

    modules = data.get("modules")
    if not isinstance(modules, dict):
        modules = dict(DEFAULT_MODULES)
    else:
        modules = {k: bool(v) for k, v in modules.items()}
    if "cpu" not in modules:
        modules["cpu"] = True

    try:
        interval = int(data.get("interval_seconds", DEFAULT_INTERVAL_SECONDS))
    except (TypeError, ValueError):
        interval = DEFAULT_INTERVAL_SECONDS
    interval = max(1, min(interval, 86400))

    return {
        "modules": modules,
        "interval_seconds": interval,
    }


def is_module_enabled(config: dict[str, Any], module_name: str) -> bool:
    """Retorna True se o módulo estiver ativo na config."""
    return config.get("modules", {}).get(module_name, False)


def get_interval_seconds(config: dict[str, Any]) -> int:
    """Retorna o intervalo em segundos entre atualizações."""
    return config.get("interval_seconds", DEFAULT_INTERVAL_SECONDS)
