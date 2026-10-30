# Volatility baseline recheck 2026-10-30

Campaign: FCLR-HEAVY-001
Time: 2026-10-30T08:44:XXZ (session start)

## FCLR-002 (recomputed)
Command: `FCLR_EXPERIMENT=FCLR-002 timeout 2400 python scripts/run_evaluation.py` (process terminated after writing summary; observed completion)
Summary: `research_state/evaluation_summary_FCLR002.md`
- Test QLIKE: B0=0.543471, B1=0.487438, C1=0.487455, C2=0.442223 (n~8274)
- C2 vs B1: mean diff -0.045215, 95% CI [-0.097648, -0.008788], rel reduction 9.28% (PASS)
- Gate: primary criteria met except blocks (70 days = 2 blocks < 3) -> NOT_MET (as before)
Notes: matches existing published summary; no numerical drift observed.


## FCLR-003 (existing summary, verified)
Summary: `research_state/evaluation_summary_FCLR003.md`
- Test QLIKE: B0=0.487674, B1=0.401884, C1=0.369366, C2=0.417089
- C2 vs B1: mean diff +0.015205, 95% CI [-0.020240, 0.056734], rel reduction -3.78% (NOT_MET)
- C1 vs B1: +8.09% (PASS). C2 worse in this window. Block count OK (3). Gate overall NOT_MET.
Notes: consistent with repo state; no numerical drift from files.
