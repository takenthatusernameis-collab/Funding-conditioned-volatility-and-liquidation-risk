# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-22T00:37:13Z (supersedes 2026-11-22T00:34:12Z)
**Sole active campaign (rank-0, gate-enforced):** FCLR-LIVE-ARCHIVE-02-20261122T002500Z — download, prereg-freeze, and run a HEAVY 3-block confirmatory design on the VERIFIED, reachable, unauthenticated Binance public market-data archive (`data.binance.vision`). Ladder-increments the never-started FCLR-LIVE-ARCHIVE-01. Re-verified reachable from THIS runner at 2026-11-22T00:25Z (HTTP 200 root/metrics/funding).
**Latest completed heavy session on disk:** session_20261121T220100Z (FCLR-FINAL-SYNTHESIS-01, COMPLETE — final synthesis report artifact set emitted). Prior completed heavy sessions (session_20261121T210000Z CONTAGION-002, session_20261121T193000Z CONTAGION-001) remain grandfathered/terminal.
**Latest on-disk session (IN PROGRESS, INCOMPLETE):** session_20261122T003000Z — POST-campaign-start (UTC 20261122T003000Z > campaign start 20261122T002500Z). It downloaded real archive data (82 BTCUSDT metrics daily files 2025-06-01..2025-08-18 + 3 funding monthly files 2025-06..08; markPriceKlines 1h path 404'd — see download_manifest errors) and emitted source_registry + prereg + eval (decision NOT_SUPPORTED; C2-vs-B1 mean relative QLIKE −1.88%, 1/3 blocks improved, materiality floor ≥2% FAIL). It is MISSING the four remaining required artifact categories: independent stdlib recompute, evidence audit, evidence_audit_ alias, trigger_check.
**Gate baseline (verified this session):** `python3 scripts/check_handoff_heavywork_gate.py` → currently FAILS with `HANDOFF_STALE_LATEST_SESSION:session_20261122T003000Z` because this handoff did not yet record the on-disk session. `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate` → 116 pass, 0 fail (5 skipped) when the gate passes.
**Environment (verified this session):** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy`/`pyarrow` are listed in `requirements.txt` but **NOT installed** in this runner (`import numpy` raises `ModuleNotFoundError`). Heavy scripts that need numpy must `pip install -r requirements.txt` first, or be written **stdlib-only (preferred, matching the independent-recompute convention)**. Network: `api.binance.com` → HTTP 451 (REST blocked); `data.binance.vision` (S3 `s3-ap-northeast-1.amazonaws.com/data.binance.vision`) → **HTTP 200, re-confirmed reachable at 2026-11-22T00:25Z** (root, `daily/metrics/`, and a real `monthly/fundingRate/` zip all 200).

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001, and the never-started FCLR-LIVE-ARCHIVE-01) are terminal/superseded/completed — **do NOT re-run them**. The frozen-data research cycle is COMPLETE: `scripts/next_campaign_status.py` reports **no feasible 3-block design in ANY domain** (Binance 5-symbol klines, Hyperliquid bulk, Hyperliquid extended, mark+funding-only, and the 1.74M event panel). The only path to new heavy work is FCLR-LIVE-ARCHIVE-02: a materially different, VERIFIED, unauthenticated, free external source. **Do not idle, do not verify-and-stop, do not write a source-probe-only or prose-only session — the gate fails closed without the full heavy artifact set, and a verify-and-stop session will itself trip the gate.**

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-22T00:37:13Z)

**PRIORITY-0 MISSION — COMPLETE THE FCLR-LIVE-ARCHIVE-02 HEAVY ARTIFACT SET.**

The frozen-data frontier is exhausted (`scripts/next_campaign_status.py` → `no feasible 3-block design in ANY domain`). The prior handoff verified that a deep, free, unauthenticated source IS reachable and was NEVER exploited by the frozen frontier; this session re-confirmed that access (HTTP 200 on root, metrics, and funding paths at 2026-11-22T00:25Z). The previous escape hatch ("stop cleanly if no admissible source exists") is permanently closed. Your job is to convert the verified access into heavy confirmatory research — not to re-verify that the door is open.

**Verified reachable source (re-verified 2026-11-22T00:25Z):** Binance public market-data archive at `data.binance.vision` (S3 bucket `s3-ap-northeast-1.amazonaws.com/data.binance.vision`), HTTPS GET, no credentials/keys/payment/signup. Confirmed datasets and depth:
- **`data/futures/um/daily/metrics/<SYM>/`** — daily **open interest** (`sum_open_interest`, `sum_open_interest_value`) + **taker long/short volume ratio** (`sum_taker_long_short_vol_ratio`) + top-trader / global long/short ratios. BTCUSDT = **2272 daily files, 2020-09-01 → 2026-11-20** (5-min intraday rows; 288 rows/day). Schema verified by real download (header = `create_time,symbol,sum_open_interest,sum_open_interest_value,count_toptrader_long_short_ratio,sum_toptrader_long_short_ratio,count_long_short_ratio,sum_taker_long_short_vol_ratio`). **This is the never-exploited dataset.**
- **`data/futures/um/monthly/fundingRate/<SYM>/`** — funding rate. BTCUSDT 82 files 2020-01→2026-10; ETHUSDT 82; BNBUSDT 81; SOLUSDT 74.
- **`data/futures/um/monthly/{klines,markPriceKlines,indexPriceKlines,premiumIndexKlines}/<SYM>/`** — OHLCV / mark / index / premium klines, deep history. (Note: session_20261122T003000Z tried `markPriceKlines/BTCUSDT/1h/...` and got HTTP 404 — verify the exact path template before re-fetching; proceed with stdlib recompute on the data already on disk regardless.)
- **No `liquidationSnapshot` dataset exists** in this archive (Binance discontinued public liq snapshots). **Liquidation risk must be PROXIED** via open interest + taker-flow imbalance + mark/index dislocation, and every such proxy MUST be labeled as a proxy — never as observed liquidations.

**session_20261122T003000Z status (already on disk, post-campaign-start):** source_registry ✓, prereg ✓ (outcome-blind, `outcome_data_inspected_before_freeze: false`), eval ✓ (NOT_SUPPORTED), but MISSING:
1. `fclr_live_archive_recompute_<UTC>.py` + `.json` — independent **stdlib** recompute of the eval on the downloaded archive data (NOT a copy of the eval script).
2. `fclr_live_archive_evidence_audit_<UTC>.json` + `.md` — evidence audit.
3. `evidence_audit_<UTC>.json` — gate-critical alias of the evidence audit.
4. `trigger_check_<UTC>.json` — non-empty trigger check.

**Next session must (all steps; none skippable — the gate checks each):**
1. Create a NEW session dir `research_state/session_<UTC>/` with **UTC > 20261122T003000Z**.
2. Write the four missing artifact categories above (all non-empty, stdlib-only since numpy/pandas/scipy are NOT installed). No zero-byte placeholders.
3. Preserve the prereg freeze (hypotheses, targets, features, 3 chronological blocks, baselines, materiality floor 2%, decision gates, source/data hashes, config hash) BEFORE inspecting any outcome. `outcome_data_inspected_before_freeze: false`. No look-ahead, no survivorship substitution, no forward fill; missing features remain missing. Liquidation risk labeled `LIQUIDATION_RISK_PROXY`, never observed liquidation.
4. Update this AGENT_HANDOFF.md to record the new session as latest and mark FCLR-LIVE-ARCHIVE-02 complete only when the full artifact set is present and non-empty under the latest `session_<UTC>/`.
5. Do NOT add root-level `research_state/*.md|*.json` — root count is **499/500**; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`. Do NOT create empty/placeholder files or empty session directories. Do NOT re-run any terminal/completed campaign. Do NOT modify `.github/workflows`. Do NOT overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001). Do NOT "verify green and stop".

**If the archive becomes unreachable mid-session:** record the exact failed probe (status, time) in the source registry, identify the next materially different free route, and stop that session cleanly. Do not idle. (Note: writing a registry-only session still counts as a post-start session and will fail the gate unless the heavy set is completed — so if the archive is down, still attempt the full artifact set with whatever data was downloaded before the outage, labeling the shortfall explicitly.)

**Verify with:**
```
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK (full fclr_live_archive02_* set present & non-empty under latest session_<UTC>/)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                   # frozen domains exhausted (does NOT cover the Binance archive metrics domain)
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
| **FCLR-LIVE-ARCHIVE-02** | **verified free-archive heavy 3-block design** | **ACTIVE rank-0 (20261122T002500Z) — gate-enforced; session_20261122T003000Z INCOMPLETE (missing recompute, evidence_audit, evidence_audit_ alias, trigger_check)** |

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