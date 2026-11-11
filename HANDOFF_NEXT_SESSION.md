# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION (INITIAL TASK MESSAGE)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T23:37:42Z
**Status:** AUTHORITATIVE. Execute this file only. Treat `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` as redirects to this file.

## INITIAL TASK (EXECUTE IMMEDIATELY — HEAVY WORK, NO STATUS-ONLY)
**Priority (inferred from repo name):** Advance **funding-conditioned volatility forecasting** on an admissible, **untested** Hyperliquid panel (liquidation-risk co-priority only where admissible). Produce substantive artifacts + atomic state updates this session. **Do not idle, do not relitigate closed/sealed results, do not output status-only.**

### Bottlenecks — status and removals (act, do not wait)
| Bottleneck | Status | Action now |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | **BLOCKED, not agent-removable** | Act only if `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with all required fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation → run Branch 1 deterministically (promotion + `--expect-go` validators → on all-green GO run confirmatory Track C multi-split ablation, verdict, atomic state updates). **Verified absent now** (only `_BLOCKED`/`_UNRESOLVED`/`_partial`). Never guess, never set `fabricated=true`, never bypass. Do not wait — proceed to Branch 2. |
| No frozen prereg for untested admissible **funding-conditioned volatility** claim | **REMOVABLE NOW — primary blocker** | **Execute Branch 2 Step 1 immediately:** freeze a new volatility prereg before any outcome computation, then build+evaluate+update state in-session. |
| Data for core volatility panel | **REMOVED (cache available)** | `research_state/data_cache/hyperliquid_candles/` (17 coins: AAVE,ADA,AVAX,BCH,BNB,BTC,CRV,DOGE,ETH,LINK,LTC,NEAR,SOL,SUI,UNI,XRP,ZEC; months 2025-11..2026-10 cached) and `research_state/data_cache/hyperliquid_funding/` (same 17 coins, ~2025-11..2026-10 JSON) are present. Cache-first audit; no redundant polling. Bounded first-time unauthenticated fetches only if strictly required by frozen prereg, with `.accessed.json` + `.sha256`. |
| Ironflow observed liquidation labels (optional/context) | **Present for 2025-05..2026-10** | `research_state/data_cache/ironflow_events/` (2025-05..2026-10). Use only if explicitly needed by a frozen admissible claim and as observed labels only. |

## FOCUS CAMPAIGN (MANDATORY) — `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS`
**Default branch now = Branch 2.** Execute in strict order. **No outcome inspection before prereg freeze.** Heavy work required in-session.

### Step 1 — Freeze volatility prereg (REQUIRED, before outcomes)
Create `research_state/tracka_prereg_volatility_<UTC>.json` and matching `.md` (or a scriptable prereg JSON sufficient for deterministic execution) **before inspecting any forecast outcomes**. Must include:
- New hypothesis id (e.g. `H_tracka_hl_volatility_forecast_<UTC>`) distinct from sealed/closed H1, Track B/C, and Track A liquidation claims.
- Venue/source: `hyperliquid_perpetuals` only. **No Binance/2024 conflation.**
- Estimand: next-24h realized **volatility** (or realized variance, consistently defined) computed causally from 1h mark-price candles — a **distinct estimand** from closed Track A liquidation-intensity claims. State formula and computability preconditions.
- Panel inputs: cached admissible Hyperliquid candles + funding (17 cached coins; 2025-11..2026-10 all cached for candles). Observed ironflow labels only if explicitly needed and admissible; **no modeled/proxy/synthetic liquidation labels**.
- Universe/symbol selection rule **ex ante** (frozen here). Candidates: the 17 cached-coin universe or a justified subset with explicit frozen inclusion/exclusion rule (event/coverage adequacy, not outcome-based). Minima: **>=5 paired instruments**, RV computable, funding coverage sufficient.
- Primary contrast: **B1 (RV-only baseline)** vs **C2 (funding-conditioned)** (or justified prereg alternative). Metric **QLIKE** (pre-registered, lower-better or clearly specified). Materiality: **>=2% relative reduction** AND **95% block-bootstrap CI** supporting improvement (excludes zero in favor of C2) as applicable.
- Splits: chronological with **>=7-day embargo**, **>=3 non-overlapping 30-day test blocks**. Define train/val/test or test-block scheme explicitly; seed for bootstrap.
- Hard infeasibility rule: if minima (symbols/blocks/RV/funding) cannot be met on admissible cached data after deterministic build, verdict **INADMISSIBLE** with concrete evidence.
- Forbidden actions: no outcome peeking, no threshold-shopping, no sealed-holdout reuse, no prereg changes after outcomes inspected.

### Step 2 — Bounded acquisition (only if missing)
Cache-first audit. Fetch only strictly required missing inputs with provenance + acquisition/gap report (`.accessed.json` + `.sha256` as applicable). Do not re-fetch complete cached months/coins. No redundant network polling.

### Step 3 — Deterministic panel build
Emit `research_state/tracka_vol_panel_<UTC>.parquet` (or documented equivalent) + `research_state/tracka_vol_panel_build_report_<UTC>.json` (hashes, coverage by symbol/period, embargo/leakage notes, RV/funding completeness). All features causal/trailing-only. **No evaluation before panel matches prereg.**

### Step 4 — Pre-registered evaluation
Run B1 vs C2 per prereg (bootstrap seed/CI, minima/materiality). Emit `research_state/evaluation_summary_TRACKA-VOL-<UTC>.md` with verdict **MET / NOT_MET / INADMISSIBLE** and full evidence (n, instruments, blocks, point estimates, CI, relative reduction, gate pass/fail per criterion).

### Step 5 — Atomic state update (MANDATORY)
Update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, and append addendum to `research_state/final_confirmatory_verdict.md`. Preserve all sealed/closed records; **never mutate closed verdicts**. Record new experiment id, prereg path, artifacts, verdict.

### Step 6 — If INADMISSIBLE — do NOT stop
Emit concrete infeasibility artifact with exact evidence, update state, then **immediately preregister and execute the next best admissible untested volatility (or liquidation) claim** in-session with Steps 1–5. Continuous heavy work until a claim-worthy evaluation is completed or all admissible cached routes are exhausted with documented evidence.

## COMPLETED / SEALED (DO NOT REOPEN OR RETUNE)
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (C2 vs B1 rel QLIKE reduction 19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10, symbols AAVE/ADA/BCH/CRV/LTC/NEAR/UNI/ZEC). Sealed; do not rerun/retune.
- Track A 9-symbol 2026-05..2026-10 = **NOT_MET** (closed). Track A early 2025-11..2026-04 = **INADMISSIBLE** (closed, candle gap documented).
- Track B/C 2024 and H1/FCLR-002/003 sealed/closed negative contexts remain immutable. H1 primary remains NOT_SUPPORTED on its tested panels.

## HARD BANS (BINDING)
- No outcome inspection before freeze/prereg. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue/source must match artifacts (Hyperliquid-only for this campaign).
- No modeled/proxy/synthetic liquidation labels presented as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Deliver prereg + (build+eval or documented infeasibility + pivot attempt) + state updates.

## KEY REFS
- Caches: `research_state/data_cache/hyperliquid_candles/` (17 coins, 2025-11..2026-10), `research_state/data_cache/hyperliquid_funding/` (17 coins, ~2025-11..2026-10), `research_state/data_cache/ironflow_events/` (2025-05..2026-10)
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`
- Gate 4 audit dir: `research_state/fclr016_local_audit/` (no valid `fclr016_v5_terms_evidence_RESOLVED_*` at handoff time)
- Patterns/scripts: `scripts/tracka_hl_build_panel_with_rv.py`, `scripts/tracka_hl_evaluate_successor.py`, `scripts/run_volatility_funding_eval.py`, `scripts/run_gate4_v4_exploratory_diag.py`, `src/volatility/features_ext.py`, `src/volatility/eval.py`, `src/volatility/block_bootstrap.py`
- Prior prereg templates: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`, `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`

**Execute now:** Branch 1 only if valid Gate 4 RESOLVED trigger present; otherwise begin **Branch 2 Step 1 — freeze volatility prereg** immediately and carry through Steps 2–5/6 in this session.

(End of file - total 66 lines)