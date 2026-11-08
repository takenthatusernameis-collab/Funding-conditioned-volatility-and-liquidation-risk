#!/usr/bin/env python3
"""FCLR inventory reconciliation: read-only diff between research_state/data_cache/{SYM}_2024_{MM}/
and research_state/data_inventory.json (root raw-zip refs).

Computes per-symbol/month file counts and sha256 from LOCAL files only. Records gaps.
Never fabricates or overwrites unverified refs. Deterministic; testable via tmp fixtures.
No network, no outcomes, no sealed-anchor writes.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "research_state", "data_cache")
INVENTORY = os.path.join(ROOT, "research_state", "data_inventory.json")

SYM_MONTH_RE = re.compile(r"^(?P<sym>[A-Z0-9]+(?:USDT|BUSD|USDC)?)_(?P<year>20\d{2})_(?P<month>0[1-9]|1[0-2])$")


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def scan_cache(cache_dir):
    """Return {sym_year_month: {relpath: sha256}} for leaf files under cache."""
    out = defaultdict(dict)
    if not os.path.isdir(cache_dir):
        return out
    for entry in sorted(os.listdir(cache_dir)):
        m = SYM_MONTH_RE.match(entry)
        if not m:
            continue
        leaf = os.path.join(cache_dir, entry)
        if not os.path.isdir(leaf):
            continue
        key = (m.group("sym"), int(m.group("year")), int(m.group("month")))
        for fn in sorted(os.listdir(leaf)):
            fp = os.path.join(leaf, fn)
            if os.path.isfile(fp):
                try:
                    out[key][fn] = sha256_file(fp)
                except OSError as e:
                    out[key][fn] = f"ERROR:{e}"
    return out


def load_inventory(path):
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        return json.load(f)


def inventory_index(inv):
    """Index inventory entries by (sym, year, month) derived from path basename."""
    idx = defaultdict(list)
    if not inv:
        return idx
    for e in inv:
        p = e.get("path", "")
        base = os.path.basename(p)
        m = SYM_MONTH_RE.match(base)
        if not m:
            # try date-stamped file names like BTCUSDT-1h-2024-01-01.zip
            dm = re.search(r"(?P<sym>[A-Z0-9]+USDT)-1h-(?P<year>20[0-9][0-9])-(?P<month>0[1-9]|1[0-2})-([0-9][0-9])\.zip", base)
            if not dm:
                continue
            key = (dm.group("sym"), int(dm.group("year")), int(dm.group("month")))
        else:
            key = (m.group("sym"), int(m.group("year")), int(m.group("month")))
        idx[key].append(e)
    return idx


def reconcile(cache_dir=CACHE, inventory_path=INVENTORY, out_path=None):
    scanned = scan_cache(cache_dir)
    inv = load_inventory(inventory_path)
    inv_idx = inventory_index(inv)

    all_keys = sorted(set(scanned) | set(inv_idx))
    missing_in_inventory = []
    stale_in_inventory = []
    matched = []
    for key in all_keys:
        sym, year, month = key
        files = scanned.get(key, {})
        entries = inv_idx.get(key, [])
        if files and not entries:
            missing_in_inventory.append({
                "symbol": sym, "year": year, "month": month,
                "month_label": f"{sym}_{year}_{month:02d}",
                "cache_files": len(files),
                "cache_sha256_sample": list(files.values())[:3],
            })
        elif entries and not files:
            stale_in_inventory.append({
                "symbol": sym, "year": year, "month": month,
                "month_label": f"{sym}_{year}_{month:02d}",
                "inventory_entries": len(entries),
            })
        else:
            matched.append({
                "symbol": sym, "year": year, "month": month,
                "month_label": f"{sym}_{year}_{month:02d}",
                "cache_files": len(files),
                "inventory_entries": len(entries),
            })

    result = {
        "artifact": "fclr_inventory_reconciliation",
        "schema_version": 1,
        "generated_utc": None,
        "cache_dir": os.path.relpath(cache_dir, ROOT),
        "inventory_path": os.path.relpath(inventory_path, ROOT),
        "inventory_present": inv is not None,
        "inventory_entry_count": len(inv) if inv else 0,
        "cache_month_dirs": len(scanned),
        "cache_files_total": sum(len(v) for v in scanned.values()),
        "matched_months": len(matched),
        "missing_in_inventory": missing_in_inventory,
        "stale_in_inventory": stale_in_inventory,
        "matched": matched,
        "reconciled": len(missing_in_inventory) == 0 and len(stale_in_inventory) == 0,
        "note": "Read-only. Computes sha256 from local files only. Does not modify data_inventory.json.",
    }
    return result


def main():
    ap = argparse.ArgumentParser(description="FCLR inventory reconciliation (read-only)")
    ap.add_argument("--cache-dir", default=CACHE)
    ap.add_argument("--inventory", default=INVENTORY)
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true", help="emit JSON to stdout")
    args = ap.parse_args()

    import datetime
    res = reconcile(args.cache_dir, args.inventory)
    res["generated_utc"] = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(res, f, indent=1)

    print(json.dumps(res, indent=1))
    return 0 if res["reconciled"] else 1


if __name__ == "__main__":
    sys.exit(main())