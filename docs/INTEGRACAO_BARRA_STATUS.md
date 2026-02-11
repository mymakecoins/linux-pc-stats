# Integração com Polybar e Waybar

Este documento descreve como exibir a saída do **Utilitário para a barra do sistema** (linux-stats) na Polybar ou na Waybar. O executável mantém o nome `linux-stats-statusbar`; em inglês, “status bar” = barra do sistema (barra do Gerenciador de Tarefas). A aplicação imprime **uma linha por ciclo** na saída padrão (stdout); logs de diagnóstico vão para stderr.

---

## Se você instalou pelo pacote .deb

1. **Config:** crie a configuração (senão só o módulo CPU aparece, com defaults):
   ```bash
   mkdir -p ~/.config/linux-stats
   cp /usr/share/linux-stats/config.json.example ~/.config/linux-stats/config.json
   # Edite com seu CEP, weather_api_key e módulos desejados
   ```

2. **Comando na barra:** use sempre o executável do pacote:
   - **Exec:** `/usr/bin/linux-stats-statusbar`
   (Não use caminho do projeto nem `run-statusbar.sh`.)

3. Adicione o módulo na config da Polybar ou Waybar conforme as seções abaixo, usando `exec = /usr/bin/linux-stats-statusbar` (Polybar) ou `"exec": "/usr/bin/linux-stats-statusbar"` (Waybar).

4. **Reinicie a barra** (recarregar config ou reiniciar o processo da Polybar/Waybar).

---

## Pré-requisitos (instalação pelo código-fonte)

- Ter executado `./install.sh` na raiz do projeto (ou instalado as dependências com `pip install -r requirements.txt`).
- Caminho absoluto do projeto (ex.: `/home/user/linux-stats`). Abaixo usa `LINUX_STATS_DIR` como placeholder — substitua pelo seu caminho.

Se você usa o script de execução:

```bash
LINUX_STATS_DIR="/home/user/linux-stats"   # ajuste
"$LINUX_STATS_DIR/run-statusbar.sh"        # usa .venv/bin/python se existir, senão python3
```

---

## Polybar

A aplicação roda em loop e imprime uma nova linha a cada intervalo (ex.: 60 segundos). Use o módulo **custom/script** com **tail = true** para que a Polybar leia a saída de forma contínua.

Adicione um módulo no seu `config` da Polybar (ex.: `~/.config/polybar/config`):

**Se instalou pelo .deb:**
```ini
[module/linux-stats]
type = custom/script
exec = /usr/bin/linux-stats-statusbar
tail = true
interval = 0
```

**Se instalou pelo código-fonte:**
```ini
[module/linux-stats]
type = custom/script
exec = /home/user/linux-stats/run-statusbar.sh
tail = true
interval = 0
```

- **exec:** com .deb use `/usr/bin/linux-stats-statusbar`; com código-fonte use o caminho absoluto para `run-statusbar.sh`.
- **tail = true:** a Polybar mantém o script rodando e exibe cada nova linha impressa.
- **interval = 0:** a atualização é controlada pelo script, não por um timer da Polybar.

Inclua o módulo na barra na seção `modules-right` (ou `modules-left` / `modules-center`):

```ini
modules-right = ... linux-stats ...
```

Reinicie a Polybar para aplicar. A linha de status será atualizada a cada intervalo definido no seu `config.json` (ex.: 60 segundos).

### Troubleshooting (Polybar)

- **Nada aparece na barra:** (1) Confira se em `exec` está `/usr/bin/linux-stats-statusbar` (após .deb) ou o caminho correto para `run-statusbar.sh`. (2) Crie `~/.config/linux-stats/config.json` (copie de `/usr/share/linux-stats/config.json.example` ou do projeto). (3) Reinicie a Polybar (killall polybar e suba de novo, ou recarregue a config). (4) Teste no terminal: `linux-stats-statusbar` ou `/usr/bin/linux-stats-statusbar` e veja se imprime uma linha.
- **Só uma linha e não atualiza:** verifique se `tail = true` está definido.
- **Erro de Python ou módulo:** com .deb não deve ocorrer; com código-fonte rode `./install.sh` e use `run-statusbar.sh`.

---

## Waybar

No Waybar, um módulo **custom** pode executar um script. Como a aplicação fica em loop, duas abordagens são possíveis.

### Opção 1: Script que imprime uma linha e encerra (recomendado)

Use **interval** para reexecutar o script a cada N segundos e capture apenas a primeira linha. Ajuste o intervalo para o mesmo valor (ou próximo) do `interval_seconds` do seu `config.json`.

No seu `config` do Waybar (ex.: `~/.config/waybar/config`):

**Se instalou pelo .deb:**
```json
"custom/linux-stats": {
    "exec": "/usr/bin/linux-stats-statusbar 2>/dev/null | head -1",
    "interval": 60,
    "format": "{}"
}
```

**Se instalou pelo código-fonte:**
```json
"custom/linux-stats": {
    "exec": "/home/user/linux-stats/run-statusbar.sh 2>/dev/null | head -1",
    "interval": 60,
    "format": "{}"
}
```

- **exec:** com .deb use `/usr/bin/linux-stats-statusbar`; com código-fonte use o caminho para `run-statusbar.sh`. O `head -1` faz o processo encerrar após a primeira linha (o Waybar mata o processo ao reexecutar).
- **interval:** em segundos; use o mesmo valor (ou próximo) do `interval_seconds` do `config.json` (ex.: 60).
- **format:** `{}` exibe o texto retornado pelo script.

Inclua o módulo na barra, por exemplo em `modules-right`:

```json
"modules-right": ["custom/linux-stats", ...]
```

### Opção 2: Script em execução contínua

Se a sua versão do Waybar suportar um script que roda de forma contínua e emite linhas (estilo “stream”), você pode usar diretamente:

```json
"custom/linux-stats": {
    "exec": "/home/user/linux-stats/run-statusbar.sh",
    "format": "{}"
}
```

O comportamento exato depende do Waybar; se a barra não atualizar sozinha, use a opção 1.

### Troubleshooting (Waybar)

- **Módulo vazio ou não atualiza:** use a opção 1 com `interval` e `head -1`; confira o caminho em `exec` e se `run-statusbar.sh` é executável.
- **Atraso na primeira exibição:** na opção 1, a primeira linha pode demorar até um ciclo (ex.: 60 s); é o comportamento esperado.

---

## Saída em stdout

A aplicação **só imprime a linha de status em stdout** (uma linha por ciclo). Mensagens de log (erros, debug) vão para **stderr**, para não interferir na integração com Polybar/Waybar. Se redirecionar stderr (ex.: `2>/dev/null`), eventuais erros não aparecerão no terminal.
