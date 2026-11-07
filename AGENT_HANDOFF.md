# AGENT_HANDOFF.md — SINGLE DURABLE INITIAL TASK (NEXT SESSION)

**TIMESTAMP (UTC):** 2026-11-07T03:25:00Z
**REPO (priority):** `Funding-conditioned-volatility-and-liquidation-risk` — **P0 = funding-conditioned volatility (Gate 4, Track C)** using local admissible data. **Liquidation risk (Track A) = BLOCKED/GUARDED, no trigger** — do not resume Track A probing/outcome inspection.
**AUTHORITY:** This file is the **only** durable session handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md`, frontier entries, or stale notes conflict, follow this file and record reconciliation in durable artifacts (not status-only files).

## THIS SESSION (measurable delta, 2026-11-07T03:15:53Z–03:25:00Z)
- **Gate 4 pilot rigor strengthened (code + tests + run + durable artifacts):**
  - `scripts/run_funding_ablations.py`: added per-split paired ΔQLIKE table vs A (instability visibility), exploratory block-bootstrap sensitivity (12h/24h/48h; 24h remains primary per prereg) using same pooled paired observations/seed/reps/CI method, and per-split paired frame capture. No change to pre-registered contrasts/ablations/splits/model/metrics.
  - `tests/test_funding_ablations_multisplit.py`: asserts 3 per-split paired frames returned.
  - `research_state/pre_registration_gate4_funding_multisplit_20261107_exploratory_sensitivity_addendum.md` (EXPL-SENS-001, frozen before running sensitivity outputs): exploratory only, not confirmatory/claim-bearing.
  - Regenerated: `research_state/evaluation_summary_funding.md` (2026-11-07T03:21:33Z, SHA 97dbc2add1a0441f49b1d901e4aae546a1282a37), `research_state/evaluation_summary.md` section, `research_state/run_manifest.json` (adds `per_split_paired_delta_vs_A`, `exploratory_sensitivity_block_hours`, addendum ref), `research_state/leakage_audit.md` unchanged/clean.
- **Verification (local, no network in tests):** `python -m unittest tests.test_funding_ablations tests.test_funding_ablations_multisplit -v` → **11/11 OK**. `python scripts/run_funding_ablations.py` (local data only) → pilot verdict unchanged: **PILOT/INCONCLUSIVE** (data-sufficiency criteria not met). `python -m unittest discover -s tests -t .` → **722/722 OK**. `python scripts/tracka_resume_check.py` → **pass:true, 17/17**. `research_state` root md+json = **148** (under cap). Probes == 2. No workflow changes. No Track A probing/outcome inspection. No creds/paid data/manual downloads/bypass.

## VERIFIED PILOT RESULTS (pre-registered; do not promote)
- Pre-reg: `research_state/pre_registration_gate4_funding_multisplit_20261107.md` (frozen 2026-11-07T01:36:11Z). Exploratory addendum frozen before sensitivity outputs.
- Data: **local only** BTC/ETH/SOL/XRP 1h klines + fundingRate 2024-01..03 (extracted CSVs/zips). Missing = NaN, never zero. Basis/premium **omitted** (no aligned admissible local series verified).
- 3 pre-reg walk-forward splits (14-day tests 2024-02-05..02-18, 02-19..03-03, 03-04..03-17; train-only normalization; purge/embargo=7d). Direct-variance OLS HAR (no log/exp).
- Aggregate QLIKE (mean): A=7.4632551696362475, B=16.987894189880944, C=16.987894189880944, D=16.987894191103717, E=5.543607735488995.
- **Primary E vs A (pre-reg, block=24h): ΔQLIKE=4.6124034791315704, 95% block-bootstrap CI [-0.1288482496015316, 13.12243540310433], n_obs=1819, n_blocks=41, seed=12345, reps=2000, joint across instruments. CI spans 0.**
- **Instability (visible):** per-split paired ΔQLIKE(E vs A) = [7.225674132309532 (n=1091), 1.6403717659065886 (n=343), -0.14518458575410795 (n=385)] — sign flips in split 2; small/uneven valid_n. B/C/D unstable/worse in aggregate (split 2 dominated).
- **Exploratory sensitivity (12h/24h/48h):** E vs A CIs all span 0 (pts equal by construction of point estimate; CIs similar scale) — no stability gain; **do not promote**.
- **Verdict: PILOT/INCONCLUSIVE.** Shortfalls: `instruments=4 < 5`, `no_30day_non_overlapping_test_blocks` (14-day windows; Q1 2024 local ~90 days cannot fit >=3×30-day tests + train/purge), `q1_2024_only_local_data`. **No confirmatory claim, no economic value, no overlay.**

## BOTTLENECKS (evidence-backed)
1. **Data-sufficiency (blocks instrument count partially):** BNBUSDT local zips exist (2024-01..03 1h + funding, same schema) — adding it would satisfy >=5 instruments **but requires a NEW pre-registered experiment/version** (cannot change current prereg retroactively). Even with 5 instruments, **Q1 2024 local data cannot satisfy >=3 non-overlapping 30-day test blocks with train/purge** (90 days total). **Materially different route:** obtain/verify **additional admissible local months/symbols** (no creds/paid/manual) with alignment, then preregister 30-day non-overlapping blocks + instrument set + contrasts before outcomes.
2. **Basis/premium omitted:** no aligned admissible local series verified; keep NaN-omitted. Add only with verified alignment/no-lookahead under a versioned prereg addendum.
3. **Split 2 fragility:** valid_n drops (558/506/418) and sign/scale instability; pilot evidence only. Do not interpret as confirmatory.

## NEXT HEAVY-WORK CAMPAIGN (MANDATORY — P0, do not stop after reading)
Every session must produce a **measurable delta** (code + tests + run + durable artifact) or an evidence-backed blocker + next materially different route. **No status-only churn.**

1. **5-instrument pilot v2 (pre-registered, measurable):** If BNBUSDT local alignment is clean, create `research_state/pre_registration_gate4_funding_multisplit_v2_5sym_<UTC>.md` **BEFORE outcomes** (add BNBUSDT; keep same leakage/splits/model/contrasts or justify changes; explicitly state 30-day block criterion still NOT MET under Q1-only). Implement symbol list/config, run, record results as a **separate** pilot (v2) — do not overwrite v1 claims. Add/extend tests for 5-symbol loading/alignment (fixtures/mocked/local where available, no network).
2. **Block-bootstrap robustness (exploratory, bounded):** consider stationary bootstrap or circular-block edge handling only if pre-registered as exploratory addendum before running; report stability/instability honestly.
3. **Train-only regularization (only if pre-registered):** ridge/HAR-regularized variant selected **on train or train/val within split only, never test**; versioned prereg addendum required before outcomes. Compare to A/E as exploratory; do not tune to test.
4. **Data expansion path (evidence-backed, no bypass):** audit `data/`/repo for any other admissible local months/symbols with verified provenance/alignment; if found, preregister claim-worthy 30-day blocks. If not found locally, record blocker — **do not fetch with creds/paid/auth/manual**.
5. **Durable artifacts:** keep `evaluation_summary.md`, `evaluation_summary_funding.md` (or v2 file clearly labeled), `run_manifest.json`, `leakage_audit.md` synchronized with actual runs. `leakage_audit.md` must remain clean.

## TRACK A — GUARDED, NO TRIGGER (BOTTLENECK REMOVED PREVIOUSLY)
Trigger **NO** (data_through 2026-10; 2026-11..2027-02 absent). Probes == 2. **Do not re-probe, do not inspect outcomes, do not resume 131/132/139 without coherent artifacts.** Maintain invariants (17/17, bounds, no new probe families). If trigger appears: **PREREG BEFORE INSPECTING OUTCOMES**, Hyperliquid-only, observed ≠ modeled, fail-closed.

## CONSTRAINTS (NON-NEGOTIABLE)
- **No trading, no creds/API keys, no paid data, no auth bypass, no manual downloads.** Local admissible files only.
- **Never modify `.github/workflows/`.**
- **Leakage-resistant:** chronological only, purge/embargo, train-only normalization/stats/thresholds.
- **Missing != 0. Observed liquidations ≠ modeled boundary breaches ≠ volatility/stress.** Never merge tracks.
- **PREREG BEFORE OUTCOMES** for confirmatory/trigger evaluation or instrument-set changes that affect claims.
- **Heavy work required:** measurable delta or evidence-backed blocker + materially different next route. No status-only churn.
