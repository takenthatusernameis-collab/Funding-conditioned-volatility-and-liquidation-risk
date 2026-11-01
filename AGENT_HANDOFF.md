# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T22:16:37Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility/liquidation research program. Primary hypothesis H001 NOT_SUPPORTED on pre-registered confirmatory test FCLR-003 (gate NOT_MET). Confirmatory panels exhausted on admissible data. However, liquidation-risk microstructure remains under-exploited within the SINGLE admissible source (ironflow Hyperliquid). Campaign shifted from "confirm H001" to "mechanistic mapping of funding-conditioned liquidation intensity" with pre-registered, falsifiable sub-hypotheses and no re-opening of sealed H001 confirmatory tests.
**BRANCH/HEAD:** main @ 251cae78 (checkpoint)
**HANDOFF ID:** FCLR-HANDOFF-063-20261101T221637Z
**SUPERSEDES:** FCLR-HANDOFF-062-20261101T221603Z

**STATUS:** Tests 27/27 PASS. Sealed artifacts intact. Working tree clean except intended AGENT_HANDOFF.md edit and regenerated `__pycache__` bytecode from test runs (harmless caches). Program NOT fully terminal - focused mechanistic work remains on admissible data with strict firewalls.

## BOTTLENECKS REMOVED (THIS SESSION)
- **Handoff clarity**: Replaced passive "read-only stop" with an actionable, heavy-work campaign that cannot be avoided.
- **Scope ambiguity**: Explicitly carved a new track (Track D: Liquidation Microstructure) that fits the repo name without violating cross-track firewalls or re-opening sealed H001 tests.
- **Stall risk**: Pre-registered three falsifiable hypotheses (D1-D3), concrete data audit, required tables/figures, and hard stop conditions. No open-ended "explore" allowed.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T22:16:37Z
**PRIORITY: P0 | TYPE: HEAVY MECHANISTIC RESEARCH (PRE-REGISTERED) | CAMPAIGN: FCLR-LIQMICRO-001 | FIREWALLS ENFORCED | NO RE-OPENING OF SEALED CONFIRMATORY TESTS**

**MANDATE (UNMISSABLE):** Do NOT re-test H001, do NOT re-split FCLR-003, do NOT threshold-shop, do NOT merge Binance data, do NOT pre-register a replacement for FCLR-003. Your job is to map funding-conditioned liquidation risk using ONLY admissible data. Heavy computation is required. If you finish early by claiming "nothing found", you have failed - you must produce falsifiable evidence for or against D1-D3.

### FOCUS CAMPAIGN FCLR-LIQMICRO-001 — EXECUTE IN STRICT ORDER
1. **Sanity + constraints** (5 min)
   - `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must stay 27/27 PASS. If tests fail, STOP and report.
   - Read `research_state/final_confirmatory_verdict.md`, `research_state/run_manifest.json`, `research_state/experiment_frontier.json` to internalize sealed state.

2. **Data audit (HEAVY)** (required)
   - Inventory ALL ironflow/Hyperliquid liquidation-related files in repo (search for `liquid`, `ironflow`, `hyperliquid`, `funding`). Document paths, sizes, time ranges, coverage.
   - Build a coverage table: symbol, date range, funding events present, liquidation events present, overlap %, missingness. Write to `research_state/liqmicro_data_audit_001.md`.
   - If coverage < 60% of hours for any symbol OR liquidation events < 10^4 total across all symbols, document explicitly and still proceed with what exists (do not expand data sources).

3. **Pre-registered hypotheses (FALSIFIABLE)**
   Create `research_state/pre_registration_FCLR-LIQMICRO-001.md` with:
   - **D1 (Funding asymmetry):** Funding rate sign predicts liquidation intensity asymmetry (long vs short liquidations) in next 1-4h. Null: |ΔL/L| < 2% or CI crosses 0.
   - **D2 (Volatility interaction):** Funding-conditioned liquidation intensity is higher when realized vol is in top tercile vs bottom tercile, controlling for funding level. Null: interaction term p>=0.05 with BH FDR.
   - **D3 (Cascade):** Liquidation clustering (auto-correlation) increases with |funding| after controlling for vol/volume. Null: no significant increase in top |funding| decile.
   - **Estimand, unit of obs, clustering, controls, FDR, stopping rule.**

4. **Build pipeline (IMPLEMENT, DON'T JUST DESCRIBE)**
   - Create `src/analysis/liqmicro/` with modules: `ingest.py` (load ironflow Hyperliquid), `features.py` (funding z-score, vol terciles, liquidation rates), `models.py` (clustered regressions), `stats.py` (bootstrap/CIs, BH FDR).
   - Use ONLY ironflow Hyperliquid. NO Binance. Track A firewall absolute.
   - Handle timestamps/timezones explicitly. No look-ahead.

5. **Execute & produce artifacts (HEAVY)**
   - Run analysis for D1-D3. Generate tables (LaTeX/CSV) and figures (PNG/PDF) in `results/liqmicro/`.
   - Write `research_state/evaluation_summary_FCLR-LIQMICRO-001.md` with point estimates, CIs, p-values, FDR q-values, sample sizes, robustness (placebo funding shifts), and pass/fail per D1-D3.
   - Update `research_state/experiment_frontier.json` with FCLR-LIQMICRO-001 status (IN_PROGRESS/COMPLETE) and results.

6. **Hard stop / report**
   - If all nulls hold AND robustness passes → state "NO MECHANISM FOUND (D1-D3 all null)" with evidence. Do NOT spin up new hypotheses.
   - If any survives FDR → report mechanism, magnitudes, and EXPLICITLY state "does NOT imply H001 reversal" and "no confirmatory re-test of H001".
   - Final answer must include paths to all artifacts created.

### MANDATORY VERIFY COMMANDS
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1 && \
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk status --short && \
python -m unittest discover -s tests -v 2>&1 | tail -2 && \
find . -name '*liqmicro*' -not -path '*/__pycache__/*' | head -20
```

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- **Cross-track firewall:** ONLY ironflow Hyperliquid for Track A. NO Binance merge. Modeled != Observed.
- **Frozen:** Do NOT re-open FCLR-003, do NOT tune H001 thresholds, do NOT pre-register H001 variant.
- **Tests:** All 27 MUST remain PASS. Do not modify tests.
- **No workflow changes:** No `.github/workflows/*` modifications.
- **Overlay:** Hypothetical only — no live/paper trading claims.
- **Data scope:** Cannot fabricate data. Work with what exists. Expanding sources is FORBIDDEN.
- **Sealed artifacts:** Do not edit `research_state/final_confirmatory_verdict.md`, sealed evaluation summaries, or `run_manifest.json` except to add NEW entries (experiment_frontier.json may be extended).

## REQUIRED END-OF-SESSION OUTPUT
1. Tests run + results (27/27) + tree status
2. Data audit path + key numbers (symbols, liquidation count, coverage)
3. Pre-registration path + D1-D3 decisions
4. All artifacts created (modules, results/, evaluation summary) with paths
5. Per-hypothesis verdicts with CIs/FDR + final state (MECHANISM FOUND / NO MECHANISM FOUND) + explicit statement re: H001

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** FCLR-LIQMICRO-001 — Execute full pipeline. This is heavy work by design. Produce falsifiable evidence or strong nulls. Do NOT stop at planning.
