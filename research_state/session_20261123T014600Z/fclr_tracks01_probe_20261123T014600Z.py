#!/usr/bin/env python3
"""
FCLR-TRACKA-SOURCE-AUDIT-01 — fclr_tracks01_probe_20261123T014600Z.py
Bounded unauthenticated source probes for observed-liquidation labels.

Runs only lightweight HEAD/GET probes with short timeouts, a small retry budget
and exponential backoff. No authentication, no payment, no manual downloads.
Reads nothing from the sealed holdout. Outputs one JSON record per candidate
source: access proof (HTTP status, bytes, content-type, error), the
discoverable history depth / schema / cadence where the endpoint reveals it,
and an explicit rejection reason when a source is inadmissible for Track A.

Stdlib only (urllib). No network is required for the heavy evaluation; this
script is the source-probe phase and is allowed to probe live endpoints.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SESSION_UTC = "20261123T014600Z"
OUT_JSON = Path(__file__).resolve().parent / f"fclr_tracks01_probe_{SESSION_UTC}.json"

REQUEST_TIMEOUT = 12
MAX_RETRIES = 2
BACKOFF_BASE = 2.0
USER_AGENT = "fclr-tracks01-source-audit-probe/1.0 (research; unauthenticated)"

# Candidate free sources for OBSERVED liquidation labels (Track A) plus the
# mark-price/funding sources that support a Track B modeled-breach pivot.
CANDIDATES = [
    {
        "name": "Binance public market-data archive",
        "family": "exchange_official_archive",
        "base_url": "https://data.binance.vision",
        "purpose": "observed liquidation labels (liquidationSnapshot) + mark-price/funding/OI for Track B features",
        "endpoints": [
            {"url": "https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/", "label": "metrics directory listing"},
            {"url": "https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/", "label": "fundingRate directory listing"},
            {"url": "https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/", "label": "klines directory listing"},
            {"url": "https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/BTCUSDT-metrics-2026-01-01.zip", "label": "metrics sample zip (BTCUSDT 2026-01-01)"},
            {"url": "https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-2026-01.zip", "label": "fundingRate sample zip (BTCUSDT 2026-01)"},
            {"url": "https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/BTCUSDT/", "label": "liquidationSnapshot directory (expected absent)"},
            {"url": "https://data.binance.vision/data/futures/um/monthly/liquidationSnapshot/BTCUSDT/", "label": "liquidationSnapshot monthly (expected absent)"},
        ],
    },
    {
        "name": "Bybit public REST API (v5, linear)",
        "family": "exchange_public_rest",
        "base_url": "https://api.bybit.com",
        "purpose": "historical funding, klines, and any public liquidation history",
        "endpoints": [
            {"url": "https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=60&limit=2", "label": "kline"},
            {"url": "https://api.bybit.com/v5/market/funding/history?category=linear&symbol=BTCUSDT&limit=2", "label": "funding history"},
            {"url": "https://api.bybit.com/v5/market/liquidation?category=linear&symbol=BTCUSDT&limit=2", "label": "liquidation history"},
        ],
    },
    {
        "name": "OKX public REST API (v5)",
        "family": "exchange_public_rest",
        "base_url": "https://www.okx.com",
        "purpose": "historical funding, candles, and any public liquidation history",
        "endpoints": [
            {"url": "https://www.okx.com/api/v5/market/candles?instId=BTC-USDT-SWAP&bar=1H&limit=2", "label": "candles"},
            {"url": "https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP&limit=2", "label": "funding rate"},
            {"url": "https://www.okx.com/api/v5/public/liquidation?instId=BTC-USDT-SWAP&limit=2", "label": "liquidation (expected absent)"},
        ],
    },
    {
        "name": "Hyperliquid public API",
        "family": "exchange_public_rest",
        "base_url": "https://api.hyperliquid.xyz",
        "purpose": "any unauthenticated historical liquidation endpoint with deep history",
        "endpoints": [
            {"url": "https://api.hyperliquid.xyz/info", "label": "info endpoint (POST required; GET probe)", "method": "GET"},
        ],
    },
    {
        "name": "Ironflow / Hugging Face liquidations archive",
        "family": "institutional_archive",
        "base_url": "https://huggingface.co/datasets/ironflow/hyperliquid-liquidations",
        "purpose": "observed liquidation events (Hyperliquid), CC BY 4.0; on-disk ironflow bulk is the capped-sample feed",
        "endpoints": [
            {"url": "https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/2025-05.parquet?download=true", "label": "liquidation events parquet 2025-05"},
        ],
    },
    {
        "name": "Public GitHub / Zenodo / Hugging Face institutional archives (generic)",
        "family": "public_archive",
        "base_url": None,
        "purpose": "downloadable historical liquidation/event records without signup or keys",
        "endpoints": [],
        "note": "No specific URL verified admissible in this session; candidate family enumerated for the record. See RESEARCH_PROMPT.md section 5.",
    },
]


def fetch(url: str, method: str = "GET") -> dict:
    """One bounded fetch attempt. Returns a result dict (no exception raised)."""
    result = {"url": url, "method": method, "status": None, "error": None,
              "content_type": None, "content_length": None, "body_preview": None,
              "ok": False}
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": USER_AGENT,
                                        "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
            result["status"] = r.status
            result["content_type"] = r.headers.get("Content-Type")
            result["content_length"] = r.headers.get("Content-Length")
            body = r.read(2048)
            try:
                result["body_preview"] = body.decode("utf-8", "replace")
            except Exception:
                result["body_preview"] = f"<binary {len(body)} bytes>"
            result["ok"] = 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["error"] = f"HTTPError {e.code}: {e.reason}"
        try:
            result["body_preview"] = e.read(256).decode("utf-8", "replace")
        except Exception:
            result["body_preview"] = "<unreadable error body>"
    except Exception as e:  # URLError, timeout, socket, TLS
        result["error"] = f"{type(e).__name__}: {e}"
    return result


def probe_endpoint(endpoint: dict) -> dict:
    url = endpoint["url"]
    method = endpoint.get("method", "GET")
    attempts = []
    last = None
    for attempt in range(1, MAX_RETRIES + 2):
        last = fetch(url, method=method)
        attempts.append({**last, "attempt": attempt})
        if last["ok"] or last["status"] in (403, 404, 451):
            break
        if attempt < MAX_RETRIES + 1:
            time.sleep(BACKOFF_BASE * attempt)
    return {"endpoint": endpoint.get("label"), "url": url, "method": method,
            "attempts": attempts, "final": attempts[-1]}


def main() -> None:
    results = []
    for cand in CANDIDATES:
        cand_result = {
            "name": cand["name"],
            "family": cand["family"],
            "base_url": cand["base_url"],
            "purpose": cand["purpose"],
            "probed_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endpoints": [],
            "admissible_track_a_observed_liquidation": False,
            "rejection_reason": None,
            "notes": cand.get("note"),
        }
        for ep in cand["endpoints"]:
            cand_result["endpoints"].append(probe_endpoint(ep))
        cand_result["admissible_track_a_observed_liquidation"] = _judge(cand, cand_result["endpoints"])
        cand_result["rejection_reason"] = _reason(cand, cand_result)
        results.append(cand_result)

    summary = {
        "session_utc": SESSION_UTC,
        "campaign": "FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z",
        "phase": "SOURCE_ENUMERATION_PROBE",
        "method": "bounded unauthenticated GET/HEAD probes; stdlib urllib; no auth; no payment; no manual download",
        "n_candidates": len(results),
        "n_admissible_track_a": sum(1 for r in results if r["admissible_track_a_observed_liquidation"]),
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    OUT_JSON.write_text(json.dumps({"summary": summary, "candidates": results},
                                   indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=1))


def _judge(cand: dict, endpoints: list) -> bool:
    """True only if a candidate actually serves observed liquidation history."""
    for ep in endpoints:
        fin = ep["final"]
        if fin["ok"] and ("liquidation" in ep["url"].lower()):
            return True
    return False


def _reason(cand: dict, r: dict) -> str:
    if r["admissible_track_a_observed_liquidation"]:
        return None
    statuses = [ep["final"]["status"] for ep in r["endpoints"]]
    errors = [ep["final"]["error"] for ep in r["endpoints"] if ep["final"]["error"]]
    liquid_ok = any(ep["final"]["ok"] and "liquidation" in ep["url"].lower()
                    for ep in r["endpoints"])
    if any(s == 404 for s in statuses) and not liquid_ok:
        return "No public liquidation endpoint returned 200; observed-liquidation history not served."
    if any(s == 403 for s in statuses):
        return "Endpoint reachable but forbidden (403) without credentials; not an unauthenticated source."
    if errors:
        return "Unreachable / errored: " + "; ".join(errors[:2])
    return "No verified unauthenticated historical observed-liquidation path with defensible coverage."


if __name__ == "__main__":
    main()
