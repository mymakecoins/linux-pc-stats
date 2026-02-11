# Empacotamento .deb (Debian/Ubuntu)

É possível empacotar o **Utilitário para a barra do sistema** (linux-stats; o executável mantém o nome `linux-stats-statusbar` — “status bar” = barra do sistema) em um pacote `.deb` para instalação em sistemas baseados em Debian/Ubuntu.

## Estrutura

A pasta `debian/` contém os arquivos de empacotamento:

| Arquivo | Descrição |
|---------|-----------|
| `debian/control` | Metadados do pacote, dependência de `python3` (>= 3.10), recomendação de `lm-sensors`. |
| `debian/rules` | Regras de build: copia `project/` (contém `src/`) e `config.json.example` para `/usr/share/linux-stats/`, instala dependências Python em `/usr/share/linux-stats/lib`, cria o script `/usr/bin/linux-stats-statusbar` e o `.desktop`. |
| `debian/changelog` | Histórico de versões (edite ao lançar nova versão). |
| `debian/compat` | Nível de compatibilidade do debhelper. |
| `debian/linux-stats.docs` | Documentos instalados em `/usr/share/doc/linux-stats/`. |
| `debian/postinst` | Script pós-instalação (byte-compila Python e lembra da configuração). |

## Pré-requisitos para build

```bash
sudo apt install build-essential debhelper python3 python3-pip python3-venv
```

## Gerar o .deb

Na **raiz do repositório** (onde estão `debian/`, `project/`, `requirements.txt`):

```bash
dpkg-buildpackage -us -uc -b
```

- `-b`: apenas o pacote binário (não assina o source).
- `-us -uc`: não assina com sua chave (útil para build local).

O arquivo gerado fica no diretório pai, por exemplo:

- `../linux-stats_1.0.0-1_all.deb`

## Instalar o pacote

```bash
sudo dpkg -i ../linux-stats_1.0.0-1_all.deb
```

Se faltar alguma dependência:

```bash
sudo apt install -f
```

## Onde os arquivos vão

| Após instalação | Conteúdo |
|-----------------|----------|
| `/usr/bin/linux-stats-statusbar` | Script que define `PYTHONPATH` e executa `python3 -m src`. |
| `/usr/share/linux-stats/` | Código (`project/src/`), `config.json.example` e dependências em `lib/`. |
| `/usr/share/applications/linux-stats-statusbar.desktop` | Atalho .desktop (Exec aponta para `/usr/bin/linux-stats-statusbar`). |
| `/usr/share/doc/linux-stats/` | README e INTEGRACAO_BARRA_STATUS.md. |

## Configuração após instalar o .deb

A aplicação continua lendo a config em:

1. Diretório atual (se você rodar de um dir que tenha `config.json`).
2. `~/.config/linux-stats/config.json`.

Recomendado para instalação via .deb:

```bash
mkdir -p ~/.config/linux-stats
cp /usr/share/linux-stats/config.json.example ~/.config/linux-stats/config.json
# Edite com seu CEP, weather_api_key e módulos
```

Depois, use na Polybar/Waybar o executável:

- **Exec:** `/usr/bin/linux-stats-statusbar`

(Em vez de `run-statusbar.sh` do repositório.)

## Atualizar a versão no pacote

1. Edite `debian/changelog`: nova entrada no topo com versão (ex.: `1.0.1-1`) e descrição das mudanças.
2. Rebuild: `dpkg-buildpackage -us -uc -b`.
3. Reinstale: `sudo dpkg -i ../linux-stats_1.0.1-1_all.deb`.

## Manutenção do pacote

- **Maintainer:** altere `Maintainer` em `debian/control` e no `changelog` para seu nome/e-mail.
- **Dependências:** se adicionar novas bibliotecas em `requirements.txt`, o build continua usando `pip install --target=...`; não é necessário listar cada uma em `Depends`, pois ficam em `/usr/share/linux-stats/lib`.
