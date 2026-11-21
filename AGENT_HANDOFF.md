# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Timestamp:** 2026-11-21T22:25:40Z (supersedes 2026-11-21T22:23:41Z)
**Sole active campaign:** FCLR-LIVE-DATA-ACQUISITION-001 — open a materially different free-data route (live/unfrozen external sources, no credentials) so heavy research can continue; frozen-data frontier exhausted, no re-runs permitted.
**Latest completed heavy session on disk:** session_20261121T220100Z (FCLR-FINAL-SYNTHESIS-01, COMPLETE — final synthesis report artifact set emitted). session_20261121T210000Z (FCLR-LIQ-CONTAGION-002, COMPLETE — full artifact set emitted) remains the heavy-session bundle of record. session_20261121T193000Z (FCLR-LIQ-CONTAGION-001, COMPLETE) remains grandfathered.
**Gate baseline:** `python3 scripts/check_handoff_heavywork_gate.py` → PASS (`reason=OK`, `root=499/500`). `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144` → 68 pass, 0 fail. `python3 scripts/next_campaign_status.py` → confirms CONTAGION-002 executed; **CAMPAIGN STATUS: no feasible 3-block design in ANY domain** (Binance 5-symbol, Hyperliquid bulk, Hyperliquid extended all exhausted).
**Environment:** Python 3.12.3; `numpy 2.5.5`, `pandas 3.1.1`, `scipy 1.18.1`, `pyarrow 26.0.1` verified importable.

---

> **SINGLE DURABLE HANDOFF.** This supersedes all prior handoffs and `NEXT_SESSION_TASK.md` files. All prior campaigns (STARTER-001, FCLR-001, FCLR-XSEC-001..008, LIQ-XSEC-QLIKE/ORDERING, LIQ-COMBINED-PANEL, FCLR-LIQ-OOS-FORECAST-001, FCLR-BOUNDED-TRIGGER-ONLY, FCLR-SESSION-SYNTHESIS-01, FCLR-PANEL-FE-001, Track A/B/C, FCLR-LIQ-CONTAGION-001, FCLR-LIQ-CONTAGION-002, FCLR-FINAL-SYNTHESIS-01) are terminal/superseded/completed — **do NOT re-run them**. The final synthesis campaign FCLR-FINAL-SYNTHESIS-01 is COMPLETE under `session_20261121T220100Z/`. The frozen-data research cycle is COMPLETE. No session may idle on a trigger that cannot fire inside this closed frozen-data environment. The only remaining path to heavy work is FCLR-LIVE-DATA-ACQUISITION-001: a materially different, unauthenticated, free external data source.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-21T22:25:40Z)

**PRIORITY-0 MISSION — OPEN A MATERIALLY DIFFERENT FREE-DATA ROUTE (FCLR-LIVE-DATA-ACQUISITION-001).** Frozen-data frontier is exhausted: `next_campaign_status.py` confirms **no feasible 3-block design in ANY domain** — Binance 5-symbol cache, ironflow Hyperliquid bulk cache (candles+funding+OI+observed liq), and extended Hyperliquid stores (candles+funding+observed liq events) are all exhausted. Every frozen prereg has an evaluation artifact. The research frontier on frozen data is closed. Future sessions must NOT re-run terminal campaigns or idle on frozen data.

Next session must:
**(a) Discover and verify a new admissible free source** — live/unfrozen external data, unauthenticated, no credentials, no paid plans, no manual downloads, no user-provided files. Verify the actual unauthenticated download path, history depth, schema, licensing, and limits before integrating (RESEARCH_PROMPT.md §5, §7). Candidate families: official Binance public market-data archive (github.com/binance/binance-public-data, data.binance.vision), public unauthenticated exchange APIs (historical funding/mark/index/klines/OI), public GitHub/Zenodo/Hugging Face/institutional archives with downloadable historical liquidation/event records without signup or keys. Do NOT assume a REST endpoint returning recent records provides complete historical labels; a live-only stream does not reconstruct the past.

**(b) Freeze a prereg with outcome-blind hypotheses on that new data** — preregister before any outcome inspection; `outcome_data_inspected_before_freeze: false`; assert source/data hashes; record earliest/latest timestamp, cadence, symbol coverage, gaps.

**(c) Execute a heavy 3-block design with non-empty artifacts** under `research_state/session_<UTC>/` (UTC > 20261121T220100Z). Non-avoidance constraints: no prose-only/trigger-only/audit-only/verify-and-stop/placeholder sessions; root cap 499/500; no empty files or empty session dirs; no threshold-shopping or relaxing the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED; do NOT re-run any terminal campaign; do NOT modify `.github/workflows`; do NOT overwrite `research_state/research_protocol.md`.

---

**Completed: FCLR-FINAL-SYNTHESIS-01 (final synthesis report) — COMPLETE under `session_20261121T220100Z/`**

Final synthesis campaign executed (UTC > 20261121T210000Z), all non-empty:
- `fclr_final_synthesis_report_20261121T220100Z.md` — full synthesis report
- `fclr_final_synthesis_report_20261121T220100Z.json` — manifest
- `evidence_audit_20261121T220100Z.json` — evidence audit of the synthesis session
- `recompute_20261121T220100Z.json` — independent verification of cited CONTAGION-002 statistics
- `trigger_check_20261121T220100Z.json` — trigger check (no external trigger required)

**Forecast gate:** NOT PASSED for any primary volatility or liquidation target (FCLR-H001..H004 all NOT_SUPPORTED / DATA_BLOCKED). No risk overlay was or could be evaluated (RESEARCH_PROMPT.md §9). All nulls and inconclusive results preserved per §7, §12, §20.

**What was completed this cycle (final heavy session: session_20261121T210000Z):**
1. **Prereg freeze (outcome-blind):** `fclr_liq_contagion02_prereg_20261121T210000Z.json` + `.md` — H_recon_materiality, H_recon_robustness, H_recon_stability; materiality_floor 0.02; panel sha256 asserted; outcome_data_inspected_before_freeze: false.
2. **Reconciliation evaluation (HEAVY, executed):** `fclr_liq_contagion02_recon_20261121T210000Z.py` + `.json` + `.md`. All 210 directed pairs: per-edge variance_explained (12/210 clear the 0.02 floor; bootstrap CI [6,19]; mean 0.0063, median 0.0039); four-criterion ladder raw=184/Bonferroni=156/BH-FDR=199/permutation=102; pairwise Jaccard 0.5126–0.9246; eval-vs-recompute disagreement (47 of 210 pairs); funding-tercile reconciliation; 90d/30d rolling stability; block-bootstrap stability (1000 resamples; 12 stable edges; mean freq 0.6722).
3. **Independent recompute:** `fclr_liq_contagion02_recompute_20261121T210000Z.py` + `.json` — separate stdlib/numpy code path; n_clearing=15/210, n_stable=0/210, `recompute_concurs_with_recon: false` (honestly reported discrepancy).
4. **Evidence audit:** `fclr_liq_contagion02_evidence_audit_20261121T210000Z.json` + `.md`, plus gate-critical alias `evidence_audit_20261121T210000Z.json`.
5. **Trigger check:** `trigger_check_20261121T210000Z.json` — `required: false` (no external trigger).

**Hypothesis verdicts:** H_recon_materiality=SUPPORTED; H_recon_robustness=SUPPORTED; H_recon_stability=SUPPORTED.

**Full campaign ledger (all terminal):**
| Campaign | Mechanism | Session | Verdict / Status |
|----------|-----------|---------|------------------|
| FCLR-STARTER-001 | Time-series 24h forward RV (B0/B1/C1/C2) | 20261120T052201Z | NOT_SUPPORTED (terminal) |
| FCLR-XSEC-001..008 | Pooled/regime funding contrasts, cross-panel, alt regime | 2026-11-20/21 | terminal (mixed) |
| FCLR-LIQ-OOS-FORECAST-001 | OOS forecast next-24h liq notional | 20261121T055825Z | NOT_SUPPORTED (terminal) |
| FCLR-LIQ-COMBINED-PANEL | Time-series 24h liq intensity | 20261115T185844Z | NOT_MET (terminal) |
| FCLR-BOUNDED-TRIGGER-ONLY | Trigger-only sentinel | 20261121T071500Z | SUPERSEDED |
| FCLR-SESSION-SYNTHESIS-01 | Consolidation + meta-analysis | 20261121T080000Z | CONSOLIDATORY_ONLY (terminal) |
| FCLR-PANEL-FE-001 | Panel-FE + walk-forward OOS | 20261121T130159Z | NOT_SUPPORTED (terminal) |
| Track A/B/C / FCLR-011 | observed liq / modeled breach / vol forecast | many | blocked/null (terminal) |
| **FCLR-LIQ-CONTAGION-001** | Cross-coin contagion + funding spillover (1.74M panel) | **20261121T193000Z** | **COMPLETE** — H_contagion_liq SUPPORTED (11 edges); H_contagion_funding NOT_SUPPORTED; overall NOT_SUPPORTED; recompute discrepancy (58 vs 11 edges) disclosed and resolved by CONTAGION-002 |
| **FCLR-LIQ-CONTAGION-002** | Edge-set robustness + per-edge materiality reconciliation | **20261121T210000Z** | **COMPLETE** — all 3 hypotheses SUPPORTED; full artifact set emitted |
| **FCLR-FINAL-SYNTHESIS-01** | Final synthesis report | **20261121T220100Z** | **COMPLETE** — all primary hypotheses terminal (NOT_SUPPORTED / DATA_BLOCKED); forecast gate NOT PASSED; no overlay evaluated |

**Acceptance — the gate (PASSES):**
```bash
python3 scripts/check_handoff_heavywork_gate.py          # → PASS reason=OK
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_144  # 68 pass, 0 fail
python3 scripts/next_campaign_status.py                   # CAMPAIGN STATUS: no feasible 3-block design in ANY domain
ls -la research_state/session_20261121T220100Z/           # non-empty artifact set
```

---

## 2. NEXT FOCUS CAMPAIGN — FCLR-LIVE-DATA-ACQUISITION-001 (LIVE/FREE-DATA ROUTE)

**Campaign ID:** FCLR-LIVE-DATA-ACQUISITION-001
**Status:** ACTIVE — sole rank-0 campaign; not yet executed
**Start UTC:** 2026-11-21T22:25:40Z (opened by this handoff)
**Executable UTC:** > 20261121T220100Z

**Mission:** Open a materially different free-data route so heavy research can continue. The frozen-data frontier is closed (no feasible 3-block design in any domain; all frozen preregs evaluated). The only path to new heavy work is an unauthenticated, free, external source with live/unfrozen historical coverage that is not already exhausted on disk.

**Required execution steps (all three must be completed; none may be skipped):**

1. **Source discovery & verification (outcome-blind, pre-freeze):** Enumerate candidate free sources (Binance public archive, unauthenticated exchange REST endpoints, public GitHub/Zenodo/Hugging Face/institutional archives). For each candidate, verify: unauthenticated download path; actual history depth (not just recent records); schema and field availability; licensing/terms; earliest and latest timestamp; cadence; symbol/venue coverage; known gaps; file hashes or ETags; rejection reason if inadmissible. Record results in `research_state/data_source_registry.json` and a per-source probe artifact under `research_state/session_<UTC>/`. Do NOT bypass access controls, rate limits, or usage terms. Exclude sources requiring payment, signup, manually issued keys, or requester-pays charges.

2. **Prereg freeze on the new data:** Freeze hypotheses, targets, features, splits, baselines, thresholds, and decision gates BEFORE inspecting outcomes. `outcome_data_inspected_before_freeze: false`. Assert source/data hashes. Record configuration hash and UTC freeze time.

3. **Execute a heavy 3-block design:** On the verified new data, execute a pre-registered 3-block confirmatory design with non-empty artifacts under `research_state/session_<UTC>/` (UTC > 20261121T220100Z). Artifact set must include: prereg freeze (json+md), evaluation triad (py+json+md), independent stdlib recompute (py+json), evidence audit (json+md), trigger check (json). No zero-byte placeholders.

**Non-avoidance constraints (machine-checkable via gate + root cap):**
- **Do NOT** create root-level `research_state/*.md|*.json` — count 499/500; cap enforced by test + gate. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261121T220100Z). Prose-only, trigger-only, audit-only, verify-and-stop, and placeholder artifacts do NOT satisfy the gate.
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** re-run any terminal/completed campaign above.
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** "verify green and stop" while claiming heavy work remains — the gate passes BECAUSE no heavy work remains on frozen data.

**If no admissible free source exists:** Write the evidence for the blocker (what was probed, why each source failed admissibility), identify the next materially different route, and stop that session cleanly. Do not idle waiting for an external trigger that cannot fire on frozen data.

**If no future session occurs:** This handoff stands as the final record. All evidence is preserved. No gate was passed. No overlay was evaluated. The null results are the result.

---

## 3. Frozen inputs (verified — do NOT re-derive, do NOT substitute)

- **Combined liquidation panel:** `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` — sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 1,740,415 event rows, 15 coins, 2025-03-22 → 2026-10-31 UTC. Columns: `timestamp`, `coin`, `notional_usd`, `side`, `source`, `tx_hash`, `fundingRate`, `premium`, `abs_fund_pct`, `mark`, `ema_dist`, `rv24h`, `rv168h`. **Assert sha256 in your script header before any read.**
- **Coins (15):** AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP. Directed pairs = 15×14 = **210**.
- **FCLR-001 panel (funding/RV baseline, if needed for funding alignment):** `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` — sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`, 29,136 rows × 22 cols, 5 coins, 5,832 hours. `premium` all-null; do not use.

---

## 4. Hard constraints (do NOT violate)

- **Do NOT** re-run any terminal/completed campaign above (including CONTAGION-001's point-estimate network).
- **Do NOT** modify `.github/workflows` (protected control plane).
- **Do NOT** overwrite `research_state/research_protocol.md` (sealed legacy FCLR-001).
- **Do NOT** add root-level `research_state/*.md|*.json` — count 499/500; cap enforced by test + gate. All new artifacts go under `research_state/session_<UTC>/`.
- **Do NOT** create empty/placeholder files or empty session directories (gate checks non-zero size).
- **Do NOT** threshold-shop or relax the 2% materiality floor after outcomes; preserve nulls as NOT_SUPPORTED.
- **Do NOT** claim completion without the full artifact set under a new `session_<UTC>/` (UTC > 20261121T210000Z). Prose-only, trigger-only, audit-only, verify-and-stop, and placeholder artifacts do NOT satisfy the gate.
- **Do NOT** "verify green and stop" while claiming heavy work remains — the gate passes BECAUSE no heavy work remains.

---

## 5. Per-session close-out (RESEARCH_PROMPT.md §12/§19)

Before finishing, update this AGENT_HANDOFF.md with: what changed and why; what was tested with exact outcomes; what evidence was added and where; the state of each research gate; the single highest-value next task; the precise verifying command; any blocker with the next materially different free-data route. **No active rank-0 campaign.** The frozen-data frontier is exhausted. **No prose-only, no trigger-only, no audit-only, no verify-and-stop sessions.** Commit nothing merely to show activity. If a final synthesis is produced, record it and stop cleanly. If no future session occurs, this handoff is the final record.

---

(End of handoff)