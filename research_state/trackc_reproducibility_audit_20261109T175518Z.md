# Track C Funding-Conditioned Volatility — Reproducibility & Audit (Offline)

**Artifact:** `research_state/trackc_reproducibility_audit_20261109T175518Z.md`
**Timestamp (UTC):** 2026-11-09T17:55:18Z (filename timestamp) / generated this session 2026-11-09T17:52:40Z context
**Scope:** Reproducibility verification of completed exploratory Track C deeper-validation artifacts only. **No new sealed outcomes inspected. No confirmatory claims. No network probing performed.**
**Track boundary:** Track C = volatility/stress forecast outcomes from admissible public price/mark/funding data. Do **not** conflate with observed liquidations (Track A) or synthetic/modeled boundary breaches (Track B labels).

## 1) Artifact integrity (SHA256, size, mtime)

| Path | Bytes | mtime (UTC-ish from FS) | SHA256 |
|---|---:|---|---|
| `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md` | 4478 | 2026-11-09 16:30:51.592359160 +0000 | `9d1c7660fda4286267b0242ea6ce1acc6867b1b7984c5f3021a1ff26c43e81ca` |
| `research_state/evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md` | 20493 | 2026-11-09 16:39:00.820646329 +0000 | `42df57ac371c5c46084943f0fde200fa5b5bd5bfddea466a7ea86a9f4b155a31` |
| `research_state/data_cache/fclr002_panel.json` | 6384632 | 2026-11-09 16:07:06.021005717 +0000 | `fd27207b3e2c26a0910f8081e5712794287244723edcbc439f907fa9d4bce28a` |
| `research_state/run_manifest.json` | 1536739 | 2026-11-09 16:07:05.137003201 +0000 | `7649055f22a81d9a7f6944b9bb713273389f00a6fe99ff3341b474719e0e8788` |
| `research_state/experiment_frontier.json` | (see hash) | — | `29503be80158eeb305e85a6a1b13897470a4a021a9b53fce11566a909b4ba8a2` |
| `research_state/negative_results_report.md` | (see hash) | — | `30aa920911fce04bb0bfa2eaeb2b263487bffa707bdab38615c4b621ec8a9f8c` |
| `research_state/block_count_resolution_20261103T102000Z.md` | (see hash) | — | `d4b27616c0754d58341edbd289dafadfcb887423168fe45b7ce4687febbe4bba` |
| `AGENT_HANDOFF.md` | (see hash) | — | `8b697ec3042f4ae6cf97464738c13b29ed77b107eba7029cb825b50c48710357` |

**Panel/manifest split refs (verified):** `fclr002_panel.json` contains `splits`: train `2024-04-01T00:00:00Z..2024-06-08T23:00:00Z`, val `2024-06-16T00:00:00Z..2024-07-15T23:00:00Z`, test `2024-07-23T00:00:00Z..2024-09-30T23:00:00Z`. `run_manifest.json` `split_boundaries` is `frozen`, chronological unique UTC timestamps, 7-day embargo (FCLR-002 pre-registered) with the same train/val/test windows. Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (FCLR-002 panel metadata / summaries).

## 2) Exact rerun commands (recorded; reruns not executed this session)

Run from repo root with `PYTHONPATH` as needed:

```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
# Exploratory deep analysis (frozen FCLR-002 splits; no sealed-panel peeking beyond cached panel/manifest)
PYTHONPATH=$PWD python scripts/run_stream_b_deep_analysis_001.py
PYTHONPATH=$PWD python scripts/run_stream_b_deep_analysis_002.py
```

**Environment (this session, 2026-11-09T17:52:40Z):** Python 3.12.3 (GCC 13.3.0). Modules: `numpy` OK, `pandas` OK, `scipy` OK; `pyarrow` MISSING (ModuleNotFoundError), `sklearn` MISSING, `matplotlib` MISSING. Rerunning analysis scripts requires the deps those scripts import; record actual imports before rerun. Full `python -m unittest discover tests` is **not** claimable here due to heavy-dep import errors; dep-light verification only:

```bash
python -m unittest tests.test_synthetic_boundary_labels  # 8/8 OK (verified 2026-11-09T17:52:40Z)
```

## 3) Confirmatory blocker evidence (structural; no new outcomes)

- **Block count:** FCLR-002 test window `2024-07-23..2024-09-30` = 70 days = **2** non-overlapping 30-day blocks; protocol requires **>=3** for confirmatory claims. Evidence: `research_state/block_count_resolution_20261103T102000Z.md` (`d4b2761...`), `AGENT_HANDOFF.md`, STREAM_B summaries.
- **Data horizon:** Binance public archive admissible coverage ends **2026-11-02** for the relevant unsealed forward path probed in prior work (404 beyond); 2024 partitions consumed (FCLR-004 BLOCKED). No cached >=3-block unsealed Track C panel ready. **Do not manufacture a confirmatory claim.**
- **Decision already recorded:** `FUNDING_CONDITIONING_DEEPER_VALIDATION-002` = **COMPLETE_INCONCLUSIVE (EXPLORATORY_ONLY)** in `research_state/experiment_frontier.json` (`29503be...`) and `research_state/negative_results_report.md` Track C section (`30aa920...`, appended 2026-11-09T16:39:00Z).

## 4) Carried-forward exploratory results (evidence only; not promotable)

- **ANALYSIS-001 (2026-11-09T16:27:03Z):** C2_all vs B1 +4.588% rel QLIKE on TEST, diff -0.030400, 95% CI [-0.044345,-0.018402] excludes 0; funding/price ablations mixed as reported. 2 blocks < 3 → exploratory only.
- **ANALYSIS-002 (2026-11-09T16:35:17Z):** regime-stratified (train-only quartiles, no look-ahead, 2000 block-bootstrap reps). Q1 extreme-funding regimes show robust incremental skill (CI excludes 0 in reported aggregate/symbol cells); Q1_low_abs_pos +5.346% aggregate YES all symbols positive; Q2_neg/Q4_high_abs_neg negative/NO as reported. **Exploratory only**; do not promote.

## 5) Next confirmatory path (single, concrete) — PREREG BEFORE OUTCOMES

**Resume trigger (admissible only):** appearance of a new unauthenticated, provenance-auditable Binance (or equivalently admissible public) panel with **>=5 symbols** and **>=3 non-overlapping 30-day OOS blocks** (or an equivalent pre-registered design meeting the same claim-worthiness/block criteria), with sufficient mark/index/funding/klines coverage and documented gaps.

**Before any outcome inspection:**
1. Verify source admissibility (no auth/payment/manual/key/bypass), exact URLs/ETags/checksums, schema, license/terms, coverage/gaps.
2. Freeze protocol/preregistration (hypotheses, targets, features, splits, embargo/purge, baselines, primary/secondary contrasts, block-bootstrap settings, multiplicity, decision gates) in a **new** versioned file: `research_state/pre_registration_fclr014_confirmatory_funding_vol_<UTC>.json` (and optional companion `.md`) — **create and freeze this before computing outcomes**.
3. Register splits/manifest entries as frozen-before-outcomes; preserve negative/inconclusive results.
4. Only then build/evaluate; do not reuse sealed holdouts; do not threshold-shop.

**Track A unchanged:** no probing/scans/wrappers; trigger-only with Hyperliquid/ironflow admissibility rules and prereg before outcomes.

## 6) Session evidence

- `git status --short`: clean (verified).
- `python -m unittest tests.test_synthetic_boundary_labels`: **Ran 8 tests in 1.566s — OK**.
- Hash/size/stat/env checks recorded above. No `__pycache__`/cache commits; no `.github/workflows` edits; no network probing.
