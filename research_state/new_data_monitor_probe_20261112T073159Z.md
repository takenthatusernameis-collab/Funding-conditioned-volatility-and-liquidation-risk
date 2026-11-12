# New-data monitor probe (bounded, in-session)
**Timestamp (UTC):** 2026-11-12T07:31:59Z
**Purpose:** Recheck Gate 4 trigger and probe plausibly-adjacent external sources for newly admissible claim-worthy window (§16) before any prereg/outcome work.

## 1) Gate 4 Branch 1 trigger
- Checked: `research_state/fclr016_local_audit/*RESOLVED*`
- Result: **ABSENT** (no `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Only BLOCKED/UNRESOLVED artifacts present.
- Action: Branch 1 not executable. No polling/wait.

## 2) ironflow/hyperliquid-liquidations (HF API, unauthenticated)
- Endpoint: `https://huggingface.co/api/datasets/ironflow/hyperliquid-liquidations`
- `lastModified`: `2026-11-07T10:18:25.000Z`
- `sha`: `65bad6c39c63ee24eae920753f05303020e549fa`
- `siblings_count`: 38
- Latest event month file observed in prior/known manifests: `data/events/2026-10.parquet` (no post-2026-10-31 event file, no 2026-11 event file).
- Determination: **No verified post-2026-10-31 observed liquidation labels.** Track A observed-label extension not eligible.

## 3) Hyperliquid 2026-11+ depth (public info API, unauthenticated, from 2026-11-01T00:00:00Z)
- BTC 1d candles: 12 rows (first `1793491200000` 2026-11-01, last `1794441600000` 2026-11-12) — span ~12.0 days inclusive.
- BTC funding history: 272 rows (first `1793491200061`, last `1794466800018`) — ~11.29 days.
- Eligibility minima for claim-worthy monitored reprobe (per campaign): HL ≥100 days and verifiable post-2026-10-31 observed labels.
- Determination: **11–12 days << 100 days and << 90 days (3×30d blocks). INELIGIBLE now.**

## 4) §16 admissibility summary
- `new_claim_worthy_experiment_eligible_now`: **false**
- Ineligibility reasons (evidenced): (i) no Gate 4 RESOLVED trigger; (ii) no verified post-2026-10-31 observed liquidation labels (ironflow unchanged beyond 2026-10); (iii) HL 2026-11+ window ~12d far below 100d/90d feasibility; (iv) metpie 2025Q2 remains sealed INADMISSIBLE (block-feasibility ~65d < 90d); (v) all cached-data designs sealed/exhausted.
- Next bounded reprobe only if plausibly eligible (HL depth ≥100d **and** verifiable post-2026-10-31 observed labels, or other genuinely new admissible source evidenced). **No polling.**

## Evidence artifacts
- This report: `research_state/new_data_monitor_probe_20261112T073159Z.md`
- Machine-readable: `research_state/new_data_monitor_probe_20261112T073159Z.json`
