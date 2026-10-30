# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T05:15:00Z
HEAD: 7a1debef (main, origin/main)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## PRIORITY (repo name): LIQUIDATION RISK — FCLR-005 / H004 TRACK A IS THE ONLY PATH FORWARD

The repository name is "Funding-conditioned-volatility-and-liquidation-risk". Observed liquidation risk (FCLR-H004 / Track A) is the namesake priority. All other forecast gates (FCLR-001–004) are SEALED (NOT_MET/BLOCKED). Do NOT re-run them. Do NOT build risk overlays/simulations/merges. Do NOT touch .github/workflows/.

## BOTTLENECKS REMOVED (enforced — do not re-open)

- **Source discovery**: Bybit census via HuggingFace `ochinimus/crypto-liquidation-ticks` (CC BY 4.0, unauthenticated) is admissible and verified. All 2024 liquidation routes exhausted and recorded (Binance archives/API 404/451, Bybit/OKX/Deribit no census, HF/Zenodo/GitHub dead ends). Do NOT re-probe without concrete new evidence.
- **Feature cache**: 2026 feature cache VERIFIED COMPLETE on disk — mark/index/premium klines 1h + monthly fundingRate for 2026-04-01..2026-08-06 present under `research_state/data_cache/<SYM>_2026_*/` (extracted CSVs confirmed). `research_state/data_cache/liquidations_full_20260807.csv` verified via `scripts/h004_audit.py` (1,442,664 rows; bybit=346,269 / okx=236,896 / binance=859,499; target symbols present). `scripts/h004_complete_cache.py` NOT needed — do not re-run.
- **Protocol frozen**: `research_state/research_protocol_fclr005.md` (FCLR-005 v1.0) frozen before outcome inspection. Do NOT change targets/features/splits.
- **Capped != census; absence != zero**: Bybit rows = census arm only. Binance/OKX = undercounted lower-bound only. Never infer event-free intervals from missing data.

## SINGLE TIMESTAMPED INITIAL TASK — CAMPAIGN H004-20261030T051500Z (HEAVY WORK, MANDATORY, NO ESCAPE HATCH)

> **[2026-10-30T05:15:00Z] CAMPAIGN: BUILD AND EXECUTE FCLR-005 END-TO-END — TRACK A OBSERVED LIQUIDATION OUTCOMES ON THE 2026 BYBIT CENSUS**

**Binary outcome required:** Produce either (a) `research_state/evaluation_summary_FCLR005.md` with exact numbers for B0/B1/C1/C2 (Brier, log-loss, calibration slope/intercept, precision-recall, AUPRC), base rate/event prevalence, coverage gaps, leave-one-symbol-out stability, block-bootstrap uncertainty, and an honest PILOT/EXPLORATORY verdict (the ~30-day label window cannot meet the >=3-block confirmatory gate — do NOT claim confirmatory skill), OR (b) a concrete, evidence-backed blocker with the exact failing step and what is missing.

**Network:** Reachable. Unauthenticated downloads/probes are allowed. Do NOT use "no network" as an excuse.

### HEAVY WORK (DO ALL IN ORDER — NO SHORTCUTS)

1. **Absorb context (mandatory):**
   - `research_state/research_protocol_fclr005.md` (read completely, treat as frozen)
   - `research_state/fclr_h004_tracka_viable.json`
   - `research_state/liquidation_sources_enumeration.md` (§1-4, §84-92)
   - `research_state/binance_source_probe.md`
   - `research_state/hypothesis_registry.json` (FCLR-H004)
   - `AGENT_HANDOFF.md` (this file)

2. **Verify cache completeness (confirm only):**
   - Confirm all 5 symbols have extracted mark/index/premium 1h klines and monthly fundingRate CSVs for 2026-04-01..2026-08-06 under `research_state/data_cache/<SYM>_2026_*/`
   - Confirm `research_state/data_cache/liquidations_full_20260807.csv` exists. If unsure, run `python scripts/h004_audit.py` once.

3. **Build the Track A pipeline (CREATE NEW SCRIPT — HEAVY WORK):**
   Create `scripts/h004_fclr005_pipeline.py` that is idempotent, checkpoint-resumable, and deterministic (fixed seed). It MUST:
   - Load Bybit liquidation rows from `liquidations_full_20260807.csv` ONLY for the census arm (exchange == 'bybit'). Never use Binance/OKX to construct the binary presence/absence target.
   - Merge with Binance 2026 features (mark/index/premium klines 1h + funding) at hourly UTC granularity for symbols {BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT}.
   - Construct hourly targets: event count and USD notional intensity for long_liquidated and short_liquidated separately. Treat hours with zero Bybit rows as "observed zero in census arm only" — NEVER infer "no liquidations" from missing data.
   - Compute frozen predictors per `research_state/research_protocol_fclr005.md` §3 (RV1h/RV24h/RV168h, signed funding, |funding| percentile over trailing 90d with >=30 obs, mark/index premium, mark/EMA24 distance). No forward-fill, no zero-fill across splits.
   - Enforce chronological train/val/test split within 2026-07-08..2026-08-06 with embargo/purge. Explicitly record that window length < 3x30d blocks.
   - Implement B0 (persistence), B1 (RV-only), C1 (+funding), C2 (+price). Fixed logistic form, no hyperparameter search, no threshold tuning on outcomes.
   - Run block bootstrap (over complete UTC hours), leave-one-symbol-out stability, deterministic seed. Compute Brier, log-loss, calibration slope/intercept, precision-recall, AUPRC.
   - Write intermediate checkpoints (e.g., `research_state/.cache/fclr005_*.parquet` or JSON) to resume without recomputing.
   - Log all row counts, merges, drops, and coverage gaps.

4. **Execute evaluation (RUN THE PIPELINE):**
   Run `python scripts/h004_fclr005_pipeline.py` to completion. Do not stop early. If it fails, fix the script (not the protocol) and resume from checkpoints.

5. **Forensic logging (MANDATORY):**
   Append a dated execution record to `research_state/liquidation_sources_enumeration.md` with UTC timestamp, script run, git SHA, rows merged by (exchange,symbol), symbol coverage, label window used, train/val/test boundaries, sample counts, events per hour stats, drops, and checkpoint paths.

6. **Write deliverables & update state:**
   - `research_state/evaluation_summary_FCLR005.md` — exact numbers, base rates, prevalence, coverage gaps, block counts, bootstrap CIs where computed, leave-one-symbol-out, and explicit PILOT/EXPLORATORY verdict stating cannot meet >=3-block confirmatory gate and FCLR-H004 remains BLOCKED for frozen 2024.
   - `research_state/hypothesis_registry.json` — update FCLR-H004 status to PILOT_ONLY/EXPLORATORY_ONLY for 2026 window with evidence links to the new summary and protocol; keep BLOCKED for frozen 2024.
   - `research_state/run_manifest.json` — append/update with run_id, git SHA, config hash, data hashes (liquidations_full_20260807.csv + feature files used), UTC start/end, sample counts, results status, blocker state.
   - `AGENT_HANDOFF.md` — update with precise next actions and any new blockers.

### HARD CONSTRAINTS (NON-NEGOTIABLE)
- No credentials, paid services/trials, manually supplied keys/files, user intervention. No bypassing auth/rate limits/terms.
- No forecast gate re-runs (FCLR-001–004 sealed). No .github/workflows changes. No trading/risk-overlay/simulation/merge tracks until a forecast gate passes.
- Observed (Track A) != modeled (Track B) != volatility-only (Track C). Capped sample != census. Absence != zero. Event-free intervals may NEVER be inferred from missing data.
- Bybit = census arm only. Binance/OKX = lower-bound partial evidence only (never census, never binary absence/presence target).
- Do NOT change `research_protocol_fclr005.md`. Do NOT threshold-shop. Do NOT claim confirmatory skill.
- Commit nothing merely to show activity.

### VERIFICATION GATES (MUST PASS BEFORE STOPPING)
- `python -m unittest tests.test_funding_correction_replication -v` → 10/10
- `python scripts/h004_audit.py` → liquidations_full_20260807.csv schema/coverage confirmed
- `research_state/liquidation_sources_enumeration.md` grew monotonically with FCLR-005 execution record (appended this session)
- `scripts/h004_fclr005_pipeline.py` exists, is idempotent/resumable, and ran to completion
- `research_state/evaluation_summary_FCLR005.md` exists with exact numbers + honest PILOT/EXPLORATORY verdict + explicit statement about <3 blocks
- `research_state/hypothesis_registry.json` and `research_state/run_manifest.json` updated with evidence links

**START NOW. HEAVY WORK ON FCLR-005 / H004 TRACK A. Liquidation risk is the repo's namesake priority — this is the only liquidation path forward.**
