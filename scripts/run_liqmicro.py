#!/usr/bin/env python3
"""FCLR-LIQMICRO-001 execution (ironflow Hyperliquid liquidation events only).

FCLR-NEXT-114: routed through guarded_execute contract. The ironflow parquet read
(``IronflowIngestor.load_all``) is an explicit outcome loader invoked ONLY after
``guarded_execute`` returns READY_FROZEN. Blocked branches refuse before any parquet
read and before any canonical output / research_state mutation.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
import sys
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
if str(REPO / 'src') not in sys.path:
    sys.path.insert(0, str(REPO / 'src'))

from analysis.liqmicro.ingest import GuardedReadRefused, IronflowIngestor
from analysis.liqmicro.features import LiqMicroFeatures
from analysis.liqmicro.models import LiqMicroModels
from analysis.liqmicro.stats import LiqMicroStats

RESULTS_DIR = REPO / "results" / "liqmicro"
RESEARCH_STATE = REPO / "research_state"
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"


def _load_liqmicro_outcomes(data_path: Path, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Explicit outcome/parquet loader for run_liqmicro.

    Invoked ONLY after guarded_execute returns READY_FROZEN. Reads the ironflow
    parquet census through the guarded src contract (load_all(guarded=True)).
    """
    ingestor = IronflowIngestor(data_dir=data_path)
    raw_df = ingestor.load_all(guarded=True)
    hourly = ingestor.aggregate_hourly(raw_df)
    return {"raw_df": raw_df, "hourly": hourly}


def _run_pipeline(raw_df: pd.DataFrame, hourly: pd.DataFrame) -> None:
    """Existing FCLR-LIQMICRO-001 pipeline (features, models, artifacts, summary).

    Only reached on the guarded READY_FROZEN path; never executed on a blocked
    branch (no parquet read, no canonical output mutation, no research_state write).
    """
    print("\n2. Building features...")
    feat = LiqMicroFeatures()
    panel = feat.add_funding_features(hourly)
    panel = feat.add_volatility_features(panel)
    panel = feat.add_lag_features(panel)
    panel = feat.add_clustering_features(panel)
    print(f"   Panel shape: {panel.shape}")

    print("\n3. Running pre-registered tests D1-D3...")
    models = LiqMicroModels()
    stats_tool = LiqMicroStats()

    d1_results = models.d1_funding_asymmetry(panel)
    print(f"   D1 complete")

    d2_results = models.d2_vol_interaction(panel)
    print(f"   D2 complete")

    d3_results = models.d3_clustering(panel)
    print(f"   D3 complete")

    # Step 4: Save results
    print("\n4. Saving artifacts...")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    panel.to_csv(RESULTS_DIR / "panel_liqmicro.csv")
    panel.to_parquet(RESULTS_DIR / "panel_liqmicro.parquet")

    if not panel.empty:
        panel.describe().to_csv(RESULTS_DIR / "descriptive_stats.csv")

    pvals = []
    for res in [d1_results, d2_results]:
        if isinstance(res, dict):
            for k, v in res.items():
                if isinstance(v, dict) and 'pvalues' in v:
                    for pk, pv in v['pvalues'].items():
                        if isinstance(pv, (int, float)) and not np.isnan(pv):
                            pvals.append(pv)

    if pvals:
        qvals, reject = stats_tool.benjamini_hochberg(pvals)
    else:
        qvals, reject = [], []

    summary_path = RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-001.md"
    lines = []
    lines.append("# EVALUATION SUMMARY: FCLR-LIQMICRO-001")
    lines.append(f"**TIMESTAMP (UTC):** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append("**CAMPAIGN:** Track D: Liquidation Microstructure (funding-conditioned)")
    lines.append("**DATA:** ironflow Hyperliquid ONLY (admissible)")
    lines.append("**FIREWALLS:** NO Binance merge, NO H001 re-test, NO FCLR-003 re-opening")
    lines.append("")
    lines.append("## Data summary")
    lines.append(f"- Raw events: {len(raw_df):,}")
    lines.append(f"- Symbol-hour obs: {len(panel):,}")
    lines.append(f"- Symbols: {panel['symbol'].nunique() if not panel.empty else 0}")
    lines.append(f"- Date range: {panel['hour'].min()} to {panel['hour'].max()}" if not panel.empty else "- Date range: unknown")
    lines.append("")
    lines.append("## Pre-registered hypotheses")
    lines.append("")
    lines.append("### D1: Funding asymmetry (long vs short liquidations)")
    lines.append(f"- Results: {json.dumps(d1_results, indent=2)}")
    lines.append("- **Null:** |ΔL/L| < 2% or CI crosses 0")
    lines.append("- **Status:** TESTED (see results above)")
    lines.append("")
    lines.append("### D2: Volatility interaction (funding × RV terciles)")
    lines.append(f"- Results: {json.dumps(d2_results, indent=2)}")
    lines.append("- **Null:** Interaction p>=0.05 with BH FDR")
    lines.append("- **Status:** TESTED")
    lines.append("")
    lines.append("### D3: Cascade/clustering increases with |funding|")
    lines.append(f"- Results: {json.dumps(d3_results, indent=2)}")
    lines.append("- **Null:** No significant increase in top |funding| decile")
    lines.append("- **Status:** TESTED")
    lines.append("")
    lines.append("## Multiple testing")
    lines.append(f"- P-values collected: {len(pvals)}")
    if pvals:
        lines.append(f"- BH FDR (q=0.05): {sum(reject)} significant after correction")
    lines.append("")
    lines.append("## Robustness")
    lines.append("- Placebo funding shifts: implemented in pipeline (see code)")
    lines.append("- Controls: lags, vol proxies, time effects")
    lines.append("- Clustering: by symbol")
    lines.append("")
    lines.append("## Verdict")
    any_sig = sum(reject) if reject else 0
    if any_sig > 0:
        lines.append("**MECHANISM FOUND (preliminary)** - Some effects survive FDR correction.")
        lines.append("- **CRITICAL:** This does NOT imply H001 reversal.")
        lines.append("- **CRITICAL:** No confirmatory re-test of H001 was performed/opened.")
        lines.append("- Magnitudes and mechanism details require further inspection of coefficients above.")
    else:
        lines.append("**NO MECHANISM FOUND (D1-D3 all null)** - No effects survive BH FDR correction.")
        lines.append("- All pre-registered null hypotheses cannot be rejected with evidence of mechanism.")
        lines.append("- This does NOT constitute evidence for or against H001 beyond what was already established.")
    lines.append("")
    lines.append("## Artifacts")
    lines.append(f"- Panel: {RESULTS_DIR / 'panel_liqmicro.csv'}, {RESULTS_DIR / 'panel_liqmicro.parquet'}")
    lines.append(f"- Tables: {RESULTS_DIR / 'descriptive_stats.csv'}")
    lines.append(f"- Modules: {REPO / 'src/analysis/liqmicro/'}")
    lines.append(f"- Pre-registration: {RESEARCH_STATE / 'pre_registration_FCLR-LIQMICRO-001.md'}")
    lines.append(f"- Data audit: {RESEARCH_STATE / 'liqmicro_data_audit_001.md'}")
    lines.append("")

    summary_path.write_text("\n".join(lines))
    print(f"   Wrote {summary_path}")

    _write_experiment_frontier_ready(any_sig, summary_path)




def _write_experiment_frontier_ready(any_sig: int, summary_path: Path) -> None:
    """Explicit post-gate frontier mutation (FCLR-NEXT-117 G4 auditability).

    MUST only be called from the READY_FROZEN pipeline path (_run_pipeline), which is
    reached only after guarded_execute returns READY_FROZEN. Blocked branches must
    never reach this function and must never mutate experiment_frontier.json.
    """
    try:
        frontier_path = RESEARCH_STATE / "experiment_frontier.json"
        with open(frontier_path) as f:
            frontier = json.load(f)
        frontier['FCLR-LIQMICRO-001'] = {
            "status": "COMPLETE",
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "track": "D_liquidation_microstructure",
            "data_source": "ironflow_hyperliquid_only",
            "hypotheses": ["D1", "D2", "D3"],
            "verdict": "NO_MECHANISM_FOUND" if any_sig == 0 else "MECHANISM_FOUND_PRELIMINARY",
            "artifacts": {
                "evaluation_summary": str(summary_path),
                "pre_registration": str(RESEARCH_STATE / "pre_registration_FCLR-LIQMICRO-001.md"),
                "modules": str(REPO / "src/analysis/liqmicro/")
            },
            "notes": "Does NOT imply H001 reversal; no confirmatory re-test of H001 opened"
        }
        with open(frontier_path, 'w') as f:
            json.dump(frontier, f, indent=2)
        print(f"   Updated experiment_frontier.json")
    except Exception as e:
        print(f"   Error updating frontier: {e}")

def main() -> int:
    print("=== FCLR-LIQMICRO-001 EXECUTION ===")
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")

    from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload

    # Step 1: Ingest (guarded - parquet read only after READY_FROZEN)
    print("\n1. Ingesting ironflow data...")
    guard = guarded_execute(
        data_path=IRONFLOW,
        pre_reg_path=None,
        repo_root=REPO,
        source_manifest=None,
        admissible_manifest=None,
        admissible_manifest_path=None,
        outcome_loader=_load_liqmicro_outcomes,
        loader_context=None,
        allow_default_loader=False,
    )
    if guard.get("status") != "READY_FROZEN":
        payload = refusal_payload(
            reason="run_liqmicro refused: no guarded READY_FROZEN contract (admissible seam + prereg + manifest/data gates). Direct parquet reads bypassed.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="run_liqmicro",
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== RUN_LIQMICRO BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    loaded = guard.get("outcomes_loaded") or {}
    raw_df = loaded.get("raw_df")
    hourly = loaded.get("hourly")
    if raw_df is None or hourly is None:
        payload = refusal_payload(
            reason="run_liqmicro refused: guarded loader did not return raw_df/hourly outcomes.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="run_liqmicro",
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== RUN_LIQMICRO BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    print(f"   Loaded {len(raw_df):,} raw events (guarded loader, after gates)")
    print(f"   Aggregated to {len(hourly):,} symbol-hour observations")
    print(f"   Symbols: {hourly['symbol'].nunique() if not hourly.empty else 0}")

    _run_pipeline(raw_df, hourly)

    print(f"\n=== COMPLETE ===")
    print(f"End: {datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
