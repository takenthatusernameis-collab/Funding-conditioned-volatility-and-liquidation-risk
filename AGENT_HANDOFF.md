## Initial Task Message (2026-11-07T22:40:31Z) — Next Agentic Session

**Repo priority (by name: Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; forecast gate NOT MET (H001 NOT_SUPPORTED). (2) **Gate 4 v5 confirmatory path** — NOT_READY/NO_GO until 2025+ canonical identity + license/terms + completeness + freeze/prereg proven; **no confirmatory outcomes on unprovenanced/incomplete 2025+ cache** (FCLR-014 guard active). (3) **Track A observed liquidation risk** — DATA_BLOCKED, no trigger (data_through 2026-10; 2026-11..2027-02 absent; Hyperliquid-only); **NO re-probe**. (4) **Track B modeled boundary breach** — CLOSED_NEGATIVE.

### Single highest-value next task (heavy, measurable, unblocked)
**P0 — Make 2025-08..10 a v5-candidate only by completing canonical identity+provenance; do NOT run outcomes.**
1. **Repair canonical cache completeness** for `BNBUSDT,SOLUSDT,XRPUSDT` across `2025-08,2025-09,2025-10` (all 5 kinds: `fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines`; daily kinds require `<kind>-YYYY-MM-DD>/<SYM>-1h-YYYY-MM-DD.zip`). Evidence from this session: BTC/ETH sampled canonical files MATCH Binance Vision (34/34 for 2025-09+10; BTC/ETH 2025-08 canonical present where matched), but BNB/SOL/XRP are missing sampled daily canonical subdirs (BNB 2025-09 also missing `klines-*` subdirs). If admissible local source bytes already exist, promote only with verifiable sha256 lineage; otherwise perform bounded unauthenticated Binance Vision acquisition with deterministic manifest + remote sha256/etag/last-modified + license/terms evidence recorded in `research_state/fclr016_local_audit/` (no outcomes, no auth/paid/manual/key bypass).
2. **Rerun bounded FCLR-016 probe** (sample days 1,15,28 minimum; expand to `full` only if bounded/justified) for the repaired months/symbols; require for any v5 GO_PARTIAL/GO claim: `mismatch==0, missing_local==0, missing_remote==0, remote_error==0, placeholder_duplicate_files==0` on the frozen sampled/full scope, plus explicit `confirmatory_claim_go` remains NO_GO until license/completeness/leakage/prereg/freeze are satisfied.
3. **If identity cannot be completed admissibly:** keep Gate 4 v5 `NOT_READY/NO_GO`; ship ≥1 substantive hardening/test/guardrail with green gates (e.g., completeness-threshold guard refusing confirmatory manifests whose canonical cache coverage is below required symbol×kind×day set; fixture test) and record evidence. Do not draft a confirmatory prereg claiming GO for 2025-08..10.
4. **Track A:** only on genuinely new unauthenticated admissible source passing strict rubric; otherwise skip re-probe.

### Current gate state (evidence-backed)
- Track A = `DATA_BLOCKED` (no trigger; monitor-only).
- Track B = `CLOSED_NEGATIVE`.
- Track C/H001 = `NOT_SUPPORTED` (forecast gate NOT MET).
- Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09; not promotable).
- Gate 4 v5 = `NOT_READY` / confirmatory `NO_GO`.
  - 2025-01 BTC/ETH canonical sampled: `GO_PARTIAL_BOUNDED` match=6 mismatch=0 (`fclr016_binance_vision_probe_202501_bounded_canonical_20261107T210801Z.*`).
  - 2025-08 canonical v2 sampled: match=37 mismatch=0 **missing_local=48** placeholder_duplicate_files=32 => `NO_GO` (`*_202508_*canonical_v2_20261107T223731Z.*`).
  - 2025-09..10 canonical sampled: match=74 mismatch=0 **missing_local=96** placeholder_duplicate_files=64 => `NO_GO` (`*_202509_202510_*canonical_20261107T223633Z.*`). BTC/ETH matched 34/34; BNB/SOL/XRP lacked canonical daily coverage.
  - Non-overlap proof for 2025-08-01..2025-10-29 vs consumed/confounded/guard windows (FCLR-002/003/013 committed 2024 ranges, v3 2024-01..03-30, v4 2024-04..09-29, guard 2024-01..12, 2026-07..09): **no overlap** (necessary only).

### Bottlenecks removed / guardrails active
- FCLR-014 confirmatory provenance guard in `scripts/run_funding_ablations.py`: confirmatory 2025+ runs fail closed (rc=2, JSON `REFUSED`) without `--provenance-manifest` / verified evidence; exploratory/pilot unaffected. Guarded by `tests/test_fclr014*.py` (10 tests).
- FCLR-016 canonical-path guardrails (no network): `tests/test_fclr016_provenance_probe.py` (3 tests) — top-level same-name daily zips are **not** canonical identity evidence; placeholders flagged.
- Track A inefficiency removed: no re-probe of exhausted/absent months/windows; monitor-only.
- Superseded/misleading evidence control: 2025-08 non-canonical probe comparing top-level placeholders is superseded by `*_canonical_v2_*`; do not cite as identity evidence.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
python3 scripts/fclr016_verify_cache_provenance_2025plus.py --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months 2025-08,2025-09,2025-10 --kinds fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines --sample-days 1,15,28 --out-tag <tag>
python3 scripts/tracka_resume_check.py
python3 -m unittest tests.test_funding_ablations -v  # requires numpy; run in project env
python3 -m unittest discover -s tests -q
```

### Acceptance criteria
- Deterministic JSON+MD probe artifacts under `research_state/fclr016_local_audit/` with explicit `cache_identity_vs_binance_vision` and `confirmatory_claim_go` fields.
- No confirmatory outcomes on unprovenanced/incomplete 2025+ cache; FCLR-014 guard remains fail-closed.
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected; no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A months/windows; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat v4/exploratory as confirmatory; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

**Focus campaign (mandatory, no opt-out):** Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 bounded canonical identity/provenance verification with green gates, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked on NO-GO. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions.

---

## 2026-11-07T22:37:31Z — FCLR-016 bounded 2025-08..10 canonical identity probe (NO OUTCOMES)

**Focus (mandatory):** (a) advanced FCLR-016 bounded identity verification across symbols×months with green gates.

### Work done
- Bounded unauthenticated Binance Vision probes (sample days 1,15,28; BTC/ETH/BNB/SOL/XRP; `fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines`; canonical). No confirmatory outcomes.
  - `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202508_5sym_5kind_sampled_canonical_v2_20261107T223731Z.json|.md`: match=37 mismatch=0 missing_local=48 missing_remote=0 remote_error=0 placeholder_duplicate_files=32 => `cache_identity_vs_binance_vision=NO_GO` (canonical subdirs incomplete).
  - `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202509_202510_5sym_5kind_sampled_canonical_20261107T223633Z.json|.md`: match=74 mismatch=0 missing_local=96 missing_remote=0 remote_error=0 placeholder_duplicate_files=64 => `NO_GO`. BTC/ETH sampled MATCH 34/34 for 2025-09+10; BNB/SOL/XRP missing daily canonical coverage (BNB 2025-09 missing `klines-*` subdirs).
- 2025-01 BTC/ETH canonical sampled retained as `GO_PARTIAL_BOUNDED` match=6 mismatch=0 (`*_202501_bounded_canonical_20261107T210801Z.*`). Earlier 2025-08 top-level-placeholder probe superseded by `*_canonical_v2_*`.
- Added `tests/test_fclr016_provenance_probe.py` (3 tests, green, no network): top-level placeholder not canonical/flagged; canonical subdir selected; fundingRate monthly path.

### Non-overlap (necessary only)
2025-08-01..2025-10-29 candidate: no overlap vs FCLR-002/003/013 2024 committed ranges, Gate4 v3 2024-01..03-30, v4 2024-04..09-29, guards 2024-01..12 and 2026-07..09. Still `confirmatory_claim_go=NO_GO` until full canonical identity+license/terms+completeness+leakage/prereg+freeze.

### Verification
- `python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v` — 6 OK
- `python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v` — 10 OK
- `python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/run_funding_ablations.py` — OK
- `python3 scripts/tracka_resume_check.py` — pass=true, network=false
- `python3 -m unittest tests.test_funding_ablations -v` — env-blocked (`numpy` missing); no funding-ablation logic changed.

### Next
P0: complete/verify admissible canonical daily subdirs for BNB/SOL/XRP 2025-08..10 with deterministic sha256+license evidence (no outcomes), rerun FCLR-016; if not admissible/complete keep v5 `NOT_READY/NO_GO` and ship completeness-threshold confirmatory guard + tests. Track A monitor-only.

**Focus campaign (mandatory, no opt-out):** Every session until Track C/H001 forecast gate passes must either (a) advance FCLR-016 bounded identity verification across symbols×months with green gates, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked on NO-GO. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions.
