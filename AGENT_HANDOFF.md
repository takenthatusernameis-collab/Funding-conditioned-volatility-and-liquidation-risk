# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-13T04:20:00Z
**Status:** `ACTIVE_HEAVY_CAMPAIGN` — **not closed, not monitor-only.**

**This file is the ONLY durable handoff.** It supersedes every earlier handoff, checkpoint, closure, and frontier entry. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are redirects to this file. Do not create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file. Update this file in place by appending a dated `## SESSION LOG` entry.

---

## START HERE — `FCLR-HEAVY-CONFIRM-20261113T041200Z` (P1, Track C)

**The previous handoff was wrong.** It declared every volatility campaign `NOT_MET` and "all claim-worthy local admissible experiments exhausted," then banned heavy work. That conclusion is contradicted by the repository's own sealed artifacts and by the data still on disk. This campaign exists to resolve the contradiction with a pre-registered, adequately-powered test.

### The contradiction that was suppressed

| Experiment | Window | Result | Block gate |
|---|---|---|---|
| **FCLR-011** | 2026-05-08..2026-08-06 | **FORECAST_GATE_PASSED**: C2 vs B1 rel QLIKE **4.94%**, 95% CI **[-0.032546, -0.001418]**, 5 instruments | **3 blocks — PASS** |
| FCLR-012-V | 2026-10-29..2026-11-02 | +15.19% point estimate, CI crosses zero | 0 blocks — INCONCLUSIVE |
| FCLR-013 | 2026-08-26..2026-09-30 | -1.32% | 1 block — NOT_MET |
| FCLR-014 | 2025-05-22..2025-06-07 | 1.14%, CI crosses zero | 0 blocks — NOT_MET |
| FCLR-009 | 2025-06-08..2025-12-31 | -0.43% | 6 blocks — NOT_MET |
| FCLR-006 / FCLR-007 | 2026 | underpowered | 2 / 0 blocks |

`research_state/evaluation_summary_FCLR-011.md` is a real gate PASS. No artifact invalidates it. `H1_primary.last_experiment` was stale at FCLR-014, which predates FCLR-011. The old handoff therefore hid the single most important result in the repository. The prior "exhausted" claim was a **process failure**, not an evidence conclusion.

### What this session actually executed

A new frozen prereg, `research_state/prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.{json,md}`, and a complete heavy pipeline, `scripts/fclr_fwd_vol_confirm.py`, ran end-to-end on cached Binance mark/premium/index/funding data (no network):

- **Rolling-origin walk-forward**, 3 × 30-day blocks, 7-day embargo, 5 instruments, 2000-replicate day-block bootstrap, Holm across 12 cells, LOIO, 200-permutation funding placebo, exclude-inspected-days sensitivity, and an exact-convention FCLR-011 reproduction cell.
- **Forward result:** pooled C2 vs B1 mean diff **+0.02676** (positive = C2 worse), 95% CI **[0.000343, 0.064822]** favouring B1, relative reduction **-5.55%**, n=10,200, 85 days. **5/5 LOIO subsets negative** (3/5 CI excludes zero). Placebo not significant. Sensitivity excluding inspected days: **-7.82%**.
- **Reproduction result:** **4.39%** vs the sealed **4.94%** — delta **0.552pp**, just outside the pre-registered ±0.5pp tolerance. The frozen verdict rule therefore returns **INCONCLUSIVE**, not NOT_REPLICATED.

Artifacts:
- `research_state/evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.{md,json}`
- `research_state/tracka_fwd_vol_panel_20261113T041934Z.parquet`
- `research_state/tracka_fwd_vol_build_report_20261113T041934Z.json`
- `research_state/coverage_audit_binance_fwd_vol_20261113T041200Z.{json,md}`

**Scientific reading:** the FCLR-011 PASS does **not** generalize to the next three months; on fresh data C2 is significantly *worse* than the RV-only baseline. But the pipeline does not yet reproduce the sealed PASS within tolerance, so the honest aggregate is INCONCLUSIVE pending exact panel reconstruction. Do not promote, and do not re-label FCLR-011 as NOT_SUPPORTED.

---

## NEXT SESSION: MANDATORY HEAVY WORK (no status-only sessions)

### Step 1 — Close the reproduction gap (blocking)

```bash
cd <repo>
# 1a. Try to materialize the sealed panel (may be offline)
git lfs pull --include research_state/data_cache/fclr011_panel.json || true
ls -l research_state/data_cache/fclr011_panel.json || echo "LFS_PANEL_UNAVAILABLE"

# 1b. Re-run the heavy pipeline (writes a new timestamped artifact set)
python3 scripts/fclr_fwd_vol_confirm.py

# 1c. The FCLR-011 reproduction cell must report pass=true (delta <= 0.5pp)
python3 - <<'PY'
import json, glob
f = sorted(glob.glob('research_state/evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-*.json'))[-1]
d = json.load(open(f))
print(f, d['verdict'], d['repro_011'])
PY
```

If `LFS_PANEL_UNAVAILABLE`, reconstruct the exact legacy panel from the same cache using the feature code in `scripts/run_evaluation.py` (`load_mark_series`, `build_features_for_origin`, `fit_ols`, `predict`, `qlike`, `block_bootstrap_diff`). The residual 0.55pp is small; the likely cause is RV/EMA computed on valid mark rows vs the hourly grid. Do not widen the frozen tolerance; fix the pipeline or add a new prereg version with a documented reason.

### Step 2 — Issue the final forward verdict

- If the pooled C2-vs-B1 CI remains in favour of B1 (`ci_lo > 0`) and materiality `< 2%`: record **`NOT_REPLICATED`**.
- If the pooled CI excludes zero in favour of C2 (`ci_hi < 0`), materiality `>= 2%`, and all 8 checks pass: record **`CONFIRMED`**.
- Update `research_state/hypothesis_registry.json` (`H_fclr_fwd_vol_011_confirm`, `H1_primary`) and `research_state/experiment_frontier.json` with the final verdict and artifact hashes.

### Step 3 — Pass the definition-of-done gate

```bash
python3 scripts/fclr_heavy_confirm_gate.py
# must print: GATE: PASS
```

The gate currently prints `GATE: FAIL` because the verdict is INCONCLUSIVE. That is intentional: **the campaign cannot be closed without a final verdict.**

### Step 4 — Secondary mandatory heavy work (after Step 3)

Do not stop at the primary gate. The repo name includes liquidation risk; the following are the next heavy, pre-registerable cells. Each requires a frozen prereg before outcomes and a timestamped evaluation artifact.

1. **`FCLR-LIQ-010-CONFIRM`** — independent recomputation + LOIO/placebo/leakage audit of the FCLR-010 observed-liquidation PASS (Brier -2.21%, 95% CI [-0.004892, -0.001263], 199 instruments, 5 blocks, Hyperliquid ironflow). Freeze prereg → recompute from cached panel → verdict `CONFIRMED / FRAGILE / NOT_REPLICATED`.
2. **`FCLR-EXP-ROBUST-REDO`** — pre-register a new expansion-robustness design meeting LOIO ≥ 6/8 and placebo PASS, then execute on the sealed expansion panel. The prior sealed 19.04% PASS is FRAGILE (LOIO 4/8, placebo 21.10% ≥ 19.04%); do not re-score it.
3. **`FCLR-FWD-VOL-2025-CROSS`** — pre-register a 2025-02..2025-05 walk-forward (3 blocks) to test whether FCLR-011's PASS is period-specific. Use only the cached Binance panel; freeze before outcomes.

---

## ACCEPTANCE GATE (session completion)

1. `python3 scripts/fclr_heavy_confirm_gate.py` → `GATE: PASS`.
2. The latest `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-*.json` has a final verdict (`CONFIRMED` or `NOT_REPLICATED`) and all 8 checks.
3. `research_state/hypothesis_registry.json` and `research_state/experiment_frontier.json` agree with the verdict.
4. `python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate` → all OK.
5. No sealed artifact is mutated; no raw cache is committed; no workflow files are patched.

### Known pre-existing test debt (do not attribute to this campaign)

`python -m unittest discover -s tests` reports 1172 tests with 74 failures + 1 error. These are **pre-existing** and dominated by Track A hardening/drift/registry guards, not by the new campaign:

- `test_registry_covers_all_scripts` / `test_real_repo_passes`: 12 pre-existing scripts were already unregistered (`early4h_campaign.py`, `early4h_liq_glm*.py`, `fclr_campaign_gate.py`, `fclr_final_structural_closure.py`, `fclr_build_tracka_*`, `fclr_ironflow_bulk.py`, `tracka_hl_*`). This session registered its two new scripts; the remaining 12 are pre-existing.
- `test_root_md_json_count_bounded`: root md+json count 352 > 260 (pre-existing artifact accumulation).
- Track A drift preflight (`DRIFT_PREFLIGHT_FAIL_BEFORE_PREREG`) and the recurring-timestamped-family guards were already red before this session.

The **targeted campaign suite is green**: `tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate tests.test_run_evaluation_experiment_contract` → 125 tests OK. Do not spend this session on unrelated Track A test debt; the heavy campaign is the priority.

---

## HARD BANS (enforced)

- **No status-only sessions.** Re-running the old monitor checks without executing Step 1–4 is not progress.
- **No "monitor-only / no heavy work authorized" closure.** That state is revoked; it contradicted RESEARCH_PROMPT §16, §19, §20.
- No threshold shopping, post-hoc feature/model/universe changes, or reuse of an inspected window as fresh confirmation without the disclosed sensitivity.
- No zero-fill/forward-fill to force comparability (the legacy reproduction uses zero-fill only for non-core features, and this is documented).
- No mutation of sealed FCLR-011/012-V/013/014 artifacts; no re-labelling a PASS as NOT_SUPPORTED.
- No agent-set Gate 4 `RESOLVED_VERIFIED`; no paid/manual/credentialed data; no `.github/workflows/*` patches.

---

## BOTTLENECKS REMOVED THIS SESSION

| Bottleneck | Resolution |
|---|---|
| False "all volatility NOT_MET" summary | Corrected: FCLR-011 PASS restored; `H1_primary` set INCONCLUSIVE with reconciliation; new campaign rank-0. |
| "No heavy work authorized" deadlock | Revoked; replaced with a mandatory heavy campaign and a fail-closed completion gate. |
| `run_manifest.json` is an unresolved Git-LFS pointer (130 bytes) → every `run_evaluation.py` call crashed | Added `scripts/run_evaluation.py::load_manifest()` + committed `research_state/run_manifest_local.json` offline fallback with verbatim split boundaries. |
| No enforcement that the campaign is executed | Added `scripts/fclr_heavy_confirm_gate.py` and `tests/test_fclr_heavy_confirm_gate.py`; gate fails until a final verdict exists. |
| Frontier/registry drift | Frontier rank-0 is now `FCLR-HEAVY-CONFIRM-20261113T041200Z` / `ACTIVE_HEAVY_CAMPAIGN`; prior FULLHIST entry demoted to rank 1; registry reconciled. |
| Underpowered 5–76 day test windows | New design uses 3 × 30-day blocks with 5 instruments and a 2000-replicate bootstrap. |

---

## EXACT START COMMANDS

```bash
cd <repo>

# Preflight
python3 -c "import numpy,pandas,scipy,pyarrow; print('deps OK')"

# Gate 4 external trigger (expected absent; do not poll)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# Current campaign state
python3 scripts/fclr_heavy_confirm_gate.py || true

# Run the heavy pipeline (about 30-40s; writes new timestamped artifacts)
python3 scripts/fclr_fwd_vol_confirm.py

# Final acceptance
python3 scripts/fclr_heavy_confirm_gate.py
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate
```

---

## DEFINITION OF DONE (answer in the handoff)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## KEY REFERENCES

- `research_state/prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.{json,md}` — frozen prereg (3 × 30-day blocks, gates, verdict rules).
- `research_state/coverage_audit_binance_fwd_vol_20261113T041200Z.{json,md}` — coverage-only audit (5 symbols, 2024-01-01..2026-11-08).
- `scripts/fclr_fwd_vol_confirm.py` — heavy pipeline (walk-forward, bootstrap, Holm, LOIO, placebo, sensitivity, repro).
- `scripts/fclr_heavy_confirm_gate.py` — definition-of-done gate.
- `tests/test_fclr_heavy_confirm_gate.py` — gate enforcement tests.
- `research_state/evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.{md,json}` — current forward result.
- `research_state/evaluation_summary_FCLR-011.md` — the sealed PASS that was suppressed.
- `research_state/evaluation_summary_FCLR-012-V.md` — +15.19% signal, 0 blocks.
- `research_state/run_manifest_local.json` — offline split fallback.
- `RESEARCH_PROMPT.md` §16, §17, §18, §19, §20.

---

## SESSION LOG (append-only; newest first)

## 2026-11-13T04:20:00Z — Kilo session: Rebuilt the durable handoff as a mandatory heavy campaign; reconciled the suppressed FCLR-011 PASS; executed a new frozen forward walk-forward; gate fails closed on INCONCLUSIVE pending exact reproduction.

- **What changed:** Replaced the "all NOT_MET / no heavy work / monitor-only" handoff with `FCLR-HEAVY-CONFIRM-20261113T041200Z`. Froze `prereg_fclr_fwd_vol_011_confirm_20261113T041200Z`; built `scripts/fclr_fwd_vol_confirm.py`; added `scripts/fclr_heavy_confirm_gate.py` + `tests/test_fclr_heavy_confirm_gate.py`; added `research_state/run_manifest_local.json` and an LFS-tolerant `load_manifest()` in `scripts/run_evaluation.py`; set frontier rank-0 to `ACTIVE_HEAVY_CAMPAIGN`; corrected `H1_primary` from stale `NOT_SUPPORTED` to `INCONCLUSIVE` with a reconciliation record; added `H_fclr_fwd_vol_011_confirm`.
- **Evidence supported:** FCLR-011 is a genuine gate PASS (4.94%, CI excludes zero, 3 blocks). Prior volatility NOT_MET verdicts were largely block-count failures (5–76 day test windows). The new forward walk-forward finds C2 significantly worse than B1 (pooled +0.02676, 95% CI [0.000343, 0.064822], rel -5.55%, 5/5 LOIO negative).
- **Evidence contradicted:** The claim that "all claim-worthy local admissible experiments are exhausted." The Binance cache (5 symbols, 2024-01-01..2026-11-08) and the unrefuted FCLR-011 PASS remain.
- **Unknown / dominant limitation:** Exact reproduction of the sealed FCLR-011 panel. The pipeline lands at 4.39% vs 4.94% (delta 0.552pp), just outside the pre-registered ±0.5pp tolerance, because `research_state/data_cache/fclr011_panel.json` is an unresolved Git-LFS pointer and the legacy feature code differs slightly on RV/EMA missing-row handling.
- **Strongest alternative explanation:** The FCLR-011 PASS is period-specific (2026-05..2026-08) and does not generalize; the forward C2 degradation is genuine, not a pipeline artifact.
- **Highest expected information gain:** Close the reproduction gap (materialize the sealed panel or exactly replicate the legacy features), then issue the final forward verdict; afterwards run `FCLR-LIQ-010-CONFIRM`, `FCLR-EXP-ROBUST-REDO`, and `FCLR-FWD-VOL-2025-CROSS`.
- **Artifacts/commands:** `python3 scripts/fclr_fwd_vol_confirm.py` → `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.{md,json}`, panel, build report. `python3 scripts/fclr_heavy_confirm_gate.py` → `GATE: FAIL` (INCONCLUSIVE, by design). `python -m unittest tests.test_active_campaign_gate tests.test_fclr_heavy_confirm_gate` → OK.

<!-- Prior monitor-only entries (2026-11-13T02:44Z..03:23Z) are retained in git history; they are superseded by this entry. -->