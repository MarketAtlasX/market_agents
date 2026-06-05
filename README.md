# market_agents

MarketAtlas `market_agents` contains three lightweight Python agents plus a local FastAPI microservices layer.

- Impact Analysis Agent: extracts simple relations from text and computes a composite risk index.
- Market Data Agent: computes momentum, 14-day rolling volatility, and volume status.
- Recommendation Agent: combines impact and market signals into BUY/HOLD/SELL decisions.

## Quick Demo

Run from inside `market_agents`:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Microservices

The service layer keeps the existing agent code intact and exposes it through separate FastAPI apps:

| Service | Module | Port | Main endpoint |
| --- | --- | ---: | --- |
| Gateway | `market_agents.services.gateway:app` | 8000 | `POST /analyze` |
| Market data | `market_agents.services.market_service:app` | 8001 | `POST /snapshot` |
| Impact | `market_agents.services.impact_service:app` | 8002 | `POST /impact` |
| Recommendation | `market_agents.services.recommendation_service:app` | 8003 | `POST /recommendation` |

Every service exposes:

- `GET /health` for probes.
- `GET /metrics` for Prometheus scraping.
- OpenAPI at `/openapi.json` and Swagger UI at `/docs`.

Start all local services:

```powershell
.\scripts\run_local_services.ps1
```

Example gateway request:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/analyze `
  -ContentType 'application/json' `
  -Body '{"text":"CountryA launched a strike on FactoryB.","prices":[100,101,102,103,104,105,106,107,108,109,110,111,112,113,114],"volumes":[100,100,100,100,100,100,100,100,100,100,100,100,100,100,160]}'
```

## Observability

- OpenTelemetry FastAPI instrumentation is enabled for all services.
- Critical code paths are wrapped with spans and Prometheus histograms:
  - `market.snapshot`
  - `impact.pipeline`
  - `recommendation.decide`
  - `gateway.analyze`
- Prometheus metrics are exposed through `/metrics`.
- Logs are structured JSON on stdout, ready for Grafana Loki, ELK, or another collector.
- OTLP trace export is enabled when `OTEL_EXPORTER_OTLP_ENDPOINT` is set.

Recommended local aggregation path:

1. Prometheus scrapes each service's `/metrics`.
2. Promtail or Vector ships service stdout JSON logs to Grafana Loki.
3. OpenTelemetry Collector receives OTLP traces and exports to Tempo, Jaeger, or another tracing backend.

## Gateway Resilience

The gateway includes:

- SlowAPI rate limiting.
- Circuit breakers around downstream calls to market, impact, and recommendation services.
- Environment-configurable downstream URLs:
  - `MARKET_SERVICE_URL`
  - `IMPACT_SERVICE_URL`
  - `RECOMMENDATION_SERVICE_URL`
  - `RATE_LIMIT`
  - `ANALYZE_RATE_LIMIT`

## Contracts

Generated contracts live under `docs/`:

- `docs/openapi/gateway.openapi.json`
- `docs/openapi/market-data.openapi.json`
- `docs/openapi/impact.openapi.json`
- `docs/openapi/recommendation.openapi.json`
- `docs/events/agent-event.schema.json`

Regenerate them:

```powershell
$env:PYTHONPATH=(Split-Path (Resolve-Path .))
.\.venv\Scripts\python.exe scripts\generate_contracts.py
```

## Ingest Cache

Create `market_agents/.env` with API keys if available:

```text
ALPHAVANTAGE_API_KEY=your_key_here
FRED_API_KEY=your_key_here
EIA_API_KEY=your_key_here
```

Run the cache fetch:

```powershell
python -m market_agents.ingest.cache
```

If keys are missing, the helpers return deterministic fallback data so demos and tests remain runnable.

## Tests

Run from inside `market_agents`:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -q -s tests
```

## Microservices Plan

1. Keep the current services as independently deployable FastAPI apps.
2. Move service-to-service calls from direct HTTP defaults to service discovery or a gateway mesh when deployed.
3. Add a Docker Compose stack for Prometheus, Grafana, Loki, Tempo, and the OpenTelemetry Collector.
4. Replace the rule-based impact extractor with a structured LLM/event extractor.
5. Persist impact graphs to Neo4j behind the impact service.
6. Add auth, request IDs, retries with bounded backoff, and deployment-specific rate-limit policies.
