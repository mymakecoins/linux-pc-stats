# Fase 4: Interface Gráfica de Configuração

**Objetivo:** Oferecer uma interface gráfica para configurar o CEP e habilitar/desabilitar cada módulo (CPU, RAM, Bateria, Disco, GPU, Tempo), com persistência em `config.json` e confirmação ao salvar.

---

## 1. Objetivos da Fase

- Permitir que o usuário **configure o CEP** em um campo de texto e salve de forma persistente (histórias 2.1 e 3.1 de [REQUISTOS.md](REQUISTOS.md)).
- Permitir que o usuário **habilite ou desabilite cada módulo** (CPU, RAM, Bateria, Disco, GPU, Tempo) por meio de checkboxes (ou equivalente) e salve essas preferências.
- Garantir que as configurações sejam **gravadas em `config.json`** no mesmo formato e local esperados pelo core engine (pasta do projeto ou `~/.config/linux-stats/`), para que na próxima execução do core as opções e o CEP reflitam o que foi salvo.
- Exibir **mensagem de confirmação** após o usuário clicar em Salvar (história 2.1).
- Usar biblioteca de GUI simples e sem dependências pesadas; **Tkinter** é a opção recomendada na análise técnica.

---

## 2. Tarefas Técnicas

| # | Tarefa | Detalhes |
|---|--------|----------|
| 1 | Escolha da biblioteca | Usar Tkinter (incluído no Python padrão) para evitar dependências extras. |
| 2 | Estrutura da GUI | Uma janela com: campo CEP (Entry); checkboxes para CPU, RAM, Bateria, Disco, GPU, Tempo; botão "Salvar"; opcionalmente botão "Fechar". |
| 3 | Leitura da config | Ao abrir a janela, carregar `config.json` do local definido no projeto (mesmo que o core use); preencher campo CEP e estado dos checkboxes com os valores atuais. Se o arquivo não existir, usar valores padrão (ex.: todos os módulos ativos, CEP vazio). |
| 4 | Validação de CEP | Validação básica de formato (ex.: 8 dígitos, com ou sem hífen). Não bloquear salvamento; pode exibir aviso se formato inválido e ainda assim salvar. Opcional: chamar Brasil API para validar ao salvar. |
| 5 | Escrita da config | Ao clicar em Salvar: montar o dicionário/estrutura equivalente ao `config.json` esperado pelo core (módulos ativos, cep, weather_api_key se já existir, interval_seconds, etc.); escrever no mesmo caminho de onde foi lido; criar diretório/pasta se necessário. |
| 6 | Confirmação | Após gravar com sucesso, exibir mensagem (messagebox ou label): "Configurações salvas com sucesso." ou similar. |
| 7 | Ponto de entrada da GUI | Script ou comando dedicado para abrir apenas a GUI, ex.: `python -m src.gui` ou `python -m src.config_ui`, ou executável `configure-statusbar.py` na raiz. Não iniciar o loop do core ao abrir a GUI. |
| 8 | Localização do config | Alinhar com o que o core usa: se o core lê de `~/.config/linux-stats/config.json`, a GUI deve ler e escrever no mesmo path; documentar no README. |

---

## 3. Arquivos a Criar ou Alterar

| Arquivo | Ação |
|---------|------|
| `src/gui/__init__.py` | Criar |
| `src/gui/config_window.py` (ou `src/config_ui.py`) | Criar — janela principal com CEP, checkboxes e botão Salvar |
| `src/main.py` | Não é obrigatório alterar; a GUI apenas escreve no mesmo `config.json` que o main lê |
| `config.json` / exemplo | A estrutura escrita pela GUI deve ser compatível com a já definida nas fases anteriores |
| `README.md` | Alterar — como abrir a GUI de configuração (comando ou atalho) |

---

## 4. Critérios de Sucesso

- [ ] O usuário consegue abrir a interface gráfica (via comando definido no README).
- [ ] O usuário consegue inserir ou alterar o CEP no campo apropriado e clicar em Salvar; o CEP é armazenado de forma persistente no `config.json`.
- [ ] O usuário consegue marcar/desmarcar cada módulo (CPU, RAM, Bateria, Disco, GPU, Tempo) e salvar; na próxima execução do core, as informações exibidas na barra do sistema refletem apenas os módulos habilitados.
- [ ] Uma mensagem de confirmação é exibida após Salvar com sucesso.
- [ ] As preferências são mantidas entre reinicializações do sistema (persistência no mesmo arquivo que o core lê).
- [ ] Critérios de aceite das histórias 2.1 (Configurar Localização) e 3.1 (Gerenciar Módulos) de [REQUISTOS.md](REQUISTOS.md) estão atendidos.
