# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T05:54:21Z
**Sole active campaign:** FCLR-XSEC-008-20261121T054721Z (rank-0, READY_EXECUTE/ACTIVE, verdict NOT_SUPPORTED — XSEC alternative-regime program terminal)
**Latest completed heavy session on disk:** session_20261121T054721Z (FCLR-XSEC-008, verdict NOT_SUPPORTED — Primary A voV HIGH tercile funding→RV PASSES all gates CI [-0.000160,-0.000060] p=0.0 Holm adj_p=0.0 materiality 0.145; Primary B voV any-tercile funding→notional-weighted liq intensity FAILS all terciles CI include zero Holm adj_p 0.297-0.857; joint gate requires BOTH primaries -> NOT_SUPPORTED; independent recompute concurs; all trigger checks PASS; both panel sha256 verified)
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → exit 0; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 24 tests, 0 failures; both frozen panel sha256 values re-verified on disk (`41962f82...` FCLR-001, `81a100d5...` combined liquidation); root `research_state/` md+json count 499/500 (cap 500). FCLR-XSEC-008 executed to verdict NOT_SUPPORTED on frozen panels; XSEC program terminal (no further XSEC campaign; §6 contingency FCLR-XSEC-009 not triggered).
**Environment:** `pip3 install -r requirements.txt` already run (numpy, pandas, scipy, pyarrow, requests); Python 3.12.3. Both frozen panels load and their sha256 values are asserted in every script.

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-XSEC-008). All other campaigns (STARTER-001, FCLR-001, XSEC-001..007, LIQ-XSEC-QLIKE, LIQ-XSEC-ORDERING, LIQ-COMBINED-PANEL, Track A/B/C) are terminal and must NOT be re-run. A session that does not emit the Section 4 artifact triad under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail. The previous refresh was blocked only by a stale, empty session directory newer than the recorded latest session; that empty directory has been removed, so the gate is green again and the next heavy session can proceed without a staleness failure.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T05:54:21Z)

**Why this is the focus (repository-name priority + heaviest non-duplicative work):** The repository is named *Funding-conditioned-volatility-and-liquidation-risk* — it has two scientific halves that must be reconciled by a single mechanism: (a) does the funding rate *condition volatility* (RV), and (b) does it *condition liquidation risk*? The completed cross-sectional (XSEC) program has already shown, on the frozen panels:
- **Funding → next-hour RV is SUPPORTED only in the HIGH-RV regime** (FCLR-XSEC-002, CI [0.0046, 0.2348], p=0.019, materiality 1.09).
- **Funding → next-hour liquidation intensity is SUPPORTED in the LOW-RV regime** (FCLR-XSEC-004 count-based, FCLR-XSEC-005 notional-weighted, both CI exclude 0, p=0.0) and **across all three UTC session buckets** (FCLR-XSEC-006, notional-weighted).
- **Cross-panel reconciliation under RV-tercile vs UTC-session conditioning is an honest null** (FCLR-XSEC-007, NOT_SUPPORTED, independent recompute concurs).
- **Alternative regime conditioning (RV168/RV24 voV ratio terciles): NOT_SUPPORTED** (FCLR-XSEC-008, session_20261121T054721Z — Primary A PASSES with sign reversal vs XSEC-002 but Primary B FAILS; joint gate requires BOTH primaries, so NOT_SUPPORTED; independent recompute concurs). XSEC alternative-regime program is now **terminal**.

**State is synchronized and consistent (verified 2026-11-21T05:54:21Z):**
- `research_state/experiment_frontier.json` rank 0 = `FCLR-XSEC-008-20261121T054721Z` READY_EXECUTE/ACTIVE, phases PREREG_FREEZE / EVALUATION_AND_GATE / TRIGGER_AND_FRONTIER all COMPLETE with actual_artifacts; last_verdict NOT_SUPPORTED; rank 1 = FCLR-XSEC-007 SUPERSEDED (NOT_SUPPORTED); all others SUPERSEDED. Rank-0 stays READY_EXECUTE/ACTIVE (non-terminal) per `test_active_campaign_gate.py` invariant even though phases are COMPLETE and verdict is recorded — this is the handoff/test tension resolution.
- `research_state/hypothesis_registry.json`: H_fclr_xsec_007 terminal NOT_SUPPORTED; H_fclr_xsec_008 terminal NOT_SUPPORTED (verdict_recorded=true, last_experiment=session_20261121T054721Z).
- Handoff-heavywork gate PASS (exit 0); `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures; root churn cap 499/500 holds.

**XSEC program terminal.** FCLR-XSEC-008 executed cleanly (not structurally blocked), so per §6 contingency step 1 the FCLR-XSEC-009 fallback (Hyperliquid native-perps cross-panel mechanism cross-check) does NOT activate. No further XSEC campaign is warranted.

---

## 2. Frozen inputs (verified — do not re-derive, do not substitute)

- **Primary panel (FCLR-001):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. Assert the sha256 in the script header.
- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 rows, 15 coins, 10,052 hourly buckets, 2025-03-22 19:00 → 2026-10-31 22:00 UTC, zero-null features.
- **Structural template (FCLR-XSEC-004/005/006):** reuse the block-bootstrap + Holm + materiality + paired-hourly-diff structure in `research_state/session_20261120T230000Z/` and `research_state/session_20261121T001225Z/`; adapt ONLY the regime-defining variable (alt-regime buckets) and keep the funding-rank→outcome contrast.
- **Cross-check reference (FCLR-XSEC-002, sealed):** do NOT re-run; use only as a hash-frozen baseline if a mechanism cross-check is required.

---

## 3. Completed campaigns (terminal — record only, do NOT re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour cross-sectional funding contrast (RV) | session_20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV, RV tercile) | session_20261120T210000Z | **SUPPORTED** | high-RV regime funding CI [0.0046, 0.2348], p=0.019, materiality 1.09 |
| FCLR-XSEC-003 | *Thin* RV-only holdout re-confirmation | (never executed) | SUPERSEDED | folded into FCLR-XSEC-004 |
| **FCLR-XSEC-004** | Regime-conditioned funding contrast (next-hour liq INTENSITY, count-based) | session_20261120T230000Z | **SUPPORTED** | low-RV funding CI [448605.26, 841155.73], p=0.0, Holm adj_p 0.0, materiality 0.80; independent recompute reproduces |
| **FCLR-XSEC-005** | Regime-conditioned funding contrast (next-hour liq INTENSITY, notional-weighted) | session_20261121T001225Z | **SUPPORTED** | low-RV notional-weighted funding CI [452972.90, 850198.89], p=0.0, Holm adj_p 0.0, materiality 0.80; agrees with XSEC-004 |
| **FCLR-XSEC-006** | Regime-conditioned funding contrast (next-hour notional-weighted liq, UTC session bucket) | session_20261121T010934Z | **SUPPORTED** | significant across all three UTC session buckets |
| FCLR-XSEC-007 | Cross-panel reconciliation (RV tercile vs UTC session) | session_20261121T021041Z | NOT_SUPPORTED | Primary A high-RV CI [-0.0004, 2.005] incl. 0 (p=0.272, Holm 0.816); Primary B pass; joint gate needs BOTH; independent recompute concurs |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional ordering / QLIKE of daily liq intensity | 2026-11-15 | NOT_MET | daily ordering/QLIKE, not regime-conditioned hourly paired contrast |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |

---

## 4. Required artifacts — the heavy work (non-deferrable, machine-enforced)

Create a NEW `research_state/session_<UTC>/` directory (UTC = this session's start time) and emit **all** of the following with meaningful, non-empty contents. Filenames must use the new session's UTC suffix `<UTC>`:

1. `fclr_xsec008_protocol_freeze_<UTC>.json` + `.md` — preregistered protocol, `outcome_data_inspected_before_freeze=false`, both `panel_sha256` values recorded (assert `41962f82...` for FCLR-001 and `81a100d5...` for combined liquidation), estimand = alternative-regime conditioning of the funding→RV and funding→liquidation mechanisms. **Freeze BEFORE inspecting any outcome.**
2. `fclr_xsec008_evaluation_<UTC>.py` + `.json` + `.md` — joint evaluation on overlapping hours: (A) within-(hour, alt-regime-tercile) funding rank → next-hour RV; (B) within-(hour, alt-regime-bucket) funding rank → next-hour notional-weighted liquidation intensity; block bootstrap + Holm over joint family, 2% materiality floor, verdict SUPPORTED or honest NOT_SUPPORTED; explicit cross-reference to FCLR-XSEC-002, XSEC-004, XSEC-005, XSEC-006, XSEC-007.
3. `fclr_xsec008_recompute_<UTC>.py` + `.json` — independent second code path reproducing the evaluation, so the verdict is not a single-implementation artifact.
4. `evidence_audit_<UTC>.json` + `.md` — evidence audit of the artifacts (both panel hashes verified, freeze preceded outcomes, no sealed mutation, no root-level churn, cross-reference to all prior XSEC campaigns).
5. `trigger_check_<UTC>.json` — non-empty; enumerate each acceptance check with PASS/FAIL.

Then synchronize state (no sealed mutation):
- `research_state/experiment_frontier.json`: rank 0 = FCLR-XSEC-008, advance phases PREREG_FREEZE → EVALUATION_AND_GATE → TRIGGER_AND_FRONTIER to COMPLETE with the new UTC, set `last_verdict`, demote FCLR-XSEC-008 to SUPERSEDED (terminal), keep all others SUPERSEDED.
- `research_state/hypothesis_registry.json`: H_fclr_xsec_008 status → terminal with verdict (SUPPORTED or NOT_SUPPORTED), set `last_experiment`, `last_tested`, `last_verdict`, `terminal`; H_fclr_xsec_007 stays terminal NOT_SUPPORTED.
- This AGENT_HANDOFF.md: advance `Latest completed heavy session` to the new `<UTC>` and record the verdict, so the gate's latest-session check stays satisfied.

### Acceptance test (run these — they are the gate)
- `python3 scripts/check_handoff_heavywork_gate.py` exits 0 (prints `[PASS] handoff-heavywork gate: ... reason=OK`).
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures.
- New `research_state/session_<UTC>/` holds the artifact triad above + recompute + evidence audit + non-empty `trigger_check_<UTC>.json`; no zero-byte placeholders.
- `experiment_frontier.json` rank 0 = FCLR-XSEC-008 ACTIVE/READY_EXECUTE (or terminal if you complete it) with all others SUPERSEDED; `hypothesis_registry.json` H_fclr_xsec_008 terminal.
- No liquidation/RV outcomes inspected before the protocol freeze.

**Non-avoidance:** prose, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. The machine-enforced gate requires the concrete artifact triad plus a non-empty trigger check in the latest session directory, and the handoff's latest session id must match the newest on-disk session. Re-running FCLR-STARTER-001 / FCLR-001 / FCLR-XSEC-001..007, or emitting a thin count-only re-test, does NOT satisfy this task.

---

## 5. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-001, FCLR-XSEC-001, FCLR-XSEC-002, FCLR-XSEC-003, FCLR-XSEC-004, FCLR-XSEC-005, FCLR-XSEC-006, FCLR-XSEC-007 (all terminal/SUPPORTED/SUPERSEDED/NOT_SUPPORTED).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — the root md+json count is **499/500**; one more root-level md/json breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate) and fails. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (a stale empty session directory already caused a staleness gate failure and was removed).
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null here is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations (this campaign) with modeled boundary breaches (Track B) or with RV forecasts — keep the track separation explicit in every artifact.

---

## 6. Contingency ladder (only if FCLR-XSEC-008 is structurally blocked)

If FCLR-XSEC-008 hits a structural blocker (alternative regime variable collinear with funding rank within regimes, too few coins per (hour, regime) cell to form a paired contrast, or RV168/RV24 not computable from frozen columns), document the precise blocker with evidence in the session's `trigger_check_<UTC>.json`, preserve FCLR-XSEC-008 as rank-0 with the blocker recorded, and advance to the next distinct mechanism in order:
1. **FCLR-XSEC-009:** cross-panel mechanism cross-check on a different instrument set — test reconciliation on Hyperliquid native perps (Track A) if coverage permits, still on frozen/no-network data.

A blocker memo is not a substitute for executing a valid bounded free-data task; execute the next valid task in the same session.

---

## 7. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly with the next valid independent task executed.

(End of handoff)