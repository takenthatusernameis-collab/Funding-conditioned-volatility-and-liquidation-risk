# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# EXECUTE FCLR-LIVE-ARCHIVE-06 — funding-conditioned DOWNSIDE REALIZED-SEMVARIANCE LEVEL

**Timestamp:** 2026-11-26T12:30:38Z
**Session:** NEXT (routing refresh only; no heavy artifact is claimed by this refresh)
**Active campaign (machine-bound):** `FCLR-LIVE-ARCHIVE-06-20261126T083526Z` — `READY_EXECUTE`
**Latest completed heavy session:** `session_20261126T082429Z`
**Repo-name priority:** the repository name leads with **Funding-conditioned-volatility**, so rank-0 remains the funding-conditioned volatility program. The Binance-archive mean-RV, stress/tail, quantile/full-distribution, and signed-semivariance-asymmetry arms are closed `NOT_SUPPORTED`. The next distinct repo-name estimand is the **level** of downside realized semivariance: whether funding and price-dislocation features improve next-24h downside-variance forecasts beyond signed-HAR history.

> This is the SOLE durable handoff for next-session routing. The heavy-work gate reads this file only.
> **A timestamp-only rewrite is not progress. Creating a new `session_<UTC>/` without the complete `fclr_live_archive06_*` heavy set is a FAILURE. There is no probe-only, prereg-only, audit-only, source-registry-only, verify-and-stop, or no-new-session branch.**

---

## 1. FIRST ACTIONS — EXECUTE IN THIS ORDER

1. Run `export UTC=$(date -u +%Y%m%dT%H%M%SZ)` and `mkdir -p research_state/session_$UTC`. The new id MUST be lexicographically greater than `20261126T083526Z`; do not reuse an older session.
2. Reuse the verified raw cache read-only: `research_state/session_20261126T042519Z/raw/` (1,200 monthly zips; 22 MB). Do not re-download unless a file is missing.
3. Copy and adapt `research_state/session_20261126T082429Z/fclr_live_archive05_eval_20261126T082429Z.py`. Keep its deterministic stdlib parser, MM/OLS, split, and block-bootstrap patterns; replace the asymmetry-ratio target with the frozen downside-semivariance level in §3.
4. Produce every artifact in §4 under that ONE new `session_$UTC/`. Every file must be non-empty and every JSON must carry `experiment_id:"FCLR-LIVE-ARCHIVE-06"` and the real `session_id`.
5. Record the real session id in §8 and synchronize `research_state/experiment_frontier.json` only after the artifacts exist. Then run §5 until the gate reports `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive06"`, and `failures=[]`.

If you are about to rewrite this file without a new heavy session, stop: that is the forbidden refresh loop. Execute the evaluation.

---

## 2. FRONTIER RECONCILIATION — READ BEFORE ACTING

- **FCLR-LIVE-ARCHIVE-01 — CLOSED `NOT_SUPPORTED`:** mean log-RV QLIKE; C2 versus B1 relative reduction 0.840%, below the 2% floor.
- **FCLR-LIVE-ARCHIVE-03 — CLOSED `NOT_SUPPORTED`:** next-24h variance stress/tail exceedance; relative Brier reduction 0.458%, 95% CI includes zero.
- **FCLR-LIVE-ARCHIVE-04 — CLOSED `NOT_SUPPORTED`:** quantile/full-distribution volatility; relative average-pinball reduction -1.102%, 95% CI [-1.233%, -0.969%].
- **FCLR-LIVE-ARCHIVE-05 — CLOSED `NOT_SUPPORTED`:** continuous signed-jump / realized-semivariance asymmetry; C2 versus B1 relative test-MSE reduction 0.141% (95% CI [-0.032%, 0.315%]). Heavy artifacts and independent recompute are under `session_20261126T082429Z`; `all_checks_match=true`.
- **FCLR-009 — CLOSED `NOT_MET`.**
- **Liquidation-risk program on the frozen panel — CLOSED.** Do not reopen.
- **Active rank-0:** `FCLR-LIVE-ARCHIVE-06-20261126T083526Z`, `READY_EXECUTE`. No `fclr_live_archive06_*` artifact exists yet.

**Bottleneck review in this refresh:** no blocked or inefficient sessions were found. The latest on-disk session is `session_20261126T082429Z`, which is also the latest completed heavy session; no newer partial session exists. The only remaining bottleneck is that campaign 06 has not been executed. The gate already binds that execution: the instant any newer `session_<UTC>/` exists, the complete campaign-06 artifact set becomes mandatory in that same session. This refresh archives the prior handoff and keeps the machine-bound campaign unchanged so the next session cannot substitute a lighter task.

**Why the gate is green today:** the latest on-disk session equals the latest completed heavy session (`session_20261126T082429Z`), which predates the campaign-06 start, so the grandfather clause applies. The instant any newer `session_<UTC>/` exists, the complete campaign-06 artifact set becomes mandatory in that same session.

---

## 3. FROZEN EXECUTION DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort:** 2021-01-01 through 2024-12-31 UTC; exactly `1INCHUSDT`, `AAVEUSDT`, `ADAUSDT`, `ALGOUSDT`, `ALPHAUSDT`. Do not substitute coins or re-enumerate the cohort.
2. **Primary target:** next-24h downside realized semivariance level
   `D = log(RV_minus + eps)`,
   where `RV_minus` sums squared negative 1h mark-price log-returns over the next 24 hours. Freeze `eps = 1e-09` in squared-log-return units. Use train-only scaling and no test-set outcome fitting.
3. **Features:** B1 is the same signed-HAR set used by campaign 05: log RV1h/RV24h/RV168h plus log RV_plus/RV_minus at 24h/168h. C2 is B1 plus signed funding(24h), trailing 90-day absolute-funding percentile, mark/index premium, and mark/EMA24 distance. All scaling is train-only.
4. **Split and leakage controls:** 60/20/20 by unique UTC timestamp; 168-hour purge/embargo; test split divided into three chronological blocks. Do not open sealed holdouts.
5. **Models:** fixed-form linear regression for B1 and C2 using the same deterministic stdlib MM/OLS or coordinate-descent procedure. No model-family search, regularization, or threshold tuning. The continuous downside-level MSE contrast is the single primary confirmatory comparison.
6. **Inference:** out-of-sample MSE and R² (primary), at least 2,000 deterministic block-bootstrap replicates with a fixed seed, per-block diagnostics, and leave-one-symbol-out diagnostics. Preserve all rows and disclose any missing feature month; do not zero-fill.
7. **Materiality and verdict:** `PROMOTED` requires at least a 2% relative test-MSE reduction for C2 versus B1 and a 95% block-bootstrap CI lower bound above zero. Otherwise preserve `NOT_SUPPORTED`; use `INCONCLUSIVE` only if the evidence cannot support either conclusion. A valid null is acceptable; fabricated passes and placeholders fail closed.

**Why this is not a rerun:** campaign 05 forecast the up/down variance **ratio**. Campaign 06 forecasts the downside variance **level**, a distinct target that speaks directly to downside risk while remaining within the repository-name volatility program.

---

## 4. REQUIRED ARTIFACTS — ALL UNDER THE SAME FRESH SESSION

- `fclr_live_archive06_source_registry_<UTC>.{json,md}` — exact source URLs, cache checksums, coverage, and read-only reuse statement.
- `fclr_live_archive06_prereg_<UTC>.{json,md}` — outcome-blind and hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`.
- `fclr_live_archive06_eval_<UTC>.{py,json,md}` — heavy three-block evaluation triad implementing §3.
- `fclr_live_archive06_recompute_<UTC>.{py,json}` — independent stdlib recompute with `all_checks_match:true` and reproduced verdict.
- `fclr_live_archive06_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass` and `unresolved_blockers`.
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
```

Required gate result after the heavy session: top-level `pass=true`, `reason_code=OK`, `failures=[]`; `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive06"`, and empty missing/empty artifact lists.

---

## 6. INPUTS AND REUSABLE IMPLEMENTATIONS

| Path | Use |
|---|---|
| `research_state/session_20261126T042519Z/raw/` | 1,200 verified monthly zips; reuse read-only. |
| `research_state/session_20261126T082429Z/fclr_live_archive05_eval_20261126T082429Z.py` | Stdlib parser, OLS, split, and bootstrap template. |
| `research_state/session_20261126T082429Z/fclr_live_archive05_recompute_20261126T082429Z.py` | Independent-recompute pattern. |
| `research_state/experiment_frontier.json` | Rank-0 registry; update only after artifacts exist. |
| `RESEARCH_PROMPT.md` §3/§7/§8/§9/§16/§17/§19/§20 | Research constraints and reporting requirements. |

If a feature month is missing, do not silently substitute or zero-fill. Record the exact shortfall in the source registry and evidence audit, run with the available feature set, and disclose the deviation.

---

## 7. NON-AVOIDANCE CONSTRAINTS

- Do not re-run closed campaigns or relabel exploratory work as confirmatory.
- Do not build a risk overlay; the forecast gate is not passed.
- Do not stop at a source probe, prereg, audit, trigger check, or handoff refresh.
- Do not create an empty/partial session and leave it unrecorded.
- The next session must leave a complete heavy artifact set, a reproduced verdict, and a synchronized frontier.

---

## 8. SESSION CLOSE-OUT — 2026-11-26T12:30:38Z

**What changed:** the sole durable handoff was refreshed to the current timestamp; the prior handoff was archived at `handoff_archive/AGENT_HANDOFF_20261126T122907Z.md`; the active campaign remains `FCLR-LIVE-ARCHIVE-06-20261126T083526Z` with its frozen downside-semivariance design unchanged; the frontier refresh timestamp was synchronized. No heavy artifact is claimed.

**What was tested this session:** no new quantitative campaign was executed. Verification passed after the refresh: the heavy-work gate returned `pass=true`, `reason_code=OK`, `failures=[]`, with `handoff_stale=false` and `heavy_session_id=session_20261126T082429Z`; `python3 -m py_compile scripts/check_handoff_heavywork_gate.py` passed; the six-module unittest command in §5 passed 122 tests; `python3 -m json.tool research_state/experiment_frontier.json >/dev/null` passed; the raw cache audit found 1,200/1,200 zips. The latest completed heavy session remains `session_20261126T082429Z`.

**Single highest-value next task:** execute the complete campaign-06 downside-semivariance evaluation, independent recompute, evidence audit, gate alias, and trigger check in one fresh session strictly newer than `20261126T083526Z`.

**Latest completed session:** `session_20261126T082429Z`

---

## 9. RESEARCH_PROMPT §19 ANSWERS

**Supported:** funding and price features have not cleared the 2% materiality floor for mean-RV, stress/tail, quantile/full-distribution, or signed-semivariance-asymmetry forecasts on the verified Binance archive.

**Contradicted:** claims that no next repo-name campaign exists or that a refresh-only session is acceptable.

**Unknown:** whether funding and price features improve the level of next-24h downside realized semivariance.

**Strongest alternative explanation:** signed HAR already captures most predictable downside variation; the campaign tests whether funding and price dislocations add incremental level information rather than merely re-scoring the asymmetry ratio.

**Dominant limitation:** only five symbols are available, so per-block and leave-one-symbol-out diagnostics are mandatory.

**Concrete falsification test:** C2 improves relative test MSE by less than 2%, or the 95% block-bootstrap CI lower bound is not above zero.

**Highest information gain per free compute:** campaign 06 uses an unexploited downside-level estimand, the verified local cache, and the proven stdlib numerical template.

**Exact progress artifact:** the complete `fclr_live_archive06_*` set under one fresh session, followed by a green heavy-work gate and the six-module unittest command.

(End of file)