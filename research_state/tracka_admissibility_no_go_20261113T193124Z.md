# Track A Admissibility NO_GO (terminal evidence)

**timestamp_utc:** 2026-11-13T19:31:24Z
**artifact:** `tracka_admissibility_no_go_20261113T193124Z.json`
**track:** A (observed-liquidation resume)
**verdict:** NO_GO — TERMINAL_BLOCKED_EXTERNAL_DATA

## Reason
Track A resume requires an Ironflow Hyperliquid `events`+`fills` candidate for month **>= 2026-11**.
The cache holds ironflow **events** only through **2026-10**; there is **no 2026-11 events/fills parquet**,
no candidate manifest, and **no admissible alternative observed-liquidation source** (22 candidates falsified
in `alt_source_deep_review_latest.md` 2026-11-13T17:12:25Z). The seam is wired and fail-closed; the resume
check correctly returns `NO_CANDIDATE_PENDING` because no real candidate/data exists.

## Cache gap (verified 2026-11-13T19:31:24Z)
- ironflow events months: 2026-10 is the latest (range 2025-05..2026-10); **2026-11 absent**.
- ironflow fills months: NONE cached.
- Required: events **and** fills for **2026-11** (or >=3 non-overlapping 30-day blocks; same data gap).

## Candidate considered
| Candidate | Evidence | Verdict | Failing minima |
|---|---|---|---|
| ironflow/hyperliquid-liquidations 2026-11 (events+fills) | cache scan 2026-11-13T19:31:24Z: events through 2026-10; fills absent; no 2026-11 parquet | **NO_GO** | data_not_present; month_below_cache_max; fills_missing |

## Seam check
`assess_ironflow_month_admissibility` → structurally valid manifests can return GO, but
`tracka_resume_check.admissible_seam_check(None)` → `pass:true, NO_CANDIDATE_PENDING`
(`ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE`). Offline, manifest-only, no parquet/outcome reads.

## Interpretation (RESEARCH_PROMPT section 16)
This cell is **blocked on external data only** (post-2026-10 observed HL liquidation labels). No internal
work can satisfy the trigger. Per section 16, **do not write further blocker memos or re-verify**; the blocked
cell blocks only itself. Advance the unblocked tracks below with real, bounded work.

## Unblocked heavy-work tracks (execute these; do not idle)
1. **Track C** volatility/stress outcomes from admissible cached price/mark history (never needs liquidation labels).
2. **Funding-conditioned volatility** ablations / Gate 4 on cached data; coverage & inference diagnostics.
3. **Section-16 narrow-cohort pilots** with new IDs, preregistered before outcomes.
4. **Seam/gate/CLI hardening** with tmp-isolated tests; keep regression green; no status-only churn.

## Next trigger (only)
A materially new, unauthenticated, observed-liquidation source **or** Ironflow month **>= 2026-11**
events+fills appears (not falsified above) → build + seam-assess manifest to **GO** before any outcome
inspection → freeze prereg → execute → sealed evaluation.
