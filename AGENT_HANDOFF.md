## Initial Task Message (2026-11-07T23:49:02Z) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; H001 NOT_SUPPORTED, forecast gate NOT MET. (2) **Gate 4 v5 confirmatory path** — 2025-08..10 canonical cache for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT has full daily kind coverage locally (FCLR-016 repair chunks completed, `sha256_mismatch_after_download=0`); **full-day Binance Vision identity probe (all 5 symbols, 1855 checks total) must reach GO + placeholder quarantine + license/terms/completeness/leakage/prereg/freeze evidence before any confirmatory outcomes** (FCLR-014 fail-closed). (3) **Track A observed liquidation risk** — DATA_BLOCKED/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — CLOSED_NEGATIVE.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Obtain full-scope Gate 4 v5 canonical identity GO + assemble admissibility evidence (NO outcomes).**
1. **Finish/verify full identity probes** (resumable, deterministic manifests, no outcomes). Background probes started 2026-11-07T23:47:13Z..23:47:53Z:
   - BTC/ETH: `--symbols BTCUSDT,ETHUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --resume research_state/fclr016_local_audit/_partial_20261107T233742Z.json --checkpoint-every 100 --out-tag 202508_202510_btc_eth_full_canonical_v5` (bgp_1b86a345d001heQIsGYvhtSQOC). Expected 742 checks.
   - BNB/SOL/XRP: `--symbols BNBUSDT,SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --checkpoint-every 100 --out-tag 202508_202510_bnb_sol_xrp_full_canonical_v5` (bgp_1b869b0c3001ktMPrILtLl4hBJ). Expected 1113 checks.
   - **Check progress:** inspect latest `_partial_*.json` in `research_state/fclr016_local_audit/` (newest partials by mtime) and final `fclr016_binance_vision_probe_*v5*.json/md`. **GO requires** `match>0` and `mismatch==0 && missing_local==0 && missing_remote==0 && remote_error==0 && placeholder_duplicate_files==0` on frozen scope (`cache_identity_vs_binance_vision` GO; `confirmatory_claim_go` remains NO_GO until full admissibility). Any conflict => audited repair/quarantine via `scripts/fclr016_repair_canonical_cache.py` (reversible manifests), then re-probe; no outcomes.
2. **Assemble Gate 4 v5 admissibility evidence package** (still NO confirmatory run): (a) full identity probe GO artifacts for all 5 symbols/months/kinds, (b) explicit Binance Vision/data-use license/terms evidence as machine-readable provenance manifest for `--provenance-manifest` (FCLR-014 guard), (c) completeness/leakage checks (no overlap vs consumed/confounded/guard windows; full symbol×kind×day coverage; placeholder duplicates quarantined with reversible evidence), (d) only if all pass, draft preregistered confirmatory design doc (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until manifest committed/frozen and FCLR-014 guard accepts it. If blocked, keep v5 `NOT_READY/NO_GO` and ship ≥1 substantive hardening/test/guardrail with green gates.
3. **Track A:** only on genuinely new unauthenticated admissible Hyperliquid-only source passing strict rubric + prereg before outcome inspection; otherwise skip re-probe entirely.

### Current gate state (evidence-backed, re-verified 2026-11-07T23:49:02Z)
- Track A = `DATA_BLOCKED` (no trigger). Track B = `CLOSED_NEGATIVE`. Track C/H001 = `NOT_SUPPORTED` (forecast gate NOT MET). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09; not promotable).
- Gate 4 v5 sampled identity (prior, bounded): `GO_PARTIAL_BOUNDED` for 2025-08..10, 5 symbols, 5 kinds, sample days 1,15,28+last — `fclr016_binance_vision_probe_202508_202510_5sym_5kind_sampled_canonical_postrepair_postquarantine_v4_20261107T224842Z.json` (match=255 mismatch=0 missing_local=0 missing_remote=0 remote_error=0 placeholder_duplicate_files=0). **Sampled only; not confirmatory GO.**
- **Measurable state at handoff:** BNB/SOL/XRP 2025-08..10 daily canonical coverage repaired to 1104/1104 present (BTC/ETH 736/736). Repair manifests `sha256_mismatch_after_download=0`: `fclr016_canonical_repair_202508_202510_bnbsolxrp_full_chunk{1..6}_20261107T233538Z..234107Z.json` (+md). Quarantine evidence: `fclr016_quarantine_top_level_placeholders_20261107T224836Z.json` (220 moves, reversible). Existing BTC/ETH partial from prior session: `_partial_20261107T233742Z.json` (300 MATCH checks through BTCUSDT 2025-10 markPriceKlines 2025-10-22). **Full 5-symbol GO not established; `confirmatory_claim_go` remains NO_GO.**
- **This session removed bottlenecks:** resumed/started BTC/ETH full probe and started previously-missing BNB/SOL/XRP full probe (unauthenticated Binance Vision identity checks only). No outcomes run.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
# Check probe progress/final artifacts:
ls -1t research_state/fclr016_local_audit/*v5* research_state/fclr016_local_audit/_partial_*.json 2>/dev/null | head
# If a probe stopped, resume with --resume <latest matching partial> and same out-tag.
python3 scripts/tracka_resume_check.py
```

### Acceptance criteria
- Deterministic JSON+MD probe artifacts with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go`; full-scope GO requires `mismatch/missing_local/missing_remote/remote_error/placeholder_duplicate_files==0`.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard fail-closed.
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (2); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory/sampled-only identity/partial probes as confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

### Focus campaign (mandatory, no opt-out)
Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 full canonical identity+provenance/admissibility with green gates and no outcomes, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated `AGENT_HANDOFF.md` is incomplete.

---
Previous detailed session log retained in git history (`AGENT_HANDOFF.md` prior revision).
