## Initial Task Message (2026-11-07T23:59:22Z, git b0948fe569c53ba9bcd403c696b31eae286c24da) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; H001 NOT_SUPPORTED, forecast gate NOT MET. (2) **Gate 4 v5 confirmatory path** — 2025-08..10 canonical cache for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT has daily-kind repair/quarantine evidence; **full-scope Binance Vision identity GO on frozen scope + placeholder hazards resolved + license/terms/provenance/completeness/leakage/prereg/freeze evidence required before any confirmatory outcomes** (FCLR-014 fail-closed). (3) **Track A observed liquidation risk** — DATA_BLOCKED/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — CLOSED_NEGATIVE.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Complete full-scope Gate 4 v5 canonical identity GO for all 5 symbols, then assemble admissibility evidence (NO outcomes).**

1. **BTCUSDT/ETHUSDT: resume+complete full identity probe (192 checks remaining).** Latest resumable partial: `research_state/fclr016_local_audit/_partial_20251107T235328Z.json` (550/742, BTCUSDT 371/371 complete, ETHUSDT 179/371, last `ETHUSDT 2025-09 markPriceKlines 2025-09-23`, summary MATCH=550). All MATCH so far; placeholders 0 in probe context. Run:
   `python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --resume research_state/fclr016_local_audit/_partial_20251107T235328Z.json --checkpoint-every 100 --out-tag 202508_202510_btc_eth_full_canonical_v5`
   *If resume path differs, use the actual latest BTC/ETH partial under `research_state/fclr016_local_audit/_partial_*.json` with BTC/ETH checks.*

2. **BNBUSDT identity: post-quarantine reconciliation GO recorded (caveated).** Evidence: `fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_chunk_20261107T2350Z_20261107T235409Z.json` (371/371 MATCH; chunk self-reported placeholders at run time), quarantine manifest `fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json` (240 moves total; 80 BNB), post-quarantine recheck `fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_postquarantine_recheck_20261107T2356Z_20261107T235610Z.json` (20 checks, placeholders 0), reconciliation `fclr016_bnb_postquarantine_reconciliation_20261107T235830Z.json` (identity GO, confirmatory_claim_go=NO_GO, caveat: binds prior remote MATCH checks to cleaned filesystem; not a single fresh monolithic full probe). **Action if stricter evidence desired:** run a clean full BNB post-quarantine probe artifact; otherwise carry reconciliation as BNB identity evidence and document caveat in admissibility package.

3. **SOLUSDT/XRPUSDT: run full post-quarantine probes (742 checks, clean filesystem).** Prior chunk `fclr016_binance_vision_probe_202508_202510_sol_xrp_full_canonical_v5_chunk_20261107T2350Z_20261107T235450Z.json` and dirty partial were pre-quarantine/placeholder-dirty (`NO_GO`) — **do not treat as coverage**. Top-level BNB/SOL/XRP placeholders quarantined (0 remaining). Run resumable full probe:
   `python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --checkpoint-every 100 --out-tag 202508_202510_sol_xrp_full_canonical_v5_postquarantine`

4. **Identity GO definition (probe semantics):** `cache_identity_vs_binance_vision` GO requires `match>0 && mismatch==0 && missing_local==0 && missing_remote==0 && remote_error==0 && placeholder_duplicate_files==0` on frozen scope. Any hazard => fail-closed; repair/quarantine reversibly, re-probe; no outcomes.

5. **After 5-symbol identity evidence is complete:** assemble Gate 4 v5 admissibility package (NO confirmatory outcomes): all identity artifacts/reconciliation, machine-readable Binance Vision/data-use license/terms/provenance manifest for `--provenance-manifest` (FCLR-014 guard), completeness/leakage checks (no overlap vs consumed/confounded/guard windows; full symbol×kind×day coverage; reversible quarantine evidence), then only if all pass draft/commit preregistered confirmatory design (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until frozen+guard-accepted. If blocked, keep v5 `NOT_READY/NO_GO` and ship ≥1 substantive hardening/test/guardrail with green gates.

6. **Track A:** only on genuinely new unauthenticated admissible Hyperliquid-only source passing strict rubric + prereg before outcome inspection; otherwise skip re-probe entirely.

### Current gate state (evidence-backed, 2026-11-07T23:59:22Z)
- Track A = `DATA_BLOCKED` (no trigger). Track B = `CLOSED_NEGATIVE`. Track C/H001 = `NOT_SUPPORTED` (forecast gate NOT MET). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09). Gate 4 v5 confirmatory = `NOT_READY/NO_GO`.
- BTC/ETH: **550/742 MATCH, 0 mismatch/missing/remote_error, placeholders 0** (`_partial_20251107T235328Z.json` actual file in audit dir may have 20261107 timestamp — verify latest); **incomplete / not GO**.
- BNB: **371/371 remote MATCH checks + post-quarantine filesystem clean**; reconciliation `GO` (identity-only, caveated); `confirmatory_claim_go=NO_GO`.
- SOL/XRP: **not complete** (prior artifacts pre-quarantine/dirty; need clean full post-quarantine run).
- This session bottleneck removal (no outcomes): advanced BTC/ETH and BNB probe checks, quarantined 240 top-level placeholders (`fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json`), produced BNB post-quarantine recheck/reconciliation artifacts.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
ls -1t research_state/fclr016_local_audit/_partial_*.json research_state/fclr016_local_audit/fclr016_*v5* 2>/dev/null | head -15
python3 scripts/tracka_resume_check.py
```

### Acceptance criteria
- Deterministic JSON+MD probe artifacts with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go`; full-scope GO requires `match>0 && mismatch/missing_local/missing_remote/remote_error/placeholder_duplicate_files==0` on frozen scope.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard fail-closed.
- Refusals parseable JSON, exit!=0, no tracebacks, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (`AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md`); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat sampled/chunk/partial/placeholder-dirty/reconciliation-caveated artifacts as unconditional confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

### Focus campaign (mandatory, no opt-out)
Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 full canonical identity+provenance/admissibility with green gates and no outcomes, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated `AGENT_HANDOFF.md` is incomplete.

---
Previous detailed session logs retained in git history.
