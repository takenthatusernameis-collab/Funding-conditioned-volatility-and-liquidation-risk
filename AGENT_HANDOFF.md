## Initial Task Message (2026-11-07T23:56:47Z) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; H001 NOT_SUPPORTED, forecast gate NOT MET. (2) **Gate 4 v5 confirmatory path** — 2025-08..10 canonical cache for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT has daily-kind repair chunks completed (`sha256_mismatch_after_download=0`); **full-day Binance Vision identity probe (all 5 symbols, 1855 checks total) must reach GO on frozen scope + placeholder hazards resolved + license/terms/completeness/leakage/prereg/freeze evidence before any confirmatory outcomes** (FCLR-014 fail-closed). (3) **Track A observed liquidation risk** — DATA_BLOCKED/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — CLOSED_NEGATIVE.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Complete full-scope Gate 4 v5 canonical identity GO for all 5 symbols, then assemble admissibility evidence (NO outcomes).**
1. **Resume/complete BTC/ETH full identity probe** (unauthenticated Binance Vision checks only). Latest progress: `research_state/fclr016_local_audit/_partial_20261107T235328Z.json` — **550/742 checks, all MATCH so far** (BTCUSDT complete 371/371; ETHUSDT 179/371; last `ETHUSDT 2025-09 markPriceKlines 2025-09-23`). Expected remaining 192. Command (resumable, deterministic artifacts):
   `cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk && python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --resume research_state/fclr016_local_audit/_partial_20261107T235328Z.json --checkpoint-every 100 --out-tag 202508_202510_btc_eth_full_canonical_v5`
2. **BNBUSDT identity evidence (completed this session, needs placeholder-clean final artifact):** chunk artifact `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_chunk_20261107T2350Z_20261107T235409Z.json` contains **371/371 checks, all MATCH** (`new_this_run=71`, total BNB coverage complete) but reported `placeholder_duplicate_files=61` because stale top-level BNB daily zips existed at that run time. I quarantined remaining top-level BNB/SOL/XRP placeholders with reversible manifest `research_state/fclr016_local_audit/fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json` (240 moves). **Action:** run a full BNB post-quarantine probe (no `--max-checks`; it will be fast if local canonical files intact and remote checks still required — use resumable strategy if needed) to emit a clean GO/NO_GO artifact with `placeholder_duplicate_files==0`, OR if remote rate/time is costly, produce a deterministic reconciliation note/manifest that binds the 371 all-MATCH checks to post-quarantine state and rechecks placeholder count is 0 — but prefer an auditable probe artifact. Do not claim GO without artifact evidence.
3. **Run full SOLUSDT+XRPUSDT probes** (post-quarantine). Partial chunk `fclr016_binance_vision_probe_202508_202510_sol_xrp_full_canonical_v5_chunk_20261107T2350Z_20261107T235526Z.json` was 60 checks / 742 scope with placeholders before quarantine (`NO_GO`); do **not** trust it as coverage. Start/resume a clean full probe:
   `python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --checkpoint-every 100 --out-tag 202508_202510_sol_xrp_full_canonical_v5_postquarantine`
4. **Identity GO definition (frozen by probe script semantics):** `cache_identity_vs_binance_vision` GO requires `match>0 && mismatch==0 && missing_local==0 && missing_remote==0 && remote_error==0 && placeholder_duplicate_files==0` on frozen scope. Any MISMATCH/MISSING/REMOTE_ERROR/placeholder hazard => fail-closed; repair/quarantine with reversible manifest (`scripts/fclr016_repair_canonical_cache.py` / audited moves), re-probe; no outcomes.
5. **After full 5-symbol identity GO artifacts exist:** assemble Gate 4 v5 admissibility package (still NO confirmatory outcomes): (a) all 5-symbol full identity GO artifacts, (b) machine-readable Binance Vision/data-use license/terms/provenance manifest for `--provenance-manifest` (FCLR-014 guard), (c) completeness/leakage checks (no overlap vs consumed/confounded/guard windows; full symbol×kind×day coverage; placeholders quarantined with reversible evidence), (d) only if all pass, draft/commit preregistered confirmatory design (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until frozen+guard-accepted. If blocked, keep v5 `NOT_READY/NO_GO` and ship ≥1 substantive hardening/test/guardrail with green gates.
6. **Track A:** only on genuinely new unauthenticated admissible Hyperliquid-only source passing strict rubric + prereg before outcome inspection; otherwise skip re-probe entirely.

### Current gate state (evidence-backed, re-verified 2026-11-07T23:56:47Z)
- Track A = `DATA_BLOCKED` (no trigger). Track B = `CLOSED_NEGATIVE`. Track C/H001 = `NOT_SUPPORTED` (forecast gate NOT MET). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09; not promotable). Gate 4 v5 confirmatory = `NOT_READY/NO_GO`.
- BTC/ETH full probe: **550/742 MATCH, 0 mismatch/missing/remote_error, placeholder_duplicate_files=0 in latest partial context** (`_partial_20261107T235328Z.json`); **not complete / not GO**.
- BNBUSDT checks complete in chunk evidence: **371/371 MATCH** (`fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_chunk_20261107T2350Z_20261107T235409Z.json`); chunk self-reported placeholders at run time — post-quarantine clean artifact still needed.
- SOLUSDT/XRPUSDT: **not complete** (prior chunk dirty/pre-quarantine; 742 checks remaining for clean post-quarantine full run).
- This session removed bottlenecks: advanced BTC/ETH 500→550 checks, completed BNB 300→371 checks, quarantined 240 top-level BNB/SOL/XRP placeholder zips (`fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json`), emitted bounded probe artifacts; **no outcomes run**.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
# Probe progress/finals:
ls -1t research_state/fclr016_local_audit/_partial_*.json research_state/fclr016_local_audit/fclr016_binance_vision_probe_*v5* 2>/dev/null | head -12
python3 scripts/tracka_resume_check.py
```

### Acceptance criteria
- Deterministic JSON+MD probe artifacts with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go`; full-scope GO requires `mismatch/missing_local/missing_remote/remote_error/placeholder_duplicate_files==0`.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard fail-closed.
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (2: `AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md`); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat sampled/chunk/partial/placeholder-dirty artifacts as confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

### Focus campaign (mandatory, no opt-out)
Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 full canonical identity+provenance/admissibility with green gates and no outcomes, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated `AGENT_HANDOFF.md` is incomplete.

---
Previous detailed session log retained in git history (`AGENT_HANDOFF.md` prior revision).
