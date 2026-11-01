#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
IRONFLOW = REPO / "research_state" / "data_cache" / "ironflow_events"
OUT = REPO / "research_state" / "liqmicro_data_audit_001.md"

def main():
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

    files = sorted([f for f in os.listdir(IRONFLOW) if f.endswith('.parquet')])
    lines.append(f"**Files found:** {len(files)}")
    lines.append("")

    total_events = 0
    all_markets = set()
    all_dates = set()
    has_side_info = True

    # Per file stats
    lines.append("## Per-file inventory")
    lines.append("")
    lines.append("| File | Size (MB) | Rows | Markets | Date range (UTC) | Long/Short present |")
    lines.append("|------|-----------|------|---------|-------------------|--------------------|")

    for fname in files:
        fpath = IRONFLOW / fname
        size_mb = fpath.stat().st_size / (1024*1024)
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
                except:
                    drange = "unknown"
            else:
                drange = "unknown"
            side_col = 'position_side' if 'position_side' in df.columns else ('side' if 'side' in df.columns else None)
            side_info = "yes" if side_col else "no"
            if not side_col:
                has_side_info = False
            lines.append(f"| {fname} | {size_mb:.2f} | {nrows} | {mcount} | {drange} | {side_info} |")
        except Exception as e:
            lines.append(f"| {fname} | {size_mb:.2f} | ERR | - | - | - |")
            lines.append(f"  - Error: {e}")

    lines.append("")
    lines.append("## Aggregate")
    lines.append(f"- **Total events:** {total_events:,}")
    lines.append(f"- **Unique markets:** {len(all_markets)}")
    lines.append(f"- **Date range:** {min(all_dates) if all_dates else 'unknown'} to {max(all_dates) if all_dates else 'unknown'} ({len(all_dates)} unique days)")
    lines.append(f"- **Native perp markets (end with -PERP, no colon):** {len([m for m in all_markets if isinstance(m,str) and m.endswith('-PERP') and ':' not in m])}")
    lines.append(f"- **Long/short separation available:** {has_side_info}")
    lines.append("")

    # Funding data check - look for funding files
    lines.append("## Funding data availability")
    funding_files = []
    for p in REPO.rglob("*funding*"):
        if p.is_file() and not '__pycache__' in str(p):
            funding_files.append(str(p.relative_to(REPO)))
    lines.append(f"- **Funding-related files found:** {len(funding_files)}")
    for ff in funding_files[:15]:
        lines.append(f"  - {ff}")
    if len(funding_files) > 15:
        lines.append(f"  - ... and {len(funding_files)-15} more")
    lines.append("")

    # Check if we can build hourly panels
    lines.append("## Coverage assessment")
    total_days = len(all_dates)
    if total_days > 0:
        hours_approx = total_days * 24
        lines.append(f"- **Approx hours span:** ~{hours_approx}")
        lines.append(f"- **Events per hour (avg):** ~{total_events/hours_approx:.1f}")
        if total_events < 10000:
            lines.append("  - **WARNING:** Liquidation events < 10^4 total (as noted in handoff constraints)")
        else:
            lines.append(f"  - **OK:** {total_events:,} >= 10^4 events total")
    else:
        lines.append("- **ERROR:** No dates found")

    if len(all_markets) >= 5:
        lines.append(f"  - **OK:** {len(all_markets)} >= 5 markets")
    else:
        lines.append(f"  - **WARNING:** {len(all_markets)} < 5 markets")

    lines.append("")
    lines.append("## Notes")
    lines.append("- Using ONLY ironflow Hyperliquid data (admissible per Track A firewall)")
    lines.append("- No Binance data will be merged")
    lines.append("- Data cached at `research_state/data_cache/ironflow_events/`")

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Total events: {total_events:,}, Markets: {len(all_markets)}")

if __name__ == "__main__":
    main()
