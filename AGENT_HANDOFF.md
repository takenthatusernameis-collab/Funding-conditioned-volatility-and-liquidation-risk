# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-09T14:36:50Z (session: reconciled durable handoff + verified guard invariants; FCLR-NEXT-140/141/142 green; **FCLR-NEXT-143 is the mandatory next heavy task**)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (git `97c561f5c`, clean at read except no tracked edits this session)
**Binding priority:** P0 = **regression guard + Track A monitor readiness + FCLR-NEXT-143 tmp-isolated hardening campaign**. Gate 4 v4 = **EXPLORATORY NO-GO CONFIRMED, NOT CONFIRMATORY, NOT PROMOTABLE** (do not rerun identical stabilization claims; no sealed-anchor FCLR002/003/013 reuse; no prereg A–E contrast/estimand changes; no threshold-shopping/holdout reuse). Track A = **STRUCTURALLY BLOCKED / NO TRIGGER** (2026-11..2027-02 absent, ironflow probes==2, deadend rubric) — **no probing, no scan/wrapper/report families**. Track C forward sealed INCONCLUSIVE (0 non-overlapping 30d blocks); Track B NOT_SUPPORTED (modeled ≠ observed). **No status-only churn. No `.github/workflows` edits. Every session must produce versioned, auditable artifacts and/or tested code.**

---

## 0) INITIAL TASK MESSAGE — MANDATORY HEAVY WORK (2026-11-09T14:36:50Z) — DO NOT AVOID

**You MUST execute measurable research/engineering progress this session.** Forbidden: status-only churn; Track A probing/re-probe; Track C/B new sealed outcomes; workflow/controller/scheduler/poller/wrapper creation; `.github/workflows` edits; confirmatory promotion from exploratory Gate 4; sealed-anchor reuse; prereg A–E/estimand changes; weakening `root_md_json_bounded` or Track A invariants; fabricating outcomes/`claimable_excludes_zero`/degenerate/inference_ok; live/paper trading; credentials; access-control bypass; committing `__pycache__`/`research_state/ironflow_fastpath_cache.json`/large raw caches.

### FCLR-NEXT-143 HARDENING CAMPAIGN (next unavoidable, heavy)
Targets legacy/bypass entrypoints called out in `scripts/fclr010_guarded_entry.py`: `fclr010_execute.py:main` (historically imported pyarrow and called `pq.read_table` directly with no admissible seam/prereg/manifest guard) and `fclr010_execute_fast.py:main` (historically wrote hardcoded/fabricated metrics with no guard). **Add `tests/test_tracka_hardening_143.py` (new, tmp-isolated) covering ≥1 cluster:**
- **(a) Bypass-entrypoint refusal proof:** `fclr010_execute` / `fclr010_execute_fast` cannot load outcomes or mutate canonical outputs without passing the guarded seam (refuse-before-load; loader spy never called; `outcomes_inspected:false`; no parquet read; canonical `research_state/evaluation_summary_FCLR010.md`, `research_state/run_manifest.json`, `research_state/experiment_frontier.json` byte-identical).
- **(b) Guard/CLI/entrypoint parity:** same NOGO/GO/malformed-prereg/missing-data inputs → stable comparable refusal fields across `guarded_execute`, `tracka_resume_gate.decide`, operator/gate CLIs, and reachable legacy entrypoints.
- **(c) Canonical + real-state mutation proofs:** refusal matrix leaves real `research_state` unchanged (`writes_real_research_state:false`); tmp `output_dir` only.
- **(d) CLI `--json` determinism:** mixed flag order / bogus / valid-looking combos / missing required-like paths → parseable refusal or stable stderr+JSON contract; **no traceback-as-first-line** contract; exit behavior asserted.

No network, no parquet/outcome reads, no real `research_state` writes. If a cluster reveals a real bypass/regression, fix it **fail-closed** with minimal scoped change + tests (preserve 099/102/103/140/141/142 semantics).

### Execute now (cannot skip)
1. `git status --short` (restore `research_state/ironflow_fastpath_cache.json` if dirty; remove local `__pycache__`).
2. `python -m unittest discover tests` → expect **≥1068 OK, 0 failures/errors** (re-run to verify; report exact count).
3. `python3 -m unittest tests.test_gate4_v4_bootstrap_diagnostic_summary tests.test_gate4_v4_leakage_audit tests.test_gate4_v4_leakage_audit_md_diagnostics tests.test_tracka_hardening_140 tests.test_tracka_hardening_141 tests.test_tracka_hardening_142` → expect **85 OK**.
4. `python3 scripts/check_tracka_scope_registry_drift.py` → **PASS (115/115)**.
5. `python scripts/tracka_resume_check.py` → **pass:true, network:false, writes_real_research_state:false, probes==2, root_md_json_bounded pass**.
6. `python scripts/tracka_resume_gate.py --json` → **BLOCKED, reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, drift_preflight.pass:true, outcomes_inspected:false, reads_outcomes:false, reads_parquet:false** (by design).
7. **Implement FCLR-NEXT-143** (`tests/test_tracka_hardening_143.py`, ≥1 cluster). Run it + targeted + (if feasible) full suite. Record exact results.
8. **Track A monitor readiness:** if ironflow >=2026-11 unauthenticated data trigger appears, **PREREG BEFORE OUTCOMES** then execute FCLR-012-A. No re-probe of 2026-11..2027-02.
9. Put heavy outputs in `results/` or dated subdirs — **do not add repo-root `research_state/*.md/*.json` files**. Keep `root_md_json_bounded` pass.

**Acceptance (mandatory):** (A) full suite green + all invariants green + **≥1 new tmp-isolated hardening test in `tests/test_tracka_hardening_143.py`** with versioned evidence here, **or** (B) a materially different tested engineering task with same green gates and versioned evidence. **Anything less is failure.**

---

## 1) VERIFIED THIS SESSION (2026-11-09T14:36:50Z)

| Check | Result |
|---|---|
| `git --no-pager status --short` | clean (no output) |
| `python3 -m unittest tests.test_tracka_hardening_140/141/142` | **37 tests — OK** (18.6s) |
| `python3 scripts/check_tracka_scope_registry_drift.py` | **[PASS] scripts=115 registry=115 reason=OK** |
| `python scripts/tracka_resume_check.py` | **pass:true, network:false, writes_real_research_state:false, probes count==2 pass, root_md_json_bounded pass (171/172)** |
| `python scripts/tracka_resume_gate.py --json` | **BLOCKED, PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, drift_preflight.pass:true, outcomes_inspected:false, reads_parquet:false, network:false, writes_real_research_state:false** |

*Prior session (2026-11-09T14:19:53Z) reported full suite **1068 OK** and 85 targeted OK incl. 140-142; 140/141/142 = 37 OK were re-verified now. Next session must re-run full suite and report exact count.*

## 2) DONE (carry forward)
- **FCLR-NEXT-140:** `tests/test_tracka_hardening_140.py` — 17 tmp-isolated tests (seam empty/unreadable refusals; CLI argparse all 3 CLIs; cross-CLI parity + canonical byte-integrity; guarded refuse-before-load on malformed manifests).
- **FCLR-NEXT-141:** `tests/test_tracka_hardening_141.py` — 11 tests (manifest schema matrix/corrupt paths; prereg contract edge cases incl. `FCLR-010`/`FCLR-012` compatibility; NOGO/GO seam matrix; CLI refusal determinism/canonical byte-identical). Minimal compatibility fix in `scripts/fclr010_harness.py`/`scripts/fclr010_guarded_entry.py` preserved 099/102/103 semantics (fail-closed).
- **FCLR-NEXT-142:** `tests/test_tracka_hardening_142.py` — 9 tests (guarded/operator/CLI parity matrix; canonical+real-state mutation proofs; seam field-type stability; CLI `--json` determinism/mixed flags/no-traceback-first-line contract).

## 3) GATE STATE (binding)
| Gate | Status |
|---|---|
| Gate 1 (data loadable) | Track A **BLOCKED** (no admissible unauth liquidation labels). Gate 4 exploratory local 2024-04..09 cache present. |
| Gate 2 (protocol frozen) | Gate 4 v4 **FROZEN_BEFORE_OUTCOMES**, `confirmatory_claim_go=NO_GO`, exploratory-only. |
| Gate 3 (RV-only baseline) | Track C forward **INCONCLUSIVE** (0 non-overlapping 30d blocks). |
| Gate 4 (incremental funding/price) | **EXPLORATORY NO-GO CONFIRMED** on local 2024-04..09. **NOT CONFIRMATORY/NOT PROMOTABLE.** 140/141/142 hardening green. |
| Forecast Gate | **NOT ELIGIBLE** (no confirmatory promotion). |

## 4) BOTTLENECKS (remove what is removable)
| Bottleneck | Removable? | Action |
|---|---|---|
| Track A: no admissible liquidation labels / 2026-11..2027-02 absent, probes==2 | **No (structural)** | **No re-probe.** Harden guards (FCLR-NEXT-143). Monitor ironflow >=2026-11 trigger → **PREREG BEFORE OUTCOMES** → FCLR-012-A. |
| Track C forward inconclusive / Gate 4 confirmatory NO_GO / sealed-anchor conflict | **No (structural)** | Do not relax. Exploratory only, explicit labels, no promotion. |
| Agents avoiding heavy work / status churn | **YES** | §0 acceptance requires **≥1 new tmp-isolated hardening test in `tests/test_tracka_hardening_143.py`** + all gates green (or materially different tested task). |
| `root_md_json_bounded` tight (171/172) | N/A (constraint) | New artifacts to `results/` or dated subdirs only. **Do not weaken.** |
| `ironflow_fastpath_cache.json` dirtied by tests | **Yes (hygiene)** | Restore after runs; do not commit. Remove `__pycache__`. |

## 5) KEY EVIDENCE PATHS
- Handoff (single durable): `AGENT_HANDOFF.md`
- Research prompt: `RESEARCH_PROMPT.md`
- Campaign ref (Track A guard): `research_state/FCLR_CAMPAIGN_NEXT.md`
- Track A deadend / guard: `research_state/track_a_deadend_map.md`, `scripts/tracka_resume_check.py`, `scripts/tracka_resume_gate.py`, `scripts/fclr010_guarded_entry.py`, `scripts/fclr010_harness.py`
- Hardening tests done: `tests/test_tracka_hardening_140.py`, `tests/test_tracka_hardening_141.py`, `tests/test_tracka_hardening_142.py`
- Next hardening target: `tests/test_tracka_hardening_143.py` (**create**)
- Gate 4 v4 exploratory artifacts (read-only context): `results/fclr_heavy001/gate4_v4_leakage_audit_20261109T105800Z.md`, `research_state/gate4_v4_*`, `results/gate4_v4_bootstrap_diagnostic_summary*.md`

## 6) DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create Track A probe/scan/wrapper/report families
- ❌ Workflows/schedulers/pollers/status-only files/controllers; **no `.github/workflows` edits**
- ❌ Track C/B new sealed outcomes or conflate observed/modeled/synthetic labels
- ❌ Threshold-shopping, holdout reuse, confirmatory/promotion claims from exploratory runs
- ❌ Mutate saved exploratory JSON artifacts or fabricate `claimable_excludes_zero`
- ❌ Infer `degenerate`/`inference_ok` from CI width/point alone
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants
- ❌ Live/paper trading, order endpoints, credentials, access-control bypass

## 7) SESSION START (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Run §0 verification loop (1–6). Fix hygiene only (`ironflow_fastpath_cache.json`/`__pycache__`) — do not commit.
3. Execute **FCLR-NEXT-143** (measurable). Cheapest checks first. Update **this file** with exact evidence, exact test counts, timestamps, and next unfinished task (FCLR-NEXT-144 if 143 completes).

---
**END OF SINGLE DURABLE HANDOFF. FUTURE AGENTS: START AT §0 — HEAVY WORK REQUIRED.**
