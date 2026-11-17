# FCLR Focus Campaign — `FCLR-TRIGGER-READINESS-01-20261117T203457Z` — aligned 2026-11-17T20:52:56Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY` / `BOUNDED_TRIGGER_ONLY`, `all_terminal=true`, `next_action_heavy=null`).
**Sole durable handoff:** `AGENT_HANDOFF.md` (authoritative). This file is the detailed subordinate campaign note; if it conflicts with the handoff, the handoff wins.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, re-score sealed results, fabricate data, edit `.github/workflows/*`, poll, re-probe the HuggingFace tree, use paid/credentialed/manual outcome data, or run `git lfs pull`.
**Artifact rule:** write every new artifact to a new `research_state/session_<UTC>/`. The `research_state/` root is at **500/500** md/json; adding root files breaks the enforced churn cap.

## Current target (mandatory) — `FCLR-TRIGGER-READINESS-01`

The frontier-verification line is **CLOSED**: two independent exhaustive audits (`session_20261117T193323Z` csv-count heuristic; `session_20261117T194457Z` month-interval arithmetic) reproduce the same closed-world result with `all_exact_match=true`. Do **not** run verify-08+ or any further cached-data frontier re-audit.

The program is `CLOSED_TERMINAL` and every reopen trigger is `OPEN`. The agent-removable heavy work is therefore **outcome-blind trigger-activation readiness**, not another re-audit and not a new outcome claim.

Required NEW package in the next `research_state/session_<UTC>/`:

- `trigger_activation_executor_<UTC>.{py,json}` — a stdlib-only **referee, not a runner**. Reads `resume_trigger_registry.json` + `ironflow_monitor_state.json` once; maps each of `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` to (estimand, `paired_n` floor — Gate4/TrackC `>=23224`, TrackA/HL/expansion `>=11689`, `>=3` non-overlapping 30d blocks, `7d` purge/embargo, `>=5` instruments, Holm family enumeration, MDE `<2%` target); emits a per-trigger `prereg_instantiation_plan` with `outcome_data_inspected_before_freeze=false`; exits non-zero/refuses when any pre-outcome gate is unmet; never opens an outcome file.
- `trigger_activation_selftest_<UTC>.{py,json}` — real `unittest` self-tests on **synthetic** data: 30d-train + 7d-embargo + 30d-test block arithmetic and non-overlap detection; `paired_n` floor enforcement below/above 23224 and 11689; Holm-family enumeration determinism; refusal behaviour when gates fail; explicit outcome-blindness assertion (no outcome path opened). Record pass/fail counts + EXIT.
- `trigger_activation_readiness_<UTC>.{json,md}` — readiness certificate mapping each trigger to a concrete pre-powered executable plan + expected artifacts + the irreducible human step (Gate 4 legal attestation is human-owned), plus an explicit do-not-run list. Must state `promotable=false`, `program_status=CLOSED_TERMINAL`, `new_scientific_claim=false`.
- Plus `trigger_check_<UTC>.json` and `evidence_audit_<UTC>.md` per the handoff.

Do not merely copy `trigger_readiness_power.py` / `trigger_readiness_power_calibration_*`; this is new executable code + self-tests + a per-trigger plan.

## Completed work — do not repeat

- **Frontier (CLOSED):** `session_20261117T193323Z` and `session_20261117T194457Z` — full-C2 0 blocks/no ≥127d; mark+funding-only 4 individually / 2 mutually non-overlapping; `all_exact_match=true`; `BLOCKED_ON_DESIGN`, `promotable=false`. No verify-08+.
- **FCLR-REPRO-SYNTH-05 — DONE (`session_20261117T072040Z`).** Design-frontier certificate + replication robustness; `promotable=false`.
- **FCLR-014 — DONE / BLOCKED-ON-DESIGN (`session_20261117T071110Z`).** 4-block "freeze a prereg" claim is **RETRACTED**; cite `session_20261117T071110Z`.
- **Replication synthesis — DONE (`session_20261117T071110Z`).** 7/7 qualitative corroboration; 0 promotable positives.
- FCLR-013 — `session_20261117T031656Z` (NOT_REPLICATED); FCLR-010 — `session_20261117T002014Z` (NOT_REPLICATED); FCLR-002/003 — `session_20261117T000400Z`; FCLR-009 — `session_20261116T125624Z`; FCLR-006 — `session_20261116T185811Z`; FCLR-008 — `session_20261116T230140Z`; FCLR-RCA-011 — `session_20261116T100533Z`.

Incomplete / non-counting (do not resume/copy/count): `session_20261116T104644Z/`, `session_20261116T105341Z/`, `session_20261116T134957Z/` (trigger-only); `session_20261116T140001Z/` and `session_20261116T221127Z/` superseded.

## Why this campaign exists (bottlenecks removed)

- **Frontier-audit treadmill removed:** repeated independent frontier re-audits all reproduced the same closed result; two now agree with `all_exact_match=true`. Further cached-data re-audits are prohibited and no longer satisfy the heavy-work gate.
- **Handoff staleness corrected and blocked:** the prior handoff named `session_20261117T193323Z` as latest while `session_20261117T194457Z` already existed; both are now recorded and the frontier line is closed. The gate now fails (`HANDOFF_STALE_LATEST_SESSION`) if a newer on-disk session is not recorded in `AGENT_HANDOFF.md`, so the handoff cannot go stale to dodge the package.
- **Gate regression fixed:** the frontier regex read the campaign-number group instead of the timestamp group, breaking pre-start grandfathering (`test_pre_start_session_is_grandfathered`). Fixed; a `trigger_readiness` enforcement state was added.
- **Parquet engine absent:** use ZIP/CSV twins; network installs prohibited.
- **Root churn:** 500/500 — session-only writes.
- **Handoff authority:** `AGENT_HANDOFF.md` only.

## Non-skippable execution contract

### Phase A — Check external triggers once
Read only `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Record timestamp and verdict in `trigger_check_<UTC>.json`. No network/polling/HF re-probe. Current: all four OPEN; Ironflow `data_through=2026-10`, `consecutive_absent=3`; 2026-11/12/2027-01 `CONFIRMED_ABSENT`.

### Phase B — Emit the outcome-blind trigger-activation package
No trigger fired → produce `trigger_activation_executor_<UTC>.{py,json}`, `trigger_activation_selftest_<UTC>.{py,json}`, `trigger_activation_readiness_<UTC>.{json,md}` exactly as specified above. If a trigger fired → `RESEARCH_PROMPT.md` §16 admissibility/source audit, freeze a pre-sized prereg from `session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json` per `session_20261116T100533Z/trigger_readiness_power_calibration_20261116T100533Z.md` (Gate4/TrackC `paired_n>=23224`, TrackA/expansion `paired_n>=11689`, ≥3 blocks, 7d purge/embargo, `outcome_data_inspected_before_freeze=false`), then execute and record an honest verdict.

### Phase C — Verify and hand off
1. Create `research_state/session_<UTC>/` (all new artifacts inside).
2. Audit carried-forward bundles: `session_20261116T100533Z/`, `125624Z/`, `185811Z/`, `230140Z/`, `20261117T000400Z/`, `002014Z/`, `031656Z/`, `071110Z/`, `072040Z/`, `193323Z/`, `194457Z/`.
3. Write concise `evidence_audit_<UTC>.md`.
4. Run and capture under the session dir: `check_handoff_heavywork_gate.py --json` (must show `trigger_readiness.pass=true` and `handoff_stale=false`), `check_tracka_scope_registry_drift.py --json`, targeted `python3 -m unittest tests.test_active_campaign_gate tests.test_next_campaign_status tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_143`, and `python3 -m unittest discover -q` to completion (record count/skip/error/EXIT). **Baseline is environment-dependent:** targeted 82 tests / 6 pre-existing missing-`numpy` errors / 0 failures; discovery 1126 tests / 62 errors / 9 failures / 14 skipped / EXIT 1. Record the actual run; never treat a missing-dependency error set as green. Revert timestamp-only tracked-file side effects. Record the new session id in `AGENT_HANDOFF.md` before the final gate capture, or the stale-handoff check fails closed.
5. Update only `AGENT_HANDOFF.md`; preserve sole-handoff contract and blockers.

Trigger checks, tests/gates, copied bundles, frontier re-audits, re-runs of FCLR-014 or the synthesis, "no trigger → stop cleanly", and handoff-only refreshes are **not** completion.

## Verification record — 2026-11-17T205209Z

- Handoff refreshed: `AGENT_HANDOFF.md` is the sole durable handoff; `FCLR-TRIGGER-READINESS-01-20261117T203457Z` is the active mandatory heavy campaign.
- Heavy-work gate hardened: `scripts/check_handoff_heavywork_gate.py` now fails with `HANDOFF_STALE_LATEST_SESSION:<id>` when the newest `research_state/session_<UTC>/` on disk is not the newest session id recorded in the handoff. Added `TestHandoffFreshnessGate` (2 tests) to `tests/test_tracka_hardening_143.py`.
- `check_handoff_heavywork_gate.py --json`: **PASS** (`reason_code: OK`, root 500/500, latest handoff/on-disk session `session_20261117T194457Z`, `handoff_stale=false`, `trigger_readiness.required=false` → grandfathered).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code: OK`).
- Targeted suite: **82 tests, 6 pre-existing missing-`numpy` errors, 0 failures**. Full discovery baseline: 1126/62/9/14/EXIT 1 (environmental).
- No new session artifact produced in this refresh; the next session must satisfy `FCLR-TRIGGER-READINESS-01`.