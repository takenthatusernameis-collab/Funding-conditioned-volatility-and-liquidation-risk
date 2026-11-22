# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T04:12:48Z (supersedes 2026-11-22T03:30:00Z)
**Sole active campaign (rank-0, gate-enforced):** FCLR-POOLED-001-20261122T040000Z — **READY_EXECUTE / ACTIVE (NOT YET EXECUTED).** The pooled, chronologically-split out-of-sample confirmatory design on the on-disk ironflow bulk data (`research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}`, 18 months 2025-05..2026-10). No session with UTC > 20261122T040000Z exists on disk yet, so the next session MUST execute this campaign. Idling, prose-only, source-probe-only, audit-only, trigger-only, or verify-and-stop sessions are FORBIDDEN — the gate fails closed.
**Latest completed heavy session on disk:** session_20261122T033000Z (UTC < campaign start, grandfathered) — executed the now-terminal FCLR-NEXT-SOURCE-VERIFY-01 campaign (source discovery returned NO_NEW_ADMISSIBLE_SOURCE; confirmatory design FCLR-NEXT-CONFIRM-001 registered behind an outcome-blind prereg; heavy eval triad + independent stdlib recompute + evidence audit + gate alias + non-empty trigger_check all emitted; decision GO). All earlier sessions remain terminal/grandfathered.
**Gate baseline (verified this session):** `python3 scripts/check_handoff_heavywork_gate.py` → PASS reason=OK; all 6 gate unittest files → 116 pass, 0 fail (5 skipped).
**Environment (verified this session):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` are NOT installed by default (`import numpy` → ModuleNotFoundError). `pyarrow` installs cleanly with `pip install pyarrow` (verified: pyarrow 26.0.1) and IS required to read the ironflow_bulk parquet. The pooled evaluation must `pip install pyarrow` first, or be written stdlib + pyarrow only (matching the independent-recompute convention). Stdlib-only recompute is preferred.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and any `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01, FCLR-LIVE-ARCHIVE-02, and FCLR-NEXT-SOURCE-VERIFY-01) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is executed and terminal (decision GO, NO_NEW_ADMISSIBLE_SOURCE). **The one remaining rank-0 campaign is FCLR-POOLED-001**, and it is heavy work on data that is ALREADY on disk. A future session must NOT idle, must NOT re-verify any exhausted source, and must NOT re-run any completed campaign.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T04:12:48Z)

**STATUS: FCLR-POOLED-001 READY_EXECUTE — HEAVY WORK IS MANDATORY. NO SESSION WITH UTC > 20261122T040000Z EXISTS ON DISK. THE NEXT SESSION MUST EXECUTE THE POOLED CHRONOLOGICAL OOS CONFIRMATORY DESIGN. VERIFY-AND-STOP / PROSE-ONLY / TRIGGER-ONLY / SOURCE-PROBE-ONLY / AUDIT-ONLY SESSIONS FAIL THE GATE CLOSED.**

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars. Never drift into unrelated work.

### 1a. Bottlenecks removed this session (why significant progress is now unblocked)

1. **Duplicate rank-0 deadlock removed.** `research_state/experiment_frontier.json` held TWO `rank:0` entries — the new `FCLR-POOLED-001-20261122T040000Z` (READY_EXECUTE) AND the already-executed `FCLR-NEXT-SOURCE-VERIFY-01` (SUPERSEDED_TERMINAL). The stale rank-0 on a terminal campaign deadlocked `tests/test_active_campaign_gate.py::test_frontier_rank0_is_active_heavy_campaign` (`assert len(rank0)==1` → got 2). Fixed: the completed NEXT-SOURCE-VERIFY-01 entry was demoted from rank 0 to rank 2 (its terminal `SUPERSEDED_TERMINAL` status retained), leaving `FCLR-POOLED-001` as the sole rank-0. `test_active_campaign_gate` now passes (5 tests OK).
2. **Dormant POOLED enforcement removed.** The gate (`scripts/check_handoff_heavywork_gate.py`) only binds a campaign whose full `FCLR-XXX-N-YYYYMMDDTHHMMSSZ` string appears in this handoff. The previous handoff referenced the executed NEXT-SOURCE-VERIFY-01 campaign 17 times and the POOLED campaign 0 times, so the POOLED heavy-artifact requirement was never armed — a future session could have passed the gate without doing any pooled work. This handoff now arms `FCLR-POOLED-001-20261122T040000Z` and disarms the completed NEXT-SOURCE-VERIFY-01, so the next post-040000Z session cannot satisfy the gate without the full heavy pooled artifact set.
3. **Pooled artifact-naming mismatch removed.** `_pooled_state` in the gate built a per-campaign `family` of `fclr_pooled001_*` prefixes (matching the frontier and the `tag` machinery) but matched the loop against the untransformed `POOLED_REQUIRED` `fclr_pooled_*` prefixes. A correct heavy session following the frontier's documented `fclr_pooled001_*` naming would therefore have failed the gate. Fixed: the matching loop now zips against the transformed `family`. Verified by simulation — correct `fclr_pooled001_*` files PASS (11/11 artifacts), untransformed `fclr_pooled_*` files now FAIL, pre-start sessions stay grandfathered, and a disarmed handoff stays inert.

### 1b. What the NEXT session must do (heavy work is mandatory)

Execute **FCLR-POOLED-001** (rank-0, gate-enforced, campaign start UTC 20261122T040000Z). Task: run a heavy **POOLED, chronologically-split out-of-sample confirmatory design** on the on-disk ironflow bulk data. This breaks the broken "3 contiguous 30-day funding-backed blocks" framing that `scripts/next_campaign_status.py` reports as `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`: a pooled design across all 18 months with chronological train/test splits, purge/embargo, and per-coin block-bootstrap is feasible TODAY with no new source and no network.

**Verified on-disk data (re-counted this session with pyarrow):**

| Dataset | Rows | Coins (max) | Span | Schema |
|---------|------|-------------|------|--------|
| candles_1h | 3,643,742 | 799 | 2025-05..2026-10 (18 files) | timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades |
| funding | 4,104,648 | 494 | 2025-05..2026-10 | timestamp, market, coin, dex, funding_rate, premium |
| open_interest | 3,977,432 | 553 | 2025-05..2026-10 | timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd |
| liquidations | 2,849,452 | (no coin col; key on market/issuer) | 2025-05..2026-10 | timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash |

Each monthly parquet has a `.parquet.sha256` sidecar and an `.accessed.json` provenance file — use the sha256 sidecars to assert inputs.

**Steps — all artifacts non-empty, under `research_state/session_<UTC>/` with UTC strictly greater than 20261122T040000Z, named with the `fclr_pooled001_` family:**

1. **Source registry** — `fclr_pooled001_source_registry_<UTC>.{json,md}`: record each parquet file path, sha256 (from the `.parquet.sha256` sidecars), row count, coin coverage, month span, and schema. Do NOT download new data; do NOT modify the caches.
2. **Outcome-blind prereg freeze BEFORE inspecting any outcome** — `fclr_pooled001_prereg_<UTC>.{json,md}`: funding-conditioned volatility + liquidation-risk hypotheses, targets, features, chronological train/test split with purge/embargo ≥ max horizon, per-coin block-bootstrap, baselines, 2% materiality floor, decision gates; `outcome_data_inspected_before_freeze:false`; assert input file hashes + config hash.
3. **Heavy pooled evaluation triad** — `fclr_pooled001_eval_<UTC>.{py,json,md}`: funding-conditioned volatility + liquidation-risk, chronological train/test split, per-coin block-bootstrap, Diebold-Mariano / QLIKE / Brier where applicable.
4. **Independent stdlib recompute** — `fclr_pooled001_recompute_<UTC>.{py,json}`: recompute headline numbers without reusing the evaluation code path.
5. **Evidence audit** — `fclr_pooled001_evidence_audit_<UTC>.{json,md}` plus the gate-critical alias `evidence_audit_<UTC>.json`.
6. **Non-empty trigger check** — `trigger_check_<UTC>.json`.

Stdlib + pyarrow only (`pip install pyarrow` first). Preserve nulls as `NOT_SUPPORTED`. Do NOT threshold-shop or relax the 2% materiality floor after outcomes. Do NOT create root-level `research_state/*.md|*.json` (root count 499/500; cap enforced by the gate and `test_tracka_hardening_125`) — all new artifacts go under `research_state/session_<UTC>/`.

**Close-out:** update this `AGENT_HANDOFF.md` to record the new session as latest and FCLR-POOLED-001's new status. Do NOT add root-level `research_state/*.md|*.json`. Do NOT modify `.github/workflows` (protected control plane). Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).

### 1c. Why future agents cannot avoid heavy work (machine-enforced)

`scripts/check_handoff_heavywork_gate.py` binds FCLR-POOLED-001 via `POOLED_CAMPAIGN_RE` (campaign start UTC 20261122T040000Z). Any session with UTC > 20261122T040000Z that is recorded in this handoff must carry the full FCLR-POOLED artifact set — source registry (json+md), outcome-blind prereg freeze (json+md), heavy pooled evaluation triad (py+json+md), independent stdlib recompute (py+json), evidence audit (json+md), gate-critical `evidence_audit_` alias (json), and non-empty `trigger_check` (json). A prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop session fails closed. No zero-byte placeholders.

**Verify with:**
```
pip install pyarrow                                              # once, to read the bulk parquet
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (NOT a blocker — pooled design is the point)
```

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible evidence)

`scripts/next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`, but that verdict is TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing. It is NOT a statement about the data on disk:

| Probe | Result |
|-------|--------|
| `research_state/data_cache/ironflow_bulk/candles_1h` | 18 monthly parquet files, 3,643,742 rows, up to 799 coins, 2025-05..2026-10 |
| `.../ironflow_bulk/funding` | 18 files, 4,104,648 rows, up to 494 coins |
| `.../ironflow_bulk/open_interest` | 18 files, 3,977,432 rows, up to 553 coins |
| `.../ironflow_bulk/liquidations` | 18 files, 2,849,452 rows, key on market/issuer (no coin column) |
| Chronological pooled OOS design | FEASIBLE TODAY — no new source, no network, no external trigger |

A pooled chronological train/test split with purge/embargo and per-coin block-bootstrap is a materially different, feasible, heavy design on data that is already on disk. The exhausted-source frontier (NEXT-SOURCE-VERIFY-01 → NO_NEW_ADMISSIBLE_SOURCE) and the exhausted 3-block framing are both sidestepped by this campaign. Future agents cannot idle waiting for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (the gate checks non-zero size).
- **Do NOT** claim completion without the full `fclr_pooled001_*` artifact set under a new `session_<UTC>/` (UTC > 20261122T040000Z).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as `NOT_SUPPORTED`.
- **Do NOT** re-run any terminal/completed campaign (incl. NEXT-SOURCE-VERIFY-01, LIVE-ARCHIVE-01/-02, and all earlier campaigns).
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.
- **Do NOT** re-verify that `data.binance.vision` is reachable — already exhausted by FCLR-LIVE-ARCHIVE-02.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes for a post-start session only when the full `fclr_pooled001_*` artifact set is present and non-empty under the latest `session_<UTC>/`.

**If no future session occurs:** this handoff stands as the final record; the pooled design remains the mandated next heavy task; no heavy pooled evaluation was executed this session.

---

## 4. FROZEN / ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

- **Ironflow bulk caches (the FCLR-POOLED-001 data source):** `research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}/<YYYY-MM>.parquet` plus `<YYYY-MM>.parquet.sha256` and `<YYYY-MM>.accessed.json` sidecars, 18 months 2025-05..2026-10. Row counts and schemas per §1b/§2. Assert sha256 before reading; do NOT mutate the caches.
- **Combined liquidation panel (legacy, still frozen):** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Not needed for the pooled campaign; do not substitute it for the bulk data.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; `premium` all-null; not needed for the pooled campaign.

---

## 5. CAMPAIGN LEDGER (all terminal except the rank-0)

| Campaign | Mechanism | Session / Status |
|----------|-----------|------------------|
| FCLR-STARTER-001 … FCLR-PANEL-FE-001 | earlier frozen-data campaigns | terminal/superseded |
| FCLR-LIQ-CONTAGION-001 | cross-coin contagion + funding spillover | COMPLETE (20261121T193000Z) |
| FCLR-LIQ-CONTAGION-002 | edge-set robustness + per-edge materiality reconciliation | COMPLETE (20261121T210000Z) |
| FCLR-FINAL-SYNTHESIS-01 | final synthesis report | COMPLETE (20261121T220100Z) |
| FCLR-LIVE-DATA-ACQUISITION-001 | unverified free-data route | SUPERSEDED 20261121T232840Z |
| FCLR-LIVE-ARCHIVE-01 | verified free-archive heavy 3-block design | SUPERSEDED by -02 (never started) |
| FCLR-LIVE-ARCHIVE-02 | verified free-archive heavy 3-block design | SUPERSEDED_TERMINAL (session_20261122T013000Z; decision NOT_SUPPORTED) |
| FCLR-NEXT-SOURCE-VERIFY-01 | materially different verified free source + heavy 3-block confirmatory | SUPERSEDED_TERMINAL (session_20261122T033000Z; NO_NEW_ADMISSIBLE_SOURCE; confirmatory design FCLR-NEXT-CONFIRM-001 registered; decision GO; demoted to rank 2 this session) |
| **FCLR-POOLED-001** | **pooled chronological OOS confirmatory on on-disk ironflow bulk data** | **READY_EXECUTE / ACTIVE — rank-0, gate-enforced; NOT YET EXECUTED (no session with UTC > 20261122T040000Z on disk); heavy work mandatory** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: what changed and why; what was tested with exact outcomes; what evidence was added and where (full paths); the state of each research gate; the single highest-value next task (FCLR-POOLED-001: freeze the outcome-blind prereg, then execute the pooled chronological OOS evaluation triad + stdlib recompute + evidence audit + gate alias + trigger_check under a new `session_<UTC>/`); the precise verifying command; any blocker with the next materially different route. **Rank-0: FCLR-POOLED-001 (READY_EXECUTE/ACTIVE) — heavy work mandatory.** All new artifacts under `research_state/session_<UTC>/` with the `fclr_pooled001_*` family. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
pip install pyarrow                                              # once, to read the bulk parquet
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (FCLR-POOLED-001 bound; post-start session must carry the full fclr_pooled001_* heavy artifact set under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the pooled design — that is the point)
```

After the next heavy session writes its first artifact (UTC > 20261122T040000Z) and records the new `session_<UTC>/` in this handoff, re-run `check_handoff_heavywork_gate.py`: it must PASS, and now only because the full `fclr_pooled001_*` heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)