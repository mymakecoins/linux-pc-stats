# Documento de Requisitos de Software: Utilitário para a barra do sistema

**Versão:** 1.0
**Data:** 11/02/2026
**Autor:** Manus (Analista de Requisitos Sênior)

## 1. Visão Geral e Objetivos de Negócio

O projeto **Utilitário para a barra do sistema** (em inglês, Status Bar Utility) visa desenvolver uma aplicação para sistemas operacionais baseados em Ubuntu que enriqueça a **barra do sistema** (barra do Gerenciador de Tarefas, próximo ao relógio e ícones) com informações contextuais e em tempo real.

O objetivo principal é fornecer ao usuário acesso rápido e conveniente a dados vitais do sistema e informações externas úteis, eliminando a necessidade de abrir múltiplos aplicativos ou terminais. A aplicação deve ser discreta, eficiente e altamente configurável para atender às necessidades individuais de cada usuário.

### Valor de Negócio:
*   **Aumento de Produtividade:** Centraliza informações importantes, reduzindo a troca de contexto e economizando tempo.
*   **Monitoramento Proativo:** Permite ao usuário observar a saúde e o desempenho do seu sistema de forma passiva, podendo identificar problemas (como superaquecimento ou falta de bateria) antes que se tornem críticos.
*   **Experiência do Usuário Aprimorada:** Oferece uma experiência de desktop mais rica e personalizada.

## 2. Escopo do Produto

### Funcionalidades Incluídas (MVP - Minimum Viable Product):
*   Coleta e exibição de telemetria de hardware (CPU, RAM, Bateria, SSDs, GPU).
*   Coleta e exibição de previsão do tempo com base no CEP do usuário.
*   Interface gráfica para configuração dos módulos e do CEP.
*   Saída de dados em formato de texto e ícones simples para a barra do sistema.

### Funcionalidades Excluídas (Fora do Escopo Inicial):
*   Suporte a múltiplos provedores de previsão do tempo.
*   Temas visuais avançados ou customização de CSS na GUI.
*   Notificações de alerta (ex: "Bateria fraca!").
*   Suporte a outras distribuições Linux que não sejam baseadas em Ubuntu.
*   Plugins ou extensões de terceiros.

## 3. Requisitos Funcionais (Histórias de Usuário)

---

### **Épico 1: Monitoramento de Telemetria do Sistema**
*Como um usuário avançado, eu quero visualizar a telemetria do meu hardware diretamente na barra do sistema para poder monitorar a saúde e o desempenho do meu computador em tempo real.*

**História de Usuário 1.1: Visualizar Uso da CPU**
> **Eu, como usuário, quero ver o percentual de uso e a temperatura da minha CPU** para poder identificar gargalos de processamento ou problemas de superaquecimento.

**Critérios de Aceite:**
*   **Dado que** o módulo de CPU está ativo,
*   **Quando** a aplicação atualiza os dados de telemetria,
*   **Então** a barra do sistema deve exibir o uso atual da CPU em percentual (ex: "CPU: 42%").
*   **E** a barra do sistema deve exibir a temperatura atual da CPU em graus Celsius (ex: "🌡️ 55°C").

**História de Usuário 1.2: Visualizar Uso da Memória RAM**
> **Eu, como usuário, quero ver o percentual de uso da minha memória RAM** para saber se preciso fechar aplicações ou se estou perto de atingir o limite.

**Critérios de Aceite:**
*   **Dado que** o módulo de RAM está ativo,
*   **Quando** a aplicação atualiza os dados de telemetria,
*   **Então** a barra do sistema deve exibir o uso atual da RAM em percentual (ex: "RAM: 68%").

**História de Usuário 1.3: Visualizar Status da Bateria**
> **Eu, como usuário de notebook, quero ver o percentual de carga e a temperatura da minha bateria** para poder gerenciar meu tempo de uso fora da tomada e monitorar a saúde da bateria.

**Critérios de Aceite:**
*   **Dado que** o módulo de Bateria está ativo e o dispositivo possui uma bateria,
*   **Quando** a aplicação atualiza os dados de telemetria,
*   **Então** a barra do sistema deve exibir o percentual de carga restante (ex: "BAT: 83%").
*   **E** um ícone deve indicar se a bateria está carregando, descarregando ou cheia.
*   **E** a barra do sistema deve exibir a temperatura da bateria (ex: "🌡️ 32°C").

**História de Usuário 1.4: Visualizar Uso dos Discos (SSDs)**
> **Eu, como usuário, quero ver o percentual de uso e a temperatura dos meus SSDs** para gerenciar meu espaço de armazenamento e garantir que não estão superaquecendo.

**Critérios de Aceite:**
*   **Dado que** o módulo de Disco está ativo,
*   **Quando** a aplicação atualiza os dados de telemetria,
*   **Então** a barra do sistema deve exibir o percentual de espaço utilizado do disco principal (ex: "SSD: 54%").
*   **E** a barra do sistema deve exibir a temperatura do disco (ex: "🌡️ 45°C").

**História de Usuário 1.5: Visualizar Uso da Placa de Vídeo (GPU)**
> **Eu, como usuário, quero ver o percentual de uso e a temperatura da minha GPU** para monitorar o desempenho durante jogos ou tarefas de renderização.

**Critérios de Aceite:**
*   **Dado que** o módulo de GPU está ativo e uma GPU compatível (NVIDIA/AMD) está presente,
*   **Quando** a aplicação atualiza os dados de telemetria,
*   **Então** a barra do sistema deve exibir o uso atual da GPU em percentual (ex: "GPU: 75%").
*   **E** a barra do sistema deve exibir a temperatura da GPU (ex: "🌡️ 68°C").

---

### **Épico 2: Exibição da Previsão do Tempo**
*Como um usuário, eu quero ver a previsão do tempo da minha cidade na barra do sistema para me planejar para o dia sem precisar abrir um site ou aplicativo específico.*

**História de Usuário 2.1: Configurar Localização**
> **Eu, como usuário, quero poder inserir e salvar meu CEP através de uma interface gráfica** para que a aplicação saiba para qual localidade buscar a previsão do tempo.

**Critérios de Aceite:**
*   **Dado que** eu abri a janela de configurações,
*   **Quando** eu insiro um CEP válido no campo apropriado e clico em "Salvar",
*   **Então** o CEP deve ser armazenado de forma persistente no meu sistema.
*   **E** uma mensagem de confirmação deve ser exibida.

**História de Usuário 2.2: Visualizar Tempo Atual**
> **Eu, como usuário, quero ver a temperatura atual e um ícone representando a condição do tempo** para ter uma noção rápida do clima lá fora.

**Critérios de Aceite:**
*   **Dado que** o módulo de Tempo está ativo e um CEP válido foi configurado,
*   **Quando** a aplicação atualiza os dados de tempo,
*   **Então** a barra do sistema deve exibir a temperatura atual em graus Celsius (ex: "23°C").
*   **E** um ícone correspondente à condição climática (ex: ☀️ para ensolarado, ☁️ para nublado, 🌧️ para chuva) deve ser exibido ao lado da temperatura.

---

### **Épico 3: Configuração da Aplicação**
*Como um usuário, eu quero ter uma interface gráfica simples para configurar quais informações são exibidas, para que eu possa personalizar a aplicação de acordo com minhas preferências.*

**História de Usuário 3.1: Gerenciar Módulos**
> **Eu, como usuário, quero poder habilitar ou desabilitar cada módulo de informação (CPU, RAM, Tempo, etc.) individualmente** através de uma interface gráfica.

**Critérios de Aceite:**
*   **Dado que** eu abri a janela de configurações,
*   **Quando** eu marco ou desmarco a caixa de seleção de um módulo (ex: "CPU") e salvo as alterações,
*   **Então** a informação correspondente deve aparecer ou desaparecer da barra do sistema na próxima atualização.
*   **E** essa preferência deve ser salva e mantida entre as reinicializações do sistema.

## 4. Requisitos Não-Funcionais

*   **Desempenho:** A aplicação deve ter um consumo de recursos (CPU e RAM) mínimo para não impactar o desempenho geral do sistema. A coleta de dados deve ser otimizada e ocorrer nos intervalos definidos (telemetria a cada minuto, tempo a cada hora).
*   **Confiabilidade:** A aplicação deve ser resiliente a falhas. Em caso de falha na coleta de um dado (ex: API de tempo indisponível), o módulo correspondente deve exibir um estado de erro (ex: "Tempo: N/A") sem travar o restante da aplicação.
*   **Usabilidade:** A interface de configuração deve ser intuitiva e acessível, não exigindo conhecimento técnico para sua operação.
*   **Manutenibilidade:** O código-fonte deve ser modular, bem documentado e seguir as melhores práticas de desenvolvimento em Python para facilitar futuras atualizações e a adição de novos módulos.
