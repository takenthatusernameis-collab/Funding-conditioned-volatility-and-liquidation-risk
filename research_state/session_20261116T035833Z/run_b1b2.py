import json, math, time
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

IN_PANEL = Path("research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet")
OUT_DIR = Path("research_state/session_20261116T035833Z")
UTC = "20261116T035833Z"
N_BOOT = 2000
RNG_SEED = 20261114
PURGE_DAYS = 7
TRAIN_START = pd.Timestamp("2026-01-01T00:00:00Z")
TRAIN_END = pd.Timestamp("2026-03-17T23:00:00Z")
TEST_START = pd.Timestamp("2026-05-08T00:00:00Z")
TEST_END = pd.Timestamp("2026-08-06T23:00:00Z")
EPS = 1e-12
MATERIALITY_PCT = 2.0

# Per recompute audit design: B1 HAR on log RV; C1 adds funding_z, abs_fund_pct_z; C2 adds ema24_dist_z (premium not computable)
CORE = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_funding_pct_trail", "ema24_dist"]
SPECS = {
    "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
    "B1_plus_funding": ["log_rv1h", "log_rv24h", "log_rv168h", "funding_z", "abs_fund_pct_z"],
    "B1_plus_ema24": ["log_rv1h", "log_rv24h", "log_rv168h", "ema24_dist_z"],
    "B1_plus_funding_plus_ema24": ["log_rv1h", "log_rv24h", "log_rv168h", "funding_z", "abs_fund_pct_z", "ema24_dist_z"],
}

def qlike(y, yhat):
    y = np.asarray(y, float); yhat = np.asarray(yhat, float)
    yhat = np.maximum(yhat, EPS); y = np.maximum(y, EPS)
    r = y / yhat
    return float(np.mean(r - np.log(r) - 1.0))

def fit_sm_predict(train, test, cols):
    Xtr = sm.add_constant(train[cols].to_numpy(float), has_constant='add')
    ytr = train['log_target'].to_numpy(float)
    Xte = sm.add_constant(test[cols].to_numpy(float), has_constant='add')
    res = sm.OLS(ytr, Xtr).fit()
    smear = float(np.mean(np.exp(res.resid)))
    pred = np.exp(np.clip(res.predict(Xte), -50, 50)) * smear
    pred = np.maximum(pred, EPS)
    params = [float(x) for x in res.params]
    return pred, {
        "smear": smear, "rsquared": float(res.rsquared), "nobs": int(res.nobs),
        "params": dict(zip(["const"]+cols, params)),
        "aic": float(res.aic), "bic": float(res.bic),
    }

def fit_lstsq_predict(train, test, cols):
    # independent QR/SVD path via numpy lstsq
    Xtr = train[cols].to_numpy(float)
    ytr = train['log_target'].to_numpy(float)
    Xte = test[cols].to_numpy(float)
    A = np.column_stack([np.ones(len(Xtr)), Xtr])
    Ate = np.column_stack([np.ones(len(Xte)), Xte])
    beta, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    resid = ytr - A @ beta
    smear = float(np.mean(np.exp(resid)))
    pred = np.exp(np.clip(Ate @ beta, -50, 50)) * smear
    pred = np.maximum(pred, EPS)
    ss_res = float(np.sum(resid**2)); ss_tot = float(np.sum((ytr - np.mean(ytr))**2))
    r2 = 1.0 - ss_res/ss_tot if ss_tot > 0 else float('nan')
    return pred, {"smear": smear, "rsquared": r2, "nobs": int(len(ytr)), "params": dict(zip(["const"]+cols, [float(x) for x in beta]))}

def block_boot(train_like_y, pred_a, pred_b, day_keys, n_boot, seed):
    # paired per-row qlike diff (a-b), resample by UTC-day blocks
    y = np.asarray(train_like_y, float)
    qa = y/np.maximum(pred_a,EPS) - np.log(y/np.maximum(pred_a,EPS)) - 1.0
    qb = y/np.maximum(pred_b,EPS) - np.log(y/np.maximum(pred_b,EPS)) - 1.0
    d = qa - qb
    udays = np.unique(day_keys)
    blocks = [np.where(day_keys==u)[0] for u in udays]
    blocks = [b for b in blocks if len(b)]
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_boot):
        take = []
        for _ in range(len(blocks)):
            blk = blocks[int(rng.integers(0, len(blocks)))]
            take.append(d[blk])
        means.append(float(np.concatenate(take).mean()))
    arr = np.array(means)
    ci = (float(np.percentile(arr,2.5)), float(np.percentile(arr,97.5)))
    return d, ci, int(len(blocks))

def main():
    t0=time.time()
    df = pd.read_parquet(IN_PANEL)
    df['ts'] = pd.to_datetime(df['ts'], utc=True)
    df = df.sort_values(['coin','ts']).reset_index(drop=True)
    # splits with 7d purge before test
    purge_cut = TEST_START - pd.Timedelta(days=PURGE_DAYS)
    train = df[(df['ts']>=TRAIN_START) & (df['ts']<=TRAIN_END)].copy()
    train = train[train['ts'] < purge_cut]
    test = df[(df['ts']>=TEST_START) & (df['ts']<=TEST_END)].copy()
    # core completeness
    train = train.dropna(subset=CORE + ['target_rv24h'])
    test = test.dropna(subset=CORE + ['target_rv24h'])
    # train-only scaling for funding/ema features
    for col, out in [("signed_funding","funding_z"), ("abs_funding_pct_trail","abs_fund_pct_z"), ("ema24_dist","ema24_dist_z")]:
        mu = float(train[col].mean()); sd = float(train[col].std(ddof=0)); sd = sd if sd>1e-12 else 1.0
        train[out] = (train[col]-mu)/sd; test[out] = (test[col]-mu)/sd
    train['log_target'] = np.log(train['target_rv24h'].clip(lower=EPS))
    test['log_target'] = np.log(test['target_rv24h'].clip(lower=EPS))
    y = test['target_rv24h'].to_numpy(float)
    day_keys = test['ts'].dt.floor('D').to_numpy()

    sm_preds, sm_infos = {}, {}
    ls_preds, ls_infos = {}, {}
    for name, cols in SPECS.items():
        sm_preds[name], sm_infos[name] = fit_sm_predict(train, test, cols)
        ls_preds[name], ls_infos[name] = fit_lstsq_predict(train, test, cols)
        print(name, 'sm_qlike', qlike(y, sm_preds[name]), 'ls_qlike', qlike(y, ls_preds[name]), flush=True)

    contrasts = [
        ("B1_plus_funding","B1","funding_increment"),
        ("B1_plus_ema24","B1","ema24_increment"),
        ("B1_plus_funding_plus_ema24","B1","joint_increment"),
        ("B1_plus_funding_plus_ema24","B1_plus_funding","ema24_over_funding"),
        ("B1_plus_funding_plus_ema24","B1_plus_ema24","funding_over_ema24"),
    ]
    out = {"meta":{"utc":UTC,"train_rows":len(train),"test_rows":len(test),"n_boot":N_BOOT,"seed":RNG_SEED,
                    "train_window":[str(TRAIN_START),str(TRAIN_END)],"test_window":[str(TEST_START),str(TEST_END)],
                    "purge_days":PURGE_DAYS,"panel":str(IN_PANEL),"design_note":"C2 premium slot not computable from cached 2026 archive; ema24_dist used as C2 structural slot per recompute"},
           "models":{}, "contrasts":{}, "impl_crosscheck":{}}
    for name in SPECS:
        qsm=qlike(y,sm_preds[name]); qls=qlike(y,ls_preds[name])
        out['models'][name]={"sm_qlike":qsm,"lstsq_qlike":qls,"sm":sm_infos[name],"lstsq":{k:v for k,v in ls_infos[name].items() if k!='params'}, "pred_max_abs_diff_sm_vs_lstsq": float(np.max(np.abs(sm_preds[name]-ls_preds[name])))}
    for a,b,label in contrasts:
        qa=out['models'][a]['sm_qlike']; qb=out['models'][b]['sm_qlike']
        d, (lo,hi), nblocks = block_boot(y, sm_preds[a], sm_preds[b], day_keys, N_BOOT, RNG_SEED)
        mean_diff=float(np.mean(d)); rel = (qb-qa)/qb*100.0 if qb>0 else None
        # bootstrap on rel reduction
        udays = np.unique(day_keys); bl=[np.where(day_keys==u)[0] for u in udays]; bl=[x for x in bl if len(x)]
        rng=np.random.default_rng(RNG_SEED); rels=[]
        for _ in range(N_BOOT):
            take=[]
            for __ in range(len(bl)):
                blk=bl[int(rng.integers(0,len(bl)))]; take.append(blk)
            sel=np.concatenate(take)
            qaa=y[sel]/np.maximum(sm_preds[a][sel],EPS)-np.log(y[sel]/np.maximum(sm_preds[a][sel],EPS))-1.0
            qbb=y[sel]/np.maximum(sm_preds[b][sel],EPS)-np.log(y[sel]/np.maximum(sm_preds[b][sel],EPS))-1.0
            rels.append((float(np.mean(qbb))-float(np.mean(qaa)))/float(np.mean(qbb))*100.0 if float(np.mean(qbb))>0 else np.nan)
        rels=np.array(rels)
        rlo,rhi=float(np.percentile(rels,2.5)), float(np.percentile(rels,97.5))
        out['contrasts'][f"{a}_vs_{b}"]={"label":label,"a":a,"b":b,"qlike_a":qa,"qlike_b":qb,"mean_diff_a_minus_b":mean_diff,
            "rel_reduction_pct":rel,"rel_ci95_lo":rlo,"rel_ci95_hi":rhi,"ci_excludes_zero_improvement": bool(rhi < 0 or rlo > 0),
            "material_ge_2pct": bool(rel is not None and rel >= MATERIALITY_PCT and rlo >= MATERIALITY_PCT),
            "ci_crosses_zero": bool(rlo <= 0 <= rhi), "n_blocks":nblocks}
        print('contrast',a,'vs',b,rel,rlo,rhi, flush=True)
    # impl crosscheck summary vs sm
    for a,b,_ in contrasts:
        d_sm = out['contrasts'][f"{a}_vs_{b}"]['rel_reduction_pct']
        qa_ls=out['models'][a]['lstsq_qlike']; qb_ls=out['models'][b]['lstsq_qlike']
        rel_ls = (qb_ls-qa_ls)/qb_ls*100.0 if qb_ls>0 else None
        out['impl_crosscheck'][f"{a}_vs_{b}"]={"sm_rel_pct":d_sm,"lstsq_rel_pct":rel_ls,
            "abs_diff_pct_points": None if (d_sm is None or rel_ls is None) else abs(d_sm-rel_ls),
            "sm_qlike_a":out['models'][a]['sm_qlike'],"sm_qlike_b":out['models'][b]['sm_qlike'],
            "lstsq_qlike_a":qa_ls,"lstsq_qlike_b":qb_ls}
    out['elapsed_s']=time.time()-t0
    (OUT_DIR/f"rca011_feature_attribution_{UTC}.json").write_text(json.dumps(out, indent=2))
    # md
    L=[f"# RCA011 Feature Attribution & Impl Crosscheck {UTC}","",
       f"Panel: `{IN_PANEL}`","Design: OLS on log(RV+1e-12), train-only z-scaling for funding/ema24_dist, Duan smearing, 7d purge before test, paired 24h block bootstrap (2000, seed={RNG_SEED}).",
       "C2 premium slot not computable from cached 2026 archive; joint spec uses ema24_dist as the C2 structural slot (matches recompute).","",
       f"Train rows={len(train)} (after purge/dropna), Test rows={len(test)}.", "", "## Models","|model|SM QLIKE|lstsq QLIKE|max|pred_sm-pred_ls||SM R2|smear|","|---|---:|---:|---:|---:|---:|"]
    for n,m in out['models'].items():
        L.append(f"|{n}|{m['sm_qlike']:.6f}|{m['lstsq_qlike']:.6f}|{m['pred_max_abs_diff_sm_vs_lstsq']:.3e}|{m['sm']['rsquared']:.6f}|{m['sm']['smear']:.6f}|")
    L+=["","## Contrasts (statsmodels path, block bootstrap)","|contrast|label|rel%|CI95 lo|CI95 hi|ci_cross0|","|---|---|---:|---:|---:|:---:|"]
    for k,c in out['contrasts'].items():
        L.append(f"|{k}|{c['label']}|{c['rel_reduction_pct']:.4f}|{c['rel_ci95_lo']:.4f}|{c['rel_ci95_hi']:.4f}|{c['ci_crosses_zero']}|")
    L+=["","## Implementation cross-check (SM vs numpy.linalg.lstsq)","|contrast|SM rel%|lstsq rel%|abs diff pp|","|---|---:|---:|---:|"]
    for k,c in out['impl_crosscheck'].items():
        L.append(f"|{k}|{c['sm_rel_pct']:.6f}|{c['lstsq_rel_pct']:.6f}|{c['abs_diff_pct_points']:.6e}|")
    L+=["","## Attribution read",
        "- **funding_increment** = B1_plus_funding vs B1 (signed_funding + trailing |funding| percentile, z-scored).",
        "- **ema24_increment** = B1_plus_ema24 vs B1 (ema24_dist, z-scored).",
        "- **joint_increment** = B1_plus_funding_plus_ema24 vs B1 (cached-archive analogue of C2 vs B1 without premium).",
        "- Marginals over the other: ema24_over_funding, funding_over_ema24.",
        "- Negative rel% means the augmented model is worse (higher QLIKE) than baseline.",
        f"",f"Elapsed {out['elapsed_s']:.2f}s"]
    (OUT_DIR/f"rca011_feature_attribution_{UTC}.md").write_text("\n".join(L)+"\n")
    # separate impl crosscheck json
    (OUT_DIR/f"rca011_impl_crosscheck_{UTC}.json").write_text(json.dumps({
        "utc":UTC,"panel":str(IN_PANEL),"method_sm":"statsmodels.api.OLS + Duan smearing (train-only)",
        "method_lstsq":"numpy.linalg.lstsq + Duan smearing (train-only, independent path)",
        "models":{n:{"sm_qlike":out['models'][n]['sm_qlike'],"lstsq_qlike":out['models'][n]['lstsq_qlike'],
                     "max_abs_pred_diff":out['models'][n]['pred_max_abs_diff_sm_vs_lstsq']} for n in SPECS},
        "contrasts":out['impl_crosscheck'],
        "conclusion":"numerical parity indicates no lstsq/smearing implementation artifact explains the recompute degradation" if all((v['abs_diff_pct_points'] or 0) < 1e-6 for v in out['impl_crosscheck'].values()) else "non-trivial implementation divergence observed",
    }, indent=2))
    print('DONE', flush=True)

if __name__=='__main__':
    main()
