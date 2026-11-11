# HANDOFF: Next Agentic Work Session (2026-11-11T12:02:14Z)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility AND liquidation risk)
**Single durable handoff (authoritative):** This file is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` point here. Do not start from older/parallel campaign notes without reconciling against this handoff. Read this entire file before any action.

## Prioritization (from repository name)

The repo name encodes a dual mission:
1. **Funding-conditioned volatility forecasting** (Track C / Gate 4): test whether funding extremes + realized volatility + price-dislocation features improve out-of-sample forecasts of future realized volatility vs. an RV-only baseline.
2. **Liquidation-risk forecasting** (Track A): test whether funding-conditioned features improve out-of-sample forecasts of observed liquidation intensity vs. an RV-only baseline.

Both are in scope per the repo name. However, **Track C confirmatory on 2025+ Binance data is structurally BLOCKED** pending verifiable human/legal review of Binance Vision market-data terms (`research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`). This is an external dependency an agent cannot automate or fabricate. **Do not stall on Track C.**

Therefore the **primary computable campaign for this session is Track A** (observed Hyperliquid liquidation-intensity forecasting): SOURCE-GO (ironflow CC BY 4.0, unauthenticated, complete months 2025-06..2026-10, 2.85M rows), prereg frozen pre-outcomes (`TRACKA-HL-20261111T073000Z`), but panel alignment context is pending. Execute computable Track A work now; keep Track C documented-but-blocked.

## Hard state (do not relitigate)

- **Track B/C confirmatory (2024 Binance):** closed/negative — `research_state/final_confirmatory_verdict.md`: H001 NOT_SUPPORTED. No rescue on sealed holds. Overlay INELIGIBLE. Forecast gate NOT_MET.
- **Gate 4 / Track C extension (2025+ Binance confirmatory):** BLOCKED (structural, external). Requires verifiable human/legal Binance terms review → create `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (all 8 fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal reviewer). Fail-closed guards prohibit confirmatory outcomes on 2025+ until resolved. No code/tests/data work can bypass.
- **Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0):** SOURCE GO but PANEL BLOCKED. Prereg frozen pre-outcomes: `research_state/tracka_prereg_hyperliquid_2026.json` (2025-06..2026-10, C2 vs B1, QLIKE). Labels cached: `research_state/data_cache/ironflow_events/` (2025-05..2026-10, 2.85M rows, 468 markets). Alignment blocker: `research_state/tracka_hl_alignment_blocker.md` — admissible unauthenticated Hyperliquid-native context incomplete for full prereg window (funding 2025-11..2026-10 only; mark-price candles ~2026-05..2026-10 only; no admissible historical index/premium/klines back to 2025-06). Full prereg panel not buildable as frozen.
- **Forbidden (all tracks):** no outcome inspection before (successor) prereg freeze; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; no network polling/redundant GETs beyond cached provenance; no status-only output.

## Bottlenecks to remove (next session must execute; heavy work required)

**1. Track C Gate 4 — externally blocked, document only.**
- Status: `EXPLICIT_BLOCKER_UNRESOLVED` on `license_terms`. All other v5 artifacts (provenance manifest, completeness/leakage audit `PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC`, prereg draft, identity consolidation) are complete and green.
- Action this session: record explicit status note in this handoff that human/legal terms review is pending. Do **not** attempt any bypass, fabrication, or `RESOLVED_VERIFIED` without human fields. Track C confirmatory remains on hold until `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists.

**2. Track A alignment closure — primary computable campaign (heavy, inescapable).**
Bring Track A to a terminal, auditable state by picking exactly one path and recording it:

- **(a) Extend coverage with evidence:** search local/admissible cached artifacts and documented Hyperliquid-native unauthenticated sources for mark/index/premium/klines/funding covering 2025-06..2026-10 for overlapping symbols (BTC, ETH, BNB, SOL, XRP, AVAX, DOGE, LINK, SUI as `-PERP`). Document provenance (URL, access date, hash/ETag, license, terms) and exact coverage in `research_state/tracka_alignment_patha_audit_<UTC>.md` (+json if useful). Reusable scripts: `scripts/hyperliquid_funding_fetch.py` (fundingHistory), `scripts/tracka_hl_pathb_probe.py` (bounded overlap probe, writes probe JSON, no outcomes inspected).
- **Decision gate:**
  - If full prereg window+context becomes admissibly complete → build aligned panel, run **pre-registered** evaluation per `tracka_prereg_hyperliquid_2026.json` (no outcome inspection before frozen inputs/checksums recorded), emit verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md` and update frontier/registry/manifest/final verdict atomically.
  - If not (expected): **(b) scope-down requires NEW successor prereg before any outcome computation** — freeze `research_state/tracka_prereg_hyperliquid_successor_<UTC>.json` on the maximal overlap where labels+all required context exist (document exact window/symbols/splits/≥3 test blocks if claim-worthy), build panel, run evaluation, emit verdict artifact + atomic state updates; OR **(c) terminal closure** if no admissible aligned overlap meets prereg minimums — emit verdict artifact documenting alignment inadmissible/insufficient with evidence and close Track A panel as NOT_SUPPORTED/BLOCKED, with atomic state updates.

**3. Gate 4 promotion only after (1):** if resolved terms evidence is produced this session, run deterministic reconciliation/promotion (frozen scope 2025-08-01..2025-10-31, 5 symbols, 5 kinds, consistent `admissibility_refs_sha256`) then:
- `python scripts/fclr016_v5_preflight_summary.py <prov> <compl> <terms_RESOLVED> <prereg>`
- `python scripts/fclr016_validate_v5_admissibility.py ... --expect-go`
- `python scripts/run_funding_ablations.py --check-admissibility-package ... --expect-go`
Only on all-green GO: execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) and produce frozen evaluation artifacts. If (1) absent, do **not** fake/force GO.

## Required outputs this session (non-negotiable)

- Evidence/audit or verdict artifact for the Track A path taken (a/b/c) under `research_state/`.
- Any successor prereg (if path b) frozen **before** outcome computation, with hashes/inputs recorded.
- `run_manifest`/`experiment_frontier`/`hypothesis_registry`/final verdict updated atomically if a terminal evaluation/closure is reached.
- This handoff kept current: timestamped note of what was done, what remains, exact next command/files.
- No status-only output. Obey all hard bans above.

## Key refs

- Track A: `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/hl_coverage_probe.json`, `src/analysis/tracka_admissible.py`, `scripts/hyperliquid_funding_fetch.py`, `scripts/tracka_hl_pathb_probe.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/run_funding_ablations.py`
- Prior closeout: `research_state/final_confirmatory_verdict.md`
- Repo-wide checks: `python -m unittest discover -s tests -v` (all passing baseline)

**End of Handoff — Next Agent Must Read This Entire File Before Any Action**
