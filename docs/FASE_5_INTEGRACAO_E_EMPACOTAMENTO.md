# Fase 5: Integração com a barra do sistema e Empacotamento

**Objetivo:** Garantir que a saída da aplicação seja consumível por Polybar e Waybar (uma linha em stdout), fornecer script de instalação e arquivo .desktop para autostart, e documentar o uso na barra do sistema.

---

## 1. Objetivos da Fase

- Confirmar que a aplicação imprime **uma única linha** por ciclo em **stdout**, no formato já definido (módulos separados por ` | `), para que Polybar/Waybar possam executá-la como módulo customizado e exibir o texto.
- Fornecer **script de instalação** (`install.sh`) que prepare o ambiente (dependências do sistema se necessário, Python, venv, `pip install -r requirements.txt`, e opcionalmente instalar/copiar o executável ou atalhos).
- Fornecer **arquivo .desktop** para que o usuário possa colocar em autostart e a aplicação (loop da barra do sistema) inicie no login, se desejado.
- **Documentar** no README e, se útil, em `docs/INTEGRACAO_BARRA_STATUS.md`, como configurar um módulo na Polybar e na Waybar que execute o script Python e exiba a saída na barra do sistema.
- Respeitar ambientes (dev/test/prod): não simular dados em produção; uso de config e variáveis de ambiente conforme já definido.

---

## 2. Tarefas Técnicas

| # | Tarefa | Detalhes |
|---|--------|----------|
| 1 | Verificação da saída | Garantir que o core não imprima logs ou mensagens extras em stdout (apenas a linha de status); logs de diagnóstico podem ir para stderr ou arquivo. |
| 2 | Documentação Polybar | Exemplo de bloco em `config` do Polybar: módulo `type = custom/script` (ou equivalente) que executa o comando Python (ex.: `python /caminho/para/src/main.py` ou script wrapper) e exibe `tail = true` se necessário para atualização contínua. |
| 3 | Documentação Waybar | Exemplo de módulo custom em Waybar que chama o mesmo script e exibe o retorno (format conforme Waybar). |
| 4 | Script `install.sh` | Verificar Python 3; opcional: criar venv no diretório do projeto ou em `~/.local`; instalar dependências com `pip install -r requirements.txt`; mencionar dependência de sistema `lm-sensors` se ainda não documentado; opcional: copiar `.desktop` para `~/.config/autostart/` ou indicar que o usuário faça isso manualmente. Script deve ser idempotente e informativo (mensagens claras). |
| 5 | Arquivo .desktop | Criar `linux-stats-statusbar.desktop` (ou nome equivalente): `Exec` apontando para o script Python ou wrapper que inicia o core (ex.: `python -m src`); `Type=Application`; opcionalmente `Hidden=false`, `X-GNOME-Autostart-enabled=true`; comentar que para uso na barra do sistema o usuário geralmente não inicia o app via .desktop e sim via config da Polybar/Waybar; o .desktop pode servir para "iniciar em background" em alguns setups. |
| 6 | README | Seção "Integração com a barra do sistema" com links ou conteúdo de como configurar Polybar e Waybar; instruções de instalação usando `install.sh`; onde fica o `config.json` e como abrir a GUI. |
| 7 | Opcional: INTEGRACAO_BARRA_STATUS.md | Em `docs/`, arquivo dedicado com exemplos de configuração completos (trechos de config da Polybar e Waybar) e troubleshooting (ex.: caminho do Python, venv). |

---

## 3. Arquivos a Criar ou Alterar

| Arquivo | Ação |
|---------|------|
| `README.md` | Alterar — seção de integração com a barra do sistema, instalação, uso do .desktop |
| `install.sh` | Criar — script de instalação (executável, com shebang) |
| `linux-stats-statusbar.desktop` (ou similar) | Criar — entrada para autostart/execução |
| `docs/INTEGRACAO_BARRA_STATUS.md` | Criar (opcional) — exemplos Polybar/Waybar e dicas |

Se o core imprimir algo além da linha em stdout (ex.: debug), ajustar `src/main.py` para redirecionar logs para stderr ou desativar em produção.

---

## 4. Critérios de Sucesso

- [ ] A instalação via `install.sh` deixa o ambiente utilizável (Python, dependências instaladas; usuário consegue rodar `python -m src` ou o comando documentado).
- [ ] O usuário consegue colar um bloco de configuração na Polybar ou Waybar (documentado no README ou em `docs/INTEGRACAO_BARRA_STATUS.md`) e ver a linha de status atualizando conforme o intervalo configurado.
- [ ] A aplicação não imprime nada além da linha de status em stdout (uma linha por ciclo).
- [ ] O arquivo .desktop está disponível e documentado; quando usado em autostart (se aplicável ao fluxo desejado), a aplicação inicia no login sem erros evidentes (ou documentar que o uso típico é via integração na barra, não via autostart separado).
- [ ] README contém instruções claras de instalação, execução e integração com a barra do sistema.
