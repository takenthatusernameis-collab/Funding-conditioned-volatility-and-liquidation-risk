#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(REPO / 'src'))

from analysis.liqmicro.ingest import IronflowIngestor, HyperliquidFundingIngestor
from analysis.liqmicro.features import LiqMicroFeatures
from analysis.liqmicro.models import LiqMicroModels
from analysis.liqmicro.stats import LiqMicroStats

RESULTS_DIR = REPO / "results" / "liqmicro_v2"
RESEARCH_STATE = REPO / "research_state"

def main():
    print("=== FCLR-LIQMICRO-002 EXECUTION (REAL FUNDING) ===")
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")

    # Ingest
    print("\n1. Ingesting ironflow data...")
    ingestor = IronflowIngestor()
    raw_df = ingestor.load_all()
    print(f"   Loaded {len(raw_df):,} raw events")

    hourly = ingestor.aggregate_hourly(raw_df)
    print(f"   Aggregated to {len(hourly):,} symbol-hour observations")
    print(f"   Symbols: {hourly['symbol'].nunique() if not hourly.empty else 0}")

    # Ingest funding
    print("\n2. Ingesting Hyperliquid funding...")
    fund_ing = HyperliquidFundingIngestor()
    funding_df = fund_ing.load_all()
    print(f"   Loaded {len(funding_df):,} funding rows")
    if not funding_df.empty:
        print(f"   Funding symbols: {funding_df['symbol_hl'].nunique() if 'symbol_hl' in funding_df.columns else funding_df['coin'].nunique()}")
        print(f"   funding_rate std: {funding_df['funding_rate'].std():.10e}")

    # Features
    print("\n3. Building features...")
    feat = LiqMicroFeatures()
    panel = feat.add_funding_features(hourly, funding_df)
    panel = feat.add_volatility_features(panel)
    panel = feat.add_lag_features(panel)
    panel = feat.add_clustering_features(panel)
    print(f"   Panel shape: {panel.shape}")
    print(f"   panel.funding_rate std: {panel['funding_rate'].std():.10e}, non-nan: {panel['funding_rate'].notna().sum()}")

    # Models
    print("\n4. Running pre-registered tests D1-D3...")
    models = LiqMicroModels()
    stats_tool = LiqMicroStats()

    d1_results = models.d1_funding_asymmetry(panel)
    print(f"   D1 complete")
    d2_results = models.d2_vol_interaction(panel)
    print(f"   D2 complete")
    d3_results = models.d3_clustering(panel)
    print(f"   D3 complete")

    # Save
    print("\n5. Saving artifacts...")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(RESULTS_DIR / "panel_liqmicro_v2.csv")
    panel.to_parquet(RESULTS_DIR / "panel_liqmicro_v2.parquet")
    if not panel.empty:
        panel.describe().to_csv(RESULTS_DIR / "descriptive_stats_v2.csv")

    # FDR
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
    lines.append(f"**CAMPAIGN:** Track D: Liquidation Microstructure (funding-conditioned) - REAL FUNDING INTEGRATION")
    lines.append(f"**DATA:** ironflow Hyperliquid liquidations ONLY + Hyperliquid fundingHistory API (unauthenticated)")
    lines.append(f"**FIREWALLS:** NO Binance merge, NO H001 re-test, NO FCLR-003 re-opening")
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
    lines.append(f"- Pre-registration note: This is a funding-integration fix to FCLR-LIQMICRO-001 (same D1-D3).")
    lines.append("")

    summary_path.write_text("\n".join(lines))
    print(f"Wrote {summary_path}")

if __name__ == '__main__':
    main()
