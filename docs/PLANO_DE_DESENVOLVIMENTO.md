# Plano de Desenvolvimento: Utilitário para a barra do sistema

**Versão:** 1.0  
**Data:** 11/02/2026

---

## Resumo Executivo

O **Utilitário para a barra do sistema** (em inglês, Status Bar Utility) é uma aplicação modular em Python que exibe telemetria do sistema (CPU, RAM, GPU, disco, bateria) e previsão do tempo na **barra do sistema** (barra do Gerenciador de Tarefas ou Polybar/Waybar) de ambientes de desktop Linux. O desenvolvimento está organizado em **cinco fases** incrementais: primeiro a estrutura base e o módulo CPU; em seguida os demais módulos de telemetria; depois o módulo de previsão do tempo; em seguida a interface gráfica de configuração; e por fim a integração com a barra do sistema e o empacotamento (instalação e autostart). Cada fase entrega valor testável e mantém o código modular e alinhado aos requisitos e ao formato de saída definidos em [REQUISTOS.md](REQUISTOS.md) e [ANALISE_TECNICA.md](ANALISE_TECNICA.md).

---

## Fases do Plano

| Fase | Nome | Objetivo principal | Detalhamento |
|------|------|--------------------|---------------|
| 1 | Estrutura e CPU | Projeto modular, `config.json`, core loop e primeiro módulo (CPU) funcionando | [Fase 1 — Estrutura e CPU](FASE_1_ESTRUTURA_E_CPU.md) |
| 2 | Telemetria adicional | Módulos RAM, Bateria, Disco e GPU (NVIDIA com GPUtil) | [Fase 2 — Telemetria adicional](FASE_2_TELEMETRIA_ADICIONAL.md) |
| 3 | Previsão do tempo | CEP → Brasil API → WeatherAPI, módulo tempo na saída | [Fase 3 — Previsão do tempo](FASE_3_PREVISAO_DO_TEMPO.md) |
| 4 | GUI de configuração | Interface para CEP e ativar/desativar módulos, persistência em `config.json` | [Fase 4 — GUI de configuração](FASE_4_GUI_CONFIGURACAO.md) |
| 5 | Integração e empacotamento | Saída para Polybar/Waybar, `install.sh` e `.desktop` para autostart | [Fase 5 — Integração e empacotamento](FASE_5_INTEGRACAO_E_EMPACOTAMENTO.md) |

---

## Resumos pós-implementação

Após a implementação de cada fase, deve ser criado um arquivo de resumo no diretório `docs/`:

- **Fase 1:** [RESUMO_FASE_1.md](RESUMO_FASE_1.md) — o que foi feito, desafios e confirmação dos critérios de sucesso.
- **Fase 2:** [RESUMO_FASE_2.md](RESUMO_FASE_2.md)
- **Fase 3:** [RESUMO_FASE_3.md](RESUMO_FASE_3.md)
- **Fase 4:** [RESUMO_FASE_4.md](RESUMO_FASE_4.md)
- **Fase 5:** [RESUMO_FASE_5.md](RESUMO_FASE_5.md)

Esses arquivos devem ser criados somente quando a fase correspondente for concluída, documentando o que foi implementado, os desafios encontrados e a verificação de que os critérios de sucesso da fase foram atendidos.
