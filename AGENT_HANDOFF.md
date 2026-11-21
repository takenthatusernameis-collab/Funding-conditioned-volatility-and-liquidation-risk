# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T01:04:33Z
**Sole active campaign:** FCLR-XSEC-006-20261121T010433Z (rank-0, READY_EXECUTE/ACTIVE, verdict pending)
**Latest completed heavy session on disk:** session_20261121T001225Z (FCLR-XSEC-005, verdict SUPPORTED — notional-weighted low-RV funding contrast CI [452972.90, 850198.89], p=0.0, Holm adj_p 0.0, materiality 0.80 ≥ 0.02; independent recompute reproduces; strong agreement with FCLR-XSEC-004 count-based CI [448605.26, 841155.73])
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS, exit 0; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures.
**Environment:** `pip3 install -r requirements.txt` already run (numpy, pandas, scipy, pyarrow, requests). Python 3.12.3. The frozen FCLR-001 panel and the frozen combined liquidation panel both load; both sha256 values are verified below.

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-XSEC-006). All other campaigns (STARTER-001, FCLR-001, XSEC-001/002/003/004/005, LIQ-XSEC-QLIKE, LIQ-XSEC-ORDERING, LIQ-COMBINED-PANEL) are terminal and must NOT be re-run. A future session that does not emit the Section 4 artifact triad under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T01:04:33Z)

**Why this is the focus (repository-name priority + heaviest non-duplicative work):** This repository is `Funding-conditioned-volatility-and-liquidation-risk`. As of session_20261121T001225Z **both halves of the mandate are now SUPPORTED but regime-distinct**: FCLR-XSEC-002 (volatility, HIGH-RV regime) and FCLR-XSEC-004/005 (liquidation intensity, LOW-RV regime — count-based CI [448605.26, 841155.73] and notional-weighted CI [452972.90, 850198.89], both p=0.0, Holm adj_p 0.0, materiality ~0.80). FCLR-XSEC-005 (session_20261121T001225Z) is COMPLETE: the notional-weighted low-RV liquidation finding agrees with the count-based finding (strong agreement, both high-RV regimes honest nulls). The single heaviest, highest-value, **still-open, non-duplicative** next step matching the repo mandate is to test whether this low-RV liquidation funding effect survives a **different regime definition**: UTC trading-session buckets (Asian/European/US) instead of the RV tercile. That is FCLR-XSEC-006 — a distinct estimand (UTC-session-conditioned cross-sectional funding effect on next-hour notional-weighted liquidation intensity) on the same frozen panel, feasible with zero new data / no network / no credentials. It is the contingency-ladder next mechanism and is *not* a re-run of any terminal campaign.

**State synchronized (this session — 2026-11-21T01:04:33Z):**
- `experiment_frontier.json` rank 0 → FCLR-XSEC-006 READY_EXECUTE/ACTIVE; FCLR-XSEC-005 demoted to SUPERSEDED (last_verdict SUPPORTED); FCLR-XSEC-004 and all others SUPERSEDED.
- `hypothesis_registry.json` H_fclr_xsec_005 terminal SUPPORTED (verdict_recorded=true, last_experiment session_20261121T001225Z, last_verdict SUPPORTED); H_fclr_xsec_006 NOT_STARTED (terminal=false).
- handoff-heavywork gate PASS (exit 0); `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures; root churn cap 499/500 holds.

### Next focus campaign: FCLR-XSEC-006 — UTC-session-bucketed regime-conditioned notional-weighted liquidation-intensity confirmation.

Execute a distinct, unblocked, **heavy** confirmation campaign (no new data, no network, no credentials) that tests whether the FCLR-XSEC-004/XSEC-005 low-RV funding signal survives a **UTC-session-bucketed** regime transform instead of the RV-tercile transform. Concretely:

1. **Panel (frozen, hash-verified — do NOT rebuild):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`, sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14` (1,740,415 rows, 15 coins, 10,052 hourly buckets, 2025-03-22..2026-10-31; columns `timestamp, coin, notional_usd, side, source, tx_hash, fundingRate, premium, abs_fund_pct, mark, ema_dist, rv24h, rv168h`; zero-null features). Assert the sha256 at the top of every script. Use the FCLR-XSEC-005 evaluation + recompute scripts in `research_state/session_20261121T001225Z/` as the structural template — change ONLY the regime variable from RV tercile to UTC trading-session bucket (Asian/European/US).
2. **Pre-register the protocol freeze BEFORE examining any holdout outcome** (`outcome_data_inspected_before_freeze=false`). Define the estimand *ex ante*: hourly **notional-weighted** observed-liquidation intensity per coin = sum of `notional_usd` of observed-liquidation events in the closed UTC hour; **regime** = UTC trading-session bucket at hour t (Asian/European/US; apply Holm across the session-bucket family); **predictor** = within-(hour,session) cross-sectional rank of `abs_fund_pct` (high vs low funding); **baseline (specificity control)** = within-session RV persistence (coin's own rv24h split high/low within session). **Freeze the freeze file first; do not compute outcomes before it exists.**
3. **Recompute the session-conditioned notional-weighted contrast** on the frozen panel: paired within-(hour,session) high-minus-low funding contrast on next-hour notional-weighted liquidation intensity, per session bucket; run the persistence baseline as specificity control; **block bootstrap across whole UTC hours within each session bucket** (seed 20261121, ≥2000 deterministic reps); **Holm over the test family** (session buckets × {funding contrast, persistence baseline}); 95% CIs; **2% materiality floor** (effect / mean-abs-outcome ≥ 0.02). Verdict = SUPPORTED only if a funding-contrast CI excludes zero AND Holm passes AND materiality clears; otherwise preserve the **honest null as NOT_SUPPORTED**. Do not threshold-shop; do not relax the floor after seeing outcomes. Explicitly cross-reference FCLR-XSEC-004 (count-based) and FCLR-XSEC-005 (notional-weighted, RV-tercile) — if the session-bucketed contrast agrees, that is a stronger joint result; if it diverges, report the divergence honestly and do not reconcile by relaxing the floor.
4. **Emit the full heavy artifact triad** under a NEW `research_state/session_<UTC>/` (Section 4), synchronize `experiment_frontier.json` + `hypothesis_registry.json`, and advance this handoff's latest-session line.
5. **Acceptance (the gate):** `python3 scripts/check_handoff_heavywork_gate.py` exits 0 AND `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures; no holdout outcomes inspected before freeze; zero-byte placeholders do NOT count.

**Non-avoidance:** prose, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. The machine-enforced gate requires the concrete artifact triad (protocol_freeze + evaluation + evidence_audit) plus a non-empty `trigger_check` in the latest session directory, and the handoff's latest session id must match the newest on-disk session. A session that re-runs FCLR-STARTER-001 / FCLR-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003 / FCLR-XSEC-004 / FCLR-XSEC-005 or emits a thin count-only re-test of XSEC-004/XSEC-005 has NOT done this task.

---

## 2. Frozen inputs (verified this session — do not re-derive, do not substitute)

- **Primary panel (FCLR-XSEC-005):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 rows × 13 cols, 15 coins, 10,052 hourly buckets, 2025-03-22 19:00 → 2026-10-31 22:00 UTC, zero-null features. Assert the sha256 in the script header.
- **Structural template (FCLR-XSEC-004, SUPPORTED, count-based):** `research_state/session_20261120T230000Z/fclr_xsec004_evaluation_20261120T230000Z.py` (block bootstrap + Holm + materiality + paired-hourly-diff structure) and `research_state/session_20261120T230000Z/recompute_fclr_xsec004_20261120T230000Z.py` (independent recompute). Adapt these — change ONLY the outcome transform from event count to notional-weighted sum.
- **Cross-check panel (FCLR-XSEC-002, sealed):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`, sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4` (29,136 rows × 22 cols, 5 coins, 5,832 hours). Do NOT re-run FCLR-XSEC-002; use only as a hash-frozen reference if a mechanism cross-check is required.

---

## 3. Completed campaigns (terminal — record only, do not re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour cross-sectional funding contrast (RV) | session_20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV) | session_20261120T210000Z | **SUPPORTED** | high-RV regime funding CI [0.0046, 0.2348], p=0.019, materiality 1.09 ≥ 0.02 |
| FCLR-XSEC-003 | *Thin* RV-only holdout re-confirmation | (never executed) | SUPERSEDED | folded into FCLR-XSEC-004 |
| **FCLR-XSEC-004** | **Regime-conditioned funding contrast (next-hour liquidation INTENSITY, count-based)** | **session_20261120T230000Z** | **SUPPORTED** | **low-RV regime funding CI [448605.26, 841155.73], p=0.0, Holm adj_p 0.0, materiality 0.80 ≥ 0.02; high-RV regime honest null (CI incl. 0); independent recompute reproduces** |
| **FCLR-XSEC-005** | **Regime-conditioned funding contrast (next-hour liquidation INTENSITY, notional-weighted dollar severity)** | **session_20261121T001225Z** | **SUPPORTED** | **low-RV regime notional-weighted funding CI [452972.90, 850198.89], p=0.0, Holm adj_p 0.0, materiality 0.80 ≥ 0.02; high-RV honest null (CI incl. 0); independent recompute reproduces; strong agreement with FCLR-XSEC-004 count-based result** |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liquidation intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional *ordering / QLIKE* of daily liquidation intensity | 2026-11-15 | NOT_MET | daily ordering/QLIKE, not regime-conditioned hourly paired contrast |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |

---

## 4. Required artifacts — the heavy work (non-deferrable, machine-enforced)

Create a NEW `research_state/session_<UTC>/` directory (UTC = this session's start time) and emit **all** of the following with meaningful, non-empty contents. Filenames must use the new session's UTC suffix `<UTC>`:

1. `fclr_xsec006_protocol_freeze_<UTC>.json` + `.md` — preregistered protocol, `outcome_data_inspected_before_freeze=false`, `panel_sha256` recorded (assert it: 81a100d5...), estimand = UTC-session-bucketed regime-conditioned cross-sectional funding effect on **next-hour notional-weighted observed liquidation intensity** (distinct from FCLR-XSEC-004's count-based and FCLR-XSEC-005's RV-tercile estimands). **Freeze BEFORE inspecting any liquidation outcome.**
2. `fclr_xsec006_evaluation_<UTC>.py` + `.json` + `.md` — session-conditioned notional-weighted funding contrast on next-hour liquidation intensity (Asian/European/US session buckets), within-session RV-persistence baseline as specificity control, block bootstrap across holdout hours within session bucket (seed 20261121, ≥2000 reps), Holm over the session-bucket × {funding contrast, persistence baseline} family, 2% materiality floor, verdict SUPPORTED or honest NOT_SUPPORTED; explicit cross-reference to FCLR-XSEC-004 and FCLR-XSEC-005.
3. `fclr_xsec006_recompute_<UTC>.py` + `.json` — independent second code path reproducing the evaluation (mirrors `recompute_fclr_xsec004_*`), so the verdict is not a single-implementation artifact.
4. `evidence_audit_<UTC>.json` + `.md` — evidence audit of the artifacts (panel hash verified, freeze preceded outcomes, no sealed mutation, no root-level churn, cross-reference to FCLR-XSEC-004 count result and FCLR-XSEC-005 notional-weighted result).
5. `trigger_check_<UTC>.json` — non-empty; enumerate each acceptance check with PASS/FAIL.

Then synchronize state (no sealed mutation):
- `research_state/experiment_frontier.json`: rank 0 = FCLR-XSEC-006, advance phases PREREG_FREEZE → EVALUATION_AND_GATE → TRIGGER_AND_FRONTIER to COMPLETE with the new UTC, set `last_verdict`, demote FCLR-XSEC-005 to SUPERSEDED, keep all others SUPERSEDED.
- `research_state/hypothesis_registry.json`: H_fclr_xsec_006 status → terminal with verdict (SUPPORTED or NOT_SUPPORTED), `last_experiment`, `last_tested`, `last_verdict`, `terminal`; H_fclr_xsec_005 stays terminal SUPPORTED.
- This AGENT_HANDOFF.md: advance `Latest completed heavy session` to the new `<UTC>` and record the verdict, so the gate's latest-session check stays satisfied.

### Acceptance test (run these — they are the gate)
- `python3 scripts/check_handoff_heavywork_gate.py` exits 0 (prints `[PASS] handoff-heavywork gate: ...`).
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures.
- New `research_state/session_<UTC>/` holds the artifact triad above + recompute + evidence audit + non-empty `trigger_check_<UTC>.json`; no zero-byte placeholders.
- `experiment_frontier.json` rank 0 = FCLR-XSEC-006 ACTIVE/READY_EXECUTE (or terminal if you complete it) with FCLR-XSEC-005 SUPERSEDED; `hypothesis_registry.json` H_fclr_xsec_006 terminal.
- No liquidation outcomes inspected before the protocol freeze.

**Non-avoidance:** prose, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. The machine-enforced gate requires the concrete artifact triad plus a non-empty trigger check in the latest session directory, and the handoff's latest session id must match the newest on-disk session. Re-running FCLR-STARTER-001 / FCLR-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003 / FCLR-XSEC-004 / FCLR-XSEC-005, or emitting a thin count-only re-test of XSEC-004/XSEC-005, does NOT satisfy this task.

---

## 5. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002, FCLR-XSEC-003, or FCLR-XSEC-004 (all terminal/SUPPORTED/SUPERSEDED).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — the root md+json count is **499/500**; one more root-level md/json breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate) and fails. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null here is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations (Track A / this campaign) with modeled boundary breaches (Track B) or with RV forecasts — keep the track separation explicit in every artifact.

---

## 6. Contingency ladder (only if FCLR-XSEC-006 is structurally blocked)

If FCLR-XSEC-006 hits a structural blocker (insufficient regime variation in notional-weighted intensity, funding rank collinear with RV within regimes, or too few coins per (hour, regime) cell to form a paired contrast), document the precise blocker with evidence in the session's `trigger_check_<UTC>.json`, preserve FCLR-XSEC-006 as rank-0 with the blocker recorded, and advance to the next distinct mechanism in order:
1. **FCLR-XSEC-007:** cross-panel mechanism cross-check — does the regime-conditioned funding effect that is SUPPORTED for RV (FCLR-XSEC-002, HIGH-RV) and for liquidation intensity (FCLR-XSEC-004/005, LOW-RV) reconcile on the *same 5-coin FCLR-001 hours* (requires joining the two panels on coin×hour; only if coverage permits).
2. **FCLR-XSEC-008:** alternative regime conditioning — volatility-of-volatility (RV168/RV24 ratio) or funding-rate-volatility buckets instead of RV tercile or UTC session.

A blocker memo is not a substitute for executing a valid bounded free-data task; execute the next valid task in the same session.

---

## 7. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly with the next valid independent task executed.

(End of handoff)