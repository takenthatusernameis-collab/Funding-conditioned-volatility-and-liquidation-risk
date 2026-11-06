#!/usr/bin/env python3
"""LIQMICRO Data Audit (FCLR-LIQMICRO-001) — ironflow Hyperliquid liquidation events only.

FCLR-NEXT-112: routed through guarded_execute contract. Direct parquet/pandas reads
are an explicit outcome_loader invoked ONLY after guarded_execute returns READY_FROZEN.
Blocked branches refuse before any parquet read.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional

REPO = Path(__file__).resolve().parents[1]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
OUT = REPO / "research_state" / "liqmicro_data_audit_001.md"


def _load_liqmicro_outcomes(data_path: Path, context: Optional[Dict] = None) -> Dict:
    """Explicit outcome/parquet loader for liqmicro audit.

    Invoked ONLY after guarded_execute returns READY_FROZEN. Reads parquet files
    to compute audit statistics (no outcome/QLIKE/model inspection).
    """
    import pandas as pd

    files = sorted([f for f in os.listdir(data_path) if f.endswith('.parquet')]) if data_path.exists() else []
    total_events = 0
    all_markets = set()
    all_dates = set()
    has_side_info = True
    per_file = []

    for fname in files:
        fpath = data_path / fname
        size_mb = fpath.stat().st_size / (1024 * 1024)
        try:
            df = pd.read_parquet(fpath)
            nrows = len(df)
            total_events += nrows
            if 'market' in df.columns:
                markets = set(df['market'].astype(str).unique())
                all_markets.update(markets)
                mcount = len(markets)
            else:
                mcount = 0
            if 'timestamp' in df.columns:
                try:
                    ts = pd.to_datetime(df['timestamp'])
                    dmin = ts.min()
                    dmax = ts.max()
                    drange = f"{dmin.date()} to {dmax.date()}"
                    for d in ts.dt.date:
                        all_dates.add(d)
                except Exception:
                    drange = "unknown"
            else:
                drange = "unknown"
            side_col = 'position_side' if 'position_side' in df.columns else ('side' if 'side' in df.columns else None)
            side_info = "yes" if side_col else "no"
            if not side_col:
                has_side_info = False
            per_file.append({
                "fname": fname, "size_mb": round(size_mb, 2), "rows": nrows, "markets": mcount,
                "drange": drange, "side_info": side_info,
            })
        except Exception as e:
            per_file.append({
                "fname": fname, "size_mb": round(size_mb, 2), "rows": "ERR", "markets": "-",
                "drange": "-", "side_info": "-", "error": str(e),
            })

    native_markets = [m for m in all_markets if isinstance(m, str) and m.endswith('-PERP') and ':' not in m]
    return {
        "files": files,
        "total_events": total_events,
        "all_markets": sorted(list(all_markets)),
        "native_markets": native_markets,
        "native_count": len(native_markets),
        "all_dates": sorted([str(d) for d in all_dates]),
        "date_count": len(all_dates),
        "has_side_info": has_side_info,
        "per_file": per_file,
    }


def main():
    from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload

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
            reason="liqmicro_audit refused: no guarded READY_FROZEN contract (admissible seam + prereg + manifest/data gates). Direct parquet reads bypassed.",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="liqmicro_audit",
            guard=guard,
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        print(f"=== LIQMICRO-AUDIT BLOCKED {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===", flush=True)
        return 1

    loaded = guard.get("outcomes_loaded")
    lines = []
    lines.append("# LIQMICRO Data Audit (FCLR-LIQMICRO-001)")
    lines.append(f"**TIMESTAMP (UTC):** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    lines.append(f"**Source (admissible):** ironflow Hyperliquid liquidation events ONLY")
    lines.append(f"**Path:** {IRONFLOW}")
    lines.append("")

    if not IRONFLOW.exists():
        lines.append("**ERROR:** ironflow cache missing")
        OUT.write_text("\n".join(lines))
        print(f"Wrote {OUT}")
        return

    lines.append(f"**Files found:** {len(loaded['files'])}")
    lines.append("")

    # Per file stats
    lines.append("## Per-file inventory")
    lines.append("")
    lines.append("| File | Size (MB) | Rows | Markets | Date range (UTC) | Long/Short present |")
    lines.append("|------|-----------|------|---------|-------------------|--------------------|")

    for pf in loaded["per_file"]:
        lines.append(f"| {pf['fname']} | {pf['size_mb']:.2f} | {pf['rows']} | {pf['markets']} | {pf['drange']} | {pf['side_info']} |")
        if "error" in pf:
            lines.append(f"  - Error: {pf['error']}")

    lines.append("")
    lines.append("## Aggregate")
    lines.append(f"- **Total events:** {loaded['total_events']:,}")
    lines.append(f"- **Unique markets:** {len(loaded['all_markets'])}")
    if loaded["all_dates"]:
        lines.append(f"- **Date range:** {loaded['all_dates'][0]} to {loaded['all_dates'][-1]} ({loaded['date_count']} unique days)")
    else:
        lines.append("- **Date range:** unknown to unknown (0 unique days)")
    lines.append(f"- **Native perp markets (end with -PERP, no colon):** {loaded['native_count']}")
    lines.append(f"- **Long/short separation available:** {loaded['has_side_info']}")
    lines.append("")

    # Funding data check
    lines.append("## Funding data availability")
    funding_files = []
    for p in REPO.rglob("*funding*"):
        if p.is_file() and '__pycache__' not in str(p):
            funding_files.append(str(p.relative_to(REPO)))
    lines.append(f"- **Funding-related files found:** {len(funding_files)}")
    for ff in funding_files[:15]:
        lines.append(f"  - {ff}")
    if len(funding_files) > 15:
        lines.append(f"  - ... and {len(funding_files)-15} more")
    lines.append("")

    # Coverage assessment
    lines.append("## Coverage assessment")
    total_days = loaded["date_count"]
    if total_days > 0:
        hours_approx = total_days * 24
        lines.append(f"- **Approx hours span:** ~{hours_approx}")
        lines.append(f"- **Events per hour (avg):** ~{loaded['total_events']/hours_approx:.1f}")
        if loaded['total_events'] < 10000:
            lines.append("  - **WARNING:** Liquidation events < 10^4 total (as noted in handoff constraints)")
        else:
            lines.append(f"  - **OK:** {loaded['total_events']:,} >= 10^4 events total")
    else:
        lines.append("- **ERROR:** No dates found")

    if loaded['native_count'] >= 5:
        lines.append(f"  - **OK:** {loaded['native_count']} >= 5 markets")
    else:
        lines.append(f"  - **WARNING:** {loaded['native_count']} < 5 markets")

    lines.append("")
    lines.append("## Notes")
    lines.append("- Using ONLY ironflow Hyperliquid data (admissible per Track A firewall)")
    lines.append("- No Binance data will be merged")
    lines.append("- Data cached at `research_state/data_cache/ironflow_events/`")

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Total events: {loaded['total_events']:,}, Markets: {len(loaded['all_markets'])}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
