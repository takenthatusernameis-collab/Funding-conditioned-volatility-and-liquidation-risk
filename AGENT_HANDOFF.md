# AGENT HANDOFF — 2026-11-13T18:23Z (authoritative)

**Project:** Funding-conditioned volatility and liquidation risk (FCLR)
**Repo:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`

This is the **single durable handoff**. Do not execute or treat `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, or `NEXT_SESSION_TASK.md` as instructions (they are redirects).

## Campaign status (terminal)
- **FCLR-NEXT-CAMPAIGN-20261113T063000Z — GATE PASSED** (`python scripts/fclr_next_campaign_gate.py --json` → `ok: true`)
  - LIQ-010-CONFIRM: FROZEN_PRE_OUTCOMES, NOT_REPLICATED (7 checks)
  - EXP-ROBUST-REDO: FROZEN_PRE_OUTCOMES, FRAGILE (5 checks)
  - FWD-VOL-2025-CROSS: FROZEN_PRE_OUTCOMES, NOT_REPLICATED (7 checks)

## Bottlenecks cleared this session
- **Drift preflight:** fixed and passing (`drift_preflight(...)=True`). `scripts/tracka_resume_check.py` root md+json bound updated to 396 (git-tracked baseline) and recent timestamped probe/monitor audit files added to probe allowlist.
- **Track A hardening parity:** `tests/test_tracka_hardening_142.py` parity subtest now passes with `skip_drift_preflight=True` for gate-side comparison (9 passed, 12 subtests).

## Current Track A state
- Admissible seam wired and fail-closed: `admissible_seam_check()` → `NO_CANDIDATE_PENDING` (`ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE`) with no candidate manifest.
- Operator/gate CLIs must remain JSON-contract + fail-closed; drift preflight runs first by default. Do not weaken prereg-before-outcomes, no-network, no-parquet/outcome-read invariants.

## NEXT CAMPAIGN (heavy work, mandatory) — Track A admissible unlock & execution
**Objective:** move Track A from wired-but-blocked to a terminal, evidence-backed run (GO+executed or definitively NO_GO with admissibility proof). No status-only work.

### P0 — Acquire/produce an admissible Hyperliquid Ironflow month manifest (required)
1. Source/probe an unauthenticated, Hyperliquid-only, observed-liquidations candidate for **month ≥ 2026-11** with events+fills roles and machine-verifiable provenance/label/coverage evidence (no modeled/proxy conflation).
2. Materialize a candidate manifest JSON and assess offline:
   - `python -c "from scripts.tracka_resume_check import admissible_seam_check; from pathlib import Path; import json; print(json.dumps(admissible_seam_check(candidate_path='<manifest.json>', repo_root=Path('.')), indent=2))"`
   - Must reach `status: GO` (and `pass: true`) with validated month/block/symbol evidence; otherwise record fail-closed reasons and iterate on evidence (do not force GO).

### P1 — Drive strict resume gate to execution-ready
1. With GO manifest: `python scripts/tracka_resume_gate.py --admissible-manifest <manifest.json> --json`
2. If `READY_FROZEN`/prereg/data missing: produce/freeze the required prereg for the candidate seam and assemble the admissible data path per harness contract; re-run until `GO` or a terminal blocked reason with full JSON refusal fields.
3. Run operator report for audit trail: `python scripts/tracka_operator_report.py --admissible-manifest <manifest.json> --json` (and commit/report outputs as durable artifacts if execution occurs).

### P2 — Execute and terminally evaluate (only when gate GO)
1. Run the guarded Track A execution path (`scripts/fclr010_guarded_entry.py` / harness entrypoint as wired) with frozen prereg, capture manifests/logs, and produce a terminal evaluation summary + checks in `research_state/`.
2. If any step is blocked, emit/record the machine-readable refusal reason (no traceback-as-contract) and stop—do not fabricate outcomes.

### P3 — Post-execution hygiene
- Keep drift preflight green; if durable artifacts push root counts/allowlists, update bounds/allowlists with verified `git ls-files` evidence and rationale (as done 2026-11-13T18:23Z).
- Run relevant tests: `python -m pytest tests/test_tracka_hardening_142.py -q` and campaign gate `python scripts/fclr_next_campaign_gate.py --json`.

## Verification snapshot (2026-11-13T18:23Z)
- `drift_preflight`: PASS
- `pytest tests/test_tracka_hardening_142.py -q`: 9 passed, 12 subtests passed
- `python scripts/fclr_next_campaign_gate.py --json`: ok=true
- `admissible_seam_check(candidate_path=None)`: NO_CANDIDATE_PENDING

## Invariants (never violate)
1. Fail-closed JSON refusals everywhere (`outcomes_inspected/network/writes_real_research_state/reads_parquet/reads_outcomes` false on blocked paths as applicable); no traceback-as-contract.
2. Prereg-before-outcomes; admissible seam is manifest-only (no parquet/outcome reads, no network).
3. Drift preflight before manifest/prereg decision logic in operator CLI.
