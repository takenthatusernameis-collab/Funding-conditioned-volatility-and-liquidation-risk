# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T21:06:15Z
**Status:** AUTHORITATIVE. Execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are pointers/redirects. Ignore conflicting or stale docs.

## INITIAL TASK MESSAGE (EXECUTE NOW)
**Mission (repo-prioritized):** Advance funding-conditioned **liquidation-risk forecasting** and co-priority **volatility forecasting** on admissible, unauthenticated, provenance-backed data. Do **not** idle, do **not** produce status-only output, and do **not** relitigate closed work. Execute the first applicable heavy-work branch below and leave substantive artifacts plus consistent state updates.

**Verified entry state (2026-11-11T21:06:15Z):**
- **Gate 4 / Branch 1:** BLOCKED (external, human/legal). `research_state/fclr016_local_audit/` contains no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (present: `..._BLOCKED_20261108T014835Z.json`, `..._UNRESOLVED_20261108T204000Z.json`, `fabricated=false`). Do **not** set `RESOLVED_VERIFIED`/`fabricated=true` or bypass terms.
- **Track A (closed/recorded, do not relitigate or retune):**
  - `TRACKA-HL-S-20261111T133430Z` 2026-05..2026-10 9-symbol successor **NOT_MET** (`research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`).
  - `TRACKA-HL-EARLY-20261111T191958Z` / `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` **INADMISSIBLE** (`research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`).
  - `TRACKA-HL-EXPANSION-20261111T195500Z` / `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` **PASS** on pre-registered primary gate (C2 vs B1, QLIKE next-24h observed Hyperliquid liquidation intensity, 2026-05..2026-10, ex-ante 8 symbols ZEC,NEAR,UNI,AAVE,CRV,ADA,LTC,BCH; rel reduction 19.04%, 95% CI [-5.088,-0.478], 593 pairs, 8 instruments, 3 blocks). See `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md` and linked panel/build artifacts.
- **Track B/C (2024):** closed negative; sealed holds immutable (H001 NOT_SUPPORTED and prior 2024 records preserved).
- **Cached admissible assets:** ironflow observed labels 2025-05..2026-10 (432 PERP markets), Hyperliquid funding/candles for 9 original + 8 expansion coins and related caches under `research_state/data_cache/` with provenance where recorded. Reuse cache-first; verify coverage before any fetch.

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH

### Branch 1 (CONDITIONAL — only if trigger appears now)
**Trigger:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
**Actions (deterministic, in order):** run promotion/admissibility validators (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or equivalents) with required `--expect-go`; only on all-green GO execute confirmatory Track C multi-split ablation on frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds); emit verdict(s) and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If absent (current):** proceed to Branch 2.

### Branch 2 (DEFAULT, MANDATORY NOW): `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS`
**Goal:** Advance **funding-conditioned volatility forecasting** on an admissible, untested Hyperliquid/cache-backed panel (co-priority with liquidation risk). Expansion liquidation PASS is recorded; do not rerun/retune it. Pursue new pre-registered evidence for volatility on data not sealed/closed by prior negative 2024 Track B/C/FCLR-002/003 claims, with no Binance/2024 conflation.

**Execute in order (substantive artifacts required):**
1. **Select & preregister before outcomes (frozen).** Audit cached admissible inputs (Hyperliquid funding + candles + any admissible targets available locally) and define a NEW volatility-forecast claim on an untested panel/window/symbol set (distinct from sealed 2024 holds). Emit `research_state/tracka_prereg_volatility_<UTC>.json|.md` freezing: hypothesis/claim, venue/source, exact panel universe/window, target (e.g. next-period realized volatility derived causally from cached marks/candles), features (RV-only baseline B1 vs funding-conditioned C2 as appropriate), splits/embargo (>=7d), test blocks/instruments minima, metric/materiality/CI, event/coverage adequacy, and infeasibility rule. **No outcome inspection before prereg freeze.**
2. **Bounded acquisition only if needed.** If required Hyperliquid inputs are missing for the preregistered panel, perform bounded first-time unauthenticated fetches with provenance (`.accessed.json` + `.sha256`) and cache-first checks; do not re-fetch already-valid cached data. Emit acquisition/gap report.
3. **Build deterministic panel.** Construct causal features/targets from admissible cached data; emit panel + build report with hashes, coverage, leakage/embargo notes, symbol-period completeness. **No outcome computation beyond what build requires; evaluation only after build complete per prereg.**
4. **Run pre-registered evaluation.** B1 vs C2 (or prereg contrasts) on volatility target with block bootstrap CIs, embargo, and pre-registered minima/materiality. Emit `research_state/evaluation_summary_TRACKA-VOL-<UTC>.md` with verdict **MET / NOT_MET / INADMISSIBLE** and full evidence.
5. **Update state atomically.** Append/update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum; preserve 2024 H001 and all prior Track A/B/C records, including expansion PASS). Keep sealed records immutable.
6. **If infeasible under prereg minima:** emit concrete infeasibility artifact with exact evidence (coverage gaps, <min instruments/blocks, target not computable), update state, then preregister and attempt the next best admissible untested volatility/liquidation claim in-session (same discipline) so substantive progress continues.

## HARD BANS (BINDING)
- No outcome inspection before freeze/prereg; do not run forecast eval before panel/build complete per prereg.
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed.
- No threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C).
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance allowed where specified).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no Gate 4 human/legal bypass.
- **No status-only output:** every session must leave a substantive artifact (prereg/acquisition/panel/eval or documented infeasibility + state updates).

## Key refs
- Handoff (authoritative): `HANDOFF_NEXT_SESSION.md`
- Pointers: `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md`
- Expansion PASS: `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`, `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`, `research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json`
- Prior Track A: `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md` (NOT_MET), `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md` (INADMISSIBLE)
- Scripts: `scripts/tracka_hl_*`, admissible data utilities under `scripts/`
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`

**Execute now:** Branch 1 only if Gate 4 RESOLVED trigger is present now; otherwise Branch 2 (`GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS`) — start at frozen preregistration for an untested admissible volatility claim before any outcome inspection.
