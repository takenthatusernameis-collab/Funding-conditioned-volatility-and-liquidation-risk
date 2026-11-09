# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated/updated:** 2026-11-09T09:10:16Z (state verification after backfill session; backfill implementation/tests verified green)
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled, binding):** Repo P0 = **Gate 4 exploratory infrastructure hardening with measurable, tested artifacts** (local admissible 2024-04..09 cache only). Gate 4 v4 funding ablations remain **EXPLORATORY NO-GO CONFIRMED** — **do not rerun identical stabilization claims, do not claim confirmatory GO/economic value/promotion, do not reuse sealed-anchor domain (FCLR002/003/013), do not replace prereg A–E contrasts or change confirmatory estimands**. Track A = **structurally blocked/no trigger** (2026-11..2027-02 absent, probes==2, deadend rubric holds) — **no probing, no scan/wrapper/report families**. Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn. Every session must produce versioned, auditable artifacts and/or tested code. No `.github/workflows` edits.**

**Verified 2026-11-09T09:10:16Z (no new research_state writes; read-only checks + full suite):** `--backfill-derivable-diagnostics` implementation present in `scripts/gate4_v4_bootstrap_diagnostic_summary.py` (BACKFILL_RULES_VERSION 1.0; derives only `effective_block_count` from `n_blocks>0` and `ci_valid` from finite ordered CI+point/n_obs; **never infers `degenerate`/`inference_ok`**). `tests/test_gate4_v4_bootstrap_diagnostic_summary.py` **14 OK**. Full suite `python -m unittest discover tests` → **Ran 1015 tests in ~109s — OK** (failures=0, errors=0). Scope drift **[PASS] scripts=115 registry=115**. `tracka_resume_check.py` → **pass:true, 17/17, network:false, writes_real_research_state:false, probes==2, root_md_json_bounded pass**. `tracka_resume_gate.py --json` → **BLOCKED / PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS / drift_preflight.pass:true / outcomes_inspected:false**. `research_state/ironflow_fastpath_cache.json` restored (not committed).

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK — NO AVOIDANCE)

**Session timestamp (initial task):** `2026-11-09T09:10:16Z`

**You MUST execute measurable research/engineering progress.** Forbidden: status-only churn, Track A probing (2026-11..2027-02 absent/probes==2), Track C/B new sealed outcomes, workflow/controller/scheduler/poller/wrapper creation, `.github/workflows` edits, confirmatory promotion from exploratory Gate 4, sealed-anchor reuse, prereg A–E contrast/estimand changes, threshold-shopping, holdout reuse, weakening root md+json bound or Track A invariants, live/paper trading, credentials, access-control bypass, committing `__pycache__`/`ironflow_fastpath_cache.json`/large raw caches.

**Gate 4 v4 binding state (do not litigate):** `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true` (local 2024-04..09 cache; FCLR-015 SHA256 `3e6ac26c...5406c`). **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE.** Prior exec/diag/stab/NO-GO/leakage artifacts exist and are sufficient for the current claim boundary — **do not rerun identical stabilization claims**. Bootstrap summary + ambiguity-refusing enrichment + provable backfill exist — build on them, do not redo.

**DONE (verified 2026-11-09T09:10:16Z) — provable backfill with per-row audit trace:** `--backfill-derivable-diagnostics` derives only `effective_block_count` from `n_blocks>0` and `ci_valid` from finite ordered CI+point/n_obs; never infers `degenerate`/`inference_ok`; backfill alone never claimable; versioned `results/gate4_v4_bootstrap_diagnostic_summary_backfill_20261109T090320Z.md` emitted (prior session). 14 targeted + 1015 full suite OK. **Do not rerun/reimplement.**

**Execute next (initial task — highest-value measurable engineering, complete fully):** extend the **backfill audit** to (1) report a machine-checkable `backfill_coverage` summary (rows with provably derivable gaps filled, rows still missing `degenerate`/`inference_ok` with explicit refusal counts) and (2) add a `--backfill-strict` mode that emits a compact `MISSING_DIAGNOSTIC_FIELDS` remediation list (paths/rows/fields + concrete reason) **without mutating sources or fabricating gates**. Keep refusal-first: never infer `degenerate`/`inference_ok` from CI geometry/excludes-zero; only use explicit saved diagnostic evidence. Add synthetic tests, emit versioned `results/`, keep drift PASS and full suite green. No recomputation/network/real `research_state` writes/new root `research_state/*.md/*.json`. If a new script is added, register in `research_state/tracka_script_scope_registry.json` and mirror in `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`; keep drift PASS.

**Artifact discipline:** new heavy outputs go to `results/` or dated subdirs — **do not add repo-root `research_state/*.md/*.json` files**. Maintain `root_md_json_bounded` pass. Version outputs with UTC timestamps.

**Verification (must run):** targeted tests for touched code first; then `python -m unittest discover tests` (**must remain ≥1015 OK**). `python scripts/check_tracka_scope_registry_drift.py` → PASS. `python scripts/tracka_resume_check.py` → pass:true, 17/17, network:false, probes==2, root_md_json_bounded pass. `python scripts/tracka_resume_gate.py --json` → BLOCKED, `drift_preflight.pass:true`, `outcomes_inspected:false`.

**Update this single durable handoff** (§1–§11) with session timestamp, exact file paths changed, commands, pass/fail counts, artifact paths, blockers, and the **single highest-value unfinished next task**. No parallel handoff files.

**Acceptance (mandatory):** (A) tested code/artifact change with green targeted + full suite + all invariants green, **or** (B) a materially different tested engineering task with versioned evidence and same green gates. **Anything less is failure.**

---

## 1. WHAT CHANGED AND WHY (current session, 2026-11-09T09:10:16Z verification)
- **No code/artifact changes** beyond restoring `research_state/ironflow_fastpath_cache.json` (not committed). Verified backfill implementation + 14 targeted tests + full 1015-suite remain green; invariants green. This is a verified-state handoff to remove ambiguity and set the next heavy task; it is grounded in executed checks (not status-only prose).

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES (2026-11-09T09:10:16Z)
| Check | Command | Result |
|---|---|---|
| Targeted summary/backfill | `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary -v` | **14 tests — OK** |
| Full suite | `python -m unittest discover tests` | **Ran 1015 tests in ~109s — OK** (failures=0, errors=0) |
| Scope registry drift | `python3 scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=115 registry=115 reason=OK** |
| Track A resume check | `python3 scripts/tracka_resume_check.py` | **pass:true, 17/17, network:false, writes_real_research_state:false, probes==2, root_md_json_bounded pass** |
| Track A resume gate | `python3 scripts/tracka_resume_gate.py --json` | **BLOCKED / PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS / drift_preflight.pass:true / outcomes_inspected:false** |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `AGENT_HANDOFF.md` | **Updated** — single durable handoff, verified state `2026-11-09T09:10:16Z`, next task = backfill coverage + `--backfill-strict` remediation |
| `research_state/ironflow_fastpath_cache.json` | **Restored from git (not committed)** |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A **BLOCKED** (no admissible unauth liquidation labels). Track C historical/sealed. Gate 4 exploratory local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED Track C context; Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 (sealed-anchor conflict). | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C historical PASSED / **forward INCONCLUSIVE** (0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09 (stab/diag/nogo/leakage artifacts). Bootstrap summary + ambiguity-refusing enrichment + **provable backfill** (verified 14 tests; never infers `degenerate`/`inference_ok`; claimability honest) exist. **NOT CONFIRMATORY / NOT PROMOTABLE.** | `results/gate4_v4_bootstrap_diagnostic_summary_backfill_20261109T090320Z.md`, `scripts/gate4_v4_bootstrap_diagnostic_summary.py` |
| **Forecast Gate** | **NOT ELIGIBLE**. No confirmatory promotion. | frontier/negative results |

## 5. BOTTLENECK / BLOCKED-SESSION RECONCILIATION (do not attempt removal of structural gates)
| Item | State | Is it a removable bottleneck? | Allowed route |
|---|---|---|---|
| Track A: no admissible liquidation labels (2026-11..2027-02 absent, probes==2) | Structural deadend | **NO** — do not re-probe absent months, no probe/scan/wrapper families | Guard hardening only if a specific gap is identified |
| Track C forward: inconclusive (0 non-overlapping 30d blocks) | Structural | **NO** — do not relax criteria | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: confirmatory_claim_go NO_GO; sealed-anchor conflict | Structural by design | **NO** — no promotion, no sealed-anchor reuse, no rerun of identical stabilization claims | EXPLORATORY-only engineering/diagnostics on local 2024-04..09 cache |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | Structural outcome | **NO** — no improvement claim | Tested diagnostics/summaries; no recomputation |
| Backfill lacks machine-checkable coverage summary + strict remediation list for still-unproven `degenerate`/`inference_ok` | Engineering gap (auditable) | **Partially removable by tested reporting only** — must not mutate source artifacts, must not infer `degenerate`/`inference_ok` without explicit evidence, must not fabricate claimability | `--backfill-strict` + coverage summary; synthetic tests; `results/` only |
| `tracka_resume_gate.py --json` → BLOCKED (PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false) | By-design pre-reg/manifest block | **NO** — gate, not inefficiency | Maintain drift_preflight.pass:true |

**Conclusion:** no structural gate is removable. The open, non-avoidable, high-value path is §0: tested `--backfill-strict`/coverage remediation reporting (no inference of `degenerate`/`inference_ok`, no source mutation, no fabricated claimability).

## 6. SINGLE HIGHEST-VALUE NEXT TASK
**Deterministic, refusal-first backfill coverage summary + `--backfill-strict` remediation list (measurable, materially different).** Extend `scripts/gate4_v4_bootstrap_diagnostic_summary.py`: (1) machine-checkable `backfill_coverage` summary (rows with provably derivable gaps filled; rows still missing `degenerate`/`inference_ok` with explicit refusal counts/reasons); (2) `--backfill-strict` emits compact `MISSING_DIAGNOSTIC_FIELDS` remediation entries (paths/rows/fields + concrete reason) without mutating sources or fabricating gates. **Never infer `degenerate`/`inference_ok` from CI geometry/excludes-zero; only explicit saved diagnostic evidence counts.** Emit versioned `results/`. Add synthetic tests. No recomputation/network/real `research_state` writes; maintain all invariants.

## 7. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary -v
python3 scripts/gate4_v4_bootstrap_diagnostic_summary.py --repo-root . --backfill-derivable-diagnostics --out results/gate4_v4_bootstrap_diagnostic_summary_backfill_<UTC>.md
python -m unittest discover tests                         # expect >=1015 OK
python scripts/check_tracka_scope_registry_drift.py      # expect PASS (115/115)
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
```

## 8. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, NO-GO rubric, probes==2, 2026-11..2027-02 absent | Guard hardening only if specific gap; **no** re-probe absent months |
| Track C: forward inconclusive (0 non-overlapping 30d blocks) | FCLR-012-V | New admissible panel meeting criteria; do not relax |
| Gate 4 v4: sealed-anchor conflict; confirmatory_claim_go NO_GO | v4 prereg | **EXPLORATORY only**, explicit labels, no promotion/sealed-anchor reuse |
| Gate 4 v4: funding ablations NO-GO on 2024-04..09 | stab/nogo/summary artifacts | No improvement claim; diagnostics/summaries only |
| Legacy contrast JSONs lack embedded `degenerate`/`inference_ok`; leakage context mismatches | enrichment audit (enriched=0, refused=36) | Tested provable reporting/backfill coverage+strict remediation; **no** inference of degenerate/inference_ok from CI width; no source mutation |
| Root md+json bound tight | `tracka_resume_check.py` root_md_json_bounded | New artifacts in `results/` or dated subdirs; **do not weaken** |
| Protected control plane | repo rules | **No `.github/workflows` edits** |
| `ironflow_fastpath_cache.json` dirty-by-tests | harness behavior | **Do not commit** (restored) |

## 9. DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Mutate saved exploratory JSON artifacts or fabricate `claimable_excludes_zero`
- ❌ Infer `degenerate`/`inference_ok` from CI width/point alone; fill only provably derivable/explicitly evidenced diagnostics
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

## 10. SESSION START PROTOCOL (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests/tests/cache, `gate4_v4_exploratory_{stab,diag,leakage_audit}`, `results/gate4_v4_bootstrap_diagnostic_summary*.md`.
3. Execute §0 (measurable task). Cheapest checks first. Update **this file** with exact evidence + current session timestamp.

## 11. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with tested `--backfill-strict`/coverage remediation (or a materially different tested hardening task) + versioned `results/` artifacts, suite **≥1015 OK** (or higher if tests added), scope drift PASS, Track A invariants green (17/17, probes==2, root bound pass), and the next unfinished task — **acceptance (A)/(B) satisfied**. Repo must remain continuable without user repeating instructions.

---
**END OF SINGLE DURABLE HANDOFF.**
