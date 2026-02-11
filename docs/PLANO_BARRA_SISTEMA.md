# Plano: Exibir dados na barra do sistema (próximo ao relógio e ícones)

**Objetivo:** Exibir a saída do **Utilitário para a barra do sistema** (linux-stats) na **barra do Gerenciador de Tarefas / barra do sistema** do ambiente de desktop, alinhada à direita, próxima aos ícones de sistema e ao relógio (em vez de, ou além de, Polybar/Waybar).

---

## 1. Escopo da mudança

- **Fonte de dados:** A aplicação atual não precisa mudar: ela continua imprimindo **uma linha por ciclo** em stdout (ex.: `CPU: 20% 🌡82°C | RAM: 65% | ...`). Essa linha é a entrada para qualquer barra.
- **O que muda:** O **destino** da exibição. Em vez de (ou além de) configurar Polybar/Waybar, o usuário configura a **barra nativa** do ambiente de desktop (GNOME, KDE, XFCE, etc.) para executar o comando e mostrar o texto à direita, perto do relógio e dos ícones.

---

## 2. Dependência do ambiente de desktop

A forma de “colar” esse texto na barra do sistema depende do **ambiente de desktop**:

| Ambiente | Barra típica | Como exibir nosso texto |
|----------|----------------|--------------------------|
| **GNOME (Ubuntu padrão)** | Barra superior (top bar) com relógio e ícones à direita | **Extensão GNOME Shell**: um pequeno script/extension que executa `linux-stats-statusbar` (ou lê de um pipe/arquivo) e exibe o resultado em um label no painel. Não há “módulo de script” nativo; precisa de extensão. |
| **KDE Plasma** | Painel inferior ou superior | **Widget / Plasmoid**: applet que executa o comando em intervalo e atualiza um label. Ou uso do widget “Command Output” / similar se existir. |
| **XFCE** | Painel (panel) | **Plugin “Generic Monitor”**: permite comando + intervalo e exibe a saída no painel. Nossa aplicação pode ser chamada com `timeout` + `head -1` a cada N segundos, ou um script wrapper que imprime uma linha e sai. |
| **MATE** | Painel | **Applet “Generic Monitor”** ou similar. |
| **Outros (i3, Sway sem barra nativa)** | Normalmente usa Polybar/Waybar | Manter documentação atual (Polybar/Waybar). |

---

## 3. Pergunta crítica para o plano

**Qual ambiente de desktop você está usando?**

- Se for **GNOME** (Ubuntu padrão, Fedora, etc.): o plano será criar (ou indicar) uma **extensão GNOME Shell** que rode `linux-stats-statusbar` e mostre o texto à direita na top bar.
- Se for **KDE Plasma**: o plano será um **widget de painel** (Plasmoid) ou documentar uso de um applet existente que execute comando e mostre a saída.
- Se for **XFCE**: o plano será **documentar** o uso do plugin “Generic Monitor” (ou equivalente) com nosso comando, sem alterar o código da aplicação.

Assim que você informar o ambiente (ex.: “GNOME” ou “Ubuntu com barra padrão”), o próximo passo é:

1. **Documentar** no repositório como integrar nessa barra (passo a passo + exemplo de config ou script).
2. **Se for GNOME:** avaliar se faz sentido fornecer um esqueleto de extensão GNOME Shell no repositório (JavaScript) que apenas execute `/usr/bin/linux-stats-statusbar` e mostre a linha à direita, próximo ao relógio.

---

## 4. O que não muda

- **Aplicação Python:** Continua igual: `linux-stats-statusbar` (ou `run-statusbar.sh`) em loop, imprimindo uma linha em stdout a cada intervalo.
- **Config:** Continua em `~/.config/linux-stats/config.json`.
- **Formato da linha:** O mesmo (módulos separados por ` | `).

---

## 5. Próximos passos (após definir o ambiente)

1. **Você informa:** “Uso GNOME” ou “Uso KDE” ou “Uso XFCE”.
2. **Plano detalhado:** Será criada uma seção (ou arquivo) específico para esse ambiente com:
   - requisitos (extensão, widget ou plugin);
   - como instalar/configurar;
   - como posicionar à direita, próximo aos ícones e ao relógio;
   - lembrete de reiniciar a sessão ou a barra após configurar.
3. **README / INTEGRACAO:** Inclusão de um link ou seção “Barra do sistema (GNOME/KDE/XFCE)” apontando para esse plano/instruções.

Se quiser, responda apenas com o nome do ambiente (ex.: **GNOME**) para eu detalhar o plano e os passos de configuração para a barra do Gerenciador de Tarefas alinhada à direita, próxima aos ícones e ao relógio.
