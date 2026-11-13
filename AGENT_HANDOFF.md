# AGENT HANDOFF — 2026-11-13T19:19:03Z (authoritative, single durable handoff)

**Initial task for next agentic session (read this first):** execute the Phase 0→4 campaign below to produce a **terminal, evidence-backed** Track A outcome (GO candidate → prereg → guarded execution → sealed evaluation, or timestamped NO_GO admissibility evidence). Do not stop at planning or status reruns.

**Project:** Funding-conditioned volatility and liquidation risk (FCLR)
**Repo root:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`
**This file is the single durable handoff.** `FOCUS_CAMPAIGN.md`, `HANDOFF_NEXT_SESSION.md`, `NEXT_SESSION_TASK.md` are redirects only — do not execute them.

## 1) Repo-priority context (name-driven)
Core claim: extreme funding/volatility/price-dislocation features improve **out-of-sample** forecasts of future volatility or liquidation stress/risk, vs volatility-only baselines, on admissible data with frozen prereg + leakage-safe evaluation.
Cached/pre-registered volatility & liquidation confirm/cross cells are **terminal with gate PASS** (LIQ-010-CONFIRM NOT_REPLICATED; EXP-ROBUST-REDO FRAGILE; FWD-VOL 2024Q4/2025/2025H2/2025Q1Q2-CROSS NOT_REPLICATED). `research_state/alt_source_deep_review_latest.md` (2026-11-13T17:12:25Z) records **0 GO/admissible new observed-liquidation sources** from that bounded hunt.
**Highest-value unfinished frontier:** unlock Track A on an admissible **Hyperliquid observed-liquidations** candidate via the wired seam (month ≥ 2026-11, events+fills, machine-verifiable provenance/label/coverage, no modeled/proxy conflation). No other cached claim-worthy design remains open.

## 2) Current verified state (2026-11-13T19:19:03Z)
- `python scripts/fclr_next_campaign_gate.py --json` → `ok: true` (all listed terminal cells present/consistent).
- `admissible_seam_check(candidate_path=None)` (`scripts.tracka_resume_check`) → `pass: true`, `status: NO_CANDIDATE_PENDING`, `reason_code: ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE` (fail-closed, offline, manifest-only, `network=false`, `reads_parquet=false`, `reads_outcomes=false`, `writes_real_research_state=false`).
- No `*2026-11*hyperliquid*` candidate manifest / no `tracka_admissibility_no_go_*` artifact found in `research_state/`.
- Harness CLIs present: `scripts/fclr_next_campaign_gate.py`, `scripts/tracka_resume_check.py`, `scripts/tracka_resume_gate.py`, `scripts/tracka_operator_report.py`, `scripts/fclr010_guarded_entry.py`.

## 3) Bottlenecks (remove to make progress)
- **P0 MATERIAL BLOCKER (active, 2026-11-13T19:19:03Z):** no admissible candidate manifest for Hyperliquid observed liquidations (month ≥ 2026-11, events+fills roles, verifiable provenance/license/label/coverage; ≥1 complete month or ≥3 non-overlapping 30-day blocks; ≥5 instruments as required; venue-consistent, no modeled/proxy/DeFi conflation). Track A execution is correctly fail-closed until seam returns GO.
- **No infra blockers identified:** gate/seam checks pass; operator/gate/report path is wired. Do **not** spend sessions on status-only reruns, re-probing terminal cells, or polling without new evidence.
- **Hygiene blocker:** multiple stale `FOCUS_CAMPAIGN`/`HANDOFF_NEXT_SESSION`/`NEXT_SESSION_TASK` artifacts exist under `research_state/` (e.g. `research_state/FOCUS_CAMPAIGN.md`, `research_state/NEXT_SESSION_TASK.md`) — **ignore them**; only this root `AGENT_HANDOFF.md` is authoritative.

## 4) NEXT CAMPAIGN — mandatory heavy work (do not stop at planning)
**Objective:** produce a terminal, evidence-backed Track A outcome: either (A) admitted GO candidate → frozen prereg → guarded execution → sealed evaluation artifacts, or (B) timestamped NO_GO with per-minimum admissibility evidence proving no candidate is admissible. No threshold shopping; no silent skips.

### Phase 0 — Bounded discovery/probe (only if materially new evidence exists)
1. Search for a **new** unauthenticated Hyperliquid-only observed-liquidations source/candidate not already falsified in `research_state/alt_source_deep_review_latest.md` (2026-11-13T17:12:25Z). If nothing materially new exists, do not re-probe the same endpoints; proceed to Phase 0B.
2. Collect machine-checkable evidence for: exact URL/dataset id, unauthenticated access, license/terms, label definition (observed fills/events, not modeled), schema/fields, UTC timestamps, symbol coverage (≥5), and coverage proving ≥1 complete month (≥ 2026-11) or ≥3 non-overlapping 30-day blocks with events+fills roles.
3. **Phase 0B (if no admissible candidate):** emit `research_state/tracka_admissibility_no_go_<UTC>.md` (and `.json` if useful) listing each candidate considered, evidence timestamp, and exact failing §16 minima; record that frontier remains blocked on external admissible data. This is a terminal evidence artifact, not a status stub.

### Phase 1 — Materialize and assess candidate manifest (required before outcomes)
1. Create candidate manifest JSON with full machine-verifiable provenance/label/coverage/block/symbol evidence required by `src.analysis.tracka_admissible.assess_ironflow_month_admissibility` / `scripts.tracka_resume_check.admissible_seam_check`.
2. Assess offline (fail-closed):
   `python -c "from scripts.tracka_resume_check import admissible_seam_check; from pathlib import Path; import json; print(json.dumps(admissible_seam_check(candidate_path='<manifest.json>', repo_root=Path('.')), indent=2))"`
3. **GO only if** `status: GO` and `pass: true` with validated month/block/symbol evidence. If NO_GO, fix evidence or record timestamped NO_GO proof (Phase 0B) — never force GO.

### Phase 2 — Gate to execution-ready (GO manifest only)
1. `python scripts/tracka_resume_gate.py --admissible-manifest <manifest.json> --json`
2. `python scripts/tracka_operator_report.py --admissible-manifest <manifest.json> --json`
3. If gate not GO (e.g. missing frozen prereg/data per harness): **freeze prereg BEFORE any outcome inspection** and assemble admissible data per contract; re-run until `GO` or a terminal, machine-readable blocked refusal is emitted and recorded.

### Phase 3 — Execute and terminally evaluate (only when gate GO)
1. Run guarded Track A execution (e.g. `PYTHONPATH=. python scripts/fclr010_guarded_entry.py ...` per its contract / wired harness entrypoint) with frozen prereg; capture manifests/logs.
2. Produce terminal evaluation summary + checks in `research_state/` (and any required registry/frontier updates) consistent with project contracts.
3. On any block: emit/record machine-readable refusal reason (no traceback-as-contract) and stop — do not fabricate outcomes.

### Phase 4 — Hygiene / closeout
- Keep `python scripts/fclr_next_campaign_gate.py --json` → `ok: true`.
- Run relevant deterministic tests for touched code/paths (at minimum Track A hardening/resume/gate tests affected by changes).
- Commit only meaningful research/engineering artifacts; update this handoff with exact commands, results, new artifact paths, and the next unfinished heavy task.

## 5) Invariants (never violate)
1. Fail-closed refusals; blocked paths must not inspect outcomes/parquet or write real `research_state`/canonical outputs except explicit durable evidence artifacts called for above.
2. **Preregistration before outcomes;** seam assessment is manifest-only (no parquet/outcome reads, no network).
3. Drift preflight before manifest/prereg decision logic in operator CLI.
4. No re-probe polling without new trigger/candidate evidence; no status-only churn; no conflation of observed vs modeled labels; no credentials/payment/manual downloads.
5. Do not modify `.github/workflows`.

## 6) Immediate next action for the next session
Start at **Phase 0/1**: determine whether a materially new Hyperliquid observed-liquidations candidate (≥2026-11, events+fills, §16-admissible) exists that is **not** falsified in `research_state/alt_source_deep_review_latest.md` (2026-11-13T17:12:25Z). If yes, build and seam-assess its manifest to GO (Phases 1-3). If no, produce the timestamped NO_GO admissibility evidence artifact (Phase 0B: `research_state/tracka_admissibility_no_go_<UTC>.md` + `.json`) listing each considered candidate, evidence timestamp, and exact failing §16 minima so the frontier is terminally evidenced rather than merely pending.

## 7) Session log — 2026-11-13T19:19:03Z
- **Verified (no-churn):** `python scripts/fclr_next_campaign_gate.py --json` → `ok: true`; `admissible_seam_check(None)` → `pass:true, NO_CANDIDATE_PENDING, ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE` (offline, manifest-only). No `*2026-11*hyperliquid*` candidate manifest and no prior `tracka_admissibility_no_go_*` artifact present.
- **Bottleneck status:** P0 material blocker unchanged — no admissible observed-liquidation candidate manifest (≥2026-11, events+fills, §16). No infra/workflow blockers; `.github/workflows` not modified.
- **Handoff consolidated:** refreshed this root file as the single timestamped durable handoff (2026-11-13T19:19:03Z) with explicit Phase 0-4 heavy-work campaign and terminal NO_GO path; flagged stale `research_state/FOCUS_CAMPAIGN.md` et al. as non-authoritative.
- **Next heavy task (unfinished):** Phase 0/1 — find/materialize & seam-assess a §16-admissible Hyperliquid candidate manifest to GO, or emit terminal `research_state/tracka_admissibility_no_go_<UTC>.{md,json}` evidence.
