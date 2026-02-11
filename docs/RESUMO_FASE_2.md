# Resumo da Fase 2: Módulos de Telemetria Adicionais

**Data de conclusão:** 11/02/2026

## O que foi feito

- **requirements.txt:** Adicionado `GPUtil>=1.4.0` para suporte a GPU NVIDIA.
- **BaseModule:** Incluída propriedade `fallback_label` (padrão: `name.upper()`) para exibir "X: N/A" em falhas; módulo battery usa "Bateria".
- **Módulo RAM** (`src/modules/ram.py`): `psutil.virtual_memory().percent`; saída `RAM: X%`; em erro `RAM: N/A`.
- **Módulo Bateria** (`src/modules/battery.py`): `psutil.sensors_battery()` para percentual e `power_plugged`; ícones ⚡ (carregando), 🔋 (descarregando), 🔌 (cheia); temperatura da bateria quando disponível em sensores; em sistema sem bateria ou erro `Bateria: N/A`.
- **Módulo Disco** (`src/modules/disk.py`): `psutil.disk_usage(path)` com path configurável via `config["disk_path"]` ou `config["disk"]["path"]` (padrão `"/"`); temperatura de disco quando disponível (nvme, drivetemp, etc.); saída `SSD: X% 🌡️Y°C` ou `SSD: X%`; em erro `SSD: N/A`.
- **Módulo GPU** (`src/modules/gpu.py`): GPUtil para primeira GPU NVIDIA (load e temperatura); saída `GPU: X% 🌡️Y°C`; sem NVIDIA ou em erro `GPU: N/A`. AMD fora do escopo (documentado como melhoria futura).
- **main.py:** Registrados os módulos na ordem fixa CPU, RAM, Bateria, Disco, GPU; uso de `fallback_label` na captura de exceções.
- **config.json.example e config.json:** Incluídos `ram`, `battery`, `disk`, `gpu` e `disk_path` (opcional).
- **README.md:** Documentados os módulos em `modules`, opção `disk_path` e nota de que apenas GPU NVIDIA é suportada; AMD como melhoria futura.

## Desafios encontrados

- Nenhum bloqueador. Em máquinas sem NVIDIA, o módulo GPU retorna `GPU: N/A` normalmente. GPUtil é importado apenas dentro de `gpu.py` na função de coleta, evitando falha de import em sistemas sem driver NVIDIA.

## Critérios de sucesso atendidos

- [x] Com todos os módulos de telemetria ativos, a saída segue o formato esperado (ex.: `CPU: 7% 🌡77°C | RAM: 64% | 🔋 99% | SSD: 26% 🌡30°C | GPU: N/A`), com ícones de bateria conforme estado.
- [x] Ordem dos blocos fixa: CPU, RAM, Bateria, Disco, GPU.
- [x] Cada módulo pode falhar isoladamente (ex.: GPU sem NVIDIA); o bloco correspondente exibe `N/A` e os demais seguem normais.
- [x] Em sistema sem bateria, o módulo de bateria exibe `Bateria: N/A`.
- [x] README deixa explícito que a GPU suportada nesta fase é apenas NVIDIA; AMD está planejada como melhoria futura.
