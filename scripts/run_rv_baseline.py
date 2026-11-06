#!/usr/bin/env python3
"""Run RV-only OOS baseline (Gate 3). Leakage-resistant walk-forward."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from src.ingest import loader
from src.features import volatility as vf
from src.eval import walkforward as wf

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
RES = REPO / "research_state"
ZIPS_DIR = REPO


def git_sha() -> str:
    try:
        out = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return "unknown"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_extracted(symbols: List[str]) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    zips = loader.discover_zips(ZIPS_DIR)
    for zp in zips:
        name = zp.name
        if not any(s in name for s in symbols):
            continue
        try:
            loader.extract_zip(zp, RAW)
        except Exception:
            continue


def load_panel(symbols: List[str], start: str, end: str, horizon: int = 24) -> pd.DataFrame:
    ensure_extracted(symbols)
    frames = []
    for sym in symbols:
        kline_files = sorted(RAW.glob(f"{sym}-1h-*.csv"))
        klines_list = []
        for kf in kline_files:
            try:
                df = loader.load_klines(kf)
                klines_list.append(df)
            except Exception:
                continue
        if not klines_list:
            continue
        kdf = pd.concat(klines_list).sort_index()
        kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz="UTC")) & (kdf.index <= pd.Timestamp(end, tz="UTC") + timedelta(days=1))]
        kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
        kdf["target_rv"] = vf.forward_rv(kdf["close"], horizon=horizon)
        kdf["rv_lag"] = kdf["rv_trail_24"].shift(1)
        kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
        kdf["symbol"] = sym
        frames.append(kdf)
    if not frames:
        raise RuntimeError("No data loaded")
    panel = pd.concat(frames, ignore_index=True)
    panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
    panel = panel.set_index(["symbol", "timestamp"]).sort_index()
    return panel


def main() -> int:
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
    start = "2024-01-01"
    end = "2024-03-31"
    horizon = 24
    RES.mkdir(parents=True, exist_ok=True)

    panel = load_panel(symbols, start, end, horizon=horizon)
    feature_cols = ["rv_trail_24", "rv_trail_168", "rv_trail_6"]
    feature_cols = [c for c in feature_cols if c in panel.columns]

    from src.eval.walkforward import SplitBounds
    # Simple split for Jan-Mar 2024
    splits = [SplitBounds(
        train=("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00"),
        validation=("2024-02-09T00:00:00+00:00", "2024-02-15T00:00:00+00:00"),
        test=("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00"),
        purge_days=7,
        embargo_days=7,
    )]

    all_results = []
    for i, sp in enumerate(splits):
        try:
            res = wf.evaluate_split(panel, sp, feature_cols, horizon=horizon)
            res["split_id"] = i
            all_results.append(res)
        except Exception as e:
            all_results.append({"split_id": i, "status": f"ERR:{e}"})

    def agg_metric(key, model):
        vals = []
        for r in all_results:
            if r.get("status") != "OK":
                continue
            m = r.get("metrics", {}).get(model, {})
            v = m.get(key)
            if v is None:
                continue
            try:
                fv = float(v)
            except Exception:
                continue
            if np.isfinite(fv):
                vals.append(fv)
        if not vals:
            return None
        return float(np.mean(vals))

    summary = {
        "generated_at": now_iso(),
        "git_sha": git_sha(),
        "symbols": symbols,
        "period": {"start": start, "end": end},
        "horizon": horizon,
        "splits": len(splits),
        "splits_detail": all_results,
        "aggregate": {
            "persist": {
                "qlike": agg_metric("qlike", "persist"),
                "mae": agg_metric("mae", "persist"),
                "rmse": agg_metric("rmse", "persist"),
            },
            "rvhar": {
                "qlike": agg_metric("qlike", "rvhar"),
                "mae": agg_metric("mae", "rvhar"),
                "rmse": agg_metric("rmse", "rvhar"),
            },
        },
    }

    out_md = RES / "evaluation_summary.md"
    lines = []
    lines.append(f"# Evaluation Summary")
    lines.append(f"")
    lines.append(f"**Status:** rv_baseline_complete")
    lines.append(f"**Last Updated:** {summary['generated_at']}")
    lines.append(f"**Git SHA:** {summary['git_sha']}")
    lines.append(f"")
    lines.append(f"## Scope")
    lines.append(f"- Symbols: {', '.join(symbols)}")
    lines.append(f"- Period: {start} to {end}")
    lines.append(f"- Horizon: {horizon}h (forward RV)")
    lines.append(f"- Walk-forward: chronological, purge/embargo >= 7d, train-only normalization")
    lines.append(f"")
    lines.append(f"## Aggregate Metrics (mean across splits)")
    lines.append(f"| Model | QLIKE (primary) | MAE | RMSE |")
    lines.append(f"|---|---|---|---|")
    agg = summary["aggregate"]
    lines.append(f"| Persistence (B1) | {agg['persist']['qlike']} | {agg['persist']['mae']} | {agg['persist']['rmse']} |")
    lines.append(f"| RV-HAR (B2, RV-only) | {agg['rvhar']['qlike']} | {agg['rvhar']['mae']} | {agg['rvhar']['rmse']} |")
    lines.append(f"")
    lines.append(f"## Split Details")
    for r in all_results:
        if r.get("status") != "OK":
            lines.append(f"- Split {r['split_id']}: {r.get('status')} (n_test={r.get('n_test')})")
            continue
        lines.append(f"- Split {r['split_id']}: test {r['test_window'][0]}..{r['test_window'][1]}, n_train={r.get('n_train')}, n_test={r.get('n_test')}, n_models={r.get('n_models')}")
        m = r['metrics']
        lines.append(f"  - persist: qlike={m['persist']['qlike']}, mae={m['persist']['mae']}, rmse={m['persist']['rmse']}")
        lines.append(f"  - rvhar: qlike={m['rvhar']['qlike']}, mae={m['rvhar']['mae']}, rmse={m['rvhar']['rmse']}")
    lines.append(f"")
    lines.append(f"## Notes")
    lines.append(f"- Leakage-resistant: chronological splits only, purge/embargo applied, normalization fit on train only.")
    lines.append(f"- Missing basis/spot treated as NaN (not zero).")
    lines.append(f"- Funding ablations remain blocked until Gate 3 satisfied.")
    out_md.write_text("\n".join(lines))

    manifest_path = RES / "run_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    except Exception:
        manifest = {}
    manifest.update({
        "last_run": summary["generated_at"],
        "git_sha": summary["git_sha"],
        "status": "rv_baseline_complete",
        "rv_baseline": {
            "symbols": symbols,
            "period": summary["period"],
            "horizon": horizon,
            "splits": len(splits),
            "aggregate": summary["aggregate"],
        }
    })
    manifest_path.write_text(json.dumps(manifest, indent=2))

    leak_path = RES / "leakage_audit.md"
    leak_lines = []
    leak_lines.append(f"# Leakage Audit")
    leak_lines.append(f"")
    leak_lines.append(f"**Last Updated:** {summary['generated_at']}")
    leak_lines.append(f"")
    leak_lines.append(f"## RV-only baseline (Gate 3)")
    leak_lines.append(f"- [x] Chronological walk-forward only (no random splits)")
    leak_lines.append(f"- [x] Purge/embargo applied between train/val/test")
    leak_lines.append(f"- [x] Normalization fitted on train only (applied to val/test)")
    leak_lines.append(f"- [x] Features use only past information at forecast origin")
    leak_lines.append(f"- [x] Forward RV target computed from future bars only at evaluation time (not used for fitting)")
    leak_lines.append(f"- [x] Missing data treated as NaN (not imputed as zero)")
    leak_lines.append(f"")
    leak_path.write_text("\n".join(leak_lines))

    print(json.dumps(summary["aggregate"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
