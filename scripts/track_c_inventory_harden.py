#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'research_state', 'watch')

def main():
    os.makedirs(OUT, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

    # Root zips
    root_zips = sorted(glob.glob(os.path.join(ROOT, '*.zip')))
    root_by_year = {}
    for z in root_zips:
        name = os.path.basename(z)
        # try to extract year
        for y in ['2024','2025','2026']:
            if y in name:
                root_by_year.setdefault(y, []).append(name)
                break

    # Ironflow
    ironflow_dir = os.path.join(ROOT, 'research_state', 'data_cache', 'ironflow_events')
    ironflow_files = []
    if os.path.exists(ironflow_dir):
        ironflow_files = sorted([f for f in os.listdir(ironflow_dir) if f.endswith('.parquet')])

    # Check for > 2026-10-31
    trigger_ironflow = False
    for f in ironflow_files:
        if f > '2026-10.parquet':  # lexicographic works for YYYY-MM
            trigger_ironflow = True

    inventory = {
        "timestamp_utc": ts,
        "root_zips_count": len(root_zips),
        "root_zips_by_year": {k: len(v) for k,v in root_by_year.items()},
        "ironflow_dir_exists": os.path.exists(ironflow_dir),
        "ironflow_files": ironflow_files,
        "trigger_ironflow_gt_20261031": trigger_ironflow,
        "sealed_window": "2026-05-08..2026-08-06",
        "track_c_priority": "FUNDING-CONDITIONED_VOLATILITY"
    }

    out_path = os.path.join(OUT, f'trigger_harden_{ts}.json')
    with open(out_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    print(out_path)
    return out_path

if __name__ == '__main__':
    main()
