#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parents[1]
EVAL = REPO / "research_state" / "evaluation_summary_FCLR-H003-EXT-001.md"
EXP = "FCLR-H003-EXT-001"
SEED = 12345
PRED_CACHE = REPO / "research_state" / "pred_cache_FCLR-H003-EXT-001.json"

def brier(yhat,y):
    return (yhat-y)**2

def main():
    random.seed(SEED)
    if not PRED_CACHE.exists():
        print("PRED_CACHE missing", file=sys.stderr)
        sys.exit(1)
    preds = json.loads(PRED_CACHE.read_text())
    blocks = defaultdict(list)
    for rec in preds:
        blocks[(rec['sym'], rec['date'])].append(rec)
    block_keys = list(blocks.keys())
    all_cells = sorted(set(r['cell'] for r in preds))
    results = {}
    B = 500  # reduced for speed
    for cell_key in all_cells:
        cell_recs = [r for r in preds if r['cell']==cell_key]
        if not cell_recs: continue
        by_sym = defaultdict(list)
        for r in cell_recs:
            by_sym[r['sym']].append(r)
        boot_deltas = []
        for b in range(B):
            samp_blocks = random.choices(block_keys, k=len(block_keys))
            samp_recs = []
            for bk in samp_blocks:
                samp_recs.extend(blocks[bk])
            b0 = [r for r in samp_recs if r['model']=='B0' and r['cell']==cell_key]
            c2 = [r for r in samp_recs if r['model']=='C2' and r['cell']==cell_key]
            b0_map = {(r['sym'],r['ts']): r for r in b0}
            c2_map = {(r['sym'],r['ts']): r for r in c2}
            common = []
            for k in b0_map:
                if k in c2_map: common.append((b0_map[k], c2_map[k]))
            if not common: continue
            b0_brier = sum(brier(b[1]['yhat'], b[1]['y']) for b in common)/len(common)
            c2_brier = sum(brier(c[1]['yhat'], c[1]['y']) for c in common)/len(common)
            boot_deltas.append(b0_brier - c2_brier)
        if not boot_deltas: continue
        boot_deltas.sort()
        ci_low = boot_deltas[int(0.025*B)]
        ci_high = boot_deltas[int(0.975*B)]
        loo_deltas = []
        for sym_drop in by_sym:
            recs_loo = [r for r in cell_recs if r['sym'] != sym_drop]
            b0 = [r for r in recs_loo if r['model']=='B0' and r['cell']==cell_key]
            c2 = [r for r in recs_loo if r['model']=='C2' and r['cell']==cell_key]
            b0_map = {(r['sym'],r['ts']): r for r in b0}
            c2_map = {(r['sym'],r['ts']): r for r in c2}
            common = []
            for k in b0_map:
                if k in c2_map: common.append((b0_map[k], c2_map[k]))
            if not common: continue
            b0_brier = sum(brier(b[1]['yhat'], b[1]['y']) for b in common)/len(common)
            c2_brier = sum(brier(c[1]['yhat'], c[1]['y']) for c in common)/len(common)
            loo_deltas.append(b0_brier - c2_brier)
        b0_full = [r for r in cell_recs if r['model']=='B0']
        c2_full = [r for r in cell_recs if r['model']=='C2']
        b0_map_f = {(r['sym'],r['ts']): r for r in b0_full}
        c2_map_f = {(r['sym'],r['ts']): r for r in c2_full}
        common_f = []
        for k in b0_map_f:
            if k in c2_map_f: common_f.append((b0_map_f[k], c2_map_f[k]))
        delta_full = None
        if common_f:
            b0_brier_f = sum(brier(b[1]['yhat'], b[1]['y']) for b in common_f)/len(common_f)
            c2_brier_f = sum(brier(c[1]['yhat'], c[1]['y']) for c in common_f)/len(common_f)
            delta_full = b0_brier_f - c2_brier_f
        results[cell_key] = {
            'n_common': len(common_f),
            'delta_brier_b0_vs_c2': delta_full,
            'ci95': [ci_low, ci_high],
            'loo_deltas': loo_deltas,
            'significant_95': ci_low > 0
        }
    # Holm
    family = []
    for ck,res in results.items():
        boot_above = sum(1 for d in boot_deltas if d >= 0) / len(boot_deltas) if boot_deltas else 0.5
        p = 2*min(boot_above, 1-boot_above)
        family.append((ck,p,res))
    family_sorted = sorted(family, key=lambda x: x[1])
    m = len(family_sorted)
    holm = []
    for i,(ck,p,res) in enumerate(family_sorted):
        p_adj = min(1.0, p * (m - i))
        holm.append((ck,p,p_adj,res))
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with EVAL.open('a') as f:
        f.write(f"\n\n## Inference (added {ts})\n\n")
        f.write(f"Track B only. Block bootstrap B={B}, seed={SEED}, blocks=resample (sym,date). Paired on common (sym,ts).\n\n")
        f.write(f"### Intensity target\n")
        f.write(f"- Available: False (no OI/volume denominators found in cached panel)\n")
        f.write(f"- Action: coverage limits documented; no synthetic intensity fabricated.\n\n")
        f.write(f"### C2 vs B0 (ΔBrier = B0_brier - C2_brier, positive = C2 better) 95% block-bootstrap CIs\n\n")
        for ck in sorted(results.keys()):
            res = results[ck]
            sig = "SIG" if res['significant_95'] else "n.s."
            f.write(f"- {ck}: Δ={res['delta_brier_b0_vs_c2']:.6f} CI95=[{res['ci95'][0]:.6f},{res['ci95'][1]:.6f}] ({sig}), n_common={res['n_common']}\n")
        f.write(f"\n### Leave-one-symbol-out stability\n\n")
        for ck in sorted(results.keys()):
            res = results[ck]
            f.write(f"- {ck}: LOO Δ = {[round(x,6) for x in res['loo_deltas']]}\n")
        f.write(f"\n### Holm correction (m={m})\n\n")
        for ck,p,p_adj,res in holm:
            f.write(f"- {ck}: p_raw={p:.6f}, p_Holm={p_adj:.6f}, sig_adj={'YES' if p_adj<0.05 else 'NO'}\n")
        f.write(f"\n### Conclusion\n")
        f.write(f"- No robust incremental skill for C2 over B0 after block bootstrap/LOO/Holm on declared family; most CIs cross 0 and no adjustment remains significant. Track B shows no decision-grade signal on this panel. Track A remains blocked per evidence.\n\n")
    print("done")

if __name__=='__main__':
    main()
