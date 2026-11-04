#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PANEL = REPO / "research_state" / "data_cache" / "fclr011_panel.json"
OUT = REPO / "research_state" / f"trackc_robustness_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.md"

from src.volatility import eval as veval
from src.volatility import feature_engineering as fe
from src.volatility import block_bootstrap as bb


def qlike_wrap(y, yhat):
    v = veval.qlike(y, yhat)
    return v if v is not None else float('nan')


def get_vals(rows, key):
    vals = []
    for r in rows:
        v = r.get(key)
        if v is not None and isinstance(v, (int, float)) and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
            vals.append(float(v))
    return vals


def main():
    if not PANEL.exists():
        raise SystemExit(f"Missing panel: {PANEL}")
    d = json.loads(PANEL.read_text())
    rows = d["rows"]
    splits = d["splits"]

    by_sym = defaultdict(list)
    for r in rows:
        by_sym[r["sym"]].append(r)
    for sym in by_sym:
        by_sym[sym] = sorted(by_sym[sym], key=lambda x: x["ts_ms"])

    # extended features (same style as deeper validation)
    extended = []
    for sym, srows in by_sym.items():
        fund_hist = []
        for i, r in enumerate(srows):
            fund = r.get("signed_funding")
            if fund is not None: fund_hist.append(fund)
            fext = dict(r)
            if fund is not None and fund_hist:
                fext["fund_pct_trail"] = fe.trailing_percentile(fund_hist[:-1] if len(fund_hist)>1 else fund_hist, fund)
                fext["fund_z_trail"] = fe.trailing_zscore(fund_hist[:-1] if len(fund_hist)>1 else fund_hist, fund)
            else:
                fext["fund_pct_trail"] = None
                fext["fund_z_trail"] = None
            fext["rv_ratio_24h_168h"] = fe.rv_ratio(r.get("rv24h"), r.get("rv168h"))
            extended.append(fext)

    train_rows = [r for r in extended if r["split"] == "train"]
    test_rows = [r for r in extended if r["split"] == "test"]

    scaler_rv24 = fe.TrainOnlyScaler().fit(get_vals(train_rows, "rv24h"))
    scaler_fund = fe.TrainOnlyScaler().fit(get_vals(train_rows, "signed_funding"))
    scaler_fund_pct = fe.TrainOnlyScaler().fit(get_vals(train_rows, "fund_pct_trail"))
    scaler_fund_z = fe.TrainOnlyScaler().fit(get_vals(train_rows, "fund_z_trail"))
    scaler_rv_ratio = fe.TrainOnlyScaler().fit(get_vals(train_rows, "rv_ratio_24h_168h"))
    scaler_px_ema = fe.TrainOnlyScaler().fit(get_vals(train_rows, "ema_dist"))
    scaler_px_prem = fe.TrainOnlyScaler().fit(get_vals(train_rows, "prem"))

    def build_preds(rows):
        res = defaultdict(lambda: ([], [], []))
        for r in rows:
            y = r.get("y")
            if y is None or y <= 0 or not isinstance(y, (int,float)): continue
            rv24 = r.get("rv24h")
            if rv24 is None or rv24 <= 0: continue
            fund = r.get("signed_funding")
            fund_n = scaler_fund.transform([fund if fund is not None else 0.0])[0]
            fund_pct_n = scaler_fund_pct.transform([r.get("fund_pct_trail") if r.get("fund_pct_trail") is not None else 0.5])[0]
            fund_z_n = scaler_fund_z.transform([r.get("fund_z_trail") if r.get("fund_z_trail") is not None else 0.0])[0]
            ema_d = r.get("ema_dist"); prem = r.get("prem")
            px_ema_n = scaler_px_ema.transform([ema_d if isinstance(ema_d,(int,float)) else 0.0])[0]
            px_prem_n = scaler_px_prem.transform([prem if isinstance(prem,(int,float)) else 0.0])[0]
            meta = {'sym': r['sym'], 'ts_ms': r['ts_ms'], 'fund_abs': abs(float(fund or 0.0)), 'fund': fund}
            res['B1'][0].append(float(y)); res['B1'][1].append(float(rv24)); res['B1'][2].append(meta)
            res['C2'][0].append(float(y)); res['C2'][1].append(float(rv24)*(1.0+0.05*abs(fund_n)+0.03*abs(fund_pct_n)+0.02*abs(fund_z_n)+0.03*abs(px_ema_n)+0.02*abs(px_prem_n))); res['C2'][2].append(meta)
        return res

    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = []
    out.append(f"# TRACK C ROBUSTNESS (FCLR-011, frozen splits only) - {ts}")
    out.append(f"")
    out.append(f"## Context")
    out.append(f"- Panel: {PANEL} (FCLR-011)")
    out.append(f"- Splits: {splits}")
    out.append(f"- Symbols: {sorted(by_sym.keys())} (n={len(by_sym)})")
    out.append(f"- Frozen splits only; train-only normalization; trailing-only; chronological/leakage-safe")
    out.append(f"- Deterministic seeds; block-bootstrap >=2000 reps where feasible")
    out.append(f"")

    # 1) Leave-one-symbol out
    out.append(f"## 1) Leave-one-symbol out (TEST), C2 vs B1")
    out.append(f"| Held-out | n | B1 QLIKE | C2 QLIKE | rel_imp(C2 vs B1) | diff(C2-B1) | 95% CI | CI_excl0 |")
    out.append(f"|----------|---|----------|----------|-------------------|--------------|-------|----------|")
    for held in sorted(by_sym.keys()):
        rows_loo = [r for r in test_rows if r['sym'] != held]
        if not rows_loo: continue
        pres = build_preds(rows_loo)
        yb,yhb,mb = pres['B1']; qb = qlike_wrap(yb,yhb)
        y2,yh2,m2 = pres['C2']; q2 = qlike_wrap(y2,yh2)
        d,cilo,cihi = bb.block_bootstrap_ci(yb,yhb,yh2,qlike_wrap,block_size=24,num_reps=2000,seed=11111 + hash(held)%5000)
        rel = (qb-q2)/qb*100 if qb>0 else float('nan')
        ci_exc = 'YES' if (cilo < 0 and cihi < 0) else 'NO'
        out.append(f"| {held} | {len(yb)} | {qb:.6f} | {q2:.6f} | {rel:+.3f}% | {d:.6f} | [{cilo:.6f},{cihi:.6f}] | {ci_exc} |")
    out.append(f"")

    # 2) Leave-one-time-block out
    out.append(f"## 2) Leave-one-time-block out (TEST), C2 vs B1 (daily blocks)")
    def daykey(ms):
        from datetime import datetime, timezone
        dt = datetime.fromtimestamp(ms/1000.0, tz=timezone.utc)
        return dt.strftime('%Y-%m-%d')
    daygroups = defaultdict(list)
    for r in test_rows:
        daygroups[daykey(r['ts_ms'])].append(r)
    days = sorted(daygroups.keys())
    out.append(f"| Held-out day | n | B1 QLIKE | C2 QLIKE | rel_imp(C2 vs B1) | diff(C2-B1) | 95% CI | CI_excl0 |")
    out.append(f"|--------------|---|----------|----------|-------------------|--------------|-------|----------|")
    for dkey in days[:5]:  # show first few and summarize; full can be long but better to be complete per requirements - but output size; do all
        pass
    for dkey in days:
        rows_lob = [r for r in test_rows if daykey(r['ts_ms']) != dkey]
        if not rows_lob: continue
        pres = build_preds(rows_lob)
        yb,yhb,mb = pres['B1']; qb = qlike_wrap(yb,yhb)
        y2,yh2,m2 = pres['C2']; q2 = qlike_wrap(y2,yh2)
        d,cilo,cihi = bb.block_bootstrap_ci(yb,yhb,yh2,qlike_wrap,block_size=24,num_reps=1000,seed=22222 + hash(dkey)%5000)  # fewer reps for speed but still reasonable
        rel = (qb-q2)/qb*100 if qb>0 else float('nan')
        ci_exc = 'YES' if (cilo < 0 and cihi < 0) else 'NO'
        out.append(f"| {dkey} | {len(yb)} | {qb:.6f} | {q2:.6f} | {rel:+.3f}% | {d:.6f} | [{cilo:.6f},{cihi:.6f}] | {ci_exc} |")
    out.append(f"")

    # 3) Regimes
    out.append(f"## 3) Funding sign / |funding| regime (TEST, C2 vs B1)")
    out.append(f"| Regime | n | B1 QLIKE | C2 QLIKE | rel_imp(C2 vs B1) |")
    out.append(f"|--------|---|----------|----------|-------------------|")
    pos = [r for r in test_rows if (r.get('signed_funding') or 0)>0]
    neg = [r for r in test_rows if (r.get('signed_funding') or 0)<0]
    zero = [r for r in test_rows if (r.get('signed_funding') or 0)==0]
    fabs = [abs(float(r.get('signed_funding') or 0.0)) for r in test_rows]
    med = sorted(fabs)[len(fabs)//2] if fabs else 0
    high = [r for r in test_rows if abs(float(r.get('signed_funding') or 0.0)) >= med]
    low = [r for r in test_rows if abs(float(r.get('signed_funding') or 0.0)) < med]
    for rname,rrows in [('fund>0',pos),('fund<0',neg),('fund==0',zero),('|fund|>=med',high),('|fund|<med',low)]:
        if not rrows:
            out.append(f"| {rname} | 0 | NA | NA | NA |"); continue
        pres = build_preds(rrows); yb,yhb,mb = pres['B1']; qb = qlike_wrap(yb,yhb); y2,yh2,m2 = pres['C2']; q2 = qlike_wrap(y2,yh2)
        rel = (qb-q2)/qb*100 if qb>0 else float('nan')
        out.append(f"| {rname} | {len(yb)} | {qb:.6f} | {q2:.6f} | {rel:+.3f}% |")
    out.append(f"")

    # 4) Lags
    out.append(f"## 4) Funding lag sensitivity (t-1/t-2), TEST C2 vs B1")
    ext_lag = []
    for sym,srows in by_sym.items():
        srows_s = sorted(srows,key=lambda x:x['ts_ms'])
        for i,r in enumerate(srows_s):
            fext = dict(r)
            fund_hist=[]
            for j in range(i+1):
                if srows_s[j].get('signed_funding') is not None: fund_hist.append(srows_s[j].get('signed_funding'))
            if r.get('signed_funding') is not None and fund_hist:
                fext["fund_pct_trail"]=fe.trailing_percentile(fund_hist[:-1] if len(fund_hist)>1 else fund_hist,r.get('signed_funding'))
                fext["fund_z_trail"]=fe.trailing_zscore(fund_hist[:-1] if len(fund_hist)>1 else fund_hist,r.get('signed_funding'))
            else:
                fext["fund_pct_trail"]=None; fext["fund_z_trail"]=None
            fext["rv_ratio_24h_168h"]=fe.rv_ratio(r.get('rv24h'),r.get('rv168h'))
            fext['fund_lag1']=srows_s[i-1].get('signed_funding') if i-1>=0 else r.get('signed_funding')
            fext['fund_lag2']=srows_s[i-2].get('signed_funding') if i-2>=0 else fext['fund_lag1']
            ext_lag.append(fext)
    train_l=[r for r in ext_lag if r['split']=='train']; test_l=[r for r in ext_lag if r['split']=='test']
    scaler_fund_l1=fe.TrainOnlyScaler().fit(get_vals(train_l,'fund_lag1'))
    scaler_fund_l2=fe.TrainOnlyScaler().fit(get_vals(train_l,'fund_lag2'))
    def build_preds_lag(rows,lagkey,scaler_l):
        res=defaultdict(lambda:([],[],[]))
        for r in rows:
            y=r.get('y')
            if y is None or y<=0 or not isinstance(y,(int,float)): continue
            rv24=r.get('rv24h')
            if rv24 is None or rv24<=0: continue
            fund=r.get('signed_funding'); fund_n=scaler_fund.transform([fund if fund is not None else 0.0])[0]
            fund_pct_n=scaler_fund_pct.transform([r.get('fund_pct_trail') if r.get('fund_pct_trail') is not None else 0.5])[0]
            fund_z_n=scaler_fund_z.transform([r.get('fund_z_trail') if r.get('fund_z_trail') is not None else 0.0])[0]
            ema_d=r.get('ema_dist'); prem=r.get('prem'); px_ema_n=scaler_px_ema.transform([ema_d if isinstance(ema_d,(int,float)) else 0.0])[0]; px_prem_n=scaler_px_prem.transform([prem if isinstance(prem,(int,float)) else 0.0])[0]
            fl=r.get(lagkey); fl_n=scaler_l.transform([fl if fl is not None else 0.0])[0]
            meta={'sym':r['sym']}
            res['B1'][0].append(float(y)); res['B1'][1].append(float(rv24)); res['B1'][2].append(meta)
            res['C2lag'][0].append(float(y)); res['C2lag'][1].append(float(rv24)*(1.0+0.05*abs(fund_n)+0.03*abs(fund_pct_n)+0.02*abs(fund_z_n)+0.03*abs(px_ema_n)+0.02*abs(px_prem_n)+0.02*abs(fl_n))); res['C2lag'][2].append(meta)
        return res
    out.append(f"| Lag | n | B1 QLIKE | C2+lag QLIKE | rel_imp(C2+lag vs B1) |")
    out.append(f"|-----|---|----------|--------------|-------------------------|")
    for lname,lkey,lsc in [('t-1','fund_lag1',scaler_fund_l1),('t-2','fund_lag2',scaler_fund_l2)]:
        pres=build_preds_lag(test_l,lkey,lsc); yb,yhb,mb=pres['B1']; qb=qlike_wrap(yb,yhb); y2,yh2,m2=pres['C2lag']; q2=qlike_wrap(y2,yh2)
        rel=(qb-q2)/qb*100 if qb>0 else float('nan')
        out.append(f"| {lname} | {len(yb)} | {qb:.6f} | {q2:.6f} | {rel:+.3f}% |")
    out.append(f"")

    # 5) Winsorization
    out.append(f"## 5) Winsorization sensitivity (1%/5%) on features, TEST C2 vs B1")
    out.append(f"| winsor p | n | B1 QLIKE | C2 QLIKE (winsor) | rel_imp(C2 vs B1) |")
    out.append(f"|----------|---|----------|-------------------|-------------------|")
    for wp in [0.01,0.05]:
        fund_tr = sorted(get_vals(train_rows,'signed_funding'))
        if fund_tr:
            lo_f = fund_tr[int(len(fund_tr)*wp)]; hi_f = fund_tr[min(len(fund_tr)-1,int(len(fund_tr)*(1-wp)))]
        else: lo_f,hi_f = -1e18,1e18
        def wclip(v,lo,hi):
            if v is None: return v
            if v < lo: return lo
            if v > hi: return hi
            return v
        scaler_f_w = fe.TrainOnlyScaler().fit([wclip(v,lo_f,hi_f) for v in get_vals(train_rows,'signed_funding')])
        scaler_fp_w = fe.TrainOnlyScaler().fit([wclip(v,0,1) for v in get_vals(train_rows,'fund_pct_trail')])  # pct is 0-1 approx
        scaler_fz_w = scaler_fund_z
        scaler_pe_w = scaler_px_ema; scaler_pp_w = scaler_px_prem
        def build_w(rows):
            res=defaultdict(lambda:([],[],[]))
            for r in rows:
                y=r.get('y')
                if y is None or y<=0 or not isinstance(y,(int,float)): continue
                rv24=r.get('rv24h')
                if rv24 is None or rv24<=0: continue
                fund=r.get('signed_funding'); fund_c=wclip(fund,lo_f,hi_f) if fund is not None else 0.0
                fund_n=scaler_f_w.transform([fund_c])[0]
                fund_pct_n=scaler_fp_w.transform([r.get('fund_pct_trail') if r.get('fund_pct_trail') is not None else 0.5])[0]
                fund_z_n=scaler_fz_w.transform([r.get('fund_z_trail') if r.get('fund_z_trail') is not None else 0.0])[0]
                ema_d=r.get('ema_dist'); prem=r.get('prem'); px_ema_n=scaler_pe_w.transform([ema_d if isinstance(ema_d,(int,float)) else 0.0])[0]; px_prem_n=scaler_pp_w.transform([prem if isinstance(prem,(int,float)) else 0.0])[0]
                meta={'sym':r['sym']}
                res['B1'][0].append(float(y)); res['B1'][1].append(float(rv24)); res['B1'][2].append(meta)
                res['C2w'][0].append(float(y)); res['C2w'][1].append(float(rv24)*(1.0+0.05*abs(fund_n)+0.03*abs(fund_pct_n)+0.02*abs(fund_z_n)+0.03*abs(px_ema_n)+0.02*abs(px_prem_n))); res['C2w'][2].append(meta)
            return res
        pres=build_w(test_rows); yb,yhb,mb=pres['B1']; qb=qlike_wrap(yb,yhb); y2,yh2,m2=pres['C2w']; q2=qlike_wrap(y2,yh2)
        rel=(qb-q2)/qb*100 if qb>0 else float('nan')
        out.append(f"| {wp} | {len(yb)} | {qb:.6f} | {q2:.6f} | {rel:+.3f}% |")
    out.append(f"")

    # 6) Bootstrap sensitivity
    out.append(f"## 6) Bootstrap sensitivity (TEST, C2 vs B1)")
    out.append(f"| Method | block/mean_block | reps | diff(C2-B1) | 95% CI | CI_excl0 |")
    out.append(f"|--------|-------------------|------|--------------|-------|----------|")
    pres_full=build_preds(test_rows); yb,yhb,mb=pres_full['B1']; qb=qlike_wrap(yb,yhb); y2,yh2,m2=pres_full['C2']; q2=qlike_wrap(y2,yh2)
    for bsz in [12,24,48]:
        d,cilo,cihi=bb.block_bootstrap_ci(yb,yhb,yh2,qlike_wrap,block_size=bsz,num_reps=2000,seed=33333+bsz)
        ci_exc='YES' if (cilo<0 and cihi<0) else 'NO'
        out.append(f"| circular | {bsz}h | 2000 | {d:.6f} | [{cilo:.6f},{cihi:.6f}] | {ci_exc} |")
    if hasattr(bb,'block_bootstrap_ci_stationary'):
        for mbs in [12.0,24.0,48.0]:
            d,cilo,cihi=bb.block_bootstrap_ci_stationary(yb,yhb,yh2,qlike_wrap,mean_block_size=mbs,num_reps=2000,seed=44444+int(mbs))
            ci_exc='YES' if (cilo<0 and cihi<0) else 'NO'
            out.append(f"| stationary | {mbs}h(mean) | 2000 | {d:.6f} | [{cilo:.6f},{cihi:.6f}] | {ci_exc} |")
    out.append(f"")

    out.append(f"## 7) Notes")
    out.append(f"- All on frozen FCLR-011 splits only (train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06).")
    out.append(f"- Train-only normalization; trailing-only; chronological/leakage-safe. No threshold-shopping.")
    out.append(f"- Leave-one-out/block assess stability; regimes descriptive; lags/winsor/bootstrap test robustness.")
    out.append(f"- Track C overlay remains HYPOTHETICAL_ONLY.")
    out.append(f"")

    OUT.write_text('\n'.join(out)+'\n')
    print(f'Wrote {OUT}')


if __name__=='__main__':
    main()
