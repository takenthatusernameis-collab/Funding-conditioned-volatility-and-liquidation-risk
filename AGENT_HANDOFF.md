# AGENT HANDOFF — 2026-11-18T02:31:04Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T02:31:04Z)

**State verified clean (2026-11-18T02:31:04Z). No heavy work due. Stop cleanly unless a reopen trigger is machine-satisfied.**

- Program: `CLOSED_TERMINAL` — `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`; verdict `NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED`; 0/58 rows §17-promotable.
- Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`).
- Campaign `FCLR-LEDGER-INTEGRITY-02-20261118T004445Z` is **COMPLETE** (`research_state/session_20261118T004445Z/`): ledger audit, frontier recompute, closure-ledger backfill plan, trigger check, trigger-activation readiness refresh, evidence audit, gates/suite capture present. Corrected frontier verified closed: `n_individually_feasible=1` (`2025-01`), `max_mutually_non_overlapping=1`, `campaign_feasible_non_overlapping=False`. Tested-window fix in `scripts/next_campaign_status.py` is applied and tested — **do not re-fix**.
- Gates (verified this session): `check_handoff_heavywork_gate.py --json` **PASS** (`reason_code=OK`, `handoff_stale=false`, `failures=[]`, latest `session_20261118T004445Z`); `check_tracka_scope_registry_drift.py --json` **PASS** (196/196). `next_campaign_status.py --json` confirms closed frontier.
- Triggers (one-shot, no network/polling): all four `OPEN`, none fired — `GATE4_BRANCH_1` (human/legal), `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION` (post-2026-10 observed labels absent through 2026-10, `consecutive_absent=3`; 2026-11/12, 2027-01 `CONFIRMED_ABSENT`), `EXPANSION_ROBUSTNESS_REDO` (re-scoring sealed 19.04% forbidden). `ironflow_monitor_state.json`: `data_through=2026-10`.

**Next session first/only action (run once, then stop if unchanged):**
```bash
python3 scripts/check_handoff_heavywork_gate.py --json | jq '{pass,reason_code,handoff_stale,latest_session_id,failures}'
python3 scripts/check_tracka_scope_registry_drift.py --json | jq '{pass,reason_code}'
python3 scripts/next_campaign_status.py --json | jq '.markfund_frontier | {n_individually_feasible,max_mutually_non_overlapping,campaign_feasible_non_overlapping,individually_feasible_months}'
```
Expected: both gates PASS, `handoff_stale=false`, frontier closed as above. **If all triggers remain OPEN and no trigger artifact satisfies its machine-checkable predicate, perform no heavy work and stop cleanly.**

## If and only if a reopen trigger becomes machine-satisfied (heavy work, non-avoidable)

1. Create `research_state/session_<UTC>/` (real UTC) and record its id in this handoff **before** final gate capture. Root `research_state/` is at 500/500 — put all new artifacts in the session dir only.
2. **GATE4_BRANCH_1:** only on `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED` and `fabricated=false` (human/legal attestation only). Execute Gate 4 Branch 1 protocol per `RESEARCH_PROMPT.md` §16 with outcome-blind prereg before outcomes.
3. **NEW_OBSERVED_LIQUIDATION_SOURCE:** only on `research_state/<source>_admissibility_audit_<UTC>.{md,json}` proving `status=ADMISSIBLE`, `observed_labels=true`, unauthenticated, provenance/license/venue-consistent, ≥5 instruments and (≥3 blocks or ≥1 complete month). Do admissibility audit BEFORE prereg/outcomes.
4. **HL_LABEL_EXTENSION:** only on verified post-2026-10-31 observed ironflow labels (≥100 days) with `research_state/hl_label_extension_audit_<UTC>.{md,json}`; then run a newly preregistered design per §17.
5. **EXPANSION_ROBUSTNESS_REDO:** only a newly preregistered design (`research_state/expansion_robustness_redo_prereg_<UTC>.json`) achieving LOIO≥6/8 AND placebo>95th null — **re-scoring sealed 19.04% is forbidden**.
6. For any triggered path: produce outcome-blind prereg, leakage/overlap audit against consumed windows (`session_20261118T004445Z/ledger_audit_20261118T004445Z.*`, `scripts/next_campaign_status.py` `TESTED_WINDOWS`), execution artifacts, evaluation summary, and gate captures in-session; do not weaken §17.

## Read first (if triggered)

1. `RESEARCH_PROMPT.md` §16–§17.
2. `research_state/fclr_final_structural_closure_20261116T114626.{md,json}` and `research_state/resume_trigger_registry.json`.
3. `research_state/session_20261118T004445Z/{ledger_audit,frontier_recompute,closure_ledger_backfill,trigger_check,trigger_activation_readiness,evidence_audit}_20261118T004445Z.*`.
4. `research_state/session_20261117T215904Z/trigger_activation_readiness_20261117T215904Z.{json,md}` and `research_state/session_20261116T035833Z/prereg_template_trigger_gated_20261116T035833Z.json`.

## Bottlenecks removed / prevented

- Tested-window ledger omission fixed and regression-tested (`FCLR-003` 2024-10-02..2024-12-31 in `TESTED_WINDOWS`); frontier honestly closed. Do not regress.
- Closure-ledger backfill plan recorded (`session_20261118T004445Z/closure_ledger_backfill_20261118T004445Z.*`); sealed closure JSON not mutated.
- Ledger-integrity campaign 02 complete with evidence artifacts; no pending integrity heavy work.
- Sole durable handoff authority maintained; no competing handoff. No empty/phantom sessions required.

## Prohibitions

- Do not start or re-run any sealed cached-data confirmatory estimand (FCLR-014, replication synthesis, design-frontier certificates, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04% re-score).
- Do not poll, re-probe HuggingFace, use paid/credentialed/manual outcome data, or run network installs/data fetches (`git lfs pull`).
- Do not mutate sealed artifacts, closure JSON, `.github/workflows/*`, or add root-level `research_state/*.md|json` (root 500/500 cap).
- Do not add `statsmodels` or unpinned heavy deps to core path.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; no engine installed).
- No parquet engine installed; `.parquet`-only tasks blocked unless CSV/JSON/ZIP twin exists (use ZIP-aware readers where applicable). Unresolved Git-LFS pointers remain unresolved — do not block on them.
- Do not treat environment-dependent missing-`numpy` discovery errors as green; discovery baseline was EXIT 1 in prior capture.
- Never inspect outcome data while producing outcome-blind trigger artifacts/preregs.
- Record any new session id in this handoff before final gate capture to keep `handoff_stale=false`.

## Reopen triggers (machine-checkable — all currently OPEN)

- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`) — human/legal only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json` (LOIO≥6/8 AND placebo>95th null; no sealed re-score).

## Verification record — 2026-11-18T02:31:04Z

- `check_handoff_heavywork_gate.py --json`: PASS (`reason_code=OK`, `handoff_stale=false`, `failures=[]`, latest `session_20261118T004445Z`).
- `check_tracka_scope_registry_drift.py --json`: PASS (196/196).
- `next_campaign_status.py --json`: `markfund_frontier` closed (`n_individually_feasible=1`, `individually_feasible_months=["2025-01"]`, `max_mutually_non_overlapping=1`, `campaign_feasible_non_overlapping=false`); `disjoint_block_frontier.n_feasible=0`.
- Triggers: all OPEN, `data_through=2026-10`, `consecutive_absent=3`, 2026-11/12 & 2027-01 `CONFIRMED_ABSENT`. No machine-satisfied reopen condition. No heavy work executed.
- `AGENT_HANDOFF.md` remains sole durable handoff; no sealed artifacts/workflows/registries modified.