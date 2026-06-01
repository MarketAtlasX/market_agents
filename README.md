# market_agents

MarketAtlas `market_agents` is a lightweight Python prototype for combining market signals with geopolitical impact analysis and simple trade recommendations.

It currently includes three small agents:

- Impact Analysis Agent: extracts basic relations from text, builds a graph, and computes a composite risk score.
- Market Data Agent: calculates momentum, rolling volatility, and volume status from a price series.
- Recommendation Agent: combines the market snapshot and impact score to produce a BUY, HOLD, or SELL decision.

## What works today

- A runnable demo entrypoint in `main.py`.
- Best-effort live ingest helpers for Alpha Vantage, FRED, EIA, GDELT, and ACLED.
- Fallback synthetic data when APIs or network calls are unavailable.
- A broader pytest suite covering the demo path, market-data logic, impact flow, recommendation rules, and ingest helper behavior.

## Repository Layout

```text
market_agents/
  main.py
  graph/
  impact/
  ingest/
  market_data/
  recommendation/
  tests/
  requirements.txt
  README.md
```

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the repository root if you want live API-backed fetches:

```env
ALPHAVANTAGE_API_KEY=your_key_here
FRED_API_KEY=your_key_here
EIA_API_KEY=your_key_here
```

If these keys are missing, the project still runs using deterministic fallback data.

## Run The Demo

From the repository root:

```bash
python main.py
```

If you want to run it as a module from a parent directory:

```bash
python -m market_agents.main
```

The demo prints:

- A market snapshot with momentum, volatility, and volume state.
- An impact summary with local and composite risk.
- A recommendation with the final action and reason.

## Fetch And Cache Data

Run the one-shot cache job to fetch live data where possible and write JSON files into `ingest/cache/`:

```bash
python -m market_agents.ingest.cache
```

This step is resilient:

- With keys and network access, it stores live responses.
- Without keys or when requests fail, it stores deterministic fallback payloads.

## Run Tests

Run the full test suite with:

```bash
python -m pytest -q tests
```

Current test coverage includes:

- Demo smoke test.
- Market-data signal calculations.
- Market-data ingest wrapper behavior.
- Impact pipeline and graph propagation.
- Recommendation decision rules.
- Alpha Vantage, FRED, and EIA helper parsing and fallback behavior.

## Current Status

- The repo is passing tests with the current implementation.
- Live API keys are wired through `.env` and used by the ingest helpers.
- The codebase still keeps the graph workflow minimal, so the current focus is on the agent pipeline, ingestion, and validation.

## Notes

- `tests/conftest.py` keeps imports stable whether pytest is run from the repository root or the package directory.
- The ingest helpers are intentionally best-effort, so the project remains runnable even when external APIs are unavailable.
- If you want, the next natural step is to turn the placeholder graph workflow into a real LangGraph pipeline.
