# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-20T22:51:15Z
**Sole active campaign:** FCLR-XSEC-004-20261120T225115Z (rank-0, READY_EXECUTE / ACTIVE, all phases NOT_STARTED)
**Latest completed heavy session on disk:** session_20261120T210000Z (FCLR-XSEC-002, verdict SUPPORTED)
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS, exit 0; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 24 tests, 0 failures.
**Environment:** `pip3 install -r requirements.txt` already run (numpy, pandas, scipy, pyarrow, requests). Python 3.12.3. The frozen FCLR-001 panel loads and its sha256 is verified below.

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-XSEC-004). All other campaigns are terminal and must not be re-run. A future session that does not emit the Section 4 artifact triad under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-20T22:51:15Z)

**Why this is the focus (repository-name priority + heaviest non-duplicative work):** This repository is `Funding-conditioned-volatility-and-liquidation-risk`. Every prior SUPPORTED finding is **volatility-only** (FCLR-XSEC-002, regime-conditioned next-hour RV). The **liquidation-risk** half of the mandate has only been tested *time-series-wise* (FCLR-010/TBRACKA expansion panels, all NOT_MET/FRAGILE) and has **never been tested as a regime-conditioned cross-sectional contrast on the combined metpie+ironflow observed-liquidation panel**. That is the single heaviest, highest-value, still-open question that matches the repo's dual mandate. It is a *distinct estimand* (liquidation intensity, not RV), uses a *materially different panel* (1.74M observed-liquidation events, 15 coins, 2025-03-22..2026-10-31), and is *feasible with zero new data / no network / no credentials* (panel already on disk with zero-null causal features). Enqueuing a thin RV-only holdout (the prior handoff's FCLR-XSEC-003) would leave the liquidation-risk half permanently avoided — so this handoff **supersedes FCLR-XSEC-003** and makes liquidation-risk the non-avoidable heavy campaign.

**State synchronized (verified this session):**
- `experiment_frontier.json` rank 0 → FCLR-XSEC-004 READY_EXECUTE/ACTIVE; FCLR-XSEC-002/001/003 and all others SUPERSEDED.
- `hypothesis_registry.json` H_fclr_xsec_004 status NOT_STARTED (terminal=false); H_fclr_xsec_003 demoted to SUPERSEDED (never executed; thin holdout folded into this heavier task).
- handoff-heavywork gate PASS (exit 0); `tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures; root churn cap 499/500 holds.

### Next focus campaign: FCLR-XSEC-004 — regime-conditioned cross-sectional liquidation-intensity confirmation.

Execute a distinct, unblocked, **heavy** confirmation campaign (no new data, no network, no credentials) that tests whether the funding effect generalizes from volatility to **liquidation risk** — the repo's other half. Concretely:

1. **Panel (frozen, hash-verified):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` (1,740,415 rows, 15 coins AAVE/ADA/AVAX/BNB/BTC/CRV/DOGE/ETH/LINK/LTC/NEAR/SOL/SUI/UNI/XRP, 10,052 hourly buckets, 2025-03-22..2026-10-31; columns `timestamp, coin, notional_usd, side, source, tx_hash, fundingRate, premium, abs_fund_pct, mark, ema_dist, rv24h, rv168h`; zero nulls in all features). Assert its sha256 at the top of every script.
2. **Pre-register the protocol freeze BEFORE examining any holdout outcome** (`outcome_data_inspected_before_freeze=false`). Define the estimand *ex ante*: hourly observed-liquidation intensity per coin = count (or notional-weighted sum) of `notional_usd` events in the closed UTC hour; **regime** = market-wide RV tercile at hour t computed from the panel's own `rv24h`/`rv168h` cross-sectional mean (high vs low tercile, mid excluded); **predictor** = within-(hour,regime) cross-sectional rank of `abs_fund_pct` (high vs low funding); **outcome** = next-hour liquidation intensity; **baseline (specificity control)** = within-regime RV persistence (coin's own rv24h split high/low within regime) predicting next-hour liquidation intensity. **Freeze the freeze file first; do not compute outcomes before it exists.**
3. **Recompute the regime-conditioned liquidation contrast** on the frozen panel: paired within-(hour,regime) high-minus-low funding contrast on next-hour liquidation intensity, per regime; run the persistence baseline as specificity control; **block bootstrap across whole UTC hours within each regime** (seed 20261120, ≥2000 deterministic reps); **Holm over the 4-test family** (2 regimes × {funding contrast, persistence baseline}); 95% CIs; **2% materiality floor** (effect / mean-abs-outcome ≥ 0.02). Verdict = SUPPORTED only if a funding-contrast CI excludes zero AND Holm passes AND materiality clears; otherwise preserve the **honest null as NOT_SUPPORTED**. Do not threshold-shop; do not relax the floor after seeing outcomes.
4. **Emit the full heavy artifact triad** under a NEW `research_state/session_<UTC>/` (Section 4), synchronize `experiment_frontier.json` + `hypothesis_registry.json`, and advance this handoff's latest-session line.
5. **Acceptance (the gate):** `python3 scripts/check_handoff_heavywork_gate.py` exits 0 AND `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures; no holdout outcomes inspected before freeze; zero-byte placeholders do NOT count.

**Non-avoidance:** prose, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. The machine-enforced gate requires the concrete artifact triad (protocol_freeze + evaluation + evidence_audit) plus a non-empty `trigger_check` in the latest session directory, and the handoff's latest session id must match the newest on-disk session. A session that re-runs FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003 or emits a thin RV-only holdout has NOT done this task.

---

## 2. Frozen inputs (verified this session — do not re-derive, do not substitute)

- **Primary panel (FCLR-XSEC-004):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — 1,740,415 rows × 13 cols, 15 coins, 10,052 hourly buckets, 2025-03-22 19:00 → 2026-10-31 22:00 UTC, zero-null features. Compute its sha256 and assert it in the script header.
- **Cross-check panel (FCLR-XSEC-002, sealed):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`, sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4` (29,136 rows × 22 cols, 5 coins, 5,832 hours). Do NOT re-run FCLR-XSEC-002; use only as a hash-frozen reference if a mechanism cross-check is required.
- **Reference implementations to adapt (change estimand to liquidation intensity + regime conditioning):**
  - Evaluation pattern: `research_state/session_20261120T210000Z/fclr_xsec002_evaluation_20261120T210000Z.py` (block bootstrap + Holm + materiality + paired-hourly-diff structure).
  - Independent recompute pattern: `research_state/session_20261120T210000Z/recompute_fclr_xsec002_20261120T210000Z.py` (separate code path for reproducibility).
  - Liquidation-panel construction reference: `research_state/fclr_liq_combined_panel_20261115T181405Z` build report (already on disk; do not rebuild).

---

## 3. Completed campaigns (terminal — record only, do not re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | Pooled within-hour cross-sectional funding contrast (RV) | session_20261120T175300Z | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0; persistence CI incl. 0 |
| FCLR-XSEC-002 | Regime-conditioned funding contrast (next-hour RV) | session_20261120T210000Z | **SUPPORTED** | high-RV regime funding CI [0.0046, 0.2348], p=0.019, materiality 1.09 ≥ 0.02; reproduced by independent recompute |
| FCLR-XSEC-003 | *Thin* RV-only holdout re-confirmation | (never executed) | SUPERSEDED | folded into FCLR-XSEC-004 (liquidation-risk is the heavier, non-duplicative task) |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liquidation intensity C2 vs B1 | FCLR-LIQ-COMBINED-20261115T185844Z | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING / -QLIKE | Cross-sectional *ordering / QLIKE* of daily liquidation intensity | 2026-11-15 | NOT_MET | prior xsec liquidation tests were *daily ordering/QLIKE*, not *regime-conditioned paired hourly contrast on the combined hourly panel* — distinct estimand |
| Track A / Track B / FCLR-011 family | observed-liq forecast / modeled boundary / vol forecast | many | blocked/null | see `final_synthesis_report.md` |

---

## 4. Required artifacts — the heavy work (non-deferrable, machine-enforced)

Create a NEW `research_state/session_<UTC>/` directory (UTC = this session's start time) and emit **all** of the following with meaningful, non-empty contents. Filenames must use the new session's UTC suffix `<UTC>`:

1. `fclr_xsec004_protocol_freeze_<UTC>.json` + `.md` — preregistered protocol, `outcome_data_inspected_before_freeze=false`, `panel_sha256` recorded (assert it), estimand = regime-conditioned cross-sectional funding effect on **next-hour observed liquidation intensity** (distinct from FCLR-001, FCLR-XSEC-001/002/003, and the daily ordering/QLIKE liquidation tests). **Freeze BEFORE inspecting any liquidation outcome.**
2. `fclr_xsec004_evaluation_<UTC>.py` + `.json` + `.md` — regime-conditioned funding contrast on next-hour liquidation intensity (high vs low market-wide-RV tercile), within-regime RV-persistence baseline as specificity control, block bootstrap across holdout hours within regime (seed 20261120, ≥2000 reps), Holm over the 4-test family, 2% materiality floor, verdict SUPPORTED or honest NOT_SUPPORTED.
3. `fclr_xsec004_recompute_<UTC>.py` + `.json` — independent second code path reproducing the evaluation (mirrors `recompute_fclr_xsec002_*`), so the verdict is not a single-implementation artifact.
4. `evidence_audit_<UTC>.json` + `.md` — evidence audit of the artifacts (panel hash verified, freeze preceded outcomes, no sealed mutation, no root-level churn).
5. `trigger_check_<UTC>.json` — non-empty; enumerate each acceptance check with PASS/FAIL.

Then synchronize state (no sealed mutation):
- `research_state/experiment_frontier.json`: rank 0 = FCLR-XSEC-004, advance phases PREREG_FREEZE → EVALUATION_AND_GATE → TRIGGER_AND_FRONTIER to COMPLETE with the new UTC, set `last_verdict`, demote FCLR-XSEC-002/001/003 to SUPERSEDED, keep all others SUPERSEDED.
- `research_state/hypothesis_registry.json`: H_fclr_xsec_004 status → terminal with verdict (SUPPORTED or NOT_SUPPORTED), `last_experiment`, `last_tested`, `last_verdict`, `terminal`; H_fclr_xsec_003 → SUPERSEDED/terminal.
- This AGENT_HANDOFF.md: advance `Latest completed heavy session` to the new `<UTC>` and record the verdict, so the gate's latest-session check stays satisfied.

### Acceptance test (run these — they are the gate)
- `python3 scripts/check_handoff_heavywork_gate.py` exits 0 (prints `[PASS] handoff-heavywork gate: ...`).
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures.
- New `research_state/session_<UTC>/` holds the artifact triad above + recompute + evidence audit + non-empty `trigger_check_<UTC>.json`; no zero-byte placeholders.
- `experiment_frontier.json` rank 0 = FCLR-XSEC-004 ACTIVE/READY_EXECUTE (or terminal if you complete it) with FCLR-XSEC-002 SUPERSEDED; `hypothesis_registry.json` H_fclr_xsec_004 terminal.
- No liquidation outcomes inspected before the protocol freeze.

**Non-avoidance:** prose, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. The machine-enforced gate requires the concrete artifact triad plus a non-empty trigger check in the latest session directory, and the handoff's latest session id must match the newest on-disk session. Re-running FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003, or emitting a thin RV-only holdout, does NOT satisfy this task.

---

## 5. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001, FCLR-XSEC-001, FCLR-XSEC-002, or the thin FCLR-XSEC-003 (all frozen/terminal/superseded).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — the root md+json count is **499/500**; one more root-level md/json breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py` and the gate) and fails. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null here is preserved as NOT_SUPPORTED.
- **Do NOT** conflate observed liquidations (Track A / this campaign) with modeled boundary breaches (Track B) or with RV forecasts — keep the track separation explicit in every artifact.

---

## 6. Contingency ladder (only if FCLR-XSEC-004 is structurally blocked)

If FCLR-XSEC-004 hits a structural blocker (insufficient regime variation in liquidation intensity, funding rank collinear with RV within regimes, or too few coins per (hour, regime) cell to form a paired contrast), document the precise blocker with evidence in the session's `trigger_check_<UTC>.json`, preserve FCLR-XSEC-004 as rank-0 with the blocker recorded, and advance to the next distinct mechanism in order:
1. **FCLR-XSEC-005:** regime-conditioned *notional-weighted* (not count) liquidation-intensity contrast on the same panel (different outcome transform, same freeze discipline).
2. **FCLR-XSEC-006:** UTC-session-bucketed (Asian/European/US) regime-conditioned liquidation contrast (robustness cut promoted to primary if tercile split is degenerate).
3. **FCLR-XSEC-007:** cross-panel mechanism cross-check — does the regime-conditioned funding effect that is SUPPORTED for RV (FCLR-XSEC-002) also appear for liquidation intensity on the *same 5-coin FCLR-001 hours* (requires joining the two panels on coin×hour; only if coverage permits).

A blocker memo is not a substitute for executing a valid bounded free-data task; execute the next valid task in the same session.

---

## 7. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly with the next valid independent task executed.

(End of handoff)