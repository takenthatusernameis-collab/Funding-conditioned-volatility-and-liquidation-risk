## Initial Task Message (2026-11-07T22:50:37Z) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; H001 NOT_SUPPORTED, forecast gate NOT MET. (2) **Gate 4 v5 confirmatory path** — sampled 2025-08..10 canonical identity/provenance is **GO_PARTIAL_BOUNDED** after FCLR-016 repair+quarantine; **full canonical completeness + license/terms + leakage/prereg/freeze still required before any confirmatory outcomes** (FCLR-014 guard remains fail-closed). (3) **Track A observed liquidation risk** — DATA_BLOCKED/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — CLOSED_NEGATIVE.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Complete Gate 4 v5 admissibility for 2025-08..10 without running outcomes.**
1. **Expand FCLR-016 from sampled (days 1,15,28+last) to full-day canonical identity verification** for `BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT` × `2025-08,2025-09,2025-10` × all 5 kinds, using bounded unauthenticated Binance Vision checks with deterministic manifests (`--sample-days full` or bounded chunked runs with `--resume`/`--checkpoint-every`; record sha256/etag/last-modified). Repair/quarantine any missing canonical or placeholder conflicts with audited, reversible actions (see `scripts/fclr016_repair_canonical_cache.py`, `research_state/fclr016_local_audit/fclr016_quarantine_top_level_placeholders_20261107T224836Z.json`). **Do not inspect/run confirmatory outcomes.**
2. **Assemble Gate 4 v5 admissibility evidence package** (still NO confirmatory run): (a) full identity probe GO (match>0, mismatch/missing/remote_error/placeholder==0 on frozen scope), (b) explicit Binance Vision/data-use license/terms evidence recorded as machine-readable provenance manifest referenced by `--provenance-manifest` path, (c) completeness/leakage checks (no overlap vs consumed/confounded/guard windows; full symbol×kind×day coverage), (d) if all pass, draft a **preregistered confirmatory design doc** (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until manifest is committed/frozen and FCLR-014 guard accepts it. If any fail, keep v5 `NOT_READY/NO_GO` and ship ≥1 substantive hardening/test/guardrail with green gates.
3. **Track A:** only on genuinely new unauthenticated admissible Hyperliquid-only source passing strict rubric + prereg before outcome inspection; otherwise skip re-probe entirely.

### Current gate state (evidence-backed, 2026-11-07T22:50:37Z)
- Track A = `DATA_BLOCKED` (no trigger). Track B = `CLOSED_NEGATIVE`. Track C/H001 = `NOT_SUPPORTED` (forecast gate NOT MET).
- Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09; not promotable).
- Gate 4 v5 sampled identity (this session): `GO_PARTIAL_BOUNDED` for 2025-08..10, 5 symbols, 5 kinds, sample days 1,15,28+last — `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202508_202510_5sym_5kind_sampled_canonical_postrepair_postquarantine_v4_20261107T224842Z.json` (summary: match=255 mismatch=0 missing_local=0 missing_remote=0 remote_error=0 placeholder_duplicate_files=0). **Partial only; full-day not yet verified; confirmatory_claim_go remains NO_GO.**
- Repair/quarantine evidence: `fclr016_canonical_repair_202508_202510_bnb_sol_xrp_sampled_canonical_repair_20261107T224555Z.json` (DOWNLOADED 144, sha256_mismatch_after_download=0, repair_identity_ok=true); `fclr016_quarantine_top_level_placeholders_20261107T224836Z.json` (220 moves, reversible, audited). 2025-01 BTC/ETH canonical sampled remains GO_PARTIAL_BOUNDED (`*_202501_bounded_canonical_20261107T210801Z.*`).

### Bottlenecks removed this session (measurable)
- Removed BNB/SOL/XRP 2025-08..10 canonical sampled-identity blocker: downloaded missing canonical Binance Vision daily zips (144) with deterministic sha256 manifests; quarantined conflicting top-level placeholders (220) with reversible manifest. Reran FCLR-016: **NO_GO -> GO_PARTIAL_BOUNDED** on sampled scope.
- Added `scripts/fclr016_repair_canonical_cache.py` (bounded, unauthenticated, no overwrite, fail-closed sha256 check).
- Preserved guards: FCLR-014 confirmatory 2025+ fail-closed (10 tests green); FCLR-016 canonical-path tests (3 green); `tracka_resume_check` pass (network=false, writes_real_research_state=false).

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days full --resume <checkpoint.json> --checkpoint-every 50 --out-tag 202508_202510_5sym_5kind_full_canonical_v5
python3 scripts/tracka_resume_check.py
```

### Acceptance criteria
- Deterministic JSON+MD probe artifacts with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go`; full-scope GO requires mismatch/missing/remote_error/placeholder==0.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard fail-closed.
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (2); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory/sampled-only identity as confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

**Focus campaign (mandatory, no opt-out):** Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 bounded/full canonical identity+provenance/admissibility with green gates and no outcomes, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions.

---

## 2026-11-07T22:50:37Z — FCLR-016 sampled canonical repair + placeholder quarantine (NO OUTCOMES)

**Focus:** (a) advanced FCLR-016 bounded identity/admissibility for 2025-08..10 with green gates.

### Work done
- **Repair:** `scripts/fclr016_repair_canonical_cache.py` downloaded 144 missing canonical Binance Vision daily zips for BNBUSDT/SOLUSDT/XRPUSDT × 2025-08..10 × 4 daily kinds × sample days {1,15,28,last} into `<kind>-<day>/` canonical subdirs. Report: `research_state/fclr016_local_audit/fclr016_canonical_repair_202508_202510_bnb_sol_xrp_sampled_canonical_repair_20261107T224555Z.json` — DOWNLOADED 144, sha256_mismatch_after_download=0, remote errors/missing 0, `repair_identity_ok=true`. Source: `https://data.binance.vision/` unauthenticated public archive; no auth/paid/manual/key bypass; no outcomes.
- **Quarantine (bottleneck removal):** moved 220 top-level same-name daily placeholder zips (BTC/ETH/BNB/SOL/XRP × 2025-08..10, sampled+present days) to audited per-month `__top_level_placeholders_quarantined_fclr016_20261107T224836Z/` dirs; reversible manifest `research_state/fclr016_local_audit/fclr016_quarantine_top_level_placeholders_20261107T224836Z.json`. Reason: top-level duplicates conflicted with canonical kind subdirs and caused `placeholder_duplicate_files` NO_GO; FCLR-016 `local_zip` ignores top-level for daily kinds.
- **Identity re-probe:** `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202508_202510_5sym_5kind_sampled_canonical_postrepair_postquarantine_v4_20261107T224842Z.json` — match=255, mismatch=0, missing_local=0, missing_remote=0, remote_error=0, placeholder_duplicate_files=0, `cache_identity_vs_binance_vision=GO_PARTIAL_BOUNDED`, `confirmatory_claim_go=NO_GO`. Scope is sampled only (1,15,28,last) × 5 symbols × 3 months × 5 kinds; full-day identity NOT yet verified.

### Cache/git note
`research_state/data_cache` is tracked in this repo; quarantine moved tracked top-level files (git shows deletions) and repair created untracked canonical subdir files. **Bulky cache zip churn is intentionally not staged in this handoff commit** (durable artifacts committed: repair script + FCLR-016 manifests/MD + handoff). Local cache state is auditable/reversible via quarantine manifest.

### Verification
- `python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py` — OK
- `python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v` — 6 OK
- `python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v` — 10 OK
- `python3 scripts/tracka_resume_check.py` — pass=true, network=false, writes_real_research_state=false

### Next (P0)
Expand to `--sample-days full` bounded/chunked identity probe for 2025-08..10 (5 symbols × 5 kinds), repair/quarantine any new conflicts with audited manifests, assemble license/terms+completeness+leakage/prereg evidence package, keep confirmatory `NO_GO` until frozen/admissible; ship hardening guardrails if blocked. Track A monitor-only.
