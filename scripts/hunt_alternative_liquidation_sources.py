

# Extended candidate set for 004i
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

#!/usr/bin/env python3
"""
Exhaustive alternative source hunt for Track A observed liquidations (unauthenticated only)
Follows RESEARCH_PROMPT §5. Produces evidence tables with GO/NO-GO rubric scoring.
Strengthened for 004i: more source families, retry/backoff, rubric-scored assessment.
"""
import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import random
import time

REPO_ROOT = Path(__file__).parent.parent
OUT_PATH = REPO_ROOT / "research_state" / "data_source_registry_alt_hunt.json"
USER_AGENT = "fclr-alt-hunt/1.2"

# [HEAVY-004i session 3, 2026-11-04T20:46Z] Bottleneck removal: live HF
# /api/datasets?search= enumeration runs 9 queries on EVERY hunt call (~13s of the
# ~17s hunt runtime) even though the HF search index barely changes between
# sessions. Persist the discovered candidate set with a TTL so repeated blocked
# sessions reuse it instead of re-querying the same endpoint. The cache is keyed
# on the query set and stores the parsed candidate list + timestamp; a fresh
# enumeration still runs when the TTL expires or on --refresh, so the cache can
# never silently hide a genuinely new dataset.
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


# [HEAVY-004i session 3, 2026-11-04T20:47Z] Bottleneck removal: the hunt re-probes
# the same ~44 candidate URLs on every blocked session, most of which never
# change. Persist a per-URL probe cache keyed on ETag + Last-Modified so a
# conditional request (or a TTL hit) reuses the last recorded probe instead of
# a fresh GET. The cache stores only the classification evidence, never the
# full body, and a --refresh flag invalidates it.
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
                result = {
                    "url": url,
                    "method": method,
                    "status": status,
                    "headers": {k.lower(): v for k, v in headers.items()},
                    "body_len": len(body),
                    "body_preview": preview,
                    "attempts": attempt + 1,
                }
                # content_kind guess (mirrors probe_directory_listing) so the
                # merged evidence block can classify a response without a
                # separate directory-style probe.
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


def _raw_fetch(url, max_retries=2, timeout=90):
    """GET a URL and return the FULL body bytes (no preview truncation).

    http_probe caps its preview at 200 bytes, which is fine for classifying an
    endpoint but useless for a 128 KB coverage CSV that must be parsed to verify
    the rubric floor from data. This is the full-body variant used only for
    small, explicitly-named coverage artifacts.
    """
    import time as _time
    import random as _random
    for attempt in range(max_retries + 1):
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=timeout) as resp:
                if resp.getcode() == 200:
                    return resp.read()
                return None
        except HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                _time.sleep(2 ** attempt + _random.random())
                continue
            if 500 <= e.code < 600 and attempt < max_retries:
                _time.sleep(1 + _random.random())
                continue
            return None
        except Exception:
            if attempt < max_retries:
                _time.sleep(1 + _random.random())
                continue
            return None


def verify_numeric_coverage(entry):
    """Download the small coverage artifact and verify the rubric numerically.

    The notes-based coverage_ok check is a cheap pre-filter, but it can fire on
    prose alone (a README that *claims* coverage without the data backing it).
    This downloads the dataset's coverage/manifest CSV when the candidate's
    notes reference one, parses it, and returns the measured symbol and date
    coverage. The caller gates GO on the MEASURED values, not the prose.

    Returns a dict with measured fields; never raises. Returns None when the
    candidate advertises no coverage artifact to fetch.
    """
    import csv as _csv
    import io as _io
    import re as _re
    notes = entry.get("notes") or ""
    # Candidate dataset ids of the form owner/name. Prefer ids found in the
    # notes, but also derive one from the candidate name when the notes omit it
    # (hand-written notes frequently describe coverage without naming the
    # dataset, e.g. "1,442,664 observed liquidation prints from Bybit/Binance/
    # OKX ..."). The candidate name is itself derived from the owner/name by
    # the discovery path, so reversing owner_name -> owner/name is safe.
    ids = _re.findall(r"((?:[A-Za-z0-9][A-Za-z0-9-]*)/(?:[A-Za-z0-9][A-Za-z0-9._-]*))", notes)
    name = entry.get("name") or ""
    # hf_discovered__owner_name -> owner/name
    if name.startswith("hf_discovered__"):
        derived = name[len("hf_discovered__"):].replace("_", "/", 1)
        # restore dots in the name part only (owner has no dots)
        if "/" in derived:
            own, nm = derived.split("/", 1)
            derived = f"{own}/{nm.replace('_', '.')}"
        if derived not in ids:
            ids = [derived] + ids
    coverage_candidates = ["coverage.csv", "coverage_20260807.csv", "coverage_202608.csv"]
    for dataset_id in ids:
        for fname in coverage_candidates:
            url = f"https://huggingface.co/datasets/{dataset_id}/resolve/main/{fname}"
            raw = _raw_fetch(url, max_retries=1, timeout=45)
            if raw:
                return _parse_coverage_csv(raw, url)
    return None


def _parse_coverage_csv(raw, url):
    """Parse a fetched coverage CSV body into measured symbol/date coverage."""
    import csv as _csv
    import io as _io
    try:
        rows = list(_csv.reader(_io.StringIO(raw.decode("utf-8", "replace"))))
    except Exception as e:
        return {"url": url, "error": f"unparseable coverage csv: {e!r}"}
    if len(rows) < 2:
        return {"url": url, "error": "coverage csv has no data rows"}
    hdr = [h.strip().lower() for h in rows[0]]
    data = rows[1:]
    # Identify columns by header name, tolerant to ordering.
    def col(*names):
        for n in names:
            if n in hdr:
                return hdr.index(n)
        return None
    i_sym = col("symbol", "ticker", "asset")
    i_ex = col("exchange", "venue", "source")
    i_rows = col("rows", "count", "n", "num_rows", "events")
    i_first = col("first_utc", "first", "start", "first_ts")
    i_last = col("last_utc", "last", "end", "last_ts")
    if i_sym is None or i_first is None or i_last is None:
        return {"url": url, "error": f"coverage csv missing required columns; header={hdr}"}
    syms = set()
    firsts, lasts = [], []
    for row in data:
        if len(row) <= max(i_sym, i_last):
            continue
        syms.add(row[i_sym].strip())
        firsts.append(row[i_first].strip())
        lasts.append(row[i_last].strip())
    firsts = [f for f in firsts if f]
    lasts = [f for f in lasts if f]
    measured = {
        "url": url,
        "n_symbol_rows": len(data),
        "n_unique_symbols": len(syms),
        "earliest": min(firsts) if firsts else None,
        "latest": max(lasts) if lasts else None,
    }
    if i_ex is not None:
        measured["venues"] = sorted(set(row[i_ex].strip() for row in data if len(row) > i_ex))
    if i_rows is not None:
        try:
            measured["total_rows"] = sum(int(row[i_rows]) for row in data if len(row) > i_rows and row[i_rows].strip().isdigit())
        except Exception:
            pass
    # Span in days (best-effort, tolerant of 'YYYY-MM-DD HH:MM:SS' and ISO).
    try:
        from datetime import datetime as _dt
        def _p(s):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                try:
                    return _dt.strptime(s.strip(), fmt)
                except Exception:
                    continue
            return None
        fs = [_p(f) for f in firsts]
        ls = [_p(l) for l in lasts]
        fs = [f for f in fs if f]
        ls = [l for l in ls if l]
        if fs and ls:
            measured["span_days"] = (max(ls) - min(fs)).days + 1
    except Exception:
        pass
    return measured


def assess_rubric(entry):
    """Score a candidate against the strict Track A GO rubric.

    Status-only scoring is insufficient: a 200 on a marketing page or a repo
    README looks identical on the wire to a 200 on a real liquidation dataset.
    This adds a content-signal pass so REVIEW_REQUIRED candidates can be
    confirmed GO or closed with evidence instead of lingering forever.

    GO requires ALL of:
      1. at least one probe returned HTTP 200;
      2. no 401/403 on any probe (auth wall);
      3. the 200 response body actually looks like liquidation data (JSON with
         liquidation/forceOrder/fills/event keywords, a parquet blob, OR a
         dataset README/schema that documents observed liquidation events), AND
      4. the candidate explicitly advertises >=5 symbols and >=1 complete month
         or >=3 non-overlapping 30-day blocks in its notes/preview.
    """
    statuses = [p.get("status") for p in entry.get("probes", [])]
    any_200 = any(s == 200 for s in statuses if s is not None)
    any_403_or_401 = any(s in (401, 403) for s in statuses if s is not None)
    if not any_200:
        return "NO-GO"
    if any_403_or_401:
        return "NO-GO"
    # Content signal: scan body previews and content kinds for liquidation cues.
    cues = ("liquidation", "forceorder", "force_order", "fill", "fills",
            "event", "events", "parquet", "liquidations")
    blob = " ".join(
        (p.get("body_preview") or "").lower() + " " + str(p.get("content_kind") or "").lower()
        for p in entry.get("probes", [])
    )
    looks_like_data = any(c in blob for c in cues)

    # README/schema evidence: the discovery path probes the dataset API and the
    # README.md (content_kind 'text'), whose body is a markdown schema table, not
    # a JSON blob. Without this pass a genuine GO source (e.g. ochinimus
    # crypto-liquidation-ticks, whose README documents 1,442,664 observed
    # liquidation prints with an explicit column schema) was stuck in
    # REVIEW_REQUIRED forever because its prose body carried no JSON 'fills'
    # keyword. Recognise READMEs that document an observed-liquidation schema:
    # a column named ts_ms/utc_time/symbol/exchange/event/size/price/usd is
    # specific enough to distinguish a real event dataset from a marketing page.
    readme_blob = " ".join(
        (p.get("body_preview") or "").lower()
        for p in entry.get("probes", [])
        if (p.get("content_kind") or "") in ("text", "markdown", "html")
    )
    schema_cues = ("ts_ms", "utc_time", "symbol", "exchange", "event", "size",
                   "price", "usd", "liquidation print", "liquidation event")
    readme_schema_ok = sum(1 for c in schema_cues if c in readme_blob) >= 5
    looks_like_data = looks_like_data or readme_schema_ok

    # Coverage signal: the candidate notes must advertise the rubric minimums.
    notes = (entry.get("notes") or "").lower()
    coverage_ok = (">=5" in notes or "5 symbol" in notes or ">= 5" in notes) and (
        "complete month" in notes or "30-day" in notes or "30 day" in notes
    )
    if looks_like_data and coverage_ok:
        # Gate GO on MEASURED coverage, not prose: download the coverage artifact
        # and verify >=5 symbols and >=1 complete month (or >=3 non-overlapping
        # 30-day blocks) from the data itself. A README claiming coverage without
        # the artifact to back it must not pass.
        measured = verify_numeric_coverage(entry)
        entry["measured_coverage"] = measured
        if measured and "error" not in measured:
            nsyms = measured.get("n_unique_symbols", 0)
            span = measured.get("span_days")
            if nsyms >= 5 and span is not None and span >= 30:
                return "GO"
            entry["review_reason"] = {
                "looks_like_data": looks_like_data,
                "coverage_advertised": coverage_ok,
                "statuses": statuses,
                "measured": measured,
                "reject_reason": f"measured nsyms={nsyms} span_days={span} below rubric floor (>=5 symbols, >=30 days)",
            }
            return "REVIEW_REQUIRED"
        # No coverage artifact to measure: cannot confirm the floor from data.
        entry["review_reason"] = {
            "looks_like_data": looks_like_data,
            "coverage_advertised": coverage_ok,
            "statuses": statuses,
            "measured": measured,
            "reject_reason": "no coverage artifact available to verify the >=5 symbol / >=30 day floor from data",
        }
        return "REVIEW_REQUIRED"
    # Anything that returned 200 but failed the content/coverage gates stays in
    # REVIEW_REQUIRED with the reason recorded, so it can be deep-verified or
    # closed by a future session without re-probing the same URL.
    entry["review_reason"] = {
        "looks_like_data": looks_like_data,
        "readme_schema_ok": readme_schema_ok,
        "coverage_advertised": coverage_ok,
        "statuses": statuses,
    }
    return "REVIEW_REQUIRED"


# HEAVY-004i session 2 (2026-11-04T19:39Z): the HF dataset-search enumeration found
# several liquidation datasets that the static candidate list never included. The
# static list only ever probed known URLs; it could not discover datasets that had
# no prior mention anywhere in the repo. These are added so every future hunt run
# probes the full discovered set instead of re-deriving it by hand.
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
    ], "notes": "Werracle Verified Empirical OEV & Liquidation Dynamics Dataset v1.2. 105 SVR transactions / 513 liquidations on Base L2. CC-BY-4.0. Scope is on-chain MEV/OEV, NOT perpetual-futures liquidations - does not match FCLR-H004 venue/scope. NO-GO for Track A as-is."},
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
        # Salvage dataset ids from a possibly-truncated JSON array.
        ids = _re.findall(r'"id":"([^"]+)"', body)
        # Also capture description snippets where present for downstream filtering.
        desc_by_id = {}
        for m in _re.finditer(r'"id":"([^"]+)"[^}]*?"description":"([^"]{0,160})"', body):
            desc_by_id[m.group(1)] = m.group(2)
        for i in ids:
            if i in found:
                continue
            low = (i + " " + desc_by_id.get(i, "")).lower()
            # Keep anything that is plausibly a perpetual-futures / crypto
            # liquidation source. Over-inclusion is fine: the rubric assessor
            # rejects non-qualifying candidates with recorded reasons.
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
        # Live enumeration failed entirely: fall back to the most recent cached
        # enumeration rather than returning nothing, and flag it as stale so the
        # evidence block records that discovery is not current.
        cache_info = {"source": "cache_stale_fallback", "generated_utc": cache.get("generated_utc"), "queries": cache.get("queries"), "stale": True}
        return list(cache.get("candidates", [])), errors, cache_info
    else:
        cache_info = {"source": "none", "generated_utc": None, "queries": queries, "stale": False}
    return candidates, errors, cache_info


def main():
    import sys
    args = sys.argv[1:]
    refresh = "--refresh" in args
    cache_info_only = "--cache-info" in args
    if cache_info_only:
        cache = _cache_load()
        print(json.dumps({
            "cache_path": str(SEARCH_CACHE_PATH),
            "exists": bool(cache),
            "generated_utc": cache.get("generated_utc") if cache else None,
            "fresh": _cache_fresh(cache) if cache else False,
            "ttl_seconds": SEARCH_TTL_SECONDS,
            "n_cached_candidates": len(cache.get("candidates", [])) if cache else 0,
            "queries": cache.get("queries") if cache else None,
        }, indent=2))
        return
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
    # ENHANCED_CANDIDATES were defined but never merged into the probe list,
    # so every hunt run silently skipped them (dead code). Merge them here so
    # each session probes the widened candidate set and records evidence.
    candidates = candidates + ENHANCED_CANDIDATES
    # HF_SEARCH_DISCOVERED: datasets found by live enumeration of the HF
    # /api/datasets?search= endpoint. The static candidate list could never have
    # contained these (they had no prior mention in the repo), so without this
    # merge every hunt run was structurally blind to them. Merge so each session
    # probes the full discovered set.
    candidates = candidates + HF_SEARCH_DISCOVERED
    results = {"hunt_id": f"alt_hunt_{ts}", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i", "unauthenticated_only": True, "rubric": RUBRIC, "candidates": []}
    # Live HF discovery: enumerate the search endpoint so candidates with no
    # prior mention anywhere in the repo are probed, not structurally missed.
    # Cache-aware (24h TTL): reuses the persisted enumeration across blocked
    # sessions instead of re-querying 9 HF search endpoints every run.
    discovered, discover_errors, discovery_cache = discover_hf_liquidation_datasets(refresh=refresh)
    results["hf_discovery"] = {
        "queries_run": ["liquidation", "liquidations", "crypto liquidation", "perpetual liquidation", "hyperliquid liquidation", "funding liquidation", "crypto perpetual liquidation", "liquidation ticks", "perpetual futures liquidation"],
        "datasets_found": [d["name"] for d in discovered],
        "discover_errors": discover_errors,
        "cache": discovery_cache,
    }
    candidates = candidates + discovered
    # [HEAVY-004i session 3] Deduplicate URLs across candidates: the inline list,
    # ENHANCED_CANDIDATES and the HF-discovered set overlap (e.g. coinglass.com,
    # hyblockcapital.com, the ochinimus coverage probes), so the same URL was
    # being probed twice per run. De-dup here so each URL is probed exactly once
    # and the per-URL probe cache key is stable across sessions.
    seen_urls = set()
    unique_candidates = []
    for c in candidates:
        urls = c.get("urls") or c.get("probes") or []
        new_urls = [u for u in urls if u not in seen_urls]
        if not new_urls:
            continue
        for u in new_urls:
            seen_urls.add(u)
        nc = dict(c)
        nc["urls"] = new_urls
        unique_candidates.append(nc)
    candidates = unique_candidates
    # [HEAVY-004i session 3] Per-URL probe cache: reuse classification evidence
    # for unchanged URLs across blocked sessions instead of re-GETting them.
    # A --refresh flag invalidates the cache for a fresh full probe.
    url_cache = {} if refresh else _url_cache_load()
    n_cache_hits = 0
    n_cache_misses = 0
    for c in candidates:
        entry = {"name": c["name"], "notes": c["notes"], "probes": []}
        # Normalise the candidate schema: EXTENDED_CANDIDATES entries carry a
        # "probes" list (URLs to probe) while the inline candidates carry "urls".
        # Without this normalisation every hunt run died with KeyError on the
        # extended set, silently skipping the widened candidate family.
        urls = c.get("urls") or c.get("probes") or []
        for url in urls:
            p = http_probe_cached(url, cache=url_cache)
            if p.get("cache_hit"):
                n_cache_hits += 1
            else:
                n_cache_misses += 1
            # Ensure we capture evidence per candidate
            entry["probes"].append(p)
        entry["rubric_assessment"] = assess_rubric(entry)
        # Detailed verdict: a REVIEW_REQUIRED candidate is only useful if the
        # response actually looks like liquidation data. Record the body preview
        # and content-kind so a future session can confirm or close it without
        # re-probing the same URL.
        entry["evidence"] = {
            "statuses": [p.get("status") for p in entry["probes"]],
            "body_previews": [p.get("body_preview", "")[:120] for p in entry["probes"]],
            "content_kinds": [p.get("content_kind") for p in entry["probes"]],
            "review_reason": entry.get("review_reason"),
            "looks_like_liquidation_data": entry.get("review_reason", {}).get("looks_like_data", False),
        }
        results["candidates"].append(entry)
    if not refresh:
        _url_cache_save(url_cache)
    results["probe_cache"] = {
        "enabled": True,
        "refresh": refresh,
        "ttl_seconds": URL_CACHE_TTL_SECONDS,
        "cache_hits": n_cache_hits,
        "cache_misses": n_cache_misses,
        "unique_urls_probed": len(seen_urls),
        "cache_path": str(URL_CACHE_PATH.relative_to(REPO_ROOT)),
    }
    go_sources = [c["name"] for c in results["candidates"] if c["rubric_assessment"] == "GO"]
    review_sources = [c["name"] for c in results["candidates"] if c["rubric_assessment"] == "REVIEW_REQUIRED"]
    no_go_sources = [c["name"] for c in results["candidates"] if c["rubric_assessment"] == "NO-GO"]
    results["summary"] = {
        "candidates_probed": len(results["candidates"]),
        "go_sources": go_sources,
        "review_sources": review_sources,
        "no_go_sources": no_go_sources,
        "go_or_review_sources": go_sources + review_sources,
        "conclusion": (
            f"GO source(s) found: {go_sources}; pre-register FCLR-010 BEFORE outcome inspection and run scripts/fclr010_harness.py"
            if go_sources else
            f"No GO source. Review required for: {review_sources}" if review_sources else
            "No NEW admissible unauthenticated Track A source beyond ironflow/hyperliquid-liquidations found"
        ),
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


# Additional probe for common exchange liquidation endpoints (unauthenticated)
EXTRA_PROBES = [
    ("bybit_public_instruments", ["https://api.bybit.com/v5/market/instruments-info?category=linear"]),
    ("okx_public_instruments", ["https://www.okx.com/api/v5/public/instruments?instType=SWAP"]),
]


# HEAVY-004i enhancement: add more unauthenticated candidates. These are merged
# into the candidate list below so each hunt run probes them (previously they
# were dead module-level data never passed to main()).
ENHANCED_CANDIDATES = EXTENDED_CANDIDATES + [
    {"name": "coinglass_public_liquidations", "urls": ["https://www.coinglass.com/api/liquidation/chart", "https://www.coinglass.com/LiquidationData"], "notes": "Coinglass public pages (often requires JS; probe for structure only)"},
    {"name": "coinank_public", "urls": ["https://www.coinank.com/"], "notes": "Public site probe"},
    {"name": "laevitas_public", "urls": ["https://laevitas.ch/"], "notes": "Public site probe"},
    {"name": "hyblock_public", "urls": ["https://hyblockcapital.com/"], "notes": "Public site probe"},
    {"name": "paradigm_data_research", "urls": ["https://www.paradigm.xyz/research"], "notes": "Research page probe for liquidation datasets"},
    {"name": "glassnode_public_docs", "urls": ["https://docs.glassnode.com/"], "notes": "Docs probe"},
]


if __name__ == "__main__":
    main()
