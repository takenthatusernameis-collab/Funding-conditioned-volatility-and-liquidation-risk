# Gate 4 v4 EXPLORATORY Diagnostic Bundle Index (NOT CONFIRMATORY / NOT PROMOTABLE)

**Generated:** 2026-11-09T06:18:43Z
**Session:** 2026-11-09T06:05:59Z (handoff §0 campaign)
**Repo SHA (baseline referenced):** `14f08775e` (verify with `git --no-pager log -1 --oneline`)
**Protocol:** Gate 4 v4 `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, exploratory smoke on local 2024-04..09 cache only (FCLR-015 SHA256 `3e6ac26c...5406c`, 2024-04-01T00:00Z..2024-09-30T23:00Z, 5 symbols). **Sealed-anchor conflict — never reuse FCLR002/003/013 domain. Never replace prereg A–E contrasts or change confirmatory estimands.**

## Verdict (binding)
**EXPLORATORY NO-GO CONFIRMED** for local 2024-04..09 funding ablations (stabilization variants V1–V4): funding does not provide reliable incremental ΔQLIKE vs RV-only; leakage controls audited PASS as an exploratory diagnostic. **No confirmatory GO, no economic value, no promotion, no holdout reuse, no threshold shopping.**

## Artifact cross-reference
| Stage | JSON | Markdown | Notes |
|---|---|---|---|
| v4 exploratory exec | `research_state/gate4_v4_exploratory_exec/gate4_v4_exploratory_exec_20261109T004003Z.json` | `research_state/gate4_v4_exploratory_exec/gate4_v4_exploratory_exec_20261109T004003Z.md` | Inconclusive E vs A; split-3 B/D blowup (prior) |
| v4 exploratory diag | `research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json` | `research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.md` | Root-cause diagnostics (prior) |
| v4 exploratory stab | `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json` | `research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.md`, `results/fclr_heavy001/gate4_v4_exploratory_stab_20261109T045805Z.md` | **NO-GO signal**: V3 E vs A +1096 CI [331,2104] worse; B amplified 45→1029; V4 worse; no LOO improvement |
| v4 exploratory NO-GO formalization | `research_state/gate4_v4_exploratory_nogo/gate4_v4_exploratory_nogo_20261109T053308Z.json` | `research_state/gate4_v4_exploratory_nogo/gate4_v4_exploratory_nogo_20261109T053308Z.md`, `results/fclr_heavy001/gate4_v4_exploratory_nogo_20261109T053308Z.md` | Formal EXPLORATORY NO-GO note (prior) |
| v4 leakage audit (diagnostic) | `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T055837Z.json` | `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T055837Z.md`, `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T055837Z.md` | **leakage_invariance_all:true; bootstrap_reproducible:true** (EXPLORATORY) |

## Reproduction / verification commands
```bash
# Leakage audit (EXPLORATORY, local cache required)
python scripts/run_gate4_v4_leakage_audit.py --out-suffix <TS>

# Targeted tests (synthetic, no network, no real research_state writes)
python -m unittest tests.test_eval_inference_diagnostics tests.test_gate4_v4_leakage_audit tests.test_funding_ablations_multisplit tests.test_gate4_v4_exploratory_diag tests.test_gate4_v4_exploratory_stab -v

# Full suite
python -m unittest discover tests

# Invariants
python scripts/check_tracka_scope_registry_drift.py   # expect PASS scripts==registry
python scripts/tracka_resume_check.py                 # expect pass:true, 17/17, probes==2, root_md_json_bounded pass (<=172)
python scripts/tracka_resume_gate.py --json           # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
```

## Code hardening added (this session, 2026-11-09T06:18:43Z)
- `src/eval/inference.py`: hardened `block_bootstrap_delta_ci_diagnostic` + `diagnose_block_bootstrap_inputs` — rejects non-finite diffs from CI accounting, reports `effective_block_count`/`n_blocks_nonempty_finite`, flags degenerate/too-few-block/no-finite-block regimes; additive fields, legacy shape preserved.
- `src/eval/__init__.py`: package init.
- `scripts/run_funding_ablations.py`: `block_bootstrap_delta_ci` delegates to hardened diagnostics (backward-compatible).
- `tests/test_eval_inference_diagnostics.py`: 5 synthetic unit tests (non-finite accounting, too-few-blocks, no-finite-blocks, effective block count/legacy fields, determinism).

## Non-actions / constraints
- No confirmatory promotion; no sealed-anchor reuse; no Track A probing (2026-11..2027-02 absent, probes==2); no new Track C/B sealed outcomes; no workflows/schedulers; no root `research_state/*.md/*.json` pressure (bound 172).
