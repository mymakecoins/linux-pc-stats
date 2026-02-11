# linux-pc-stats — Utilitário para a barra do sistema

Aplicação modular em Python que exibe telemetria do sistema (CPU, RAM, bateria, disco, GPU) e previsão do tempo na **barra do sistema** (barra do Gerenciador de Tarefas, próximo ao relógio e ícones) ou em barras alternativas (Polybar, Waybar). O executável mantém o nome `linux-stats-statusbar`; em inglês, “status bar” = barra do sistema.

## Requisitos

- Python 3.10+
- **lm-sensors** (opcional): para temperatura da CPU em Linux (`sudo apt install lm-sensors` em Ubuntu/Debian)

## Instalação rápida

```bash
git clone https://github.com/mymakecoins/linux-pc-stats.git
cd linux-pc-stats
pip install -r requirements.txt
```

Ou use o script de instalação (cria venv e instala dependências):

```bash
chmod +x install.sh run-statusbar.sh
./install.sh
```

## Configuração

Copie o exemplo e edite:

```bash
cp config.json.example config.json
```

A aplicação procura `config.json` no diretório atual ou em `~/.config/linux-stats/config.json`.

- **modules**: ativa/desativa cada módulo (`cpu`, `ram`, `battery`, `disk`, `gpu`, `weather`).
- **interval_seconds**: intervalo em segundos entre atualizações (ex.: 60).
- **disk_path** (opcional): ponto de montagem do disco (padrão: `"/"`).
- **cep** e **weather_api_key**: para o módulo de previsão do tempo (WeatherAPI.com; cadastro gratuito).
- **weather_interval_seconds** (opcional): intervalo de atualização do tempo (padrão: 3600).

GPU: apenas **NVIDIA** é suportada nesta versão (GPUtil); AMD planejada como melhoria futura.

## Execução

```bash
./run-statusbar.sh
```

Ou, sem o script:

```bash
PYTHONPATH=. python3 -m src
```

A aplicação imprime **uma linha** em stdout a cada intervalo (ex.: `CPU: 20% 🌡82°C | RAM: 65% | ...`). Logs vão para stderr.

## Exibir na barra do sistema

- **Barra do sistema (GNOME, KDE, XFCE):** execute `./scripts/detect-desktop.sh --instructions` para identificar o ambiente e ver as instruções. Se instalou pelo pacote .deb, use o comando `linux-stats-setup-bar`.
- **Polybar:** módulo `custom/script` com `exec = /caminho/para/run-statusbar.sh` e `tail = true`.
- **Waybar:** módulo `custom` com `exec` e `interval`; exemplo: `exec = "/caminho/para/run-statusbar.sh 2>/dev/null | head -1"`, `interval = 60`.

## Estrutura do repositório

- **src/**: código Python (módulos de telemetria e tempo).
- **scripts/detect-desktop.sh**: detecta o ambiente de desktop ou pergunta ao usuário; mostra instruções para exibir na barra.
- **config.json.example**: exemplo de configuração.
- **requirements.txt**: dependências (psutil, GPUtil).

## Licença

Consulte o repositório principal ou o histórico do projeto.
