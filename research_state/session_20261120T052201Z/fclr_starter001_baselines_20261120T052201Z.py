#!/usr/bin/env python3
"""FCLR-STARTER-001 Step 1 baseline script.

B0: persistence (forecast next-24h realized variance with trailing RV24h).
B1: HAR-style OLS: log(target_rv24h + 1e-12) ~ log(RV1h + 1e-12) + log(RV24h + 1e-12) + log(RV168h + 1e-12),
fit on development (train), evaluated on validation with train-only standardization and a train-only Duan
smearing correction back-transformed to the variance scale. Holdout NOT opened.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
PANEL = REPO / "research_state/fclr011_recompute_panel_20261115T234700Z.parquet"
EPS = 1e-12


def main() -> None:
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    train = df[df["split"] == "train"].copy()
    val = df[df["split"] == "validation"].copy()

    for d in (train, val):
        for c in ["rv1h", "rv24h", "rv168h", "target_rv24h"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d["lr1"] = np.log(d["rv1h"] + EPS)
        d["lr24"] = np.log(d["rv24h"] + EPS)
        d["lr168"] = np.log(d["rv168h"] + EPS)
        d["ly"] = np.log(d["target_rv24h"] + EPS)

    FEAT = ["lr1", "lr24", "lr168"]
    mtr = train[FEAT + ["ly"]].notna().all(axis=1)
    mv = val[FEAT + ["ly"] + ["target_rv24h", "rv24h"]].notna().all(axis=1)

    means = train.loc[mtr, FEAT].mean()
    stds = train.loc[mtr, FEAT].std().replace(0.0, 1.0)

    def z(d):
        return (d[FEAT] - means) / stds

    Xtr = z(train.loc[mtr])
    ytr = train.loc[mtr, "ly"].values
    Xv = z(val.loc[mv])
    yv = val.loc[mv, "target_rv24h"].values

    def ols(X, y):
        Xint = np.column_stack([np.ones(len(X)), X.values])
        return np.linalg.lstsq(Xint, y, rcond=None)[0]

    b_b1 = ols(Xtr, ytr)
    fit_tr = np.column_stack([np.ones(len(Xtr)), Xtr.values]) @ b_b1
    smear = float(np.mean(np.exp(ytr - fit_tr)))
    pred_b1 = np.exp(np.column_stack([np.ones(len(Xv)), Xv.values]) @ b_b1) * smear
    pred_b0 = val.loc[mv, "rv24h"].values

    def metrics(y, p):
        m = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
        if m.sum() == 0:
            return {"qlike": None, "mae": None, "rmse": None, "n": 0}
        yy = y[m]
        pp = p[m]
        ratio = yy / pp
        return {
            "qlike": float(np.mean(ratio - 1.0 - np.log(ratio))),
            "mae": float(np.mean(np.abs(yy - pp))),
            "rmse": float(np.sqrt(np.mean((yy - pp) ** 2))),
            "n": int(m.sum()),
        }

    out = {
        "experiment_id": "FCLR-STARTER-001-20261120T024217Z",
        "split_used": "train_validation_development_validation",
        "holdout_opened": False,
        "n_obs": int(mv.sum()),
        "eps": EPS,
        "smearing_b1": smear,
        "models": {
            "B0": {"kind": "persistence_rv24h", **metrics(yv, pred_b0)},
            "B1": {
                "kind": "har_ols_log_rv1h_rv24h_rv168h_to_log_target_duan_smearing",
                **metrics(yv, pred_b1),
                "smearing": smear,
            },
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
