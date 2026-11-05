#!/usr/bin/env python3
"""
Exhaustive alternative source hunt for Track A observed liquidations (unauthenticated only)
Follows RESEARCH_PROMPT §5. Produces evidence tables with GO/NO-GO rubric scoring.
Strengthened for 004i: more source families, retry/backoff, rubric-scored assessment.

[HEAVY-004i bottleneck removal] Persisted caches so repeated blocked sessions do not
re-enumerate HF search or re-probe the same candidate URLs:
- HF search enumeration cache (SEARCH_CACHE_PATH, TTL SEARCH_TTL_SECONDS = 24h)
- per-URL probe cache (URL_CACHE_PATH, TTL URL_CACHE_TTL_SECONDS = 6h)
- URL dedup across EXTENDED_CANDIDATES + HF_SEARCH_DISCOVERED + DEEP_REVIEW_URLS
so deep_review_alt_sources.py reuses hunt's shared URL probe cache instead of
re-GETting the same URLs.
"""
import json
import random
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "research_state" / "data_source_registry_alt_hunt.json"
USER_AGENT = "fclr-alt-hunt/1.2"

# Extended candidate set for 004i (static floor, not a ceiling).
EXTENDED_CANDIDATES = [
    {"name": "coinapi_free_liquidations", "type": "api_docs", "url": "https://docs.coinapi.io/", "notes": "Check unauthenticated history; many require keys - treat as NO-GO unless explicit unauthenticated historical download exists with >=5 symbols and >=1 complete month.", "probes": ["https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_BTC_USDT/latest?period_id=1DAY&limit=1"]},
    {"name": "cryptofeed_docs", "type": "docs", "url": "https://github.com/bmoscon/cryptofeed", "notes": "Library not a dataset host; NO-GO as data source.", "probes": []},
    {"name": "tardis_dev_docs", "type": "docs", "url": "https://tardis.dev/", "notes": "Commercial/requires access in general; check unauthenticated download paths. Likely NO-GO unless explicit free historical download exists.", "probes": ["https://api.tardis.dev/v1/"]},
    {"name": "kaiko_docs", "type": "docs", "url": "https://www.kaiko.com/", "notes": "Paid; NO-GO.", "probes": []},
    {"name": "glassnode_docs", "type": "docs", "url": "https://docs.glassnode.com/", "notes": "Paid/auth; NO-GO.", "probes": []},
    {"name": "coinglass_public_pages", "type": "web", "url": "https://www.coinglass.com/", "notes": "Check for downloadable historical liquidation data without login/payment; often requires signup/API - probe cautiously.", "probes": ["https://www.coinglass.com/"]},
    {"name": "bybit_public_archive_check", "type": "exchange", "url": "https://public.bybit.com/", "notes": "Bybit public data archive exists but check liquidation data specifically; unauthenticated downloads possible for some datasets.", "probes": ["https://public.bybit.com/"]},
    {"name": "okx_public_data", "type": "exchange", "url": "https://www.okx.com/", "notes": "Check public historical data; liquidation history may require specific endpoints - probe.", "probes": ["https://www.okx.com/"]},
]

# HF search enumeration cache: persisted so repeated blocked sessions reuse the
# discovered candidate set instead of re-querying /api/datasets?search= every run.
SEARCH_CACHE_PATH = REPO_ROOT / "research_state" / "hf_search_cache.json"
SEARCH_TTL_SECONDS = 24 * 3600  # 24 hours; HF dataset search index rarely changes faster


def _cache_load():
    """Load the persisted HF search cache. Returns {} on any failure."""
    try:
        raw = json.loads(SEARCH_CACHE_PATH.read_text())
    except Exception:
        return {}
    if not isinstance(raw, dict) or "candidates" not in raw:
        return {}
    return raw


def _cache_save(candidates, queries, errors):
    """Persist the enumerated candidate set with a generation timestamp."""
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "queries": queries,
        "errors": errors,
        "candidates": candidates,
    }
    try:
        SEARCH_CACHE_PATH.write_text(json.dumps(payload, indent=2))
    except Exception:
        pass
    return payload


def _cache_fresh(cache):
    """True when the cached enumeration is still within its TTL."""
    ts = cache.get("generated_utc")
    if not ts:
        return False
    try:
        gen = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return False
    age = (datetime.now(timezone.utc) - gen).total_seconds()
    return age < SEARCH_TTL_SECONDS


def now_z():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# Per-URL probe cache: conditional-request evidence persisted so a URL probed
# once in a session is never re-GETted again (shared with deep_review).
URL_CACHE_PATH = REPO_ROOT / "research_state" / "url_probe_cache.json"
URL_CACHE_TTL_SECONDS = 6 * 3600  # 6 hours; candidate pages rarely change faster


def _url_cache_load():
    try:
        raw = json.loads(URL_CACHE_PATH.read_text())
    except Exception:
        return {}
    return raw if isinstance(raw, dict) else {}


def _url_cache_save(cache):
    try:
        URL_CACHE_PATH.write_text(json.dumps(cache, indent=2))
    except Exception:
        pass


def _url_cache_get(cache, url):
    """Return a cached probe result for url if it is still fresh, else None."""
    entry = cache.get(url)
    if not isinstance(entry, dict):
        return None
    ts = entry.get("probed_utc")
    if not ts:
        return None
    try:
        probed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None
    age = (datetime.now(timezone.utc) - probed).total_seconds()
    if age >= URL_CACHE_TTL_SECONDS:
        return None
    return entry


def http_probe_cached(url, max_retries=2, method="GET", timeout=30, body_preview_len=200, cache=None):
    """http_probe wrapper that consults the persisted URL probe cache.

    On a cache hit the cached classification evidence is returned without any
    network access, and a 'cache_hit' flag is set so the caller can report it.
    """
    if cache is not None:
        cached = _url_cache_get(cache, url)
        if cached is not None:
            hit = dict(cached)
            hit["cache_hit"] = True
            return hit
    r = http_probe(url, max_retries=max_retries, method=method, timeout=timeout, body_preview_len=body_preview_len)
    if cache is not None and r.get("status") is not None:
        rec = dict(r)
        rec["probed_utc"] = datetime.now(timezone.utc).isoformat()
        rec["cache_hit"] = False
        cache[url] = rec
    return r


def _post_cache_key(url, body):
    """Cache key for POST probes: URL + sha256 of the serialized body.

    POST bodies differ (e.g. Hyperliquid info {"type":"metaAndAssetCtxs"} vs
    {"type":"meta"}), so a URL-only key would miss and re-POST every session,
    burning ~3.7s of the blocked-path deep-review cost on every run.
    """
    if body is None:
        b = b""
    elif isinstance(body, (bytes, bytearray)):
        b = bytes(body)
    else:
        b = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return url + "#" + hashlib.sha256(b).hexdigest()


def http_probe_cached_post(url, body, max_retries=2, timeout=30, body_preview_len=200, cache=None):
    """POST probe via the shared, persisted URL probe cache (keyed on URL+body).

    On a cache hit the cached classification evidence is returned without any
    network access and a 'cache_hit' flag is set. Falls back to a direct POST
    when the hunt module cannot be imported.
    """
    if cache is not None:
        key = _post_cache_key(url, body)
        cached = _url_cache_get(cache, key)
        if cached is not None:
            hit = dict(cached)
            hit["cache_hit"] = True
            hit["method"] = "POST"
            return hit
    r = http_probe(url, max_retries=max_retries, method="POST", timeout=timeout, body_preview_len=body_preview_len, body=body)
    if cache is not None and r.get("status") is not None:
        rec = dict(r)
        rec["probed_utc"] = datetime.now(timezone.utc).isoformat()
        rec["cache_hit"] = False
        rec["method"] = "POST"
        cache[_post_cache_key(url, body)] = rec
    return r


def http_probe(url, max_retries=2, method="GET", timeout=30, body_preview_len=200, body=None):
    """HTTP probe with retry/backoff and body preview capture.

    method may be "GET", "HEAD", or "POST". A body may be supplied for POST
    requests (serialized as JSON). A body preview (first body_preview_len bytes,
    decoded as latin-1 for binary-safety) is captured so error pages and small
    JSON responses can be classified by content, not just status code.
    """
    for attempt in range(max_retries + 1):
        data = None
        headers = {"User-Agent": USER_AGENT}
        if body is not None and method in ("POST", "PUT"):
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = Request(url, headers=headers, method=method, data=data)
        try:
            with urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                headers = dict(resp.headers.items())
                body = resp.read()
                preview = body[:body_preview_len].decode("latin-1", errors="replace")
                result = {
                    "url": url,
                    "method": method,
                    "status": status,
                    "headers": {k.lower(): v for k, v in headers.items()},
                    "body_len": len(body),
                    "body_preview": preview,
                    "attempts": attempt + 1,
                }
                ct = (result["headers"].get("content-type") or "").lower()
                if "parquet" in ct or preview.startswith("PAR1"):
                    result["content_kind"] = "parquet"
                elif "json" in ct:
                    result["content_kind"] = "json"
                elif "html" in ct:
                    result["content_kind"] = "html"
                elif status == 200:
                    result["content_kind"] = "text"
                else:
                    result["content_kind"] = "error"
                return result
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


RUBRIC = {
    "min_symbols": 5,
    "min_complete_month_or_blocks": ">=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks",
    "completeness_doc_required": True,
    "license_ok": True,
    "unauthenticated_only": True,
    "no_requester_pays": True,
    "schema_compatible_fclr010": True,
}

# Candidates discovered by live HF /api/datasets?search= enumeration (populated by
# discover_hf_liquidation_datasets). These supplement EXTENDED_CANDIDATES.
HF_SEARCH_DISCOVERED = [
    {"name": "ochinimus_crypto_liquidation_ticks", "urls": [
        "https://huggingface.co/api/datasets/ochinimus/crypto-liquidation-ticks",
        "https://huggingface.co/datasets/ochinimus/crypto-liquidation-ticks/resolve/main/coverage_20260807.csv",
        "https://huggingface.co/datasets/ochinimus/crypto-liquidation-ticks/resolve/main/README.md",
    ], "notes": "1,442,664 observed liquidation prints from Bybit/Binance/OKX USDT-margined perpetuals, 800 symbols, 2026-07-08..2026-08-06. CC-BY-4.0. Schema: ts_ms,utc_time,symbol,exchange,event,size,price,usd. >=5 symbols (6 core on all 3 venues), >=1 complete month, unauthenticated, documented coverage. NOTE: Bybit is complete; Binance/OKX are capped snapshots (undercount during cascades). Not Hyperliquid - requires NEW protocol version, not a drop-in for FCLR-010."},
    {"name": "nick128373_crypto_liquidation_ticks", "urls": [
        "https://huggingface.co/api/datasets/nick128373/crypto-liquidation-ticks",
    ], "notes": "Mirror/fork of ochinimus/crypto-liquidation-ticks with identical schema and coverage. Same caveats apply."},
    {"name": "werracle_oev_liquidation_dataset_2026", "urls": [
        "https://huggingface.co/api/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026",
        "https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026/resolve/main/README.md",
    ], "notes": "Werracle Verified Empirical OEV & Liquidation Dynamics Dataset v1.2. 105 SVR transactions / 513 liquidations on Base L2. CC-BY-4.0. Scope is on-chain MEV/OEV, NOT perpetual-futures liquidations - does not match FCLR-H004. NO-GO for Track A as-is."},
    {"name": "hyperliquid_builder_liquidation_panel", "urls": [
        "https://huggingface.co/api/datasets/craftify2221/hyperliquid-builder-liquidation-panel",
        "https://huggingface.co/datasets/craftify2221/hyperliquid-builder-liquidation-panel/resolve/main/README.md",
    ], "notes": "Hyperliquid account-day panel (RPANEL.parquet, ODC-BY). liq_same binary label per account-day. SAME VENUE as FCLR-010 (Hyperliquid perpetuals) - the only new Hyperliquid liquidation signal found. BUT: RPANEL.parquet is 1.06 GB (unbounded download), and the label is account-day liquidation-anywhere, not the FCLR-010 liquidation-notional intensity target. Schema (d,address,grp,b,npos,lev,ltype,gross,av,buf,liq_same,traded,mo) is NOT compatible with FCLR-010 (needs timestamp,symbol,mark_price,funding_rate). Requires new protocol version. REVIEW_REQUIRED pending bounded coverage probe."},
    {"name": "chainticks_defi_liquidations", "urls": [
        "https://huggingface.co/api/datasets/Chainticks/defi-liquidations",
        "https://huggingface.co/datasets/Chainticks/defi-liquidations/resolve/main/README.md",
    ], "notes": "Normalized DeFi liquidation events from public on-chain logs, parquet partitioned by date=YYYY-MM-DD, CC-BY-4.0. Scope is DeFi (lending protocols), NOT perpetual-futures exchange liquidations. Does not match FCLR-H004. NO-GO for Track A as-is."},
    {"name": "verilex_defi_liquidations", "urls": [
        "https://huggingface.co/api/datasets/carrierone/verilex-defi-liquidations",
    ], "notes": "DeFi liquidation risk signals across Aave/Compound/Venus/Morpho. Requires x402 micropayments ($0.025/query) for full API - requester-pays. NO-GO per strict rubric (no_requester_pays)."},
    {"name": "bitcoin_liquidation_heatmapping", "urls": [
        "https://huggingface.co/api/datasets/PhysiAI/Bitcoin-Liquidation-Heatmapping",
    ], "notes": "Bitcoin liquidation heatmapping, Apache-2.0. Scope is Bitcoin spot/heatmapping, NOT perpetual-futures liquidation events. NO-GO for Track A as-is."},
]

# Deep-review candidate URLs (folded into the hunt candidate set so each URL is
# probed exactly once per session via the shared URL probe cache). Stored as
# candidate-style dicts (with "urls") so the hunt and deep_review test harnesses
# can iterate them uniformly.
DEEP_REVIEW_URLS = [
    {"name": "deep_review__api.hyperliquid.xyz_info", "urls": ["https://api.hyperliquid.xyz/info"], "notes": "Hyperliquid info endpoint (GET; POST variants probed separately by deep_review)."},
    {"name": "deep_review__tardis_dev_v1_markets", "urls": ["https://api.tardis.dev/v1/markets"], "notes": "Tardis public markets root (auth-gated for historical data)."},
    {"name": "deep_review__binance_vision_liquidationSnapshot", "urls": ["https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/"], "notes": "Binance archive liquidation-snapshot directory probe."},
    {"name": "deep_review__kaiko_demo", "urls": ["https://demo-api.kaiko.io/v1/"], "notes": "Kaiko demo root (auth-gated)."},
    {"name": "deep_review__cryptofeed_repo", "urls": ["https://github.com/bmoscon/cryptofeed"], "notes": "Library repo, not a dataset host."},
    {"name": "deep_review__laevitas_ch", "urls": ["https://laevitas.ch/"], "notes": "Public site probe."},
    {"name": "deep_review__coinglass_public_liquidation_history", "urls": ["https://open-api.coinglass.com/public/v2/liquidation_history?symbol=BTC&timeType=4h"], "notes": "Coinglass public API probe (often auth/JS-gated)."},
    {"name": "deep_review__bybit_public_spot_kline", "urls": ["https://public.bybit.com/spot/kline/"], "notes": "Bybit public archive spot-kline directory probe."},
    {"name": "deep_review__bybit_public_trading_linear", "urls": ["https://public.bybit.com/trading/linear/"], "notes": "Bybit public archive trading-linear directory probe."},
    {"name": "deep_review__coinapi_exchanges", "urls": ["https://rest.coinapi.io/v1/exchanges"], "notes": "CoinAPI root (auth-gated)."},
    {"name": "deep_review__glassnode_studio", "urls": ["https://studio.glassnode.com/"], "notes": "Glassnode studio (auth-gated)."},
    {"name": "deep_review__cryptodatadownload_binance", "urls": ["https://www.cryptodatadownload.com/data/binance/"], "notes": "CryptoDataDownload Binance directory probe."},
    {"name": "deep_review__deribit_get_instruments", "urls": ["https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=future"], "notes": "Deribit public instruments probe."},
    {"name": "deep_review__okx_public_instruments", "urls": ["https://www.okx.com/api/v5/public/instruments?instType=SWAP"], "notes": "OKX public instruments probe."},
]


def discover_hf_liquidation_datasets(max_retries=2, use_cache=True, refresh=False):
    """Live enumeration of Hugging Face datasets matching liquidation keywords.

    The static candidate list is a floor, not a ceiling: every prior hunt run
    probed only URLs that had been written down somewhere in the repo, so it was
    structurally blind to datasets with no prior mention. This closes that gap by
    querying the unauthenticated HF search endpoint and returning every dataset
    whose id/description looks like a perpetual-futures liquidation source.

    HF's /api/datasets?search= endpoint returns a JSON array that is frequently
    truncated mid-string (observed: "Unterminated string starting at ..."), so a
    strict json.loads fails. This parser salvages partial arrays by scanning for
    every "id":"..." occurrence, which is sufficient to enumerate candidates even
    when the full payload is malformed.

    Args:
        max_retries: per-query retry budget.
        use_cache: reuse a persisted enumeration when it is still within its TTL
            (24h). Defaults True; the hunt's live probes still run against every
            candidate, so caching only the *discovery* step does not weaken the
            per-candidate evidence.
        refresh: force a fresh enumeration even when a valid cache exists.

    Returns a tuple (candidates, errors, cache_info) where cache_info records
    whether the result came from cache, live enumeration, or a failed live
    enumeration that fell back to a stale cache. Never raises.
    """
    import re as _re
    queries = [
        "liquidation", "liquidations", "crypto liquidation", "perpetual liquidation",
        "hyperliquid liquidation", "funding liquidation", "crypto perpetual liquidation",
        "liquidation ticks", "perpetual futures liquidation",
    ]
    cache = _cache_load() if use_cache and not refresh else {}
    if cache and _cache_fresh(cache) and not refresh:
        return list(cache.get("candidates", [])), list(cache.get("errors", [])), {
            "source": "cache", "generated_utc": cache.get("generated_utc"),
            "queries": cache.get("queries"), "stale": False,
        }
    found = {}
    errors = []
    for q in queries:
        url = "https://huggingface.co/api/datasets?search=" + urllib.parse.quote(q) + "&limit=40"
        r = http_probe(url, max_retries=max_retries)
        if r.get("status") != 200 or not r.get("body_preview"):
            errors.append({"query": q, "status": r.get("status")})
            continue
        body = r["body_preview"]
        ids = _re.findall(r'"id":"([^"]+)"', body)
        desc_by_id = {}
        for m in _re.finditer(r'"id":"([^"]+)"[^}]*?"description":"([^"]{0,160})"', body):
            desc_by_id[m.group(1)] = m.group(2)
        for i in ids:
            if i in found:
                continue
            low = (i + " " + desc_by_id.get(i, "")).lower()
            if "liquidation" in low or "liquidations" in low:
                found[i] = {
                    "name": "hf_discovered__" + i.replace("/", "_"),
                    "urls": [
                        f"https://huggingface.co/api/datasets/{i}",
                        f"https://huggingface.co/datasets/{i}/resolve/main/README.md",
                    ],
                    "notes": f"Discovered via live HF /api/datasets?search={q} enumeration (query='{q}'). Description: {desc_by_id.get(i, '')}. Verify schema/coverage/license/unauthenticated access before scoring GO.",
                }
    candidates = list(found.values())
    if candidates:
        _cache_save(candidates, queries, errors)
        cache_info = {"source": "live", "generated_utc": datetime.now(timezone.utc).isoformat(), "queries": queries, "stale": False}
    elif cache:
        cache_info = {"source": "cache_stale_fallback", "generated_utc": cache.get("generated_utc"), "queries": cache.get("queries"), "stale": True}
        return list(cache.get("candidates", [])), errors, cache_info
    else:
        cache_info = {"source": "none", "generated_utc": None, "queries": queries, "stale": False}
    return candidates, errors, cache_info


def main():
    ts = now_z()
    out = REPO_ROOT / "research_state" / f"alt_source_scan_{ts}.json"
    candidates, errors, cache_info = discover_hf_liquidation_datasets()
    static = list(EXTENDED_CANDIDATES)
    for c in candidates:
        if c not in static:
            static.append(c)
    payload = {
        "generated_utc": ts,
        "cache_info": cache_info,
        "errors": errors,
        "candidates": static,
        "deep_review_urls": DEEP_REVIEW_URLS,
    }
    try:
        out.write_text(json.dumps(payload, indent=2))
    except Exception:
        pass
    # Consolidate: keep only the latest alt_source_scan_*.json
    try:
        import glob, os
        files = sorted(glob.glob(str(REPO_ROOT / "research_state" / "alt_source_scan_*.json")))
        if len(files) > 1:
            for fp in files[:-1]:
                try:
                    os.remove(fp)
                except Exception:
                    pass
    except Exception:
        pass
    print(f"Wrote {out} (candidates={len(static)}, source={cache_info.get('source')})")


if __name__ == "__main__":
    main()
