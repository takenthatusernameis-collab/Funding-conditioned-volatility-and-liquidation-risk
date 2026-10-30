# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T04:52:10Z
HEAD: 7a1debef (main, origin/main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (repo name): LIQUIDATION RISK — FCLR-H004 / TRACK A 2026 EXPANSION IS THE ONLY UNBLOCKED LIQUIDATION PATH

The repo name is "Funding-conditioned-volatility-and-liquidation-risk". Observed liquidation risk (FCLR-H004 / Track A) is the namesake priority.

Frozen 2024 windows: Track A is BLOCKED — no admissible unauthenticated observed-liquidation census exists for 2024 (research_state/liquidation_sources_enumeration.md §1-4, §84-92; research_state/binance_source_probe.md). Three materially distinct routes spanning two source families exhausted: Binance archives+API (HTTP 404 / 451), Bybit/OKX/Deribit venue archives (no census), HF/Zenodo/GitHub repos (HF only 2026).

2026 expansion (smallest admissible scope expansion per RESEARCH_PROMPT §16): Track A is UNBLOCKED_2026 via the HF crypto-liquidation-ticks Bybit census (CC BY 4.0, unauthenticated, 2026-07-08..2026-08-06). Decision recorded at research_state/fclr_h004_tracka_viable.json (2026-10-30T02:15:00Z). Feature cache VERIFIED COMPLETE (see below). FCLR-005 pre-registered at research_state/research_protocol_fclr005.md (PROTOCOL_FROZEN 2026-10-30T04:30:00Z). FCLR-005 evaluation NOT yet run.

Forecast gates FCLR-001–004 are SEALED (NOT_MET/BLOCKED). Do NOT re-run them. Do NOT build risk overlays/simulations/merges. Do NOT touch .github/workflows/. Do NOT pivot away from H004 as the liquidation-priority track.

## BOTTLENECKS REMOVED (enforced — do not re-open)

- Source-discovery bottleneck removed: Bybit census via HF is admissible and verified; no further 2024 source probing (all confirmed dead ends recorded once; liquidation_sources_enumeration.md line 84-92). Do NOT re-probe without new evidence.
- Cache bottleneck RESOLVED: 2026 feature cache verified complete on disk — mark/index/premium klines 1h + monthly fundingRate for 2026-04-01..2026-08-06 all present under research_state/data_cache/<SYM>_2026_*/ (extracted CSVs confirmed); liquidations_full_20260807.csv verified via scripts/h004_audit.py (1,442,664 rows; bybit=346,269 / okx=236,896 / binance=859,499; target symbols present). scripts/h004_complete_cache.py is NOT needed — do not re-run. research_state/fclr_h004_tracka_viable.json §feature_cache_status_2026 is STALE (lists index/premium/funding as MISSING); treat it as corrected to COMPLETE based on on-disk verification.
- Forecast gates sealed — no re-runs, no overlay/sim/merge.
- Capped != census; absence != zero — no false "event-free" claims.
- Scope locked to H004 Track A / FCLR-005 2026 evaluation only.

## SINGLE TIMESTAMPED INITIAL TASK — CAMPAIGN H004-20261030T045210Z (HEAVY WORK, NO ESCAPE HATCH)

> **[2026-10-30T04:52:10Z] CAMPAIGN: EXECUTE FCLR-005 — TRACK A OBSERVED LIQUIDATION OUTCOMES ON THE 2026 BYBIT CENSUS**

**Mission (binary outcome):** Run the pre-registered FCLR-005 Track A evaluation on the 2026 Bybit liquidation census and produce EITHER (a) research_state/evaluation_summary_FCLR005.md with Brier/log-loss/calibration/precision-recall results for B0/B1/C1/C2 on long and short labels, base rate, event prevalence, coverage gaps, and an honest PILOT verdict (the ~30-day label window cannot meet the >=3-block confirmatory gate — do NOT claim confirmatory skill), OR (b) a documented evidence-backed blocker if the evaluation cannot run. Update hypothesis_registry.json (FCLR-H004 status) and research_state/run_manifest.json accordingly. Do NOT claim this clears any sealed FCLR-001-004 gate; FCLR-H004 remains BLOCKED for frozen 2024.

**Network:** Reachable (curl data.binance.vision → HTTP 200; HF → HTTP 302). Unauthenticated probes/downloads executable now. Do NOT treat "no network" as an excuse.

### Heavy work that cannot be avoided (do ALL, in order)

1. **Absorb context:** research_state/fclr_h004_tracka_viable.json, research_state/research_protocol_fclr005.md (FCLR-005 v1.0, pre-registered, PROTOCOL_FROZEN — do not change targets/features/splits after reading), research_state/liquidation_sources_enumeration.md §84-92, research_state/binance_source_probe.md, research_state/hypothesis_registry.json (FCLR-H004), this handoff.

2. **Verify cache completeness (already done — confirm, do not rebuild):** on-disk check that mark/index/premium klines 1h + monthly fundingRate CSVs exist for 2026-04-01..2026-08-06 for all 5 symbols under research_state/data_cache/<SYM>_2026_*/; liquidations_full_20260807.csv present with 1,442,664 rows. Re-run scripts/h004_audit.py only if evidence changes.

3. **Build Track A pipeline (HEAVY WORK — no script exists yet):** merge Bybit liquidation labels (census arm only; long/short separate) with Binance 2026 mark/funding/premium features at hourly UTC granularity; construct event count + USD notional intensity target per symbol-hour; apply frozen predictor definitions from research_protocol_fclr005.md §3 (no zero-fill / forward-fill). Write a new script under scripts/ (e.g. scripts/h004_fclr005_pipeline.py) that is idempotent, checkpointing, and resume-capable.

4. **Run evaluation:** B0 (persistence), B1 (RV-only), C1 (+funding), C2 (+price) on the 2026 window; chronological train/val/test split with embargo; report Brier, log-loss, calibration, precision-recall, AUPRC, base rate, event prevalence, coverage gaps; block bootstrap uncertainty, deterministic seed; leave-one-symbol-out stability.

5. **Forensic logging (MANDATORY):** append to research_state/liquidation_sources_enumeration.md — this session's FCLR-005 execution record (UTC timestamp, scripts run, rows merged, symbols covered, window, results). Append only, monotonic growth.

6. **Decision & deliverable:**
   - Write research_state/evaluation_summary_FCLR005.md with exact numbers and an honest PILOT verdict (~30-day label window cannot satisfy >=3-block confirmatory gate; no confirmatory skill claim).
   - Update research_state/hypothesis_registry.json FCLR-H004 status (PILOT_ONLY/EXPLORATORY_ONLY on 2026; BLOCKED for frozen 2024) and research_state/run_manifest.json (git SHA, config hash, data hashes, UTC timestamps, sample counts).

7. **Handoff readiness:** Leave FCLR-005 results complete enough that the next agent acts without re-running from scratch. Update AGENT_HANDOFF.md with precise next actions and any new blockers.

### Hard constraints (non-negotiable)
- No credentials, paid services/trials, manually supplied keys/files, user intervention. No bypassing auth/rate limits/terms.
- No forecast gate re-runs (FCLR-001–004 sealed). No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks until a forecast gate passes.
- Observed (Track A) != modeled (Track B) != volatility-only (Track C). Capped sample != census. Absence != zero. **Event-free intervals may NEVER be inferred from missing data.**
- Bybit rows = census arm; Binance/OKX rows = undercounted lower-bound only (never census, never binary absence/presence target).
- Commit nothing merely to show activity.

### Verification gates (MUST pass)
- `python -m unittest tests.test_funding_correction_replication -v` → 10/10
- `python scripts/h004_audit.py` → liquidations_full_20260807.csv schema/coverage confirmed (re-run only if evidence changes)
- research_state/liquidation_sources_enumeration.md must grow monotonically each session with dated records
- research_state/evaluation_summary_FCLR005.md exists with exact numbers + honest PILOT verdict

**START NOW. HEAVY WORK ON FCLR-005 / H004 TRACK A. Liquidation risk is the repo's namesake priority — this is the only liquidation path forward.**

## SECONDARY PATH (only if FCLR-005 is structurally exhausted)

H001's ≥3-block gate can be unblocked WITHOUT new downloads: research_state/data_cache holds cached Q4-2024 data (Oct–Dec) for all 5 symbols and run_manifest.json records pre-registered FCLR-003 splits (test 2024-10-02T00:00:00Z..2024-12-31T23:59:59Z, ~91 days = 3 non-overlapping 30-day blocks). Unblock route: coverage-only audit of the cached Q4 panel → frozen protocol version FCLR-003 v1.0 → run frozen pipeline → record canonical numbers. This does NOT open any sealed holdout for selection and does NOT change the INCONCLUSIVE verdict unless the gate passes. Do not let this distract from FCLR-005 / H004.

## CURRENT STATE SNAPSHOT

- H001 (incremental 24h volatility): INCONCLUSIVE. FCLR-002 primary contrast C2 vs B1 numerically passes (-9.28% rel QLIKE, CI [-0.097648,-0.008788] excludes zero, independently reproduced 2026-10-28 byte-identical) but minimum claim-worthy test NOT met (FCLR-001 BTCUSDT-only; 5-symbol intersection 0 timestamps Jan–Mar 2024; FCLR-002 test window = 70 days = 2 non-overlapping 30-day blocks < 3 required).
- H002 (funding-extreme correction-time replication): PARTIAL_REPLICATION (complete). 88 events Jan–Mar 2024, 5 symbols; median 8.0 h; 10/10 tests pass. SSRN HTTP 403 blocks exact replication; RV-regime contrast infeasible.
- H003 (hypothetical boundary-breach): INCONCLUSIVE. No incremental skill over B0 on any pre-specified metric.
- H004 Track A (observed liquidation labels): BLOCKED for frozen 2024 windows (structural evidence complete). UNBLOCKED_2026 via Bybit census — FCLR-005 pre-registered (research_state/research_protocol_fclr005.md), feature cache complete, evaluation NOT yet run.
- Forecast gates FCLR-001–004: NOT_MET/BLOCKED (sealed). Risk overlay: INELIGIBLE.
- Conflicting evaluation summaries flagged UNTRUSTED in research_state/evaluation_summary_conflict.md; neither verified; do not cite.
- Tests: `python -m unittest tests.test_funding_correction_replication -v` passes 10/10.

## KEY EVIDENCE

- research_state/fclr_h004_tracka_viable.json — Track A UNBLOCKED_2026 decision (2026-10-30T02:15:00Z), Bybit census source, completeness per venue, target symbol coverage, feature cache status (STALE — on-disk cache is COMPLETE), next action.
- research_state/research_protocol_fclr005.md — FCLR-005 v1.0 pre-registered protocol (frozen before outcomes).
- research_state/liquidation_sources_enumeration.md — Track A source enumeration (must grow monotonically; this session adds FCLR-005 execution record).
- research_state/binance_source_probe.md — Binance verified URLs + liquidation verdict (NOT VERIFIED / not directly downloadable).
- research_state/coverage_audit_recheck.md — FCLR-001 panel BTCUSDT-only; 5-symbol intersection 0 timestamps Jan–Mar 2024.
- research_state/hypothesis_registry.json — FCLR-H001..H004 statuses and next falsification tests.
- RESEARCH_PROMPT.md §§5, 7.2, 12, 15, 16 — constraints, source tracks, handoff contract, adaptive expansion.
- research_state/data_cache/ — cached Q4-2024 panel (H001 secondary path) + complete 2026 feature cache + liquidations_full_20260807.csv.
- scripts/h004_audit.py — audits HF crypto-liquidation-ticks (2026 window; verified valid this session).
- scripts/h004_download_2026.py / scripts/h004_complete_cache.py — cache build scripts (cache already complete; do not re-run unless evidence changes).

## DURABLE HANDOFF CONTRACT (per RESEARCH_PROMPT §12)

1. What changed and why: H004 Track A unblocked via 2026 Bybit census (fclr_h004_tracka_viable.json); 2026 feature cache verified complete (corrected stale fclr_h004_tracka_viable.json cache-status field); FCLR-005 pre-registered (research_protocol_fclr005.md); AGENT_HANDOFF.md refreshed with timestamped FCLR-005 campaign and enforced bottleneck removals.
2. What was actually tested, exact outcomes: `python -m unittest tests.test_funding_correction_replication -v` → 10/10 OK; `python scripts/h004_audit.py` → liquidations_full_20260807.csv valid (1,442,664 rows, Bybit census arm present, 2026-07-08..2026-08-06); curl data.binance.vision → HTTP 200, HF → HTTP 302 (network reachable).
3. Evidence added: research_protocol_fclr005.md (FCLR-005 pre-registration); h004_audit.py run output; AGENT_HANDOFF.md state correction. Enumeration unchanged except this handoff note — next session must grow research_state/liquidation_sources_enumeration.md with FCLR-005 execution record.
4. Current state of each research gate: H001 INCONCLUSIVE; H002 PARTIAL_REPLICATION; H003 INCONCLUSIVE; H004 BLOCKED (frozen 2024) / PILOT path open (2026 via FCLR-005); forecast gates sealed NOT_MET; overlay INELIGIBLE.
5. Single highest-value next task: execute FCLR-005 Track A evaluation on the 2026 Bybit census (this file, §CAMPAIGN H004-20261030T045210Z).
6. Precise verification command: `python -m unittest tests.test_funding_correction_replication -v` (10/10 required) + monotonic growth of research_state/liquidation_sources_enumeration.md + research_state/evaluation_summary_FCLR005.md with exact numbers.
7. Blocker with evidence and next free route: ~30-day 2026 label window cannot satisfy the >=3-block confirmatory gate → FCLR-005 verdict is PILOT/exploratory only; FCLR-H004 stays BLOCKED for frozen 2024. Next free route if FCLR-005 exhausted: H001 secondary unblock via cached Q4-2024 panel + FCLR-003 splits (secondary path, do not distract from FCLR-005).

FOCUS: FCLR-005 / H004 Track A 2026 evaluation only. Heavy work required. No escape hatch.
