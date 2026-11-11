# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T20:04:18Z
**Status:** AUTHORITATIVE. This is the only task message to execute. Read fully before acting. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are pointers only. Any conflicting doc is stale.

## INITIAL TASK MESSAGE (EXECUTE NOW)
**Mission (repo-prioritized):** Advance funding-conditioned **liquidation-risk forecasting** (co-equal with volatility forecasting) using admissible unauthenticated data with verifiable provenance. Do not idle, do not report status only, and do not relitigate closed work. Execute the first applicable heavy-work branch below and leave substantive artifacts plus consistent state updates in this session.

**Session entry (verified 2026-11-11):**
- **Gate 4 / Branch 1:** BLOCKED (external). `research_state/fclr016_local_audit/` has no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`; blocker present: `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`fabricated=false`). **Do not set `RESOLVED_VERIFIED`/`fabricated=true` or bypass human/legal terms.**
- **Track A 2026-05..2026-10 9-symbol successor:** CLOSED **NOT_MET** (`TRACKA-HL-S-20261111T133430Z`, `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`). Do not relitigate or rerun.
- **Early-window pivot (completed, closed):** `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` / `TRACKA-HL-EARLY-20261111T191958Z` is **INADMISSIBLE** with documented evidence (`research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`, `research_state/tracka_hl_early_candle_fetch_report_20261111T193140Z.json`): bounded first-time candleSnapshot acquisition 2025-11..2026-04×9 coins completed (HTTP 200, provenanced); 2025-11..2026-03 empty for all coins, 2026-04 partial (~327-328 rows/coin) → RV24h/B1 not computable, >=3 test blocks unsatisfiable. No outcome computation performed (prereg frozen pre-outcomes). Do not relitigate or re-acquire.
- **Current pivot campaign (frozen prereg, in progress):** `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`, `TRACKA-HL-EXPANSION-20261111T195500Z`, prereg frozen pre-outcomes `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json|.md`. Ex-ante label-activity probe/ranking on cached ironflow 2026-05..2026-10 (labels only, not outcomes): `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json` (top eligible by notional include ZEC, NEAR, UNI, AAVE, CRV, ADA, LTC, BCH, DOT, HBAR, FIL, TRX, ICP, ALGO, ETC, all 6/6 months). **Not yet done:** final ex-ante universe selection document, funding+candle acquisition for needed expansion candidates, deterministic panel build, pre-registered evaluation, verdict/state updates.
- **Cached admissible inputs (verified):**
  - Ironflow observed liquidation labels (Hyperliquid): `research_state/data_cache/ironflow_events/2025-05..2026-10.parquet`.
  - HL funding (9 coins AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP): `research_state/data_cache/hyperliquid_funding/*.json`, ~2025-11-01T00:00Z..2026-10-30T23:00Z.
  - HL 1h candles (same 9 coins): `research_state/data_cache/hyperliquid_candles/<COIN>/2026-05..2026-10.{json,accessed.json,sha256}`. **Expansion candidates beyond these 9 likely require bounded first-time fundingHistory/candleSnapshot acquisition for 2026-05..2026-10 with provenance.**
- **Track B/C (2024):** closed negative; sealed holds immutable.

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH

### Branch 1 (CONDITIONAL, only if trigger appears now)
**Trigger:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
**Actions (deterministic, in order):**
1. Run Gate 4 promotion/admissibility validators per tooling (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or repo equivalents) with required `--expect-go` semantics.
2. Only on all-green GO, execute confirmatory Track C multi-split ablation on the frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds) with frozen artifacts.
3. Emit verdict artifact(s) under `research_state/` and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If trigger absent (CURRENT):** proceed to Branch 2.

### Branch 2 (DEFAULT, MANDATORY NOW): `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (TRACKA-HL-EXPANSION-20261111T195500Z)
**Goal:** Execute the pre-registered symbol-expansion Track A claim on `2026-05-01..2026-10-31` (or prereg subwindow) — C2 (funding-conditioned) vs B1 (RV-only) forecasting **observed Hyperliquid liquidation intensity** — using a NEW ex-ante-selected universe (different design from closed NOT_MET 9-symbol panel). Prereg is already frozen; **do not modify prereg/split/selection rules** and **do not inspect forecast outcomes before panel/build is complete per prereg discipline**.

**Execute in order (substantive artifacts required; no status-only session):**
1. **Finalize ex-ante universe selection (labels/acquirability only, no forecast outcomes).** Apply frozen rules from `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json` to cached ironflow labels and `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`: confirm eligible *-PERP candidates (>=2 label months, exclude closed 9 + excluded prefixes/stables/fiat per prereg), choose target paired universe >=5 by ex-ante notional rank subject to funding+candle acquirability, and document final inclusion/exclusion with evidence in `research_state/tracka_hl_expansion_universe_<UTC>.json|.md`. **No cherry-picking, no test-set performance, no outcome inspection.**
2. **Bounded first-time unauthenticated acquisition (missing inputs only).** For each selected coin/symbol missing funding and/or 1h candles for required 2026-05..2026-10 months, fetch Hyperliquid `fundingHistory` and/or `candleSnapshot` and cache with provenance (`.accessed.json` + `.sha256`) under `research_state/data_cache/hyperliquid_funding/` and `research_state/data_cache/hyperliquid_candles/<COIN>/`. **Do NOT re-fetch already-cached 9-coin 2026-05..2026-10 candles or existing funding files.** Rate-limit responsibly, cache-first, no redundant polling. Emit acquisition report `research_state/tracka_hl_expansion_acquisition_report_<UTC>.json`.
3. **Build deterministic RV-augmented expansion panel.** Join observed ironflow labels + funding + 1h candle-derived RV features (causal) per prereg; emit `research_state/tracka_hl_expansion_panel_<UTC>.parquet` and build report `..._build_report_<UTC>.json|.md` with hashes, coverage, leakage/embargo notes, symbol-month completeness, label/funding/RV availability, and exact subwindow if narrowed per prereg rule.
4. **Run pre-registered evaluation only after (1)-(3).** C2 vs B1 QLIKE on next-24h observed liquidation intensity, 7d embargo, >=3 non-overlapping 30d test blocks, >=5 paired instruments, block bootstrap CIs, >=2% materiality (all per prereg). Emit `research_state/evaluation_summary_TRACKA-HL-expansion-<UTC>.md` with verdict **MET / NOT_MET / INADMISSIBLE** per prereg rules and full evidence.
5. **Update state atomically.** Append/update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_symbol_expansion_liquidation_forecast), `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum; preserve 2024 H001 and all prior Track A records including early INADMISSIBLE and 9-symbol NOT_MET). Keep sealed records immutable.
6. **If infeasible under prereg minima/event-adequacy:** emit a concrete infeasibility artifact citing exact evidence (acquirability gaps, <5 paired instruments, <3 valid test blocks, RV/label insufficiency), update state, then pivot to `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (new prereg frozen before outcomes on admissible untested Hyperliquid data; no Track C/Gate 4/2024 Binance conflation) and execute prereg→build→eval discipline as far as possible in-session.

**Secondary (only after expansion fully resolved with artifacts):** `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` with pre-registered, outcome-frozen design on admissible untested Hyperliquid data.

## Hard bans (binding)
- No outcome inspection before freeze/preregistration for any new claim (expansion prereg already frozen — do not alter; do not run forecast eval before panel/build complete).
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed (Track A requires observed labels with provenance).
- No threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C).
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance allowed/required where specified).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no bypass of Gate 4 human/legal terms.
- **No status-only output:** every session must leave a substantive artifact (universe/acquisition/panel/eval or documented infeasibility + state updates).

## Key refs
- Handoff (this file): `HANDOFF_NEXT_SESSION.md`
- Pointers: `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md`
- Expansion prereg/probe: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json|.md`, `research_state/tracka_hl_expansion_probe_report_20261111T195336Z.json`
- Prior Track A: `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`
- Scripts: `scripts/tracka_hl_*` (probe, fetch, build, evaluate utilities as applicable)
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`

**Execute now: Branch 1 only if Gate 4 RESOLVED trigger is present now; otherwise Branch 2 (`GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10`) heavy campaign — start at universe finalization/acquisition.**
