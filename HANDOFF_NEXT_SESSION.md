# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T20:07:07Z
**Status:** AUTHORITATIVE. Execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are pointers. Ignore conflicting/stale docs.

## INITIAL TASK MESSAGE (EXECUTE NOW)
**Mission (repo-prioritized):** Advance funding-conditioned **liquidation-risk forecasting** (co-equal with volatility forecasting) on admissible, unauthenticated, provenance-backed data. Do **not** idle, do **not** produce status-only output, and do **not** relitigate closed work. Execute the first applicable heavy-work branch below and leave substantive artifacts plus consistent state updates.

**Verified entry state (2026-11-11):**
- **Gate 4 / Branch 1:** BLOCKED (external, human/legal). `research_state/fclr016_local_audit/` contains no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`; blocker: `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`fabricated=false`). Do **not** set `RESOLVED_VERIFIED`/`fabricated=true` or bypass terms.
- **Track A closed (do not relitigate):** `TRACKA-HL-S-20261111T133430Z` 2026-05..2026-10 9-symbol successor **NOT_MET** (`research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`). Early window `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` / `TRACKA-HL-EARLY-20261111T191958Z` **INADMISSIBLE** (`research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`).
- **Track B/C (2024):** closed negative; sealed holds immutable.
- **Active Branch 2 campaign (frozen prereg, in progress):** `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` / `TRACKA-HL-EXPANSION-20261111T195500Z`.
  - Prereg (frozen pre-outcomes): `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json|.md`
  - Ex-ante label probe (labels only): `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`
  - Cached inputs: ironflow labels `research_state/data_cache/ironflow_events/2025-05..2026-10.parquet`; HL funding/candles for original 9 coins; **partial expansion caches already present** for top candidates `ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH` (candles 2026-05..2026-10 under `hyperliquid_candles/<COIN>/`; funding files exist but may be incomplete/partial — verify coverage vs `2026-05-01..2026-10-31` before use). `DOT,HBAR,FIL,TRX,ICP,ALGO,ETC` have no caches.
  - Scripts present: `scripts/tracka_hl_expansion_probe.py`, `scripts/tracka_hl_expansion_funding_paginate.py`, `scripts/tracka_hl_fetch_candles_successor.py`, `scripts/tracka_hl_build_panel_with_rv.py`, `scripts/tracka_hl_evaluate_successor.py` (verify/adapt parameters for expansion universe/window; do not guess).

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH

### Branch 1 (CONDITIONAL — only if trigger appears now)
**Trigger:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
**Actions (deterministic, in order):** run promotion/admissibility validators (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or equivalents) with required `--expect-go`; only on all-green GO execute confirmatory Track C multi-split ablation on frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds); emit verdict(s) and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If absent (current):** proceed to Branch 2.

### Branch 2 (DEFAULT, MANDATORY NOW): `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`
**Goal:** Execute pre-registered symbol-expansion Track A claim on `2026-05-01..2026-10-31` (or prereg subwindow): **C2 (funding-conditioned) vs B1 (RV-only)** forecasting **observed** Hyperliquid liquidation intensity on a NEW ex-ante-selected universe (not a rerun of closed 9-symbol NOT_MET panel). Prereg is frozen — **do not modify prereg/split/selection rules** and **do not inspect forecast outcomes before panel/build is complete** per prereg.

**Execute in order (substantive artifacts required):**
1. **Finalize ex-ante universe selection (labels/acquirability only).** Apply frozen rules from `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json` using cached ironflow labels and `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`: confirm eligible `*-PERP` candidates (>=2 label months, exclude closed 9 + excluded prefixes/stables/fiat per prereg), choose target paired universe **>=5** by ex-ante notional rank subject to funding+candle acquirability, document final inclusion/exclusion with evidence in `research_state/tracka_hl_expansion_universe_<UTC>.json|.md`. **No cherry-picking, no test-set performance, no outcome inspection.**
2. **Bounded first-time unauthenticated acquisition (missing inputs only).** For each selected symbol missing/partial funding or 1h candles for required 2026-05..2026-10 months, fetch Hyperliquid `fundingHistory` and/or `candleSnapshot` and cache with provenance (`.accessed.json` + `.sha256`) under `research_state/data_cache/hyperliquid_funding/` and `research_state/data_cache/hyperliquid_candles/<COIN>/`. **Do not re-fetch already-valid cached 9-coin 2026-05..2026-10 data or any already-complete expansion files; verify coverage before fetch.** Rate-limit responsibly, cache-first. Emit `research_state/tracka_hl_expansion_acquisition_report_<UTC>.json`.
3. **Build deterministic RV-augmented expansion panel.** Join observed ironflow labels + funding + 1h candle-derived RV features (causal) per prereg for final universe; emit `research_state/tracka_hl_expansion_panel_<UTC>.parquet` and build report `..._build_report_<UTC>.json|.md` with hashes, coverage, leakage/embargo notes, symbol-month completeness, label/funding/RV availability, exact subwindow if narrowed by prereg rule.
4. **Run pre-registered evaluation only after (1)-(3).** C2 vs B1 QLIKE on next-24h observed liquidation intensity, 7d embargo, >=3 non-overlapping 30d test blocks, >=5 paired instruments, block bootstrap CIs, >=2% materiality (per prereg). Emit `research_state/evaluation_summary_TRACKA-HL-expansion-<UTC>.md` with verdict **MET / NOT_MET / INADMISSIBLE** and full evidence.
5. **Update state atomically.** Append/update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_symbol_expansion_liquidation_forecast), `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum; preserve 2024 H001 and all prior Track A records). Keep sealed records immutable.
6. **If infeasible under prereg minima/event-adequacy:** emit concrete infeasibility artifact with exact evidence (acquirability gaps, <5 paired instruments, <3 valid blocks, RV/label insufficiency), update state, then pivot to `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (new prereg frozen before outcomes on admissible untested Hyperliquid data; no Track C/Gate 4/2024 Binance conflation) and execute prereg→build→eval discipline as far as possible in-session.

## HARD BANS (BINDING)
- No outcome inspection before freeze/prereg; expansion prereg already frozen — do not alter and do not run forecast eval before panel/build complete.
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed.
- No threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C).
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance allowed where specified).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no Gate 4 human/legal bypass.
- **No status-only output:** every session must leave a substantive artifact (universe/acquisition/panel/eval or documented infeasibility + state updates).

## Key refs
- Handoff (authoritative): `HANDOFF_NEXT_SESSION.md`
- Pointers: `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md`
- Expansion prereg/probe: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json|.md`, `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`
- Prior Track A: `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`
- Scripts: `scripts/tracka_hl_*` (probe, paginate/fetch, build, evaluate)
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`

**Execute now:** Branch 1 only if Gate 4 RESOLVED trigger is present now; otherwise Branch 2 (`GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`) — start at universe finalization and bounded acquisition for missing/partial expansion inputs.
