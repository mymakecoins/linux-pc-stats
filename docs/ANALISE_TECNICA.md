# Análise Técnica e Planejamento: Utilitário para a barra do sistema

**Versão:** 1.0
**Data:** 11/02/2026
**Autor:** Manus

## 1. Pesquisa de Bibliotecas e APIs

Esta seção detalha a pesquisa de tecnologias para implementar os requisitos do projeto.

### Análise e Recomendações

*   **Telemetria (CPU, RAM, Disco, Bateria):**
    *   **Biblioteca Recomendada:** `psutil`.
    *   **Justificativa:** É a solução mais completa e padrão da indústria para coletar informações de sistema em Python. É multiplataforma, robusta e fornece acesso à maioria dos dados necessários (uso de CPU, memória, disco, status da bateria) através de uma API unificada e simples.
    *   **Dependência Adicional:** Para a leitura de temperaturas (`psutil.sensors_temperatures()`), pode ser necessária a instalação do pacote `lm-sensors` no sistema Linux do usuário. Isso deve ser documentado no `README` e no script de instalação.

*   **Telemetria (GPU):**
    *   **Contexto:** A coleta de dados da GPU é altamente dependente do fabricante do hardware.
    *   **NVIDIA:** A biblioteca `GPUtil` é recomendada por ser uma camada de abstração simples sobre a `pynvml` (biblioteca oficial da NVIDIA), facilitando a obtenção de uso e temperatura.
    *   **AMD:** A coleta é mais fragmentada, geralmente envolvendo a leitura de arquivos de sistema em `/sys/class/drm/`.
    *   **Estratégia:** O desenvolvimento inicial focará no suporte para **NVIDIA** usando `GPUtil`. O suporte para **AMD** será tratado como um desafio técnico a ser explorado em uma fase posterior, para não bloquear o progresso inicial.

*   **API de Previsão do Tempo:**
    *   **Contexto:** Precisamos de uma forma de traduzir o CEP brasileiro para uma localidade e, em seguida, obter os dados climáticos para essa localidade.
    *   **APIs Recomendadas:**
        1.  **Brasil API (`https://brasilapi.com.br/` ):** Será usada para validar o CEP e convertê-lo em dados de cidade e estado. É uma API pública, gratuita e sem necessidade de chave.
        2.  **WeatherAPI.com:** Será usada para obter a previsão do tempo (temperatura e condição) a partir da cidade/estado retornada pela Brasil API. Possui um plano gratuito generoso que exige uma chave de API (API Key).
    *   **Justificativa da Combinação:** Essa abordagem de duas APIs é robusta. A Brasil API garante uma validação de CEP focada no Brasil, enquanto a WeatherAPI.com é um serviço global e confiável para dados climáticos.

## 2. Refinamento de Esforço e Análise de Riscos

Esta seção detalha a estimativa de esforço e os riscos identificados para cada fase do plano de ação.

*   **Fase 1 (Estrutura e Módulo CPU):**
    *   **Esforço:** Baixo.
    *   **Análise:** A biblioteca `psutil` simplifica muito esta fase. O principal ponto de atenção é documentar a dependência do `lm-sensors` para a leitura de temperatura.

*   **Fase 2 (Módulos de Telemetria Adicionais):**
    *   **Esforço:** Médio.
    *   **Análise:** Os módulos de RAM, Bateria e Disco são de baixo esforço com `psutil`. O esforço médio é atribuído ao **risco técnico** do módulo da **GPU**, especificamente para placas AMD, que exigirá uma pesquisa e implementação mais aprofundada.

*   **Fase 3 (Módulo de Previsão do Tempo):**
    *   **Esforço:** Baixo.
    *   **Análise:** A tarefa consiste em requisições HTTP e processamento de JSON, que são padrões em Python. O principal cuidado será no tratamento de erros, como APIs indisponíveis, CEP inválido ou chave de API incorreta.

*   **Fase 4 (Interface Gráfica de Configuração - GUI):**
    *   **Esforço:** Médio.
    *   **Análise:** A complexidade dependerá da biblioteca escolhida (`Tkinter` para simplicidade, `PyQt` para um visual mais moderno). O desafio principal é garantir que a interface seja intuitiva e que o mecanismo de salvar/carregar configurações seja confiável.

*   **Fase 5 (Integração com a barra do sistema e Empacotamento):**
    *   **Esforço:** Médio.
    *   **Análise:** Adaptar a saída para formatos como texto ou JSON é simples. O esforço está em criar um script de instalação (`install.sh`) e um arquivo de serviço (`.desktop`) robustos, que funcionem corretamente na inicialização do sistema e em diferentes ambientes de desktop.

## 3. Diagrama de Fluxo da Aplicação

O diagrama abaixo ilustra a arquitetura e o fluxo de dados da aplicação.

┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│   Usuário (GUI)   │─(1)─>│  Arquivo de Conf. │<─(2)─┤   Core Engine     │
└───────────────────┘      │    (config.json)  │      │    (main.py)      │
└───────────────────┘      └─────────┬─────────┘
│ (3)
┌────────────────────┼────────────────────┐
│ (Loop de Execução) │                    │
▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Módulo de       │    │ Módulo de       │    │ Módulo de       │
│ Telemetria      │    │ Previsão do     │    │ ... (outros)    │
│ (cpu, ram, etc) │    │ Tempo           │    └───────────────┘
└───────┬───────┘    └───────┬───────┘
│ (4)                │ (5)
▼                    ▼
┌───────────────┐    ┌───────────────┐
│   psutil /    │    │  Brasil API /   │
│   GPUtil      │    │  WeatherAPI     │
└───────────────┘    └───────────────┘
│                    │
└─────────┬──────────┘
│ (6)
▼
┌───────────────────┐
│ Formata Saída     │
└─────────┬─────────┘
│ (7)
▼
┌───────────────────┐
│ Barra do sistema  │
│ (polybar/waybar)  │
└───────────────────┘


### Legenda do Fluxo:
1.  O usuário interage com a **GUI** para definir suas preferências (CEP, módulos ativos). As configurações são salvas em um arquivo `config.json`.
2.  O **Core Engine** (`main.py`) lê o `config.json` na inicialização para saber quais módulos executar e com quais parâmetros.
3.  O **Core Engine** inicia um loop principal que, em intervalos definidos, chama os módulos que estão ativos na configuração.
4.  O **Módulo de Telemetria** usa bibliotecas como `psutil` e `GPUtil` para coletar dados do hardware.
5.  O **Módulo de Tempo** faz requisições às APIs externas (`Brasil API`, `WeatherAPI`) para obter os dados climáticos.
6.  O **Core Engine** recebe os dados de todos os módulos ativos e os organiza em uma única string formatada.
7.  A string final é impressa na saída padrão (`stdout`), que é então capturada e exibida pela **barra do sistema** (ex: Polybar, Waybar, barra do Gerenciador de Tarefas, i3status).

## 4. Formato da Saída para a barra do sistema

Para garantir uma exibição clara e consistente, a saída da aplicação será uma única linha de texto, com cada módulo de informação separado por um delimitador `|`. Ícones serão usados para melhorar a legibilidade.

### Estrutura Geral
`[Módulo 1] | [Módulo 2] | [Módulo 3] ...`

### Detalhamento por Módulo

*   **CPU:**
    *   **Formato:** `CPU: <uso>% 🌡️<temp>°C`
    *   **Exemplo:** `CPU: 42% 🌡️55°C`
    *   **Ícones:** `🌡️` (U+1F321) para temperatura.

*   **Memória RAM:**
    *   **Formato:** `RAM: <uso>%`
    *   **Exemplo:** `RAM: 68%`

*   **Bateria:**
    *   **Formato:** `<ícone> <carga>% 🌡️<temp>°C`
    *   **Exemplo (Carregando):** `⚡ 83% 🌡️32°C`
    *   **Exemplo (Descarregando):** `🔋 50% 🌡️30°C`
    *   **Exemplo (Cheia):** `🔌 100% 🌡️28°C`
    *   **Ícones:**
        *   `⚡` (U+26A1) para "carregando".
        *   `🔋` (U+1F50B) para "descarregando".
        *   `🔌` (U+1F50C) para "conectado na tomada/cheia".

*   **Disco (SSD):**
    *   **Formato:** `SSD: <uso>% 🌡️<temp>°C`
    *   **Exemplo:** `SSD: 54% 🌡️45°C`

*   **GPU:**
    *   **Formato:** `GPU: <uso>% 🌡️<temp>°C`
    *   **Exemplo:** `GPU: 75% 🌡️68°C`

*   **Previsão do Tempo:**
    *   **Formato:** `<ícone> <temp>°C`
    *   **Exemplo (Ensolarado):** `☀️ 23°C`
    *   **Exemplo (Nublado):** `☁️ 19°C`
    *   **Exemplo (Chuva):** `🌧️ 17°C`
    *   **Ícones:** Um mapa de ícones será criado para representar as condições climáticas mais comuns (ensolarado, parcialmente nublado, nublado, chuva, tempestade, neve).

### Exemplo de Saída Completa

Uma linha de saída final, com todos os módulos ativos, se pareceria com isto:

`CPU: 42% 🌡️55°C | RAM: 68% | ⚡ 83% 🌡️32°C | SSD: 54% 🌡️45°C | GPU: 75% 🌡️68°C | ☀️ 23°C`

### Tratamento de Erros
Se um módulo falhar ao obter seus dados (ex: API offline, sensor não encontrado), ele deverá exibir `N/A` para manter a consistência da formatação.

*   **Exemplo com erro no tempo:** `... | GPU: 75% 🌡️68°C | Tempo: N/A`
