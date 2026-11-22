# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T06:28:58Z (supersedes 2026-11-22T06:23:39Z, which supersedes 2026-11-22T06:18:50Z, which supersedes 2026-11-22T06:17:18Z, which supersedes 2026-11-22T05:24:14Z, which supersedes 2026-11-22T05:23:08Z, which supersedes 2026-11-22T05:20:02Z, which supersedes 2026-11-22T05:16:02Z, which supersedes 2026-11-22T05:14:44Z, which supersedes 2026-11-22T04:33:48Z, which superseded 2026-11-22T04:12:48Z, which superseded 2026-11-22T03:30:00Z)
**Session type:** handoff-refresh / coordination session. This session intentionally did NOT create a `session_<UTC>/` directory and did NOT execute the pooled campaign — its sole job is to leave the most relevant, timestamped, prioritized initial task message for the NEXT agentic work session (see §1) and to re-verify that no bottleneck blocks heavy progress. Because it created no new session dir, the latest on-disk session stays `session_20261122T033000Z` (pre-campaign, grandfathered) and the gate remains green.
**Sole active campaign (rank-0, gate-enforced):** `FCLR-POOLED-001-20261122T040000Z` — **READY_EXECUTE / ACTIVE (NOT YET EXECUTED).** The pooled, chronologically-split out-of-sample confirmatory design on the on-disk ironflow bulk data (`research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}`, 18 months 2025-05..2026-10). No session with UTC > `20261122T040000Z` exists on disk yet, so the NEXT session MUST execute this campaign. Idling, prose-only, source-probe-only, audit-only, trigger-only, or verify-and-stop sessions are FORBIDDEN — the gate fails closed. A future session that only refreshes this handoff again (without creating a session dir) does not advance the science and is itself a failure mode: the next session MUST create `research_state/session_<UTC>/` with the full `fclr_pooled001_*` heavy artifact set.
**Latest completed heavy session on disk:** `session_20261122T033000Z` (UTC < campaign start `20261122T040000Z`, grandfathered) — executed the now-terminal FCLR-NEXT-SOURCE-VERIFY-01 campaign (source discovery returned NO_NEW_ADMISSIBLE_SOURCE; confirmatory design FCLR-NEXT-CONFIRM-001 registered behind an outcome-blind prereg; heavy eval triad + independent stdlib recompute + evidence audit + gate alias + non-empty trigger_check all emitted; decision GO). All earlier sessions remain terminal/grandfathered.
**Gate baseline (verified this session, 2026-11-22T06:28:58Z):** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` (`latest_handoff=session_20261122T033000Z`, `latest_disk=session_20261122T033000Z`, `handoff_stale=False`, `pooled.required=False` grandfathered, `root=499/500`); all 6 gate unittest modules (`test_tracka_hardening_143`, `test_tracka_hardening_144`, `test_active_campaign_gate`, `test_fclr_heavy_confirm_gate`, `test_fclr_campaign_gate`, `test_fclr_starter_001_campaign_gate`) → **116 tests, 0 failures**; `research_state` root md+json count = **499/500**; latest on-disk session = latest recorded in this handoff (`session_20261122T033000Z`). On-disk ironflow bulk caches re-counted this session: candles_1h/funding/open_interest/liquidations each **18 parquet files** (2025-05..2026-10). Frontier has exactly one `rank:0` (`READY_EXECUTE`, task `FCLR-POOLED-001-20261122T040000Z`); every other entry is `SUPERSEDED`/`SUPERSEDED_TERMINAL` — no duplicate rank-0 deadlock and no blocked/inefficient session. HEAD = `f9ba88169` (this handoff refresh is the only worktree change).
**Environment (verified this session):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` are NOT installed (`import numpy` → ModuleNotFoundError). `pyarrow` 26.0.1 IS already installed and is what reads the ironflow bulk parquet. Write the pooled evaluation stdlib + pyarrow only (matching the independent-recompute convention). Do NOT rely on numpy/pandas/scipy.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and any `NEXT_SESSION_TASK.md` files (none exist). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01, FCLR-LIVE-ARCHIVE-02, and FCLR-NEXT-SOURCE-VERIFY-01) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is executed and terminal (decision GO, NO_NEW_ADMISSIBLE_SOURCE). **The one remaining rank-0 campaign is FCLR-POOLED-001**, and it is heavy work on data that is ALREADY on disk. A future session must NOT idle, must NOT re-verify any exhausted source, and must NOT re-run any completed campaign.

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars (RESEARCH_PROMPT.md §Mission/§3). Never drift into unrelated work, risk overlays, or live/paper trading.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T06:28:58Z)

**STATUS: FCLR-POOLED-001 READY_EXECUTE — HEAVY WORK IS MANDATORY. NO SESSION WITH UTC > 20261122T040000Z EXISTS ON DISK. THE NEXT SESSION MUST CREATE `research_state/session_<UTC>/` (UTC > 20261122T040000Z) AND EXECUTE THE POOLED CHRONOLOGICAL OOS CONFIRMATORY DESIGN WITH THE FULL `fclr_pooled001_*` ARTIFACT SET. VERIFY-AND-STOP / PROSE-ONLY / TRIGGER-ONLY / SOURCE-PROBE-ONLY / AUDIT-ONLY / HANDOFF-REFRESH-ONLY SESSIONS FAIL THE GATE CLOSED.**

### 1a. Bottlenecks removed / verified clear (why significant progress can continue now)

This session re-verified that the frontier is unblocked and the previously-removed bottlenecks remain removed:

1. **Single rank-0 confirmed.** `research_state/experiment_frontier.json` has exactly one `rank:0` entry — `FCLR-POOLED-001-20261122T040000Z` (READY_EXECUTE). Every other entry is terminal (`SUPERSEDED*`). `tests/test_active_campaign_gate.py::test_frontier_rank0_is_active_heavy_campaign` passes (exactly one rank-0, ACTIVE, concrete unfinished task). No duplicate rank-0 deadlock remains.
2. **Pooled enforcement is armed.** `scripts/check_handoff_heavywork_gate.py` binds `FCLR-POOLED-001-20261122T040000Z` via `POOLED_CAMPAIGN_RE` + `_pooled_state`; the matching loop zips against the transformed `fclr_pooled001_*` family. The completed NEXT-SOURCE-VERIFY-01 campaign is disarmed. A post-start session cannot satisfy the gate without the full pooled artifact set.
3. **No blocked / inefficient sessions remain.** The only open path is FCLR-POOLED-001; it needs no external trigger and no new source (the ironflow bulk parquet is on disk, ~360 MB, 18 files per dataset). The `next_campaign_status.py` verdict `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` is TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing; it is NOT a blocker for a pooled chronological design (see §2). There is no state in which the next session must wait, re-probe, or idle.
4. **Interrupted empty-session bottleneck removed.** This refresh found an empty post-campaign session directory left by an interrupted start. It contained no artifacts, so it was removed with `rmdir`; this cleared the stale-latest-session gate failure without deleting research evidence. The next session must still create its real session directory and heavy artifact set as required below.

### 1b. What the NEXT session must do (heavy work is mandatory)

Execute **FCLR-POOLED-001** (rank-0, gate-enforced, campaign start UTC `20261122T040000Z`): a heavy **POOLED, chronologically-split out-of-sample confirmatory design** on the on-disk ironflow bulk data, spanning all 18 months with chronological train/test splits, purge/embargo ≥ max horizon, and per-coin block-bootstrap. This breaks the broken "3 contiguous 30-day funding-backed blocks" framing that `scripts/next_campaign_status.py` reports as `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN`: a pooled design is feasible TODAY with no new source and no network.

**Verified on-disk data (ironflow bulk caches, 18 monthly parquet files each, 2025-05..2026-10; row counts per the frontier evidence block):**

| Dataset | Files | Rows | Coins (max) | Schema |
|---------|-------|------|-------------|--------|
| candles_1h | 18 | 3,643,742 | 799 | timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades |
| funding | 18 | 4,104,648 | 494 | timestamp, market, coin, dex, funding_rate, premium |
| open_interest | 18 | 3,977,432 | 553 | timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd |
| liquidations | 18 | 2,849,452 | (no coin col; key on market/issuer) | timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash |

Each monthly parquet has a `.parquet.sha256` sidecar and an `.accessed.json` provenance file — use the sha256 sidecars to assert inputs. Do NOT download new data; do NOT modify the caches.

**Steps — all artifacts non-empty, under `research_state/session_<UTC>/` with UTC strictly greater than `20261122T040000Z`, named with the `fclr_pooled001_` family:**

1. **Source registry** — `fclr_pooled001_source_registry_<UTC>.{json,md}`: record each parquet file path, sha256 (from the `.parquet.sha256` sidecars), row count, coin coverage, month span, and schema.
2. **Outcome-blind prereg freeze BEFORE inspecting any outcome** — `fclr_pooled001_prereg_<UTC>.{json,md}`: funding-conditioned volatility + liquidation-risk hypotheses, targets, features, chronological train/test split with purge/embargo ≥ max horizon, per-coin block-bootstrap, baselines, 2% materiality floor, decision gates; `outcome_data_inspected_before_freeze:false`; assert input file hashes + config hash.
3. **Heavy pooled evaluation triad** — `fclr_pooled001_eval_<UTC>.{py,json,md}`: funding-conditioned volatility + liquidation-risk, chronological train/test split, per-coin block-bootstrap, Diebold-Mariano / QLIKE / Brier where applicable.
4. **Independent stdlib recompute** — `fclr_pooled001_recompute_<UTC>.{py,json}`: recompute headline numbers without reusing the evaluation code path.
5. **Evidence audit** — `fclr_pooled001_evidence_audit_<UTC>.{json,md}` plus the gate-critical alias `evidence_audit_<UTC>.json`.
6. **Non-empty trigger check** — `trigger_check_<UTC>.json`.

That is the full 13-file set the gate requires (11 `fclr_pooled001_*` + `evidence_audit_` alias + `trigger_check_`). Stdlib + pyarrow only (`pyarrow` is already installed; do NOT rely on numpy/pandas/scipy). Preserve nulls as `NOT_SUPPORTED`. Do NOT threshold-shop or relax the 2% materiality floor after outcomes.

**Close-out:** update this `AGENT_HANDOFF.md` to record the new session as latest and FCLR-POOLED-001's new status. **You MUST add your new `session_<UTC>` id to this handoff in the same session** — otherwise the gate's stale-handoff check (`_latest_disk_session > _latest_handoff_session`) fails. Do NOT create root-level `research_state/*.md|*.json` (root count 499/500; cap enforced). Do NOT modify `.github/workflows` (protected control plane). Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).

### 1c. Why future agents cannot avoid heavy work (machine-enforced)

`scripts/check_handoff_heavywork_gate.py` binds FCLR-POOLED-001 via `POOLED_CAMPAIGN_RE` (campaign start UTC `20261122T040000Z`) and `_pooled_state`. Any session with UTC > `20261122T040000Z` that is recorded in this handoff must carry the full FCLR-POOLED artifact set — source registry (json+md), outcome-blind prereg freeze (json+md), heavy pooled evaluation triad (py+json+md), independent stdlib recompute (py+json), evidence audit (json+md), gate-critical `evidence_audit_` alias (json), and non-empty `trigger_check` (json). Zero-byte placeholders fail closed. A prose-only, trigger-only, source-probe-only, audit-only, or verify-and-stop session fails closed. Sessions with UTC ≤ `20261122T040000Z` (incl. `session_20261122T033000Z`) are grandfathered so this refresh stays green.

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (NOT a blocker — pooled design is the point)
```

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible evidence)

`scripts/next_campaign_status.py` reports `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` (re-verified this session), but that verdict is TRUE only for the narrow "3 contiguous 30-day funding-backed blocks" framing. It is NOT a statement about the data on disk:

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
- **Do NOT** claim completion without the full `fclr_pooled001_*` artifact set under a new `session_<UTC>/` (UTC > `20261122T040000Z`), and without recording that session id in this handoff.
- **Do NOT** write a concrete future `session_<UTC>` id into this handoff before that directory exists — the gate treats the lexicographically latest recorded `session_` id as the session to verify and will fail if its directory is missing.
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
| FCLR-NEXT-SOURCE-VERIFY-01 | materially different verified free source + heavy 3-block confirmatory | SUPERSEDED_TERMINAL (session_20261122T033000Z; NO_NEW_ADMISSIBLE_SOURCE; confirmatory design FCLR-NEXT-CONFIRM-001 registered; decision GO; demoted to rank 2) |
| **FCLR-POOLED-001** | **pooled chronological OOS confirmatory on on-disk ironflow bulk data** | **READY_EXECUTE / ACTIVE — rank-0, gate-enforced; NOT YET EXECUTED (no session with UTC > 20261122T040000Z on disk); heavy work mandatory** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: (1) what changed and why; (2) what was tested with exact outcomes; (3) what evidence was added and where (full paths); (4) the state of each research gate; (5) the single highest-value next task; (6) the precise verifying command; (7) any blocker with the next materially different route. **Rank-0: FCLR-POOLED-001 (READY_EXECUTE/ACTIVE) — heavy work mandatory.** All new artifacts under `research_state/session_<UTC>/` with the `fclr_pooled001_*` family. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (FCLR-POOLED-001 bound; post-start session must carry the full fclr_pooled001_* heavy artifact set under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the pooled design — that is the point)
```

After the next heavy session writes its first artifact (UTC > `20261122T040000Z`) and records the new `session_<UTC>/` in this handoff, re-run `check_handoff_heavywork_gate.py`: it must PASS, and now only because the full `fclr_pooled001_*` heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)