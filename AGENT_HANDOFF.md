# AGENT_HANDOFF — 2026-11-14T14:19:09Z (single durable handoff)

## Project
`Funding-conditioned-volatility-and-liquidation-risk` (repo: `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`)

## Initial task for the next agentic work session (start here)
**State: `TRIGGER_ONLY` (bounded). No agent-removable heavy campaign work is available. This is a hard stop unless an explicit trigger is satisfied.**

1. Read this file, `research_state/experiment_frontier.json` (rank 0), and run `python3 scripts/next_campaign_status.py`.
2. Check external triggers (new/material since `2026-11-14T13:27:41Z`):
   - **Gate 4:** `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` — valid only if `status==RESOLVED_VERIFIED`, `fabricated==false`, and human/legal attestation present.
   - **New observed-liquidation source (Track A):** materially new unauthenticated candidate not already falsified in `research_state/structural_exhaustion_confirmation_20261114T132741Z.md`, `research_state/new_data_admissibility_audit_20261114T123710Z.json`, `research_state/alt_source_deep_review_latest.md`.
   - **HL label extension:** Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels.
   - **Expansion robustness redo:** cached-panel robustness/falsification only with a NEW frozen prereg (pre-outcomes).
3. **If no trigger is satisfied (current default):** report a brief timestamped verification note and **clean stop**. Do not poll/wait, do not repeat identical probes, do not re-run tested/exhausted windows, do not create status-only artifacts or new handoff files.
4. **If a trigger is satisfied:** open a **NEW experiment ID** and follow atomic pre-outcomes discipline only: freeze prereg before outcomes → if new source, produce §16 admissibility audit (`research_state/<source>_admissibility_audit_<UTC>.{md,json}`) proving ALL minima before prereg/outcomes → build/eval/verdict → update registry/frontier/manifest/run artifacts with hashes/verdicts. Run relevant gates/tests (`python3 scripts/fclr_campaign_gate.py --arm all`, targeted `unittest`). No threshold shopping, no sealed holdout/anchor overwrites, no `.github/workflows` edits.

## Current verified state (2026-11-14T14:19:09Z)
- Frontier rank 0: `FCLR-BOUNDED-TRIGGER-ONLY-20261114T132741Z`, `status=TRIGGER_ONLY`, `program_status=BOUNDED_TRIGGER_ONLY`.
- `python3 scripts/next_campaign_status.py` (checked this session): no unfrozen/unexecuted prereg; **no feasible 3-block design in either domain** (Binance 5-symbol exhausted; Hyperliquid bulk forward reserve 2025-05-01..2025-05-24, 24d, too short/tested-exhausted context).
- Gate 4: **NO_VALID_GATE4_TRIGGER** (`ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` → none).
- New-source admissibility: **0 GO** (prior audits/candidates falsified or not materially new).
- Bottlenecks are external/blocking (terms/evidence, admissible new observed-label source, HL depth+labels). No local code/data fix can unblock them without a real trigger; avoid busywork.

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
