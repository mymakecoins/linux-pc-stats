#!/usr/bin/env bash
#
# Detecta o ambiente de desktop (GNOME, KDE, XFCE, etc.) ou pergunta ao usuário.
# Saída (stdout): uma única palavra (GNOME, KDE, XFCE, MATE, POLYBAR_WAYBAR, OUTRO).
# Mensagens e instruções vão para stderr.
#
set -e

# -----------------------------------------------------------------------------
# Detecção automática
# -----------------------------------------------------------------------------
_detect_from_env() {
    local xdg="${XDG_CURRENT_DESKTOP:-}"
    local session="${DESKTOP_SESSION:-}"
    xdg="${xdg^^}"
    session="${session^^}"
    case "${xdg}" in
        *GNOME*|*UBUNTU*GNOME*) echo -n "GNOME"; return 0 ;;
        *KDE*|*PLASMA*)        echo -n "KDE"; return 0 ;;
        *XFCE*)                echo -n "XFCE"; return 0 ;;
        *MATE*)                echo -n "MATE"; return 0 ;;
        *LXDE*)                echo -n "LXDE"; return 0 ;;
        *)                     : ;;
    esac
    case "${session}" in
        *GNOME*|*UBUNTU*) echo -n "GNOME"; return 0 ;;
        *PLASMA*|*KDE*)   echo -n "KDE"; return 0 ;;
        *XFCE*)           echo -n "XFCE"; return 0 ;;
        *MATE*)           echo -n "MATE"; return 0 ;;
        *)                return 1 ;;
    esac
}

_detect_from_processes() {
    if pgrep -x gnome-shell >/dev/null 2>&1; then echo -n "GNOME"; return 0; fi
    if pgrep -x plasmashell >/dev/null 2>&1; then echo -n "KDE"; return 0; fi
    if pgrep -x xfce4-panel >/dev/null 2>&1; then echo -n "XFCE"; return 0; fi
    if pgrep -x mate-panel >/dev/null 2>&1; then echo -n "MATE"; return 0; fi
    if pgrep -x polybar >/dev/null 2>&1; then echo -n "POLYBAR_WAYBAR"; return 0; fi
    if pgrep -x waybar >/dev/null 2>&1; then echo -n "POLYBAR_WAYBAR"; return 0; fi
    return 1
}

_detect_from_packages() {
    # Usado quando rodamos como root (ex.: postinst) sem sessão do usuário
    if command -v dpkg >/dev/null 2>&1; then
        if dpkg -l gnome-shell 2>/dev/null | grep -q '^ii'; then echo -n "GNOME"; return 0; fi
        if dpkg -l plasma-desktop 2>/dev/null | grep -q '^ii'; then echo -n "KDE"; return 0; fi
        if dpkg -l xfce4-panel 2>/dev/null | grep -q '^ii'; then echo -n "XFCE"; return 0; fi
        if dpkg -l mate-panel 2>/dev/null | grep -q '^ii'; then echo -n "MATE"; return 0; fi
    fi
    return 1
}

# -----------------------------------------------------------------------------
# Perguntar ao usuário (modo interativo)
# -----------------------------------------------------------------------------
_ask_user() {
    echo "Não foi possível identificar o ambiente de desktop." >&2
    echo "Onde você quer exibir os dados do linux-stats?" >&2
    echo "" >&2
    echo "  1) Barra do sistema (GNOME / Ubuntu padrão)" >&2
    echo "  2) Barra do sistema (KDE Plasma)" >&2
    echo "  3) Barra do sistema (XFCE)" >&2
    echo "  4) Barra do sistema (MATE)" >&2
    echo "  5) Polybar ou Waybar (barra alternativa)" >&2
    echo "  6) Outro / ainda não sei" >&2
    echo "" >&2
    local n
    while true; do
        printf "Escolha (1-6): " >&2
        read -r n 2>/dev/null || true
        case "${n}" in
            1) echo -n "GNOME"; return 0 ;;
            2) echo -n "KDE"; return 0 ;;
            3) echo -n "XFCE"; return 0 ;;
            4) echo -n "MATE"; return 0 ;;
            5) echo -n "POLYBAR_WAYBAR"; return 0 ;;
            6) echo -n "OUTRO"; return 0 ;;
            *) echo "Opção inválida. Use 1 a 6." >&2 ;;
        esac
    done
}

# -----------------------------------------------------------------------------
# Instruções por ambiente (imprime em stderr)
# -----------------------------------------------------------------------------
_print_instructions() {
    local de="$1"
    local cmd="${2:-/usr/bin/linux-stats-statusbar}"
    case "$de" in
        GNOME)
            echo "Ambiente: GNOME (barra superior do sistema)." >&2
            echo "Para exibir na barra: é necessária uma extensão GNOME Shell." >&2
            echo "Veja: /usr/share/doc/linux-stats/INTEGRACAO_BARRA_STATUS.md ou docs/PLANO_BARRA_SISTEMA.md" >&2
            ;;
        KDE)
            echo "Ambiente: KDE Plasma (painel do sistema)." >&2
            echo "Para exibir na barra: use um widget de painel que execute um comando (ex.: $cmd)." >&2
            echo "Veja a documentação em docs/PLANO_BARRA_SISTEMA.md" >&2
            ;;
        XFCE)
            echo "Ambiente: XFCE (painel)." >&2
            echo "Para exibir na barra: adicione o plugin 'Generic Monitor' ao painel e configure o comando: $cmd" >&2
            echo "Veja a documentação em docs/PLANO_BARRA_SISTEMA.md" >&2
            ;;
        MATE)
            echo "Ambiente: MATE (painel)." >&2
            echo "Para exibir na barra: use um applet que execute um comando (ex.: $cmd)." >&2
            echo "Veja a documentação em docs/PLANO_BARRA_SISTEMA.md" >&2
            ;;
        POLYBAR_WAYBAR)
            echo "Ambiente: Polybar ou Waybar." >&2
            echo "Adicione um módulo com exec = $cmd (Polybar: tail = true). Ver docs/INTEGRACAO_BARRA_STATUS.md" >&2
            ;;
        *)
            echo "Ambiente: $de" >&2
            echo "Consulte a documentação em docs/PLANO_BARRA_SISTEMA.md e docs/INTEGRACAO_BARRA_STATUS.md" >&2
            ;;
    esac
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
SHOW_INSTRUCTIONS=0
ASK_IF_UNKNOWN=1
for arg in "$@"; do
    case "$arg" in
        --instructions) SHOW_INSTRUCTIONS=1 ;;
        --no-ask)       ASK_IF_UNKNOWN=0 ;;
    esac
done

DE=""
_detect_from_env && DE="$(_detect_from_env)" || true
[[ -z "$DE" ]] && _detect_from_processes && DE="$(_detect_from_processes)" || true
[[ -z "$DE" ]] && _detect_from_packages && DE="$(_detect_from_packages)" || true

if [[ -z "$DE" ]]; then
    if [[ "$ASK_IF_UNKNOWN" -eq 1 ]] && [[ -t 0 ]]; then
        DE="$(_ask_user)"
    else
        echo "Ambiente de desktop não identificado. Execute este script interativamente para escolher ou use: linux-stats-setup-bar" >&2
        DE="OUTRO"
    fi
fi

if [[ "$SHOW_INSTRUCTIONS" -eq 1 ]]; then
    _print_instructions "$DE" "${LINUX_STATS_CMD:-/usr/bin/linux-stats-statusbar}"
fi

# Saída final: apenas o código do ambiente (para captura com DE=$(...))
echo "$DE"
