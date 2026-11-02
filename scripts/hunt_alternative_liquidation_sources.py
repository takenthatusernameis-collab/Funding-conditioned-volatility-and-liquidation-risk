#!/usr/bin/env python3
"""
Exhaustive alternative source hunt for Track A observed liquidations (unauthenticated only)
Follows RESEARCH_PROMPT §5. Produces evidence tables.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "research_state" / "data_source_registry_alt_hunt.json"


def now_z():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def http_probe(url):
    req = Request(url, headers={"User-Agent": "fclr-alt-hunt/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            status = resp.getcode()
            headers = dict(resp.headers.items())
            body = resp.read()
            return {"url": url, "status": status, "headers": headers, "body_len": len(body)}
    except HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        headers = dict(getattr(e, "headers", {}) or {})
        return {"url": url, "status": e.code, "headers": headers, "body_len": len(body), "error": True}
    except Exception as e:
        return {"url": url, "status": None, "headers": {}, "body_len": 0, "error": str(e)}


def main():
    ts = now_z()
    candidates = [
        {"name": "hyperliquid_public_api_info", "urls": ["https://api.hyperliquid.xyz/info"], "notes": "API may not serve historical liquidation census parquet"},
        {"name": "github_raw_search_hyperliquid_liquidations", "urls": ["https://raw.githubusercontent.com/search?q=hyperliquid+liquidations+parquet"], "notes": "Search endpoint varies; probe as-is"},
        {"name": "huggingface_other_datasets", "urls": ["https://huggingface.co/api/datasets?search=hyperliquid%20liquidations"], "notes": "Broader HF search"},
        {"name": "zenodo", "urls": ["https://zenodo.org/api/records?q=hyperliquid%20liquidations"], "notes": "Unauthenticated search"},
        {"name": "osf", "urls": ["https://api.osf.io/v2/search/"], "notes": "Search API"},
        {"name": "arxiv", "urls": ["https://export.arxiv.org/api/query?search_query=all:hyperliquid+liquidations"], "notes": "Unauthenticated"},
        {"name": "cryptodatadownload", "urls": ["https://www.cryptodatadownload.com/"], "notes": "May require auth/paid; probe"},
    ]
    results = {"hunt_id": f"alt_hunt_{ts}", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "candidates": []}
    for c in candidates:
        entry = {"name": c["name"], "notes": c["notes"], "probes": []}
        for url in c["urls"]:
            entry["probes"].append(http_probe(url))
        results["candidates"].append(entry)
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
