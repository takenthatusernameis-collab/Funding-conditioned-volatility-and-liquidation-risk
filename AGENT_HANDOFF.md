# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated:** 2026-11-09T00:33:47Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled):** Repo P0 = Phase 3 Gate 4 funding-conditioned volatility ablations using local data (measurable, unblocked). Track A = structurally blocked / no trigger (lockdown hardening only if specific gap); Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn.**
**Verified this session:** git clean (f59b4ad3a); `python -m unittest discover tests` → Ran 950 tests OK; `tracka_resume_check.py` → pass:true, 17/17, probes==2, network:false, writes_real_research_state:false; `tracka_resume_gate.py --json` → drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false; `tracka_operator_report.py` → pass:true. Local 2024-04..09 cache present; v4 prereg FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO, exploratory_smoke_authorized_after_freeze=true.

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK)

**You MUST execute measurable research/engineering progress in this session. Do not probe absent Track A months (2026-11..2027-02). Do not add workflows/schedulers/pollers/wrappers/controllers. Do not touch `.github/workflows`.**

### Campaign: Gate 4 v4 EXPLORATORY funding-conditioned volatility ablation (local 2024-04..09 cache) — produce versioned, auditable artifacts

**Intent (per frozen prereg):** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` is `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`. **All outputs MUST be labeled EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE** (sealed-anchor conflict with FCLR002/003/013 domain family). Never claim confirmatory GO or economic value.

**Preconditions verified (this session):** local cache exists under `research_state/data_cache/` (BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT months present including 2024_04..2024_09). FCLR-015 manifest present: `research_state/fclr015_local_audit/fclr015_input_manifest_2024_04_09_20261107T180626Z.json`. Regression baseline **950 tests OK** (after fclr024 fix).

**Execute (adapt paths/suffix to avoid overwriting canonical exploratory outputs; use a new timestamped suffix, e.g. `_v4_exploratory_exec_20261109T####Z`):**
1. **Read** the v4 prereg JSON+MD, `scripts/run_funding_ablations.py --help`, and relevant src loaders. Confirm split design = 4×30-day walk-forward (2024-04-01..2024-09-30, 7d purge/embargo), ablations A–E, primary QLIKE, contrast E vs A, 24h UTC block bootstrap joint across instruments.
2. **Run** the ablation with explicit exploratory labeling in experiment-id/suffix/out paths; use `--include-cache` (and `--split-design v3_30d` or auto per script contract for 2024-04..09). Ensure train-only normalization, last-known funding ≤ hour, no test tuning. Capture full stdout/stderr to a versioned log under `research_state/` or `results/` (small, committed if concise).
   - Example shape (verify flags against `--help` before running): `python scripts/run_funding_ablations.py --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --include-cache --split-design v3_30d --out-suffix _v4_exploratory_exec_20261109T<ts>Z --experiment-id GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D-EXPLORATORY-<ts> --pre-registration research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json`
3. **Validate outputs deterministically:** metrics files exist, no NaN/inf in reported aggregates without explanation, sample counts/splits match prereg, ΔQLIKE CIs reported, leakage controls documented. Run any cheap integrity checks the script provides.
4. **Run robustness/sensitivity only if prereg-scoped and cheap** (block size sensitivity, instrument leave-one-out) — label EXPLORATORY. Do NOT expand to confirmatory claims.
5. **Write/refresh a concise exploratory evaluation note** (versioned, e.g. `results/fclr_heavy001/gate4_v4_exploratory_exec_<ts>.md` or `research_state/evaluation_summary_gate4_v4_exploratory_<ts>.md`) with: exact command, git SHA, input manifest hash ref, split/sample table, per-ablation metrics, E vs A ΔQLIKE+CI, shortfalls, and explicit NOT CONFIRMATORY/NOT PROMOTABLE verdict.
6. **Tests:** `python -m unittest discover tests` must remain **>=950 OK** (fix regressions you introduce; do not weaken assertions). Re-run `python scripts/tracka_resume_check.py` and `python scripts/tracka_resume_gate.py --json` — Track A invariants must hold (17/17 pass, probes==2, BLOCKED expected, `outcomes_inspected:false`).
7. **Update this handoff** (§1–§10) with exact commands/outcomes/artifact paths and the next highest-value unfinished task.

**If the runner fails due to missing deps/data shape:** diagnose with smallest deterministic check, fix loader/path issues (no fake data), document blocker with evidence, then pivot to **Track A G1-G3 hardening gaps**: missing `test_tracka_hardening_133-135` sequence — add `tests/test_tracka_hardening_139.py` (or next appropriate) covering: (a) empty/unreadable data path under valid prereg → blocked stable reason codes, (b) CLI argparse edge cases across resume_check/gate/operator, (c) cross-CLI refusal payload parity/canonical-output immutability. Keep tmp-isolated, no network/parquet/outcome reads, no real research_state writes.

**Acceptance for next session:** at least one of (A) versioned Gate 4 v4 exploratory ablation artifacts + evaluation note with metrics/CIs and NOT CONFIRMATORY labeling, OR (B) new hardening tests merged-in-repo with full suite green and Track A invariants green — with exact evidence in this handoff.

---

## 1. WHAT CHANGED AND WHY (this session)
- **Verified preconditions for Gate 4 v4 campaign:** git tree clean at f59b4ad3a; full suite 950/950 OK; Track A invariants all green (17/17, probes==2, BLOCKED expected, outcomes_inspected:false); local 2024-04..09 cache present per FCLR-015 manifest; v4 prereg FROZEN_BEFORE_OUTCOMES with confirmatory_claim_go=NO_GO and exploratory_smoke_authorized_after_freeze=true. No code changes; state unchanged from prior session. Campaign §0 is ready to execute.
- **No Track A re-probing, no workflows/controllers added, no Track C/B scope change.**

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Full suite (this session) | `python -m unittest discover tests` | **Ran 950 tests in 110.145s — OK** |
| Track A resume check (this session) | `python scripts/tracka_resume_check.py` | `pass:true`, 17/17 checks, `network:false`, `probes==2`, `writes_real_research_state:false` |
| Track A resume gate (this session) | `python scripts/tracka_resume_gate.py --json` | `drift_preflight.pass:true`, `status:BLOCKED`, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false` |
| Track A operator report (this session) | `python scripts/tracka_operator_report.py` | `pass:true` |
| Baseline (prior session, before fclr024 fix) | `python -m unittest discover tests` | 950 ran, 3 failures, 2 errors (all `test_fclr024_v5_scope_coherence_report`) |
| Targeted fix verify (prior session) | `python -m unittest tests.test_fclr024_v5_scope_coherence_report -v` | 8 tests OK |
| Full suite (prior session, after fix) | `python -m unittest discover tests` | **Ran 950 tests in 108.634s — OK** |
| Track A resume check (prior session) | `python scripts/tracka_resume_check.py` | `pass:true`, 17/17 checks, `network:false`, `probes==2`, `writes_real_research_state:false` |
| Track A resume gate (prior session) | `python scripts/tracka_resume_gate.py --json` | `drift_preflight.pass:true`, `status:BLOCKED`, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false` |
| Track A operator report (prior session) | `python scripts/tracka_operator_report.py` | `pass:true`, exit 0 |
| Latest hardening pattern sanity | `python -m unittest tests.test_tracka_hardening_138 -v` | 9 tests OK |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `scripts/fclr024_v5_scope_coherence_report.py` | Fixed gate-input-summary consumption: stable `artifact/read_state/sha256/bytes/scope_note` fields; tolerate nested `gate_input_summary`; read-only, no GO/confirmatory claims. |
| `AGENT_HANDOFF.md` | Replaced with this single durable, timestamped handoff + mandatory heavy next-task campaign. |
| `research_state/ironflow_fastpath_cache.json` | Modified by local tooling during checks; **do not commit** (cache). |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A: **BLOCKED** (no admissible unauth liquidation labels). Track C: PASSED (historical) / sealed. Gate 4 exploratory: **local 2024-04..09 cache present** (verify per-run). | `track_a_deadend_map.md`; `fclr015_input_manifest_2024_04_09...`; `research_state/data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED (Track C FCLR-001 context); Gate 4 v4 prereg **FROZEN_BEFORE_OUTCOMES** but `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 due to sealed-anchor conflict. | `research_protocol.md`; `pre_registration_gate4_funding_multisplit_v4_20271107T1845Z.json` (canonical path in repo) |
| **Gate 3 (RV-only Baseline)** | Track C: PASSED historical / **INCONCLUSIVE forward** (5-day test window, 0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **UNFINISHED / ACTIONABLE (EXPLORATORY)** on local 2024-04..09 v4 design — **next heavy target**. Prior pilot outputs exist but shortfalls (e.g., 14-day blocks / data sufficiency) — see `evaluation_summary.md` funding section. | `scripts/run_funding_ablations.py`, v4 prereg, FCLR-015 manifest |
| **Forecast Gate** | **NOT ELIGIBLE** (Track C forward Gate 3 inconclusive; Track A blocked). No confirmatory promotion from v4 exploratory run. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
Execute **§0 Campaign**: Gate 4 v4 **EXPLORATORY** funding-conditioned volatility ablation on local 2024-04..09 cache, producing versioned metrics/CI artifacts + concise evaluation note labeled **NOT CONFIRMATORY/NOT PROMOTABLE**; keep tests/Track A invariants green. If blocked by real loader/data issues, pivot to measurable Track A G1-G3 hardening with new tests (no trigger side effects).

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python -m unittest discover tests                         # expect 950+ OK
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, network:false
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
python scripts/tracka_operator_report.py                 # expect pass:true
python scripts/run_funding_ablations.py --help          # confirm flags before Gate 4 run
# after Gate 4 exploratory exec: verify versioned outputs exist and contain sample/metric/CI tables
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, rubric NO-GO all 8 candidates; probes==2; 2026-11..2027-02 absent | **Only** if a genuinely new unauth source meets full rubric; else guard hardening only. No re-probe absent months. |
| Track C: forward panel ends 2026-11-02, 0 non-overlapping 30d test blocks | `fclr012v_coverage_audit.json`, FCLR-012-V inconclusive | New admissible panel with real volume, ≥3 non-overlapping 30d blocks; do not relax criteria. |
| Gate 4 v4: sealed-anchor conflict on 2024 slice | v4 prereg `confirmatory_claim_go:NO_GO` | Run as **EXPLORATORY only**, explicit labeling, no promotion. |
| Protected control plane | repo instructions | **No `.github/workflows` edits** without explicit maintainer authorization. |

## 8. DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create new probe/scan/wrapper/report families for Track A
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new work (sealed/NOT_SUPPORTED) except documenting hard blockers
- ❌ Conflate observed/modeled/synthetic labels; no threshold-shopping/holdout reuse
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Live/paper trading, order endpoints, credentials, bypassing access controls

## 9. SESSION START PROTOCOL (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests, tests, data cache state.
3. Execute §0 (highest-value measurable task). Run cheapest checks first.
4. Update **this file** with exact changes/commands/results/evidence/gates/next task + blockers.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with Gate 4 v4 exploratory exec evidence (or hardening evidence), full suite + Track A invariant outcomes, artifact paths, and the next unfinished task. **Repo state must remain continuable without user repeating instructions.**

---
**END OF SINGLE DURABLE HANDOFF.**
