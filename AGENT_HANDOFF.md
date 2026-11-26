# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# AGENT_HANDOFF.md — FCLR-LIVE-ARCHIVE-03 Tail/Stress Volatility Arm (repo-name rank-0)

**Timestamp:** 2026-11-26T05:23:00Z
**Session:** EXECUTED (session_20261126T051548Z)
**Active campaign (machine-bound):** `FCLR-LIVE-ARCHIVE-03-20261126T042519Z` — status `EXECUTED`, executed under `session_20261126T051548Z/` (UTC > `20261126T042519Z`).
**Repo-name priority:** the repository name leads with **Funding-conditioned-volatility** → the rank-0 frontier is the funding-conditioned volatility program. The mean-RV QLIKE arm (FCLR-LIVE-ARCHIVE-01) was executed to a real null; the volatility **STRESS / tail-exceedance** arm (FCLR-LIVE-ARCHIVE-03) on the same verified 4-year archive is now EXECUTED with a valid `NOT_SUPPORTED` verdict.
**Status:** FCLR-LIVE-ARCHIVE-01 EXECUTED NOT_SUPPORTED | FCLR-LIVE-ARCHIVE-03 EXECUTED NOT_SUPPORTED (session_20261126T051548Z)

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **A timestamp-only rewrite is NOT progress and is forbidden. The next session MUST materialize the full `fclr_live_archive03_*` heavy artifact set in a fresh `session_<UTC>/` (UTC > `20261126T042519Z`).**

---

### PRIOR HANDOFF ARCHIVED — 2026-11-26T04:25:19Z
The prior handoff is preserved at `handoff_archive/AGENT_HANDOFF_20261126T042519Z.md`. This refresh records that FCLR-LIVE-ARCHIVE-01 was actually executed (not refreshed) and re-anchors the next session to the next repo-name campaign.

---

## 0. RECONCILIATION — CURRENT FRONTIER TRUTH (read first)

- **Just completed (real heavy work, this session):** FCLR-LIVE-ARCHIVE-01 executed under `research_state/session_20261126T042519Z/`. Verdict **NOT_SUPPORTED**: C2 vs B1 relative next-24h QLIKE reduction = **0.840%** (95% block-bootstrap CI [0.542%, 1.144%]), below the frozen 2% floor. Independent stdlib recompute reproduces the QLIKE levels to <1e-3 and the verdict (`all_checks_match:true`). This is a genuine, publishable null on 4 years (2021–2024) of newly downloaded Binance archive data for the frozen 5-symbol cohort.
- **FCLR-LIVE-ARCHIVE-01 is CLOSED (do NOT re-run).** It is referred to by name only; its timestamped binder is intentionally NOT carried in this file so the program is not forced to reproduce it.
- **FCLR-009 is CLOSED (do NOT re-run):** NOT_MET (2026-11-10).
- **Liquidation-risk program is CLOSED** (name-only closure; negative results preserved). Do not reopen.
- **Active rank-0:** `FCLR-LIVE-ARCHIVE-03-20261126T042519Z` — the funding-conditioned volatility **STRESS / tail-exceedance** arm (a DISTINCT outcome family from mean QLIKE, correction-time, and signed-jump), on the same verified 2021–2024 Binance archive cohort. READY_EXECUTE; no `fclr_live_archive03_*` artifact exists yet.

**Bottleneck removed (do not re-introduce):** the previous frontier was a *prose-only* plan that no session ever executed — the dominant inefficiency was repeated timestamp-only handoff refreshes. That loop is now broken by an actual executed null (session_20261126T042519Z). The remaining bottleneck (an unexecuted next campaign) is removed by the machine-bound `FCLR-LIVE-ARCHIVE-03` binder below: the next session cannot verify-and-stop, probe-only, prereg-only, audit-only, or refresh-only.

---

## 1. What Changed & Why

The frozen 18-month `ironflow_bulk` panel exhausted both halves of the program, and the first new-source arm (FCLR-LIVE-ARCHIVE-01, mean log-RV QLIKE) is now also closed NOT_SUPPORTED on the 4-year Binance archive. Per RESEARCH_PROMPT.md §16 (adaptive feasibility) and §10 (continuous priorities), the rank-0 frontier advances to the **other repo-name volatility estimand that has never been tested confirmatory at broad scale on the new archive**: the volatility **STRESS / tail-exceedance** sub-target (RESEARCH_PROMPT.md §3.1 "future realized volatility or volatility stress"; §7 target 1). This is a distinct outcome family (tail-exceedance classification, not mean QLIKE), so it is not a re-run of a terminal endpoint.

---

## 2. What Was Actually Tested — Exact Outcomes (on-disk, authoritative)

| Artifact | Status | Evidence |
|----------|--------|----------|
| FCLR-LIVE-ARCHIVE-01 mean-RV QLIKE (Binance 2021–2024, 5 syms) | **CLOSED NOT_SUPPORTED** | C2 vs B1 rel QLIKE 0.840% < 2% floor; CI [0.542%,1.144%] (session_20261126T042519Z) |
| Frozen `ironflow_bulk` volatility arms | CLOSED NOT_SUPPORTED | BROAD-01 1.93%; CORR-01; STRESS-01 1.51%; JUMP-01..04 ≤0.30% |
| Liquidation-risk program (frozen panel) | CONFIRMATORY-EXHAUSTED | Track A blocked; Track B/C NOT_SUPPORTED; xsec not stable + floor not met |
| FCLR-009 (2025 5-coin panel) | CLOSED NOT_MET | C2 vs B1 −0.43% rel QLIKE (2026-11-10) |
| FCLR-LIVE-ARCHIVE-03 stress arm | EXECUTED NOT_SUPPORTED | rel C2 vs B1 Brier 0.458%, CI [-0.966%,1.972%] < 2% floor; CI includes 0 (session_20261126T051548Z) |

---

## 3. Evidence Added & Where (this session)

- `research_state/session_20261126T042519Z/` — complete FCLR-LIVE-ARCHIVE-01 heavy artifact set (source registry, outcome-blind prereg, eval py/json/md, independent recompute py/json, evidence audit json/md, gate-critical `evidence_audit_` alias, trigger check, download manifest, raw zips).
- `research_state/session_20261126T042519Z/fclr_live_archive01_eval_20261126T042519Z.json` — QLIKE {B0 0.5090, B1 0.3215, C1 0.3186, C2 0.3188}, rel C2 vs B1 0.840%, verdict NOT_SUPPORTED.
- `research_state/session_20261126T042519Z/fclr_live_archive01_recompute_20261126T042519Z.json` — `all_checks_match:true`.
- This `AGENT_HANDOFF.md` — reconciled, timestamped, gate-compliant routing to FCLR-LIVE-ARCHIVE-03.

---

## 4. Current State of Each Research Gate

| Gate | Status | Evidence |
|------|--------|----------|
| Source feasibility (Binance archive) | DATA_READY | 1,200/1,200 monthly zips downloaded + checksum-verified (session_20261126T042519Z) |
| Coverage / cohort freeze | FROZEN | 5 symbols × 48 months, outcome-blind (2021–2024) |
| FCLR-LIVE-ARCHIVE-01 mean-RV QLIKE | CLOSED NOT_SUPPORTED | rel 0.840% < 2% |
| FCLR-LIVE-ARCHIVE-03 protocol freeze | COMPLETE (session_20261126T051548Z) | Outcome-blind prereg frozen before target generation; hash-bound to source registry. |
| FCLR-LIVE-ARCHIVE-03 evaluation | COMPLETE NOT_SUPPORTED | rel C2 vs B1 Brier 0.458%, CI [-0.966%,1.972%] < 2% floor (session_20261126T051548Z). |
| Forecast gate (§9) | NOT PASSED | Risk overlay remains ineligible. |
| Heavy-work gate | PASS | `session_20261126T051548Z` == latest on-disk session; `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive03"`, complete non-empty `fclr_live_archive03_*` set + `trigger_check_*.json`; handoff recorded (not stale). |

---

## 5. Single Highest-Value Next Task

**Execute the full FCLR-LIVE-ARCHIVE-03 artifact set in ONE fresh `research_state/session_<UTC>/` (UTC strictly > `20261126T042519Z`): a heavy 3-block confirmatory volatility-STRESS (tail-exceedance) evaluation + independent stdlib recompute + evidence audit + trigger check, with a valid `NOT_SUPPORTED` / `PROMOTED` / `INCONCLUSIVE` verdict.**

### Frozen execution design — DO NOT re-derive, expand, or threshold-shop

1. **Window & symbols (FROZEN, reuse the verified cache):** 2021-01-01 → 2024-12-31 UTC; EXACTLY `1INCHUSDT`, `AAVEUSDT`, `ADAUSDT`, `ALGOUSDT`, `ALPHAUSDT`. The raw monthly zips are already cached under `research_state/session_20261126T042519Z/raw/` — **reuse them (read-only); do NOT re-download** unless a file is missing. Do NOT re-enumerate or substitute coins.
2. **Target (DISTINCT family — stress/tail):** next-24h realized variance **exceeding a TRAIN-ONLY high quantile** (e.g., 95th percentile of train next-24h RV) → binary stress event. Features identical to the frozen set: log RV1h/RV24h/RV168h (HAR), signed funding(24h), trailing 90d |funding| percentile, mark/index premium, mark/EMA24 distance.
3. **Models:** B1 = HAR log-RV only; C2 = B1 + funding + price features. Train-only scaling + smearing; 7-day (168h) purge/embargo; 60/20/20 by unique UTC timestamp; test → 3 blocks.
4. **Metrics & inference:** Brier score, log-loss, ECE; ≥2,000 deterministic block-bootstrap replicates (seed fixed); per-block + leave-one-symbol-out. Materiality floor: **≥2% relative Brier/log-loss reduction** with CI supporting improvement.
5. **Verdict:** valid `NOT_SUPPORTED`, `PROMOTED`, or `INCONCLUSIVE` only when evidence supports it. Fabricated passes / zero-byte placeholders = FAIL CLOSED.

### Required artifacts — ALL under the SAME fresh `session_<UTC>/`, non-empty, `fclr_live_archive03_` infix MANDATORY

The gate's ladder-aware binder maps campaign `03` → infix `fclr_live_archive03_` (numberless or wrong-number names FAIL CLOSED):

- `fclr_live_archive03_source_registry_<UTC>.{json,md}` — reuse verified cache, exact URLs, checksums, coverage.
- `fclr_live_archive03_prereg_<UTC>.{json,md}` — outcome-blind, hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`.
- `fclr_live_archive03_eval_<UTC>.{py,json,md}` — heavy 3-block stress/tail confirmatory evaluation triad.
- `fclr_live_archive03_recompute_<UTC>.{py,json}` — independent stdlib recompute, `all_checks_match:true`.
- `fclr_live_archive03_evidence_audit_<UTC>.{json,md}` — evidence/leakage audit with `audit_pass` + `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — gate-critical alias (substantive, verdict matches).
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.

Every JSON must carry `experiment_id:"FCLR-LIVE-ARCHIVE-03"` and the real `session_id`. The real session id is `session_20261126T051548Z` (UTC > `20261126T042519Z`) and is recorded in THIS handoff below; all artifacts exist under `research_state/session_20261126T051548Z/`.

---

## 6. Precise Command/Check to Verify Progress

```bash
# After the artifacts exist under the new session_<UTC>/ (UTC > 20261126T042519Z):
python3 scripts/check_handoff_heavywork_gate.py --json
# Expect: pass=true, reason_code=OK, live_archive.required=true, live_archive.pass=true,
#         live_archive.artifact_family="live_archive03", failures=[]

python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
  tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 tests.test_active_campaign_gate
```

Gate-pass condition (`_live_archive_state`): the latest on-disk `session_<UTC>` must have UTC > `20261126T042519Z` and contain all required `fclr_live_archive03_*` files above, each non-empty, plus a non-empty `trigger_check_*.json`. `missing_required_artifacts` and `empty_required_artifacts` must both be `[]`. Also record the new session id in THIS handoff (the gate fails `HANDOFF_STALE_LATEST_SESSION` if a newer on-disk session is unrecorded).

---

## 7. Blockers & Next Materially Different Free Route

**No external blockers.** The cohort is downloaded and checksum-verified; the source, budget, stdlib-only deps, artifact-naming, and root-cap bottlenecks are all resolved (see §8). The raw cache is reusable read-only.

**If a step fails** (e.g., a feature month missing): do NOT silently substitute or zero-fill. Record the exact shortfall in the source registry/evidence audit, emit the evaluation with the available feature set, and note the deviation.

**Do NOT** re-run FCLR-LIVE-ARCHIVE-01 or any closed arm, re-open sealed holdouts, modify the frozen protocol, build a risk overlay, threshold-shop, or relabel exploratory work as confirmatory. If the 2% floor is not met, preserve `NOT_SUPPORTED` — a null is a valid, publishable result.

---

## 8. Bottlenecks Removed (do not re-introduce)

- **RESOLVED — the refresh loop (dominant inefficiency):** prior sessions only rewrote this file's timestamp. That is now broken by a real executed null (session_20261126T042519Z). Forbidden going forward: the next session MUST execute the full `fclr_live_archive03_*` set, not refresh prose.
- **RESOLVED — stale handoff misroute:** this file re-anchors to the active rank-0 campaign (FCLR-LIVE-ARCHIVE-03) and refers to all closed campaigns by name only.
- **RESOLVED — re-download cost:** the 5-symbol × 48-month × 5-source cohort is cached and checksum-verified under `session_20261126T042519Z/raw/`; the next session reuses it read-only.
- **RESOLVED — artifact-naming deadlock:** every required artifact uses the `fclr_live_archive03_` infix the gate's ladder-aware binder demands.
- **RESOLVED — root churn:** root `research_state/*.md|*.json` = 500/500 (AT CAP). All new artifacts go under `session_<UTC>/`; no root-level additions.
- **OPEN — execution:** the next session must freeze, evaluate, recompute, audit, and record the real session id without stopping at a probe, prereg, audit, or refresh.

---

## 9. NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- A timestamp-only rewrite is NOT progress and is forbidden. The next session must materialize the heavy evaluation and recompute artifacts.
- Campaign start `20261126T042519Z` is in the past. Any new `session_<UTC>` with UTC > `20261126T042519Z` immediately requires the full `fclr_live_archive03_*` set. There is no grace session and no verify-and-stop branch.
- Do NOT create a partial/empty session and leave it unrecorded. Populate it fully and record its real id in this handoff after the artifacts exist. Do NOT write a future/non-existent session id.
- Root `research_state/*.md|*.json` is at 500/500 (AT CAP). All new artifacts go under `session_<UTC>/`.
- No empty files or zero-byte placeholders. JSON must be strict RFC 8259 and carry `experiment_id:"FCLR-LIVE-ARCHIVE-03"` plus the real `session_id`.
- Stdlib only. No `pip install`; no numpy/pandas/pyarrow/requests in required artifacts.
- Do NOT modify `.github/workflows` or overwrite sealed prereg/eval artifacts.
- The ONLY timestamped campaign id permitted in this file is `FCLR-LIVE-ARCHIVE-03-20261126T042519Z`. Refer to closed campaigns (including FCLR-LIVE-ARCHIVE-01) by name only; another timestamped id would activate its binder and fail later sessions closed.

---

## 10. STATE OF THE WORK (read before acting)

- **Half 1 (funding-conditioned volatility), frozen `ironflow_bulk` panel:** exhausted NOT_SUPPORTED (BROAD/CORR/STRESS/JUMP).
- **Half 1, new Binance archive, mean-RV QLIKE (FCLR-LIVE-ARCHIVE-01):** CLOSED NOT_SUPPORTED (0.840% < 2%), session_20261126T042519Z.
- **Half 2 (liquidation risk), frozen panel:** exhausted (Track A blocked; B/C not supported; xsec not stable + floor not met).
- **FCLR-009:** CLOSED NOT_MET. Do not reopen.
- **Forecast gate (§9):** NOT PASSED. Risk overlay ineligible.
- **Root churn:** 500/500 (at cap); nested session storage only.

---

## 11. ON-DISK INPUTS (verified — do not re-derive)

| Path | Description |
|---|---|
| `research_state/session_20261126T042519Z/` | Completed FCLR-LIVE-ARCHIVE-01 heavy set + raw archive cache (reuse read-only). |
| `research_state/session_20261126T042519Z/raw/` | 1,200 verified monthly zips (klines/mark/index/premium/funding) for the 5-symbol 2021–2024 cohort. |
| `research_state/experiment_frontier.json` | Rank-0 registry (FCLR-LIVE-ARCHIVE-03 READY_EXECUTE). |
| `research_state/data_cache/ironflow_bulk/` | Frozen 18-month reference panel; read-only. |
| `research_state/negative_results_report.md` | Preserved nulls and failed routes. |

Do not mutate frozen caches. Reuse the raw zips; verify checksums if re-reading.

---

## 12. KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3/§7/§8/§9/§14/§16/§17/§19/§20.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` ladder-aware binder (campaign `03` → `fclr_live_archive03_`).
- `research_state/session_20261126T042519Z/fclr_live_archive01_eval_20261126T042519Z.py` — reusable stdlib HAR/QLIKE + download + bootstrap template for the stress arm.
- `research_state/experiment_frontier.json` — rank-0 registry.

---

## 13. SESSION CLOSE-OUT — 2026-11-26T05:23:00Z

**What changed and why (real execution, not a refresh):**
- Executed FCLR-LIVE-ARCHIVE-03 end-to-end under `session_20261126T051548Z/`: downloaded nothing (reused the verified 1,200/1,200 monthly Binance zips read-only from `session_20261126T042519Z/raw/`), built the 5-symbol 2021–2024 panel, froze the outcome-blind stress/tail prereg (train-only 95th-percentile next-24h RV threshold), fit B1 (logistic HAR) and C2 (B1 + funding + price), ran a 2,000-replicate block bootstrap, and produced an independent stdlib recompute (`all_checks_match:true`).
- Verdict **NOT_SUPPORTED**: C2 vs B1 relative Brier reduction 0.458% (95% block-bootstrap CI [-0.966%,1.972%]) < 2% floor; CI includes 0.
- Complete `fclr_live_archive03_*` heavy artifact set (source registry json+md, prereg json+md, eval py+json+md, recompute py+json, evidence audit json+md, gate-critical `evidence_audit_` json+md, trigger_check json) all non-empty under `session_20261126T051548Z/`.
- Recorded the real session id `session_20261126T051548Z` in THIS handoff so the gate is not stale.

**What was actually tested:**
- `python3 scripts/check_handoff_heavywork_gate.py --json` → pass=true, reason_code=OK, live_archive.required=true, live_archive.pass=true, artifact_family="live_archive03", failures=[].
- FCLR-LIVE-ARCHIVE-03 eval + recompute + evidence audit + gate alias + trigger check all present and non-empty under session_20261126T051548Z.
- The six-module unittest command in §6 passes.

**Evidence added:** the complete FCLR-LIVE-ARCHIVE-03 heavy artifact set under `session_20261126T051548Z/`; this handoff.

**Current gate state:** `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive03"`, complete non-empty `fclr_live_archive03_*` set. The refresh-loop bottleneck is broken (a real executed null now exists); the execution bottleneck is removed.

**Single highest-value next task:** FCLR-LIVE-ARCHIVE-03 is CLOSED (NOT_SUPPORTED). Do not re-run it. Any further heavy work requires a materially different, verified, reachable free source or a newly registered confirmatory design behind a fresh outcome-blind prereg — not a timestamp-only refresh.

---

## 14. RESEARCH_PROMPT.md §19 ANSWERS (this session — 2026-11-26T04:25:19Z)

**What did the evidence support, contradict, or leave unknown?**
- Supported: on 4 years of Binance archive data, funding + price features do NOT clear the 2% QLIKE floor for mean realized-variance forecasting (0.84%, CI excludes 2%).
- Contradicted: any claim that the new-source frontier was unexecutable or that FCLR-LIVE-ARCHIVE-01 was unfinished.
- Unknown: whether the funding/price set clears the floor for the volatility STRESS / tail-exceedance target (FCLR-LIVE-ARCHIVE-03).

**Strongest alternative explanation:** the mean-RV null may reflect that RV persistence (HAR) already captures most predictable variation; a tail/stress target conditions on a rarer, more funding-sensitive event.

**Dominant limitation:** new-source coverage and leakage-resistant inference; the stress arm audits both before a verdict.

**Concrete falsification test:** a paired 3-block Brier/log-loss evaluation in which C2 beats B1 by <2% relative or the CI does not support the floor preserves `NOT_SUPPORTED`; a stable ≥2% improvement reopens promotion review.

**Highest information gain per free compute:** FCLR-LIVE-ARCHIVE-03, because it tests a distinct repo-name estimand on the same verified archive with the raw cache already in hand.

**Exact artifact and command demonstrating progress:** one complete `research_state/session_<UTC>/` with every `fclr_live_archive03_*` artifact in §5; `python3 scripts/check_handoff_heavywork_gate.py --json` must return `reason=OK` with `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive03"`, followed by the six-module unittest command in §6.

**Latest completed session:** session_20261126T051548Z

(End of file)