#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESEARCH = REPO / "research_state"

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True, timeout=300)
        return {
            "cmd": cmd,
            "rc": result.returncode,
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else ""
        }
    except Exception as e:
        return {"cmd": cmd, "error": str(e)}

def main():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = RESEARCH / f"blocker_evidence_{ts}.md"

    cmds = [
        "python scripts/monitor_ironflow_liquidations.py --verify",
        "python scripts/monitor_ironflow_liquidations.py --quick",
        "python scripts/monitor_ironflow_liquidations.py --decision",
        "python scripts/monitor_ironflow_liquidations.py --scan",
        "python -m unittest discover -s tests -v 2>&1 | tail -5",
        "ls research_state/alt_source_scan_*.json | wc -l && echo '---' && ls -lt research_state/alt_source_scan_*.json | head -2",
    ]

    results = []
    for c in cmds:
        results.append(run_cmd(c))

    lines = []
    lines.append(f"# BLOCKER EVIDENCE - Track A Liquidation Forward Validation")
    lines.append(f"**TIMESTAMP:** {ts}")
    lines.append(f"**CAMPAIGN:** LIQUIDATION_FCVR_HEAVY-005")
    lines.append(f"**STATUS:** BLOCKED_ON_DATA (STRUCTURAL)")
    lines.append(f"")
    lines.append(f"## Summary")
    lines.append(f"- Ironflow Hyperliquid liquidations dataset cached through 2026-10 only")
    lines.append(f"- Forward months 2026-11, 2026-12, 2027-01, 2027-02 all return 404")
    lines.append(f"- Consecutive absent >= 3")
    lines.append(f"- No admissible unauthenticated alternative sources found passing full FCLR rubric")
    lines.append(f"- Track B (volatility forecasting) fully unblocked with massive cached data")
    lines.append(f"")
    lines.append(f"## Command Outputs")
    for r in results:
        lines.append(f"### {r['cmd']}")
        if 'error' in r:
            lines.append(f"```\nERROR: {r['error']}\n```")
        else:
            lines.append(f"RC: {r['rc']}")
            if r['stdout']:
                lines.append(f"```\n{r['stdout']}\n```")
            if r['stderr']:
                lines.append(f"STDERR:\n```\n{r['stderr']}\n```")
        lines.append(f"")

    lines.append(f"## Resume Triggers")
    lines.append(f"1. Ironflow: YYYY-MM >= 2026-11 returns 200 with liquidation events/fills schema compatible with FCLR-010")
    lines.append(f"2. New admissible source: >=5 symbols OR broad coverage, >=1 complete month OR >=3x30d blocks, unauthenticated, no keys/requester-pays, license OK, schema mappable to FCLR-010")

    out.write_text("\n".join(lines))
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
