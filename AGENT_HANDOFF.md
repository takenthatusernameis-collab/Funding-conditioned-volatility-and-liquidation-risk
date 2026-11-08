## Initial Task Message (2026-11-08T00:33:00Z, git 113c4453) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Track C funding-conditioned volatility forecasting** — primary; FCLR-H001 `NOT_SUPPORTED`, forecast gate `NOT MET`. (2) **Gate 4 v5 confirmatory path** — 2025-08..10 canonical cache for BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT has **full-scope Binance Vision remote identity evidence** (see artifacts); `confirmatory_claim_go=NO_GO` everywhere until full admissibility package passes (license/terms/provenance manifest, completeness, leakage, prereg freeze, FCLR-014 guard acceptance). (3) **Track A observed liquidation risk** — `DATA_BLOCKED`/no trigger (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent); **NO re-probe**. (4) **Track B modeled boundary breach** — `CLOSED_NEGATIVE`.

### Completed this session (measurable, heavy, green)
- **BTCUSDT+ETHUSDT full v5 identity probe (resumed, completed):** `research_state/fclr016_local_audit/fclr016_binance_vision_probe_202508_202510_btc_eth_full_canonical_v5_20261108T003047Z.json` (+`.md`). Scope: BTCUSDT,ETHUSDT × 2025-08,09,10 × fundingRate,klines,markPriceKlines,indexPriceKlines,premiumIndexKlines × `sample-days full`. Summary: `total=742, match=742, mismatch=0, missing_local=0, missing_remote=0, remote_error=0, placeholder_duplicate_files=0, new_this_run=192` (resumed from `_partial_20261107T235328Z.json`, 550 checks). `cache_identity_vs_binance_vision=GO_PARTIAL_BOUNDED` (script label; hazards zero on frozen scope), `confirmatory_claim_go=NO_GO`.
- **BNBUSDT fresh full v5 post-quarantine identity probe:** `.../fclr016_binance_vision_probe_202508_202510_bnb_full_canonical_v5_postquarantine_fresh_20261108T003159Z.json`. `total=371, match=371, mismatch=0, missing_local=0, missing_remote=0, remote_error=0, placeholder_duplicate_files=0`. `GO_PARTIAL_BOUNDED` (hazards zero), `confirmatory_claim_go=NO_GO`. Supersedes caveat-only reliance on chunk+reconciliation for identity (reconciliation `fclr016_bnb_postquarantine_reconciliation_20261107T235830Z.json` remains historical evidence).
- **SOLUSDT+XRPUSDT full v5 post-quarantine identity probe:** `.../fclr016_binance_vision_probe_202508_202510_sol_xrp_full_canonical_v5_postquarantine_20261108T003159Z.json`. `total=742, match=742, mismatch=0, missing_local=0, missing_remote=0, remote_error=0, placeholder_duplicate_files=0`. `GO_PARTIAL_BOUNDED` (hazards zero), `confirmatory_claim_go=NO_GO`.
- **Aggregate (identity only, necessary not sufficient):** 5 symbols × 371 checks = 1855 checks, **1855 MATCH, 0 hazard** on frozen 2025-08..10 / 5-kind full-scope. **Still NO_GO for confirmatory claims** — missing admissibility package items below.
- **Gates:** `py_compile` OK (`fclr016_verify_cache_provenance_2025plus.py`, `fclr016_repair_canonical_cache.py`, `run_funding_ablations.py`). `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` = **6/6 OK**.

### Single highest-value next task (heavy, measurable)
**P0 — Assemble Gate 4 v5 full admissibility package for 2025-08..10 (5 symbols, 5 kinds), NO confirmatory outcomes.**
1. **Consolidate identity evidence manifest:** produce a single machine-readable artifact (e.g. `research_state/fclr016_local_audit/fclr016_v5_identity_consolidation_20261108T003200Z.json`) listing the 3 probe JSONs above, per-symbol totals/hazards, frozen scope, and explicit `cache_identity_vs_binance_vision_hazards_zero=true` / `confirmatory_claim_go=NO_GO` / `admissibility_complete=false`.
2. **License/terms/provenance manifest (FCLR-014 guard requirement):** create a machine-readable Binance Vision/data-use license/terms/provenance manifest for the frozen scope (source base, access dates/method, unauthenticated evidence, terms/license references as verifiable facts, no invented permissions), suitable for `--provenance-manifest`. Do **not** fabricate terms; record verifiable evidence and any uncertainty as explicit blockers.
3. **Completeness/leakage checks (no outcomes):** verify full symbol×kind×day coverage against the frozen scope (1855 checks implies full daily+monthly coverage per probe semantics); confirm no overlap with consumed/confounded/guard windows per Gate 4/v4/FCLR-014 constraints; record reversible quarantine evidence references (`fclr016_quarantine_top_level_placeholders_bnbsolxrp_full_20261107T235600Z.json` etc.). Emit deterministic audit artifact.
4. **Prereg/freeze (only if 1-3 pass):** draft/commit preregistered confirmatory design (frozen splits/features/targets/metrics/stop rule, data hashes, provenance manifest hash) but keep `confirmatory_claim_go=NO_GO` until frozen+FCLR-014 guard-accepted. **No confirmatory outcomes on unprovenanced/incomplete 2025+ cache.**
5. **If blocked:** keep v5 `NOT_READY/NO_GO`; ship ≥1 substantive hardening/test/guardrail (e.g. FCLR-014/016 guard tests for full-scope identity artifact acceptance/refusal matrix, provenance-manifest schema validation) with green gates. No status-only work.

### Current gate state (evidence-backed, 2026-11-08T00:33:00Z)
- Track A = `DATA_BLOCKED` (no trigger; `tracka_resume_check.py` PASS, local dry-run, no writes). Track B = `CLOSED_NEGATIVE`. Track C/FCLR-H001 = `NOT_SUPPORTED` (forecast gate NOT MET). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09). Gate 4 v5 confirmatory = `NOT_READY/NO_GO` (identity evidence complete on frozen scope; admissibility package incomplete).
- Green gates this session: `py_compile` OK (fclr016 verify/repair, run_funding_ablations); `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` = **6/6 OK**.

### Verification commands
```bash
python3 -m py_compile scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py scripts/run_funding_ablations.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe -v
python3 -m unittest discover -s tests -p 'test_fclr014*.py' -v
python3 scripts/tracka_resume_check.py
python3 - <<'PY'
import json,glob
for p in sorted(glob.glob('research_state/fclr016_local_audit/fclr016_binance_vision_probe_202508_202510_*_20261108T003*.json')):
    d=json.load(open(p)); print(p.split('/')[-1], d['summary'], d['cache_identity_vs_binance_vision'], d['confirmatory_claim_go'])
PY
```

### Acceptance criteria
- Identity evidence: deterministic JSON artifacts; hazards zero on frozen scope; `confirmatory_claim_go=NO_GO`.
- Admissibility: machine-readable provenance/license manifest + completeness/leakage/prereg artifacts; FCLR-014 guard fail-closed; no confirmatory outcomes until all pass.
- Refusals parseable JSON, exit!=0, no tracebacks, canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims.
- Root md+json bound respected (`AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md`); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat identity-only evidence as confirmatory GO; run confirmatory outcomes on unprovenanced 2025+; edit `.github/workflows`; add status-only families.

### Focus campaign (mandatory, no opt-out)
Every session until Track C/FCLR-H001 forecast gate passes must either (a) advance Gate 4 v5 admissibility (identity/provenance/completeness/leakage/prereg/guard evidence) with green gates and **no outcomes**, or (b) ship ≥1 substantive hardening/test/guardrail with green gates if blocked. Track A re-probe and confirmatory outcomes on unprovenanced 2025+ are prohibited. No status-only sessions. A session that ends without (a) or (b) plus an updated `AGENT_HANDOFF.md` is incomplete.

---
Previous detailed session logs retained in git history.
