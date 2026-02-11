#!/usr/bin/env bash
# Executa o utilitário da barra do sistema a partir do diretório do projeto.
# Use este script na Polybar/Waybar ou no .desktop (ajustando o caminho).
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
export PYTHONPATH="${DIR}${PYTHONPATH:+:$PYTHONPATH}"
if [[ -x "$DIR/.venv/bin/python" ]]; then
    exec "$DIR/.venv/bin/python" -m src "$@"
else
    exec python3 -m src "$@"
fi
