# AGENT_HANDOFF.md — Durable Single Source of Truth for Next Session

**Generated (UTC):** 2026-11-26T17:47:27Z
**Program status:** CLOSED_TERMINAL (per `fclr_final_structural_closure_20261124T025751.md` and `final_record_closure_audit.md`)
**Terminal verdict:** NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED
**HEAD:** (check `git rev-parse HEAD`)
**Working tree:** clean (per `git status`)

---

## 1. EXECUTIVE SUMMARY

The confirmatory research program **Funding-conditioned-volatility-and-liquidation-risk** has exhausted all feasible confirmatory paths on admissible frozen data. Every hypothesis/experiment track has been tested to a terminal verdict:

| Track / Hypothesis | Terminal Verdict | Key Evidence |
|---|---|---|
| **H1_primary** (Funding-conditioned volatility improvement) | **NOT_SUPPORTED** | FCLR-011 PASS (4.94%, 2026-05..08) did NOT replicate forward (FCLR-FWD-VOL-011-CONFIRM: -5.55%, CI favours B1). Overlay INELIGIBLE. |
| **H2_shek_replication** | **EXPLORATORY_ONLY** | SSRN 403 blocks full methodology; 88 events Jan-Mar 2024. Structural impossibility. |
| **H_trackb_modeled_breaches** | **NOT_SUPPORTED** | FCLR-TRACKB-MODELED-BREACH-01: modeled breach proxy, NOT observed liquidation; rel Brier -2.00% long / -1.00% short; CI95 upper includes 0. |
| **Track A** (Observed liquidations, FCLR-H004) | **BLOCKED/EXHAUSTED** | ≥2 materially distinct source families exhausted (Binance liquidationSnapshot 404, fapi forceOrders 451; Bybit trades non-census; HuggingFace 2026-only undercounting; Zenodo/GitHub no admissible census). No admissible liquidation census with ≥5 symbols, ≥3 non-overlapping 30-day blocks. |
| **Track B** (Modeled boundary-breach) | **NOT_SUPPORTED** | FCLR-003, FCLR-006, H003 all sealed negative/inconclusive. |
| **Track C** (Volatility: FCLR-VOL-BROAD-01, CORR-01, STRESS-01, JUMP-01/02/03) | **NOT_SUPPORTED** (all arms) | 4 broad-panel arms closed at ironflow_bulk scale (342-799 coins, 18 months): mean QLIKE (+1.93% < 2% floor), correction-time (-10% contrast, floor NOT met), stress/tail (+1.51% < 2% floor), jump (+0.3025% < 2% floor). JUMP-03 (multi-estimator/horizon leakage-hardened) closed the arm definitively. |
| **Liquidation cross-sectional** (FCLR-LIQ-XSEC-BROAD-01) | **SUPPORTED_GENERALIZATION** but **materiality NOT MET** | Rank-IC positive (long 0.155, short -0.002), bootstrap CI excludes null, placebo passes, LOIO 8/8, Holm primary significant — BUT Poisson deviance materiality floor (2%) NOT MET (long -0.23%, short +0.71%). Temporal stability (FCLR-LIQ-XSEC-BROAD-TS-01) → **NOT_STABLE**. |
| **FCLR-LIQ-CONTAGION** (cross-coin contagion panel) | **ACTIVE** (rank-0 in frontier) | 1.74M observed-liquidation event panel. Program ACTIVE/READY_EXECUTE but no evaluation artifact yet. See §4. |

**Bottom line:** No confirmatory experiment meeting §17 promotion conditions can be frozen and executed on current admissible data. The program is **closed** pending one of the reopen conditions below.

---

## 2. REOPEN CONDITIONS (Machine-Checkable — Act ONLY When Satisfied)

From `fclr_final_structural_closure_20261124T025751.md` — **do_not_act_until_satisfied: True** for all:

| Condition | Priority | Predicate (must be met exactly) | Required Evidence Artifact |
|---|---|---|---|
| **GATE4_BRANCH_1** | 1 (external) | Human/legal attestation; file `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `{"fabricated": false, "status": "RESOLVED_VERIFIED"}` | `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` |
| **NEW_OBSERVED_LIQUIDATION_SOURCE** | 2 | Unauthenticated source with `status: "ADMISSIBLE"`, `observed_labels: true`, `instruments >= 5`, AND (`blocks >= 3` OR `complete_month >= 1`), provenance/license/venue_consistent documented | `research_state/<source>_admissibility_audit_<UTC>.{md,json}` |
| **HL_LABEL_EXTENSION** | 3 | Verified post-2026-10-31 observed ironflow labels from `ironflow/hyperliquid-liquidations` with `min_depth_days >= 100`, `observed_only: true` | `research_state/hl_label_extension_audit_<UTC>.{md,json}` |
| **EXPANSION_ROBUSTNESS_REDO** | 4 (non-priority) | Newly preregistered design with LOIO ≥ 6/8 subsets pass AND placebo/permutation true effect > 95th percentile of null; MUST NOT re-score sealed 19.04% result | `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary |

**→ The next session MUST run `scripts/next_campaign_status.py` and `scripts/check_handoff_heavywork_gate.py` first. If no reopen condition is satisfied, the session MUST acknowledge closure and produce NO new confirmatory work.**

---

## 3. CAMPAIGN STATUS SNAPSHOT (from `scripts/next_campaign_status.py`)

```
== CAMPAIGN STATUS: no feasible 3-block design in ANY domain ==

Domains scanned:
- Binance 5-symbol (mark+premium+index klines + funding): 3 ready months (2024-04, 2024-05, 2025-01) — NONE feasible for disjoint 30-day blocks (train history unfunded)
- Mark+funding-only (B0/B1/C1): 1 individually feasible block (2025-01) — need ≥3 mutually non-overlapping
- Hyperliquid bulk (ironflow: candles_1h + funding + OI + liquidations): 24-day untouched region (2025-05-01..2025-05-24) — need ≥127 days for 3-block
- Hyperliquid extended (candles+funding+observed-liq events, 17 coins): 12 usable months (2025-11..2026-10) but ALL inside tested windows — no untouched contiguous region
```

**Contagion campaign** (`FCLR-LIQ-CONTAGION-01`): Rank-0 in `experiment_frontier.json`, status=READY_EXECUTE, program=ACTIVE, panel=`fclr_liq_combined_panel_20261115T181405Z.parquet` (1.74M rows). **No evaluation artifact exists yet.** This is the ONLY active heavy-work campaign on the frozen panel.

---

## 4. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

### IF a reopen condition IS satisfied (verified by artifacts in `research_state/`):

1. **Identify which condition fired** — read the corresponding evidence artifact.
2. **Freeze a NEW outcome-blind prereg** with a NEW experiment ID (UTC > 2026-11-26T17:43:46Z) under `research_state/session_<UTC>/`.
3. **Execute the heavy evaluation triad** (eval + independent stdlib recompute + evidence audit + gate alias + trigger check) in that same session directory.
4. **All artifacts non-empty** — prefix per campaign convention (e.g., `fclr_voljump04_`, `fclr_tracks01_v2_`, `fclr_liq_contagion01_`).
5. **Update `experiment_frontier.json`** and `AGENT_HANDOFF.md` AFTER artifacts exist.

### IF NO reopen condition is satisfied (the expected case):

**The session MUST:**
1. Run `scripts/next_campaign_status.py` — confirm "no feasible 3-block design in ANY domain".
2. Run `scripts/check_handoff_heavywork_gate.py` — confirm no heavy-work gate passes.
3. **Produce a closure acknowledgment artifact** under `research_state/session_<UTC>/`:
   - `fclr_program_closure_ack_<UTC>.{json,md}` — explicit acknowledgment that program remains CLOSED_TERMINAL, no confirmatory work feasible, reopen conditions unsatisfied.
   - Include verbatim output of both status scripts.
   - Record `git rev-parse HEAD` and `git status`.
4. **Update THIS `AGENT_HANDOFF.md`** with the new session timestamp and closure acknowledgment path.
5. **Do NOT** create any confirmatory experiment, prereg, or evaluation artifact.
6. **Do NOT** write root-level `research_state/*.md|*.json` (cap 500 at root — all new artifacts MUST go under `session_<UTC>/`).

---

## 5. HARD CONSTRAINTS (Violations = Failed Session)

| Constraint | Enforcement |
|---|---|
| **No sealed experiment re-run** | Only read-only verification allowed (tests, byte-identical reproduction of unsealed confirmations like FCLR-006). |
| **No threshold shopping** | Materiality floors (2%), Holm families, §17 conditions frozen at prereg. |
| **No fabrication** | All data from frozen caches (`research_state/data_cache/`); no network for confirmatory work. |
| **No track adulteration** | Track A (observed liq), Track B (modeled breach), Track C (volatility) — do not mix estimands across tracks. |
| **No overlay without §9 gate** | Forecast gate (QLIKE + Brier + LogLoss ALL pass) required; none passed. |
| **Root file cap** | `research_state/*.md|*.json` ≤ 500 at root — all new artifacts under `session_<UTC>/`. |
| **Prereg before outcomes** | `outcome_data_inspected_before_freeze: false` mandatory; sha256 input assertions. |
| **NEW_OBSERVED_LIQUIDATION_SOURCE cannot fire on frozen data** | It is a trigger for NEW admissible source discovery, not an excuse to idle. |

---

## 6. KEY ARTIFACT PATHS (for verification)

| Artifact | Path |
|---|---|
| Final structural closure | `research_state/fclr_final_structural_closure_20261124T025751.md` |
| Final record closure audit | `research_state/final_record_closure_audit.md` |
| Experiment frontier | `research_state/experiment_frontier.json` |
| Negative results report | `research_state/negative_results_report.md` |
| Final synthesis report | `research_state/final_synthesis_report.md` |
| Ironflow bulk cache | `research_state/data_cache/ironflow_bulk/` (2025-05..2026-10, 18 months) |
| Liquidation combined panel | `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` |
| Campaign status script | `scripts/next_campaign_status.py` |
| Heavy-work gate checker | `scripts/check_handoff_heavywork_gate.py` |

---

## 7. VERIFICATION COMMANDS (run at session start)

```bash
# 1. Campaign feasibility
python3 scripts/next_campaign_status.py

# 2. Heavy-work gate
python3 scripts/check_handoff_heavywork_gate.py

# 3. Git state
git rev-parse HEAD
git status

# 4. Reopen condition check (manual - look for artifacts in research_state/)
ls -la research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "GATE4_BRANCH_1: NOT SATISFIED"
ls -la research_state/*_admissibility_audit_*.json 2>/dev/null | head -5
ls -la research_state/hl_label_extension_audit_*.json 2>/dev/null || echo "HL_LABEL_EXTENSION: NOT SATISFIED"
ls -la research_state/expansion_robustness_redo_prereg_*.json 2>/dev/null || echo "EXPANSION_ROBUSTNESS_REDO: NOT SATISFIED"
```

---

## 8. SESSION TEMPLATE (if closure acknowledgment needed)

```markdown
# Session Closure Acknowledgment — <UTC>
Session: session_<UTC>/
Program status: CLOSED_TERMINAL (unchanged)
Reopen conditions verified: NONE SATISFIED
Campaign status output: [paste next_campaign_status.py output]
Heavy-work gate output: [paste check_handoff_heavywork_gate.py output]
Git HEAD: <sha>
Git status: clean
Artifacts produced: fclr_program_closure_ack_<UTC>.{json,md}
AGENT_HANDOFF.md updated: yes
```

---

**This document is the durable single source of truth.** Future agents MUST read this first, run the verification commands, and act ONLY per the decision tree in §4. No "next task" pointers outside this document are valid.

**END OF HANDOFF — 2026-11-26T17:47:27Z**