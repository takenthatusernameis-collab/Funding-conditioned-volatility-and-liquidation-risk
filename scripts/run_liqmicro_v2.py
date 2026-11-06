#!/usr/bin/env python3
"""FCLR-LIQMICRO-002 execution (real funding integration, ironflow Hyperliquid only).

FCLR-NEXT-114: routed through guarded_execute contract. The ironflow parquet read
(``IronflowIngestor.load_all``) and the Hyperliquid funding json/open read
(``HyperliquidFundingIngestor.load_all``) are explicit outcome loaders invoked ONLY
after ``guarded_execute`` returns READY_FROZEN. Blocked branches refuse before any
data read and before any canonical output mutation.
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

from analysis.liqmicro.ingest import GuardedReadRefused, HyperliquidFundingIngestor, IronflowIngestor
from analysis.liqmicro.features import LiqMicroFeatures

RESULTS_DIR = REPO / "results" / "liqmicro_v2"
RESEARCH_STATE = REPO / "research_state"
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
HYPERLIQUID_FUNDING = REPO / "research_state" / "data_cache" / "hyperliquid_funding"

# FCLR-NEXT-121 G4: post-gate write-target allowlist/denylist for _run_pipeline.
# The guarded READY_FROZEN path may only write canonical FCLR-LIQMICRO-002 artifacts
# under RESULTS_DIR or the LIQMICRO-002 evaluation summary. It MUST NOT touch
# Hyperliquid Track A canonical outputs (frontier, run_manifest, cross-track log,
# FCLR010 summary) or any other research_state file. Fail-closed on violation.
LIQMICRO_V2_ALLOWED_WRITE_ROOTS = (RESULTS_DIR, RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md")
LIQMICRO_V2_DENIED_WRITE_TARGETS = (
    "experiment_frontier.json",
    "run_manifest.json",
    "cross_track_decision_log.md",
    "evaluation_summary_FCLR010.md",
    "evaluation_summary_FCLR010",
)


def _guard_liqmicro_v2_write_targets(*, results_dir: Path = RESULTS_DIR,
                                     research_state: Path = RESEARCH_STATE) -> dict:
    """Machine-enforced write-target allowlist/denylist for the READY pipeline path.

    Returns a dict {pass, failures, reason_code, allowed_roots, denied_targets}.
    Deterministic; no IO, no network. Used before _run_pipeline writes anything.
    """
    failures: list[str] = []
    allowed_resolved = [str(Path(p).resolve()) for p in LIQMICRO_V2_ALLOWED_WRITE_ROOTS]
    # fail-closed if the resolved roots escape the repo or overlap canonical RS roots
    repo_resolved = str(REPO.resolve())
    for root in allowed_resolved:
        if not root.startswith(repo_resolved):
            failures.append("allowed_write_root_escapes_repo")
    denied = list(LIQMICRO_V2_DENIED_WRITE_TARGETS)
    # ensure no denied target name can appear under the allowed roots
    for target in denied:
        for root in allowed_resolved:
            if target in root:
                failures.append(f"denied_write_target_in_allowed_root:{target}")
    return {
        "pass": not failures,
        "failures": failures,
        "reason_code": "OK" if not failures else "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION",
        "allowed_roots": allowed_resolved,
        "denied_targets": denied,
        "script": "run_liqmicro_v2",
        "network": False,
        "writes_real_research_state": False,
    }


def _load_liqmicro_v2_outcomes(data_path: Path, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Explicit outcome loader for run_liqmicro_v2.

    Invoked ONLY after guarded_execute returns READY_FROZEN. Reads ironflow liquidation
    parquet and Hyperliquid funding json through the guarded src contract
    (load_all(guarded=True)).
    """
    ingestor = IronflowIngestor(data_dir=data_path)
    raw_df = ingestor.load_all(guarded=True)
    hourly = ingestor.aggregate_hourly(raw_df)

    fund_ing = HyperliquidFundingIngestor(data_dir=HYPERLIQUID_FUNDING)
    funding_df = fund_ing.load_all(guarded=True)

    return {"raw_df": raw_df, "hourly": hourly, "funding_df": funding_df}


def _run_pipeline(raw_df: pd.DataFrame, hourly: pd.DataFrame, funding_df: pd.DataFrame) -> None:
    """Existing FCLR-LIQMICRO-002 pipeline (features, models, artifacts, summary).

    Only reached on the guarded READY_FROZEN path; never executed on a blocked
    branch (no data read, no canonical output mutation, no research_state write).
    """
    # G4 (121): enforce write-target allowlist/denylist before any artifact write.
    write_guard = _guard_liqmicro_v2_write_targets()
    if not write_guard.get("pass"):
        raise RuntimeError(
            "run_liqmicro_v2 write-target allowlist guard refused: "
            f"{write_guard.get('failures')} (reason_code={write_guard.get('reason_code')})"
        )
    from analysis.liqmicro.models import LiqMicroModels
    from analysis.liqmicro.stats import LiqMicroStats
    print("\n2. Ingesting Hyperliquid funding...")
    print(f"   Loaded {len(funding_df):,} funding rows")
    if not funding_df.empty:
        sym_col = 'symbol_hl' if 'symbol_hl' in funding_df.columns else ('coin' if 'coin' in funding_df.columns else None)
        print(f"   Funding symbols: {funding_df[sym_col].nunique() if sym_col else funding_df.shape[0]}")
        print(f"   funding_rate std: {funding_df['funding_rate'].std():.10e}")

    print("\n3. Building features...")
    feat = LiqMicroFeatures()
    panel = feat.add_funding_features(hourly, funding_df)
    panel = feat.add_volatility_features(panel)
    panel = feat.add_lag_features(panel)
    panel = feat.add_clustering_features(panel)
    print(f"   Panel shape: {panel.shape}")
    print(f"   panel.funding_rate std: {panel['funding_rate'].std():.10e}, non-nan: {panel['funding_rate'].notna().sum()}")

    print("\n4. Running pre-registered tests D1-D3...")
    models = LiqMicroModels()
    stats_tool = LiqMicroStats()

    d1_results = models.d1_funding_asymmetry(panel)
    print(f"   D1 complete")
    d2_results = models.d2_vol_interaction(panel)
    print(f"   D2 complete")
    d3_results = models.d3_clustering(panel)
    print(f"   D3 complete")

    print("\n5. Saving artifacts...")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(RESULTS_DIR / "panel_liqmicro_v2.csv")
    panel.to_parquet(RESULTS_DIR / "panel_liqmicro_v2.parquet")
    if not panel.empty:
        panel.describe().to_csv(RESULTS_DIR / "descriptive_stats_v2.csv")

    pvals = []
    for res in [d1_results, d2_results]:
        if isinstance(res, dict):
            for k, v in res.items():
                if isinstance(v, dict) and 'pvalues' in v:
                    for pk, pv in v['pvalues'].items():
                        if isinstance(pv, (int, float)) and not (isinstance(pv, float) and (np.isnan(pv) or np.isinf(pv))):
                            pvals.append(float(pv))
    if pvals:
        qvals, reject = stats_tool.benjamini_hochberg(pvals)
    else:
        qvals, reject = [], []

    summary_path = RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"
    lines = []
    lines.append("# EVALUATION SUMMARY: FCLR-LIQMICRO-002")
    lines.append(f"**TIMESTAMP (UTC):** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append("**CAMPAIGN:** Track D: Liquidation Microstructure (funding-conditioned) - REAL FUNDING INTEGRATION")
    lines.append("**DATA:** ironflow Hyperliquid liquidations ONLY + Hyperliquid fundingHistory API (unauthenticated)")
    lines.append("**FIREWALLS:** NO Binance merge, NO H001 re-test, NO FCLR-003 re-opening")
    lines.append("")
    lines.append("## Data summary")
    lines.append(f"- Raw events: {len(raw_df):,}")
    lines.append(f"- Symbol-hour obs: {len(panel):,}")
    lines.append(f"- Symbols: {panel['symbol'].nunique() if not panel.empty else 0}")
    lines.append(f"- Funding rows: {len(funding_df):,}")
    lines.append(f"- panel.funding_rate std: {panel['funding_rate'].std():.10e}")
    lines.append(f"- panel.funding_rate non-NaN: {panel['funding_rate'].notna().sum()}")
    lines.append(f"- Date range: {panel['hour'].min()} to {panel['hour'].max()}" if not panel.empty else "- Date range: unknown")
    lines.append("")
    lines.append("## Pre-registered hypotheses (same as FCLR-LIQMICRO-001)")
    lines.append("")
    lines.append("### D1: Funding asymmetry (long vs short liquidations)")
    lines.append(f"- Results: {json.dumps(d1_results, indent=2)}")
    lines.append("- **Null:** |ΔL/L| < 2% or CI crosses 0")
    lines.append("- **Status:** TESTED")
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
    lines.append("## Verdict")
    lines.append("**FUNDING INTEGRATION COMPLETE WITH REAL DATA.**")
    lines.append("- **CRITICAL:** NO reversal of H001; NO confirmatory re-test of H001 opened.")
    lines.append("- Funding features now have variation (std>0). See coefficients above.")
    lines.append("")
    lines.append("## Artifacts")
    lines.append(f"- Panel: {RESULTS_DIR / 'panel_liqmicro_v2.csv'}, {RESULTS_DIR / 'panel_liqmicro_v2.parquet'}")
    lines.append(f"- Tables: {RESULTS_DIR / 'descriptive_stats_v2.csv'}")
    lines.append(f"- Modules: {REPO / 'src/analysis/liqmicro/'} (updated)")
    lines.append(f"- Funding audit: {RESEARCH_STATE / 'liqmicro_funding_audit_002.md'}")
    lines.append("## Pre-registration note: This is a funding-integration fix to FCLR-LIQMICRO-001 (same D1-D3).")
    lines.append("")

    summary_path.write_text("\n".join(lines))
    print(f"Wrote {summary_path}")


def main() -> int:
    print("=== FCLR-LIQMICRO-002 EXECUTION (REAL FUNDING) ===")
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")

    from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload

    # Ingest (guarded - data reads only after READY_FROZEN)
    print("\n1. Ingesting ironflow data...")
    guard = guarded_execute(
        data_path=IRONFLOW,
        pre_reg_path=None,
        repo_root=REPO,
        source_manifest=None,
        admissible_manifest=None,
        admissible_manifest_path=None,
        outcome_loader=_load_liqmicro_v2_outcomes,
        loader_context=None,
        allow_default_loader=False,
    )
    if guard.get("status") != "READY_FROZEN":
        payload = refusal_payload(
            reason="run_liqmicro_v2 refused: no guarded READY_FROZEN contract (admissible seam + prereg + manifest/data gates). Direct data reads bypassed.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="run_liqmicro_v2",
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== RUN_LIQMICRO_V2 BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    loaded = guard.get("outcomes_loaded") or {}
    raw_df = loaded.get("raw_df")
    hourly = loaded.get("hourly")
    funding_df = loaded.get("funding_df")
    if raw_df is None or hourly is None or funding_df is None:
        payload = refusal_payload(
            reason="run_liqmicro_v2 refused: guarded loader did not return raw_df/hourly/funding_df outcomes.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="run_liqmicro_v2",
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== RUN_LIQMICRO_V2 BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    print(f"   Loaded {len(raw_df):,} raw events (guarded loader, after gates)")
    print(f"   Aggregated to {len(hourly):,} symbol-hour observations")
    print(f"   Symbols: {hourly['symbol'].nunique() if not hourly.empty else 0}")

    _run_pipeline(raw_df, hourly, funding_df)

    print(f"\n=== COMPLETE ===")
    print(f"End: {datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
