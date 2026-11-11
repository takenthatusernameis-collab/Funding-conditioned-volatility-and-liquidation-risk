# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T19:07:13Z
**Status:** AUTHORITATIVE. This is the only task message to execute. Read fully before acting. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are pointers only. Any conflicting doc is stale.

## INITIAL TASK MESSAGE (EXECUTE NOW)
**Mission (repo-prioritized):** Advance funding-conditioned **liquidation-risk forecasting** (co-equal with volatility forecasting) using admissible unauthenticated data with verifiable provenance. Do not idle, do not report status only, and do not relitigate closed work. Execute the first applicable heavy-work branch below and leave substantive artifacts plus consistent state updates in this session.

**Session entry (verified 2026-11-11):**
- **Gate 4 / Branch 1:** BLOCKED (external). `research_state/fclr016_local_audit/` has no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`; blocker present: `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`fabricated=false`). **Do not set `RESOLVED_VERIFIED`/`fabricated=true` or bypass human/legal terms.**
- **Track A 2026-05..2026-10:** CLOSED **NOT_MET** (`research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`, `TRACKA-HL-S-20261111T133430Z`). Do not relitigate or rerun without a new pre-registered design/data.
- **Cached admissible inputs (verified):**
  - Ironflow observed liquidation labels (Hyperliquid, observed): `research_state/data_cache/ironflow_events/` — 18 monthly parquets `2025-05.parquet..2026-10.parquet` (2025-05 partial from 2025-05-25 per prior records).
  - HL funding (9 coins: AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP): `research_state/data_cache/hyperliquid_funding/*.json` — 8668 hourly records each, coverage ~`2025-11-01T00:00:00Z`..`2026-10-30T23:00:00Z` (ms timestamps 1761955200078..1793401200078; confirm exact per-coin bounds in prereg/build).
  - HL 1h candles (same 9 coins): `research_state/data_cache/hyperliquid_candles/<COIN>/2026-05..2026-10.{json,accessed.json,sha256}` only. **NO candle cache for 2025-11..2026-04. Do NOT re-fetch 2026-05..2026-10.**
- **Gap audit (authoritative for Branch 2):** `research_state/next_panel_gap_audit_20261111T163229Z.md|.json` — selected campaign `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`.
- **Track B/C (2024):** closed negative; sealed holds immutable.

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH

### Branch 1 (CONDITIONAL, only if trigger appears now)
**Trigger:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
**Actions (deterministic, in order):**
1. Run Gate 4 promotion/admissibility validators per tooling (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or repo equivalents) with required `--expect-go` semantics.
2. Only on all-green GO, execute confirmatory Track C multi-split ablation on the frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds) with frozen artifacts.
3. Emit verdict artifact(s) under `research_state/` and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If trigger absent (CURRENT):** proceed to Branch 2.

### Branch 2 (DEFAULT, MANDATORY NOW): `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`
**Goal:** Pre-register and evaluate a **new** funding-conditioned vs RV-only forecast of **observed Hyperliquid liquidation intensity** on an earlier admissible window, disjoint from NOT_MET 2026-05..2026-10. Use ironflow observed labels + cached HL funding (~2025-11-01..2026-04 overlap) for the 9 cached coins; candles/RV are missing for that window and must be acquired/built deterministically. Use `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` as structural template only; **do not copy outcomes**.

**Execute in order (substantive artifacts required; no status-only session):**
1. **Freeze preregistration BEFORE any outcome computation/alignment for the new claim.** Create `research_state/tracka_prereg_hyperliquid_early_<UTC>.json` (+ optional `.md`) fixing: hypothesis/claim; exact window and symbol set (from 9 coins with confirmed overlap); observed label definition/source (ironflow, Hyperliquid only) and aggregation horizon; predictor families (B1 RV-only baseline vs C2 funding-conditioned); target/metric; train/val/test splits with >=7d purge/embargo; >=3 non-overlapping 30d test blocks and >=5 paired instruments minima or explicit ex-ante infeasibility rule; block-bootstrap CI spec; materiality threshold (>=2% where applicable); missingness/inclusion rules; input provenance/checksums; git HEAD; freeze timestamp. **No outcome inspection first.**
2. **Bounded first-time unauthenticated acquisition (missing inputs only).** For prereg-specified coins/months lacking candles, fetch Hyperliquid `candleSnapshot` 1h and cache under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` with `.accessed.json` provenance and `.sha256` (endpoint, params, access UTC, status, checksums/sizes, unauthenticated/no-key/no-requester-pays/signature status). Candidate months ~2025-11..2026-04 per confirmed overlap. **Do NOT re-fetch 2026-05..2026-10.** No redundant polling; cache first.
3. **Build deterministic RV-augmented panel from cached inputs.** Emit `research_state/tracka_hl_early_panel_<UTC>.parquet` and build report JSON/MD with hashes, coverage, leakage/embargo notes, symbol-month completeness, observed-label provenance.
4. **Run pre-registered evaluation only after (1)-(3).** Compute contrasts/splits per prereg; emit `research_state/evaluation_summary_TRACKA-HL-early-<UTC>.md` with verdict (MET/NOT_MET/INADMISSIBLE per prereg), bootstrap CIs, gate checks.
5. **Update state atomically.** Append/update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum; preserve 2024 H001 and prior Track A records). Keep sealed records immutable.
6. **If infeasible under prereg minima:** emit a concrete infeasibility artifact citing exact evidence (coverage gaps, block/instrument shortfall), update state to record infeasibility, then pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (new prereg with frozen ex-ante symbol selection/event-adequacy rules; bounded first-time acquisition as needed) and execute the same prereg→build→eval discipline.

**Secondary (only after Track A candidates exhausted with documented evidence):** `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` on admissible untested Hyperliquid data, pre-registered before outcomes, no Track C/Gate 4/2024 Binance conflation.

## Hard bans (binding)
- No outcome inspection before freeze/preregistration for any new claim.
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed (Track A requires observed labels with provenance).
- No threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C).
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance allowed/required where specified).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no bypass of Gate 4 human/legal terms.
- **No status-only output:** every session must leave a substantive artifact (prereg/fetch-manifest/panel/eval or documented infeasibility + state updates).

## Key refs
- Handoff (this file): `HANDOFF_NEXT_SESSION.md`
- Pointers: `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md` (redirect)
- Gap audit: `research_state/next_panel_gap_audit_20261111T163229Z.md|.json`
- Track A template/artifacts: `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`, `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`, `scripts/tracka_hl_*`
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`
- Checks: `python -m unittest discover -s tests -v` (relevant scope)

**Execute now: Branch 1 only if Gate 4 RESOLVED trigger is present now; otherwise Branch 2 (`GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`) heavy campaign.**
