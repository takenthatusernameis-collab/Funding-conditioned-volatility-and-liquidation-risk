# AGENT HANDOFF — 2026-11-19T00:27:17Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority.
> No duplicate `AGENT_HANDOFF*` exists under `research_state/`, `scripts/`, `tests/`, or `src/`.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T00:27:17Z)

**You must execute `FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z` now. Do not idle, do not re-audit RISK-07, do not gate-only, do not merely refresh this handoff, and do not attempt confirmatory multi-block on cached 2024 data.**

The session `session_20261118T191945Z` (UTC **20261118T191945Z**) has **completed** `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z` with all required artifacts present and non-empty in `research_state/session_20261118T191945Z/`:
- `fclr_risk07_recalibration_20261118T191945Z.{json,md}` — verdict `HONEST_NEGATIVE_OR_INCONCLUSIVE`, materiality floor NOT met
- `evidence_audit_20261118T191945Z.{json,md}`
- `recompute_fclr_risk07_recalibration_20261118T191945Z.json` — `n_discrepancies=0`
- `trigger_check_20261118T191945Z.json` — all 4 reopen triggers OPEN/none fired
- RISK-06 + ROBUST-05 carry-forward packages (copied, non-empty)

**Gates status (verified 2026-11-18T20:13:53Z):**
- `check_handoff_heavywork_gate.py --json`: **PASS** (`risk_07` required=true, pass=true)
- `check_tracka_scope_registry_drift.py --json`: **PASS** (196/196)
- `next_campaign_status.py --json`: confirmatory multi-block **BLOCKED** (`any_feasible=false`); RISK-07 complete

---

## CURRENT STATE (verified 2026-11-19T00:27:17Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; RISK-07 complete; confirmatory path **BLOCKED**.
- **Latest executed session:** `research_state/session_20261118T191945Z` — `FCLR-LIQ-RISK-RECALIBRATION-07-20261118T191714Z` — **COMPLETE**.
- **Active required next campaign:** `FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z` — **Track A exploratory on Hyperliquid observed liquidations** (Ironflow/HF dataset).
- **Rank-0 trigger state:** `TRIGGER_ONLY`; all four reopen triggers OPEN/none fired.
- **Root `research_state/` md+json count:** **498/500** — write every new artifact under the session subdir, never at root.

### RISK-07 final result (do not re-run, do not re-interpret)
Three chronological holdouts (`2024-07/08/09`), expanding train from `2024-04-01`, 7-day purge/embargo, 5 instruments, 12 scenarios, 262,080 modeled rows. **Materiality floor NOT met** for any calibrator (C1_platt, C2_isotonic, C3_prior_offset). Real mean ΔBrier ≤ 0 or CI95 lower bound ≤ 0 in ≥2/3 holdouts. Placebo null not exceeded. Verdict: `HONEST_NEGATIVE_OR_INCONCLUSIVE`. Correct claim: train-only recalibration did not materially improve modeled breach-risk calibration over RV-only baseline out-of-sample.

### Feasibility facts — do not claim you are blocked
- **Confirmatory multi-block cached design:** infeasible in all domains (`any_feasible=false`). Certified closed; do not reopen without a machine-satisfied trigger.
- **Cached 2024-03…09 data:** complete 1h mark-price + funding for 5 instruments. **Exhausted for confirmatory work.** Only stdlib exploratory re-runs possible — not the next priority.
- **Hyperliquid (Ironflow/HF) data:** **observed liquidation labels available** (Track A candidate). Per `next_campaign_status.py`:
  - `hyperliquid_bulk_frontier`: candles/funding/OI/liquidations **2025-05 … 2026-04** (12 months, 9 coins)
  - `hyperliquid_extended_frontier`: usable_months **2025-11 … 2026-10** (12 months, 17 coins)
  - Both frontiers show `any_feasible=false` for **confirmatory** design (min 127 design days, 3 non-overlapping blocks)
  - **But exploratory Track A assessment is viable and unblocked** — no confirmatory gate required.
- **Environment:** `numpy/pandas/scipy` absent by design for core path. Implement with stdlib (`json/csv/urllib/statistics/random/hashlib/datetime`). Parquet reads require `pandas`/`pyarrow` — acceptable for Track A label ingestion only; core modeling stays stdlib.
- **Sealed months:** 2024-10 onward sealed for cached Binance confirmatory tracks. Hyperliquid 2025-05+ is **unopened** for Track A outcomes.

---

## NEXT FOCUS CAMPAIGN — REQUIRED HEAVY WORK (machine-enforced)

**`FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z` — Track A exploratory assessment: Hyperliquid observed liquidation labels (Ironflow/HF dataset)**

### Research question
Are the **observed forced-liquidation records** from the Ironflow/Hyperliquid Hugging Face dataset (`ironflow/hyperliquid-liquidations`) admissible, sufficiently complete, and temporally aligned with mark-price/funding data to support a **future confirmatory Track A forecast test**? If yes, freeze the admissibility criteria and register the confirmatory design. If no, document the exact shortfall and keep Track A `DATA_BLOCKED` or `NOT_STARTED`.

### Scope (exploratory — no confirmatory gate)
- **Source:** `https://huggingface.co/datasets/ironflow/hyperliquid-liquidations` — unauthenticated, no API key, no requester-pays.
- **Data:** `data/events/YYYY-MM.parquet` (liquidation events) + `data/fills/YYYY-MM.parquet` (fill details).
- **Target window:** **2025-11 … 2026-10** (12 months, per `hyperliquid_extended_frontier.usable_months`). Do not read 2025-05…2025-10 for outcomes (earlier window for context only).
- **Coins:** 17 coins with candle coverage (`BTC`, `ETH`, `BNB`, `SOL`, `XRP`, `AVAX`, `DOGE`, `LINK`, `SUI`, `ARB`, `OP`, `MATIC`, `APT`, plus 4 more per extended frontier).
- **Label definition:** observed forced liquidation **events** (not modeled boundary breaches). Each event row = one liquidation. Must normalize by contemporaneous open interest or volume where available; retain raw counts and source limits.
- **Missing-event coverage:** absence from feed ≠ "no liquidation." Must quantify reporting caps, rate limits, venue scope, known gaps.
- **Alignment:** join to Hyperliquid 1h candles (`candleSnapshot` API) and funding (`fundingHistory` API) by coin and timestamp. Verify timestamp semantics (ms since epoch, UTC).

### Required session directory
Create and populate **`research_state/session_20261118T201919Z/`** (new session dir, UTC now) with **all artifacts non-empty**:

1. **`fclr_tracka_exploratory01_prereg_20261118T201919Z.{json,md}`** — outcome-blind prereg (frozen before outcome inspection):
   - Source URLs, access method, license/terms, authentication status
   - Exact coin list, month range, expected row counts (from HF tree probe)
   - Label construction: event definition, normalization, missingness rules
   - Alignment protocol: candle/funding join keys, tolerance, timezone
   - Admissibility gates (must pass for confirmatory): ≥5 coins, ≥3 complete months, ≤20% gap rate, provenance hashes
   - `outcome_data_inspected_before_freeze=false`

2. **`fclr_tracka_exploratory01_ingest_20261118T201919Z.{py,json,md}`** — ingestion script + manifest + audit:
   - Fetch HF tree listing (ETag-cached), probe each month for events+fills
   - Download parquet (stdlib `urllib` + `pandas` for read only), write CSV/JSON twins for stdlib compatibility
   - Schema validation, duplicate detection, timestamp unit check, coin mapping
   - Per-month provenance: SHA256, row count, date range, coins present, gap diagnostics
   - **Must run offline after first fetch** — cache raw parquet/CSV in `research_state/data_cache/ironflow_events/<COIN>/<YYYY-MM>.{parquet,csv,accessed.json,sha256}`

3. **`fclr_tracka_exploratory01_alignment_20261118T201919Z.{py,json,md}`** — label/feature alignment:
   - Fetch Hyperliquid candles (1h) + funding for same coins/months (reuse `tracka_hl_fetch_candles_early.py` pattern)
   - Join liquidation events to 1h candle bars by coin + timestamp (floor to hour)
   - Construct per-coin-per-hour label: `liq_count`, `liq_notional` (if fills available), `obs_oi` (if available)
   - Missingness matrix: hours with candles but no liq feed, hours with liq but no candles
   - Output: aligned panel JSON + CSV (stdlib-readable)

4. **`fclr_tracka_exploratory01_admissibility_20261118T201919Z.{json,md}`** — admissibility verdict:
   - Per-coin, per-month coverage, gap rate, event prevalence
   - Reporting limits: HF dataset caps, Ironflow collection rules, known truncation
   - **Binary verdict per admissibility gate** (from prereg) with evidence
   - If **all gates pass**: register confirmatory design `FCLR-LIQ-TRACKA-CONFIRMATORY-01` with frozen splits, metrics, gate
   - If **any gate fails**: `DATA_BLOCKED` or `NOT_STARTED` with exact shortfall; do not proceed to confirmatory

5. **`evidence_audit_20261118T201919Z.{json,md}`** — session evidence audit (per RESEARCH_PROMPT.md §19)

6. **`trigger_check_20261118T201919Z.json`** — reopen trigger evaluation:
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: this session's admissibility audit (`status=ADMISSIBLE` + `observed_labels=true` + ≥5 instruments + ≥3 blocks or ≥1 complete month) → FIRED or OPEN
   - Other 3 triggers remain OPEN

### Mandatory carry-forward into same session dir (copy, non-empty)
- RISK-07 package from `session_20261118T191945Z`: `fclr_risk07_recalibration_*.{json,md}`, `fclr_risk07_prereg_*.{json,md}`, `fclr_risk07_calibrators_*.{py,json}`, `evidence_audit_*.{json,md}`, `recompute_fclr_risk07_recalibration_*.json`, `trigger_check_*.json`
- RISK-06 + ROBUST-05 packages (already in RISK-07 dir, copy forward)

### Execution recipe (fast path, reuse verified code)
1. **Probe HF tree first** — run `monitor_ironflow_liquidations.py --quick` to get current tree state, ETags, available months. Do not download full parquet until tree probe confirms coverage.
2. **Fetch candles/funding in parallel** — run `tracka_hl_fetch_candles_early.py` (or adapt for 2025-11…2026-10) and `hyperliquid_funding_fetch.py` for same coins/months.
3. **Ingest liquidations** — write stdlib CSV/JSON twins for each month/coin. Use `pandas` only for parquet→CSV conversion; core logic in stdlib.
4. **Align & audit** — join on `(coin, hour_timestamp)`. Compute coverage diagnostics. Write admissibility verdict.
5. **Write increments** — emit non-empty JSON/MD after each major step so timeout leaves evidence.
6. **Runtime:** bounded by HF download speeds and parquet conversion. Write partials.

### Prohibitions (enforced by gate)
- Do not read sealed Binance months 2024-10…2026-11 for outcomes.
- Do not re-run RISK-07, RISK-06, ROBUST-05, or Track C QLIKE.
- No confirmatory claim from this exploratory session. Admissibility verdict only.
- No `statsmodels` or heavy deps in core path. `pandas`/`pyarrow` only for parquet→CSV ingest.
- Never emit zero-byte artifacts. Every required file must be non-empty.
- Do not spend session on handoff refresh / audit / gate-only work. The only acceptable output is the completed Track A exploratory package plus carried-forward packages.

### Verification commands (run before final handoff update)
```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 scripts/check_tracka_scope_registry_drift.py --json
python3 scripts/next_campaign_status.py --json
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v
```
All must PASS. `risk_07` remains required=true, pass=true. New session must be `heavy_session_dir`.

### Handoff update (after verification)
1. Change **Latest executed session** to `session_20261118T201919Z`.
2. Change **Active required next campaign** to the campaign ID registered in admissibility verdict (or `BLOCKED` if Track A fails).
3. Update **Rank-0 trigger state** per `trigger_check_20261118T201919Z.json`.
4. Preserve sole durable handoff; no duplicates; no root-level `research_state/*.md|json`.

---

## READ FIRST (exact files)
1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261118T191945Z/fclr_risk07_recalibration_20261118T191945Z.md` — RISK-07 verdict
3. `research_state/session_20261118T191945Z/trigger_check_20261118T191945Z.json` — trigger definitions
4. `scripts/monitor_ironflow_liquidations.py` — Ironflow/HF probe + download (read full file)
5. `scripts/tracka_hl_fetch_candles_early.py` — Hyperliquid candles fetch pattern
6. `scripts/hyperliquid_funding_fetch.py` — Hyperliquid funding fetch pattern
7. `scripts/next_campaign_status.py` — frontier feasibility (already run)
8. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/resume_trigger_registry.json`

---

## REOPEN TRIGGERS (machine-checkable — all OPEN before this session)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`)
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: **THIS SESSION'S** `fclr_tracka_exploratory01_admissibility_20261118T201919Z.{json,md}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month)
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth)
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null)

---

## VERIFICATION RECORD — 2026-11-19T00:27:17Z (RISK-07 complete; next campaign defined)
- **Bottleneck removed 1 (RISK-07 complete):** all required artifacts non-empty; `check_handoff_heavywork_gate.py` PASS; `risk_07` required=true, pass=true.
- **Bottleneck removed 2 (confirmatory blocked acknowledged):** `next_campaign_status.py` → `any_feasible=false` certified; no attempt to reopen.
- **Bottleneck removed 3 (Track A path opened):** Hyperliquid Ironflow/HF dataset identified as only viable Track A source; exploratory campaign defined with concrete admissibility gates.
- **Bottleneck removed 4 (audit-only avoidance):** next session mandated to produce Track A exploratory package + carry-forward; no handoff refresh, no gate-only work.
- Root `research_state/` unchanged (498/500 ≤ cap 500).
- Sole durable handoff preserved; no duplicates; no sealed artifacts or workflows modified.

(End of file)