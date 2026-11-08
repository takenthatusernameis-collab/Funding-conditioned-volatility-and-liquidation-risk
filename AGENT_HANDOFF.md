## Initial Task Message (2026-11-08T02:37:50Z, git f17c20ca/HEAD clean verified) — SINGLE DURABLE HANDOFF / Next Agentic Session

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility forecasting + liquidation risk). **Mission constraint:** empirical/research only; no trading; no fabricated data/terms; chronological leakage-resistant OOS only; sealed holdouts untouched; no `.github/workflows` edits; no credentials/paid/manual/API-key/bypass sources.

### Verified current state (do not re-litigate without new evidence)
- **P0 Track C / Gate 4 v5 confirmatory (funding-conditioned volatility):** `NOT_READY / confirmatory_claim_go=NO_GO`, `admissibility_complete=false`, `confirmatory_outcomes_permitted=false`. Identity consolidated (1855/1855 MATCH, hazards 0; `f73610420932ed1c9072c447b2b537ebf73f0ba5380b1374bd3640acbb143985`). Completeness/leakage deterministic **PASS** but `admissibility_complete` remains false in frozen artifact (`32dfcddca782cf7e2f029b2814dd86c5054a0d5069785ab29e8814fd98ccfca8`, frozen 2025-08-01..2025-10-31, 5 symbols × 5 kinds). **Hard blocker (cannot be bypassed):** Binance Vision/data-use license/terms **not human-verified** — `EXPLICIT_BLOCKER_UNRESOLVED` (`8128c1d513bee2e16a57f3ee19d103d17ad0d68ca15378724c7d432e35d59923`). Provenance manifest blocked (`6888116a707a4fe1bad84d6fb1b957dfdd2890c2ce48a3c3bc9430e17f325346`). Prereg **DRAFT/not frozen** (`8bf5e7f2ac593048c9782cbb8cfabd041dea97cc46c30288d0cb09ddc8957f7f`). Validator + `run_funding_ablations` package check both return `ok=true, all_go=false, confirmatory_outcomes_permitted=false` with blockers `[terms_resolved_verified, provenance_manifest_go, completeness_leakage_pass, prereg_frozen_non_draft, prereg_claim_go]`; `--expect-go` exits 2.
- **Historical signal context:** FCLR-H001 `NOT_SUPPORTED`; forecast gate NOT MET; Track C confirmatory closed on 2024 sealed evidence (e.g., FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Gate 4 v4 `EXPLORATORY_INCONCLUSIVE` (confounded). No threshold-shopping; no sealed anchor reopen.
- **Track A (observed liquidation risk):** `DATA_BLOCKED` (Hyperliquid ironflow `data_through=2026-10`; 2026-11..2027-02 absent). **NO re-probe.** Follow trigger-only guarded protocol only if admissible unauthenticated Hyperliquid data appears AND rubric passes; preregister before outcome inspection.
- **Track B (modeled boundary breach):** `CLOSED_NEGATIVE`. Never conflate modeled vs observed.

### Green gates (verified this session)
```bash
python3 -m py_compile scripts/fclr016_validate_v5_admissibility.py scripts/run_funding_ablations.py  # OK
python3 -m unittest tests.test_fclr014_anchor_integrity tests.test_fclr016_provenance_probe tests.test_fclr016_v5_admissibility_guard tests.test_fclr016_v5_admissibility_validator -q  # 23/23 OK
python3 scripts/fclr016_validate_v5_admissibility.py --provenance-manifest research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json --completeness-audit research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json --terms-evidence research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json --prereg-draft research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # all_go=false, confirmatory_outcomes_permitted=false
python3 scripts/run_funding_ablations.py --check-admissibility-package research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json  # all_go=false, exit 0; --expect-go => exit 2
```

### Mandatory focus campaign (no opt-out, heavy work required)
Every session must produce **≥1 substantive, measurable** deliverable with green gates and update this handoff. **No status-only sessions.** Confirmatory outcomes on unprovenanced/incomplete 2025+ are prohibited.

**P0 — Gate 4 v5 admissibility (default):** option (a) human-verified Binance Vision terms review is blocked in automated environments — **do not fabricate**. Option (b) **required now:** ship fail-closed hardening/tests/guardrails around the v5 package.
1. Add adversarial refusal/acceptance tests (tmp-isolated, no network, no outcome reads): resolved terms missing required fields/conclusion/human reviewer must refuse; terms hash-ref mismatch refuses; draft prereg promoted without `admissibility_complete`+terms resolved refuses; completeness verdict/pass inconsistency refuses; `--expect-go`/exit codes stable/parseable.
2. Align `check_confirmatory_provenance` vs package-check behavior on synthetic `GO` fixtures (prove no false-accept, no canonical mutation, no outcome loading).
3. Canonicalize/verify CLI contract: stable JSON keys, parseable blocked output, nonzero on `--expect-go` refusal, zero on blocked-check-without-expect-go; add/keep tests.
4. If **real human-verified terms evidence** appears in-repo: create `fclr016_v5_terms_evidence_RESOLVED_*` with verifiable facts only (terms URL reviewed, access date UTC, version/snapshot, clause summary, human/legal `reviewer_role`, conclusion, conditions, artifacts/hashes, `fabricated=false`), reconcile provenance+completeness+prereg hashes/refs, freeze prereg before outcomes, run validator+package `--expect-go`; only then may confirmatory Gate 4 v5 proceed.

**P1 — Track A (only on trigger, no proactive probing):** new admissible unauthenticated Hyperliquid observed source passing full rubric (≥5 symbols, ≥3 non-overlapping 30-day blocks or equivalent completeness, license OK, schema compatible, census/defensible) => preregister before outcome inspection; Hyperliquid-only; never merge modeled/observed.

**P2 — Research quality (bounded, non-claim):** leakage-audit hardening, dependency-light reproducibility, deterministic tests/fixtures, provenance manifests — only if they do not touch sealed outcomes or imply confirmatory GO.

### Acceptance / do-NOT
- `confirmatory_claim_go` remains `NO_GO` until full v5 package passes with verifiable human-terms evidence + frozen prereg + all guards green.
- **DO NOT:** fabricate terms/license/reviews; run confirmatory outcomes on unprovenanced/incomplete 2025+; freeze/promote prereg while blockers exist; reopen sealed FCLR anchors; threshold-shop; merge Track A/B/C semantics; claim economic/overlay value; re-probe Track A; edit `.github/workflows`; add status-only/poller/wrapper/scheduler families; create competing handoff files.
- This file (`AGENT_HANDOFF.md`) is the **single durable handoff**. Update it with exact changes, commands, results, blockers, and next actionable task every substantive session.
