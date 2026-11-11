# HANDOFF: Next Agentic Work Session — Funding-Conditioned Volatility & Liquidation Risk

**Timestamp:** 2026-11-11T03:20:17Z
**Repo:** Funding-conditioned-volatility-and-liquidation-risk
**Primary Focus:** Unblock FCLR-016 v5 Confirmatory Experiment (Gate 4 v5)

---

## EXECUTIVE SUMMARY

The repository contains a multi-track research program on **funding-conditioned volatility and liquidation risk** in crypto perpetual futures (Binance UM + Hyperliquid). The **critical path bottleneck** is **FCLR-016 v5**, a Gate 4 v5 confirmatory experiment frozen at **2025-08-01..2025-10-31** (5 symbols × 5 data kinds, 92 calendar days, 1855 files expected).

**Status:** **BLOCKED** on human/legal terms review — cannot be automated. All other admissibility gates are green or mechanically resolvable once terms are resolved.

---

## FCLR-016 v5 — CURRENT STATE (artifacts dated 2026-11-08)

| Artifact | Status | Key Fields |
|----------|--------|------------|
| **Provenance/License Manifest** | `NO_GO` | `confirmatory_provenance_go: false`, `admissibility_complete: false`, `license_terms.status: "EXPLICIT_BLOCKER_UNRESOLVED"`, `cache_identity_vs_binance_vision: "GO_PARTIAL_BOUNDED_IDENTITY_ONLY"` |
| **Completeness/Leakage Audit** | **PASS** | `verdict: "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC"` — 1855/1855 MATCH, 0 gaps, 0 hazards. `admissibility_complete: false` (blocked by terms) |
| **Terms Evidence** | **BLOCKED** | `status: "EXPLICIT_BLOCKER_UNRESOLVED"` — "Automated agent environment cannot perform verifiable human/legal review of external Binance Vision/Binance market-data terms." |
| **Pre-registration** | **DRAFT** | `draft: true`, `frozen_before_outcomes: false`, `promotable_to_frozen: false`, all design_freeze fields = `TO_FREEZE_BEFORE_OUTCOMES` |

---

## UNBLOCKING SEQUENCE (MANDATORY ORDER)

### 1. HUMAN TERMS REVIEW — **CANNOT BE AUTOMATED**
**Required:** A human maintainer/legal reviewer must:
- Access the current Binance Vision Terms of Use / Market Data Terms at `https://data.binance.vision/` (and any linked legal pages)
- Record **verifiable facts only** (no fabrication):
  - `terms_url_reviewed` — exact URL
  - `access_date_utc` — UTC timestamp of review
  - `terms_version_or_snapshot_id` — version/effective date or `not_provided_by_source` with justification
  - `relevant_clause_summary` — factual summary of clauses on: research use, retention/redistribution of derived checksums/manifests in public repo, attribution/restrictions
  - `reviewer_role` — must include "human" / "legal" / "maintainer" (agent-only = rejection)
  - `conclusion` — one of `PERMITTED_WITH_CONDITIONS` | `PERMITTED` | `RESTRICTED` | `PROHIBITED` | `UNCLEAR`
  - `conditions_or_restrictions` — list or `[]` with justification
  - `evidence_artifacts` — optional archived snapshot paths/hashes/URLs
- Create **new artifact** (never rename in place):
  `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`
- Set: `status: "RESOLVED_VERIFIED"`, `fabricated: false`, `confirmatory_provenance_go: true`, `admissibility_complete: true`

**Template generator (read-only, safe):**
```bash
python scripts/fclr016_v5_terms_evidence_template.py \
  --out research_state/fclr016_local_audit/fclr016_v5_terms_evidence_TEMPLATE_$(date -u +%Y%m%dT%H%M%SZ).json \
  --scope-window "2025-08-01..2025-10-31"
```

### 2. UPDATE PROVENANCE MANIFEST
Once terms evidence is `RESOLVED_VERIFIED`:
- Set `license_terms.status: "RESOLVED_VERIFIED"`, `license_terms.fabricated: false`
- Set `confirmatory_provenance_go: true`, `admissibility_complete: true`
- Ensure `no_confirmatory_outcomes: true`
- Save as new timestamped artifact (preserve audit trail)

### 3. FREEZE PRE-REGISTRATION
Finalize exact design (no outcome inspection):
- `draft: false`, `frozen_before_outcomes: true`, `promotable_to_frozen: true`
- `admissibility_complete: true`, `license_terms_resolved: true`
- Populate `design_freeze` with concrete values (splits, features, targets, metrics, stop rule)
- Set `confirmatory_claim_go: "GO"` **only after all gates pass**
- Update `admissibility_refs_sha256` with hashes of the three resolved artifacts

### 4. RUN ADMISSIBILITY PACKAGE CHECK (GATE)
```bash
python scripts/run_funding_ablations.py \
  --check-admissibility-package \
  <provenance_manifest> <completeness_audit> <terms_evidence> <prereg> \
  --expect-go
```
**Must exit 0 with `all_go: true`, `confirmatory_outcomes_permitted: true`.**

### 5. CONFIRMATORY EXECUTION
With admissibility GO, run the confirmatory funding ablations:
```bash
FCLR_EXPERIMENT=FCLR-016 python scripts/run_evaluation.py
# or the Gate 4 confirmatory entry point once admissibility passes
```
**Guardrails:** The confirmatory provenance guard (`check_confirmatory_provenance` in `run_funding_ablations.py`) will refuse if:
- Terms evidence not `RESOLVED_VERIFIED` with human fields
- Provenance manifest not v5 GO (`confirmatory_provenance_go: true`, `admissibility_complete: true`)
- Pre-registration not frozen (`draft: false`, `frozen_before_outcomes: true`)
- Scope mismatch (2025-08-01..2025-10-31)

---

## SECONDARY TRACKS — STATUS & NEXT ACTIONS

| Experiment | Status | Gate | Next Action |
|------------|--------|------|-------------|
| **FCLR-014** (Track C/H001, 2025-01..06) | **NOT_MET** | C2 vs B1: 1.14% QLIKE reduction (need ≥2%), 0/30d blocks | Extend test window or accept INCONCLUSIVE |
| **FCLR-013** (2026 Q3, 2026-07..09) | **NOT_MET** | C2 vs B1: -1.32% (worse), 1/30d blocks | C1 vs B1 showed 3.32% — investigate C2 degradation |
| **FCLR-012-V** (Forward, 2026-10..11) | **INCONCLUSIVE/PILOT** | 15.19% reduction but CI spans 0, 0/30d blocks | Wait for more 2026 data (archive ends 2026-11-02) |
| **FCLR-010** (Track A, Hyperliquid ironflow) | **COMPLETE_NOT_MET** | Binary occurrence Brier — primary contrast not met | Expand Hyperliquid funding/mark features |
| **FCLR-011** (Track B TB1/TB2) | **Mixed** | TB1/TB2 robustness runs completed | Check `evaluation_summary_trackb_TB1_*.md`, `TB2_*.md` |

---

## REPO STRUCTURE QUICK REFERENCE

```
scripts/
  run_evaluation.py           # Main evaluation entry (FCLR-001..014, FCLR-012-V)
  run_funding_ablations.py    # Gate 4 multi-split + confirmatory provenance guard + admissibility package check
  fclr016_validate_v5_admissibility.py  # Standalone validator (deterministic, read-only)
  fclr016_v5_terms_evidence_template.py # Template generator (NON-evidentiary)
  fclr016_v5_admissibility_report.py    # Read-only package report
  fclr010_execute.py          # Track A observed liquidations (ironflow)
  fclr010_harness.py          # Guarded entry for FCLR-010
  ... (50+ other scripts)

src/
  ingest/loader.py            # ZIP/CSV discovery & extraction
  features/funding.py         # Funding features (ffill last-known, trailing stats)
  features/volatility.py      # RV features (trail 6/24/168h, forward RV)
  eval/walkforward.py         # Chronological splits, purge/embargo, train-only norm
  eval/inference.py           # Block bootstrap CI (joint across instruments)
  volatility/...              # Feature engineering, splits, block bootstrap

research_state/
  run_manifest.json           # LFS (1.5MB) — experiment registry, split boundaries, data sources
  fclr016_local_audit/        # FCLR-016 v5 artifacts (provenance, completeness, terms, prereg)
  evaluation_summary_*.md     # 30+ experiment summaries
  pre_registration_*.md       # Frozen pre-registrations
  data_cache/                 # Local Binance Vision cache (2024-01..2026-11)

tests/
  test_fclr016_v5_admissibility_hardening.py  # Adversarial hardening for Gate 4 v5
  test_gate4_v4_*             # Gate 4 v4 leakage/exploratory diagnostics
  test_tracka_hardening_*.py  # Track A adversarial rubric
  test_trackc_*               # Track C panel admissibility, gap repair, provenance
  ... (80+ tests)
```

---

## IMMEDIATE NEXT STEPS FOR NEXT SESSION

1. **Run current admissibility check** to confirm exact blocker state:
   ```bash
   python scripts/run_funding_ablations.py \
     --check-admissibility-package \
     research_state/fclr016_local_audit/fclr016_v5_provenance_license_manifest_20261108T014405Z.json \
     research_state/fclr016_local_audit/fclr016_v5_completeness_leakage_audit_20261108T014405Z.json \
     research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json \
     research_state/fclr016_local_audit/fclr016_v5_confirmatory_prereg_DRAFT_20261108T014835Z.json
   ```

2. **Generate terms evidence template** for human review:
   ```bash
   python scripts/fclr016_v5_terms_evidence_template.py \
     --out research_state/fclr016_local_audit/fclr016_v5_terms_evidence_TEMPLATE_$(date -u +%Y%m%dT%H%M%SZ).json \
     --scope-window "2025-08-01..2025-10-31"
   ```

3. **If human review is available**, create `RESOLVED_VERIFIED` terms evidence artifact with all required fields populated from verifiable facts.

4. **Run the hardening tests** to ensure no regressions:
   ```bash
   python -m pytest tests/test_fclr016_v5_admissibility_hardening.py -v
   python -m pytest tests/test_fclr016_v5_* -v
   ```

5. **Document the outcome** — update this handoff or create a new one with the resolved state.

---

## NON-GOALS (DO NOT PURSUE)

- ❌ Automating/fabricating the terms review — **forbidden by protocol** (validator/package check will refuse)
- ❌ Running confirmatory outcomes on unprovenanced 2025+ data — guard will refuse
- ❌ Modifying frozen splits/pre-registrations post-outcome — violates FCLR-001..014 protocols
- ❌ Mixing Binance + Hyperliquid data in confirmatory tracks — cross-track firewall enforced

---

## KEY PRINCIPLES (from research_protocol.md)

- **Fail-closed**: Any unresolved blocker → refuse confirmatory outcomes
- **Pre-registered before outcomes**: Splits, features, targets, metrics, stop rule frozen BEFORE any holdout inspection
- **No fabrication**: Automated agents must not fabricate permissions, reviews, evidence, or outcomes
- **Honest verdicts**: PILOT/INCONCLUSIVE/NO_GO preserved; no threshold shopping
- **Leakage resistance**: Train-only normalization, purge/embargo ≥7d, funding last-known at/before hour, block bootstrap on whole UTC time blocks

---

**This handoff is the single durable artifact for the next session. Do not create additional documentation files unless explicitly requested.**