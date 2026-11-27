# AGENT HANDOFF — 2026-11-27T18:27:10Z
## Project: Funding-conditioned-volatility-and-liquidation-risk

### PROGRAM STATUS: CLOSED_TERMINAL (verified 2026-11-27)
**Terminal verdict:** NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED
**Source:** `research_state/fclr_final_structural_closure_20261125T161908.md` (rows=71, §17 promotion met=0)
**Ground truth:** `python scripts/next_campaign_status.py` → `CAMPAIGN STATUS: no feasible 3-block design in ANY domain` (verified this session; all domains exhausted — Binance 5-symbol contiguous/disjoint/mark+funding, Hyperliquid bulk, Hyperliquid extended, contagion).

### CAMPAIGN STATUS: NO FEASIBLE 3-BLOCK DESIGN IN ANY DOMAIN
- Binance 5-symbol (mark+premium+index+funding): **EXHAUSTED** — no contiguous run ≥127d, 0/3 disjoint blocks feasible, mark+funding-only 1 individually feasible month (2025-01) <3 mutually non-overlapping
- Hyperliquid bulk (ironflow candles+funding+OI+observed liq): largest untouched span = 24d (need ≥127d)
- Hyperliquid extended (candles+funding+observed liq events): 12 usable months but **no contiguous untouched region** (all inside tested windows)
- Contagion campaign (FCLR-LIQ-CONTAGION-001): rank-0 but not READY_EXECUTE

### LAST EXECUTED WORK (2026-11-27T06:56:00Z)
`FCLR-LIVE-ARCHIVE-07` confirmatory evaluation → **NOT_SUPPORTED**
C2 vs B1 relative QLIKE reduction: **-0.704%** (floor 2%, 95% CI [-1.218%, -0.190%])

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (this session's directive)

**Repo-name priority:** Funding-conditioned-volatility-and-liquidation-risk → funding-conditioned next-24h volatility forecasting is the named domain, but the program is CLOSED_TERMINAL.

**Single highest-value next task: MONITOR ONLY.** Do NOT attempt confirmatory evaluations, build panels, freeze preregistrations, or add status-only files. The campaign is structurally exhausted. The only valid future work is triggered when one of the four reopen conditions below is satisfied by EXTERNAL evidence.

**Execution sequence for the next session:**
1. Read `AGENT_HANDOFF.md` and `RESEARCH_PROMPT.md` completely.
2. Run the ground-truth feasibility check: `python scripts/next_campaign_status.py`. Confirm output ends with `CAMPAIGN STATUS: no feasible 3-block design in ANY domain`. If it instead reports executable heavy work in ANY domain, execute that work (this is the only exception to MONITOR ONLY).
3. Check each of the four reopen conditions below against the repository state. Verify each artifact exists AND passes its machine-checkable predicate. Do NOT act on local cached data alone; each condition requires external evidence.
4. If NO reopen condition is satisfied: write the evidence for the blocker (which condition failed and why), confirm no materially different free route exists, update `AGENT_HANDOFF.md` with the same MONITOR ONLY directive, and stop cleanly. Do not declare the campaign reopenable.
5. If a reopen condition IS satisfied (verified externally): freeze a new preregistration per the relevant gate protocol, execute the evaluation on the newly admissible data/design, update the structural closure document, then re-run `next_campaign_status.py`.

---

### REOPEN CONDITIONS (machine-checkable; DO NOT ACT UNTIL SATISFIED)

| Priority | Condition | Required Evidence | Gate Protocol |
|----------|-----------|-------------------|---------------|
| 1 | `GATE4_BRANCH_1` | `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `fabricated=false, status=RESOLVED_VERIFIED` | RESEARCH_PROMPT.md Gate 4 Branch 1 (external/legal attestation; **never agent-set**) |
| 2 | `NEW_OBSERVED_LIQUIDATION_SOURCE` | `research_state/<source>_admissibility_audit_<UTC>.{md,json}` with `blocks≥3, complete_month≥1, instruments≥5, observed_labels=true, status=ADMISSIBLE, unauthenticated=true` | RESEARCH_PROMPT.md §5/§16 source acceptance + admissibility audit BEFORE prereg |
| 3 | `HL_LABEL_EXTENSION` | `research_state/hl_label_extension_audit_<UTC>.{md,json}` verified post-2026-10-31 observed ironflow labels, min_depth_days≥100, venue=hyperliquid_perpetuals | RESEARCH_PROMPT.md §5/§16 on verified label extension |
| 4 | `EXPANSION_ROBUSTNESS_REDO` | `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation_summary — newly preregistered design meeting all §17 conditions (LOIO≥6/8, placebo/perm >95th pctile) | RESEARCH_PROMPT.md §17 promotion (conditional, non-priority) |

### CONSTRAINTS (HARD; VIOLATION = INVALID SESSION)
- No network, downloads, paid data, manual/credentialed access
- No fabricated provenance, outcomes, or threshold shopping
- No sealed-holdout reuse; no workflow/scheduler/poller additions
- Dep-light reproducibility gate: 48/48 OK (unittest suite)
- Do not modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts
- Do not create root-level `research_state/*.md`/`*.json` files

### NEXT SESSION DIRECTIVE (final)
**MONITOR ONLY.** Verify ground truth via `next_campaign_status.py`; check the four reopen conditions; if none are externally satisfied, record the blocker evidence and stop cleanly. Do not build a new focus campaign — explicit directions are present and the campaign is sealed. No live/paper trading, no risk overlay until the forecast gate passes.

---

*Generated by session at 2026-11-27T18:27:10Z. This handoff is durable; do not overwrite without explicit user direction.*
