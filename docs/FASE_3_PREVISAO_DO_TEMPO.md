# Fase 3: Previsão do Tempo

**Objetivo:** Implementar o módulo de previsão do tempo com CEP → Brasil API → WeatherAPI.com, saída no formato `<ícone> <temp>°C`, mapa de ícones por condição climática e atualização em intervalo maior (ex.: 1 hora) para respeitar requisitos não-funcionais.

---

## 1. Objetivos da Fase

- Obter localidade (cidade/estado) a partir do CEP via **Brasil API**.
- Obter temperatura e condição do tempo para essa localidade via **WeatherAPI.com** (API Key configurável).
- Exibir na barra do sistema no formato `<ícone> <temp>°C`, com ícone conforme condição (ensolarado, nublado, chuva, etc.).
- Implementar cache/intervalo de atualização do tempo (ex.: 1 hora) distinto do intervalo de telemetria (ex.: 1 minuto), para não sobrecarregar as APIs e atender ao requisito de desempenho.
- Em caso de erro (API indisponível, CEP inválido, chave incorreta), exibir `Tempo: N/A` sem travar a aplicação.

---

## 2. Tarefas Técnicas

| # | Tarefa | Detalhes |
|---|--------|----------|
| 1 | Módulo weather | Criar `src/modules/weather.py`: obter CEP e API Key da config; chamar Brasil API para CEP → cidade/estado; chamar WeatherAPI.com com cidade/estado (ou lat/lon se preferir) para condição e temperatura atual. |
| 2 | Brasil API | GET `https://brasilapi.com.br/api/cep/v1/{cep}`; extrair localidade (ex.: `city`, `state`); tratar 404 ou resposta inválida (CEP inválido). |
| 3 | WeatherAPI.com | Usar endpoint de "current" (ex.: `https://api.weatherapi.com/v1/current.json`); parâmetros: `key`, `q` (cidade, estado ou lat,lon). Extrair temperatura em °C e código/texto de condição. |
| 4 | Mapa de ícones | Mapear códigos ou textos de condição da WeatherAPI para emojis: ☀️ (ensolarado), ☁️ (nublado), 🌧️ (chuva), etc., conforme tabela na [ANALISE_TECNICA.md](ANALISE_TECNICA.md). Condição desconhecida: ícone genérico (ex.: 🌡️ ou ☀️). |
| 5 | Cache e intervalo | Manter última resposta e timestamp no módulo; só refazer requisições após decorrido o intervalo de tempo configurado (ex.: `weather_interval_seconds: 3600`). Nos ciclos intermediários, reutilizar último valor válido. |
| 6 | Config | Adicionar em `config.json`: `cep`, `weather_api_key`, `weather_interval_seconds` (opcional, default 3600). |
| 7 | Integração no core | Registrar módulo "weather" em `src/main.py` após os módulos de telemetria; ordem da linha: ... \| GPU \| <tempo>. Em falha ou dados indisponíveis, saída `Tempo: N/A`. |
| 8 | Tratamento de erros | Capturar exceções de rede, timeout, JSON inválido, API key inválida; retornar `Tempo: N/A` e opcionalmente logar em stderr ou arquivo para diagnóstico. |
| 9 | Dependência HTTP | Usar `urllib.request` da biblioteca padrão ou adicionar `requests` em `requirements.txt`; documentar no README a necessidade de obter API Key no WeatherAPI.com e o formato do CEP. |

---

## 3. Arquivos a Criar ou Alterar

| Arquivo | Ação |
|---------|------|
| `src/modules/weather.py` | Criar |
| `src/main.py` | Alterar (registro do módulo tempo e intervalo diferenciado) |
| `config.json.example` | Alterar (cep, weather_api_key, weather_interval_seconds) |
| `README.md` | Alterar (instruções para obter API Key e configurar CEP) |
| `requirements.txt` | Alterar (se usar `requests`) |

---

## 4. Critérios de Sucesso

- [ ] Com CEP válido e API Key válida da WeatherAPI, a barra do sistema exibe algo como `☀️ 23°C` ou `☁️ 19°C`, conforme condição real.
- [ ] O ícone reflete a condição climática (ensolarado, nublado, chuva, etc.) conforme mapeamento definido.
- [ ] Em caso de erro (API fora, CEP inválido, chave errada), a saída exibe `Tempo: N/A` e a aplicação continua rodando.
- [ ] A atualização dos dados de tempo não ocorre a cada ciclo de telemetria; ocorre no máximo a cada `weather_interval_seconds` (ex.: 1 hora).
- [ ] O README explica onde obter a API Key da WeatherAPI e como preencher o CEP no config.
