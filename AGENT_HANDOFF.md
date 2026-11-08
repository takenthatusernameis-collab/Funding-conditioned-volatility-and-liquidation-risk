## Initial Task Message (2026-11-08T00:41:32Z, git 53663353) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Gate 4 v5 admissibility package — Track C funding-conditioned volatility forecasting** — primary; FCLR-H001 `NOT_SUPPORTED`, forecast gate `NOT MET`; identity evidence CONSOLIDATED (hazards zero, 1855/1855 MATCH, full-scope Binance Vision remote identity evidence for frozen 2025-08..10; BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT × 5 kinds); `confirmatory_claim_go=NO_GO` until full admissibility package passes (license/terms/provenance manifest, completeness/leakage audit, prereg freeze, FCLR-014 guard acceptance). (2) **Track A observed liquidation risk** — `DATA_BLOCKED`/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (3) **Track B modeled boundary breach** — `CLOSED_NEGATIVE`.

### Completed this session (measurable, heavy, green)
- **P0 step 1 — Identity evidence consolidated (machine-readable):** `research_state/fclr016_local_audit/fclr016_v5_identity_consolidation_20261108T003908Z.json`. Lists 3 probe artifacts + SHA256s, per-probe summaries, frozen scope (2025-08-01..2025-10-31; 5 symbols × 5 kinds; sample-days full). Aggregate: `total_checks=1855, hazards=0, cache_identity_vs_binance_vision_hazards_zero=true`. Explicit `confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `no_confirmatory_outcomes=true`. **Identity only — necessary, not sufficient.**
- **Verified:** `python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py` OK. `python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -q` **6/6 OK**.

### Single highest-value next task (heavy, measurable, NO confirmatory outcomes)
**P0 — Complete Gate 4 v5 admissibility package for frozen 2025-08..10 (5 symbols, 5 kinds). Keep `confirmatory_claim_go=NO_GO`.**

1. **License/terms/provenance manifest (FCLR-014 guard requirement):** create machine-readable manifest for frozen scope (Binance Vision source base URLs/patterns used by probes, access dates/method, unauthenticated evidence, probe artifact refs/hashes, terms/license references as **verifiable facts only** — do not fabricate permissions). Mark uncertainties as explicit blockers. Make schema suitable for `--provenance-manifest` consumption; if current tooling lacks schema validation, add a small guard/test (substantive hardening) in the same session.

2. **Completeness/leakage audit artifact (deterministic, no outcomes):** emit `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_<ts>.json` verifying full symbol×kind×day coverage matches frozen scope (1855 checks / expected calendar coverage per kind); assert no overlap with consumed/confounded/guard windows per Gate 4 v4/FCLR-014 (2024-04..09 confounded/exploratory context, other sealed/guard windows as applicable); reference quarantine artifacts (`fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json` etc.) and identity consolidation hash. Any gap => `admissibility_complete=false`, NO_GO.

3. **Prereg/freeze draft (only if 1-2 pass without blockers):** create preregistered confirmatory design doc/JSON with frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash, and explicit `confirmatory_claim_go=NO_GO` until FCLR-014 guard acceptance. **No confirmatory outcomes.**

4. **If blocked on 1-3:** keep v5 `NOT_READY/NO_GO`; ship ≥1 substantive hardening/test/guardrail (e.g. tests for provenance-manifest schema/required fields, FCLR-014 guard acceptance/refusal matrix for v5 identity+provenance artifacts, completeness-audit deterministic checks) with green gates. No status-only work.

### Focus campaign (mandatory, no opt-out)
Every session until Gate 4 v5 admissibility package is complete and `admissibility_complete=true` with `confirmatory_claim_go` still `NO_GO` pending FCLR-014 guard acceptance must either:
(a) advance Gate 4 v5 admissibility (license/terms/provenance manifest, completeness/leakage audit, prereg/freeze, guard evidence) with green gates and **no confirmatory outcomes**, or
(b) if blocked on (a), ship ≥1 substantive hardening/test/guardrail with green gates.
Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated `AGENT_HANDOFF.md` is incomplete.

### Current gate state (evidence-backed, 2026-11-08T00:41:32Z)
- Track A = `DATA_BLOCKED` (no trigger; **NO re-probe**). Track B = `CLOSED_NEGATIVE`. Track C/FCLR-H001 = `NOT_SUPPORTED` (forecast gate NOT MET; all confirmatory panels exhausted: FCLR-003 sealed 2024 -3.78%; FCLR-006 -69.90%; FCLR-007 -3.42%; FCLR-008 +4.30% but CI crosses zero). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09). Gate 4 v5 confirmatory = `NOT_READY/NO_GO` (identity evidence consolidated, hazards zero; admissibility package incomplete: provenance/license manifest, completeness/leakage audit, prereg/freeze pending).
- Green gates: `py_compile` OK (fclr016 verify/repair, run_funding_ablations); `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` = **6/6 OK**.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 - <<'PY'
import json
d=json.load(open('research_state/fclr016_local_audit/fclr016_v5_identity_consolidation_20261108T003908Z.json'))
print(d['aggregate'], d['confirmatory_claim_go'], d['admissibility_complete'])
PY
```

### Acceptance criteria
- Identity/provenance/completeness/leakage/prereg artifacts are machine-readable, deterministic, hash-referenced where applicable.
- Any uncertainty in license/terms recorded as explicit blocker (never fabricated). `confirmatory_claim_go=NO_GO` until full package passes and FCLR-014 guard accepts.
- Refusals parseable JSON, exit!=0, no tracebacks; canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims; **no confirmatory outcomes on unprovenanced 2025+**.
- Root md+json bound respected (`AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md`); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat identity-only evidence as confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

---
Previous detailed session logs retained in git history.
