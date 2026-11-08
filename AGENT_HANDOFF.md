## Initial Task Message (2026-11-08T01:46:01Z, git 53663353+) — Next Agentic Session (SINGLE DURABLE HANDOFF)

**Repo priority (Funding-conditioned-volatility-and-liquidation-risk):** (1) **Gate 4 v5 admissibility package — Track C funding-conditioned volatility forecasting** — primary; FCLR-H001 `NOT_SUPPORTED`, forecast gate `NOT MET`. Identity + deterministic completeness/leakage evidence **PASS** for frozen 2025-08-01..2025-10-31 (5 symbols × 5 kinds, 1855 checks, hazards 0, canonical cache paths present); `confirmatory_claim_go=NO_GO`, `admissibility_complete=false`. **Unresolved blocker:** Binance Vision/data-use license/terms evidence not verified/fabricated-unsafe (machine-readable manifest records explicit blocker). (2) **Track A observed liquidation risk** — `DATA_BLOCKED`/no trigger; **NO re-probe**. (3) **Track B modeled boundary breach** — `CLOSED_NEGATIVE`.

### Completed this session (measurable, heavy, green; no confirmatory outcomes)
- **P0.1 — Machine-readable provenance/license manifest (v5):** `research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json` (sha256 `6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346`). Includes frozen scope, identity consolidation/probe refs+hashes, Binance Vision URL templates/access facts, quarantine ref, **`license_terms.status=EXPLICIT_BLOCKER_UNRESOLVED`**, `fabricated=false`, `confirmatory_provenance_go=false`, `admissibility_complete=false`. Verifiable facts only.
- **P0.2 — Deterministic completeness/leakage audit:** `research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json` (sha256 `32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`). Expected/observed 1855/1855, by-kind/by-result, hazards 0, placeholder duplicates 0, canonical cache path gaps 0, `PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC`. Window non-overlap vs Gate 4 v4 confounded 2024-04..09 asserted; references identity consolidation + quarantine artifacts. No outcomes.
- **P0 hardening — v5-aware confirmatory provenance guard + tests:** `scripts/run_funding_ablations.py` `check_confirmatory_provenance` now fail-closed for v5 manifests unless `confirmatory_provenance_go=true`, `admissibility_complete=true`, `no_confirmatory_outcomes=true`, `license_terms.status=RESOLVED_VERIFIED` and not fabricated, identity not `IDENTITY_ONLY`, and scope covers requested range. Legacy behavior preserved for pre-v5 manifests. Added `tests/test_fclr016_v5_admissibility_guard.py` (7 tests) covering refusal matrix and synthetic fully-resolved fixture acceptance (test-only). **No confirmatory outcomes produced.**
- **Verified green:** `python3 -m py_compile scripts/run_funding_ablations.py scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py` OK. `python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard -v` **13/13 OK**.

### Single highest-value next task (heavy, measurable, NO confirmatory outcomes)
**P0 — Resolve/record verifiable license/terms evidence for v5 frozen scope OR (if blocked) produce substantive guard/prereg/terms-evidence scaffolding with explicit blockers. Keep `confirmatory_claim_go=NO_GO`.**

1. **License/terms evidence (blocker):** Obtain/record **verifiable facts only** (exact URL reviewed, access date UTC, version/snapshot identifier if available, relevant clause summary, conclusion) for Binance Vision/Binance market-data terms applicable to this research use and repo retention of derived checksums/manifests. **Do not fabricate.** If environment cannot verify externally, add a deterministic `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_<ts>.md/json` stating the structural blocker + exact evidence fields required, and keep `license_terms.status=EXPLICIT_BLOCKER_UNRESOLVED`, `confirmatory_provenance_go=false`.
2. **Prereg/freeze draft (NO_GO, blocked-aware):** Create `research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_<ts>.json`/`.md` with frozen splits/features/targets/metrics/stop rule, window/scope hashes (identity consolidation + provenance manifest + completeness/leakage audit SHA256s), and explicit gates: `frozen_before_outcomes=false` (draft), `confirmatory_claim_go=NO_GO`, `license_terms_resolved=false` (or true only with evidence), `admissibility_complete=false` until all pass. **Must not be promoted to frozen without terms evidence + guard acceptance; no outcomes.**
3. **Guard acceptance evidence (if feasible):** Extend tests/guard to validate prereg draft linkage fields and refusal when `admissibility_complete=false`/terms unresolved; run full relevant FCLR014/016 + funding-ablations guard tests green. Any new schema must be fail-closed.
4. **If 1 blocked:** ship ≥1 substantive hardening (e.g., terms-evidence schema + validator test; prereg-draft schema + refusal test; `run_funding_ablations` manifest-path logging/hash recording in dry-run metadata) with green gates. No status-only work.

### Focus campaign (mandatory, no opt-out)
Every session until Gate 4 v5 admissibility package is complete (`admissibility_complete=true`, verifiable license/terms evidence recorded, prereg frozen before outcomes, FCLR-014/v5 guard accepts) while `confirmatory_claim_go` remains `NO_GO` until all pass must either (a) advance admissibility with green gates and **no confirmatory outcomes**, or (b) if blocked, ship ≥1 substantive hardening/test/guardrail with green gates. Track A re-probe and confirmatory outcomes on unprovenanced/incomplete 2025+ are prohibited. No status-only sessions. A session without (a)/(b) plus updated `AGENT_HANDOFF.md` is incomplete.

### Current gate state (evidence-backed, 2026-11-08T01:46:01Z)
- **Track A** = `DATA_BLOCKED` (Hyperliquid ironflow data_through 2026-10; 2026-11..2027-02 absent). **NO re-probe.**
- **Track B** = `CLOSED_NEGATIVE`.
- **Track C / FCLR-H001** = `NOT_SUPPORTED` (forecast gate NOT MET; FCLR-003 sealed 2024 -3.78%; FCLR-006 -69.90%; FCLR-007 -3.42%; FCLR-008 +4.30% CI crosses zero). Gate 4 v4 = `EXPLORATORY_INCONCLUSIVE` (confounded 2024-04..09).
- **Gate 4 v5 confirmatory** = `NOT_READY/NO_GO` (`admissibility_complete=false`). Identity consolidated (`f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`, 1855/1855 MATCH). Completeness/leakage deterministic **PASS** (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`). Provenance/license manifest present but **terms unresolved blocker** (`6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346`). Prereg/freeze + guard acceptance pending.
- **Green gates:** `py_compile` OK (run_funding_ablations, fclr016 verify/repair). `test_fclr014_anchor_integrity` + `test_fclr016_provenance_probe` + `test_fclr016_v5_admissibility_guard` = **13/13 OK**.

### Verification commands
```bash
python3 -m py_compile scripts/run_funding_ablations.py scripts/fclr016_verify_cache_provenance_2025plus.py scripts/fclr016_repair_canonical_cache.py
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard -v
python3 - <<'PY'
import json
for p in [
 'research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json',
 'research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json']:
 d=json.load(open(p)); print(p.split('/')[-1], d['confirmatory_claim_go'], d['admissibility_complete'], d.get('verdict'))
PY
```

### Acceptance criteria
- All admissibility artifacts machine-readable, deterministic, hash-referenced. `confirmatory_claim_go=NO_GO` until full package passes and v5/FCLR-014 guard accepts.
- License/terms evidence = verifiable facts only; never fabricated. Unresolved => explicit blocker, `confirmatory_provenance_go=false`.
- Guard refusals parseable/explicit, exit!=0, no tracebacks; canonical outputs unchanged on blocked paths.
- No sealed FCLR artifacts reopened; no threshold-shopping; no track conflation; no economic/overlay claims; **no confirmatory outcomes on unprovenanced/incomplete 2025+**.
- Root md/json bound respected (`AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md` only at root research docs as applicable); no `.github/workflows` edits; no status-only/poller/wrapper/scheduler families.

### Do NOT
- Re-probe exhausted Track A; reopen sealed FCLR-001/002/003/006/007/008; threshold-shop; merge tracks; claim economic value/overlay; treat identity/completeness-only as confirmatory GO; fabricate license/terms permissions; run confirmatory outcomes on unprovenanced/incomplete 2025+; edit `.github/workflows`; add status-only families.
