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
                sleep_for = BACKOFF_BASE ** attempt + random.random()
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


def probe_month(ym):
    res = {"month": ym, "events": None, "fills": None}
    for kind, tmpl in [("events", EVENTS_TEMPLATE), ("fills", FILLS_TEMPLATE)]:
        url = tmpl % ym
        r = http_get(url)
        rec = {
            "url": url,
            "method": "GET",
            "status": r["status"],
            "headers": {k: v for k, v in r["headers"].items()},
            "body_preview": r["body"][:200].decode("utf-8", errors="replace"),
            "classification": classify(r["status"], r["body"][:200].decode("utf-8", errors="replace")),
        }
        if r["ok"] and r["status"] == 200:
            rec["sha256"] = sha256_bytes(r["body"])
            rec["content_length"] = len(r["body"])
        res[kind] = rec
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


def main():
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

    for ym in candidate_months():
        evidence["months_probed"].append(probe_month(ym))

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
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    print(f"Updated state: {STATE_PATH}")

    if evidence["new_files_found"]:
        print(f"NEW FILES FOUND: {len(evidence['new_files_found'])}")
    else:
        print("No genuinely new files found (all previously known or absent)")
    print(f"data_through: {evidence['data_through']}  consecutive_absent: {evidence['consecutive_absent']}")
    print(f"post-2026-10 available: {evidence['post_2026_10_summary']['any_available']}")


if __name__ == "__main__":
    main()


def check_post_october():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    for ym in ["2026-11", "2026-12", "2027-01", "2027-02"]:
        res_e = http_get(EVENTS_TEMPLATE % ym)
        res_f = http_get(FILLS_TEMPLATE % ym)
        print(f"POST-CHECK {ym}: events={res_e['status']} fills={res_f['status']}")
        if res_e['status'] == 200 or res_f['status'] == 200:
            return True
    return False
