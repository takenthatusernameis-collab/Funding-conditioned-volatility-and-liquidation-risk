## Initial Task Message (2026-11-07T23:41:37Z) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; H001 NOT_SUPPORTED, forecast gate NOT MET. (2) **Gate 4 v5 confirmatory path** — 2025-08..10 canonical cache for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT now has full daily kind coverage locally (repair chunks completed, sha256_mismatch_after_download=0); **full-day Binance Vision identity probe + placeholder quarantine check + license/terms/completeness/leakage/prereg/freeze evidence still required before any confirmatory outcomes** (FCLR-014 guard fail-closed). (3) **Track A observed liquidation risk** — DATA_BLOCKED/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — CLOSED_NEGATIVE.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Finish Gate 4 v5 full-day canonical identity verification + assemble admissibility evidence (NO outcomes).**
1. **Complete/collect full identity probes** for `BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT` × `2025-08,2025-09,2025-10` × `fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines` with `--sample-days full` and deterministic manifests (resume/checkpoint). At 2026-11-07T23:41:37Z: BTC/ETH probe was started/resumed in background (`--resume research_state/fclr016_local_audit/_partial_20261107T233742Z.json`, `--out-tag 202508_202510_btc_eth_full_canonical_v5`); BNB/SOL/XRP full probe **not yet started**. Run/finish BNB/SOL/XRP full probe; merge/confirm all summaries. **GO requires match>0 and mismatch/missing_local/missing_remote/remote_error/placeholder_duplicate_files==0 on frozen scope.** If any conflict appears, repair/quarantine with audited reversible manifests (`scripts/fclr016_repair_canonical_cache.py`, quarantine pattern from FCLR-016) — no outcomes.
2. **Assemble Gate 4 v5 admissibility evidence package** (still NO confirmatory run): (a) full identity probe GO artifacts, (b) explicit Binance Vision/data-use license/terms evidence as machine-readable provenance manifest for `--provenance-manifest`, (c) completeness/leakage checks (no overlap vs consumed/confounded/guard windows; full symbol×kind×day coverage), (d) only if all pass, draft preregistered confirmatory design doc (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until manifest committed/frozen and FCLR-014 guard accepts it. If blocked, keep v5 `NOT_READY/NO_GO` and ship ≥1 substantive hardening/test/guardrail with green gates.
3. **Track A:** only on genuinely new unauthenticated admissible Hyperliquid-only source passing strict rubric + prereg before outcome inspection; otherwise skip re-probe entirely.

### Current gate state (evidence-backed, re-verified 2026-11-07T23:41:37Z)
- Track A = `DATA_BLOCKED` (no trigger). Track B = `CLOSED_NEGATIVE`. Track C/H001 = `NOT_SUPPORTED` (forecast gate NOT MET).
- Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09; not promotable).
- Gate 4 v5 sampled identity (prior): `GO_PARTIAL_BOUNDED` for 2025-08..10, 5 symbols, 5 kinds, sample days 1,15,28+last — `fclr016_binance_vision_probe_202508_202510_5sym_5kind_sampled_canonical_postrepair_postquarantine_v4_20261107T224842Z.json` (match=255 mismatch=0 missing_local=0 missing_remote=0 remote_error=0 placeholder_duplicate_files=0). **Sampled only.**
- **This session progress (measurable):** BNBUSDT/SOLUSDT/XRPUSDT 2025-08..10 daily canonical coverage repaired to **1104/1104 present** (BTC/ETH 736/736 already present). Repair manifests (all `repair_identity_ok=true`, `sha256_mismatch_after_download=0`): `fclr016_canonical_repair_202508_202510_bnbsolxrp_full_chunk{1..6}_20261107T233538Z..234107Z.json` (+md). BTC/ETH full identity probe started/resumed (partial checkpoint present: `_partial_20261107T233742Z.json`). **Full 5-symbol probe GO not yet established; confirmatory_claim_go remains NO_GO.**
- Repair/quarantine evidence from prior session remains valid: `fclr016_canonical_repair_202508_202510_bnb_sol_xrp_sampled_canonical_repair_20261107T224555Z.json`; `fclr016_quarantine_top_level_placeholders_20261107T224836Z.json` (220 moves, reversible). 2025-01 BTC/ETH canonical sampled `*_202501_bounded_canonical_20261107T210801Z.*`.

### Bottlenecks removed this session (measurable)
- Removed BNB/SOL/XRP 2025-08..10 **full-day canonical missing-file** bottleneck for daily kinds (960 missing detected pre-repair across those 3 symbols; repaired in bounded chunks with deterministic sha256 manifests, no overwrites of existing canonicals, unauthenticated Binance Vision public archive only). BTC/ETH full-day probe execution unblocked and in progress.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
# Finish/verify full identity (bounded, resumable, no outcomes):
python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --resume research_state/fclr016_local_audit/_partial_20261107T233742Z.json --checkpoint-every 100 --out-tag 202508_202510_btc_eth_full_canonical_v5
python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BNBUSDT,SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --checkpoint-every 100 --out-tag 202508_202510_bnb_sol_xrp_full_canonical_v5
python3 scripts/tracka_resume_check.py
```

### Acceptance criteria
- Deterministic JSON+MD probe artifacts with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go`; full-scope GO requires mismatch/missing/remote_error/placeholder==0.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard fail-closed.
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (2); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory/sampled-only identity/partial probes as confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

### Focus campaign (mandatory, no opt-out)
Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 bounded/full canonical identity+provenance/admissibility with green gates and no outcomes, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated AGENT_HANDOFF.md is incomplete.

---
Previous detailed session log retained in git history (AGENT_HANDOFF.md prior revision).