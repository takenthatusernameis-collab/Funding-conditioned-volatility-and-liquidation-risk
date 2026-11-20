# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-20T20:55:00Z
**Sole active campaign:** FCLR-XSEC-002-20261120T180707Z (rank-0, READY_EXECUTE / ACTIVE, all phases NOT_STARTED)
**Latest completed heavy session on disk:** session_20261120T210000Z (FCLR-XSEC-002, verdict SUPPORTED)
**Machine-enforced gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS, exit 0; `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 24 tests, 0 failures.
**Environment:** `pip3 install -r requirements.txt` already run this session (numpy, pandas, scipy, pyarrow, requests). Python 3.12.3. The frozen panel loads and its sha256 is verified below.

> This is the SINGLE durable handoff. It supersedes every prior prose handoff block. There is exactly ONE initial task message (Section 1) and exactly ONE active campaign (FCLR-XSEC-002). All other campaigns are terminal and must not be re-run. A future session that does not emit the Section 4 artifact triad under a new `research_state/session_<UTC>/` directory has NOT completed the handoff and the gate will fail.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-20T20:55:00Z)

You are continuing the continuous research program in **Funding-conditioned-volatility-and-liquidation-risk**. Two identification strategies on the frozen FCLR-001 panel have already returned **NOT_SUPPORTED**: the time-series 24h forward-RV forecast (FCLR-STARTER-001) and the within-hour cross-sectional funding-intensity contrast (FCLR-XSEC-001). The ONE remaining high-information, fully-blocked-free task is the pre-registered distinct-regime exploratory campaign:

### Execute FCLR-XSEC-002 — UTC-hour / market-wide-RV conditioning of the funding effect.

This is mechanism 1 of the RESEARCH_PROMPT.md §16 contingency ladder. It is a **distinct estimand** from both prior campaigns: it conditions the within-hour funding contrast on the market-wide realized-variance regime, so a regime-masked effect (funding mattering only in high-RV hours/sessions) would surface here even though the pooled time-series and pooled cross-sectional tests were null. Same frozen panel, no new data, no network, no credentials.

Do it now, in this session, on the frozen panel. Do not defer, do not write a prose-only or trigger-only handoff, do not emit placeholders.

---

## 2. Frozen inputs (verified this session — do not re-derive, do not substitute)

- **Panel:** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`
- **panel_sha256:** `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4` (re-verified this session; assert this hash at the top of every script, exactly as `fclr_xsec001_baselines_20261120T175300Z.py` does).
- **Shape:** 29,136 rows × 22 columns; 5 coins `['BNBUSDT','BTCUSDT','ETHUSDT','SOLUSDT','XRPUSDT']`; 5,832 distinct hours; `ts` from `2026-01-01 00:00:00+00:00` to `2026-08-31 23:00:00+00:00`; 0 duplicate `(coin, ts)` pairs.
- **Columns:** `coin, ts, split, close, open, high, low, rv1h, rv24h, rv168h, target_rv24h, signed_funding, funding_asof_lag_h, abs_funding_pct_trail, abs_funding_trail_n, ema24, ema24_dist, log_rv1h, log_rv24h, log_rv168h, premium, premium_status`.
- **Causal / target construction (identical to the FCLR-XSEC-001 baseline):**
  - Unit = one eligible linear perpetual contract × one fully closed UTC hour `t`; every input available at `t`; outcomes begin at `t+1`.
  - **Target:** next-hour realized variance = `rv1h.shift(-1)` within each coin (`target_rv1h_t1` in the baseline script). Rows with a null target are excluded from that hour's contrast (the baseline uses only non-null targets).
  - **Regime variable:** market-wide RV at hour `t` = cross-sectional mean of `rv1h` across the 5 coins at `t`. Split hours into **high vs low tercile** (primary); a secondary Asian/European/US UTC-session bucketing (UTC hours 0–7 / 8–15 / 16–23) and a high/low median split are registered robustness cuts.
  - **Predictor:** within-hour cross-sectional funding rank. Use `abs_funding_pct_trail` (past-only trailing absolute-funding percentile; `abs_funding_trail_n` gives the observation count, require ≥ 30 as in FCLR-001 §14) — or `signed_funding` as a secondary signed contrast. Within each hour and **within each regime**, split coins into high- vs low-funding by within-(hour,regime) rank and form the paired next-hour RV contrast (high minus low), exactly mirroring the FCLR-XSEC-001 paired-hourly-difference structure.
  - **Baseline:** within-regime RV persistence — within each regime, split coins by their own `rv1h` at `t` (high vs low) and form the paired next-hour RV contrast. This is the same persistence baseline the FCLR-XSEC-001 script implements, now computed per regime.
  - **Inference:** block bootstrap across whole UTC hours within each regime (≥ 2,000 deterministic-seed reps, seed 20261120), Holm correction over the full family (regimes × {funding contrast, persistence baseline}), 95% CIs, materiality floor. Verdict = NOT_SUPPORTED unless a funding-contrast CI excludes zero AND Holm passes AND the effect clears the practical floor; otherwise report the honest null.

Reference implementations to adapt (do not copy verbatim — change the estimand to regime-conditioned):
- Baseline: `research_state/session_20261120T175300Z/fclr_xsec001_baselines_20261120T175300Z.py`
- Evaluation: `research_state/session_20261120T175300Z/fclr_xsec001_evaluation_20261120T175300Z.py`

---

## 3. Completed campaigns (terminal — record only, do not re-run)

| Campaign | Mechanism | Session | Verdict | Key evidence |
|----------|-----------|---------|---------|--------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | session_20261120T052201Z | NOT_SUPPORTED | C2 vs B1 +2.62% rel QLIKE (worse), CI [+0.0024,+0.0164], Holm adj_p 0.075; holdout opened & sealed |
| FCLR-XSEC-001 | Within-hour cross-sectional funding contrast | session_20261120T175300Z | NOT_SUPPORTED | funding contrast mean −0.125751, CI [−0.390010,+0.157598], Holm adj_p 0.388; persistence baseline CI [−0.121076,+0.487735], Holm adj_p 0.514; 5,334 h, 5 coins |
| Track A | Observed-liq forecasting | many | POWER-BLOCKED | RISK-12 MDE 0.0028 > plausible 0.001; not re-runnable without larger panel |
| Track B | Modeled boundary breach | session_20261110T190405Z | NOT_SUPPORTED | TB2 Log Loss +1.68% rel (< 2% floor), CI crosses zero, < 3 blocks |

---

## 4. Required artifacts — the heavy work (non-deferrable, machine-enforced)

Create a NEW `research_state/session_<UTC>/` directory (UTC = this session's start time) and emit **all** of the following with meaningful, non-empty contents. Filenames must use the new session's UTC suffix `<UTC>`:

1. `fclr_xsec002_protocol_freeze_<UTC>.json` + `.md` — preregistered protocol, `outcome_data_inspected_before_freeze=false`, panel_sha256 recorded, estimand distinct from FCLR-001 and FCLR-XSEC-001. **Freeze BEFORE inspecting any outcome.**
2. `fclr_xsec002_baselines_<UTC>.py` + `.json` + `.md` — within-regime RV persistence baselines (per-regime metrics, sample counts, coins, hour ranges).
3. `fclr_xsec002_evaluation_<UTC>.py` + `.json` + `.md` — regime-conditioned funding contrast, block bootstrap, Holm, verdict.
4. `trigger_check_<UTC>.json` — non-empty; enumerate each acceptance check with PASS/FAIL.

Then synchronize state (no sealed mutation):
- `research_state/experiment_frontier.json`: rank 0 = FCLR-XSEC-002, advance phases PREREG_FREEZE → BASELINES → EVALUATION_AND_GATE → TRIGGER_AND_FRONTIER to COMPLETE with the new UTC, set `last_verdict`, keep FCLR-XSEC-001 and all others SUPERSEDED.
- `research_state/hypothesis_registry.json`: H_fclr_xsec_002 status → terminal with verdict (NOT_SUPPORTED or otherwise), `last_experiment`, `last_tested`, `last_verdict`, `terminal` accordingly.
- This AGENT_HANDOFF.md: advance `Latest completed heavy session` to the new `<UTC>` and record the verdict, so the gate's latest-session check stays satisfied.

### Acceptance test (run these — they are the gate)
- `python3 scripts/check_handoff_heavywork_gate.py` exits 0 (prints `[PASS] handoff-heavywork gate: ...`).
- `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` → 0 failures.
- New `research_state/session_<UTC>/` holds the artifact triad above + non-empty `trigger_check_<UTC>.json`; no zero-byte placeholders.
- `experiment_frontier.json` rank 0 = FCLR-XSEC-002 ACTIVE/READY_EXECUTE (or terminal if you complete it) with FCLR-XSEC-001 SUPERSEDED; `hypothesis_registry.json` H_fclr_xsec_002 terminal.
- No holdout outcomes inspected before the protocol freeze.

**Non-avoidance:** prose, trigger-check-only, or placeholder artifacts do NOT satisfy the gate. The machine-enforced gate requires the concrete artifact triad plus a non-empty trigger check in the latest session directory, and the handoff's latest session id must match the newest on-disk session.

---

## 5. Hard constraints (do not violate)

- **Do NOT** re-run FCLR-STARTER-001 or FCLR-XSEC-001 (both frozen/terminal with NOT_SUPPORTED verdicts and complete artifacts).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001 2024-01..03).
- **Do NOT** add any root-level `research_state/*.md` or `research_state/*.json` file — the root md+json count is **499/500**; one more root-level md/json breaches the churn cap (enforced by `tests/test_tracka_hardening_125.py`) and fails the heavy-work gate. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories.
- **Do NOT** threshold-shop or relax the 2% materiality floor after seeing outcomes; a null here is preserved as NOT_SUPPORTED.

---

## 6. Contingency ladder (only if FCLR-XSEC-002 is structurally blocked)

If FCLR-XSEC-002 hits a structural blocker (insufficient regime variation, funding rank collinear with RV within regimes, or too few coins per (hour, regime) cell to form a paired contrast), document the precise blocker with evidence in the session's `trigger_check_<UTC>.json`, preserve FCLR-XSEC-002 as rank-0 with the blocker recorded, and advance to the next distinct mechanism in order:
1. liq_count persistence family (t−1 liquidation count → t liquidation intensity; uses Track A labels already in the combined panel if coverage permits).
2. RISK-13 (advance only if MDE ≤ plausible effect via MDE-by-instrument redesign or larger panel; requires new data).
3. Track B modeled boundary-breach (only if contract specs / margin tiers verifiable from public sources).

A blocker memo is not a substitute for executing a valid bounded free-data task; execute the next valid task in the same session.

---

## 7. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, ensure AGENT_HANDOFF.md answers: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; and any blocker with the next materially different free route. Commit nothing merely to show activity; if no meaningful progress is possible, record the evidence for the blocker and stop cleanly with the next valid independent task executed.

(End of handoff)