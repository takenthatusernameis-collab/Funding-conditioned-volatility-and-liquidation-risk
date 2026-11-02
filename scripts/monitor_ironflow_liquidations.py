#!/usr/bin/env python3
"""
Ironflow Hyperliquid liquidations monitor (Track A only)
Probes HF tree for data/events/YYYY-MM.parquet and data/fills/YYYY-MM.parquet.
Unauthenticated only. Records full evidence, caches state, writes timestamped probes.
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
        }
        if r["ok"] and r["status"] == 200:
            rec["sha256"] = sha256_bytes(r["body"])
            rec["content_length"] = len(r["body"])
        res[kind] = rec
    return res


def main():
    ts = now_z()
    evidence = {
        "probe_id": f"ironflow_probe_{ts}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": HF_DATASET,
        "tree_url": TREE_URL,
        "tree": None,
        "months_probed": [],
        "new_files_found": [],
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

    # Probe likely new months
    now = datetime.now(timezone.utc)
    candidates = []
    for delta in range(-1, 3):
        m = now.month + delta
        y = now.year
        while m > 12:
            m -= 12
            y += 1
        while m < 1:
            m += 12
            y -= 1
        candidates.append(f"{y:04d}-{m:02d}")
    candidates = sorted(set(candidates))
    for ym in candidates:
        evidence["months_probed"].append(probe_month(ym))
        pm = evidence["months_probed"][-1]
        if pm["events"] and pm["events"]["status"] == 200:
            evidence["new_files_found"].append({"kind": "events", "month": ym, "url": pm["events"]["url"]})
        if pm["fills"] and pm["fills"]["status"] == 200:
            evidence["new_files_found"].append({"kind": "fills", "month": ym, "url": pm["fills"]["url"]})

    evidence_path = EVIDENCE_DIR / f"ironflow_probe_{ts}.json"
    with open(evidence_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(f"Wrote evidence: {evidence_path}")

    state = {}
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH) as f:
                state = json.load(f)
        except Exception:
            state = {}
    state["last_probe"] = evidence
    state["last_probe_ts"] = ts
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
    print(f"Updated state: {STATE_PATH}")

    if evidence["new_files_found"]:
        print(f"NEW FILES FOUND: {len(evidence['new_files_found'])}")
    else:
        print("No new files found (all 404 or none 200)")


if __name__ == "__main__":
    main()
