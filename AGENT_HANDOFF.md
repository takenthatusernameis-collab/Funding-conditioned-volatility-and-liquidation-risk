# AGENT_HANDOFF — 2026-11-14T17:06:11Z (single durable handoff)

## Project
`Funding-conditioned-volatility-and-liquidation-risk` — `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`

## NEXT SESSION INITIAL TASK (inferred from repository name)
**Priority:** funding-conditioned volatility and liquidation risk. The highest-value unfinished work remains Track A observed-liquidation confirmation and, only when admissible, a new §16-compliant source or Gate 4 Branch 1. As of 2026-11-14T17:06:11Z there is no agent-removable cached-data heavy cell: `python3 scripts/next_campaign_status.py` reports no feasible 3-block design in either domain, and all frozen preregs have evaluation artifacts. Do not manufacture a new campaign or re-run tested windows. Execute the bounded trigger check below; if no trigger is satisfied, record a brief verification and clean stop. If any trigger is satisfied, immediately execute the corresponding heavy campaign under a NEW experiment ID with pre-outcomes discipline, build/eval/verdict, and atomic state updates.

## INITIAL TASK (next agentic session — execute immediately, no status-only work)
**Program state: `BOUNDED_TRIGGER_ONLY`** (frontier rank 0: `FCLR-BOUNDED-TRIGGER-ONLY-20261114T132741Z`). No unfrozen/unexecuted cached-data heavy cell is feasible now (`python3 scripts/next_campaign_status.py` → no feasible 3-block design in either domain). Bottlenecks are external (Gate 4 human/legal evidence; no §16-admissible new observed-liquidation source; HL depth/labels insufficient).

**Verification at 2026-11-14T17:06:11Z:** `python3 scripts/next_campaign_status.py` → no feasible 3-block design in EITHER domain; `python3 -m pytest tests/test_next_campaign_status.py -q` → 12 passed; Gate 4 glob → no `RESOLVED_*` file (only `BLOCKED_20261108T014835Z.json`); ironflow tree probe → HTTP 304 (no new data).

**Mandatory first actions (bounded, non-polling):**
1. Read this file and `research_state/experiment_frontier.json` (rank 0).
2. Run: `python3 scripts/next_campaign_status.py`
3. Check the four explicit triggers below against artifacts/state **newer/materially different than 2026-11-14T17:06:11Z**:
   - `GATE4_BRANCH_1`: `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` — valid only if a file exists with `status==RESOLVED_VERIFIED`, `fabricated==false`, and human/legal attestation present. (Current: none; only `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`.)
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new unauthenticated candidate not falsified in `research_state/structural_exhaustion_confirmation_20261114T132741Z.md`, `research_state/new_data_admissibility_audit_20261114T123710Z.json`, `research_state/alt_source_deep_review_latest.md` (22 candidates, 0 GO).
   - `HL_LABEL_EXTENSION`: Hyperliquid ≥100d depth AND verified post-2026-10-31 observed liquidation labels.
   - `EXPANSION_ROBUSTNESS_REDO`: cached-panel robustness/falsification with a **NEW** frozen prereg (pre-outcomes) not already executed.

**Branch:**
- **If NO trigger satisfied (expected):** report a brief verification (timestamp, status command outcomes, which triggers checked/absent) and **clean stop**. Do **not** poll/wait, repeat identical probes, re-run tested/exhausted windows, append verification-note churn, or create status-only artifacts/competing handoffs.
- **If ANY trigger satisfied:** do **not** stop at status. Immediately start the heavy campaign for that trigger under a **NEW experiment ID** (below). Pre-outcomes discipline is mandatory: freeze prereg before outcomes; for new sources produce §16 admissibility audit proving ALL minima before prereg/outcomes; build → eval → verdict → atomic state updates (registry/frontier/manifest/run artifacts with hashes/verdicts). Run relevant gates/tests (`python3 scripts/fclr_campaign_gate.py --arm all`, targeted `unittest`). No threshold shopping, no sealed holdout/anchor overwrites, no `.github/workflows` edits.

## Trigger-activated heavy campaigns (binding when triggered)
| Trigger | Go condition | Required heavy work (non-optional once triggered) |
|---|---|---|
| `GATE4_BRANCH_1` | Valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) | Execute Gate 4 Branch 1 per gate scripts/tests under NEW experiment ID; record evidence refs/hashes; update gate artifacts/state atomically. No fabricated/resolved claims. |
| `NEW_OBSERVED_LIQUIDATION_SOURCE` | Materially new observed-liquidation candidate not falsified by prior audits | Create `research_state/<source>_admissibility_audit_<UTC>.{md,json}` proving ALL §16 minima (unauthenticated download, provenance+license, venue-consistent perp liquidation events/not DeFi/OEV/modeled/heatmap, ≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, schema compatible with Track A, no Binance/2024 conflation). **If any minimum fails → NO-GO, stop that branch.** If ADMISSIBLE: freeze prereg pre-outcomes → build panel → eval → verdict → atomic state updates (NEW experiment ID). |
| `HL_LABEL_EXTENSION` | HL ≥100d depth and verified post-2026-10-31 observed labels | Bounded reprobe only, pre-registered before outcomes, under NEW experiment ID. |
| `EXPANSION_ROBUSTNESS_REDO` | Cached-panel robustness with NEW frozen prereg pre-outcomes | Execute only the preregistered robustness/falsification scope; emit eval/verdict; update state. |

## Verified constraints / exhausted space (do not retry)
- Binance 5-symbol: READY disjoint funding-backed months 2025-01/06/11/12; longest contiguous run 2025-11..2025-12 = 61d < 127d. **No feasible 3-block design.**
- Hyperliquid bulk forward reserve: 2025-05-01..2025-05-24 = 24d < 127d (TOO SHORT); 2026-01-18..2026-04-30 forward region tested/exhausted (TRACKA-LIQ-XSEC-FORWARD exploratory null, TRACKA-VOL-FORWARD exploratory null/valid_exploratory). **No untouched region ≥127d / ≥97d forward-reduced.**
- Every frozen prereg has an evaluation artifact (no unfrozen/unexecuted prereg). FCLR-LIQ-EXPANSION-RECONCILIATION completed `EXPLAINED_BY_ESTIMATOR` (exploratory). Sealed artifacts unchanged.
- Gate 4: `NO_VALID_GATE4_TRIGGER` (blocked artifact only; requires human/legal attestation).
- New-source admissibility baseline: 0 GO (`alt_source_deep_review_latest.md`, `new_data_admissibility_audit_20261114T123710Z.json`).

## Hard guardrails
- No polling/waiting loops, no repeated identical probes, no status-only sessions/verification-note churn.
- No re-execution of tested/exhausted windows (incl. 2026-01-18..2026-04-30 forward reserve).
- No `.github/workflows` edits, no sealed holdout/anchor overwrites, no competing durable handoff files.
- No confirmatory outcomes while `all_go=false` / terms unresolved; no threshold shopping.
- No fabrication of terms/license/reviews/data; never mark Gate 4 resolved without verifiable facts.
- Follow `RESEARCH_PROMPT.md` and §16 admissibility minima for any new-source work.

## Key references
- `research_state/experiment_frontier.json` (rank 0 authoritative)
- `scripts/next_campaign_status.py`
- `research_state/structural_exhaustion_confirmation_20261114T132741Z.md`
- `research_state/new_data_admissibility_audit_20261114T123710Z.json`
- `research_state/alt_source_deep_review_latest.md`
- `research_state/fclr023_local_audit/fclr023_gate4_blocker_resolution_action_plan_latest.json`
- `NEXT_SESSION_HANDOFF.md` (pointer only)

**This file is the single durable handoff. Do not create parallel handoff documents.**
