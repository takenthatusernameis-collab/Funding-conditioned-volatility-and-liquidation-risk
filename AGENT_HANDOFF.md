# AGENT_HANDOFF.md (DURABLE)
**TIMESTAMP (UTC):** 2026-10-31T23:40:18Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** (inspect at session start)
**HANDOFF ID:** FCLR-HANDOFF-20261031T234018Z
**PRIORITY:** HEAVY WORK - DATA PIPELINE FIRST

## 1) WHAT CHANGED & WHY
- **Baseline established:** Repository contains large ZIP sets of public Binance data (funding rates, klines, mark/index/premium/indexPriceKlines) for BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT covering 2024-01 through 2024-03. No `AGENT_HANDOFF.md`, `research_state/` artifacts, or obvious research pipeline code were present at inspection.
- **Bottleneck identified:** With explicit heavy data already present locally, the highest ROI action is to convert raw archives into a restartable, leakage-resistant dataset and freeze the FCLR-001 protocol before any "analysis" passes. Avoid documentation-only sessions.
- **Campaign initialized:** This handoff forces a data-first campaign (ingest → validate → features/labels → baseline) with concrete verifiable acceptance tests.

## 2) CURRENT STATE SNAPSHOT (EVIDENCE)
**Present data (high-signal):**
- Funding: `BTCUSDT-fundingRate-2024-01/02/03.zip`, `ETHUSDT-fundingRate-*.zip`, `SOLUSDT-fundingRate-*.zip`, `XRPUSDT-fundingRate-*.zip` (+ extracted dirs)
- Spot/contract klines: `*USDT-1h-YYYY-MM-DD.zip` (Jan-Mar 2024)
- Reference: `klines-1h-*`, `markPriceKlines-1h-*`, `indexPriceKlines-1h-*`, `premiumIndexKlines-1h-*` for overlapping dates

**Missing (must create):**
- `research_state/research_protocol.md` (FCLR-001 frozen)
- `research_state/data_source_registry.json`
- `research_state/run_manifest.json`
- `research_state/hypothesis_registry.json`
- `research_state/evaluation_summary.md` (empty/placeholder until computed)
- `research_state/negative_results_report.md`
- `research_state/leakage_audit.md`
- `scripts/` ingestion/feature code (tested)
- `tests/` fixtures for timestamp/split/embargo checks

## 3) SINGLE HIGHEST-VALUE NEXT TASK (DO THIS FIRST)
**TASK ID:** FCLR-T001 | **TYPE:** HEAVY ENGINEERING + DATA
**GOAL:** Build a restartable ingestion path for BTCUSDT (MVP) that unzips/reads funding + mark/index/klines, normalizes to UTC hourly, produces a validated panel, and freezes FCLR-001 protocol.

**WHY:** Repo name prioritizes funding-conditioned volatility/liquidation risk. Data is local (no network/auth needed). This unblocks baselines (B0/B1) immediately and forces measurable progress.

### Concrete steps (execute in order)
1. **Create research_state skeleton** (minimal, meaningful only):
   - `research_state/research_protocol.md` - copy FCLR-001 from RESEARCH_PROMPT.md, fill BTCUSDT scope, freeze cutoffs after coverage audit (do NOT peek at outcomes)
   - `research_state/data_source_registry.json` - log each ZIP/dir, paths, tested access, coverage
   - `research_state/hypothesis_registry.json` - FCLR-H001/H002/H003/H004 with statuses
   - `research_state/run_manifest.json` - git SHA, start time, config hash
   - `research_state/leakage_audit.md` - checklist items

2. **Ingest MVP (BTCUSDT)**:
   - Write `scripts/ingest_binance_zips.py` (or equivalent) to:
     - Discover all relevant ZIPs/dirs for `BTCUSDT`
     - Extract on-demand or read via zipfile (avoid duplicating huge raw trees unnecessarily)
     - Parse timestamps to UTC, normalize units, detect column defs
     - Build hourly panel: `fundingRate`, `markPrice`, `indexPrice`, `klines` (open/high/low/close/volume), align by timestamp
     - Emit `data/processed/btcusdt_hourly_panel.parquet` (git-ignored) + checksums in manifest

3. **Validate schema & leakage guards**:
   - Write `tests/test_ingest_timestamps.py` - UTC normalization, no future leakage, dup detection
   - Write `tests/test_split_embargo.py` - 7-day embargo logic
   - Add data quality report to `research_state/leakage_audit.md`

4. **Freeze protocol & compute coverage**:
   - Set train/val/test boundaries from coverage only (60/20/20 chronological), record hashes/cutoffs in protocol BEFORE targets
   - Run coverage audit, update `run_manifest.json`

**ACCEPTANCE TEST (must pass to call T001 done):**
- [ ] `research_state/research_protocol.md` exists, references FCLR-001, has frozen split boundaries + hashes
- [ ] `scripts/ingest_binance_zips.py` + tests pass locally
- [ ] `data/processed/btcusdt_hourly_panel.parquet` exists with row count, date range, checksum logged in `run_manifest.json`
- [ ] `tests/test_ingest_timestamps.py`, `tests/test_split_embargo.py` all pass
- [ ] `research_state/data_source_registry.json` lists all BTCUSDT sources tested with pass/fail

## 4) BOTTLENECK REMOVAL PLAN
- **No doc-sprawl:** Don't create 10 empty markdown files. Only create artifacts with real content as you build them.
- **Work with local data:** All required data is present as ZIPs - no network calls needed. Force extraction/processing, not probing.
- **Parallelize where possible:** Ingestion + tests can be written together; schema validation first.
- **Fail fast:** If a ZIP is corrupt/missing expected columns, quarantine with provenance in registry (don't guess).
- **Kill busywork:** Skip workflow changes, status dashboards, or orchestrator code unless it directly unblocks T001.

## 5) NEXT FOCUS CAMPAIGN (FOR FUTURE SESSIONS)
**CAMPAIGN NAME:** `FCLR-CAMPAIGN-01-FUNDING-VOL-BUILD`

**MANDATE:** "Build the pipeline. Compute baselines. No overlay. No trading."

**ORDER OF OPERATIONS (cannot skip):**
1. **T001 (NOW):** Ingest BTCUSDT + freeze protocol ← **BLOCKS EVERYTHING**
2. **T002:** Build features per FCLR-001 (RV1h/RV24h/RV168h, funding extremeness, premium, EMA dislocation) with training-only normalization
3. **T003:** Build targets (next-24h realized variance) + apply 7-day embargo
4. **T004:** Compute B0/B1 baselines on val, then holdout once frozen
5. **T005:** Add C1/C2, run QLIKE comparison vs B1 with block bootstrap

**RULE:** If stuck, do NOT write another handoff memo - fix the ingestion/parser/test or try the next materially different local file. Every session must produce a tested artifact or a concrete blocker with evidence.

## 6) EXACT COMMANDS TO START (COPY/PASTE)
```bash
# Verify environment
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline
ls -1 *.zip | wc -l && echo "---" && ls -d *fundingRate* *klines* 2>&1 | head -5

# Create dirs
mkdir -p research_state scripts tests data/processed data/raw_cache

# Start T001 immediately - read prompt for FCLR-001 section again
grep -n "14. Mandatory frozen starter protocol" RESEARCH_PROMPT.md | head -1
```

**DO NOT:** read the entire paper, browse web, create issue trackers, or "plan" for 3 hours. **DO:** unzip, parse, validate, test.

## 7) SESSION CHECKLIST (END OF SESSION MUST SATISFY)
- [ ] Updated `AGENT_HANDOFF.md` only if state changed materially (or leave as-is if T001 in progress)
- [ ] Logged changes/commands/results in handoff notes below
- [ ] All tests run with exact pass/fail
- [ ] `run_manifest.json` updated with hashes/timestamps
- [ ] Next action is unambiguous and executable without user input
- [ ] No placeholder files committed without content

## SESSION LOG (APPEND ONLY)
**2026-10-31T23:40:18Z - HANDOFF CREATED**
- Initialized FCLR-CAMPAIGN-01 with T001 as hard gate
- Identified local ZIP data as primary resource (no auth/network dependency)
- Forced data-first, test-driven approach per RESEARCH_PROMPT constraints
