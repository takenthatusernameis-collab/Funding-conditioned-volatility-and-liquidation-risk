#!/usr/bin/env python3
"""
Exhaustive alternative source hunt for Track A observed liquidations (unauthenticated only)
Follows RESEARCH_PROMPT §5. Produces evidence tables. Strengthened for 004i.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "research_state" / "data_source_registry_alt_hunt.json"
USER_AGENT = "fclr-alt-hunt/1.1"


def now_z():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def http_probe(url, max_retries=2):
    for attempt in range(max_retries + 1):
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=30) as resp:
                status = resp.getcode()
                headers = dict(resp.headers.items())
                body = resp.read()
                return {"url": url, "status": status, "headers": {k.lower(): v for k, v in headers.items()}, "body_len": len(body), "attempts": attempt + 1}
        except HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b""
            headers = dict(getattr(e, "headers", {}) or {})
            result = {"url": url, "status": e.code, "headers": {k.lower(): v for k, v in headers.items()}, "body_len": len(body), "error": True, "attempts": attempt + 1}
            if e.code == 429 and attempt < max_retries:
                time.sleep(2 ** attempt + random.random())
                continue
            return result
        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 + random.random())
                continue
            return {"url": url, "status": None, "headers": {}, "body_len": 0, "error": str(e), "attempts": attempt + 1}


def main():
    ts = now_z()
    candidates = [
        {"name": "hyperliquid_public_api_info", "urls": ["https://api.hyperliquid.xyz/info"], "notes": "API may not serve historical liquidation census parquet"},
        {"name": "github_raw_search_hyperliquid_liquidations", "urls": ["https://raw.githubusercontent.com/hyperliquid-dex/hyperliquid-liquidations/HEAD/README.md"], "notes": "Check repo exists/readme"},
        {"name": "github_api_repos", "urls": ["https://api.github.com/repos/hyperliquid-dex/hyperliquid-liquidations/contents"], "notes": "GitHub API unauthenticated"},
        {"name": "huggingface_other_datasets", "urls": ["https://huggingface.co/api/datasets?search=hyperliquid%20liquidations", "https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations"], "notes": "Broader HF search + dataset metadata"},
        {"name": "zenodo", "urls": ["https://zenodo.org/api/records?q=hyperliquid%20liquidations"], "notes": "Unauthenticated search"},
        {"name": "osf", "urls": ["https://api.osf.io/v2/"], "notes": "OSF root probe"},
        {"name": "arxiv", "urls": ["https://export.arxiv.org/api/query?search_query=all:hyperliquid+liquidations&max_results=5"], "notes": "Unauthenticated"},
        {"name": "data_commoncrawl", "urls": ["https://index.commoncrawl.org/"], "notes": "Index root probe only (no crawl auth)"},
        {"name": "kaggle", "urls": ["https://www.kaggle.com/api/v1/datasets/list?search=hyperliquid%20liquidations"], "notes": "Public API root/search style"},
    ]
    results = {"hunt_id": f"alt_hunt_{ts}", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i", "unauthenticated_only": True, "candidates": []}
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
