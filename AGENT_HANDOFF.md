# AGENT_HANDOFF.md — SINGLE DURABLE HANDOFF

**INITIAL TASK MESSAGE (2026-11-07T16:21:28Z, git `eb60d333`, gates verified): Next focus = execute FCLR-015 full 2024-04..09 provenance manifest + Gate 4 prereg before outcomes; Track A/B unchanged (blocked/closed), Track C enabled but confirmatory still gated.** Repo **Funding-conditioned-volatility-and-liquidation-risk** (priority: funding-conditioned volatility & liquidation risk; Track A/B/C separated).

## Verified baseline (this session)
- `python -B -m unittest discover -s tests -t .` → **751/751 OK**.
- `python -B -m unittest tests.test_fclr_canonical_artifacts -v` → **3/3 OK**.
- `python -B scripts/tracka_resume_check.py` → `pass:true, network:false, writes_real_research_state:false`.
- `research_state/ironflow_fastpath_cache.json` reverted (no timestamp-churn commit).

## Measurable progress (bottleneck reduction)
**FCLR-015 sampled Binance Vision provenance probe (unauthenticated, no keys/paid/manual/auth bypass):** compared cached 2024-04..09 files under `research_state/data_cache/{SYMBOL}_2024_0{4-9}/` to `https://data.binance.vision/` by HTTPS GET + sha256/ETag/Last-Modified.
- Scope: BTC/ETH/BNB/SOL/XRP × 2024-04..09 × {klines 1h day15, markPriceKlines 1h day15, indexPriceKlines 1h day15, premiumIndexKlines 1h day15, monthly fundingRate} = **150 checks**.
- Result: **MATCH 150/150** (`cache_identity_vs_binance_vision_sampled: GO_SAMPLED`).
- Artifacts:
  - `research_state/fclr015_local_audit/fclr015_binance_vision_2024_04_09_probe_sampled_20261107T161157Z.json` (sha256 `b9aa0a15153152cea39fa48862994d9626bb0eaa168512ab4b73d31451e6c060`)
  - `research_state/fclr015_local_audit/fclr015_binance_vision_2024_04_09_probe_sampled_20261107T161157Z.md` (sha256 `90b9c6c6f4594aabf869e682d585f1faafa16437c3a18f3594c1c6b4d561a8`)
- Reusable full probe script (bounded, day 1/15/28/last + funding; timed out before artifact write in-session but saved): `scripts/fclr015_verify_cache_provenance_2024q2q3.py` (sha256 `28ae4b732465bdd7859de3b6089adaa73fc80c67457aad38e1ba1a99cbb9f1af`).
- Prior inventory anchor: `research_state/fclr015_local_audit/fclr015_cache_2024_04_09_inventory_20261107T155942Z.json` (sha256 `d50b1f37d9f556f98b411c04a61feb802fbe65727b6faf3e22d344136c52cbc7`).

**Interpretation:** sampled cached 2024-04..09 zips are byte-identical to Binance Vision public historical archives (strong provenance identity evidence). **Confirmatory claim remains NO-GO** until: full-coverage input manifest/hashes recorded, frozen Gate 4 prereg committed **before outcomes**, chronological 60/20/20-style or predeclared splits with purge/embargo ≥ max horizon, train-only normalization, leakage checks, and ≥3 non-overlapping 30-day test blocks for claim-worthy confirmatory. Never overwrite FCLR-003/FCLR-013/v3 anchors.

## Next focus campaign (heavy, execute in order; measurable artifacts only)
1. **Full 2024-04..09 provenance/manifest (P0, Track C / Gate 4 enablement):** Run `python3 -B scripts/fclr015_verify_cache_provenance_2024q2q3.py` (adjust timeout/sampling if needed) to produce full sampled/exhaustive identity evidence; build a **committed input manifest** for all 5 symbols × 2024-04..09 × required kinds (1h klines, mark, index, premium, funding) with path, bytes, sha256, source URL, HTTP/ETag/Last-Modified where verified, and coverage counts. Record Binance Vision access as unauthenticated public historical data; include terms/license note; **no credentials/paid/manual/API keys/auth bypass**.
2. **Gate 4 prereg before outcomes (P0):** Draft/freeze `research_state/pre_registration_gate4_funding_multisplit_v4_*` **only after** full manifest is committed. Non-consumed/non-confounded boundary, predeclared chronological splits, purge/embargo ≥ max horizon, train-only normalization, missing!=0, RV/volatility targets, B0/B1/C1/C2-style ablations (persistence, RV-only, funding-augmented, combined), QLIKE primary + MAE/RMSE secondary, block bootstrap where feasible, ≥3 non-overlapping 30-day test blocks for claim-worthy. Mark `frozen_before_outcomes=true` **before any outcome run**. If blocked, write explicit NO-GO evidence.
3. **Deterministic exploratory smoke (non-confirmatory, optional if manifest incomplete):** Only label `EXPLORATORY / PROVENANCE-SAMPLED / NOT CONFIRMATORY` with leakage checks; write to a new non-canonical artifact; never promote. Prefer steps 1-2 before claims.
4. **Alt liquidation source hunt (Track A/B support, materially distinct):** Continue bounded unauthenticated scans (`scripts/hunt_alternative_liquidation_sources.py`, `scripts/deep_review_alt_sources.py`) for **actual forced-liquidation event records** with rubric (≥5 symbols, ≥1 complete month or ≥3×30-day blocks, completeness/license/provenance, no signup/keys/payment). Update `research_state/alt_source_scan_latest.json` / `alt_source_deep_review_latest.md` **only with new evidence** (exact URLs, HTTP, license, schema, coverage, hashes, ACCEPT/NO-GO). Never fabricate; never label modeled breaches as observed.
5. **Hardening/tests:** Add/extend tmp-isolated tests for any new manifest/provenance/runner logic. Keep ≥751/751 full, 3/3 canonical, tracka_resume_check pass. `research_state` root md+json bound ≤163 (place large manifests in subdirs if needed). No `.github/workflows` edits; no `__pycache__`/bulk `data/` commits.

## Track status / guardrails
- **Track A:** BLOCKED/NO TRIGGER (ironflow data_through 2026-10; probes==2). **DO NOT re-probe.** Resume only on admissible unauthenticated observed-liquidation data + strict GO rubric + prereg before outcomes.
- **Track B:** closed/inconclusive; modeled boundaries are **not** observed liquidations.
- **Track C:** viable path now strengthened by FCLR-015 sampled cache identity for 2024-04..09 local cache; confirmatory still gated by prereg/manifest/leakage/block-count.
- **Confirmatory anchors (never overwrite/promote/overlay):** FCLR-013 sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a` (C2 vs B1 +0.005953, CI [-0.011716,0.022101], RR -1.32%, NOT_MET, 1×30d block). FCLR-003 sha256 `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2` (+0.044013, CI [0.001487,0.093225], RR -10.98%, NOT_MET). v3 sha256 `9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e` (A 0.798319018412711; E vs A +0.4879023125556385 CI [-0.042160777324701186,1.1973379300276015] spans 0). Confirmatory CLOSED NEGATIVE on executed claim-worthy panels; **no overlay eligible**.
- PREREG before outcomes. Chronological splits; purge/embargo ≥ max horizon; train-only normalization; missing!=0. Preserve negative/inconclusive. No status-only churn.

**Authority:** this file is the only root durable handoff.
