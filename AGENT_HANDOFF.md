# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T09:51:12Z (supersedes 2026-11-22T09:45:49Z)
**Session type:** heavy execution — FCLR-POOLED-001 rank-0 campaign executed to completion under `session_20261122T092003Z`. All 13 required `fclr_pooled_*` artifacts present and non-empty. Gate passes.

**Sole active campaign (rank-0, gate-enforced):** `FCLR-POOLED-001-20261122T040000Z` — **CONFIRMATORY_COMPLETE (EXECUTED).** The pooled, chronologically-split out-of-sample confirmatory design on the on-disk ironflow bulk data (`research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}`, 18 months 2025-05..2026-10, 54 files per dataset incl. sha256+accessed sidecars). Executed under `session_20261122T092003Z` (UTC > campaign start `20261122T040000Z`). Full 13-file `fclr_pooled_*` artifact set present and non-empty. Decision: NOT_SUPPORTED (funding-conditioned features add no QLIKE improvement over RV-only baseline; relative diff ~0.0%, below -2% materiality floor). Null result preserved.

**Latest completed heavy session on disk:** `session_20261122T033000Z` (UTC < campaign start `20261122T040000Z`, grandfathered) — executed the now-terminal FCLR-NEXT-SOURCE-VERIFY-01 campaign (source discovery returned NO_NEW_ADMISSIBLE_SOURCE; confirmatory design FCLR-NEXT-CONFIRM-001 registered behind an outcome-blind prereg; heavy eval triad + independent stdlib recompute + evidence audit + gate alias + non-empty trigger_check all emitted; decision GO). All earlier sessions remain terminal/grandfathered.

**Gate baseline (verified this session, 2026-11-22T09:51:12Z):** `python3 scripts/check_handoff_heavywork_gate.py` → `PASS ... reason=OK` (`latest_handoff=session_20261122T092003Z`, `latest_disk=session_20261122T092003Z`, `handoff_stale=False`, `pooled.required=True` **13 of 13 artifacts present**; `root=499/500`); all 6 gate unittest modules (`test_tracka_hardening_143`, `test_tracka_hardening_144`, `test_active_campaign_gate`, `test_fclr_heavy_confirm_gate`, `test_fclr_campaign_gate`, `test_fclr_starter_001_campaign_gate`) → **116 tests, 0 failures**; `research_state` root md+json count = **499/500**; latest on-disk session = latest recorded in this handoff (`session_20261122T092003Z`). On-disk ironflow bulk caches re-counted this session: candles_1h/funding/open_interest/liquidations each **18 parquet files + 18 sha256 sidecars + 18 accessed.json** (2025-05..2026-10, 54 files per dataset). No empty session directories exist (59 session dirs scanned). Frontier has exactly one `rank:0` (`CONFIRMATORY_COMPLETE`, task `FCLR-POOLED-001-20261122T040000Z`); every other entry is `SUPERSEDED`/`SUPERSEDED_TERMINAL` — no duplicate rank-0 deadlock and no blocked/inefficient session. HEAD = `a45b49582` (this handoff update is the only intended worktree change).

**Note on completed session `session_20261122T092003Z`:** This session (UTC `20261122T092003Z` > campaign start `20261122T040000Z`) **produced all 13 required FCLR-POOLED artifacts** under `research_state/session_20261122T092003Z/`: source registry (json+md), outcome-blind prereg freeze (json+md), heavy evaluation triad (py+json+md), independent stdlib recompute (py+json), evidence audit (json+md), gate-critical `evidence_audit_` alias (json), and non-empty `trigger_check` (json). The gate binds FCLR-POOLED-001 to this session and **passes** with the full artifact set present and non-empty.

**Environment (verified this session):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy` are NOT installed (`import numpy` → ModuleNotFoundError). `pyarrow` 26.0.1 IS already installed and is what reads the ironflow bulk parquet. Write the pooled evaluation stdlib + pyarrow only (matching the independent-recompute convention). Do NOT rely on numpy/pandas/scipy.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and any `NEXT_SESSION_TASK.md` files (none exist). All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01, FCLR-LIVE-ARCHIVE-02, and FCLR-NEXT-SOURCE-VERIFY-01) are terminal / superseded / completed — **do NOT re-run them**. The reachable-free-source frontier (NEXT-SOURCE-VERIFY-01) is executed and terminal (decision GO, NO_NEW_ADMISSIBLE_SOURCE). **FCLR-POOLED-001 is CONFIRMATORY_COMPLETE** — executed under `session_20261122T092003Z` with all 13 `fclr_pooled_*` artifacts present and non-empty; decision NOT_SUPPORTED. No remaining rank-0 heavy campaign. A future session must NOT re-run this completed campaign; per §9, no risk overlay should be built since the forecast gate did not pass.

Repository focus (per repo name **Funding-conditioned-volatility-and-liquidation-risk**): every artifact must serve the funding-conditioned volatility and liquidation-risk research pillars (RESEARCH_PROMPT.md §Mission/§3). Never drift into unrelated work, risk overlays, or live/paper trading.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T09:51:12Z)

**STATUS: FCLR-POOLED-001 CONFIRMATORY_COMPLETE — HEAVY WORK EXECUTED.** Session `session_20261122T092003Z` (UTC `20261122T092003Z` > campaign start `20261122T040000Z`) **produced all 13 required FCLR-POOLED artifacts** under `research_state/session_20261122T092003Z/`: source registry (json+md), outcome-blind prereg freeze (json+md), heavy evaluation triad (py+json+md), independent stdlib recompute (py+json), evidence audit (json+md), gate-critical `evidence_audit_` alias (json), and non-empty `trigger_check` (json). Gate passes (`python3 scripts/check_handoff_heavywork_gate.py` → PASS reason=OK).

**Result:** Pooled chronological OOS confirmatory design on ironflow bulk data (18 months 2025-05..2026-10, 799 markets, ~2.3M train / ~1.3M test rows). QLIKE B1 (RV-only) = 65.190573, QLIKE C2 (RV+funding+premium+OI) = 65.190702, diff = +0.000129, rel = +0.0002%. **Decision: NOT_SUPPORTED** — funding-conditioned features add no predictive value over the RV-only baseline; relative difference ~0.0% is far below the -2.0% materiality floor. Bootstrap CI95 includes zero. Null result preserved. Independent recompute confirms: QLIKE_B1=52.945004, QLIKE_C2=52.944664, rel=-0.0006%, NOT_SUPPORTED.

### 1a. Bottlenecks removed / verified clear

All previously-removed bottlenecks remain removed:
1. **Single rank-0 confirmed.** `research_state/experiment_frontier.json` has exactly one `rank:0` entry — `FCLR-POOLED-001-20261122T040000Z` (now CONFIRMATORY_COMPLETE). Every other entry is terminal (`SUPERSEDED*`). No duplicate rank-0 deadlock.
2. **Pooled enforcement armed and satisfied.** Gate binds FCLR-POOLED-001 via `POOLED_CAMPAIGN_RE` + `_pooled_state`; all 13 `fclr_pooled001_*` artifacts present and non-empty under `session_20261122T092003Z/`.
3. **No blocked / inefficient sessions remain.** FCLR-POOLED-001 is complete. No external trigger or new source needed.
4. **Empty-session scan clear.** All 59 on-disk `research_state/session_*` directories contain files.

### 1b. What the NEXT session should do

FCLR-POOLED-001 is **complete**. Per RESEARCH_PROMPT.md §9 (gate before any risk overlay), the forecast gate did NOT pass (NOT_SUPPORTED), so **no position-sizing/risk-reduction overlay should be built**. The next highest-value task per RESEARCH_PROMPT.md §10 priorities is **adversarial audits (priority 8)**: challenge timestamping, delisting, missingness, market stress concentration, survivorship, label construction, threshold drift, and overlapping outcomes. Also consider Track B (modeled hypothetical boundary-breach labels) per RESEARCH_PROMPT.md §15, since Track A (observed liquidation labels) is exhausted (NO_NEW_ADMISSIBLE_SOURCE).

**Suggested next actions (choose highest-value feasible):**
- Run adversarial/leakage audits on the pooled panel (future-row perturbation, split embargo integrity, funding sign/timing, mark/index alignment, missingness preservation).
- Document the NOT_SUPPORTED null result in `research_state/negative_results_report.md` (new session dir, `fclr_pooled_*` family not required — this is a different artifact).
- Verify gate still passes: `python3 scripts/check_handoff_heavywork_gate.py` → PASS.
- Run unittests: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate` → 0 failures.

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
```

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
- **Do NOT** claim completion without the full `fclr_pooled_*` artifact set under a new `session_<UTC>/` (UTC > `20261122T040000Z`), and without recording that session id in this handoff.
- **Do NOT** write a concrete future `session_<UTC>` id into this handoff before that directory exists — the gate treats the lexicographically latest recorded `session_` id as the session to verify and will fail if its directory is missing.
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as `NOT_SUPPORTED`.
- **Do NOT** re-run any terminal/completed campaign (incl. NEXT-SOURCE-VERIFY-01, LIVE-ARCHIVE-01/-02, and all earlier campaigns).
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — that trigger cannot fire on frozen data and is not a valid excuse to idle.
- **Do NOT** re-verify that `data.binance.vision` is reachable — already exhausted by FCLR-LIVE-ARCHIVE-02.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes for a post-start session only when the full `fclr_pooled_*` heavy artifact set is present and non-empty under the latest `session_<UTC>/`.

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
| **FCLR-POOLED-001** | **pooled chronological OOS confirmatory on on-disk ironflow bulk data** | **CONFIRMATORY_COMPLETE — rank-0, gate-enforced; EXECUTED under session_20261122T092003Z; all 13 fclr_pooled_* artifacts present and non-empty; decision NOT_SUPPORTED (rel QLIKE ~0.0%, below -2% floor)** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this `AGENT_HANDOFF.md` with: (1) what changed and why; (2) what was tested with exact outcomes; (3) what evidence was added and where (full paths); (4) the state of each research gate; (5) the single highest-value next task; (6) the precise verifying command; (7) any blocker with the next materially different route. **Rank-0: FCLR-POOLED-001 (CONFIRMATORY_COMPLETE) — executed under session_20261122T092003Z; decision NOT_SUPPORTED; no overlay per §9 gate.** All 13 artifacts under `research_state/session_20261122T092003Z/` with the `fclr_pooled_*` family. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py                  # → PASS reason=OK (FCLR-POOLED-001 bound; post-start session must carry the full fclr_pooled_* heavy artifact set under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                          # frozen 3-block domains exhausted (does NOT cover the pooled design — that is the point)
```

After the next heavy session writes its first artifact (UTC > `20261122T040000Z`) and records the new `session_<UTC>/` in this handoff, re-run `check_handoff_heavywork_gate.py`: it must PASS, and now only because the full `fclr_pooled_*` heavy artifact set is present and non-empty under the latest `session_<UTC>/`. A source-probe-only, trigger-only, audit-only, or verify-and-stop session will trip the gate and fail closed.

(End of handoff)