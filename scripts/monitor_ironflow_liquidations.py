#!/usr/bin/env python3
"""
Ironflow Hyperliquid liquidations monitor (Track A only)
Probes HF tree for data/events/YYYY-MM.parquet and data/fills/YYYY-MM.parquet.
Unauthenticated only. Records full evidence, caches state, writes timestamped probes.

Improvements over the baseline monitor:
- State-aware diff: new_files_found only lists genuinely NEW 200 files vs the
  last known available set (baseline re-listed already-known 200 files every run).
- Wider probe window: last LOOKBACK_MONTHS completed months + LOOKAHEAD_MONTHS
  future/current months, so lagged uploads of recent months are caught.
- Failure classification per probe: NEW_AVAILABLE(200), CONFIRMED_ABSENT(404
  EntryNotFound), RATE_LIMITED(429), TRANSIENT_ERROR(network/other).
- Tracks data_through (latest month with both events+fills present) and
  consecutive_absent (months confirmed absent in a row at the forward edge) for
  a concrete, checkable resume condition.
- Idempotent: re-running produces the same evidence unless new data appears.
"""
import json
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

HF_DATASET = "ironflow/hyperliquid-liquidations"
TREE_URL = f"https://huggingface.co/api/datasets/{HF_DATASET}/tree/main?recursive=true"
EVENTS_TEMPLATE = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main/data/events/%s.parquet"
FILLS_TEMPLATE = f"https://huggingface.co/datasets/{HF_DATASET}/resolve/main/data/fills/%s.parquet"

# Probe window: trailing completed months + future/current months (catches lagged uploads).
LOOKBACK_MONTHS = 6
LOOKAHEAD_MONTHS = 3

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


def http_get(url, timeout=60):
    req = Request(url, headers={"User-Agent": "fclr-monitor/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            headers = dict(resp.headers.items())
            body = resp.read()
            return {"ok": True, "status": status, "headers": headers, "body": body, "url": url}
    except HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        headers = dict(getattr(e, "headers", {}) or {})
        return {"ok": False, "status": e.code, "headers": headers, "body": body, "url": url}
    except URLError as e:
        return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": url}
    except Exception as e:
        return {"ok": False, "status": None, "headers": {}, "body": str(e).encode("utf-8"), "url": url}


def classify(status, body_preview=""):
    if status == 200:
        return "NEW_AVAILABLE"
    if status == 404:
        return "CONFIRMED_ABSENT"
    if status == 429:
        return "RATE_LIMITED"
    return "TRANSIENT_ERROR"


def month_offset(months_back):
    """YYYY-MM `months_back` months from now (negative = future)."""
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
    # trailing completed months (1..LOOKBACK_MONTHS back)
    for i in range(1, LOOKBACK_MONTHS + 1):
        months.add(month_offset(i))
    # current + future months (0..LOOKAHEAD_MONTHS-1 forward) to catch lagged uploads
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
    """Set of (kind, month) confirmed 200 in the last probe."""
    last = state.get("last_probe", {}) if isinstance(state, dict) else {}
    available = set()
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

    # Probe tree
    tree_res = http_get(TREE_URL)
    evidence["tree"] = {
        "url": TREE_URL,
        "method": "GET",
        "status": tree_res["status"],
        "headers": {k: v for k, v in tree_res["headers"].items()},
    }
    if tree_res["ok"] and tree_res["status"] == 200:
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
        except Exception as e:
            evidence["tree"]["parsed"] = False
            evidence["tree"]["parse_error"] = str(e)
    else:
        evidence["tree"]["parsed"] = False

    # Probe candidate months
    for ym in candidate_months():
        evidence["months_probed"].append(probe_month(ym))

    # Determine genuinely NEW files vs previously available state
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

    # data_through: latest month where both events and fills are 200
    complete_months = []
    for m in evidence["months_probed"]:
        ev = (m.get("events") or {}).get("status")
        fl = (m.get("fills") or {}).get("status")
        if ev == 200 and fl == 200:
            complete_months.append(m["month"])
    if complete_months:
        evidence["data_through"] = max(complete_months)

    # consecutive_absent: count forward-edge months confirmed absent (both 404)
    # Walk backward from the latest probed month; stop at first present month.
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

    # Post-2026-10 explicit summary
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
    """Explicit check for post-2026-10 data with clear reporting."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    for ym in ["2026-11", "2026-12", "2027-01", "2027-02"]:
        res_e = http_get(EVENTS_TEMPLATE % ym)
        res_f = http_get(FILLS_TEMPLATE % ym)
        print(f"POST-CHECK {ym}: events={res_e['status']} fills={res_f['status']}")
        if res_e['status'] == 200 or res_f['status'] == 200:
            return True
    return False
