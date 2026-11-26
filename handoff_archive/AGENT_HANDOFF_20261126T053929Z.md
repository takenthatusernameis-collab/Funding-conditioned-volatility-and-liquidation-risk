# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# AGENT_HANDOFF.md — FCLR-LIVE-ARCHIVE-04 Funding-Conditioned Quantile Volatility Arm (repo-name rank-0)

**Timestamp:** 2026-11-26T05:39:29Z
**Session:** ROUTING REFRESH ONLY (no heavy artifact claimed)
**Active campaign (machine-bound):** `FCLR-LIVE-ARCHIVE-04-20261126T053929Z` — status `READY_EXECUTE`.
**Repo-name priority:** the repository name leads with **Funding-conditioned-volatility** → rank-0 remains the funding-conditioned volatility program. The mean-RV QLIKE arm, correction-time arm, stress/tail arm, and signed-jump arm are closed. The next repo-name estimand is the **full predictive distribution / quantile-volatility** arm, which has never been tested confirmatory on the verified 2021–2024 Binance archive.
**Status:** FCLR-LIVE-ARCHIVE-01 CLOSED NOT_SUPPORTED | FCLR-LIVE-ARCHIVE-03 CLOSED NOT_SUPPORTED | FCLR-LIVE-ARCHIVE-04 READY_EXECUTE

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **A timestamp-only rewrite is NOT progress and is forbidden. The next session MUST materialize the full `fclr_live_archive04_*` heavy artifact set in a fresh `session_<UTC>/` with UTC > `20261126T053929Z`.**

---

## 0. RECONCILIATION — CURRENT FRONTIER TRUTH (read first)

- **FCLR-LIVE-ARCHIVE-01 is CLOSED (do NOT re-run):** mean log-RV QLIKE, C2 vs B1 relative reduction 0.840% < 2% floor, session_20261126T042519Z.
- **FCLR-LIVE-ARCHIVE-03 is CLOSED (do NOT re-run):** next-24h realized-variance stress/tail exceedance, C2 vs B1 relative Brier reduction 0.458% (95% CI [-0.966%, 1.972%]) < 2% floor, session_20261126T051548Z.
- **FCLR-009 is CLOSED (do NOT re-run):** NOT_MET.
- **Liquidation-risk program is CLOSED** on the frozen panel. Do not reopen.
- **Active rank-0:** `FCLR-LIVE-ARCHIVE-04-20261126T053929Z` — funding-conditioned **quantile / full-distribution volatility forecasting** on the same verified 5-symbol 2021–2024 Binance archive. READY_EXECUTE; no `fclr_live_archive04_*` artifact exists yet.

**Bottleneck removed (do not re-introduce):** the prior frontier ended in a terminal “no next campaign” state, which let a future session verify-and-stop. That escape hatch is closed by the machine-bound FCLR-LIVE-ARCHIVE-04 binder below: the next post-start session cannot pass with a trigger-only, prose-only, prereg-only, audit-only, source-probe-only, verify-and-stop, or refresh-only session.

---

## 1. What Changed & Why

The frozen 18-month `ironflow_bulk` panel and the 4-year Binance archive have now rejected the mean, stress, correction-time, and signed-jump volatility estimands. Per RESEARCH_PROMPT.md §16 (adaptive feasibility) and §10 (continuous priorities), the next materially different repo-name test is the **predictive distribution** of next-24h realized variance: quantile forecasts at pre-registered levels, scored with pinball loss and calibration, rather than a mean QLIKE or a binary tail label. This is a distinct outcome family and is feasible today with the verified raw cache.

---

## 2. What Was Actually Tested — Exact Outcomes (on-disk, authoritative)

| Artifact | Status | Evidence |
|----------|--------|----------|
| FCLR-LIVE-ARCHIVE-01 mean-RV QLIKE | CLOSED NOT_SUPPORTED | rel 0.840% < 2%; session_20261126T042519Z |
| FCLR-LIVE-ARCHIVE-03 stress/tail Brier | CLOSED NOT_SUPPORTED | rel 0.458%, CI includes 0; session_20261126T051548Z |
| Frozen `ironflow_bulk` volatility arms | CLOSED NOT_SUPPORTED | BROAD/CORR/STRESS/JUMP |
| Liquidation-risk program (frozen panel) | CLOSED | Track A blocked; B/C not supported; xsec not stable + floor not met |
| FCLR-LIVE-ARCHIVE-04 quantile volatility | READY_EXECUTE | no heavy artifact yet; this handoff is routing only |

---

## 3. Evidence Added & Where (this session)

- This `AGENT_HANDOFF.md` — sole durable routing refresh to FCLR-LIVE-ARCHIVE-04.
- No new research_state session and no new quantitative artifact is claimed. The latest completed heavy session remains `session_20261126T051548Z`.

---

## 4. Current State of Each Research Gate

| Gate | Status | Evidence |
|------|--------|----------|
| Source feasibility (Binance archive) | DATA_READY | 1,200/1,200 monthly zips cached + checksum-verified under session_20261126T042519Z/raw/ |
| Coverage / cohort freeze | FROZEN | 5 symbols × 48 months, outcome-blind (2021–2024) |
| FCLR-LIVE-ARCHIVE-01 mean-RV QLIKE | CLOSED NOT_SUPPORTED | rel 0.840% < 2% |
| FCLR-LIVE-ARCHIVE-03 stress/tail | CLOSED NOT_SUPPORTED | rel Brier 0.458% < 2% |
| FCLR-LIVE-ARCHIVE-04 protocol freeze | NOT STARTED | next session must freeze before outcomes |
| Forecast gate (§9) | NOT PASSED | risk overlay remains ineligible |
| Heavy-work gate | PASS (grandfathered) | latest on-disk session `session_20261126T051548Z` predates campaign start `20261126T053929Z`; post-start session will require the full `fclr_live_archive04_*` set |

---

## 5. Single Highest-Value Next Task

**Execute the full FCLR-LIVE-ARCHIVE-04 artifact set in ONE fresh `research_state/session_<UTC>/` (UTC strictly > `20261126T053929Z`): a heavy 3-block confirmatory quantile-volatility evaluation + independent stdlib recompute + evidence audit + trigger check, with a valid `NOT_SUPPORTED` / `PROMOTED` / `INCONCLUSIVE` verdict.**

### Frozen execution design — DO NOT re-derive, expand, or threshold-shop

1. **Window & symbols (FROZEN, reuse the verified cache):** 2021-01-01 → 2024-12-31 UTC; EXACTLY `1INCHUSDT`, `AAVEUSDT`, `ADAUSDT`, `ALGOUSDT`, `ALPHAUSDT`. Reuse the raw monthly zips under `research_state/session_20261126T042519Z/raw/` read-only; do NOT re-download unless a file is missing. Do NOT re-enumerate or substitute coins.
2. **Target (DISTINCT family — full distribution):** next-24h realized variance, forecast as a predictive distribution at the pre-registered quantile levels **{0.10, 0.25, 0.50, 0.75, 0.90}**. Quantiles are estimated from training data only; no test-set quantile fitting.
3. **Features:** B1 = HAR log RV1h/RV24h/RV168h only. C2 = B1 + signed funding(24h) + trailing 90d |funding| percentile + mark/index premium + mark/EMA24 distance. Train-only scaling; 7-day (168h) purge/embargo; 60/20/20 by unique UTC timestamp; test → 3 blocks.
4. **Models:** fixed-form linear quantile regression fitted by a deterministic stdlib method (coordinate descent or IRLS); identical fitting procedure for B1 and C2. No external packages.
5. **Metrics & inference:** average pinball loss across the five quantiles (primary), per-quantile pinball loss, empirical coverage, and calibration diagnostics; ≥2,000 deterministic block-bootstrap replicates (fixed seed); per-block + leave-one-symbol-out.
6. **Materiality floor:** **≥2% relative reduction in average pinball loss** for C2 vs B1, with the 95% block-bootstrap CI lower bound > 0. If the floor is not met, preserve `NOT_SUPPORTED`; a null is valid.
7. **Verdict:** valid `NOT_SUPPORTED`, `PROMOTED`, or `INCONCLUSIVE` only when the evidence supports it. Fabricated passes / zero-byte placeholders = FAIL CLOSED.

### Required artifacts — ALL under the SAME fresh `session_<UTC>/`, non-empty, `fclr_live_archive04_` infix MANDATORY

- `fclr_live_archive04_source_registry_<UTC>.{json,md}` — reuse verified cache, exact URLs, checksums, coverage.
- `fclr_live_archive04_prereg_<UTC>.{json,md}` — outcome-blind, hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`.
- `fclr_live_archive04_eval_<UTC>.{py,json,md}` — heavy 3-block quantile-volatility evaluation triad.
- `fclr_live_archive04_recompute_<UTC>.{py,json}` — independent stdlib recompute, `all_checks_match:true`.
- `fclr_live_archive04_evidence_audit_<UTC>.{json,md}` — evidence/leakage audit with `audit_pass` + `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — gate-critical alias (substantive, verdict matches).
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.

Every JSON must carry `experiment_id:"FCLR-LIVE-ARCHIVE-04"` and the real `session_id`. Do NOT write a future/non-existent session id before the artifacts exist.

---

## 6. Precise Command/Check to Verify Progress

```bash
# After the artifacts exist under the new session_<UTC>/ (UTC > 20261126T053929Z):
python3 scripts/check_handoff_heavywork_gate.py --json
# Expect: pass=true, reason_code=OK, live_archive.required=true, live_archive.pass=true,
#         live_archive.artifact_family="live_archive04", failures=[]

python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
  tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 tests.test_active_campaign_gate
```

Gate-pass condition: the latest on-disk `session_<UTC>` must have UTC > `20261126T053929Z` and contain all required `fclr_live_archive04_*` files above, each non-empty, plus a non-empty `trigger_check_*.json`. `missing_required_artifacts` and `empty_required_artifacts` must both be `[]`. Record the new session id in THIS handoff after the artifacts exist.

---

## 7. Blockers & Next Materially Different Free Route

**No external blockers.** The cohort is cached and checksum-verified; the source, budget, stdlib-only deps, artifact-naming, and root-cap bottlenecks are resolved. The raw cache is reusable read-only.

**If a step fails** (e.g., a feature month missing): do NOT silently substitute or zero-fill. Record the exact shortfall in the source registry/evidence audit, emit the evaluation with the available feature set, and note the deviation.

**Do NOT** re-run FCLR-LIVE-ARCHIVE-01 or FCLR-LIVE-ARCHIVE-03 or any closed arm, re-open sealed holdouts, modify the frozen protocol, build a risk overlay, threshold-shop, or relabel exploratory work as confirmatory.

---

## 8. Bottlenecks Removed (do not re-introduce)

- **RESOLVED — terminal “verify green and stop” frontier:** the prior handoff had no open heavy campaign. FCLR-LIVE-ARCHIVE-04 is now machine-bound and READY_EXECUTE.
- **RESOLVED — refresh loop:** timestamp-only handoff rewrites do not satisfy the post-start binder; the next session must emit the full evaluation + recompute + audit set.
- **RESOLVED — re-download cost:** the 5-symbol × 48-month × 5-source cohort is cached and checksum-verified; reuse read-only.
- **RESOLVED — artifact-naming deadlock:** the gate’s ladder maps campaign 04 → `fclr_live_archive04_*`.
- **RESOLVED — root churn:** root `research_state/*.md|*.json` = 500/500 (AT CAP). All new artifacts go under `session_<UTC>/`.
- **OPEN — execution:** the next session must freeze, evaluate, recompute, audit, and record the real session id without stopping at a probe, prereg, audit, or refresh.

---

## 9. NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- A timestamp-only rewrite is NOT progress and is forbidden. The next session must materialize the heavy evaluation and recompute artifacts.
- Campaign start `20261126T053929Z` is in the past. Any new `session_<UTC>` with UTC > `20261126T053929Z` immediately requires the full `fclr_live_archive04_*` set. There is no grace session and no verify-and-stop branch.
- Do NOT create a partial/empty session and leave it unrecorded. Populate it fully and record its real id in this handoff after the artifacts exist.
- Root `research_state/*.md|*.json` is at 500/500 (AT CAP). All new artifacts go under `session_<UTC>/`.
- No empty files or zero-byte placeholders. JSON must be strict RFC 8259 and carry `experiment_id:"FCLR-LIVE-ARCHIVE-04"` plus the real `session_id`.
- Stdlib only. No `pip install`; no numpy/pandas/pyarrow/requests in required artifacts.
- Do NOT modify `.github/workflows` or overwrite sealed prereg/eval artifacts.
- The ONLY timestamped campaign id permitted in this file is `FCLR-LIVE-ARCHIVE-04-20261126T053929Z`. Refer to closed campaigns by name only.

---

## 10. STATE OF THE WORK (read before acting)

- **Half 1 (funding-conditioned volatility), frozen `ironflow_bulk` panel:** exhausted NOT_SUPPORTED (BROAD/CORR/STRESS/JUMP).
- **Half 1, Binance archive mean-RV QLIKE (FCLR-LIVE-ARCHIVE-01):** CLOSED NOT_SUPPORTED.
- **Half 1, Binance archive stress/tail (FCLR-LIVE-ARCHIVE-03):** CLOSED NOT_SUPPORTED.
- **Half 1, Binance archive quantile/full-distribution (FCLR-LIVE-ARCHIVE-04):** ACTIVE rank-0, READY_EXECUTE.
- **Half 2 (liquidation risk), frozen panel:** closed.
- **FCLR-009:** CLOSED NOT_MET.
- **Forecast gate (§9):** NOT PASSED. Risk overlay ineligible.
- **Root churn:** 500/500 (at cap); nested session storage only.

---

## 11. ON-DISK INPUTS (verified — do not re-derive)

| Path | Description |
|---|---|
| `research_state/session_20261126T042519Z/` | Completed FCLR-LIVE-ARCHIVE-01 heavy set + raw archive cache (reuse read-only). |
| `research_state/session_20261126T042519Z/raw/` | 1,200 verified monthly zips (klines/mark/index/premium/funding) for the 5-symbol 2021–2024 cohort. |
| `research_state/session_20261126T051548Z/` | Completed FCLR-LIVE-ARCHIVE-03 heavy set; reusable stdlib evaluation template. |
| `research_state/experiment_frontier.json` | Rank-0 registry (FCLR-LIVE-ARCHIVE-04 READY_EXECUTE). |
| `research_state/data_cache/ironflow_bulk/` | Frozen 18-month reference panel; read-only. |
| `research_state/negative_results_report.md` | Preserved nulls and failed routes. |

Do not mutate frozen caches. Reuse the raw zips; verify checksums if re-reading.

---

## 12. KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3/§7/§8/§9/§14/§16/§17/§19/§20.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` ladder-aware binder (campaign 04 → `fclr_live_archive04_`).
- `research_state/session_20261126T051548Z/fclr_live_archive03_eval_20261126T051548Z.py` — reusable stdlib HAR + download + bootstrap template.
- `research_state/experiment_frontier.json` — rank-0 registry.

---

## 13. SESSION CLOSE-OUT — 2026-11-26T05:39:29Z

**What changed and why:** routing refresh only. FCLR-LIVE-ARCHIVE-03 is closed NOT_SUPPORTED; the terminal “no next campaign” bottleneck is removed by promoting the materially different FCLR-LIVE-ARCHIVE-04 quantile/full-distribution volatility arm to rank-0 READY_EXECUTE and binding it in the heavy-work gate.

**What was actually tested:** no new heavy artifact is claimed. The existing heavy-work gate remains green because the latest on-disk session (`session_20261126T051548Z`) predates the new campaign start (`20261126T053929Z`). The next post-start session must produce the complete `fclr_live_archive04_*` set or fail closed.

**Evidence added:** this handoff and the rank-0 frontier update.

**Current gate state:** `live_archive.required=false` only because the latest session predates the campaign; `live_archive.pass=true`. After the next session, `live_archive.required=true`, `artifact_family="live_archive04"`, and the full non-empty artifact set is mandatory.

**Single highest-value next task:** execute FCLR-LIVE-ARCHIVE-04 end-to-end in one fresh `session_<UTC>` (UTC > `20261126T053929Z`): outcome-blind prereg, heavy 3-block quantile-volatility evaluation, independent stdlib recompute, evidence audit, gate alias, and trigger check.

---

## 14. RESEARCH_PROMPT.md §19 ANSWERS (this session — 2026-11-26T05:39:29Z)

**What did the evidence support, contradict, or leave unknown?**
- Supported: funding + price features do not clear the 2% floor for mean RV QLIKE or binary stress/tail on the verified 4-year Binance archive.
- Contradicted: any claim that the new-source frontier is unexecutable or that no next repo-name campaign exists.
- Unknown: whether the same feature set improves the full predictive distribution / quantile forecast of next-24h realized variance.

**Strongest alternative explanation:** the mean and tail nulls may reflect that HAR already captures most predictable variation; a quantile/full-distribution estimand can detect shape or asymmetry improvements that mean and binary metrics miss.

**Dominant limitation:** the 5-symbol cohort is narrow; quantile estimates and bootstrap inference must be reported with leave-one-symbol-out and per-block diagnostics.

**Concrete falsification test:** a paired 3-block pinball-loss evaluation in which C2 beats B1 by <2% relative or the CI does not support the floor preserves `NOT_SUPPORTED`; a stable ≥2% improvement reopens promotion review.

**Highest information gain per free compute:** FCLR-LIVE-ARCHIVE-04, because it tests a distinct repo-name estimand on the same verified archive with the raw cache already in hand.

**Exact artifact and command demonstrating progress:** one complete `research_state/session_<UTC>/` with every `fclr_live_archive04_*` artifact in §5; `python3 scripts/check_handoff_heavywork_gate.py --json` must return `reason=OK` with `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive04"`, followed by the six-module unittest command in §6.

**Latest completed session:** session_20261126T051548Z

(End of file)