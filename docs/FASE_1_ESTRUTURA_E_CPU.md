# Fase 1: Estrutura e Módulo CPU

**Objetivo:** Estabelecer a estrutura base do projeto, o core engine com loop e agregação de módulos, e o primeiro módulo de telemetria (CPU), com saída no formato definido e tratamento de falha.

---

## 1. Objetivos da Fase

- Definir a estrutura de diretórios e do projeto Python (pacotes, pontos de entrada).
- Implementar leitura de configuração a partir de `config.json` (módulos ativos, intervalo de atualização).
- Implementar o core engine (`main.py`): loop principal que, em intervalos configurados, invoca os módulos ativos, agrega as saídas e imprime uma única linha em stdout.
- Implementar o módulo CPU: uso percentual e temperatura da CPU via `psutil`, com saída no formato `CPU: <uso>% 🌡️<temp>°C`.
- Garantir que, em caso de falha na coleta (ex.: sensor indisponível), o módulo retorne/exiba `N/A` sem interromper a aplicação.
- Documentar a dependência opcional de `lm-sensors` para leitura de temperatura no README.

---

## 2. Tarefas Técnicas

| # | Tarefa | Detalhes |
|---|--------|----------|
| 1 | Criar `requirements.txt` | Incluir `psutil` com versão mínima recomendada (ex.: `psutil>=5.9.0`). |
| 2 | Estrutura de diretórios | Criar `src/`, `src/modules/`; `main.py` e `config.py` em `src/`; módulos em `src/modules/`. |
| 3 | Schema de `config.json` | Campos: `modules` (objeto ou lista com flags por módulo, ex.: `cpu: true`), `interval_seconds` (número, ex.: 60). Definir localização do arquivo (ex.: junto ao projeto ou em `~/.config/linux-stats/`). |
| 4 | Módulo de configuração | `src/config.py`: carregar e validar `config.json`; expor quais módulos estão ativos e o intervalo. Tratar arquivo ausente ou inválido (valores padrão ou saída clara de erro). |
| 5 | Interface base dos módulos | `src/modules/base.py`: definir contrato (ex.: função `get_output() -> str` ou classe base com método que retorna string). Cada módulo deve retornar um fragmento de linha ou `N/A` em falha. |
| 6 | Módulo CPU | `src/modules/cpu.py`: usar `psutil.cpu_percent()` e `psutil.sensors_temperatures()` (ou equivalente) para temperatura; formatar como `CPU: X% 🌡️Y°C`; em erro, retornar `CPU: N/A`. |
| 7 | Core engine | `src/main.py`: carregar config; registrar módulos ativos (apenas CPU nesta fase); loop: a cada `interval_seconds`, chamar cada módulo, juntar saídas com ` \| `, imprimir uma linha em stdout; tratar exceções por módulo para não derrubar o loop. |
| 8 | Ponto de entrada | Permitir execução via `python -m src` ou `python src/main.py` a partir da raiz do projeto. |
| 9 | Arquivo de config de exemplo | Fornecer `config.json.example` ou trecho no README com estrutura mínima (CPU ativo, intervalo 60). |
| 10 | Documentação | README: descrição do projeto, dependência de `lm-sensors` para temperatura da CPU em Linux, como instalar (`pip install -r requirements.txt`) e como executar. |

---

## 3. Arquivos a Criar ou Alterar

| Arquivo | Ação |
|---------|------|
| `requirements.txt` | Criar |
| `README.md` | Criar |
| `src/__init__.py` | Criar (pode ser vazio) |
| `src/main.py` | Criar |
| `src/config.py` | Criar |
| `src/modules/__init__.py` | Criar |
| `src/modules/base.py` | Criar |
| `src/modules/cpu.py` | Criar |
| `config.json.example` | Criar (ou documentar no README) |

Nenhum arquivo da análise técnica ou requisitos em `docs/` precisa ser alterado nesta fase.

---

## 4. Critérios de Sucesso

- [ ] A aplicação inicia e lê o arquivo de configuração (ou usa padrões se o arquivo não existir).
- [ ] Com o módulo CPU **ativo** na config, a aplicação imprime periodicamente uma linha no formato `CPU: X% 🌡️Y°C` (com valores reais ou temperatura como `N/A` se `lm-sensors` não estiver disponível).
- [ ] Se a coleta do módulo CPU falhar (ex.: exceção em `psutil`), a linha exibida contém `CPU: N/A` e a aplicação continua em execução.
- [ ] Com o módulo CPU **inativo** na config, a linha de saída não contém o fragmento da CPU (ou a aplicação imprime linha vazia/apenas delimitadores, conforme definido no core).
- [ ] O loop respeita o intervalo configurado em `config.json` (ex.: 60 segundos).
- [ ] O README menciona a dependência de `lm-sensors` para leitura de temperatura da CPU em Linux.
