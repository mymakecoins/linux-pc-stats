# Resumo da Fase 1: Estrutura e Módulo CPU

**Data de conclusão:** 11/02/2026

## O que foi feito

- **Estrutura do projeto:** Criados `src/`, `src/modules/`, com `main.py`, `config.py`, `__main__.py` e módulos em `src/modules/`.
- **requirements.txt:** Incluído `psutil>=5.9.0`.
- **Configuração:** `src/config.py` carrega `config.json` do diretório atual ou de `~/.config/linux-stats/config.json`; valores padrão quando o arquivo não existe ou é inválido (`modules.cpu: true`, `interval_seconds: 60`).
- **Contrato dos módulos:** `src/modules/base.py` define a classe abstrata `BaseModule` com `name` e `get_output(config)`.
- **Módulo CPU:** `src/modules/cpu.py` usa `psutil.cpu_percent(interval=0.1)` e `psutil.sensors_temperatures()`; saída no formato `CPU: X% 🌡️Y°C` ou `CPU: X% 🌡️N/A` quando não há sensor de temperatura; em falha total retorna `CPU: N/A`.
- **Core engine:** `src/main.py` carrega a config, invoca apenas o módulo CPU quando ativo, junta as saídas com ` | `, imprime uma linha em stdout e dorme pelo `interval_seconds`; exceções por módulo são tratadas e o módulo exibe `N/A` sem derrubar o loop.
- **Ponto de entrada:** Execução via `python -m src` (ou `python src/main.py`) a partir da raiz do projeto.
- **config.json.example:** Exemplo com `modules.cpu: true` e `interval_seconds: 60`.
- **README.md:** Descrição do projeto, dependência de `lm-sensors` para temperatura da CPU, instalação com `pip install -r requirements.txt`, configuração e execução.

## Desafios encontrados

- Nenhum bloqueador. Em ambientes sem `lm-sensors`, a temperatura da CPU é exibida como `N/A`, conforme previsto.
- Uso de `python3` no sistema (sem alias `python`); o README orienta a executar com o comando disponível.

## Critérios de sucesso atendidos

- [x] A aplicação inicia e lê o arquivo de configuração (ou usa padrões se o arquivo não existir).
- [x] Com o módulo CPU ativo, a aplicação imprime periodicamente uma linha no formato `CPU: X% 🌡️Y°C` (ou temperatura `N/A` quando não há sensor).
- [x] Se a coleta do módulo CPU falhar, a linha exibida contém `CPU: N/A` e a aplicação continua em execução.
- [x] Com o módulo CPU inativo na config, apenas os módulos ativos são exibidos (nesta fase, a linha fica vazia ou só com outros módulos futuros).
- [x] O loop respeita o intervalo configurado em `config.json` (ex.: 60 segundos).
- [x] O README menciona a dependência de `lm-sensors` para leitura de temperatura da CPU em Linux.
