# AGENT_HANDOFF.md — SINGLE DURABLE HANDOFF

**INITIAL TASK MESSAGE (2026-11-07T17:13:12Z, git `23446d38`, gates spot-checked): Next focus = produce exhaustive FCLR-015 2024-04..09 Binance Vision identity manifest (all days × 5 symbols × 5 kinds) from cached zips + committed input manifest/hashes, then freeze Gate 4 v4 prereg **before any outcomes**; Track A/B unchanged (blocked/closed), Track C confirmatory still gated.** Repo **Funding-conditioned-volatility-and-liquidation-risk** (priority: funding-conditioned volatility & liquidation risk; Track A/B/C separated).

## Verified this session (measurable)
- `python -B scripts/tracka_resume_check.py` → `pass:true, network:false, writes_real_research_state:false` (before/after edits).
- `python -B -m unittest tests.test_fclr_canonical_artifacts -v` → **3/3 OK**.
- Full suite: **not rerun this session** (baseline 751/751 @ `eb60d333` per prior handoff). Run `python -B -m unittest discover -s tests -t .` before merging research-code changes.
- `python -c "len(root md+json)"` → **163/163 bound OK**.

## Bottlenecks removed / progress (evidence-backed)
1. **FCLR-015 provenance script hardened (resumable, bounded):** `scripts/fclr015_verify_cache_provenance_2024q2q3.py` (sha256 `d78f1aee206e9c3edfda809781b8e0bc1c35f313b7a6e6bde4a5394e089af721`) now supports `--full-days`, `--resume`, `--checkpoint-every`, `--max-checks`, partial artifacts; prevents timeout-without-evidence failure noted previously. Sampled-mode compatibility verified (5-check smoke: 5/5 MATCH).
2. **New Binance Vision identity evidence (unauthenticated, no keys/paid/manual/auth bypass):** exhaustive-day sampled run (120 checks, BTCUSDT 2024-04/05 all days × 4 kline kinds) → **MATCH 120/120, mismatch 0, missing_remote 0, remote_error 0**. Artifacts:
   - `research_state/fclr015_local_audit/fclr015_binance_vision_2024_04_09_probe_full_partial120_20261107T171221Z.json` (sha256 `e93d261a98e033b83aa550dfa315f7c86578273d16ee7bd1184a35908dd65e98`)
   - `research_state/fclr015_local_audit/fclr015_binance_vision_2024_04_09_probe_full_partial120_20261107T171221Z.md` (sha256 `7a8b4a46a3faefb9a4aa9dcfa2e7f25c20dee11aec1cb0556a274a761978d9fd`)
3. **Prior sampled identity anchor (150/150 MATCH):** `research_state/fclr015_local_audit/fclr015_binance_vision_2024_04_09_probe_sampled_20261107T161157Z.json` sha256 `b9aa0a15153152cea39fa48862994d9626bb0eaa168512ab4b73d31451e6c060`. Inventory: `fclr015_cache_2024_04_09_inventory_20261107T155942Z.json` sha256 `d50b1f37d9f556f98b411c04a61feb802fbe65727b6faf3e22d344136c52cbc7`.
4. **Alt liquidation hunt refreshed (bounded):** `python3 -B scripts/hunt_alternative_liquidation_sources.py` updated `research_state/alt_source_scan_latest.json` (sha256 `fbc9986a0f7d481b90adb09997dae04ecf29746675b396c4caba59fe3b19e898`, candidates=21, source=cache). Deep review latest still **NO NEW GO** (`alt_source_deep_review_latest.md` 20261105T200439Z). Do not relabel modeled breaches as observed.

**Interpretation:** cached 2024-04..09 Binance UM daily 1h klines/mark/index/premium + monthly fundingRate samples are byte-identical to Binance Vision public archives (identity evidence). **Confirmatory claim remains NO-GO** until full-coverage manifest + frozen Gate 4 prereg before outcomes + leakage controls + non-overlapping test blocks.

## Next focus campaign (heavy, ordered; measurable artifacts only)
1. **P0 — Complete exhaustive FCLR-015 identity/manifest (Track C):** Resume/run `python3 -B scripts/fclr015_verify_cache_provenance_2024q2q3.py --full-days --checkpoint-every 50` (use `--resume <partial.json>` / `--max-checks` as needed) to cover **all 5 symbols × 2024-04..09 × every day × {klines,mark,index,premium} + monthly fundingRate**. Produce a **committed input manifest** (subdir OK if large; keep root bound) with: path, bytes, local sha256, source URL, remote status/sha256/ETag/Last-Modified where verified, coverage counts, unauthenticated Binance Vision access note, license/terms note. **No credentials/paid/manual/API keys/auth bypass.**
2. **P0 — Gate 4 v4 prereg before outcomes:** Only after manifest committed, freeze `research_state/pre_registration_gate4_funding_multisplit_v4_*` with `frozen_before_outcomes=true` **before any outcome run**. Non-consumed/non-confounded boundary; predeclared chronological splits; purge/embargo ≥ max horizon; train-only normalization; missing!=0; RV/volatility targets; B0/B1/C1/C2 ablations; QLIKE primary + MAE/RMSE secondary; block bootstrap where feasible; **≥3 non-overlapping 30-day test blocks** for claim-worthy confirmatory. Write explicit NO-GO evidence if blocked. Never overwrite FCLR-003/FCLR-013/v3 anchors.
3. **P1 — Deterministic exploratory smoke (non-confirmatory only):** only after manifest/prereg state is explicit; label `EXPLORATORY / NOT CONFIRMATORY`, include leakage checks, write to new non-canonical artifact, never promote.
4. **P1 — Alt liquidation source hunt (materially distinct):** bounded unauthenticated scans for **actual forced-liquidation event records** meeting rubric (≥5 symbols, ≥1 complete month or ≥3×30-day blocks, completeness/license/provenance, no signup/keys/payment). Update `alt_source_scan_latest.json` / `alt_source_deep_review_latest.md` only with new evidence (exact URLs/HTTP/license/schema/coverage/hashes, ACCEPT/NO-GO). Never fabricate.
5. **P2 — Tests/hygiene:** tmp-isolated tests for any new manifest/runner logic. Keep full suite green, 3/3 canonical, tracka_resume_check pass. No `.github/workflows` edits; no `__pycache__`/bulk `data/` commits; no status-only churn.

## Track status / guardrails
- **Track A:** BLOCKED/NO TRIGGER (ironflow data_through 2026-10; probes==2). **DO NOT re-probe.** Resume only on admissible unauthenticated observed-liquidation data + strict GO rubric + prereg before outcomes.
- **Track B:** closed/inconclusive; modeled boundaries **not** observed liquidations.
- **Track C:** FCLR-015 cache identity evidence strengthened (sampled/exhaustive-day partial); confirmatory still gated by full manifest, prereg, leakage/splits, block count.
- **Confirmatory anchors (never overwrite/promote/overlay):** FCLR-013 sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a` (C2 vs B1 +0.005953, CI [-0.011716,0.022101], RR -1.32%, NOT_MET, 1×30d block). FCLR-003 sha256 `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2` (+0.044013, CI [0.001487,0.093225], RR -10.98%, NOT_MET). v3 sha256 `9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e` (A 0.798319018412711; E vs A +0.4879023125556385 CI [-0.042160777324701186,1.1973379300276015] spans 0). Confirmatory CLOSED NEGATIVE on executed claim-worthy panels; **no overlay eligible**.
- PREREG before outcomes. Chronological splits; purge/embargo ≥ max horizon; train-only normalization; missing!=0. Preserve negative/inconclusive. No status-only churn.

**Authority:** this file is the only root durable handoff.
