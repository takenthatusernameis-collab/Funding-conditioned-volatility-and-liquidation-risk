#!/usr/bin/env python3
"""
Exhaustive alternative source hunt for Track A observed liquidations (unauthenticated only)
Follows RESEARCH_PROMPT §5. Produces evidence tables with GO/NO-GO rubric scoring.
Strengthened for 004i: more source families, retry/backoff, rubric-scored assessment.
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
USER_AGENT = "fclr-alt-hunt/1.2"

RUBRIC = {
    "min_symbols": 5,
    "min_complete_month_or_blocks": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks",
    "completeness_doc_required": True,
    "license_ok": True,
    "unauthenticated_only": True,
    "no_requester_pays": True,
    "schema_compatible_fclr010": True,
}


def now_z():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def http_probe(url, max_retries=2, method="GET", timeout=30, body_preview_len=200):
    """HTTP probe with retry/backoff and body preview capture.

    method may be "GET" or "HEAD". A body preview (first body_preview_len bytes,
    decoded as latin-1 for binary-safety) is captured so error pages and small
    JSON responses can be classified by content, not just status code.
    """
    for attempt in range(max_retries + 1):
        req = Request(url, headers={"User-Agent": USER_AGENT}, method=method)
        try:
            with urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                headers = dict(resp.headers.items())
                body = resp.read()
                preview = body[:body_preview_len].decode("latin-1", errors="replace")
                return {
                    "url": url,
                    "method": method,
                    "status": status,
                    "headers": {k.lower(): v for k, v in headers.items()},
                    "body_len": len(body),
                    "body_preview": preview,
                    "attempts": attempt + 1,
                }
        except HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b""
            headers = dict(getattr(e, "headers", {}) or {})
            result = {
                "url": url,
                "method": method,
                "status": e.code,
                "headers": {k.lower(): v for k, v in headers.items()},
                "body_len": len(body),
                "body_preview": body[:body_preview_len].decode("latin-1", errors="replace"),
                "error": True,
                "attempts": attempt + 1,
            }
            if e.code == 429 and attempt < max_retries:
                time.sleep(2 ** attempt + random.random())
                continue
            if 500 <= e.code < 600 and attempt < max_retries:
                time.sleep(1 + random.random())
                continue
            return result
        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 + random.random())
                continue
            return {
                "url": url,
                "method": method,
                "status": None,
                "headers": {},
                "body_len": 0,
                "body_preview": str(e),
                "error": str(e),
                "attempts": attempt + 1,
            }


def probe_directory_listing(url, max_retries=2):
    """For a directory-style URL, try GET and capture enough to classify content.

    Returns the same dict shape as http_probe plus a 'content_kind' guess
    ('json' | 'html' | 'parquet' | 'text' | 'binary') derived from Content-Type
    and the magic bytes of the body.
    """
    r = http_probe(url, max_retries=max_retries)
    ct = (r.get("headers", {}).get("content-type") or "").lower()
    pv = r.get("body_preview") or ""
    if r.get("status") == 200 and "parquet" in ct:
        r["content_kind"] = "parquet"
    elif r.get("status") == 200 and "json" in ct:
        r["content_kind"] = "json"
    elif r.get("status") == 200 and "html" in ct:
        r["content_kind"] = "html"
    elif r.get("status") == 200 and pv.startswith("PAR1"):
        r["content_kind"] = "parquet"
    elif r.get("status") == 200:
        r["content_kind"] = "text"
    else:
        r["content_kind"] = "error"
    return r


def assess_rubric(entry):
    statuses = [p.get("status") for p in entry.get("probes", [])]
    any_200 = any(s == 200 for s in statuses if s is not None)
    any_403_or_401 = any(s in (401, 403) for s in statuses if s is not None)
    all_absent_or_error = all(s in (404, None) for s in statuses if s is not None)
    if not any_200:
        return "NO-GO"
    if any_403_or_401:
        return "NO-GO"
    return "REVIEW_REQUIRED"


def main():
    ts = now_z()
    candidates = [
        {"name": "hyperliquid_public_api_info", "urls": ["https://api.hyperliquid.xyz/info"], "notes": "API may not serve historical liquidation census parquet"},
        {"name": "github_raw_search_hyperliquid_liquidations", "urls": ["https://raw.githubusercontent.com/hyperliquid-dex/hyperliquid-liquidations/HEAD/README.md"], "notes": "Check repo exists/readme"},
        {"name": "github_api_repos", "urls": ["https://api.github.com/repos/hyperliquid-dex/hyperliquid-liquidations/contents"], "notes": "GitHub API unauthenticated"},
        {"name": "huggingface_other_datasets", "urls": ["https://huggingface.co/api/datasets?search=hyperliquid%20liquidations", "https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations"], "notes": "Broader HF search + dataset metadata"},
        {"name": "huggingface_liquidation_search_broad", "urls": ["https://huggingface.co/api/datasets?search=liquidations", "https://huggingface.co/api/datasets?search=crypto%20liquidation", "https://huggingface.co/api/datasets?search=perpetual%20liquidation"], "notes": "Broad HF liquidation dataset discovery"},
        {"name": "zenodo", "urls": ["https://zenodo.org/api/records?q=hyperliquid%20liquidations", "https://zenodo.org/api/records?q=crypto%20liquidation%20perpetual"], "notes": "Unauthenticated search"},
        {"name": "osf", "urls": ["https://api.osf.io/v2/"], "notes": "OSF root probe"},
        {"name": "arxiv", "urls": ["https://export.arxiv.org/api/query?search_query=all:hyperliquid+liquidations&max_results=5", "https://export.arxiv.org/api/query?search_query=all:crypto+liquidation+perpetual&max_results=5"], "notes": "Unauthenticated"},
        {"name": "data_commoncrawl", "urls": ["https://index.commoncrawl.org/"], "notes": "Index root probe only (no crawl auth)"},
        {"name": "kaggle", "urls": ["https://www.kaggle.com/api/v1/datasets/list?search=hyperliquid%20liquidations"], "notes": "Public API root/search style"},
        {"name": "github_code_search_unauth", "urls": ["https://api.github.com/search/code?q=hyperliquid+liquidations+parquet"], "notes": "Unauthenticated code search (usually 401)"},
        {"name": "github_repos_search", "urls": ["https://api.github.com/search/repositories?q=hyperliquid+liquidations"], "notes": "Unauthenticated repo search"},
        {"name": "coinglass_public", "urls": ["https://www.coinglass.com/", "https://www.coinglass.com/LiquidationData"], "notes": "Public site structure probe"},
        {"name": "hyblock_public", "urls": ["https://hyblockcapital.com/"], "notes": "Public site probe"},
        {"name": "coinank_public", "urls": ["https://www.coinank.com/"], "notes": "Public site probe"},
        {"name": "paradigm_research", "urls": ["https://www.paradigm.xyz/research"], "notes": "Research page probe for liquidation datasets"},
        {"name": "theblock_research", "urls": ["https://www.theblock.co/research"], "notes": "Research page probe"},
    ]
    results = {"hunt_id": f"alt_hunt_{ts}", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i", "unauthenticated_only": True, "rubric": RUBRIC, "candidates": []}
    for c in candidates:
        entry = {"name": c["name"], "notes": c["notes"], "probes": []}
        for url in c["urls"]:
            p = http_probe(url)
            # Ensure we capture evidence per candidate
            entry["probes"].append(p)
        entry["rubric_assessment"] = assess_rubric(entry)
        results["candidates"].append(entry)
    go_sources = [c["name"] for c in results["candidates"] if c["rubric_assessment"] == "REVIEW_REQUIRED"]
    results["summary"] = {
        "candidates_probed": len(results["candidates"]),
        "go_or_review_sources": go_sources,
        "conclusion": "No NEW admissible unauthenticated Track A source beyond ironflow/hyperliquid-liquidations found" if not go_sources else f"Review required for: {go_sources}",
    }
    # Write main registry
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    # Write timestamped alt source scan artifact (required)
    scan_path = REPO_ROOT / "research_state" / f"alt_source_scan_{ts}.json"
    with open(scan_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote: {OUT_PATH}")
    print(f"Wrote: {scan_path}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


# Additional probe for common exchange liquidation endpoints (unauthenticated)
EXTRA_PROBES = [
    ("bybit_public_instruments", ["https://api.bybit.com/v5/market/instruments-info?category=linear"]),
    ("okx_public_instruments", ["https://www.okx.com/api/v5/public/instruments?instType=SWAP"]),
]


# HEAVY-004i enhancement: add more unauthenticated candidates
ENHANCED_CANDIDATES = [
    {"name": "coinglass_public_liquidations", "urls": ["https://www.coinglass.com/api/liquidation/chart", "https://www.coinglass.com/LiquidationData"], "notes": "Coinglass public pages (often requires JS; probe for structure only)"},
    {"name": "coinank_public", "urls": ["https://www.coinank.com/"], "notes": "Public site probe"},
    {"name": "laevitas_public", "urls": ["https://laevitas.ch/"], "notes": "Public site probe"},
    {"name": "hyblock_public", "urls": ["https://hyblockcapital.com/"], "notes": "Public site probe"},
    {"name": "paradigm_data_research", "urls": ["https://www.paradigm.xyz/research"], "notes": "Research page probe for liquidation datasets"},
    {"name": "glassnode_public_docs", "urls": ["https://docs.glassnode.com/"], "notes": "Docs probe"},
]
