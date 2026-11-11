# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, authoritative):** 2026-11-11T18:51:48Z
**Status:** AUTHORITATIVE. This is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. `AGENT_HANDOFF.md` is a redirect only. Any doc conflicting with this handoff is stale. Read fully before acting. **No status-only output.**

**SESSION ENTRY (VERIFIED 2026-11-11T18:51:48Z):** `research_state/fclr016_local_audit/` contains no `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`; Gate 4 remains **EXPLICIT_BLOCKER_UNRESOLVED** (`fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `fabricated=false`). **Execute Branch 2 now.** Root 2024 raw clutter is consolidated to `data/raw_legacy_2024q1_scattered/`.

## INITIAL TASK MESSAGE (EXECUTE NOW) — 2026-11-11T18:51:48Z

**Mission (repo-prioritized):** Advance `Funding-conditioned-volatility-and-liquidation-risk` on **liquidation-risk forecasting co-equal with volatility forecasting**, using admissible unauthenticated data with verifiable provenance. Track A successor (2026-05..2026-10, 9 symbols, observed ironflow) is evaluated **NOT_MET** (closed for that prereg). Track B/C (2024) are closed negative. Gate 4 is externally blocked. **Do not idle, do not report status only, do not relitigate closed work. Execute the first applicable heavy-work branch below and leave substantive artifacts + consistent state updates.**

### Current verified state
- **Gate 4 / Track C:** BLOCKED — no valid RESOLVED terms evidence in `research_state/fclr016_local_audit/`. Do not fabricate or self-attest.
- **Track A (closed, do not relitigate):** `TRACKA-HL-S-20261111T133430Z` (2026-05-01..2026-10-31) **NOT_MET** (`research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, panel `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`).
- **Cached admissible inputs (verified):**
  - Ironflow observed labels (Hyperliquid): `research_state/data_cache/ironflow_events/` — 18 monthly parquets `2025-05..2026-10` (~2.85M rows, 468 markets; 2025-05 partial from 2025-05-25).
  - HL funding (9 coins AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP): `research_state/data_cache/hyperliquid_funding/*.json` — hourly, ~`2025-11-01T00:00:00Z..2026-10-30T23:00:00Z` (confirm exact per-coin bounds in prereg/build).
  - HL 1h candles (same 9 coins): `research_state/data_cache/hyperliquid_candles/<COIN>/2026-05..2026-10.json` (+ `.accessed.json`, `.sha256`) — **NO candle cache for 2025-11..2026-04**. **Do NOT re-fetch 2026-05..2026-10.**
- **Gap audit:** `research_state/next_panel_gap_audit_20261111T163229Z.md|.json` — selected next campaign `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`.
- **Bottlenecks already removed:** single durable handoff consolidated; root 2024 raw clutter consolidated to `data/raw_legacy_2024q1_scattered/`.

---

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH

### Branch 1 (CONDITIONAL, execute immediately only if artifact exists): Gate 4 / Track C volatility unblocking
**Trigger:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
**Actions (deterministic, in order):**
1. Run Gate 4 promotion/admissibility validators per tooling (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or repo equivalents) with `--expect-go` semantics where applicable.
2. Only on all-green GO, execute confirmatory Track C multi-split ablation on the frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds) with frozen artifacts.
3. Emit verdict artifact(s) under `research_state/` and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If trigger absent (CURRENT):** remain `EXPLICIT_BLOCKER_UNRESOLVED`. **Do NOT set `RESOLVED_VERIFIED` or `fabricated=true`; do NOT bypass/fabricate terms evidence. Proceed to Branch 2.**

### Branch 2 (DEFAULT, mandatory now): New observed-liquidation Track A claim `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`
**Goal:** Pre-register and evaluate a **new** funding-conditioned vs RV-only forecast of **observed Hyperliquid liquidation intensity** on an earlier admissible window using ironflow labels + cached HL funding (~2025-11-01..2026-04 overlap, 9 coins), with candles/RV currently missing for that window. **Disjoint in design from NOT_MET 2026-05..2026-10.** Use `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` as structural template only; do not copy outcomes.

**Execute in order (substantive artifacts required; no status-only):**
1. **Freeze preregistration BEFORE any outcome computation/alignment for the new claim.** Create `research_state/tracka_prereg_hyperliquid_early_<UTC>.json` (+ optional `.md`) fixing: hypothesis/claim, exact window/symbols, observed label definition/source (ironflow, Hyperliquid only) and aggregation horizon, predictor families (B1 RV-only baseline vs C2 funding-conditioned), target/metric (e.g. QLIKE on next-24h liquidation intensity or justified alternative), train/val/test splits with >=7d purge/embargo, >=3 non-overlapping 30d test blocks and >=5 paired instruments minima (or explicit ex-ante infeasibility rule), block-bootstrap CI spec, materiality threshold (>=2% where applicable), missingness/inclusion rules, input provenance/checksums, git HEAD, freeze timestamp. **No outcome inspection first.**
2. **Bounded first-time unauthenticated acquisition (missing inputs only):** For prereg-specified coins/months lacking candles, fetch Hyperliquid `candleSnapshot` 1h and cache under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` with `.accessed.json` provenance and `.sha256` (endpoint, params, access UTC, status, checksums/sizes, unauthenticated/no-key/no-requester-pays/signature status). Candidate months ~2025-11..2026-04 per confirmed overlap. **Do NOT re-fetch 2026-05..2026-10.**
3. **Build deterministic RV-augmented panel from cached inputs:** emit `research_state/tracka_hl_early_panel_<UTC>.parquet` and build report JSON/MD with hashes, coverage, leakage/embargo notes, symbol-month completeness, observed-label provenance.
4. **Run pre-registered evaluation only after (1)-(3):** compute contrasts/splits per prereg; emit `research_state/evaluation_summary_TRACKA-HL-early-<UTC>.md` with verdict (MET/NOT_MET/INADMISSIBLE per prereg), bootstrap CIs, gate checks.
5. **Update state atomically:** append/update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum; preserve 2024 H001 and prior Track A records). Keep sealed records immutable.
6. **If infeasible under prereg minima:** emit a concrete infeasibility artifact citing exact evidence (coverage gaps, block/instrument shortfall), update state to record infeasibility, then pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (new prereg with frozen ex-ante symbol selection/event-adequacy rules; bounded first-time acquisition as needed) and execute same prereg→build→eval discipline.

**Secondary (only after Track A candidates exhausted with documented evidence):** `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` on admissible untested Hyperliquid data, pre-registered before outcomes, no Track C/Gate 4/2024 Binance conflation.

---

## Hard bans (binding)
- No outcome inspection before freeze/preregistration for any new claim.
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed (Track A = observed ironflow or equivalent with provenance).
- No threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C).
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance allowed/required where specified).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no bypass of Gate 4 human/legal terms.
- **No status-only output:** every session must leave a substantive artifact (prereg/fetch-manifest/panel/eval or documented infeasibility + state updates).

## Key refs
- Handoff/campaign: `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`
- Gap audit: `research_state/next_panel_gap_audit_20261111T163229Z.md|.json`
- Track A (closed template/artifacts): `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`, `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`, `scripts/tracka_hl_*`
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`
- Checks: `python -m unittest discover -s tests -v` (as relevant)

**End of Handoff — Execute INITIAL TASK MESSAGE now: Branch 1 if Gate 4 resolved, else Branch 2 heavy campaign (`GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1`).**
