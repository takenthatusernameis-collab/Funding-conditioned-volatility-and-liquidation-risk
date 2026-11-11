# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T21:10:42Z
**Status:** AUTHORITATIVE. Execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are pointers/redirects. Ignore conflicting/stale docs.

## INITIAL TASK MESSAGE (EXECUTE NOW — NO STATUS-ONLY)
**Mission (repo-prioritized):** Treat **funding-conditioned volatility forecasting** as the PRIMARY heavy-work target (repo name first). Co-priority: liquidation-risk where admissible. Do **not** idle, do **not** relitigate closed work (Track A 9-symbol NOT_MET, Track A early INADMISSIBLE, Track B/C negative/sealed). Produce substantive artifacts + atomic state updates every pass.

**Bottlenecks to remove now (concrete):**
- **Gate 4 (external/legal):** BLOCKED. Do **not** guess/attest `RESOLVED_VERIFIED` or set `fabricated=true`. Only proceed if `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation — then run Branch 1 deterministically. Otherwise skip.
- **Volatility gap:** H1_primary NOT_SUPPORTED on sealed panels; Track B modeled only and exhausted. No frozen prereg for an **untested admissible** funding-conditioned volatility claim exists yet. This is the clearest path to real progress given expansion liquidation PASS is already recorded.
- **Avoid redundant work:** reuse `research_state/data_cache/` (Hyperliquid funding/candles, ironflow). Only bounded first-time unauthenticated fetches with `.accessed.json` + `.sha256` if strictly required by a frozen prereg.

## MANDATORY CAMPAIGN: `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (START IMMEDIATELY)
Execute in strict order. **No outcome inspection before prereg freeze.**

### Step 1: Freeze volatility prereg (BEFORE outcomes) — REQUIRED ARTIFACT
Create `research_state/tracka_prereg_volatility_<UTC>.json` and `.md` freezing:
- **Claim/hypothesis:** new `H_tracka_hl_volatility_forecast_*` (distinct from sealed). Explicitly state "no Binance/2024 conflation", venue `hyperliquid_perpetuals`, observed-only where applicable.
- **Panel:** choose **untested** universe/window using cached admissible data (Hyperliquid candles/funding). Prefer symbols not exhausted by closed liquidation campaigns or with clean coverage. If using liquidation labels, only use observed ironflow labels with provenance; do **not** fabricate/model labels.
- **Target:** e.g. next-24h realized volatility (from cached 1h candles: RV over window derived causally; define formula, no leakage). State computability preconditions.
- **Features/splits:** B1 (RV-only) vs C2 (funding-conditioned) or prereg contrast. Chrono splits with **>=7d embargo**. >=3 non-overlapping 30d test blocks, >=5 paired instruments if possible (or justify minima).
- **Gates/materiality:** metric (e.g. QLIKE or pre-registered), min rel improvement/materiality, CI (block bootstrap), event/coverage adequacy, **hard infeasibility rule**.
- **Forbidden:** threshold-shopping, sealed-holdout reuse, outcome peeking.

### Step 2: Bounded acquisition (only if gaps)
Check caches first. If any required series missing for prereg panel, do bounded first-time unauthenticated fetches with provenance; log to acquisition report. Do not poll/re-fetch cached valid data.

### Step 3: Deterministic panel build
Build causal features/targets from cached data. Emit `research_state/tracka_vol_panel_<UTC>.parquet` + `research_state/tracka_vol_panel_build_report_<UTC>.json` with hashes, coverage by symbol/period, embargo/leakage notes. **Do not run evaluation until build complete and matches prereg.**

### Step 4: Pre-registered evaluation
Run B1 vs C2 per prereg with block bootstrap CIs, embargo, minima. Emit `research_state/evaluation_summary_TRACKA-VOL-<UTC>.md` with verdict **MET/NOT_MET/INADMISSIBLE** and full evidence.

### Step 5: Atomic state update (MANDATORY)
Update atomically: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum). Preserve all sealed records (H001, Track A NOT_MET, Track A early INADMISSIBLE, Track B/C). Never mutate closed verdicts.

### Step 6: If INADMISSIBLE — do NOT stop
If infeasible under prereg minima, emit concrete infeasibility artifact with exact evidence, update state, **immediately preregister next best admissible untested volatility (or liquidation) claim in-session** with same discipline and execute Steps 1-5. The goal is continuous heavy work, not a status report.

## HARD BANS (BINDING)
- No outcome inspection before freeze/prereg.
- No Binance/2024 conflation; venue/source must match artifacts.
- No modeled/proxy/synthetic liquidation labels as observed.
- No threshold-shopping; no sealed-holdout reuse.
- No `.github/workflows` edits.
- No redundant network polling.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must leave substantive artifact(s) + consistent state updates.

## KEY REFS
- Expansion PASS (liquidation): `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`, panel/build artifacts under `research_state/`
- Closed Track A: `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md` (NOT_MET), `research_state/evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md` (INADMISSIBLE)
- Caches: `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`, `research_state/data_cache/ironflow_events/`
- Gate 4: `research_state/fclr016_local_audit/` (+ validators `scripts/fclr016_v5_*`)
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`

**EXECUTE NOW:** Branch 1 only if Gate 4 RESOLVED trigger present now; else **Branch 2** starting at Step 1 (frozen volatility prereg) before any outcome inspection. Force heavy work across the full campaign.
