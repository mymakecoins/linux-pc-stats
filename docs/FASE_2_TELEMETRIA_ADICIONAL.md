# Fase 2: Módulos de Telemetria Adicionais

**Objetivo:** Implementar os módulos de RAM, Bateria, Disco (SSD) e GPU (NVIDIA via GPUtil), mantendo o formato de saída definido na análise técnica, o fallback `N/A` por módulo e a ordem/delimitador na linha final.

---

## 1. Objetivos da Fase

- Implementar o módulo **RAM**: uso percentual da memória; saída no formato `RAM: <uso>%`.
- Implementar o módulo **Bateria**: percentual de carga, estado (carregando/descarregando/cheia) e temperatura quando disponível; ícones ⚡ (carregando), 🔋 (descarregando), 🔌 (cheia); formato `<ícone> <carga>% 🌡️<temp>°C`.
- Implementar o módulo **Disco (SSD)**: uso percentual do disco principal e temperatura quando disponível; formato `SSD: <uso>% 🌡️<temp>°C`; definir convenção ou config para "disco principal" (ex.: montagem `/`).
- Implementar o módulo **GPU**: uso e temperatura para NVIDIA via GPUtil; formato `GPU: <uso>% 🌡️<temp>°C`; em sistemas sem GPU NVIDIA ou em falha, exibir `GPU: N/A`. Suporte a AMD fica fora do escopo (documentar como melhoria futura).
- Garantir que a ordem dos módulos na linha final seja consistente (ex.: CPU | RAM | Bateria | SSD | GPU) e que o delimitador seja ` | `.
- Garantir que falha em um módulo não derrube os demais e que o módulo com falha exiba `N/A`.

---

## 2. Tarefas Técnicas

| # | Tarefa | Detalhes |
|---|--------|----------|
| 1 | Adicionar GPUtil | Incluir `GPUtil` (e dependência `nvidia-ml-py` se necessário) em `requirements.txt`. |
| 2 | Módulo RAM | `src/modules/ram.py`: usar `psutil.virtual_memory().percent`; formato `RAM: X%`; em erro, `RAM: N/A`. |
| 3 | Módulo Bateria | `src/modules/battery.py`: usar `psutil.sensors_battery()` para percentual e status (power_plugged); ícones ⚡ (carregando), 🔋 (descarregando), 🔌 (conectado/cheia); temperatura via sensors se disponível; em sistema sem bateria ou erro, `N/A`. |
| 4 | Módulo Disco | `src/modules/disk.py`: uso do disco da montagem principal (ex.: `/` via `psutil.disk_usage('/')`); temperatura via `psutil.sensors_temperatures()` se houver entrada para disco; formato `SSD: X% 🌡️Y°C` ou `SSD: X%` se temp indisponível; em erro, `SSD: N/A`. Permitir configurar o caminho do disco (ex.: `disk_path` em config). |
| 5 | Módulo GPU | `src/modules/gpu.py`: usar GPUtil para obter primeira GPU NVIDIA (uso e temperatura); formato `GPU: X% 🌡️Y°C`; em ausência de GPU NVIDIA ou erro, `GPU: N/A`. Documentar no README que apenas NVIDIA é suportada nesta fase; AMD como melhoria futura. |
| 6 | Registro e ordem no core | Em `src/main.py`, registrar os novos módulos na ordem definida (CPU, RAM, Bateria, Disco, GPU); para cada um, verificar na config se está ativo; agregar saídas na mesma ordem com ` \| `. |
| 7 | Config por módulo | Estender `config.json` com flags ou opções por módulo (ex.: `ram`, `battery`, `disk`, `gpu`); opção para `disk_path` se implementado. |
| 8 | Tratamento de exceções | Cada módulo deve capturar exceções internamente e retornar string `N/A` para o próprio bloco (ex.: `GPU: N/A`), sem propagar exceção ao core. |

---

## 3. Arquivos a Criar ou Alterar

| Arquivo | Ação |
|---------|------|
| `requirements.txt` | Alterar (adicionar GPUtil) |
| `src/modules/ram.py` | Criar |
| `src/modules/battery.py` | Criar |
| `src/modules/disk.py` | Criar |
| `src/modules/gpu.py` | Criar |
| `src/main.py` | Alterar (registro e ordem dos módulos) |
| `config.json.example` | Alterar (incluir novos módulos) |
| `README.md` | Alterar (mencionar suporte NVIDIA apenas; AMD como futuro) |

---

## 4. Critérios de Sucesso

- [ ] Com todos os módulos de telemetria ativos, a saída segue o formato: `CPU: 42% 🌡️55°C | RAM: 68% | ⚡ 83% 🌡️32°C | SSD: 54% 🌡️45°C | GPU: 75% 🌡️68°C` (valores reais podem variar; ícones de bateria conforme estado).
- [ ] A ordem dos blocos na linha é fixa: CPU, RAM, Bateria, Disco, GPU.
- [ ] Cada módulo pode falhar isoladamente (ex.: desativar GPU ou remover NVIDIA): o bloco correspondente exibe `N/A` e os demais continuam normais.
- [ ] Em sistema sem bateria, o módulo de bateria exibe `N/A` ou é desativável via config sem quebrar a aplicação.
- [ ] README ou documentação em `docs/` deixa explícito que a GPU suportada nesta fase é apenas NVIDIA; AMD está planejada como melhoria futura.
