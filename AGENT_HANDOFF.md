# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# EXECUTE FCLR-LIVE-ARCHIVE-07 — DISJOINT-COHORT OUT-OF-SAMPLE REPLICATION (2024-04..2026-10, BNB/BTC/ETH/SOL/XRP)

**Timestamp:** 2026-11-26T14:32:24Z
**Session:** EXECUTE (campaign-06 COMPLETED under session_20261126T133828Z; verdict NOT_SUPPORTED)
**Active campaign (machine-bound):** `FCLR-LIVE-ARCHIVE-07-20261126T143224Z` — `READY_EXECUTE`
**Latest completed heavy session:** `session_20261126T133828Z`
**Repo-name priority:** the repository name leads with **Funding-conditioned-volatility**, so rank-0 remains the funding-conditioned volatility program. All five next-24h estimands on the 2021-2024 five-symbol archive (mean-RV QLIKE, stress/tail, quantile/full-distribution, signed-semivariance-asymmetry, downside-realized-semivariance LEVEL) are closed `NOT_SUPPORTED`, and the broad ironflow arms (VOL-BROAD/CORR/STRESS/JUMP) are closed `NOT_SUPPORTED` at broad scale. The single highest-value unexecuted repo-name test is the **pre-registered disjoint-cohort replication**: the 2024-04..2026-10 window on BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT has a verified on-disk cache but has NEVER fed a confirmatory campaign. This is sequential confirmatory look k=2 under RESEARCH_PROMPT.md §17 (alpha-spending: alpha_2 = 0.05/(2x3) = 0.008333), not a re-run: new symbols, new window, new regime, frozen before outcomes.

> This is the SOLE durable handoff for next-session routing. The heavy-work gate reads this file only.
> **A timestamp-only rewrite is not progress. Creating a new `session_<UTC>/` without the complete `fclr_live_archive07_*` heavy set is a FAILURE. There is no probe-only, prereg-only, audit-only, source-registry-only, verify-and-stop, closure-synthesis, or no-new-session branch.**

---

## 1. FIRST ACTIONS — EXECUTE IN THIS ORDER

1. Run `export UTC=$(date -u +%Y%m%dT%H%M%SZ)` and `mkdir -p research_state/session_$UTC`. The new id MUST be lexicographically greater than `20261126T143224Z`; do not reuse an older session.
2. Reuse the verified on-disk cache read-only: `research_state/data_cache/<SYM>_<YYYY_MM>/` for the five symbols in §3. Do not re-download; the environment has no network dependency for this campaign.
3. Copy and adapt `research_state/session_20261126T082429Z/fclr_live_archive05_eval_20261126T082429Z.py`. Keep its deterministic stdlib zip parser, MM/OLS, split, and block-bootstrap patterns; replace the asymmetry-ratio target with the frozen targets in §3. **Do NOT use the `fclr_volbroad01_*` template: this environment has no numpy/pandas/pyarrow installed and package installation is forbidden — stdlib only.**
4. Produce every artifact in §4 under that ONE new `session_$UTC/`. Every file must be non-empty and every JSON must carry `experiment_id:"FCLR-LIVE-ARCHIVE-07"` and the real `session_id`.
5. Record the real session id in §8 and synchronize `research_state/experiment_frontier.json` only after the artifacts exist (rank-0 -> `COMPLETED_VALIDATED` with the reproduced verdict; demote this campaign to a non-zero rank). Then run §5 until the gate reports `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive07"`, and `failures=[]`.

If you are about to rewrite this file without a new heavy session, stop: that is the forbidden refresh loop. Execute the evaluation.

---

## 2. FRONTIER RECONCILIATION — READ BEFORE ACTING

- **FCLR-LIVE-ARCHIVE-01 — CLOSED `NOT_SUPPORTED`:** mean log-RV QLIKE on the 2021-2024 archive; C2 versus B1 relative reduction 0.840%, below the 2% floor.
- **FCLR-LIVE-ARCHIVE-03 — CLOSED `NOT_SUPPORTED`:** next-24h variance stress/tail exceedance; relative Brier reduction 0.458%, 95% CI includes zero.
- **FCLR-LIVE-ARCHIVE-04 — CLOSED `NOT_SUPPORTED`:** quantile/full-distribution volatility; relative average-pinball reduction -1.102%.
- **FCLR-LIVE-ARCHIVE-05 — CLOSED `NOT_SUPPORTED`:** signed-jump / realized-semivariance asymmetry; relative test-MSE reduction 0.141% (95% CI [-0.032%, 0.315%]). Heavy artifacts under `session_20261126T082429Z`; `all_checks_match=true`.
- **FCLR-LIVE-ARCHIVE-06 — CLOSED `NOT_SUPPORTED`:** next-24h downside realized-semivariance **level**; relative test-MSE reduction 0.716% (95% block-bootstrap CI [0.419%,1.020%]), below the 2% floor. Heavy artifacts and independent recompute under `session_20261126T133828Z`; `all_checks_match=true`.
- **Broad-scale ironflow arms — CLOSED `NOT_SUPPORTED`:** FCLR-VOL-BROAD-01 (mean-RV QLIKE, 1.93% < 2%), FCLR-VOL-CORR-01 (funding-extreme correction-time/hazard), FCLR-VOL-STRESS-01 (tail exceedance), FCLR-VOL-JUMP-01 (signed-jump/asymmetry).
- **FCLR-009 — CLOSED `NOT_MET`.** **Liquidation-risk program on the frozen ironflow panel — CLOSED.** Do not reopen.
- **FCLR-LIVE-ARCHIVE-07 — ACTIVE rank-0 `READY_EXECUTE`:** disjoint-cohort replication of the repo-name primary estimand (next-24h mean log-RV QLIKE) with the downside-semivariance level as the declared Holm secondary, on the verified 2024-04..2026-10 five-symbol cache. This is the only remaining heavy confirmatory campaign that is feasible stdlib-only in this environment.

**Bottlenecks removed in this session:** (1) the six-module verification suite was RED — `tests.test_active_campaign_gate.test_frontier_rank0_is_active_heavy_campaign` failed because the prior session left frontier rank-0 at `COMPLETED_VALIDATED`, a status that test forbids at rank-0; rank-0 is now the active campaign-07 entry and the suite is green again. (2) The prior handoff's "close the frontier / negative-results synthesis or confirm exhaustion" direction was a light-work escape hatch; it is replaced by the binding heavy campaign above — a closure-synthesis session now fails the gate. (3) The prior handoff pointed at templates without disclosing that numpy/pandas/pyarrow are absent in this environment; the stdlib-only constraint and the correct template are now explicit. No blocked or inefficient sessions remain.

---

## 3. FROZEN EXECUTION DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort:** 2024-04-01 through 2026-10-31 UTC; exactly `BNBUSDT`, `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`. This cohort is disjoint from the 2021-2024 five-symbol cohort of campaigns 01-06. Do not substitute coins, do not extend into 2026-11 (partial month, no funding zip), and do not re-enumerate the cohort. Funding zips exist 2024-04..2026-10 for all five symbols; klines/index/mark/premium daily zips exist 2024-01..2026-11 (per-day subdirectories `klines-YYYY-MM-DD/` etc. in some months, top-level daily zips in others — record the exact per-month layout in the source registry).
2. **Primary target (repo-name primary, campaign-01 estimand):** next-24h mean log realized variance `y = log(RV_24h_next + eps)`, `eps = 1e-09` in squared-log-return units, from 1h mark-price log-returns. Metric: QLIKE.
3. **Declared secondary (campaign-06 estimand, Holm-adjusted across the 2-family):** next-24h downside realized-semivariance level `D = log(RV_minus + 1e-09)`. Metric: MSE. The family is exactly these two targets; no other target may be added post hoc.
4. **Features:** B1 is the same signed-HAR set used by campaigns 05/06: log RV1h/RV24h/RV168h plus log RV_plus/RV_minus at 24h/168h. C2 is B1 plus signed funding(24h), trailing 90-day absolute-funding percentile, mark/index premium, and mark/EMA24 distance. All scaling is train-only.
5. **Split and leakage controls:** 60/20/20 by unique UTC timestamp; 168-hour purge/embargo; test split divided into three chronological blocks. Do not open sealed holdouts.
6. **Models:** fixed-form linear regression for B1 and C2 using the same deterministic stdlib MM/OLS (or coordinate-descent) procedure as the campaign-05/06 template. No model-family search, regularization, or threshold tuning.
7. **Inference:** out-of-sample QLIKE/MSE and R² (primary), at least 2,000 deterministic block-bootstrap replicates with a fixed seed, per-block diagnostics, and leave-one-symbol-out diagnostics. Preserve all rows and disclose any missing feature month; do not zero-fill. Record any zip that cannot be verified against its `.sha256` sidecar or `research_state/cached_inputs_hashes.json` (20,694 entries) as an exact shortfall in the source registry and evidence audit.
8. **Materiality and verdict:** `PROMOTED` requires the primary C2-versus-B1 relative QLIKE reduction of at least 2% with a 95% block-bootstrap CI lower bound above zero at the look-k=2 alpha (0.008333), and the Holm-adjusted secondary direction consistent. Otherwise preserve `NOT_SUPPORTED`; use `INCONCLUSIVE` only if the evidence cannot support either conclusion. A valid null is acceptable; fabricated passes and placeholders fail closed.

**Why this is not a rerun:** campaigns 01-06 tested the 2021-2024 cohort (1INCH/AAVE/ADA/ALGO/ALPHA). This campaign tests disjoint symbols in a later, higher-liquidity regime (2024-04..2026-10), which is the direct test of the dominant limitation recorded in every prior handoff (five symbols, one window). It is the §17 sequential confirmatory look k=2 with alpha-spending, frozen before any outcome is computed.

---

## 4. REQUIRED ARTIFACTS — ALL UNDER THE SAME FRESH SESSION

- `fclr_live_archive07_source_registry_<UTC>.{json,md}` — exact cache paths, per-file sha256 verification results, coverage per symbol/dataset, layout notes, read-only reuse statement.
- `fclr_live_archive07_prereg_<UTC>.{json,md}` — outcome-blind and hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`; records look k=2 and alpha_2 = 0.008333.
- `fclr_live_archive07_eval_<UTC>.{py,json,md}` — heavy three-block evaluation triad implementing §3.
- `fclr_live_archive07_recompute_<UTC>.{py,json}` — independent stdlib recompute with `all_checks_match:true` and reproduced verdict.
- `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass` and `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — substantive gate-critical alias matching the verdict.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.

No zero-byte placeholders. Stdlib only; do not install packages. Do not add root-level `research_state/*.md` or `*.json` files: the root is at its 500-file cap. Do not modify workflows or overwrite sealed artifacts.

---

## 5. VERIFICATION COMMANDS

```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
tests.test_tracka_hardening_143 tests.test_active_campaign_gate
python3 -m json.tool research_state/experiment_frontier.json >/dev/null
```

Required gate result after the heavy session: top-level `pass=true`, `reason_code=OK`, `failures=[]`; `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive07"`, and empty missing/empty artifact lists. The six-module unittest command must pass 122 tests.

**Pre-existing red legacy modules (do not chase, do not "fix" by installing packages):** `tests.test_tracka_hardening_116/118/119`, `tests.test_fclr016_v5_*`, and `tests.test_fclr024_v5_scope_coherence_report` fail on the pristine tree in this environment (Track A scripts import numpy at load time; numpy/pandas/pyarrow are absent and installation is forbidden). These gate the CLOSED liquidation-risk Track A program, not campaign-07. The six-module command above is the verification contract; do not modify those legacy tests or the closed Track A scripts.

---

## 6. INPUTS AND REUSABLE IMPLEMENTATIONS

| Path | Use |
|---|---|
| `research_state/data_cache/<SYM>_<YYYY_MM>/` (SYM in §3.1) | Verified daily zips + monthly funding zip; reuse read-only. |
| `research_state/cached_inputs_hashes.json` | 20,694-entry sha256 registry; verify and disclose gaps. |
| `research_state/session_20261126T082429Z/fclr_live_archive05_eval_20261126T082429Z.py` | Stdlib parser, OLS, split, and bootstrap template. |
| `research_state/session_20261126T082429Z/fclr_live_archive05_recompute_20261126T082429Z.py` | Independent-recompute pattern. |
| `research_state/experiment_frontier.json` | Rank-0 registry; update only after artifacts exist. |
| `RESEARCH_PROMPT.md` §3/§7/§8/§9/§16/§17/§19/§20 | Research constraints and reporting requirements. |

If a feature month is missing or a zip fails verification, do not silently substitute or zero-fill. Record the exact shortfall in the source registry and evidence audit, run with the available feature set, and disclose the deviation.

---

## 7. NON-AVOIDANCE CONSTRAINTS

- Do not re-run closed campaigns (01/03/04/05/06, broad ironflow arms) or relabel exploratory work as confirmatory.
- Do not build a risk overlay; the forecast gate is not passed.
- Do not stop at a source probe, prereg, audit, trigger check, closure synthesis, or handoff refresh.
- Do not create an empty/partial session and leave it unrecorded.
- The next session must leave a complete heavy artifact set, a reproduced verdict, and a synchronized frontier.

---

## 8. SESSION CLOSE-OUT — 2026-11-26T14:32:24Z

**What changed:** the sole durable handoff was updated to announce campaign `FCLR-LIVE-ARCHIVE-07-20261126T143224Z` as the active rank-0 heavy campaign. The prior handoff was archived at `handoff_archive/AGENT_HANDOFF_20261126T135020Z.md`. `experiment_frontier.json` rank-0 was moved from the terminal campaign-06 entry (`COMPLETED_VALIDATED`, now demoted to a non-zero rank) to the new `READY_EXECUTE` campaign-07 entry with `program_status:"ACTIVE"`, a concrete `next_unfinished_task`, and three pending phases — this repairs the red `test_active_campaign_gate` failure (rank-0 must never hold a completed/superseded campaign). No root-level `research_state` files were added (root remains 500/500). No sealed artifacts were touched.

**What was verified this session:** heavy-work gate `pass=true`, `reason_code=OK`, `failures=[]` (campaign-07 start 20261126T143224Z is after the latest session, so the live-archive binder is grandfathered until the next session executes); the six-module unittest command passes 122 tests after the frontier repair; `python3 -m json.tool research_state/experiment_frontier.json` passes. Cache feasibility was verified on disk: funding zips 2024-04..2026-10 for all five symbols; klines/index/mark/premium daily zips 2024-01..2026-11 with per-file `.sha256` sidecars; 3,689 zips in the symbol dirs; registry sample-verified with zero mismatches.

**Single highest-value next task:** execute campaign-07 exactly as frozen in §3 and produce the complete `fclr_live_archive07_*` artifact set under one fresh `session_<UTC>/` (id > 20261126T143224Z), with an independent stdlib recompute reproducing the verdict, then synchronize the frontier and re-run §5 until green.

**Latest completed session:** `session_20261126T133828Z`

---

## 9. RESEARCH_PROMPT §19 ANSWERS

**Supported:** funding and price features have not cleared the 2% materiality floor for any next-24h volatility estimand on the 2021-2024 five-symbol archive or at broad scale on the ironflow panel; signed-HAR history already captures most predictable variation.

**Contradicted:** claims that no next repo-name campaign exists, that a closure-synthesis or verify-and-stop session is acceptable, or that the frontier is terminal while a verified disjoint-cohort cache is unexecuted.

**Unknown:** whether the funding-conditioned volatility null generalizes to disjoint symbols and the 2024-2026 regime — campaign-07 is the pre-registered look k=2 test of exactly that.

**Strongest alternative explanation:** the null is a five-symbol, single-window artifact; a disjoint-cohort replication either confirms a publishable generalized null or reopens the program.

**Dominant limitation:** only five symbols per cohort are available on the verified archive; per-block and leave-one-symbol-out diagnostics are mandatory.

**Concrete falsification test:** C2 improves relative test QLIKE by at least 2% with bootstrap 95% CI lower bound above 0 at alpha_2 = 0.008333 on the 2024-04..2026-10 cohort.

**Highest information gain per free compute:** campaign-07 reuses a fully verified on-disk cache and the proven stdlib numerical template; either outcome is decisive for the repo-name program.

**Exact progress artifact:** the complete `fclr_live_archive07_*` set under the new session, a green heavy-work gate, and the six-module unittest command passing 122 tests.

(End of file)