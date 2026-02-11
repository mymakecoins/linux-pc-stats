#!/usr/bin/env bash
#
# Script de instalação do Status Bar Utility.
# Executar a partir da raiz do projeto: ./install.sh
# Idempotente: pode ser executado várias vezes.
#
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[linux-stats] Diretório do projeto: $SCRIPT_DIR"

# Verificar Python 3
if ! command -v python3 &>/dev/null; then
    echo "[linux-stats] ERRO: python3 não encontrado. Instale Python 3.10 ou superior (ex.: sudo apt install python3 python3-pip)." >&2
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || true)
echo "[linux-stats] Python encontrado: $(python3 --version 2>&1)"

# Criar venv se não existir
VENV_DIR="$SCRIPT_DIR/.venv"
if [[ ! -d "$VENV_DIR" ]]; then
    echo "[linux-stats] Criando ambiente virtual em $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
else
    echo "[linux-stats] Ambiente virtual já existe: $VENV_DIR"
fi

# Instalar dependências
echo "[linux-stats] Instalando dependências (pip install -r requirements.txt) ..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "[linux-stats] Dependências instaladas."

# Config padrão
if [[ ! -f "$SCRIPT_DIR/config.json" ]]; then
    if [[ -f "$SCRIPT_DIR/config.json.example" ]]; then
        cp "$SCRIPT_DIR/config.json.example" "$SCRIPT_DIR/config.json"
        echo "[linux-stats] config.json criado a partir de config.json.example. Edite-o com seu CEP, API key do tempo e módulos desejados."
    fi
fi

# Dependência opcional do sistema para temperatura da CPU
echo ""
echo "[linux-stats] Opcional: para exibir temperatura da CPU, instale lm-sensors:"
echo "  sudo apt install lm-sensors   # Ubuntu/Debian"
echo "  sudo sensors-detect           # calibração (opcional)"
echo ""
echo "[linux-stats] Para executar a aplicação:"
echo "  $SCRIPT_DIR/run-statusbar.sh"
echo "  ou, a partir deste diretório:"
echo "  PYTHONPATH=. .venv/bin/python -m src"
echo ""

# Detectar ambiente de desktop (ou perguntar) e mostrar instruções para exibir na barra
if [[ -x "$SCRIPT_DIR/scripts/detect-desktop.sh" ]]; then
    echo "[linux-stats] Onde exibir os dados na barra do sistema:"
    "$SCRIPT_DIR/scripts/detect-desktop.sh" --instructions 1>&2
    echo ""
fi

echo "[linux-stats] Instalação concluída."
