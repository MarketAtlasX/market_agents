# market_agents

This folder contains three lightweight agents implemented in pure Python:

- Impact Analysis Agent: extracts simple relations from text and computes a composite risk index.
- Market Data Agent: computes momentum, 14-day rolling volatility, and volume status.
- Recommendation Agent: combines the two to emit BUY/HOLD/SELL signals using heuristics.

# Quick demo

Run the demo (from the repository root):

```bash
python -m market_agents.main
```

Or run inside the package folder:

```bash
cd market_agents
python main.py
```

One-shot fetch-and-cache (Alpha Vantage, FRED, EIA)
-----------------------------------------------

1. Create `market_agents/.env` with your API keys (optional — fallbacks exist):

```
ALPHAVANTAGE_API_KEY=your_key_here
FRED_API_KEY=your_key_here
EIA_API_KEY=your_key_here
```

2. Run the cache fetch (writes JSON files to `market_agents/ingest/cache/`):

```bash
python -m market_agents.ingest.cache
```

If you do not provide keys, the cache step writes deterministic fallback JSON so the agents remain runnable.

Tests
-----

Run the unit test suite from inside `market_agents`:

```bash
python -m pytest -q tests
```

Dependencies
------------

Install runtime dependencies (recommended inside a venv):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
pip install -r requirements.txt
```

Notes
-----
- The current ingest helpers will attempt live fetches when API keys are provided in `.env`. If keys are missing or network calls fail, the helpers return fallback synthetic data so the demo and tests always run deterministically.
- Next steps: integrate an LLM extractor for impact parsing, persist graphs to Neo4j, or expose agents via FastAPI. I can implement any of these on request.

# MarketAtlas - market_agents restructure

New layout:

```
agents/
  impact/
    impact_agent.py
  market_data/
    market_data_agent.py
  recommendation/
    recommendation_agent.py

graph/
  workflow/

tests/

main.py
.env
.venv (created previously)
```

Run demo:

```bash
.venv\Scripts\python.exe main.py
```
