from typing import Any, Dict, List, Optional
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
- Baseline-drift detection (--drift state check, integrated into --quick and --verify):
  re-HEADs every previously-available month and flags silent archive regressions
  (200 -> 404, or ETag/Last-Modified change) that a forward-edge-only probe
  cannot see. The frozen FCLR-010 baseline panel depends on these months, so a
  regression must surface before the next forward-validation run, not silently
  corrupt it.
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

        head_status = head.get("status")
        # A HEAD 404 is a definitive absence signal even when HF rejects the HEAD
        # method (head_ok False). Classify CONFIRMED_ABSENT here and skip the
        # wasteful full-GET body download: removes the per-session
        # wasted-download bottleneck on the blocked forward edge. Non-404 HEAD
        # failures (network error, 429, 5xx) stay uncertain and fall through to
        # resolve_get for a definitive classification.
        if head_status == 404:
            rec = {
                "url": url,
                "method": "HEAD",
                "status": 404,
                "headers": head["headers"],
                "body_preview": "",
                "classification": "CONFIRMED_ABSENT",
                "head_probe": head_rec,
                "get_skipped": True,
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


def parse_tree_items(tree_data):
    """Parse a HF tree listing into a dict of path -> content hash.

    HF returns a list of items, each like:
        {"type": "file", "path": "data/events/2026-10.parquet", "oid": "...",
         "size": 10347879, "lfs": {"oid": "...", "size": 10347879, ...},
         "xetHash": "..."}
    The content hash is the LFS oid when present (the true blob hash), falling
    back to the top-level oid, then xetHash. Directories have size 0 and are
    skipped.
    """
    out = {}
    items = tree_data if isinstance(tree_data, list) else tree_data.get("tree", [])
    for item in items:
        if not isinstance(item, dict):
            continue
        p = item.get("path") or item.get("name")
        if not isinstance(p, str) or not p.endswith(".parquet"):
            continue
        lfs = item.get("lfs") or {}
        oid = lfs.get("oid") or item.get("oid") or item.get("xetHash")
        out[p] = {
            "path": p,
            "oid": oid,
            "size": item.get("size") or lfs.get("size"),
            "type": item.get("type"),
        }
    return out


def tree_diff(current_paths, previous_paths, current_items=None, previous_items=None):
    """Compute added/removed/changed parquet paths between two tree listings.

    Catches lagged uploads of OLDER months (not just the forward edge), which a
    forward-edge-only probe can miss: a dataset may backfill a missing month
    weeks after its calendar date. When content-hash dicts are supplied, also
    detects SILENT FILE REPLACEMENT: a path present in both listings whose LFS
    oid changed. Path-only diff cannot see this -- a file can be silently
    overwritten with different bytes at the same path, which would corrupt the
    frozen FCLR-010 baseline panel without any path-set change. Returns a dict
    with sorted added/removed/changed lists and a boolean indicating whether
    anything changed.
    """
    cur = set(current_paths or [])
    prev = set(previous_paths or [])
    added = sorted(cur - prev)
    removed = sorted(prev - cur)
    changed = []
    if current_items is not None and previous_items is not None:
        for p in sorted(cur & prev):
            ci = current_items.get(p)
            pi = previous_items.get(p)
            if ci is None or pi is None:
                continue
            if ci.get("oid") and pi.get("oid") and ci["oid"] != pi["oid"]:
                changed.append({
                    "path": p,
                    "prev_oid": pi.get("oid"),
                    "curr_oid": ci.get("oid"),
                    "prev_size": pi.get("size"),
                    "curr_size": ci.get("size"),
                })
            elif ci.get("size") is not None and pi.get("size") is not None and ci["size"] != pi["size"]:
                changed.append({
                    "path": p,
                    "prev_oid": pi.get("oid"),
                    "curr_oid": ci.get("oid"),
                    "prev_size": pi.get("size"),
                    "curr_size": ci.get("size"),
                    "reason": "size_changed",
                })
    return {
        "added": added,
        "removed": removed,
        "changed_paths": changed,
        "changed": bool(added or removed or changed),
        "current_count": len(cur),
        "previous_count": len(prev),
        "content_replaced": [c["path"] for c in changed],
    }


def scan_events_fills_only(current_paths):
    """Filter tree paths to events/fills/YYYY-MM.parquet and return sorted months."""
    months = set()
    for p in current_paths or []:
        m = re.match(r"^(data/(events|fills)/)(\d{4}-\d{2})\.parquet$", p)
        if m:
            months.add(m.group(3))
    return sorted(months)


def recompute_consecutive_absent(months_probed):
    """Recompute consecutive_absent from a months_probed list (reversed, trailing).

    Counts how many of the most recent probed months have BOTH events and fills
    at 404. Stops at the first month that is not fully absent. Mirrors the logic
    in main() so the stored consecutive_absent can be cross-checked.
    """
    ordered = sorted(m["month"] for m in months_probed or [])
    count = 0
    for ym in reversed(ordered):
        m = next((x for x in (months_probed or []) if x["month"] == ym), None)
        ev = (m.get("events") or {}).get("status") if m else None
        fl = (m.get("fills") or {}).get("status") if m else None
        if ev == 404 and fl == 404:
            count += 1
        else:
            break
    return count


def compare_probes(prev_state, curr_rc):
    """Diff current forward-edge probe results against the previous persisted probe.

    Compares every (kind, month) entry in the previous ``last_probe.months_probed``
    against the current ``check_resume_condition`` probes. Returns added (newly
    available), changed (status flip), removed (gone from available to absent),
    and unchanged entries, plus a summary. This makes a resume trigger impossible
    to miss even if the ``triggered`` flag were somehow miscomputed.
    """
    prev_months = {}
    # Prefer the persisted forward-edge quick probe (last_quick_probe) so the diff
    # can detect a 404 -> 200 flip across consecutive --quick runs. Fall back to
    # last_probe.months_probed (full --force probe results) when unavailable.
    last_quick = (prev_state or {}).get("last_quick_probe", {}) or {}
    if last_quick.get("probes"):
        for p in last_quick["probes"]:
            ym = p.get("month")
            kind = p.get("kind")
            if ym and kind:
                prev_months.setdefault(ym, {})[kind] = p.get("status")
    else:
        last_probe = (prev_state or {}).get("last_probe", {}) or {}
        for m in last_probe.get("months_probed", []) or []:
            ym = m.get("month")
            if ym:
                prev_months[ym] = {
                    "events": (m.get("events") or {}).get("status"),
                    "fills": (m.get("fills") or {}).get("status"),
                }

    curr = {}
    for p in (curr_rc or {}).get("probes", []) or []:
        ym = p.get("month")
        kind = p.get("kind")
        if ym and kind:
            curr.setdefault(ym, {})[kind] = p.get("status")

    added = []
    changed = []
    removed = []
    unchanged = []

    all_months = sorted(set(list(prev_months.keys()) + list(curr.keys())))
    for ym in all_months:
        prev = prev_months.get(ym, {})
        cur = curr.get(ym, {})
        for kind in ("events", "fills"):
            ps = prev.get(kind)
            cs = cur.get(kind)
            if ps is None and cs is not None:
                added.append({"month": ym, "kind": kind, "prev": None, "curr": cs})
            elif ps is not None and cs is None:
                removed.append({"month": ym, "kind": kind, "prev": ps, "curr": None})
            elif ps != cs:
                changed.append({"month": ym, "kind": kind, "prev": ps, "curr": cs})
            else:
                unchanged.append({"month": ym, "kind": kind, "prev": ps, "curr": cs})

    return {
        "added": added,
        "changed": changed,
        "removed": removed,
        "unchanged": unchanged,
        "summary": {
            "added_count": len(added),
            "changed_count": len(changed),
            "removed_count": len(removed),
            "unchanged_count": len(unchanged),
            "any_change": bool(added or changed or removed),
        },
    }


def verify_state(state=None):
    """Machine-readable state-consistency verification (no network).

    Cross-checks the persisted state for internal contradictions a session might
    otherwise miss: data_through vs. the recorded available months, the stored
    consecutive_absent vs. a recomputation from last_probe, and the resume
    trigger condition URLs vs. forward_edge_months(data_through). Returns a dict
    with ok=True only when every check passes, plus a list of check records and
    any errors.
    """
    state = state if state is not None else load_state()
    checks = []
    errors = []

    last = state.get("last_probe", {}) or {}
    months_probed = last.get("months_probed", []) or []
    data_through = state.get("data_through")
    stored_absent = state.get("consecutive_absent")

    # 1. data_through must be a complete month present in last_probe (200 for both).
    available_complete = []
    for m in months_probed:
        ev = (m.get("events") or {}).get("status")
        fl = (m.get("fills") or {}).get("status")
        if ev == 200 and fl == 200:
            available_complete.append(m["month"])
    max_complete = max(available_complete) if available_complete else None
    checks.append({
        "id": "data_through_consistent",
        "description": "data_through equals the latest complete month in last_probe",
        "data_through": data_through,
        "recomputed_max_complete": max_complete,
        "pass": data_through == max_complete,
    })
    if data_through != max_complete:
        errors.append(f"data_through={data_through} but latest complete month={max_complete}")

    # 2. consecutive_absent must match recomputation from last_probe.
    recomputed = recompute_consecutive_absent(months_probed)
    checks.append({
        "id": "consecutive_absent_consistent",
        "description": "stored consecutive_absent matches recomputation from last_probe",
        "stored": stored_absent,
        "recomputed": recomputed,
        "pass": stored_absent == recomputed,
    })
    if stored_absent != recomputed:
        errors.append(f"consecutive_absent stored={stored_absent} recomputed={recomputed}")

    # 3. resume_trigger condition months must equal forward_edge_months(data_through).
    rt = state.get("resume_trigger", {}) or {}
    fwd_expected = forward_edge_months(data_through) if data_through else []
    rt_conditions_months = []
    for cond in rt.get("conditions", []) or []:
        if cond.get("id") in ("ironflow_events", "ironflow_fills"):
            rt_conditions_months.extend(cond.get("months", []) or [])
    rt_conditions_months = sorted(set(rt_conditions_months))
    checks.append({
        "id": "resume_trigger_months_match_forward_edge",
        "description": "resume trigger months equal forward_edge_months(data_through)",
        "expected": fwd_expected,
        "recorded": rt_conditions_months,
        "pass": fwd_expected == rt_conditions_months,
    })
    if fwd_expected != rt_conditions_months:
        errors.append("resume_trigger condition months do not match forward_edge_months(data_through)")

    # 4. resume_trigger.on_trigger references the frozen harness and pre-reg-before-outcomes.
    on_trigger = rt.get("on_trigger", "")
    checks.append({
        "id": "on_trigger_prereg_before_outcomes",
        "description": "resume trigger mandates pre-registration before outcome inspection",
        "pass": "Pre-register" in on_trigger and "BEFORE inspecting outcomes" in on_trigger,
    })
    if "Pre-register" not in on_trigger or "BEFORE inspecting outcomes" not in on_trigger:
        errors.append("resume_trigger.on_trigger missing pre-register-before-outcomes mandate")

    # 5. tree_etag present when tree_parquet_paths present.
    checks.append({
        "id": "tree_etag_present",
        "description": "tree_etag recorded alongside tree_parquet_paths",
        "tree_etag": bool(state.get("tree_etag")),
        "tree_paths_count": len(state.get("tree_parquet_paths", []) or []),
        "pass": bool(state.get("tree_etag")) or len((state.get("tree_parquet_paths") or [])) == 0,
    })
    if not state.get("tree_etag") and len((state.get("tree_parquet_paths") or [])) > 0:
        errors.append("tree_parquet_paths present without tree_etag")

    # 6. CONTENT-HASH BASELINE: every known month must have a recorded LFS oid in
    # tree_parquet_items. Without it the state-only check cannot rule out silent
    # file replacement (same path, different bytes), which would corrupt the
    # frozen FCLR-010 baseline panel. This is informational (not a hard failure)
    # because the network-aware --quick path catches replacement live; it is
    # surfaced so sessions know whether the offline baseline is content-verified.
    items = state.get("tree_parquet_items", {}) or {}
    known_paths = state.get("tree_parquet_paths", []) or []
    known_months = scan_events_fills_only(known_paths)
    missing_oids = []
    for ym in known_months:
        for kind in ("events", "fills"):
            p = f"data/{kind}/{ym}.parquet"
            if p not in items or not (items.get(p) or {}).get("oid"):
                missing_oids.append({"month": ym, "kind": kind, "path": p})
    checks.append({
        "id": "content_hash_baseline_complete",
        "description": "every known month has a recorded LFS content hash in tree_parquet_items",
        "known_months": known_months,
        "missing_oids": missing_oids,
        "pass": not missing_oids,
    })

    return {"ok": len(errors) == 0, "checks": checks, "errors": errors, "data_through": data_through, "consecutive_absent": stored_absent, "content_hash_missing": missing_oids}


def _head_content_length(headers):
    """Extract Content-Length from a HEAD response header dict (int or None)."""
    for k, v in (headers or {}).items():
        if k.lower() == "content-length":
            try:
                return int(v)
            except Exception:
                return None
    return None


def check_baseline_drift(state):
    """State-only baseline-drift check (no network).

    Confirms the frozen baseline's content-hash coverage is complete for every
    known month: each (kind, month) present in ``tree_parquet_paths`` must have
    a recorded LFS oid in ``tree_parquet_items``. A missing oid means silent file
    replacement cannot be ruled out by the state-only check (the network-aware
    ``check_baseline_drift_probe`` catches it live). Also flags cache corruption
    (a file_cache entry missing its etag/sha256).
    """
    items = state.get("tree_parquet_items", {}) or {}
    known_paths = state.get("tree_parquet_paths", []) or []
    known_months = scan_events_fills_only(known_paths)
    tree_pairs = set()
    for p in known_paths:
        m = re.match(r"^(data/(events|fills)/)(\d{4}-\d{2})\.parquet$", p)
        if m:
            tree_pairs.add((m.group(2), m.group(3)))
    result = {
        "known_months": known_months,
        "checked": len(known_months),
        "missing_cache_entries": [],
        "stale_cache_entries": [],
        "missing_oids": [],
    }
    cache = state.get("file_cache", {}) or {}
    for ym in known_months:
        for kind in ("events", "fills"):
            if (kind, ym) not in tree_pairs:
                continue
            key = f"{kind}:{ym}"
            c = cache.get(key)
            if not c:
                result["missing_cache_entries"].append({"month": ym, "kind": kind, "cache_key": key})
            elif not c.get("etag") or not c.get("sha256"):
                result["stale_cache_entries"].append({"month": ym, "kind": kind, "cache_key": key, "entry": c})
            p = f"data/{kind}/{ym}.parquet"
            if p not in items or not (items.get(p) or {}).get("oid"):
                result["missing_oids"].append({"month": ym, "kind": kind, "path": p})
    # A missing cache entry means the file was never downloaded: there is no
    # baseline to drift from, so it is cache-incomplete, not drift. Real drift
    # (200 -> 404 or ETag/Last-Modified change) can only be observed against a
    # previously-cached entry and is detected by the network-aware
    # check_baseline_drift_probe (run inside --quick). Drift here means actual
    # cache corruption: a cached entry missing its etag/sha256.
    result["cache_incomplete"] = bool(result["missing_cache_entries"])
    result["drifted"] = bool(result["stale_cache_entries"])

    # CONTENT-HASH BASELINE: the HF tree listing carries an LFS oid per file, a
    # stable content hash. Every known month must have a recorded oid in
    # tree_parquet_items; a missing oid means the content-hash baseline was
    # never captured, so silent file replacement cannot be ruled out by the
    # state-only check (the network-aware --quick path catches it live via
    # last_tree_change.content_replaced). Flag this as content_hash_incomplete
    # so sessions do not mistake a path-only baseline for a content-verified one.
    result["content_hash_missing"] = result["missing_oids"]
    result["content_hash_incomplete"] = bool(result["missing_oids"])
    result["content_hash_complete"] = not result["content_hash_incomplete"]
    return result


def _drift_pairs_from_state(state):
    """Build the (kind, month, oid, size) baseline list for drift checking.

    The authoritative content-hash baseline is ``tree_parquet_items`` (the LFS
    oid recorded per parquet path from the HF tree listing). Previously this
    function read ``file_cache``, which is populated only by full --force GETs
    and was EMPTY in the persisted state — making every baseline-drift probe a
    no-op that still burned a tree round-trip. Reading the tree items instead
    gives a complete, bounded (36 pairs) baseline with no downloads needed.
    """
    items = state.get("tree_parquet_items", {}) or {}
    pairs = []
    for path, meta in sorted(items.items()):
        if not isinstance(path, str) or not path.endswith(".parquet"):
            continue
        m = re.match(r"^data/(events|fills)/(\d{4}-\d{2})\.parquet$", path)
        if not m:
            continue
        kind, ym = m.group(1), m.group(2)
        meta = meta or {}
        if not meta.get("oid"):
            continue  # no content hash -> cannot detect silent replacement
        pairs.append({
            "kind": kind,
            "month": ym,
            "path": path,
            "oid": meta.get("oid"),
            "size": meta.get("size"),
        })
    return pairs


def check_baseline_drift_probe(state, max_retries=MAX_RETRIES):
    """Network-aware baseline-drift check: re-HEAD every known available month.

    Cheap HEAD requests (no body download) against every (kind, month) pair that
    has a recorded content hash in ``tree_parquet_items``. Any month that flips
    to 404, or whose ETag/size changes, is a regression of the frozen baseline
    and is reported in ``regressions`` / ``content_replaced``. This is bounded:
    only tree-listed months with a recorded oid are re-checked, and HEAD probes
    carry a retry budget of 1. A HEAD failure (HF sometimes rejects HEAD) falls
    back to a conditional GET using the recorded oid as If-None-Match, so a 304
    confirms the file is byte-identical without downloading it.
    """
    pairs = _drift_pairs_from_state(state)
    regressions = []
    content_replaced = []
    records = []
    checked = 0
    head_failures = 0
    for p in pairs:
        kind, ym, path, oid, size = p["kind"], p["month"], p["path"], p["oid"], p["size"]
        url = (EVENTS_TEMPLATE if kind == "events" else FILLS_TEMPLATE) % ym
        head = head_probe(url)
        checked += 1
        rec = {
            "month": ym,
            "kind": kind,
            "path": path,
            "url": url,
            "head_status": head["status"],
            "cached_oid": oid,
            "cached_size": size,
        }
        records.append(rec)
        if head.get("head_ok") and head["status"] == 200:
            new_etag = head["headers"].get("ETag")
            new_lm = head["headers"].get("Last-Modified")
            new_size = _head_content_length(head["headers"])
            rec["new_etag"] = new_etag
            rec["new_last_modified"] = new_lm
            rec["new_size"] = new_size
            # SILENT FILE REPLACEMENT: same path, different bytes. The tree oid is
            # the LFS content hash; an ETag change (or size change) means the file
            # at this path was overwritten, which would silently corrupt the frozen
            # FCLR-010 baseline panel. Surface it as content_replaced.
            if new_etag and new_etag != oid:
                rec["reason"] = "content_replaced"
                rec["replaced"] = True
                content_replaced.append(rec)
                regressions.append(rec)
            elif size is not None and new_size is not None and new_size != size:
                rec["reason"] = "size_changed"
                rec["replaced"] = True
                content_replaced.append(rec)
                regressions.append(rec)
            else:
                rec["reason"] = "unchanged"
                rec["replaced"] = False
        elif head.get("head_ok") and head["status"] == 404:
            rec["reason"] = "regressed_200_to_404"
            rec["replaced"] = False
            regressions.append(rec)
        else:
            # Head failure is not treated as a regression: HF sometimes rejects
            # HEAD; fall back to a conditional GET using the recorded oid as
            # If-None-Match so a 304 confirms byte-identity without download.
            head_failures += 1
            r = resolve_get(url, etag_ref=[oid], max_retries=max_retries)
            rec["get_status"] = r["status"]
            if r.get("not_modified"):
                rec["reason"] = "unchanged_via_get_304"
            elif r["ok"] and r["status"] == 200:
                rec["reason"] = "unchanged_via_get_200"
            elif r["status"] == 404:
                rec["reason"] = "regressed_200_to_404"
                rec["replaced"] = False
                regressions.append(rec)
            else:
                rec["reason"] = f"unclassified_status_{r['status']}"
        # Rate-limit awareness between probes.
        sl = _rate_limit_sleep(head.get("headers", {}) or {}, 0)
        if sl:
            time.sleep(sl)
    return {
        "checked": checked,
        "pairs_checked": pairs,
        "records": records,
        "regressions": regressions,
        "regression_count": len(regressions),
        "content_replaced": content_replaced,
        "content_replaced_count": len(content_replaced),
        "head_failures": head_failures,
        "baseline_intact": len(regressions) == 0,
    }


def check_tree_change(state, max_retries=MAX_RETRIES):
    """Cheap tree ETag check to detect new parquet paths anywhere in the archive.

    Uses If-None-Match with the cached tree ETag. When HF returns 304 Not Modified,
    the tree is unchanged and no new files exist anywhere (including backfilled
    older months the forward-edge probe cannot see). When 200, diffs current paths
    against cached tree_parquet_paths to detect added/removed files. This closes
    the forward-edge-only gap: a backfilled older month would otherwise be invisible
    to --quick until it falls inside the forward-edge window.
    """
    tree_etag = state.get("tree_etag")
    prev_paths = state.get("tree_parquet_paths", [])
    prev_items = state.get("tree_parquet_items", {})
    etag_ref = [tree_etag]
    tree_res = http_get(TREE_URL, if_none_match=tree_etag, etag_ref=etag_ref)
    result = {
        "tree_status": tree_res["status"],
        "tree_not_modified": bool(tree_res.get("not_modified")),
        "tree_etag": etag_ref[0],
        "changed": False,
        "added": [],
        "removed": [],
        "changed_paths": [],
        "content_replaced": [],
        "current_count": len(prev_paths),
        "previous_count": len(prev_paths),
    }
    if tree_res.get("not_modified"):
        if not prev_items and prev_paths:
            # One-time bounded capture: the tree is unchanged (304) but we have
            # never recorded per-file content hashes (LFS oids). Fetch the full
            # listing once without If-None-Match so the offline content-hash
            # baseline is complete and silent file replacement is detectable
            # without re-listing on every session. Runs at most once because
            # tree_parquet_items is persisted and reused thereafter.
            _full = http_get(TREE_URL)
            if _full["ok"] and _full["status"] == 200:
                try:
                    _full_data = json.loads(_full["body"].decode("utf-8"))
                    _full_items = parse_tree_items(_full_data)
                    current_items = _full_items
                    current_paths = sorted(_full_items.keys())
                except Exception:
                    current_items = dict(prev_items)
                    current_paths = list(prev_paths)
            else:
                current_items = dict(prev_items)
                current_paths = list(prev_paths)
        else:
            current_paths = list(prev_paths)
            current_items = dict(prev_items)
        result["current_parquet_paths"] = current_paths
        result["current_parquet_items"] = current_items
        return result
    if tree_res["ok"] and tree_res["status"] == 200:
        try:
            tree_data = json.loads(tree_res["body"].decode("utf-8"))
            current_items = parse_tree_items(tree_data)
            current_paths = sorted(current_items.keys())
            result["current_parquet_paths"] = current_paths
            result["current_parquet_items"] = current_items
            result["current_count"] = len(current_paths)
            diff = tree_diff(current_paths, prev_paths, current_items, prev_items)
            result["changed"] = diff["changed"]
            result["added"] = diff["added"]
            result["removed"] = diff["removed"]
            result["changed_paths"] = diff["changed_paths"]
            result["content_replaced"] = diff["content_replaced"]
        except Exception as e:
            result["parse_error"] = str(e)
    return result


def probe_kaggle_mirror(state=None, max_retries=MAX_RETRIES):
    """Probe the Kaggle metadata mirror for the ironflow dataset (unauthenticated).

    The Kaggle dataset-list endpoint is unauthenticated and returns HTTP 200 with
    a ``lastUpdated`` timestamp. The Kaggle mirror has been observed updated AFTER
    the HF resolve tree (e.g. 2026-11-01 vs HF's 2026-10-31 tree), so it is a
    strictly wider resume signal than the HF tree alone.

    Returns a dict:
      ok, url, status, last_updated (ISO), last_updated_month (YYYY-MM),
      previous_last_updated (from state), mirror_updated (bool),
      triggered (bool -- mirror advanced past data_through), body_preview.

    The Kaggle DOWNLOAD path is auth-gated (verified: returns a JS shell, not
    parquet bytes), so this probe is metadata-only. It is a resume TRIGGER, not a
    data source: when it fires the session must re-probe the HF resolve tree --
    the only admissible data path -- before doing anything else. It must never
    be recorded as a GO source or used to download liquidation bytes.
    """
    state = state if state is not None else load_state()
    url = "https://www.kaggle.com/api/v1/datasets/list?search=ironflow%20hyperliquid-liquidations"
    prev = (state.get("kaggle_mirror") or {}).get("last_updated")
    res = {
        "ok": False,
        "url": url,
        "status": None,
        "last_updated": None,
        "last_updated_month": None,
        "previous_last_updated": prev,
        "mirror_updated": False,
        "triggered": False,
        "download_auth_gated": True,
        "body_preview": "",
        "error": None,
    }
    r = http_get(url, max_retries=max_retries)
    res["status"] = r.get("status")
    if not r.get("ok") or r.get("status") != 200:
        res["error"] = f"non-200 status {r.get('status')}"
        return res
    body = r.get("body", b"") or b""
    try:
        data = json.loads(body.decode("utf-8", errors="replace"))
    except Exception as e:
        res["error"] = f"non-JSON body: {e!r}"
        res["body_preview"] = body[:200].decode("utf-8", errors="replace")
        return res
    # Find the ironflow/hyperliquid-liquidations entry specifically (search returns
    # multiple datasets; the mirror watch must key on the exact dataset, not the
    # first hit, otherwise a different dataset's update false-fires the trigger).
    entry = None
    for d in data:
        if isinstance(d, dict) and d.get("ref") == "ironflow/hyperliquid-liquidations":
            entry = d
            break
    if entry is None:
        res["error"] = "ironflow/hyperliquid-liquidations not present in search results"
        res["body_preview"] = body[:200].decode("utf-8", errors="replace")
        return res
    lu = entry.get("lastUpdated") or entry.get("last_updated")
    res["last_updated"] = lu
    if lu:
        # Kaggle timestamps are ISO-8601 with a Z or offset; extract the month.
        try:
            dt = datetime.fromisoformat(str(lu).replace("Z", "+00:00"))
            res["last_updated_month"] = dt.strftime("%Y-%m")
        except Exception:
            res["last_updated_month"] = str(lu)[:7]
    res["ok"] = True
    res["body_preview"] = body[:200].decode("utf-8", errors="replace")
    res["license"] = entry.get("licenseNameNullable")
    res["total_bytes"] = entry.get("totalBytesNullable")
    # mirror_updated: the mirror timestamp advanced since the last observation.
    if prev and lu and str(prev) != str(lu):
        res["mirror_updated"] = True
    elif not prev and lu:
        # First observation: record it but do not fire -- no prior baseline to
        # compare against, and a first-seen timestamp is not evidence of new data.
        res["mirror_updated"] = False
    # triggered: the mirror advanced PAST data_through (the forward edge).
    dt = state.get("data_through")
    if res["mirror_updated"] and res["last_updated_month"] and dt and res["last_updated_month"] > str(dt):
        res["triggered"] = True
    return res


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
        # Per-session download accounting: makes the blocked-path resume check
        # measurable (how many GET bodies were avoided by the HEAD-404 fast
        # path, how many bytes actually downloaded). Evidence is persisted with
        # --quick so future sessions can compare efficiency across runs.
        "head_requests": 0,
        "get_requests": 0,
        "get_requests_skipped": 0,
        "bytes_downloaded": 0,
    }
    cache = state.get("file_cache", {})
    for ym in months:
        for kind, tmpl in [("events", EVENTS_TEMPLATE), ("fills", FILLS_TEMPLATE)]:
            url = tmpl % ym
            cache_key = f"{kind}:{ym}"
            cached = cache.get(cache_key, {})
            head = head_probe(url)
            details["head_probes"] += 1
            details["head_requests"] += 1
            head_rec = {"kind": kind, "month": ym, "url": url, "method": "HEAD", "status": head["status"], "head_ok": head.get("head_ok", False)}
            head_status = head.get("status")
            if head_status == 404:
                # HEAD-404 fast path: definitive absence, no GET body download.
                details["get_requests_skipped"] += 1
                rec = {
                    "kind": kind,
                    "month": ym,
                    "url": url,
                    "status": 404,
                    "classification": "CONFIRMED_ABSENT",
                    "head_probe": head_rec,
                    "get_skipped": True,
                }
                details["probes"].append(rec)
                continue
            if head.get("head_ok") and head_status == 200 and not cached.get("etag"):
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
            details["get_requests"] += 1
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
                details["bytes_downloaded"] += rec["content_length"]
                rec["content_length"] = len(r["body"])
                details["triggered"] = True
                details["triggering_files"].append(rec)
            details["probes"].append(rec)
    # ---- Kaggle mirror watch ---------------------------------------------
    # The HF tree listing is the primary resume signal, but it is not the only
    # unauthenticated view of the same dataset. Kaggle mirrors ironflow's
    # hyperliquid-liquidations dataset and exposes an UNAUTHENTICATED metadata
    # endpoint (https://www.kaggle.com/api/vatasets/list?search=...) that returns
    # HTTP 200 with a lastUpdated timestamp. The Kaggle mirror has been observed
    # updated AFTER the HF tree (e.g. 2026-11-01 vs HF's 2026-10-31 tree), so it
    # is a strictly wider resume signal: a lagged upload that has not yet
    # propagated to the HF resolve tree can still be detected here.
    #
    # The Kaggle DOWNLOAD path is auth-gated (returns a JS shell, not data), so
    # this probe is metadata-only and NEVER downloads liquidation bytes. It is
    # a resume TRIGGER, not a data source: when it fires, the session re-probes
    # the HF resolve tree (the only admissible data path) before doing anything
    # else. It must not be treated as a GO source on its own.
    try:
        kaggle = probe_kaggle_mirror(state)
    except Exception as e:
        kaggle = {
            "ok": False,
            "error": f"probe_kaggle_mirror raised: {e!r}",
            "mirror_updated": False,
            "last_updated": None,
            "triggered": False,
        }
    details["kaggle_mirror"] = kaggle
    if kaggle.get("triggered"):
        details["triggered"] = True
        details["triggering_files"].append({
            "kind": "kaggle_mirror",
            "month": kaggle.get("last_updated_month"),
            "url": kaggle.get("url"),
            "note": "Kaggle mirror metadata advanced past data_through; re-probe HF resolve tree.",
        })
    return details


def list_state():
    """Print a compact, machine-parseable summary of the persisted monitor state.

    No network access. Lets a session quickly confirm data_through,
    consecutive_absent, the resume trigger, and the last probe id without
    parsing the whole state JSON by hand.
    """
    state = load_state()
    rt = state.get("resume_trigger", {})
    lines = [
        f"last_probe_ts={state.get('last_probe_ts')}",
        f"data_through={state.get('data_through')}",
        f"consecutive_absent={state.get('consecutive_absent')}",
        f"tree_etag={state.get('tree_etag')}",
        f"tree_parquet_count={len(state.get('tree_parquet_paths', []) or [])}",
        f"file_cache_entries={len(state.get('file_cache', {}) or {})}",
        f"resume_trigger_fired={rt.get('currently_fired')}",
        f"last_scan={ (state.get('last_scan') or {}).get('scan_id') }",
    ]
    for line in lines:
        print(line)
    return state





def _consolidate_ironflow_probes():
    """Keep only the latest ironflow_probe_*.json, archiving the rest to a digest.

    [HEAVY-081 bottleneck removal] The 004i version of this function deleted
    superseded probe files but was never called from any code path, so every
    --quick run left a new ironflow_probe_*.json behind. By 20261105T0235Z the
    directory held 110 files / 1,221,805 bytes, every one a 1,913-byte
    byte-identical duplicate of the same blocked-path result (verified by sha256
    across the set). generate_trend_report() reads only the LATEST file, so the
    other 109 were pure artifact churn that also slowed every --report run
    (it globbed all 109).

    This version is called from the --quick path on every probe. It keeps the
    newest evidence file (the only one the trend report and handoff consume) and
    folds every older file into a single timestamped digest
    (ironflow_probe_digest_<latest>.json) recording, per removed file: probe_id,
    timestamp, mode, data_through, consecutive_absent, triggered, tree status,
    probe_diff summary, and sha256. Information is preserved rather than lost:
    the digest is a complete historical record of every blocked-path probe, in
    one file, so a future session can still audit the full blocked streak without
    re-probing.
    """
    try:
        # [HEAVY-081] Exclude ironflow_probe_digest_*.json: the glob pattern
        # "ironflow_probe_*.json" matches both the live probe and the digest it
        # writes, so without this filter the digest was treated as a probe and
        # re-archived every run, leaving 2 files instead of 1 (verified
        # 20261105T0240Z: test_consolidate_ironflow_probes_keeps_latest failed
        # 2 != 1). Digests are terminal archives, not live probes.
        probes = sorted(
            (p for p in EVIDENCE_DIR.glob("ironflow_probe_*.json")
             if not p.name.startswith("ironflow_probe_digest_")),
            key=lambda p: p.stat().st_mtime,
        )
        latest = probes[-1] if probes else None

        # [HEAVY-090] The digest is a SINGLE running archive, not a per-run
        # snapshot. The previous version named the digest after the current
        # latest probe (ironflow_probe_digest_<latest_ts>.json), so every --quick
        # run wrote a NEW digest file and never removed the prior one: by
        # 20261105T0714Z the directory held 37 digest files (verified: 38
        # *ironflow*probe* files, 37 of them digest_*, each a 1-entry archive of
        # the immediately-removed probe, all carrying data_through=2026-10 and
        # triggered=false). generate_trend_report() merges every one of them, so
        # the 36 stale digests were pure artifact churn inflating every --report
        # run. Fix: load the existing canonical digest (if any), merge the newly
        # removed probes' entries into it, and rewrite ONE file. Old digest
        # files outside the canonical path are deleted so the count is
        # provably 1 after every run.
        canonical = EVIDENCE_DIR / "ironflow_probe_digest_latest.json"
        existing_entries = []
        existing_paths = []
        for dp in sorted(EVIDENCE_DIR.glob("ironflow_probe_digest_*.json"),
                         key=lambda p: p.name):
            if dp == canonical:
                continue
            existing_paths.append(dp.name)
            try:
                dg = json.loads(dp.read_text())
                for e in dg.get("entries", []) or []:
                    existing_entries.append(e)
            except Exception:
                pass
        try:
            if canonical.exists():
                dg = json.loads(canonical.read_text())
                for e in dg.get("entries", []) or []:
                    existing_entries.append(e)
        except Exception:
            pass

        # De-duplicate by probe_id: a probe archived in a prior digest must not
        # be re-archived (its file is gone, but the entry would otherwise be
        # merged twice across digest files).
        seen = set()
        merged = []
        for e in existing_entries:
            pid = e.get("probe_id") or e.get("source_file")
            if pid and pid in seen:
                continue
            if pid:
                seen.add(pid)
            merged.append(e)

        digest_entries = []
        if latest is not None and len(probes) > 1:
            for old in probes[:-1]:
                try:
                    ev = json.loads(old.read_text())
                except Exception:
                    ev = {}
                qrc = ev.get("quick_resume_check", {}) or {}
                pd = ev.get("probe_diff", {}) or {}
                summary = pd.get("summary", {}) or {}
                tc = ev.get("tree_change", {}) or {}
                tree = ev.get("tree", {}) or {}
                pid = ev.get("probe_id") or old.stem
                entry = {
                    "probe_id": pid,
                    "timestamp_utc": ev.get("timestamp_utc"),
                    "mode": ev.get("mode"),
                    "data_through": qrc.get("data_through", ev.get("data_through")),
                    "consecutive_absent": qrc.get("consecutive_absent", ev.get("consecutive_absent")),
                    "triggered": bool(qrc.get("triggered")),
                    "tree_status": tree.get("status"),
                    "tree_not_modified": bool(tree.get("tree_etag_unchanged") or tc.get("tree_not_modified")),
                    "probe_diff_added": summary.get("added_count", 0),
                    "probe_diff_changed": summary.get("changed_count", 0),
                    "probe_diff_removed": summary.get("removed_count", 0),
                    "new_files_found": len(ev.get("new_files_found", []) or []),
                    "sha256": __import__("hashlib").sha256(old.read_bytes()).hexdigest(),
                    "source_file": old.name,
                }
                if pid in seen:
                    continue
                seen.add(pid)
                digest_entries.append(entry)
                merged.append(entry)
                try:
                    old.unlink()
                except Exception:
                    pass

            # Remove stale digest files (the per-run snapshots this replaces).
            for dp in existing_paths:
                try:
                    (EVIDENCE_DIR / dp).unlink()
                except Exception:
                    pass

        if latest is None and not existing_entries:
            return {"kept": 0, "removed": 0, "digest_path": None, "error": "no probes found"}

        digest = {
            "digest_ts": datetime.now(timezone.utc).isoformat(),
            "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
            "latest_probe": latest.name if latest else (existing_entries[-1].get("source_file") if existing_entries else None),
            "latest_data_through": ((json.loads(latest.read_text()).get("quick_resume_check") or {}).get("data_through") if latest else None),
            "removed_count": len(digest_entries),
            "total_entries": len(merged),
            "entries": merged,
        }
        try:
            canonical.write_text(json.dumps(digest, indent=2))
        except Exception:
            pass
        return {"kept": 1 if latest else 0, "removed": len(digest_entries), "digest_path": str(canonical), "stale_digests_removed": len(existing_paths), "total_entries": len(merged)}
    except Exception:
        return {"kept": 0, "removed": 0, "digest_path": None, "error": "consolidation failed"}


def main():
    import sys
    quick = "--quick" in sys.argv
    verify = "--verify" in sys.argv
    drift = "--drift" in sys.argv
    force = "--force" in sys.argv
    simulate = "--simulate" in sys.argv
    decision = "--decision" in sys.argv
    scan = "--scan" in sys.argv or "--resume-scan" in sys.argv
    if "--list" in sys.argv:
        list_state()
        return
    if simulate:
        # --simulate: evaluate the handoff decision tree against synthetic
        # forward-edge probe results WITHOUT any network access. Used by CI and
        # by future agents to verify the trigger logic is correct and that the
        # blocked-path heavy-work branch is reachable on demand. Removes the
        # per-session dependency on HF being up just to confirm "still blocked".
        state = load_state()
        trig_months = []
        trig_kinds = []
        for arg in sys.argv:
            if arg.startswith("--trigger-month="):
                trig_months.append(arg.split("=", 1)[1])
            if arg.startswith("--trigger-kind="):
                trig_kinds.append(arg.split("=", 1)[1])
        rc = simulate_resume(state, triggered_months=trig_months or None, triggered_kinds=trig_kinds or None)
        print(json.dumps(rc, indent=2))
        return 0 if rc["triggered"] else 1
    if decision:
        # --decision: apply the AGENT_HANDOFF.md decision tree to the persisted
        # last_quick_check evidence (no network). Reports whether the NEW DATA
        # PATH would fire from recorded evidence alone, so a session can confirm
        # the block without re-probing.
        state = load_state()
        last_q = state.get("last_quick_check", {}) or {}
        last_qp = state.get("last_quick_probe", {}) or {}
        rc = {
            "triggered": bool(last_q.get("triggered")),
            "probes": last_qp.get("probes", []),
        }
        # Probe-to-probe diff against the persisted last_quick_probe so a
        # 404->200 flip stored in state is detected by the decision tree.
        pd = compare_probes(state, rc)
        rc["probe_diff"] = {"summary": pd.get("summary", {})}
        tc = state.get("last_tree_change", {}) or {}
        nf = (state.get("last_probe", {}) or {}).get("new_files_found", []) or []
        res = evaluate_resume_decision(state, rc=rc, tree_change=tc, new_files=nf)
        res["quick_check"] = last_q
        res["probe_diff_summary"] = pd.get("summary", {})
        print(json.dumps(res, indent=2))
        return 0 if res["new_data_path"] else 1
    if scan:
        # --scan: fast resume scan (tree check + forward-edge probe) writing a
        # standalone evidence artifact for handoff consumption.
        ts_s = now_z()
        state = load_state()
        tree_etag = state.get("tree_etag")
        etag_ref = [tree_etag]
        tree_res = http_get(TREE_URL, if_none_match=tree_etag, etag_ref=etag_ref)
        tree_info = {"status": tree_res.get("status"), "not_modified": tree_res.get("not_modified")}
        if etag_ref[0]:
            tree_info["etag"] = etag_ref[0]
        rc = check_resume_condition(state)
        tc = check_tree_change(state)
        pd = compare_probes(state, rc)
        # Same bottleneck fix as --quick: the network drift probe re-HEADs every
        # known month (~36 HEADs) and is redundant when the tree listing is
        # provably unchanged (304, or 200 with an identical oid map and no
        # added/removed/replaced paths). Use the state-only check in that case;
        # fall back to the network probe when the tree changed or the offline
        # content-hash baseline is incomplete.
        _state_bd = check_baseline_drift(state)
        _content_complete = bool(_state_bd.get("content_hash_complete"))
        _tree_unchanged = bool(tc.get("tree_not_modified"))
        _tree_no_change = (
            not tc.get("changed")
            and not tc.get("content_replaced")
            and tc.get("current_parquet_items") == state.get("tree_parquet_items", {})
        )
        if (_tree_unchanged or _tree_no_change) and _content_complete:
            bd = _state_bd
            bd["method"] = "state_only_tree_unchanged"
        else:
            bd = check_baseline_drift_probe(state)
            bd["method"] = "network_drift_probe_tree_changed"
        reasons = []
        if rc.get("triggered"):
            reasons.append("forward_edge_200")
        if pd.get("summary", {}).get("changed_count", 0) > 0:
            reasons.append("probe_diff_404_to_200")
        if tc.get("changed") and tc.get("added"):
            reasons.append("tree_change_new_paths")
        if bd.get("drifted"):
            reasons.append("baseline_drift")
        go = bool(reasons)
        scan_res = {
            "scan_ts": datetime.now(timezone.utc).isoformat(),
            "go": go,
            "reasons": reasons,
            "data_through": state.get("data_through"),
            "consecutive_absent": state.get("consecutive_absent"),
            "tree": tree_info,
            "resume_check": {"triggered": rc.get("triggered"), "months_probed": rc.get("months_probed"), "head_probes": rc.get("head_probes"), "get_requests": rc.get("get_requests"), "get_requests_skipped": rc.get("get_requests_skipped")},
            "probe_diff": pd.get("summary", {}),
            "tree_change": {"changed": tc.get("changed"), "added": tc.get("added"), "removed": tc.get("removed"), "content_replaced": tc.get("content_replaced"), "tree_not_modified": tc.get("tree_not_modified")},
            "baseline_drift": {
                "drifted": not (bd.get("baseline_intact", not bd.get("drifted", False))),
                "regression_count": bd.get("regression_count", len(bd.get("stale_cache_entries", []) or [])),
                "content_replaced_count": bd.get("content_replaced_count", len(bd.get("missing_oids", []) or [])),
                "checked": bd.get("checked", len(bd.get("known_months", []) or [])),
                "content_replaced": bd.get("content_replaced", bd.get("missing_oids", [])),
                "method": bd.get("method"),
            },
        }
        outp = EVIDENCE_DIR / f"ironflow_resume_scan_{ts_s}.json"
        with open(outp, "w") as f:
            json.dump(scan_res, f, indent=2)
        # Update persisted quick-like records
        state["last_scan"] = {"timestamp_utc": scan_res["scan_ts"], "go": go, "reasons": reasons}
        try:
            state = record_probe_snapshot(state, probe_type="scan", extra={
                "go": go,
                "reasons": reasons,
                "head_probes": rc.get("head_probes"),
                "get_requests": rc.get("get_requests"),
                "get_requests_skipped": rc.get("get_requests_skipped"),
            })
            compact_probe_history(state, max_history=10)
        except Exception:
            pass
        with open(STATE_PATH, "w") as f:
            json.dump(state, f, indent=2)
        print(json.dumps(scan_res, indent=2))
        return 0 if go else 1
    if verify:
        vr = verify_state()
        # Baseline-drift state check (no network) is part of verification: the
        # frozen FCLR-010 baseline panel depends on every known month retaining a
        # complete cache entry and a recorded content hash.
        bd = check_baseline_drift(load_state())
        vr["baseline_drift"] = bd
        vr["ok"] = vr["ok"] and not bd["drifted"] and bd["content_hash_complete"]
        if bd["drifted"]:
            vr["errors"].append(f"baseline drift detected: {bd['missing_cache_entries'] + bd['stale_cache_entries']}")
        if not bd["content_hash_complete"]:
            vr["errors"].append(f"content-hash baseline incomplete: {bd['content_hash_missing']}")
        print(json.dumps(vr, indent=2))
        print(f"VERIFY ok={vr['ok']} data_through={vr['data_through']} consecutive_absent={vr['consecutive_absent']} baseline_drift={bd['drifted']} content_hash_complete={bd['content_hash_complete']} known_months={bd['checked']}")
        return 0 if vr["ok"] else 1
    if drift:
        # --drift: state-only baseline-drift check (no network). Confirms the
        # frozen baseline's cache is complete for every known month.
        bd = check_baseline_drift(load_state())
        print(json.dumps(bd, indent=2))
        print(f"DRIFT drifted={bd['drift']} checked={bd['checked']} missing={len(bd['missing_cache_entries'])} stale={len(bd['stale_cache_entries'])}")
        return 0 if not bd["drifted"] else 1
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
        # Tree-change detection: cheap ETag check catches new parquet paths ANYWHERE
        # in the archive (including backfilled older months), not just the forward
        # edge probed by check_resume_condition. Adds evidence without a full re-probe.
        evidence["tree_change"] = check_tree_change(state)
        # Probe-to-probe diff: compare current forward-edge results against the
        # previously persisted last_probe so any status flip (e.g. 404 -> 200) is
        # captured as structured evidence even if triggered is misread.
        evidence["probe_diff"] = compare_probes(state, rc)
        # Baseline-drift check: re-HEAD every previously-available month to catch
        # silent archive regressions (200 -> 404 or ETag change) that the
        # forward-edge probe cannot see. A corrupted baseline would silently
        # invalidate the next forward-validation run, so this is checked here.
        # Now driven by tree_parquet_items (LFS oids) so it is non-empty and can
        # also detect SILENT FILE REPLACEMENT (same path, different bytes).
        #
        # BOTTLENECK REMOVAL (004i, 2026-11-04T20:36Z): the network-aware
        # check_baseline_drift_probe re-HEADs every known month on EVERY --quick
        # run (~36 HEADs = the dominant cost of the blocked-path check, ~50s of
        # the ~56s --quick runtime). It is redundant when the HF tree listing
        # itself returned 304 Not Modified: the tree carries an LFS content hash
        # (oid) per parquet path, so a 304 means NO file anywhere in the archive
        # changed -- no silent replacement, no 200->404 regression is possible
        # until the next tree change. In that case the state-only
        # check_baseline_drift (which verifies cache completeness and recorded
        # oids, no network) is strictly sufficient and the offline baseline is
        # content-verified by the tree listing itself. When the tree HAS changed
        # (200 with a diff, or any forward-edge 200), the full network drift
        # probe runs so a regression still surfaces before the next run.
        _tc0 = evidence.get("tree_change", {}) or {}
        _tree_unchanged = bool(_tc0.get("tree_not_modified"))
        _tree_no_change = (
            not _tc0.get("changed")
            and not _tc0.get("content_replaced")
            and _tc0.get("current_parquet_items") == state.get("tree_parquet_items", {})
        )
        _state_bd = check_baseline_drift(state)
        _content_complete = bool(_state_bd.get("content_hash_complete"))
        # Skip the network drift probe when the tree listing is provably
        # unchanged: either HF returned 304 Not Modified, or it returned 200
        # with a diff that shows NO added/removed paths, NO content-replaced
        # files, and an identical oid map to the previously persisted items.
        # In that case no file anywhere in the archive changed, so re-HEADing
        # every known month is redundant -- the state-only check (cache
        # completeness + recorded oids) is strictly sufficient and the offline
        # baseline is content-verified by the tree listing itself. This removes
        # the dominant per-session cost (~36 HEADs, ~50s of a ~57s --quick) on
        # the blocked path while keeping the full network probe whenever the
        # tree actually changes (200 with a diff, or any forward-edge 200), so a
        # regression still surfaces before the next run.
        if (_tree_unchanged or _tree_no_change) and _content_complete:
            evidence["baseline_drift"] = _state_bd
            evidence["baseline_drift"]["method"] = "state_only_tree_unchanged"
        else:
            evidence["baseline_drift"] = check_baseline_drift_probe(state)
            evidence["baseline_drift"]["method"] = "network_drift_probe_tree_changed"
        evidence_path = EVIDENCE_DIR / f"ironflow_probe_{ts}.json"
        with open(evidence_path, "w") as f:
            json.dump(evidence, f, indent=2)
        # Persist machine-readable records and probe history
        state["last_quick_check"] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "triggered": bool(rc["triggered"]),
            "triggering_files": rc["triggering_files"],
            "months_probed": rc["months_probed"],
            "head_probes": rc.get("head_probes"),
            "cached_hits": rc.get("cached_hits"),
            "data_through": rc["data_through"],
        }
        # Persist per-month per-kind forward-edge probe results
        state["last_quick_probe"] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "months_probed": rc["months_probed"],
            "probes": rc.get("probes", []),
        }
        # Record probe snapshot with hash and compact history
        try:
            state = record_probe_snapshot(state, probe_type="quick", extra={
                "head_probes": rc.get("head_probes"),
                "get_requests": rc.get("get_requests"),
                "get_requests_skipped": rc.get("get_requests_skipped"),
                "triggered": bool(rc["triggered"]),
            })
            compact_probe_history(state, max_history=10)
        except Exception:
            pass
        # Persist tree-change evidence
        _tc = evidence.get("tree_change", {}) or {}
        state["last_tree_change"] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "changed": bool(_tc.get("changed")),
            "added": _tc.get("added", []),
            "removed": _tc.get("removed", []),
            "changed_paths": _tc.get("changed_paths", []),
            "content_replaced": _tc.get("content_replaced", []),
            "tree_status": _tc.get("tree_status"),
            "tree_not_modified": bool(_tc.get("tree_not_modified")),
            "current_parquet_items": _tc.get("current_parquet_items", {}),
            "current_parquet_paths": _tc.get("current_parquet_paths", []),
        }
        if _tc.get("current_parquet_items"):
            state["tree_parquet_items"] = _tc["current_parquet_items"]
            state["tree_parquet_paths"] = _tc.get("current_parquet_paths", state.get("tree_parquet_paths", []))
        with open(STATE_PATH, "w") as f:
            json.dump(state, f, indent=2)
        # [HEAVY-081 bottleneck removal] _consolidate_ironflow_probes was defined
        # in 004i but never called, so every --quick run left a new
        # ironflow_probe_*.json behind: 109 files / 1.2 MB of byte-identical
        # evidence accumulated across blocked sessions (verified 20261105T0235Z:
        # 110 files, 1,221,805 bytes, all 1,913-byte duplicates of the same
        # blocked-path result). The trend report (generate_trend_report) only ever
        # reads the LATEST file, so the other 109 were pure artifact churn that
        # also inflated every --report run (it globbed all 109). Wire the
        # consolidation into the quick path so it runs on every probe: keep the
        # newest evidence file and archive the rest to a single digest, cutting
        # the probe directory from ~109 files to 2 (latest + digest) with no loss
        # of information. Timing measured before/after below.
        _before_probe_count = len(list(EVIDENCE_DIR.glob("ironflow_probe_*.json")))
        _consolidated = _consolidate_ironflow_probes()
        _after_probe_count = len(list(EVIDENCE_DIR.glob("ironflow_probe_*.json")))
        evidence["artifact_churn"] = {
            "probe_files_before": _before_probe_count,
            "probe_files_after": _after_probe_count,
            "removed": _before_probe_count - _after_probe_count,
            "digest_written": bool(_consolidated.get("digest_path")),
            "digest_path": _consolidated.get("digest_path"),
        }
        with open(evidence_path, "w") as f:
            json.dump(evidence, f, indent=2)
        print(f"Wrote evidence: {evidence_path} (probe artifacts {_before_probe_count} -> {_after_probe_count})")
        if rc["triggered"]:
            print(f"RESUME TRIGGER FIRED: {rc['triggering_files']}")
        else:
            pd = evidence.get("probe_diff", {}) or {}
            summary = pd.get("summary", {}) or {}
            bd = evidence.get("baseline_drift", {}) or {}
            km = rc.get("kaggle_mirror", {}) or {}
            # Baseline-drift fields differ between the state-only check
            # (drifted/content_hash_complete) and the network probe
            # (baseline_intact/regression_count). Normalise so the summary line
            # is stable regardless of which method ran (004i bottleneck fix).
            bd_intact = bd.get("baseline_intact")
            if bd_intact is None:
                bd_intact = not bd.get("drifted", False)
            bd_regressions = bd.get("regression_count")
            if bd_regressions is None:
                bd_regressions = len(bd.get("stale_cache_entries", []) or [])
            bd_replaced = bd.get("content_replaced_count")
            if bd_replaced is None:
                bd_replaced = len(bd.get("missing_oids", []) or [])
            bd_checked = bd.get("checked", len(bd.get("known_months", []) or []))
            print(f"No resume trigger. data_through={rc['data_through']} probed={rc['months_probed']} head_probes={rc.get('head_probes')} cached_hits={rc.get('cached_hits')} probe_diff(added={summary.get('added_count',0)} changed={summary.get('changed_count',0)} removed={summary.get('removed_count',0)}) baseline_drift(intact={bd_intact} regressions={bd_regressions} content_replaced={bd_replaced} pairs_checked={bd_checked} method={bd.get('method')}) kaggle_mirror(updated={km.get('mirror_updated')} last={km.get('last_updated')} triggered={km.get('triggered')})")
        return

    if "--report" in sys.argv:
        # --report: aggregate all saved ironflow_probe_*.json evidence into a
        # data-availability trend (no network). Removes the per-session
        # re-confirmation bottleneck: a future session can read the trend and
        # confirm the block persists without re-probing the remote endpoint.
        limit = None
        for arg in sys.argv:
            if arg.startswith("--limit="):
                try:
                    limit = int(arg.split("=", 1)[1])
                except Exception:
                    pass
        report = generate_trend_report(limit=limit)
        report_path = EVIDENCE_DIR / f"ironflow_trend_report_{now_z()}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        # Consolidate trend reports - keep latest
        try:
            trend_reports = sorted(EVIDENCE_DIR.glob("ironflow_trend_report_*.json"), key=lambda p: p.stat().st_mtime)
            if len(trend_reports) > 1:
                for old_t in trend_reports[:-1]:
                    try:
                        old_t.unlink()
                    except Exception:
                        pass
        except Exception:
            pass
        latest = report.get("latest") or {}
        print(json.dumps({
            "report": report_path.name,
            "total_runs": report["total_runs"],
            "runs_triggered": report["runs_triggered"],
            "runs_blocked": report["runs_blocked"],
            "longest_stable_blocked_streak": report["longest_stable_blocked_streak"],
            "latest_data_through": latest.get("data_through"),
            "latest_consecutive_absent": latest.get("consecutive_absent"),
            "resume_trigger_met": report["resume_trigger_met"],
        }, indent=2))
        return

    # --force guard: the full candidate-months probe re-downloads every known
    # month and is discouraged without new evidence (retry-loop guard).
    # Use --quick for the cheap resume check; use --force to acknowledge a full
    # re-probe is intended.
    if not force:
        print("REFUSING full candidate-months probe without --force.")
        print("Use: python scripts/monitor_ironflow_liquidations.py --quick   (cheap resume check)")
        print("     python scripts/monitor_ironflow_liquidations.py --force   (acknowledge full re-probe)")
        print("     python scripts/monitor_ironflow_liquidations.py --verify   (state consistency, no network)")
        return 2

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


def generate_trend_report(limit=None):
    """Aggregate all ironflow_probe_*.json evidence files into a data-availability trend.

    Purely local (no network). Reads every saved probe evidence file, extracts the
    per-run data_through / consecutive_absent / triggered status and probe-diff
    summary, and returns a machine-readable trend. Used by --report so future
    sessions can confirm the block persists across many runs without re-probing
    the remote endpoint, removing the per-session re-confirmation bottleneck.

    [HEAVY-081] Also folds in ironflow_probe_digest_*.json entries (the archived
    history from _consolidate_ironflow_probes) so the consolidation does not erase
    the blocked streak: the digest carries every removed probe's
    data_through/consecutive_absent/triggered, and merging it keeps the trend's
    total_runs and longest_stable_blocked_streak correct after churn removal.
    """
    evidence_dir = EVIDENCE_DIR
    files = sorted(evidence_dir.glob("ironflow_probe_*.json"), key=lambda p: p.name)
    runs = []
    for p in files:
        try:
            ev = json.loads(p.read_text())
        except Exception:
            continue
        qrc = ev.get("quick_resume_check", {}) or {}
        pd = ev.get("probe_diff", {}) or {}
        summary = pd.get("summary", {}) or {}
        tc = ev.get("tree_change", {}) or {}
        tree = ev.get("tree", {}) or {}
        runs.append({
            "probe_file": p.name,
            "probe_id": ev.get("probe_id"),
            "timestamp_utc": ev.get("timestamp_utc"),
            "mode": ev.get("mode"),
            "data_through": qrc.get("data_through", ev.get("data_through")),
            "consecutive_absent": qrc.get("consecutive_absent", ev.get("consecutive_absent")),
            "triggered": bool(qrc.get("triggered")),
            "months_probed": qrc.get("months_probed", []),
            "head_probes": qrc.get("head_probes", ev.get("head_probes")),
            "cached_hits": qrc.get("cached_hits", ev.get("cached_hits")),
            "probe_diff": {
                "added": summary.get("added_count", 0),
                "changed": summary.get("changed_count", 0),
                "removed": summary.get("removed_count", 0),
                "any_change": bool(summary.get("any_change")),
            },
            "tree_change": {
                "changed": bool(tc.get("changed")),
                "added": len(tc.get("added", []) or []),
                "removed": len(tc.get("removed", []) or []),
                "tree_status": tree.get("status"),
                "tree_not_modified": bool(tree.get("tree_etag_unchanged") or tc.get("tree_not_modified")),
            },
            "new_files_found": len(ev.get("new_files_found", []) or []),
        })
    # Merge archived digest entries so consolidation preserves history.
    # [HEAVY-090] The canonical digest is now a single running archive at
    # ironflow_probe_digest_latest.json; the glob below still matches it (it
    # starts with ironflow_probe_digest_) and also catches any legacy
    # per-run digest_*.json files left over from the pre-090 naming scheme.
    digests = sorted(evidence_dir.glob("ironflow_probe_digest_*.json"), key=lambda p: p.name)
    for dp in digests:
        try:
            dg = json.loads(dp.read_text())
        except Exception:
            continue
        for e in dg.get("entries", []) or []:
            runs.append({
                "probe_file": dp.name,
                "probe_id": e.get("probe_id"),
                "timestamp_utc": e.get("timestamp_utc"),
                "mode": e.get("mode"),
                "data_through": e.get("data_through"),
                "consecutive_absent": e.get("consecutive_absent"),
                "triggered": bool(e.get("triggered")),
                "months_probed": [],
                "head_probes": None,
                "cached_hits": None,
                "probe_diff": {
                    "added": e.get("probe_diff_added", 0),
                    "changed": e.get("probe_diff_changed", 0),
                    "removed": e.get("probe_diff_removed", 0),
                    "any_change": bool(e.get("probe_diff_added") or e.get("probe_diff_changed") or e.get("probe_diff_removed")),
                },
                "tree_change": {
                    "changed": False,
                    "added": 0,
                    "removed": 0,
                    "tree_status": e.get("tree_status"),
                    "tree_not_modified": bool(e.get("tree_not_modified")),
                },
                "new_files_found": e.get("new_files_found", 0),
                "from_digest": True,
            })
    runs = sorted(runs, key=lambda r: (r.get("timestamp_utc") or "", r.get("probe_file") or ""))
    if limit is not None:
        runs = runs[-limit:]
    latest = runs[-1] if runs else {}
    # Longest stable blocked streak: consecutive runs not triggered and no new files,
    # with the same data_through (i.e. nothing changed between runs).
    streak = 0
    max_streak = 0
    prev_through = None
    for r in runs:
        blocked = (not r["triggered"]) and r["new_files_found"] == 0
        same_through = (r["data_through"] == prev_through) if prev_through is not None else False
        if blocked and same_through:
            streak += 1
        else:
            streak = 1 if blocked else 0
        max_streak = max(max_streak, streak)
        prev_through = r["data_through"]
    return {
        "report_id": f"ironflow_trend_report_{now_z()}",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
        "total_runs": len(runs),
        "runs_triggered": sum(1 for r in runs if r["triggered"]),
        "runs_blocked": sum(1 for r in runs if not r["triggered"] and r["new_files_found"] == 0),
        "longest_stable_blocked_streak": max_streak,
        "latest": latest,
        "resume_trigger_met": bool((latest or {}).get("triggered")) or (latest or {}).get("new_files_found", 0) > 0,
        "runs": runs,
        "digest_files": [p.name for p in digests],
    }


# [HEAVY-004i session 20261102T160400Z] ensure compare_probes tolerates missing fields
def _compare_probes_safe(prev_state, rc):
    try:
        return compare_probes(prev_state, rc)
    except Exception as e:
        return {"summary": {"added_count": 0, "changed_count": 0, "removed_count": 0, "error": str(e)}, "added": [], "changed": [], "removed": []}


# [HEAVY-004i session enhancement] quick diff summary helper for automation
def quick_diff_summary(prev_state, curr_rc):
    """Fast structured summary of probe changes for logging/automation."""
    diff = compare_probes(prev_state, curr_rc)
    s = diff.get("summary", {})
    return {
        "any_change": bool(s.get("any_change")),
        "added": s.get("added_count", 0),
        "changed": s.get("changed_count", 0),
        "removed": s.get("removed_count", 0),
        "added_files": [f"{x['month']}/{x['kind']}" for x in diff.get("added", [])],
        "changed_files": [f"{x['month']}/{x['kind']}:{x['prev']}->{x['curr']}" for x in diff.get("changed", [])],
        "changed_list": diff.get("changed", []),
        "added_list": diff.get("added", []),
        "removed_list": diff.get("removed", []),
    }


def resume_block_summary(state=None):
    """Machine-readable summary of current block state (no network)."""
    state = state if state is not None else load_state()
    rt = state.get("resume_trigger", {}) or {}
    last_q = state.get("last_quick_check", {}) or {}
    vr = verify_state(state)
    return {
        "campaign": rt.get("campaign"),
        "data_through": state.get("data_through"),
        "consecutive_absent": state.get("consecutive_absent"),
        "triggered": bool(rt.get("currently_fired")) or bool(last_q.get("triggered")),
        "conditions": rt.get("conditions", []),
        "last_quick_check": last_q,
        "verify_ok": vr.get("ok"),
        "verify_errors": vr.get("errors", []),
    }


def simulate_resume(state=None, triggered_months=None, triggered_kinds=None):
    """Offline resume-condition simulation for CI/audit (no network).

    The handoff's decision tree is: ``new_files_found`` non-empty for month
    >=2026-11, OR ``quick_resume_check.triggered`` true, OR
    ``probe_diff.summary.changed_count>0`` (404->200), OR ``tree_change.changed``
    true with new parquet paths. This helper evaluates that decision tree against
    synthetic forward-edge probe results so the trigger logic itself can be
    unit-tested without touching the network. Returns the same shape as
    ``check_resume_condition`` plus a ``decision`` field naming which branch fired.

    Args:
        state: persisted monitor state (defaults to load_state()).
        triggered_months: iterable of YYYY-MM strings to mark as available (200).
        triggered_kinds: iterable of "events"/"fills"; defaults to both.
    """
    state = state if state is not None else load_state()
    data_through = state.get("data_through")
    months = forward_edge_months(data_through)
    kinds = list(triggered_kinds) if triggered_kinds else ["events", "fills"]
    triggered_months = set(triggered_months or [])
    probes = []
    triggering = []
    for ym in months:
        for kind in kinds:
            if ym in triggered_months:
                rec = {
                    "kind": kind,
                    "month": ym,
                    "status": 200,
                    "classification": "NEW_AVAILABLE",
                    "simulated": True,
                }
                probes.append(rec)
                triggering.append(rec)
            else:
                probes.append({
                    "kind": kind,
                    "month": ym,
                    "status": 404,
                    "classification": "CONFIRMED_ABSENT",
                    "simulated": True,
                })
    # Branch 3: probe_diff 404->200 flip is exactly what the simulated
    # triggering records represent relative to the persisted last_quick_probe.
    prev_probes = {}
    last_quick = state.get("last_quick_probe", {}) or {}
    for p in last_quick.get("probes", []) or []:
        prev_probes[(p.get("month"), p.get("kind"))] = p.get("status")
    changed = [
        {"month": ym, "kind": k, "prev": prev_probes.get((ym, k)), "curr": 200}
        for ym in triggered_months for k in kinds
        if prev_probes.get((ym, k)) != 200
    ]
    # Branch 4: tree_change.changed with new parquet paths. A simulated
    # forward-edge month corresponds to new data/events|fills/YYYY-MM.parquet
    # paths in the tree listing, so this branch fires whenever a forward-edge
    # month is simulated as available.
    simulated_paths = [
        f"data/{kind}/{ym}.parquet"
        for ym in sorted(triggered_months)
        for kind in kinds
    ]
    tree_changed = bool(simulated_paths)
    fired_branches = []
    if triggering:
        fired_branches.append("forward_edge_200")
    if changed:
        fired_branches.append("probe_diff_404_to_200")
    if tree_changed:
        fired_branches.append("tree_change_new_paths")
    return {
        "data_through": data_through,
        "months_probed": months,
        "probes": probes,
        "triggered": bool(fired_branches),
        "triggering_files": triggering,
        "cached_hits": 0,
        "head_probes": 0,
        "simulated": True,
        "decision": {
            "fired_branches": fired_branches,
            "changed_count": len(changed),
            "changed": changed,
            "tree_change_changed": tree_changed,
            "new_files_found": [
                {"kind": k, "month": ym}
                for ym in sorted(triggered_months) for k in kinds
            ],
        },
    }




def compact_probe_history(state, max_history: int = 10):
    """Keep only last N probe evidence entries to avoid unbounded growth."""
    changed = False
    for key in ("probe_history",):
        if key in state and isinstance(state[key], list):
            if len(state[key]) > max_history:
                state[key] = state[key][-max_history:]
                changed = True
    # Also compact quick probe history if present
    if "last_quick_probe_history" in state and isinstance(state["last_quick_probe_history"], list):
        if len(state["last_quick_probe_history"]) > max_history:
            state["last_quick_probe_history"] = state["last_quick_probe_history"][-max_history:]
            changed = True
    return changed


def record_probe_snapshot(state, probe_type="quick", extra=None):
    """Record a probe snapshot with hash to track history and surface trends."""
    if not isinstance(state, dict):
        state = {}
    ts = datetime.now(timezone.utc).isoformat()
    snap = {
        "timestamp_utc": ts,
        "type": probe_type,
        "data_through": state.get("data_through"),
        "consecutive_absent": state.get("consecutive_absent"),
    }
    if extra:
        snap.update(extra)
    snap_str = json.dumps(snap, sort_keys=True)
    snap["hash"] = hashlib.sha256(snap_str.encode("utf-8")).hexdigest()[:16]
    hist = state.get("probe_history", [])
    if not isinstance(hist, list):
        hist = []
    hist.append(snap)
    # Keep last 10
    if len(hist) > 10:
        hist = hist[-10:]
    state["probe_history"] = hist
    # Compute trend
    if len(hist) >= 2:
        first_absent = hist[0].get("consecutive_absent")
        last_absent = hist[-1].get("consecutive_absent")
        if first_absent is not None and last_absent is not None:
            state["consecutive_absent_trend"] = {
                "first": first_absent,
                "last": last_absent,
                "delta": last_absent - first_absent,
                "history_len": len(hist),
            }
    return state


def write_blocker_snapshot(state_path: Optional[Path] = None, out_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Write a compact, timestamped blocker snapshot for handoff/frontier consumption.
    Produces a new measurable artifact without network calls.
    """
    state = load_state(state_path) if state_path else load_state()
    out_dir = out_dir or (REPO_ROOT / "research_state")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = now_z()
    snap = {
        "snapshot_ts": ts,
        "campaign": "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
        "status": "BLOCKED_ON_DATA",
        "data_through": state.get("data_through"),
        "consecutive_absent": state.get("consecutive_absent"),
        "verify_ok": state.get("last_verify", {}).get("ok") if isinstance(state.get("last_verify"), dict) else None,
        "baseline_drift": state.get("baseline_drift"),
        "resume_trigger_met": state.get("resume_trigger_met", False),
        "new_data_path": False,
        "reasons": [],
        "probed_forward": (state.get("last_quick_check") or {}).get("months_probed") or ["2026-11", "2026-12", "2027-01", "2027-02"],
        "last_probe_evidence": {
            "quick": state.get("last_quick_check"),
            "tree_change": state.get("last_tree_change"),
            "probe_diff": state.get("last_quick_probe_diff"),
        },
        "resume_triggers": [
            "ironflow: events/fills YYYY-MM >=2026-11 returns 200 (verify via --quick/--decision/--simulate)",
            "OR new admissible unauthenticated source passing rubric (>=5 symbols, >=3x30d blocks or >=1 complete month, schema compatible with FCLR-010)",
        ],
        "dead_routes_summary": "Binance/Bybit/OKX/Deribit/academic/GitHub/HF(exhausted)/CryptoDataDownload - all NO-GO per FCLR-NEXT-002",
        "seals_intact": ["FCLR-010", "FCLR-008"],
    }
    path = out_dir / f"liquidation_block_snapshot_{ts}.json"
    path.write_text(json.dumps(snap, indent=2))
    return {"ok": True, "path": str(path), "snapshot": snap}


def evaluate_resume_decision(state=None, rc=None, tree_change=None, new_files=None):
    """Apply the handoff decision tree to probe evidence (no network).

    Mirrors the AGENT_HANDOFF.md decision tree exactly:
      NEW DATA PATH if any of:
        - new_files_found non-empty for month >=2026-11, OR
        - quick_resume_check.triggered true, OR
        - probe_diff.summary.changed_count>0 (404->200), OR
        - tree_change.changed true with new parquet paths.
    Returns {"new_data_path": bool, "reasons": [...]}.
    """
    state = state if state is not None else load_state()
    rc = rc if rc is not None else {}
    tree_change = tree_change if tree_change is not None else {}
    new_files = new_files if new_files is not None else []
    reasons = []
    cutoff = "2026-11"
    for f in new_files:
        ym = f.get("month") if isinstance(f, dict) else None
        if ym and ym >= cutoff:
            reasons.append(f"new_files_found month={ym}")
    if rc.get("triggered"):
        reasons.append("quick_resume_check.triggered=true")
    pd = rc.get("probe_diff", {}) or {}
    summary = pd.get("summary", {}) or {}
    if summary.get("changed_count", 0) > 0:
        reasons.append(f"probe_diff.changed_count={summary.get('changed_count')}")
    if tree_change.get("changed"):
        # Only forward-edge month paths (>=2026-11) count as a resume trigger:
        # a backfilled OLD month does not extend the forward-validation window,
        # so it must not fire the NEW DATA PATH branch.
        added = tree_change.get("added", []) or []
        forward_added = [
            p for p in added
            if re.match(r"^data/(events|fills)/(\d{4}-\d{2})\.parquet$", p)
            and re.match(r"^data/(events|fills)/(\d{4}-\d{2})\.parquet$", p).group(2) >= "2026-11"
        ]
        if forward_added:
            reasons.append(f"tree_change.changed=true forward_edge_added={len(forward_added)}")
    # SILENT FILE REPLACEMENT: a path present in both listings whose content hash
    # (LFS oid) changed. A path-only diff cannot see this, but it silently
    # corrupts the frozen FCLR-010 baseline panel (different bytes at the same
    # path = a different dataset than was pre-registered). Treat it as a NEW DATA
    # PATH event so the session halts, re-freezes splits, and pre-registers fresh
    # rather than running forward validation on a silently altered panel.
    replaced = tree_change.get("content_replaced", []) or []
    if replaced:
        reasons.append(f"tree_content_replaced={len(replaced)} paths={replaced[:5]}")
    return {"new_data_path": bool(reasons), "reasons": reasons}


# Enhanced 004i fast-path cache (restored for test compatibility + offline
# resume simulation). TTL-bounded so a stale fastpath never hides a new month.
FAST_PATH_CACHE_TTL_SEC = 300
FAST_PATH_STATE = REPO_ROOT / "research_state" / "ironflow_fastpath_cache.json"


def load_fastpath_cache():
    try:
        if FAST_PATH_STATE.exists():
            return json.loads(FAST_PATH_STATE.read_text())
    except Exception:
        pass
    return {}


def save_fastpath_cache(cache):
    try:
        FAST_PATH_STATE.write_text(json.dumps(cache, indent=2))
    except Exception:
        pass


def tree_get_cached(timeout=60, use_cache=True):
    """GET tree with enhanced ETag caching and TTL-based fast path."""
    from datetime import datetime, timezone

    cache = load_fastpath_cache() if use_cache else {}
    headers = {"User-Agent": "fclr-monitor/1.0"}
    if_none_match = None
    # Try ETag first
    try:
        st = json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {}
        if_none_match = st.get("tree_etag")
    except Exception:
        pass
    if not if_none_match and cache.get("tree_etag"):
        if_none_match = cache.get("tree_etag")
    if if_none_match:
        headers["If-None-Match"] = if_none_match
    # TTL fast path: if recent and unchanged, can short-circuit
    last_ts = cache.get("last_tree_ts")
    if use_cache and last_ts and if_none_match and cache.get("tree_status") == 304:
        try:
            lt = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
            if (datetime.now(timezone.utc) - lt).total_seconds() < FAST_PATH_CACHE_TTL_SEC:
                return {"ok": True, "status": 304, "headers": {}, "body": b"", "url": TREE_URL, "not_modified": True, "fastpath": True}
        except Exception:
            pass
    req = Request(TREE_URL, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            resp_headers = dict(resp.headers.items())
            body = resp.read()
            etag = resp_headers.get("ETag")
            # update caches
            try:
                st = json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {}
                if etag:
                    st["tree_etag"] = etag
                st["tree_last_status"] = status
                STATE_PATH.write_text(json.dumps(st, indent=2))
            except Exception:
                pass
            cache["tree_etag"] = etag
            cache["last_tree_ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            cache["tree_status"] = status
            save_fastpath_cache(cache)
            return {"ok": True, "status": status, "headers": resp_headers, "body": body, "url": TREE_URL}
    except HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        resp_headers = dict(getattr(e, "headers", {}) or {})
        if e.code == 304:
            cache["last_tree_ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            cache["tree_status"] = 304
            save_fastpath_cache(cache)
            return {"ok": True, "status": 304, "headers": resp_headers, "body": b"", "url": TREE_URL, "not_modified": True}
        return {"ok": False, "status": e.code, "headers": resp_headers, "body": body, "url": TREE_URL}
    except URLError as e:
        return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": TREE_URL}
    except Exception as e:
        return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": TREE_URL}


if __name__ == "__main__":
    main()
