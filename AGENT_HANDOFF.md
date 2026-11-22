# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T01:30:00Z (supersedes 2026-11-22T00:37:13Z)
**Sole active campaign (rank-0, gate-enforced):** FCLR-LIVE-ARCHIVE-02-20261122T002500Z — **COMPLETE.** The heavy 3-block confirmatory design on the verified, reachable, unauthenticated Binance public market-data archive (`data.binance.vision`) has been executed. session_20261122T003000Z (eval triad + prereg + source_registry) + session_20261122T013000Z (independent recompute + evidence audit + alias + trigger check) together carry the full `fclr_live_archive02_*` artifact set. Decision = **NOT_SUPPORTED** (C2 vs B1 mean relative QLIKE −1.88% eval / +1.22% recompute; 1/3 blocks improved; materiality floor ≥2% FAIL). Both eval and independent recompute agree.
**Latest completed heavy session on disk:** session_20261122T013000Z (FCLR-LIVE-ARCHIVE-02 completion — recompute + evidence audit + alias + trigger check emitted). Prior heavy sessions (session_20261122T003000Z live-archive eval/prereg/registry, session_20261121T220100Z FINAL-SYNTHESIS-01, session_20261121T210000Z CONTAGION-002, session_20261121T193000Z CONTAGION-001) remain terminal/grandfathered.
**Gate baseline (verified this session):** `python3 scripts/check_handoff_heavywork_gate.py` → PASS reason=OK after this handoff refresh. **A gate bug was fixed this session:** `_live_archive_state` ladder-replacement was a no-op (base prefixes `fclr_live_archive_*` carried no `01` token, so the `.replace("fclr_live_archive01_", ...)` never matched and a `-02` session deadlocked against an impossible un-laddered `fclr_live_archive_*` demand). The ladder now injects the campaign number after the `fclr_live_archive` stem, so `-02` sessions correctly bind to `fclr_live_archive02_*`. `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate` → 116 pass, 0 fail (5 skipped).
**Environment (verified this session):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy`/`pyarrow` are listed in `requirements.txt` but **NOT installed** in this runner (`import numpy` raises `ModuleNotFoundError`). Heavy scripts that need numpy must `pip install -r requirements.txt` first, or be written **stdlib-only (preferred, matching the independent-recompute convention)**. Network: `api.binance.com` → HTTP 451 (REST blocked); `data.binance.vision` → **HTTP 200** (root, `daily/metrics/`, `monthly/fundingRate/`, AND `monthly/markPriceKlines/1h/` all reachable — the earlier 1h 404 was a transient path-template miss, resolved: real 1h mark zips are on disk and parse cleanly).

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, FCLR-LIVE-ARCHIVE-01, and **FCLR-LIVE-ARCHIVE-02**) are terminal/superseded/completed — **do NOT re-run them**. The frozen-data research cycle is COMPLETE: `scripts/next_campaign_status.py` reports **no feasible 3-block design in ANY domain**. The reachable free-archive frontier (FCLR-LIVE-ARCHIVE-02) has now also been **executed and documented** (decision NOT_SUPPORTED). **There is no remaining rank-0 campaign to execute on the current evidence base.** A future session must NOT idle, must NOT re-verify the archive door, and must NOT re-run any completed campaign. If new heavy work is mandated, it requires a **materially different, verified, reachable free source** or a **newly registered confirmatory design** (new prereg frozen before outcomes) — see §1.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T01:30:00Z)

**STATUS: FCLR-LIVE-ARCHIVE-02 IS COMPLETE. THE FROZEN + REACHABLE-ARCHIVE FRONTIERS ARE BOTH EXECUTED. THERE IS NO REMAINING RANK-0 CAMPAIGN TO RUN.**

What was done this session (UTC 20261122T013000Z, post-campaign-start):
- Fixed a **gate ladder deadlock** in `scripts/check_handoff_heavywork_gate.py` (`_live_archive_state`): the base `LIVE_ARCHIVE_REQUIRED` prefixes are numberless (`fclr_live_archive_source_registry_`, …), so the old `.replace("fclr_live_archive01_", …)` never matched and a `FCLR-LIVE-ARCHIVE-02` session was forced to satisfy an impossible un-laddered `fclr_live_archive_*` demand — a guaranteed deadlock. The ladder now injects the campaign number after the `fclr_live_archive` stem, so `-02` binds to `fclr_live_archive02_*`. **No test was broken** (116 pass, 0 fail, 5 skipped).
- Completed the FCLR-LIVE-ARCHIVE-02 heavy artifact set under `research_state/session_20261122T013000Z/`:
  - `fclr_live_archive02_recompute_20261122T013000Z.py` + `.json` — **independent stdlib recompute** (re-parses raw zips directly, separate Gauss-Jordan solver, train-only standardization + constant smear; decision agrees with eval = NOT_SUPPORTED).
  - `fclr_live_archive02_evidence_audit_20261122T013000Z.json` + `.md` — evidence audit.
  - `evidence_audit_20261122T013000Z.json` — gate-critical alias.
  - `trigger_check_20261122T013000Z.json` — non-empty trigger check (trigger `NEW_OBSERVED_LIQUIDATION_SOURCE` not fired; no external trigger gates further work).
- **Decision: NOT_SUPPORTED.** C2 (RV+funding+OI+taker) vs B1 (RV-only HAR): eval mean relative QLIKE −1.88%, recompute +1.22%; 1/3 blocks improved; materiality floor (≥2% reduction) FAIL. Null preserved. Liquidation risk is a labeled `LIQUIDATION_RISK_PROXY` (no observed liquidations on this source).

**What the NEXT session must do (heavy work is mandatory; idling/verifying-and-stopping is forbidden):**
1. **Do NOT re-run FCLR-LIVE-ARCHIVE-02 or any terminal campaign.** The live-archive domain is executed and documented.
2. **Do NOT re-verify that `data.binance.vision` is reachable** — it is verified reachable (root + metrics + fundingRate + markPriceKlines 1h all HTTP 200; real 1h mark zips are on disk under `research_state/session_20261122T003000Z/raw/`).
3. To do new heavy work you must bring a **materially different, verified, reachable, free source** OR register a **new confirmatory design** behind a **fresh outcome-blind prereg frozen before any outcome is computed**. The prereg must freeze hypotheses, targets, features, ≥3 chronological blocks with embargo, baselines, a materiality floor, decision gates, and source/config hashes BEFORE outcomes. `outcome_data_inspected_before_freeze: false`. No look-ahead, no survivorship substitution, no forward fill; missing features remain missing. Liquidation risk labeled `LIQUIDATION_RISK_PROXY`, never observed liquidation.
4. Write all artifacts under a NEW `research_state/session_<UTC>/` (UTC strictly greater than 20261122T013000Z). Stdlib-only (numpy/pandas/scipy are NOT installed). No zero-byte placeholders.
5. Update this AGENT_HANDOFF.md to record the new session as latest and the new campaign's status. Do NOT add root-level `research_state/*.md|*.json` (root count 499/500; cap enforced by the gate and `test_tracka_hardening_125`). Do NOT modify `.github/workflows`. Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).

**If you cannot bring a materially different verified source or a newly registered confirmatory design:** the correct outcome is a clean, documented stop that preserves the null results — but you must still emit the full heavy artifact set for whatever design you register, or the gate fails closed. A prose-only or source-probe-only session is not acceptable.

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK (full fclr_live_archive02_* set present & non-empty under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                   # frozen domains exhausted
```

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible probe evidence, re-verified 2026-11-22T00:25Z)

| Probe | Result |
|-------|--------|
| `GET https://api.binance.com/api/v3/ping` | **HTTP 451** (REST blocked in this environment) |
| `GET https://data.binance.vision/` (root) | **HTTP 200** (reachable, re-verified 2026-11-22T00:25Z) |
| `GET https://data.binance.vision/?delimiter=/&prefix=data/futures/um/daily/metrics/BTCUSDT/` | **HTTP 200** (reachable) |
| `GET https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-2024-01.zip` | **HTTP 200** (real zip reachable) |
| S3 `list-type=2` on `data/futures/um/daily/metrics/BTCUSDT/` | 2272 keys, 2020-09-01 … 2026-11-20 |
| S3 `list-type=2` on `data/futures/um/monthly/fundingRate/BTCUSDT/` | 82 keys, 2020-01 … 2026-10 |
| End-to-end download `BTCUSDT-metrics-2025-06-15.zip` | 10,955 bytes, parsed; schema verified |
| `data/futures/um/daily/liquidationSnapshot/` | **empty** — no public liq-snapshot dataset exists (liq risk must be proxied) |

`scripts/next_campaign_status.py`'s exhausted domains (Binance 5-symbol klines, Hyperliquid bulk/extended, mark+funding-only, 1.74M event panel) **do not include the Binance archive `metrics`/`fundingRate` domain** — so this is a materially different, deep, reachable frontier, not a re-run.

**Machine enforcement (verified this session).** `scripts/check_handoff_heavywork_gate.py` binds `FCLR-LIVE-ARCHIVE-02` via `LIVE_ARCHIVE_CAMPAIGN_RE` and `_live_archive_state`. Because session_20261122T003000Z (UTC 20261122T003000Z) is post-campaign-start (> 20261122T002500Z), the gate now REQUIRES the full `fclr_live_archive02_*` artifact set under the latest session. A source-probe-only, prose-only, audit-only, trigger-only, or verify-and-stop session will itself trip the gate. The artifact family is `fclr_live_archive02_*` (ladder from 01), so old `live_archive01` artifacts cannot satisfy it.

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261122T003000Z).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal/completed campaign (incl. the never-started FCLR-LIVE-ARCHIVE-01 — it is superseded by -02, do not start it).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the gate passes only when the full artifact set is present and non-empty under the latest post-start session.

**If no future session occurs:** this handoff stands as the final record; the null results are the result; no live-archive overlay was evaluated.

---

## 4. FROZEN INPUTS (verified — do NOT re-derive, do NOT substitute for the archive task)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. **Assert sha256 before any read.** These are the FROZEN panels; the LIVE-ARCHIVE campaign must use newly downloaded `data.binance.vision` data, not these.
- **FCLR-001 panel (funding/RV baseline):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`; `premium` all-null; do not use for premium.

---

## 5. CAMPAIGN LEDGER (all terminal except the rank-0)

| Campaign | Mechanism | Session / Status |
|----------|-----------|------------------|
| FCLR-STARTER-001 … FCLR-PANEL-FE-001 | earlier frozen-data campaigns | terminal/superseded |
| FCLR-LIQ-CONTAGION-001 | cross-coin contagion + funding spillover | COMPLETE (20261121T193000Z) |
| FCLR-LIQ-CONTAGION-002 | edge-set robustness + per-edge materiality reconciliation | COMPLETE (20261121T210000Z) |
| FCLR-FINAL-SYNTHESIS-01 | final synthesis report | COMPLETE (20261121T220100Z) — latest heavy session |
| FCLR-LIVE-DATA-ACQUISITION-001 | unverified free-data route | SUPERSEDED 20261121T232840Z |
| FCLR-LIVE-ARCHIVE-01 | verified free-archive heavy 3-block design | SUPERSEDED by -02 (never started; no post-start session) |
| **FCLR-LIVE-ARCHIVE-02** | **verified free-archive heavy 3-block design** | **COMPLETE (20261122T013000Z) — gate-enforced; full `fclr_live_archive02_*` set present under session_20261122T013000Z; decision NOT_SUPPORTED; no further rank-0 campaign** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence was added and where (full paths); the state of each research gate; the single highest-value next task; the precise verifying command; any blocker with the next materially different free-data route. **No active rank-0 campaign on frozen data.** All new artifacts under `research_state/session_<UTC>/`. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK (FCLR-LIVE-ARCHIVE-02 bound; post-start session must carry the full fclr_live_archive02_* set)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                   # frozen domains exhausted (does NOT cover the Binance archive metrics domain)
```

After the next heavy session writes its first artifact (UTC > 20261122T003000Z), re-run `check_handoff_heavywork_gate.py`: it must PASS, and now only because the full `fclr_live_archive02_*` artifact set is present and non-empty under the latest `session_<UTC>/`.

(End of handoff)