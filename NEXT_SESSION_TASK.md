# NEXT_SESSION_TASK.md — Single Durable Initial Task for Next Agentic Session
**Timestamp (UTC):** 2026-11-10T16:11:30Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Project priority (by repo name):** 1) liquidation risk — Track B modeled boundary breaches (TESTED, NOT_SUPPORTED), 2) funding-conditioned volatility — Track C (concluded NOT_SUPPORTED), 3) Track A observed liquidations (STRUCTURALLY_BLOCKED).

## Current verdict (do not relitigate)
- **Track B (modeled liquidation boundary breaches): TESTED — NOT_SUPPORTED.** Preregistered campaign `TRACKB-MODELED-BREACH-20261110T154307Z` executed with frozen prereg (`prereg_hash=3c91885038e79345d7fdb28396505a5b7e57a6e7de146b9c3323d59bbfca0dc3`, `frozen_before_outcomes=true`) before outcomes. Panel 2025-01-01..2025-10-31, 5 symbols, provenance_verified=true/unmapped_count==0. Splits 40/20/40 + 7d purge/embargo, test 3 non-overlapping 30-day blocks. C2 vs B1 rel improvement 1.50% < 2% materiality floor, 95% CI [-0.005, 0.035] crosses zero → gate NOT_MET, overlay NOT ELIGIBLE. Modeled proxy only (NOT observed liquidations).
- **Track C / H1_primary: CONCLUDED UNDER CONSTRAINTS / NOT_SUPPORTED.** All locally available provenance-verified Track C panels with >=3 non-overlapping 30-day blocks tested. `next_unfinished_task (Track C): NONE` pending materially different verifiable data route.
- **Track A (observed liquidations): STRUCTURALLY_BLOCKED.**

## Completed artifacts
- `research_state/trackb_20251110T154307Z_admissibility.json`
- `research_state/research_protocol_trackb_20251110T154307Z.md` (frozen, prereg_hash recorded)
- `research_state/run_manifest.json` updated with Track B run + frozen splits
- `research_state/evaluation_summary_trackb_20251110T154307Z.md`
- Registries/frontier/negative-results/AGENT_HANDOFF updated

## Next unfinished task
**`next_unfinished_task: NONE — program concluded under constraints pending new admissible unauthenticated source`** (Track A blocked, Track B tested NOT_SUPPORTED, Track C concluded NOT_SUPPORTED). No network/new data available locally. Do not fabricate data/provenance; if a materially different admissible unauthenticated source appears, re-evaluate per protocol with prereg before outcomes.