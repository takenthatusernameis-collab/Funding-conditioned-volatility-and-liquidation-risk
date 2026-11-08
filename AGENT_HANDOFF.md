## Initial Task Message (2026-11-08T00:01:24Z, git 3280eed6) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; FCLR-H001 `NOT_SUPPORTED`, forecast gate `NOT MET`. (2) **Gate 4 v5 confirmatory path** — 2025-08..10 canonical cache for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT has daily-kind repair/quarantine evidence; **full-scope Binance Vision identity GO on frozen scope + placeholder hazards resolved + license/terms/provenance/completeness/leakage/prereg/freeze evidence required before any confirmatory outcomes** (FCLR-014 fail-closed). (3) **Track A observed liquidation risk** — `DATA_BLOCKED`/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — `CLOSED_NEGATIVE`.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Produce full-scope 5-symbol Gate 4 v5 canonical identity evidence (Binance Vision, 2025-08..10, 5 kinds), then assemble admissibility package (NO outcomes).**

1. **BTCUSDT/ETHUSDT: resume+complete full identity probe (192 checks remaining of 742).** Verified resumable partial: `research_state/fclr016_local_audit/_partial_20261107T235328Z.json` — **550/742 checks, BTCUSDT 371/371 complete, ETHUSDT 179/371, last `ETHUSDT 2025-09 markPriceKlines 2025-09-23`, summary MATCH=550, placeholders 0**. No mismatches/missing/remote errors recorded in checks so far. Run (resumable, checkpoints every 100):
   ```bash
   python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --resume research_state/fclr016_local_audit/_partial_20261107T235328Z.json --checkpoint-every 100 --out-tag 202508_202510_btc_eth_full_canonical_v5
   ```
   *If a newer BTC/ETH partial appears, use the actual latest one containing BTC+ETH checks.*

2. **BNBUSDT: identity evidence is caveated, not a single clean full monolithic post-quarantine GO.** Remote full checks: `fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_chunk_20261107T2350Z_20261107T235409Z.json` (371/371 MATCH). Placeholders quarantined: `fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json` (240 moves total; 80 BNB; reversible). Post-quarantine recheck: `fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_postquarantine_recheck_20261107T2356Z_20261107T235610Z.json` (20 checks, placeholders 0). Reconciliation: `fclr016_bnb_postquarantine_reconciliation_20261107T235830Z.json` (`identity GO` caveated; `confirmatory_claim_go=NO_GO`). **Action (preferred for strictness):** run a fresh clean full BNB post-quarantine probe artifact:
   ```bash
   python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BNBUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --checkpoint-every 100 --out-tag 202508_202510_bnb_full_canonical_v5_postquarantine_fresh
   ```
   If time-constrained, carry reconciliation but state caveat explicitly in the admissibility package.

3. **SOLUSDT/XRPUSDT: run full clean post-quarantine probes (742 checks total).** Canonical kind-specific daily files present under `research_state/data_cache/SOLUSDT_2025_{08,09,10}` and `XRPUSDT_2025_{08,09,10}` (non-quarantined). Prior SOL/XRP chunk/dirty partials were pre-quarantine/placeholder-dirty (`NO_GO`) — **do not treat as coverage**. Run:
   ```bash
   python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --checkpoint-every 100 --out-tag 202508_202510_sol_xrp_full_canonical_v5_postquarantine
   ```
   Resume from the latest SOL/XRP post-quarantine partial if one exists with matching scope.

4. **Identity GO definition (probe semantics):** `cache_identity_vs_binance_vision` GO requires `match>0 && mismatch==0 && missing_local==0 && missing_remote==0 && remote_error==0 && placeholder_duplicate_files==0` on frozen scope. Any hazard => fail-closed; repair/quarantine reversibly, re-probe; **no outcomes**.

5. **After 5-symbol identity evidence is complete:** assemble Gate 4 v5 admissibility package (NO confirmatory outcomes): all identity artifacts/reconciliation, machine-readable Binance Vision/data-use license/terms/provenance manifest for `--provenance-manifest` (FCLR-014 guard), completeness/leakage checks (no overlap vs consumed/confounded/guard windows; full symbol×kind×day coverage; reversible quarantine evidence), then only if all pass draft/commit preregistered confirmatory design (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until frozen+guard-accepted. If blocked, keep v5 `NOT_READY/NO_GO` and ship ≥1 substantive hardening/test/guardrail with green gates.

6. **Track A:** only on genuinely new unauthenticated admissible Hyperliquid-only source passing strict rubric + prereg before outcome inspection; otherwise skip re-probe entirely.

### Current gate state (evidence-backed, 2026-11-08T00:01:24Z)
- Track A = `DATA_BLOCKED` (no trigger; `tracka_resume_check.py` PASS, local dry-run, no writes). Track B = `CLOSED_NEGATIVE`. Track C/FCLR-H001 = `NOT_SUPPORTED` (forecast gate NOT MET). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09). Gate 4 v5 confirmatory = `NOT_READY/NO_GO`.
- BTC/ETH: **550/742 MATCH, placeholders 0** (`_partial_20261107T235328Z.json`); **incomplete / not GO**.
- BNB: **371/371 remote MATCH checks + clean post-quarantine recheck (20) + caveated reconciliation GO**; `confirmatory_claim_go=NO_GO`; fresh monolithic post-quarantine full probe preferred.
- SOL/XRP: **not complete** (clean filesystem, but full post-quarantine probe needed).
- Green gates this session: `py_compile` OK (fclr016 verify/repair, run_funding_ablations); `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` = **6/6 OK**.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
ls -1t research_state/fclr016_local_audit/_partial_*.json research_state/fclr016_local_audit/fclr016_*v5* 2>/dev/null | head -15
python3 scripts/tracka_resume_check.py
```

### Acceptance criteria
- Deterministic JSON probe artifacts with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go`; full-scope GO requires `match>0 && mismatch/missing_local/missing_remote/remote_error/placeholder_duplicate_files==0` on frozen scope.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard fail-closed.
- Refusals parseable JSON, exit!=0, no tracebacks, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (`AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md`); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat sampled/chunk/partial/placeholder-dirty/reconciliation-caveated artifacts as unconditional confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

### Focus campaign (mandatory, no opt-out)
Every session until Track C/FCLR-H001 forecast gate passes must either (a) advance FCLR-016 full canonical identity+provenance/admissibility with green gates and no outcomes, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated `AGENT_HANDOFF.md` is incomplete.

---
Previous detailed session logs retained in git history.
