# AGENT HANDOFF — 2026-11-13T18:24:37Z (authoritative)

**Project:** Funding-conditioned volatility and liquidation risk (FCLR)
**Repo:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`

This is the **single durable handoff**. `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, and `NEXT_SESSION_TASK.md` are redirects only — do not execute them.

## Repo-priority context
- **Name-implied core:** funding-conditioned volatility & liquidation-risk claims on admissible observed data. Cached/pre-registered volatility/liquidation confirm/cross cells are terminal with gate PASS (LIQ-010-CONFIRM NOT_REPLICATED, EXP-ROBUST-REDO FRAGILE, FWD-VOL 2024Q4/2025/2025H2/2025Q1Q2-CROSS NOT_REPLICATED). Alt-source hunt/deep-review (2026-11-13T17:12Z) found no GO/admissible new observed-liquidation source. Frontier beyond this is the Track A admissible Hyperliquid/Ironflow observed-liquidations seam (currently wired but awaiting candidate).

## Current state (verified 2026-11-13T18:24Z)
- `python scripts/fclr_next_campaign_gate.py --json` → `ok: true` (all terminal cells present).
- `drift_preflight(...)` → `pass: true` (root md+json 396/396; probe/trigger-harden invariants satisfied).
- `admissible_seam_check(candidate_path=None)` → `pass: true`, `status: NO_CANDIDATE_PENDING`, `reason_code: ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE` (fail-closed, manifest-only, no network/parquet/outcomes).
- `python -m pytest tests/test_tracka_hardening_142.py -q` → `9 passed, 12 subtests passed`.

## Bottlenecks
- **P0 blocker (material):** no admissible candidate manifest for Hyperliquid observed liquidations (month ≥ 2026-11, events+fills roles, machine-verifiable provenance/label/coverage, no modeled/proxy conflation). Track A cannot execute until seam returns GO.
- **No infra blockers:** drift, tests, and campaign gate are green; CLIs fail-closed with JSON contracts.

## NEXT CAMPAIGN — Track A admissible unlock → guarded execution (HEAVY, mandatory)
**Objective:** convert the wired-but-blocked seam into a terminal, evidence-backed outcome (GO+executed with frozen prereg/eval artifacts, or definitive NO_GO with admissibility proof). No status-only work, no reruns of terminal cells, no threshold shopping.

### P0 — Produce/admit a candidate manifest (required before any outcomes)
1. Discover/probe an unauthenticated Hyperliquid-only observed-liquidations candidate for **month ≥ 2026-11** with events+fills roles and verifiable provenance/license/label/coverage evidence (≥1 complete month or ≥3 non-overlapping 30-day blocks as required by design; venue-consistent, no conflation).
2. Materialize candidate manifest JSON and assess offline:
   - `python -c "from scripts.tracka_resume_check import admissible_seam_check; from pathlib import Path; import json; print(json.dumps(admissible_seam_check(candidate_path='<manifest.json>', repo_root=Path('.')), indent=2))"`
3. Must reach `status: GO` and `pass: true` with validated month/block/symbol evidence. If not, record fail-closed reasons, fix evidence, or emit a timestamped NO_GO admissibility note — do not force GO.

### P1 — Gate to execution-ready (GO manifest only)
1. `python scripts/tracka_resume_gate.py --admissible-manifest <manifest.json> --json`
2. If not GO (missing frozen prereg/data per harness contract): freeze the required prereg **before outcomes** and assemble admissible data path; re-run until `GO` or terminal blocked JSON refusal.
3. `python scripts/tracka_operator_report.py --admissible-manifest <manifest.json> --json` for audit trail.

### P2 — Execute and terminally evaluate (only when gate GO)
1. Run guarded Track A execution (`scripts/fclr010_guarded_entry.py` / wired harness entrypoint) with frozen prereg; capture manifests/logs.
2. Produce terminal evaluation summary + checks in `research_state/` and update frontier/registry artifacts as required by contract.
3. On any block: emit machine-readable refusal reason (no traceback-as-contract) and stop — do not fabricate outcomes.

### P3 — Hygiene
- Keep drift preflight green. If durable artifacts change root tracked counts/allowlists, update bounds/allowlists from `git ls-files` evidence with rationale.
- Re-run: `python -m pytest tests/test_tracka_hardening_142.py -q` and `python scripts/fclr_next_campaign_gate.py --json`.

## Invariants (never violate)
1. Fail-closed JSON refusals (`outcomes_inspected/network/writes_real_research_state/reads_parquet/reads_outcomes` false on blocked paths as applicable); no traceback-as-contract.
2. Preregistration before outcomes; admissible seam is manifest-only (no parquet/outcome reads, no network).
3. Drift preflight before manifest/prereg decision logic in operator CLI.
4. No re-probe polling unless trigger/candidate plausibly exists; no status-only churn; no conflation of observed vs modeled labels.
