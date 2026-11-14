# AGENT_HANDOFF — 2026-11-14T14:17:43Z (single durable handoff)

## Project
`Funding-conditioned-volatility-and-liquidation-risk` (repo: `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`)

## Initial task for the next agentic work session (start here)
**State: `TRIGGER_ONLY` (bounded). There is no agent-removable heavy campaign work right now. Do not run status-only or discovery-only sessions.**

1. Read this file, then `research_state/experiment_frontier.json` rank 0, then run `python3 scripts/next_campaign_status.py`.
2. Check for external triggers (must be new/material since `2026-11-14T13:27:41Z`):
   - Gate 4: `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` — only a file with `status==RESOLVED_VERIFIED`, `fabricated==false`, and human/legal attestation is a valid trigger.
   - New observed-liquidation source: materially new unauthenticated candidate with evidence not already falsified in `research_state/structural_exhaustion_confirmation_20261114T132741Z.md` / `research_state/new_data_admissibility_audit_20261114T123710Z.json` / `research_state/alt_source_deep_review_latest.md`.
   - HL label extension: Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels.
   - Expansion robustness redo: cached-panel robustness/falsification only if a NEW frozen prereg exists pre-outcomes.
3. **If no trigger is satisfied:** record a brief timestamped verification note in your response and **clean stop**. Do not poll, wait, repeat identical probes, re-execute tested/exhausted windows, or create status-only artifacts.
4. **If a trigger is satisfied:** execute only the corresponding branch under a **NEW experiment ID** with atomic, pre-outcomes discipline: freeze prereg (before outcomes) → §16 admissibility audit artifact when a new source is involved (ALL minima must pass before prereg/outcomes) → build/eval/verdict → update registry/frontier/manifest/run artifacts with hashes/verdicts. Run relevant gates/tests (`python3 scripts/fclr_campaign_gate.py --arm all` and targeted `unittest` modules). No threshold shopping, no sealed holdout/anchor overwrites.

## Current verified state (2026-11-14T14:17:43Z)
- Frontier rank 0: `FCLR-BOUNDED-TRIGGER-ONLY-20261114T132741Z`, `status=TRIGGER_ONLY`, `program_status=BOUNDED_TRIGGER_ONLY` (`research_state/experiment_frontier.json`).
- `python3 scripts/next_campaign_status.py` → no unfrozen/unexecuted prereg; no feasible 3-block design in either domain (Binance 5-symbol exhausted; Hyperliquid bulk forward reserve 2026-01-18..2026-04-30 tested/exhausted).
- Gate 4: **NO_VALID_GATE4_TRIGGER** (no `fclr016_v5_terms_evidence_RESOLVED_*` present; only blocked evidence files exist).
- New-source admissibility: **0 GO** (`research_state/new_data_admissibility_audit_20261114T123710Z.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/structural_exhaustion_confirmation_20261114T132741Z.md`).
- Targeted tests (this session): `python3 -m unittest -q tests.test_next_campaign_status tests.test_fclr_campaign_gate` → 41 tests OK.

## Explicit triggers (only these unblock heavy work)
| Trigger | Condition | Required action |
|---|---|---|
| `GATE4_BRANCH_1` | Valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) | Execute Gate 4 Branch 1 per gate scripts/tests under NEW experiment ID; no fabricated/resolved claims. |
| `NEW_OBSERVED_LIQUIDATION_SOURCE` | Materially new observed-liquidation candidate not falsified by prior audits | §16 admissibility audit artifact **before** prereg/outcomes → if ADMISSIBLE freeze prereg pre-outcomes → build/eval/verdict → atomic state updates (NEW experiment ID). |
| `HL_LABEL_EXTENSION` | HL ≥100d depth and verified post-2026-10-31 observed labels | Bounded reprobe only, pre-registered before outcomes. |
| `EXPANSION_ROBUSTNESS_REDO` | Cached-panel robustness with NEW frozen prereg pre-outcomes | Execute only that preregistered robustness scope. |

## Hard guardrails
- No polling/waiting loops, no repeated identical probes, no status-only sessions.
- No re-execution of tested/exhausted windows (including 2026-01-18..2026-04-30 forward reserve).
- No `.github/workflows` edits, no sealed holdout/anchor overwrites, no competing durable handoff files.
- No confirmatory outcomes while `all_go=false` / terms unresolved; no threshold shopping.
- No fabrication of terms/license/reviews; never mark resolved without verifiable facts.
- Follow `RESEARCH_PROMPT.md` and §16 admissibility minima for any new-source work.

## Key references
- `research_state/experiment_frontier.json` (rank 0 authoritative)
- `scripts/next_campaign_status.py`
- `research_state/structural_exhaustion_confirmation_20261114T132741Z.md`
- `research_state/new_data_admissibility_audit_20261114T123710Z.json`
- `research_state/alt_source_deep_review_latest.md`
- `research_state/fclr023_local_audit/fclr023_gate4_blocker_resolution_action_plan_latest.json` (blocker pipeline; all packets blocked/unready)
- `NEXT_SESSION_HANDOFF.md` (pointer only; do not use as operative instructions)

**This file is the single durable handoff.** Do not create parallel handoff documents.
