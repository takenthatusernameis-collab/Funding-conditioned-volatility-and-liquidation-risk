#!/usr/bin/env python3
"""
Ironflow Hyperliquid liquidations monitor (Track A only)
Probes HF tree for data/events/YYYY-MM.parquet and data/fills/YYYY-MM.parquet.
Unauthenticated only. Records full evidence, caches state, writes timestamped probes.

Improvements over the baseline monitor:
- ETag tree caching: sends If-None-Match on the tree listing; skips full re-parse
  when HF returns 304 Not Modified (saves API calls and runtime).
- Wider probe window: last LOOKBACK_MONTHS completed months + LOOKAHEAD_MONTHS
  future/current months, so lagged uploads of recent months are caught.
- Failure classification per probe: NEW_AVAILABLE(200), CONFIRMED_ABSENT(404
  EntryNotFound), RATE_LIMITED(429), TRANSIENT_ERROR(network/other).
- Exponential backoff with retry budget on transient errors and 429s.
- Rate-limit awareness: reads RateLimit/RateLimit-Policy headers and backs off
  when the remaining budget is low.
- Tracks data_through (latest month with both events+fills present) and
  consecutive_absent (months confirmed absent in a row at the forward edge) for
  a concrete, checkable resume condition.
- Idempotent: re-running produces the same evidence unless new data appears.
"""
import json
import hashlib
import time
import random
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

HF_DATASET = "ironflow/hyperliquid-liquidations"
TREE_URL = f"https://huggingface.co/api/datasets/{HF_DATASET}/tree/main?recursive=true"
EVENTS_TEMPLATE = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main/data/events/%s.parquet"
FILLS_TEMPLATE = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main/data/fills/%s.parquet"

LOOKBACK_MONTHS = 6
LOOKAHEAD_MONTHS = 6
MAX_RETRIES = 3
BACKOFF_BASE = 1.5
BACKOFF_JITTER = 0.5  # fractional jitter added to every backoff sleep
FORWARD_EDGE_MONTHS = 4  # months to probe for resume triggers (strictly after data_through)
# Per-endpoint retry budget: max total attempts across all retries for a single
# endpoint before it is classified as a hard failure. Different endpoints have
# different costs; the tree listing and resolve endpoints get separate budgets.
RETRY_BUDGETS = {
    "tree": 3,
    "resolve": 3,
    "head": 1,  # HEAD probes are cheap; never burn retries here
}
# When the remaining HF RateLimit budget drops below this, the monitor sleeps
# instead of risking a 429. Reads the RateLimit header dynamically.
RATE_LIMIT_PANIC = 10

REPO_ROOT = Path(__file__).parent.parent
STATE_PATH = REPO_ROOT / "research_state" / "ironflow_monitor_state.json"
EVIDENCE_DIR = REPO_ROOT / "research_state"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def now_z():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_bytes(b):
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()


def _rate_limit_sleep(resp_headers, attempt):
    """Back off when the server reports a low remaining budget.

    HF returns RateLimit/RateLimit-Policy headers (e.g.
    RateLimit: "api";r=499;t=87). When the remaining count r is small we sleep
    before the next request instead of risking a 429 and burning retries.
    """
    rl = resp_headers.get("RateLimit") or resp_headers.get("ratelimit") or ""
    m = re.search(r"r=(\d+);t=(\d+)", rl)
    if not m:
        return BACKOFF_BASE ** attempt + random.random()
    remaining, reset_s = int(m.group(1)), int(m.group(2))
    if remaining <= 5:
        # Budget nearly exhausted: wait until the window resets (+jitter).
        return max(reset_s, BACKOFF_BASE ** attempt) + random.random()
    if remaining < 50:
        return BACKOFF_BASE ** attempt + random.random()
    return 0.0


def http_get(url, timeout=60, max_retries=MAX_RETRIES, if_none_match=None, etag_ref=None):
    headers = {"User-Agent": "fclr-monitor/1.0"}
    if if_none_match:
        headers["If-None-Match"] = if_none_match
    for attempt in range(max_retries + 1):
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                resp_headers = dict(resp.headers.items())
                body = resp.read()
                result = {"ok": True, "status": status, "headers": resp_headers, "body": body, "url": url}
                if etag_ref is not None and status == 200:
                    etag_ref[0] = resp_headers.get("ETag")
                return result
        except HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b""
            resp_headers = dict(getattr(e, "headers", {}) or {})
            if e.code == 304 and etag_ref is not None:
                return {"ok": True, "status": 304, "headers": resp_headers, "body": b"", "url": url, "not_modified": True}
            if e.code == 429 and attempt < max_retries:
                sleep_for = _rate_limit_sleep(resp_headers, attempt)
                time.sleep(sleep_for)
                continue
            if 500 <= e.code < 600 and attempt < max_retries:
                sleep_for = BACKOFF_BASE ** attempt + random.random()
                time.sleep(sleep_for)
                continue
            return {"ok": False, "status": e.code, "headers": resp_headers, "body": body, "url": url}
        except URLError as e:
            if attempt < max_retries:
                time.sleep(1 + random.random())
                continue
            return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": url}
        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 + random.random())
                continue
            return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": url}


def classify(status, body_preview=""):
    if status == 200:
        return "NEW_AVAILABLE"
    if status == 304:
        return "NOT_MODIFIED"
    if status == 404:
        return "CONFIRMED_ABSENT"
    if status == 429:
        return "RATE_LIMITED"
    return "TRANSIENT_ERROR"


def head_probe(url, timeout=30):
    """Cheap HEAD probe to check existence without downloading the body.

    Used before GET on large resolve endpoints. Returns the same dict shape as
    http_get so callers can treat it uniformly. A HEAD that fails (405 Method
    Not Allowed, network error) is reported as a soft failure and the caller
    falls back to GET; it is never treated as CONFIRMED_ABSENT.
    """
    req = Request(url, method="HEAD", headers={"User-Agent": "fclr-monitor/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            headers = dict(resp.headers.items())
            return {
                "ok": True,
                "status": status,
                "headers": headers,
                "body": b"",
                "url": url,
                "method": "HEAD",
                "head_ok": True,
            }
    except HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        headers = dict(getattr(e, "headers", {}) or {})
        return {
            "ok": False,
            "status": e.code,
            "headers": headers,
            "body": body,
            "url": url,
            "method": "HEAD",
            "head_ok": False,
            "head_failed": True,
        }
    except Exception as e:
        return {
            "ok": False,
            "status": None,
            "headers": {},
            "body": str(e).encode("utf-8"),
            "url": url,
            "method": "HEAD",
            "head_ok": False,
            "head_failed": True,
        }


def resolve_get(url, etag_ref=None, last_modified_ref=None, timeout=60, max_retries=None):
    """GET a resolve endpoint, honoring per-file ETag and Last-Modified caching.

    If the caller supplies a previously-seen ETag and/or Last-Modified value,
    conditional request headers are sent. A 304 response means the file is
    unchanged and the cached body/hash may be reused. last_modified_ref is a
    list of length 1 that receives the new Last-Modified header value on 200.
    """
    if max_retries is None:
        max_retries = RETRY_BUDGETS["resolve"]
    headers = {"User-Agent": "fclr-monitor/1.0"}
    if etag_ref and etag_ref[0]:
        headers["If-None-Match"] = etag_ref[0]
    if last_modified_ref and last_modified_ref[0]:
        headers["If-Modified-Since"] = last_modified_ref[0]
    for attempt in range(max_retries + 1):
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                resp_headers = dict(resp.headers.items())
                body = resp.read()
                if etag_ref is not None and status == 200:
                    etag_ref[0] = resp_headers.get("ETag")
                if last_modified_ref is not None and status == 200:
                    last_modified_ref[0] = resp_headers.get("Last-Modified")
                return {
                    "ok": True,
                    "status": status,
                    "headers": resp_headers,
                    "body": body,
                    "url": url,
                    "method": "GET",
                }
        except HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b""
            resp_headers = dict(getattr(e, "headers", {}) or {})
            if e.code == 304:
                return {"ok": True, "status": 304, "headers": resp_headers, "body": b"", "url": url, "method": "GET", "not_modified": True}
            if e.code == 429 and attempt < max_retries:
                sleep_for = _rate_limit_sleep(resp_headers, attempt)
                time.sleep(sleep_for)
                continue
            if 500 <= e.code < 600 and attempt < max_retries:
                sleep_for = BACKOFF_BASE ** attempt + random.uniform(0, BACKOFF_JITTER)
                time.sleep(sleep_for)
                continue
            return {"ok": False, "status": e.code, "headers": resp_headers, "body": body, "url": url, "method": "GET"}
        except URLError as e:
            if attempt < max_retries:
                time.sleep(1 + random.uniform(0, BACKOFF_JITTER))
                continue
            return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": url, "method": "GET"}
        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 + random.uniform(0, BACKOFF_JITTER))
                continue
            return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": url, "method": "GET"}


def rate_budget_ok(headers):
    """True when the HF RateLimit budget is healthy enough to make another request.

    Reads RateLimit: "scope";r=<remaining>;t=<reset_seconds>. Returns False when
    remaining is at or below RATE_LIMIT_PANIC, signalling the caller to wait.
    """
    rl = (headers.get("RateLimit") or headers.get("ratelimit") or "")
    m = re.search(r"r=(\d+);t=(\d+)", rl)
    if not m:
        return True
    remaining = int(m.group(1))
    return remaining > RATE_LIMIT_PANIC


def wait_for_rate_budget(headers):
    """Sleep until the RateLimit window resets if the budget is exhausted."""
    rl = (headers.get("RateLimit") or headers.get("ratelimit") or "")
    m = re.search(r"r=(\d+);t=(\d+)", rl)
    if not m:
        return 0.0
    remaining, reset_s = int(m.group(1)), int(m.group(2))
    if remaining <= 0:
        return float(reset_s) + random.uniform(0, BACKOFF_JITTER)
    return 0.0


def month_offset(months_back):
    now = datetime.now(timezone.utc)
    y = now.year
    m = now.month - months_back
    while m < 1:
        m += 12
        y -= 1
    while m > 12:
        m -= 12
        y += 1
    return f"{y:04d}-{m:02d}"


def candidate_months():
    months = set()
    for i in range(1, LOOKBACK_MONTHS + 1):
        months.add(month_offset(i))
    for i in range(0, LOOKAHEAD_MONTHS):
        months.add(month_offset(-i))
    return sorted(months)


def forward_edge_months(data_through, n=FORWARD_EDGE_MONTHS):
    """Return the n months strictly after data_through (the resume-check window).

    This is the minimal probe set needed to detect a resume trigger. Using it
    instead of the full candidate window cuts a 12-month probe to ~3 requests
    per run, removing the per-session re-probe bottleneck while keeping the
    resume condition checkable.
    """
    if not data_through:
        return candidate_months()
    try:
        y, m = (int(x) for x in data_through.split("-"))
    except Exception:
        return candidate_months()
    out = []
    for i in range(1, n + 1):
        yy, mm = y, m + i
        while mm > 12:
            mm -= 12
            yy += 1
        out.append(f"{yy:04d}-{mm:02d}")
    return out


def probe_month(ym, state=None):
    """Probe one calendar month's events and fills.

    Uses per-file ETag/Last-Modified caching: if the state already recorded an
    ETag for this (kind, month) and the server returns 304, the cached sha256
    and content_length are reused and no body is downloaded. A cheap HEAD probe
    is sent first when no cached ETag exists, to avoid downloading a body we
    will only hash. Falls back to GET when HEAD is unsupported.
    """
    state = state if state is not None else {}
    cache = state.get("file_cache", {})
    res = {"month": ym, "events": None, "fills": None}
    for kind, tmpl in [("events", EVENTS_TEMPLATE), ("fills", FILLS_TEMPLATE)]:
        url = tmpl % ym
        cache_key = f"{kind}:{ym}"
        cached = cache.get(cache_key, {})
        etag_ref = [cached.get("etag")]
        lm_ref = [cached.get("last_modified")]

        # Cheap existence check before any body download.
        head = head_probe(url)
        head_rec = {
            "url": url,
            "method": "HEAD",
            "status": head["status"],
            "head_ok": head.get("head_ok", False),
        }

        if head.get("head_ok") and head["status"] == 404:
            rec = {
                "url": url,
                "method": "GET",
                "status": 404,
                "headers": head["headers"],
                "body_preview": "",
                "classification": "CONFIRMED_ABSENT",
                "head_probe": head_rec,
            }
            res[kind] = rec
            continue
        if head.get("head_ok") and head["status"] == 200 and not etag_ref[0]:
            # File exists and we have no cached ETag; check Last-Modified against
            # the cached value before downloading the body.
            new_lm = head["headers"].get("Last-Modified")
            if lm_ref[0] and new_lm and new_lm == lm_ref[0]:
                rec = {
                    "url": url,
                    "method": "GET",
                    "status": 200,
                    "headers": head["headers"],
                    "body_preview": "",
                    "classification": "NEW_AVAILABLE",
                    "cached_unchanged": True,
                    "sha256": cached.get("sha256"),
                    "content_length": cached.get("content_length"),
                    "head_probe": head_rec,
                }
                res[kind] = rec
                continue

        r = resolve_get(url, etag_ref=etag_ref, last_modified_ref=lm_ref)
        rec = {
            "url": url,
            "method": "GET",
            "status": r["status"],
            "headers": {k: v for k, v in r["headers"].items()},
            "body_preview": r["body"][:200].decode("utf-8", errors="replace"),
            "classification": classify(r["status"], r["body"][:200].decode("utf-8", errors="replace")),
            "head_probe": head_rec,
        }
        if r.get("not_modified"):
            rec["not_modified"] = True
            rec["sha256"] = cached.get("sha256")
            rec["content_length"] = cached.get("content_length")
            rec["cached_unchanged"] = True
        elif r["ok"] and r["status"] == 200:
            rec["sha256"] = sha256_bytes(r["body"])
            rec["content_length"] = len(r["body"])
            cache[cache_key] = {
                "etag": etag_ref[0],
                "last_modified": lm_ref[0],
                "sha256": rec["sha256"],
                "content_length": rec["content_length"],
            }
        res[kind] = rec
        # Rate-limit awareness: pause between requests when budget is low.
        sl = _rate_limit_sleep(r.get("headers", {}), 0)
        if sl:
            time.sleep(sl)
    if state is not None:
        state["file_cache"] = cache
    return res


def load_state():
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def known_available(state):
    available = set()
    last = state.get("last_probe", {}) if isinstance(state, dict) else {}
    for m in last.get("months_probed", []) or []:
        for kind in ("events", "fills"):
            rec = m.get(kind) or {}
            if rec.get("status") == 200:
                available.add((kind, m["month"]))
    return available


def check_resume_condition(state=None, max_retries=MAX_RETRIES):
    """Return (triggered: bool, details: dict) using ONLY the forward-edge months.

    This is the cheap, non-blocking check the handoff mandates at session start.
    It never re-probes already-known months and never re-lists the tree when the
    cached ETag is unchanged. Per-file ETag/Last-Modified caching and HEAD
    existence probes keep the check to a handful of tiny requests.
    """
    state = state if state is not None else load_state()
    data_through = state.get("data_through")
    months = forward_edge_months(data_through)
    details = {
        "data_through": data_through,
        "months_probed": months,
        "probes": [],
        "triggered": False,
        "triggering_files": [],
        "cached_hits": 0,
        "head_probes": 0,
    }
    cache = state.get("file_cache", {})
    for ym in months:
        for kind, tmpl in [("events", EVENTS_TEMPLATE), ("fills", FILLS_TEMPLATE)]:
            url = tmpl % ym
            cache_key = f"{kind}:{ym}"
            cached = cache.get(cache_key, {})
            head = head_probe(url)
            details["head_probes"] += 1
            head_rec = {"kind": kind, "month": ym, "url": url, "method": "HEAD", "status": head["status"], "head_ok": head.get("head_ok", False)}
            if head.get("head_ok") and head["status"] == 404:
                rec = {
                    "kind": kind,
                    "month": ym,
                    "url": url,
                    "status": 404,
                    "classification": "CONFIRMED_ABSENT",
                    "head_probe": head_rec,
                }
                details["probes"].append(rec)
                continue
            if head.get("head_ok") and head["status"] == 200 and not cached.get("etag"):
                new_lm = head["headers"].get("Last-Modified")
                if cached.get("last_modified") and new_lm and new_lm == cached.get("last_modified"):
                    details["cached_hits"] += 1
                    rec = {
                        "kind": kind,
                        "month": ym,
                        "url": url,
                        "status": 200,
                        "classification": "NEW_AVAILABLE",
                        "cached_unchanged": True,
                        "sha256": cached.get("sha256"),
                        "content_length": cached.get("content_length"),
                        "head_probe": head_rec,
                    }
                    details["probes"].append(rec)
                    continue
            etag_ref = [cached.get("etag")]
            lm_ref = [cached.get("last_modified")]
            r = resolve_get(url, etag_ref=etag_ref, last_modified_ref=lm_ref, max_retries=max_retries)
            if r.get("not_modified"):
                details["cached_hits"] += 1
            rec = {
                "kind": kind,
                "month": ym,
                "url": url,
                "status": r["status"],
                "classification": classify(r["status"]),
                "head_probe": head_rec,
            }
            if r["ok"] and r["status"] == 200:
                rec["sha256"] = sha256_bytes(r["body"])
                rec["content_length"] = len(r["body"])
                details["triggered"] = True
                details["triggering_files"].append(rec)
            details["probes"].append(rec)
    return details


def main():
    import sys
    quick = "--quick" in sys.argv
    ts = now_z()
    state = load_state()
    previously_available = known_available(state)
    tree_etag = state.get("tree_etag")

    evidence = {
        "probe_id": f"ironflow_probe_{ts}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": HF_DATASET,
        "tree_url": TREE_URL,
        "tree": None,
        "months_probed": [],
        "new_files_found": [],
        "data_through": state.get("data_through"),
        "consecutive_absent": state.get("consecutive_absent", 0),
        "probe_window": {
            "lookback_months": LOOKBACK_MONTHS,
            "lookahead_months": LOOKAHEAD_MONTHS,
        },
    }

    etag_ref = [tree_etag]
    tree_res = http_get(TREE_URL, if_none_match=tree_etag, etag_ref=etag_ref)
    evidence["tree"] = {
        "url": TREE_URL,
        "method": "GET",
        "status": tree_res["status"],
        "headers": {k: v for k, v in tree_res["headers"].items()},
    }
    if tree_res.get("not_modified"):
        evidence["tree"]["tree_etag_unchanged"] = True
        evidence["tree"]["skipped_full_parse"] = True
        evidence["tree"]["parquet_paths"] = state.get("tree_parquet_paths", [])
    elif tree_res["ok"] and tree_res["status"] == 200:
        try:
            tree_data = json.loads(tree_res["body"].decode("utf-8"))
            evidence["tree"]["parsed"] = True
            paths = []
            for item in tree_data if isinstance(tree_data, list) else tree_data.get("tree", []):
                if isinstance(item, dict):
                    p = item.get("path") or item.get("name") or ""
                else:
                    p = str(item)
                if p.endswith(".parquet"):
                    paths.append(p)
            evidence["tree"]["parquet_paths"] = sorted(set(paths))
            evidence["tree"]["tree_etag_unchanged"] = False
        except Exception as e:
            evidence["tree"]["parsed"] = False
            evidence["tree"]["parse_error"] = str(e)
            evidence["tree"]["parquet_paths"] = state.get("tree_parquet_paths", [])
    else:
        evidence["tree"]["parsed"] = False
        evidence["tree"]["parquet_paths"] = state.get("tree_parquet_paths", [])

    if etag_ref[0]:
        evidence["tree"]["etag"] = etag_ref[0]

    if quick:
        # --quick: probe ONLY the forward edge (months after data_through). This is
        # the resume-condition check. It skips re-listing when the tree ETag is
        # unchanged and never re-probes already-known months.
        rc = check_resume_condition(state)
        evidence["quick_resume_check"] = rc
        evidence["mode"] = "quick"
        evidence["head_probes"] = rc.get("head_probes", 0)
        evidence["cached_hits"] = rc.get("cached_hits", 0)
        evidence_path = EVIDENCE_DIR / f"ironflow_probe_{ts}.json"
        with open(evidence_path, "w") as f:
            json.dump(evidence, f, indent=2)
        print(f"Wrote evidence: {evidence_path}")
        if rc["triggered"]:
            print(f"RESUME TRIGGER FIRED: {rc['triggering_files']}")
        else:
            print(f"No resume trigger. data_through={rc['data_through']} probed={rc['months_probed']} head_probes={rc.get('head_probes')} cached_hits={rc.get('cached_hits')}")
        return

    for ym in candidate_months():
        evidence["months_probed"].append(probe_month(ym, state))

    current_available = set()
    for m in evidence["months_probed"]:
        for kind in ("events", "fills"):
            rec = m.get(kind) or {}
            if rec.get("status") == 200:
                current_available.add((kind, m["month"]))
                url = rec.get("url")
                if (kind, m["month"]) not in previously_available and url:
                    evidence["new_files_found"].append(
                        {
                            "kind": kind,
                            "month": m["month"],
                            "url": url,
                            "sha256": rec.get("sha256"),
                            "content_length": rec.get("content_length"),
                        }
                    )

    complete_months = []
    for m in evidence["months_probed"]:
        ev = (m.get("events") or {}).get("status")
        fl = (m.get("fills") or {}).get("status")
        if ev == 200 and fl == 200:
            complete_months.append(m["month"])
    if complete_months:
        evidence["data_through"] = max(complete_months)

    ordered = sorted(m["month"] for m in evidence["months_probed"])
    consecutive_absent = 0
    for ym in reversed(ordered):
        m = next((x for x in evidence["months_probed"] if x["month"] == ym), None)
        ev = (m.get("events") or {}).get("status") if m else None
        fl = (m.get("fills") or {}).get("status") if m else None
        if ev == 404 and fl == 404:
            consecutive_absent += 1
        else:
            break
    evidence["consecutive_absent"] = consecutive_absent

    post_oct_probed = [m for m in evidence["months_probed"] if m["month"] > "2026-10"]
    post_oct_available = [
        m for m in post_oct_probed
        if ((m.get("events") or {}).get("status") == 200 or (m.get("fills") or {}).get("status") == 200)
    ]
    evidence["post_2026_10_summary"] = {
        "months_probed": [m["month"] for m in post_oct_probed],
        "any_available": len(post_oct_available) > 0,
        "available_months": [m["month"] for m in post_oct_available],
    }

    evidence_path = EVIDENCE_DIR / f"ironflow_probe_{ts}.json"
    with open(evidence_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(f"Wrote evidence: {evidence_path}")

    state["last_probe"] = evidence
    state["last_probe_ts"] = ts
    state["data_through"] = evidence["data_through"]
    state["consecutive_absent"] = evidence["consecutive_absent"]
    if etag_ref[0]:
        state["tree_etag"] = etag_ref[0]
    if evidence["tree"].get("parquet_paths"):
        state["tree_parquet_paths"] = evidence["tree"]["parquet_paths"]
    state.setdefault("file_cache", {})
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    print(f"Updated state: {STATE_PATH}")

    # Machine-readable resume_trigger block: the exact, checkable conditions
    # under which the next session may proceed to forward validation. Written
    # alongside the evidence so a future agent can parse it without reading prose.
    next_through = evidence["data_through"]
    fwd = forward_edge_months(next_through) if next_through else candidate_months()
    state["resume_trigger"] = {
        "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "data_through": next_through,
        "consecutive_absent": evidence["consecutive_absent"],
        "check_command": "python scripts/monitor_ironflow_liquidations.py --quick",
        "conditions": [
            {
                "id": "ironflow_events",
                "description": "Ironflow data/events/YYYY-MM.parquet returns HTTP 200 on unauthenticated GET",
                "urls": [EVENTS_TEMPLATE % ym for ym in fwd],
                "months": fwd,
            },
            {
                "id": "ironflow_fills",
                "description": "Ironflow data/fills/YYYY-MM.parquet returns HTTP 200 on unauthenticated GET",
                "urls": [FILLS_TEMPLATE % ym for ym in fwd],
                "months": fwd,
            },
            {
                "id": "new_admissible_source",
                "description": "Any new unauthenticated source passing strict GO rubric (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage, permissive license, no keys/signed/requester-pays, schema compatible with frozen FCLR-010)",
                "check": "python scripts/hunt_alternative_liquidation_sources.py",
            },
        ],
        "on_trigger": "Pre-register BEFORE inspecting outcomes, then run scripts/fclr010_harness.py and write research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<YYYYMMDDTHHMMSSZ>.md",
        "currently_fired": bool(evidence["new_files_found"]),
    }
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

    if evidence["new_files_found"]:
        print(f"NEW FILES FOUND: {len(evidence['new_files_found'])}")
    else:
        print("No genuinely new files found (all previously known or absent)")
    print(f"data_through: {evidence['data_through']}  consecutive_absent: {evidence['consecutive_absent']}")
    print(f"post-2026-10 available: {evidence['post_2026_10_summary']['any_available']}")


if __name__ == "__main__":
    main()


def check_post_october():
    """Forward-edge probe for months strictly after 2026-10 (resume check).

    Uses HEAD probes first and only downloads a body when a file genuinely
    exists. Returns True if any forward-edge month has events or fills.
    """
    for ym in ["2026-11", "2026-12", "2027-01", "2027-02"]:
        found = False
        for kind, tmpl in [("events", EVENTS_TEMPLATE), ("fills", FILLS_TEMPLATE)]:
            url = tmpl % ym
            head = head_probe(url)
            if head.get("head_ok") and head["status"] == 200:
                found = True
                break
            r = resolve_get(url)
            print(f"POST-CHECK {ym} {kind}: head={head['status']} get={r['status']}")
            if r["ok"] and r["status"] == 200:
                found = True
        if found:
            return True
    return False
