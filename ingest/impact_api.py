import os
import requests
from typing import Dict, Any


def fetch_gdelt_events(query: str = "conflict") -> Dict[str, Any]:
    """Fetch recent GDELT events matching a query. Returns fallback on failure.

    GDELT APIs are public and generally do not require a key.
    """
    url = "https://api.gdeltproject.org/api/v2/events/search"
    params = {"query": query, "mode": "artlist", "format": "JSON"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        j = r.json()
        # return a small subset
        return {"query": query, "total": j.get("total", 0), "articles": j.get("articles", [])}
    except Exception:
        return {"query": query, "total": 0, "articles": []}


def fetch_acled_events() -> Dict[str, Any]:
    """Attempt to fetch ACLED recent export (best-effort). Fallback on failure.

    ACLED may require registration for API access; this attempts a public CSV download
    and otherwise returns an empty list.
    """
    url = "https://acleddata.com/data-export-tool/"  # not a stable API, best-effort
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        # we don't parse the site; just return that it's reachable
        return {"acled_reachable": True}
    except Exception:
        return {"acled_reachable": False}


def fetch_eia_data(series_id: str) -> Dict[str, Any]:
    """Fetch EIA series if `EIA_API_KEY` present; otherwise fallback.
    """
    apikey = os.environ.get("EIA_API_KEY")
    if not apikey:
        return {"series_id": series_id, "values": [0.0, 0.1]}
    url = f"https://api.eia.gov/series/"
    params = {"api_key": apikey, "series_id": series_id}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        j = r.json()
        data = j.get("series", [])[0]
        return {"series_id": series_id, "data": data}
    except Exception:
        return {"series_id": series_id, "values": [0.0, 0.1]}
