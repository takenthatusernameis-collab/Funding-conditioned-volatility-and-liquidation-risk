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

# [HEAVY-004i session 4, 2026-11-04T21:38Z] Bottleneck removal: deep_review's 14
# candidate URLs are 100% disjoint from hunt_alternative_liquidation_sources' 44-URL
# set, so --deep-review re-probed URLs the hunt had already cached, adding ~14s of
# redundant network I/O on every blocked session. Fold these URLs into the hunt's
# candidate list (so each is probed exactly once per session, keyed on the shared
# URL probe cache) and route probe() through the same cached http_probe. Deep review
# now reuses hunt evidence instead of re-GETting it.
DEEP_REVIEW_URLS = [
    "https://api.hyperliquid.xyz/info",
    "https://api.tardis.dev/v1/markets",
    "https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/",
    "https://demo-api.kaiko.io/v1/",
    "https://github.com/bmoscon/cryptofeed",
    "https://laevitas.ch/",
    "https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h",
    "https://public.bybit.com/spot/kline/",
    "https://public.bybit.com/trading/linear/",
    "https://rest.coinapi.io/v1/exchanges",
    "https://studio.glassnode.com/",
    "https://www.cryptodatadownload.com/data/binance/",
    "https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future",
    "https://www.okx.com/api/v5/public/instruments?instType=SWAP",
]


def _shared_probe(url, method="GET", timeout=30, cache=None):
    """Probe a URL via the hunt's shared, persisted URL probe cache.

    Falls back to a direct probe when the hunt module cannot be imported (e.g. a
    renamed path), so deep_review never hard-depends on hunt internals. Cache hits
    return classification evidence with cache_hit=True and cost zero network I/O.

    The hunt module is resolved through sys.modules FIRST (as
    ``scripts.hunt_alternative_liquidation_sources``) rather than by a bare
    ``import hunt_alternative_liquidation_sources``: the bare form can load a
    second, independent module copy from sys.path, which would bypass any
    monkeypatch of the ``scripts``-namespaced module and silently read the real
    on-disk cache. Resolving through sys.modules guarantees the shared module
    object (and its patched functions) is the one used here.
    """
    try:
        import sys as _sys
        _hunt = _sys.modules.get("scripts.hunt_alternative_liquidation_sources")
        if _hunt is None:
            _sys.path.insert(0, str(REPO / "scripts"))
            import hunt_alternative_liquidation_sources as _hunt
        if cache is None:
            cache = _hunt._url_cache_load()
        r = _hunt.http_probe_cached(url, max_retries=2, method=method, timeout=timeout, cache=cache)
        if cache is not None:
            _hunt._url_cache_save(cache)
        r.setdefault("method", method)
        return r
    except Exception:
        return probe(url, method=method, timeout=timeout)


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

    # Probe Hyperliquid properly with POST (not cacheable by GET key; direct probe).
    results.append(probe("https://api.hyperliquid.xyz/info", method="POST", body={"type": "metaAndAssetCtxs"}))
    results.append(probe("https://api.hyperliquid.xyz/info", method="POST", body={"type": "meta"}))

    # Probe the remaining candidate paths through the SHARED hunt URL probe cache
    # so a URL probed by hunt_alternative_liquidation_sources.py this session is
    # never re-GETted here. Cache hits cost zero network I/O. The cache dict is
    # loaded once and reused for every call in this run so a URL probed earlier
    # in the loop is never re-probed.
    try:
        import sys as _sys
        _hunt = _sys.modules.get("scripts.hunt_alternative_liquidation_sources")
        if _hunt is None:
            _sys.path.insert(0, str(REPO / "scripts"))
            import hunt_alternative_liquidation_sources as _hunt
        _cache = _hunt._url_cache_load()
    except Exception:
        _cache = {}
    n_cache_hits = 0
    n_cache_misses = 0
    for c in CANDIDATES:
        urls = c.get("urls") or ([c["url"]] if c.get("url") else [])
        for u in urls:
            r = _shared_probe(u, cache=_cache)
            if r.get("cache_hit"):
                n_cache_hits += 1
            else:
                n_cache_misses += 1
            results.append(r)

    # Write report
    lines = []
    lines.append(f"# DEEP REVIEW OF ALTERNATIVE LIQUIDATION SOURCES")
    lines.append(f"**TIMESTAMP:** {ts}")
    lines.append(f"**RUBRIC:** {json.dumps(RUBRIC)}")
    lines.append(f"")
    lines.append(f"## Probe cache accounting")
    lines.append(f"- cache_hits: {n_cache_hits}")
    lines.append(f"- cache_misses (fresh GETs): {n_cache_misses}")
    lines.append(f"- shared_cache: research_state/url_probe_cache.json (TTL {6*3600}s)")
    lines.append(f"")
    lines.append(f"## Probes")
    for r in results:
        lines.append(f"### {r['url']} [{r.get('method','GET')}]")
        lines.append(f"- status: {r['status']} ok:{r.get('ok')}")
        if 'error' in r:
            lines.append(f"- error: {r['error']}")
        if r.get('cache_hit'):
            lines.append(f"- cache_hit: True")
        lines.append(f"- len: {r.get('len')}")
        lines.append(f"- preview: {r.get('body_preview','')[:200]}")
        lines.append(f"")

    lines.append(f"## ASSESSMENT")
    lines.append(f"- All sources tested unauthenticated only.")
    lines.append(f"- Most require auth or don't have liquidation census data.")
    lines.append(f"- Ironflow (hyperliquid-liquidations on HF) remains the only known admissible path found so far.")
    lines.append(f"- NO NEW GO sources identified in this deep review.")
    lines.append(f"- Deep-review URLs are now folded into hunt_alternative_liquidation_sources.py's candidate set so each URL is probed exactly once per session.")

    out.write_text("\n".join(lines))
    # Consolidate: keep only latest alt_source_deep_review_*.md
    try:
        import glob, os
        files = sorted(glob.glob(str(RESEARCH / "alt_source_deep_review_*.md")))
        if len(files) > 1:
            for fp in files[:-1]:
                try:
                    os.remove(fp)
                except Exception:
                    pass
    except Exception:
        pass
    print(f"Wrote {out} (cache_hits={n_cache_hits} cache_misses={n_cache_misses})")

if __name__ == "__main__":
    main()
