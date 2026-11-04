#!/usr/bin/env python3
import json
import os
import glob
import re
import zipfile
import subprocess
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'research_state', 'watch')
os.makedirs(OUT, exist_ok=True)
ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

ZIP_RE = re.compile(r'^(?P<asset>[A-Z]+)USDT-1h-(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\.zip$')

# --- (1) Root zips: full inventory by asset/month/year ---
root_zips = sorted(glob.glob(os.path.join(ROOT, '*.zip')))
by_year = {}
by_asset_month = {}
placeholder_candidates = []
for z in root_zips:
    name = os.path.basename(z)
    m = ZIP_RE.match(name)
    if m:
        by_year.setdefault(m.group('year'), []).append(name)
        by_asset_month.setdefault((m.group('asset'), m.group('year'), m.group('month')), []).append(name)
    try:
        size = os.path.getsize(z)
    except OSError:
        size = -1
    # Admissibility gate is CONTENT-based (non-zero volume/taker_buy), NOT size-based.
    # A size heuristic mislabels real 2024 kline zips (used by sealed FCLR-002) as placeholders.
    vol = None
    try:
        if 'fundingRate' not in name:
            with zipfile.ZipFile(z) as zf:
                rows = zf.read(zf.namelist()[0]).decode().split('\n')
                data = [r for r in rows[1:] if r.strip()]
                if data:
                    cols = data[0].split(',')
                    vol = float(cols[5]) if len(cols) > 5 else None
    except Exception:
        vol = None
    if vol is not None and vol == 0:
        placeholder_candidates.append({'name': name, 'size_bytes': size, 'volume': vol, 'reason': 'zero-volume synthetic placeholder'})

# --- Ironflow: scan for any file > 2026-09-30 (i.e. 2026-10 and later) ---
ironflow_dir = os.path.join(ROOT, 'research_state', 'data_cache', 'ironflow_events')
ironflow_files = sorted([f for f in os.listdir(ironflow_dir) if f.endswith('.parquet')]) if os.path.exists(ironflow_dir) else []
trigger_ironflow_gt_20260930 = any(f > '2026-09.parquet' for f in ironflow_files)
ironflow_latest = ironflow_files[-1] if ironflow_files else None

# --- Tests: confirm suite still green (part of mandatory action 1) ---
test_count = None
test_status = None
try:
    res = subprocess.run(['python', '-m', 'unittest', 'discover', '-s', 'tests'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    m = re.search(r'Ran (\d+) tests?', res.stdout.decode() + res.stderr.decode())
    test_count = int(m.group(1)) if m else None
    test_status = 'OK' if res.returncode == 0 else f'FAILED_rc{res.returncode}'
except Exception as e:
    test_status = f'ERR:{e}'

# --- Diff vs latest previous trigger_harden_*.json ---
prev_path = None
prev = None
candidates = sorted(glob.glob(os.path.join(OUT, 'trigger_harden_*.json')))
for c in reversed(candidates):
    if os.path.basename(c) != f'trigger_harden_{ts}.json':
        prev_path = c
        break
if prev_path and os.path.exists(prev_path):
    with open(prev_path) as f:
        prev = json.load(f)

diffs = []
if prev:
    p_inv = prev.get('inventory', {})
    if p_inv.get('root_zips_count') != len(root_zips):
        diffs.append(f"root_zips_count {p_inv.get('root_zips_count')} -> {len(root_zips)}")
    if p_inv.get('trigger_ironflow_gt_20260930') is not None and p_inv.get('trigger_ironflow_gt_20260930') != trigger_ironflow_gt_20260930:
        diffs.append(f"ironflow_gt_20260930 {p_inv.get('trigger_ironflow_gt_20260930')} -> {trigger_ironflow_gt_20260930}")
    p_ph = p_inv.get('placeholder_candidates', [])
    if len(p_ph) != len(placeholder_candidates):
        diffs.append(f"placeholder_candidates {len(p_ph)} -> {len(placeholder_candidates)}")
    if p_inv.get('test_count') != test_count:
        diffs.append(f"test_count {p_inv.get('test_count')} -> {test_count}")
else:
    diffs.append('no previous snapshot; baseline created')

if not diffs:
    diffs.append('no inventory change vs previous snapshot')

inventory = {
    "timestamp_utc": ts,
    "root_zips_count": len(root_zips),
    "root_zips_by_year": {k: len(v) for k, v in sorted(by_year.items())},
    "root_zips_by_asset_month": {f"{a}/{y}/{m}": len(v) for (a, y, m), v in sorted(by_asset_month.items())},
    "placeholder_candidates": placeholder_candidates,
    "placeholder_count": len(placeholder_candidates),
    "ironflow_dir_exists": os.path.exists(ironflow_dir),
    "ironflow_files": ironflow_files,
    "ironflow_latest": ironflow_latest,
    "trigger_ironflow_gt_20260930": trigger_ironflow_gt_20260930,
    "binance_root_contains_2025_2026": any(('2025' in n or '2026' in n) for n in (os.path.basename(z) for z in root_zips)),
    "sealed_window": "2026-05-08..2026-08-06",
    "track_c_priority": "FUNDING-CONDITIONED_VOLATILITY_FIRST",
    "tests": {"count": test_count, "status": test_status},
    "diff_vs_previous": {"previous_snapshot": prev_path, "diffs": diffs},
}

out_path = os.path.join(OUT, f'trigger_harden_{ts}.json')
with open(out_path, 'w') as f:
    json.dump({"inventory": inventory}, f, indent=2)
print(out_path)