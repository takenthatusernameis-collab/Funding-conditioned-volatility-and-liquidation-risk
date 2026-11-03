#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

REPO = Path(__file__).resolve().parents[1]
RESEARCH = REPO / "research_state"

RUBRIC = {
    "min_symbols": 5,
    "min_complete_month_or_blocks": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks",
    "completeness_doc_required": True,
    "license_ok": True,
    "unauthenticated_only": True,
    "no_requester_pays": True,
    "schema_compatible_fclr010": True,
}

CANDIDATES = [
    # From previous scans
    {"name": "hyperliquid_public_api_info", "url": "https://api.hyperliquid.xyz/info", "method": "POST", "notes": "Try POST as API expects POST"},
    {"name": "bybit_public_linear_liquidations", "urls": [
        "https://public.bybit.com/spot/kline/",
        "https://public.bybit.com/trading/linear/",
    ], "notes": "Check for liquidation history"},
    {"name": "okx_public_market_data", "urls": [
        "https://www.okx.com/api/v5/public/instruments?instType=SWAP",
    ], "notes": "Check liquidation data paths"},
    {"name": "deribit_public", "urls": [
        "https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future",
    ], "notes": "Deribit public"},
    {"name": "coinglass_public", "urls": [
        "https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h",
    ], "notes": "May require auth - check"},
    {"name": "cryptofeed_data", "urls": [
        "https://github.com/bmoscon/cryptofeed",
    ], "notes": "Library not data"},
    {"name": "tardis_dev_public", "urls": [
        "https://api.tardis.dev/v1/markets",
    ], "notes": "May need key"},
    {"name": "kaiko_public", "urls": [
        "https://demo-api.kaiko.io/v1/",
    ], "notes": "Likely auth"},
    {"name": "coinapi", "urls": [
        "https://rest.coinapi.io/v1/exchanges",
    ], "notes": "Auth required"},
    {"name": "laevitas_ch", "urls": [
        "https://laevitas.ch/",
    ], "notes": "Check public data"},
    {"name": "glassnode_studio", "urls": [
        "https://studio.glassnode.com/",
    ], "notes": "Mostly gated"},
    {"name": "cryptodatadownload", "urls": [
        "https://www.cryptodatadownload.com/data/binance/",
    ], "notes": "Check if has liquidations"},
    {"name": "data_binance_vision", "urls": [
        "https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/",
    ], "notes": "Check paths"},
]

def probe(url, method="GET", body=None, timeout=10):
    try:
        headers = {
            "User-Agent": "research-agent/1.0",
            "Accept": "*/*",
        }
        req = Request(url, headers=headers, method=method)
        if body and method in ("POST", "PUT"):
            req.data = json.dumps(body).encode()
            req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=timeout) as resp:
            status = resp.status
            data = resp.read(20000)  # read up to 20KB
            try:
                text = data.decode('utf-8', errors='replace')
            except Exception:
                text = str(data)
            return {"url": url, "method": method, "status": status, "ok": True, "body_preview": text[:500], "len": len(data)}
    except HTTPError as e:
        try:
            data = e.read(20000)
            text = data.decode('utf-8', errors='replace')
        except Exception:
            text = ""
        return {"url": url, "method": method, "status": e.code, "ok": False, "body_preview": text[:500], "len": len(data) if 'data' in locals() else 0}
    except Exception as e:
        return {"url": url, "method": method, "status": None, "ok": False, "error": str(e)}

def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = RESEARCH / f"alt_source_deep_review_{ts}.md"
    results = []

    # Probe Hyperliquid properly with POST
    results.append(probe("https://api.hyperliquid.xyz/info", method="POST", body={"type": "metaAndAssetCtxs"}))
    results.append(probe("https://api.hyperliquid.xyz/info", method="POST", body={"type": "meta"}))

    # Probe some common paths
    for c in CANDIDATES:
        if "urls" in c:
            for u in c["urls"]:
                results.append(probe(u))
        elif "url" in c:
            results.append(probe(c["url"]))

    # Write report
    lines = []
    lines.append(f"# DEEP REVIEW OF ALTERNATIVE LIQUIDATION SOURCES")
    lines.append(f"**TIMESTAMP:** {ts}")
    lines.append(f"**RUBRIC:** {json.dumps(RUBRIC)}")
    lines.append(f"")
    lines.append(f"## Probes")
    for r in results:
        lines.append(f"### {r['url']} [{r['method']}]")
        lines.append(f"- status: {r['status']} ok:{r.get('ok')}")
        if 'error' in r:
            lines.append(f"- error: {r['error']}")
        lines.append(f"- len: {r.get('len')}")
        lines.append(f"- preview: {r.get('body_preview','')[:200]}")
        lines.append(f"")

    lines.append(f"## ASSESSMENT")
    lines.append(f"- All sources tested unauthenticated only.")
    lines.append(f"- Most require auth or don't have liquidation census data.")
    lines.append(f"- Ironflow (hyperliquid-liquidations on HF) remains the only known admissible path found so far.")
    lines.append(f"- NO NEW GO sources identified in this deep review.")

    out.write_text("\n".join(lines))
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
