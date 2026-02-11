# Resumo da Fase 3: Previsão do Tempo

**Data de conclusão:** 11/02/2026

## O que foi feito

- **Módulo weather** (`src/modules/weather.py`):
  - **Brasil API:** GET `https://brasilapi.com.br/api/cep/v1/{cep}` para obter cidade e estado; CEP aceito com ou sem hífen; validação de 8 dígitos.
  - **WeatherAPI.com:** GET `https://api.weatherapi.com/v1/current.json?key=...&q=city,state` para temperatura atual (°C) e código de condição.
  - **Mapa de ícones:** mapeamento dos códigos de condição da WeatherAPI para emojis (☀️ ensolarado, ⛅ parcialmente nublado, ☁️ nublado, 🌧️ chuva, ⛈️ tempestade, ❄️ neve, 🌫️ neblina); condição desconhecida usa ☀️.
  - **Cache:** última resposta e timestamp armazenados em variável de módulo; novas requisições só após decorrido `weather_interval_seconds` (default 3600). Nos ciclos intermediários é reutilizado o último valor válido.
  - **Config:** leitura de `cep` (ou `weather_cep`), `weather_api_key` (ou `weatherapi_key`) e `weather_interval_seconds` (opcional, default 3600).
  - **Erros:** falhas de rede, CEP inválido, chave incorreta ou resposta inválida retornam `Tempo: N/A`; exceções tratadas com log em debug.
- **HTTP:** uso de `urllib.request` da biblioteca padrão (sem nova dependência).
- **main.py:** registro do módulo `weather` após GPU; ordem da linha: ... | GPU | <tempo>.
- **config.json.example e config.json:** inclusão de `weather` em `modules`, `cep`, `weather_api_key` e `weather_interval_seconds`.
- **README.md:** seção "Previsão do tempo", instruções para obter API Key no WeatherAPI.com e como preencher CEP; documentação dos novos campos do config.

## Desafios encontrados

- Nenhum bloqueador. A Brasil API retorna `city` e `state` (ou `localidade` e `estado`); o código trata ambos os formatos. O cache com `time.monotonic()` garante que o intervalo seja respeitado mesmo com o loop de telemetria em intervalo menor.

## Critérios de sucesso atendidos

- [x] Com CEP válido e API Key válida, a barra do sistema exibe temperatura e ícone no formato `<ícone> <temp>°C` (ex.: `☀️ 23°C`, `☁️ 19°C`).
- [x] O ícone reflete a condição climática conforme mapeamento (ensolarado, nublado, chuva, etc.).
- [x] Em caso de erro (API fora, CEP inválido, chave errada), a saída exibe `Tempo: N/A` e a aplicação continua rodando.
- [x] A atualização dos dados do tempo não ocorre a cada ciclo de telemetria; ocorre no máximo a cada `weather_interval_seconds` (ex.: 1 hora).
- [x] O README explica onde obter a API Key da WeatherAPI e como preencher o CEP no config.
