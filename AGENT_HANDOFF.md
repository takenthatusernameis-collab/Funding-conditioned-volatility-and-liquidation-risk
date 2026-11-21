# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T23:28:40Z (supersedes 2026-11-21T23:25:36Z)
**Sole active campaign (rank-0, gate-enforced):** FCLR-LIVE-ARCHIVE-01-20261121T232840Z — download, prereg-freeze, and run a HEAVY 3-block confirmatory design on the VERIFIED, reachable, unauthenticated Binance public market-data archive (data.binance.vision). The prior handoff's claim that "no admissible free source exists / you may stop cleanly" is FALSE and is corrected here with reproducible probe evidence.
**Latest completed heavy session on disk:** session_20261121T220100Z (FCLR-FINAL-SYNTHESIS-01, COMPLETE — final synthesis report artifact set emitted). Prior completed heavy sessions (session_20261121T210000Z CONTAGION-002, session_20261121T193000Z CONTAGION-001) remain grandfathered/terminal.
**Gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`, `root=499/500`, `heavy_session=session_20261121T220100Z`). `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate` → 116 pass, 0 fail (5 skipped).
**Environment:** Python 3.12.3 at `/usr/bin/python3`. `numpy`/`pandas`/`scipy`/`pyarrow` are listed in `requirements.txt` but **not installed in this runner** (the prior handoff's "verified importable" note was inaccurate for this environment — `import numpy` raises `ModuleNotFoundError`). Any heavy script that needs numpy must `pip install -r requirements.txt` first, or be written stdlib-only (preferred, matching the independent-recompute convention). Network: `api.binance.com` → HTTP 451 (blocked); `data.binance.vision` (S3 `s3-ap-northeast-1.amazonaws.com/data.binance.vision`) → HTTP 200 (reachable, unauthenticated).

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01, FCLR-LIVE-DATA-ACQUISITION-001) are terminal/superseded/completed — **do NOT re-run them**. The frozen-data research cycle is COMPLETE (no feasible 3-block design in any FROZEN domain). The only path to new heavy work is FCLR-LIVE-ARCHIVE-01: a materially different, VERIFIED, unauthenticated, free external source. **Do not idle, do not verify-and-stop, do not write a source-probe-only or prose-only session — the gate fails closed without the full heavy artifact set.**

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T23:28:40Z)

**PRIORITY-0 MISSION — EXECUTE FCLR-LIVE-ARCHIVE-01 ON THE VERIFIED FREE ARCHIVE.**
The frozen-data frontier is exhausted (`next_campaign_status.py` → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN across Binance 5-symbol klines, Hyperliquid bulk, Hyperliquid extended, and the 1.74M event panel). The previous handoff left the live-data route UNVERIFIED and told agents they could "stop cleanly if no admissible source exists." **That escape hatch is now closed.** This session verified, reproducibly, that a deep, free, unauthenticated source IS reachable and was NEVER exploited by the frozen frontier. Your job is to convert that verified access into heavy confirmatory research — not to re-verify that the door is open.

**Verified reachable source (evidence in §2):** Binance public market-data archive at `data.binance.vision` (S3 bucket `s3-ap-northeast-1.amazonaws.com/data.binance.vision`), HTTPS GET, no credentials/keys/payment/signup. Confirmed datasets and depth:
- **`data/futures/um/daily/metrics/<SYM>/`** — daily **open interest** (`sum_open_interest`, `sum_open_interest_value`) + **taker long/short volume ratio** (`sum_taker_long_short_vol_ratio`) + top-trader / global long/short ratios. BTCUSDT = **2272 daily files, 2020-09-01 → 2026-11-20** (5-min intraday rows; 289 rows/day). Schema verified by real download (11,561 bytes, parsed). **This is the never-exploited dataset.**
- **`data/futures/um/monthly/fundingRate/<SYM>/`** — funding rate. BTCUSDT 82 files 2020-01→2026-10; ETHUSDT 82; BNBUSDT 81; SOLUSDT 74.
- **`data/futures/um/monthly/{klines,markPriceKlines,indexPriceKlines,premiumIndexKlines}/<SYM>/`** — OHLCV / mark / index / premium klines, deep history.
- **No `liquidationSnapshot` dataset exists** in this archive (Binance discontinued public liq snapshots). **Liquidation risk must be PROXIED** via open interest + taker-flow imbalance + mark/index dislocation, and every such proxy MUST be labeled as a proxy — never as observed liquidations.

**Next session must (all three steps; none skippable):**
**(a) Source registry + verified-download evidence.** Record the download probe (path, ETag/sha256, earliest/latest timestamp, cadence, symbol coverage, gaps, license/terms) in `research_state/data_source_registry.json` AND a per-campaign artifact `fclr_live_archive_source_registry_<UTC>.{json,md}` under `research_state/session_<UTC>/` (UTC > 20261121T232840Z). This is EVIDENCE of a working download, not a substitute for the heavy design. Do NOT bypass access controls, rate limits, or terms; do NOT use any source requiring payment/signup/keys.

**(b) Outcome-blind prereg freeze.** Freeze hypotheses, targets, features, 3 chronological blocks, baselines, materiality floor (2%), and decision gates BEFORE inspecting any outcome on the newly downloaded archive data. Assert source/data hashes and config hash; `outcome_data_inspected_before_freeze: false`. Artifacts: `fclr_live_archive_prereg_<UTC>.{json,md}`.

**(c) Heavy 3-block confirmatory design.** Execute the pre-registered design on the archive data with non-empty artifacts under `research_state/session_<UTC>/` (UTC > 20261121T232840Z): evaluation triad `fclr_live_archive_eval_<UTC>.{py,json,md}`; independent stdlib recompute `fclr_live_archive_recompute_<UTC>.{py,json}`; evidence audit `fclr_live_archive_evidence_audit_<UTC>.{json,md}` + gate-critical alias `evidence_audit_<UTC>.json`; and `trigger_check_<UTC>.json`. No zero-byte placeholders.

---

## 2. WHY THIS CAMPAIGN CANNOT BE AVOIDED (reproducible probe evidence, 2026-11-21T23:2x Z)

| Probe | Result |
|-------|--------|
| `GET https://api.binance.com/api/v3/ping` | **HTTP 451** (REST blocked in this environment) |
| `GET https://data.binance.vision/...` | **HTTP 200** (reachable) |
| S3 `list-type=2` on `data/futures/um/daily/metrics/BTCUSDT/` | 2272 keys, 2020-09-01 … 2026-11-20 |
| S3 `list-type=2` on `data/futures/um/monthly/fundingRate/BTCUSDT/` | 82 keys, 2020-01 … 2026-10 |
| End-to-end download `SOLUSDT-metrics-2025-06-15.zip` | 11,561 bytes, parsed; header = `create_time,symbol,sum_open_interest,sum_open_interest_value,count_toptrader_long_short_ratio,sum_toptrader_long_short_ratio,count_long_short_ratio,sum_taker_long_short_vol_ratio` |
| `data/futures/um/daily/liquidationSnapshot/` | **empty** — no public liq-snapshot dataset exists (liq risk must be proxied) |

`next_campaign_status.py`'s exhausted domains (Binance 5-symbol klines, Hyperliquid bulk/extended, the 1.74M event panel) **do not include the Binance archive `metrics`/`fundingRate` domain** — so this is a materially different, deep, reachable frontier, not a re-run.

**Machine enforcement.** `scripts/check_handoff_heavywork_gate.py` now binds `FCLR-LIVE-ARCHIVE-01` (`_live_archive_state`). Once a post-start session exists (UTC > 20261121T232840Z), the gate FAILS CLOSED unless the full artifact set in §1(c) is present and non-empty. A source-probe-only, prose-only, audit-only, trigger-only, or verify-and-stop session does NOT satisfy the gate.

---

## 3. NON-AVOIDANCE CONSTRAINTS (machine-checked)

- **Do NOT** create root-level `research_state/*.md|*.json` — root count is 499/500; the cap is enforced by the gate and `test_tracka_hardening_125`. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261121T232840Z).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal/completed campaign.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" — the frozen-data gate passes BECAUSE no heavy frozen work remains; the live-archive gate does NOT pass until the heavy design is emitted.

**If the archive becomes unreachable mid-session:** record the exact failed probe (status, time) in the source registry, identify the next materially different free route, and stop that session cleanly. Do not idle.

**If no future session occurs:** this handoff stands as the final record; the null results are the result; no overlay was evaluated.

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
| FCLR-LIVE-DATA-ACQUISITION-001 | unverified free-data route | SUPERSEDED 20261121T232840Z (escape hatch closed) |
| **FCLR-LIVE-ARCHIVE-01** | **verified free-archive heavy 3-block design** | **ACTIVE rank-0 (20261121T232840Z) — gate-enforced** |

---

## 6. PER-SESSION CLOSE-OUT (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence was added and where (full paths); the state of each research gate; the single highest-value next task; the precise verifying command; any blocker with the next materially different free-data route. **No active rank-0 campaign on frozen data.** All new artifacts under `research_state/session_<UTC>/`. Commit nothing merely to show activity.

---

## 7. ACCEPTANCE — THE GATE

```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK (FCLR-LIVE-ARCHIVE-01 bound; grandfathered until a post-start session exists)
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144 tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate tests.test_fclr_campaign_gate tests.test_fclr_starter_001_campaign_gate
python3 scripts/next_campaign_status.py                   # frozen domains exhausted (does NOT cover the Binance archive metrics domain)
```

(End of handoff)