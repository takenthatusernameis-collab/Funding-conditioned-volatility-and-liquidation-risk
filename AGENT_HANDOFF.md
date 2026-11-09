# AGENT_HANDOFF.md — Single Durable Handoff (next session must continue from here)

**Generated:** 2026-11-09T01:09:49Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Priority (reconciled):** Repo P0 = Phase 3 Gate 4 funding-conditioned volatility ablations using local data (measurable, unblocked). Track A = structurally blocked / no trigger (lockdown hardening only if specific gap); Track C sealed/inconclusive forward; Track B NOT_SUPPORTED. **No status-only churn.**
**Verified this session (baseline):** git clean at start (758eee502 HEAD); Gate 4 v4 EXPLORATORY ablation executed previously (exit 0, NOT CONFIRMATORY/NOT PROMOTABLE) on local 2024-04..09 cache with versioned artifacts under `research_state/gate4_v4_exploratory_exec/` satisfying Track A root bound (172) — no check weakened; `python -m unittest discover tests` → Ran 950 tests OK; `tracka_resume_check.py` → pass:true, 17/17 checks, root_md_json_bounded 171/172 pass, probes==2, network:false, writes_real_research_state:false; `tracka_resume_gate.py --json` → drift_preflight.pass:true, status:BLOCKED, reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, outcomes_inspected:false. Local 2024-04..09 cache present; v4 prereg FROZEN_BEFORE_OUTCOMES, confirmatory_claim_go=NO_GO, exploratory_smoke_authorized_after_freeze=true.

---

## 0) INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION (MANDATORY, HEAVY WORK)

**You MUST execute measurable research/engineering progress in this session. Do not probe absent Track A months (2026-11..2027-02). Do not add workflows/schedulers/pollers/wrappers/controllers. Do not touch `.github/workflows`.**

### Campaign: Gate 4 v4 EXPLORATORY follow-up — diagnose instability + prereg-scoped robustness (local 2024-04..09) — produce versioned, auditable artifacts

**Intent (per frozen prereg):** `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` is `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`, `exploratory_smoke_authorized_after_freeze=true`. **All outputs MUST be labeled EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE** (sealed-anchor conflict with FCLR002/003/013 domain family). Never claim confirmatory GO or economic value.

**Completed this session (do not rerun identically; build on it):** `GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D-EXPLORATORY-20261109T004003Z` (SHA 2f21b1dd4, 2026-11-09T00:40:03Z). Exit 0. Primary E vs A ΔQLIKE (alt−base; negative=better) **+0.4879, 95% block CI [-0.04216, 1.19734] (spans 0, n_obs=12969, n_blocks=120)** — **INCONCLUSIVE, no improvement claim**. Data sufficiency met (5 instruments, 4×30d splits). B/D show extreme split instability (split 3 B vs A Δ=44.69, D vs A Δ=10.33); E vs A inconclusive across block 12/24/48h. Artifacts: `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md`, `research_state/gate4_v4_exploratory_exec/evaluation_summary_funding_v4_exploratory_exec_20261109T004003Z.md`, `research_state/gate4_v4_exploratory_exec/run_manifest_funding_v4_exploratory_exec_20261109T004003Z.json`, `research_state/gate4_v4_exploratory_exec/gate4_v4_exploratory_exec_20261109T004003Z.log`. FCLR-015 manifest SHA256 `3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c`.

**Execute (versioned suffix, e.g. `_v4_exploratory_diag_20261109T####Z`; do not overwrite prior exec outputs):**
1. **Read** prior run manifest/evaluation + `scripts/run_funding_ablations.py` and src (e.g., `src/models/funding_ablations.py` or equivalent) to understand B/D/E feature construction, direct-variance OLS HAR, clipping/bounds, and why B/D explode on split 3.
2. **Diagnose instability deterministically (no fake data):** inspect per-split/per-instrument predictions/loss contributions if supported; otherwise add a small, tested diagnostic path (versioned script or flag) that emits EXPLORATORY diagnostics (coefficient magnitudes, prediction bounds, NaN/inf counts, per-instrument ΔQLIKE) without changing primary estimands. Run targeted unit tests for any new code.
3. **Run prereg-scoped exploratory robustness only if cheap and justified:** instrument leave-one-out for E vs A; confirm train-only normalization/last-known funding alignment; optionally stabilized variant comparison labeled EXPLORATORY (do NOT replace A–E prereg contrasts; do NOT claim confirmatory improvement).
4. **Write a concise versioned diagnostic note** (`results/fclr_heavy001/gate4_v4_exploratory_diag_<ts>.md` or `research_state/...`) with: commands, git SHA, tables, root-cause hypotheses for B/D split-3 blowup, E vs A interpretation, and explicit NOT CONFIRMATORY/NOT PROMOTABLE verdict.
5. **Tests:** `python -m unittest discover tests` must remain **>=950 OK** (fix regressions you introduce). Re-run `python scripts/tracka_resume_check.py` and `python scripts/tracka_resume_gate.py --json` — Track A invariants must hold (17/17 pass, probes==2, root bound satisfied, BLOCKED expected, `outcomes_inspected:false`).
6. **Root-bound bottleneck:** `tracka_resume_check` enforces `root_md_json_bounded <= 172`. Place new Gate 4 exploratory artifacts under subdirs (e.g., `research_state/gate4_v4_exploratory_exec/`, `research_state/gate4_v4_exploratory_diag/`, `results/fclr_heavy001/`) rather than adding root md/json files. **Do not weaken the bound/check.**
7. **Update this handoff** (§1–§10) with exact commands/outcomes/artifact paths and the next highest-value unfinished task.

**If Gate 4 is blocked by real code/data issues:** document with evidence, then pivot to **Track A G1-G3 hardening gaps**: add next hardening tests (tmp-isolated, no network/parquet/outcome reads, no real research_state writes) covering edge cases across resume_check/gate/operator; keep invariants green.

**Acceptance for next session:** at least one of (A) versioned Gate 4 v4 exploratory diagnostic/robustness artifacts explaining B/D instability and E vs A with NOT CONFIRMATORY labeling, OR (B) new hardening tests merged-in-repo with full suite green and Track A invariants green — with exact evidence in this handoff.

---

## 1. WHAT CHANGED AND WHY (this session)
- **Executed Gate 4 v4 EXPLORATORY ablation (measurable progress):** ran `scripts/run_funding_ablations.py` (exit 0) for 2024-04-01..2024-09-30, 5 symbols, `--include-cache --split-design v3_30d`, v4 prereg `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json`. Produced versioned run manifest/evaluation/log + results note, all labeled NOT CONFIRMATORY/NOT PROMOTABLE. Primary E vs A ΔQLIKE +0.4879, 95% CI [-0.04216,1.19734] (spans 0) — inconclusive. Data sufficiency met (4×30d splits). B/D unstable (split 3 blowups); flagged honestly.
- **Bottleneck removed (root bound, no weakening):** `tracka_resume_check.root_md_json_bounded` cap is 172 and new exec artifacts initially made root count 173 (failing check). Moved exec run manifest/evaluation/log into `research_state/gate4_v4_exploratory_exec/` (kept results note in `results/fclr_heavy001/`); updated paths in results note. `resume_check` now passes; `resume_gate` remains BLOCKED/expected. **Did not change bound or checks.**
- **Verified invariants after changes:** full suite 950/950 OK; Track A 17/17, probes==2, network:false, writes_real_research_state:false; gate BLOCKED, `outcomes_inspected:false`.
- **No Track A re-probing, no workflows/controllers added, no Track C/B scope change.**

## 2. WHAT WAS ACTUALLY TESTED — EXACT OUTCOMES
| Check | Command | Result |
|---|---|---|
| Deps sanity | `python -c "import pandas,numpy,scipy; print('deps ok')"` | `deps ok` |
| Ablation tests | `python -m unittest tests.test_funding_ablations -v` | **7 tests OK** |
| **Gate 4 v4 exploratory exec** | `python scripts/run_funding_ablations.py --symbols BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT --start 2024-04-01 --end 2024-09-30 --include-cache --split-design v3_30d --out-suffix _v4_exploratory_exec_20261109T004003Z --experiment-id GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D-EXPLORATORY-20261109T004003Z --pre-registration research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` (tee log) | **Exit 0**. `DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (E vs A CI spans 0)`. Aggregate QLIKE A=0.7983,B=12.1836,C=0.8460,D=3.4493,E=1.2417. E vs A Δ=+0.4879 CI [-0.04216,1.19734], n=12969, blocks=120. |
| Full suite (final) | `python -m unittest discover tests` | **Ran 950 tests in ~99s — OK** |
| Track A resume check | `python scripts/tracka_resume_check.py` | `pass:true`, 17/17 checks, `network:false`, `probes==2`, `writes_real_research_state:false`, `root_md_json_bounded` pass (171/172) |
| Track A resume gate | `python scripts/tracka_resume_gate.py --json` | `drift_preflight.pass:true`, `status:BLOCKED`, `reason_code:PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS`, `outcomes_inspected:false` |

## 3. EVIDENCE ADDED / MODIFIED (paths)
| Path | Change |
|---|---|
| `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md` | **Added.** EXPLORATORY exec note (command, SHA, manifest SHA256, splits/samples, metrics/CIs, instability, NOT CONFIRMATORY verdict). |
| `research_state/gate4_v4_exploratory_exec/evaluation_summary_funding_v4_exploratory_exec_20261109T004003Z.md` | **Added (moved under subdir for root-bound).** Script-generated evaluation summary. |
| `research_state/gate4_v4_exploratory_exec/run_manifest_funding_v4_exploratory_exec_20261109T004003Z.json` | **Added (moved under subdir for root-bound).** Machine-readable manifest (splits, metrics, CIs, sensitivity, per-split deltas, sufficiency). |
| `research_state/gate4_v4_exploratory_exec/gate4_v4_exploratory_exec_20261109T004003Z.log` | **Added (moved under subdir for root-bound).** Full stdout log. |
| `research_state/ironflow_fastpath_cache.json` | Modified by local tooling during checks; **do not commit** (cache). |
| `AGENT_HANDOFF.md` | Replaced with this single durable, timestamped handoff + mandatory heavy next-task campaign. |

## 4. CURRENT STATE OF EACH RESEARCH GATE
| Gate | Status | Evidence / Notes |
|---|---|---|
| **Gate 1 (Data Loadable)** | Track A: **BLOCKED** (no admissible unauth liquidation labels). Track C: PASSED (historical) / sealed. Gate 4 exploratory: local 2024-04..09 cache present (FCLR-015). | `track_a_deadend_map.md`; `fclr015_input_manifest_2024_04_09...` SHA256 `3e6ac26c...5406c`; `research_state/data_cache/*_2024_04..09` |
| **Gate 2 (Protocol Frozen)** | PASSED (Track C FCLR-001 context); Gate 4 v4 prereg **FROZEN_BEFORE_OUTCOMES** but `confirmatory_claim_go=NO_GO`, exploratory-only on 2024-04..09 due to sealed-anchor conflict. | `pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` |
| **Gate 3 (RV-only Baseline)** | Track C: PASSED historical / **INCONCLUSIVE forward** (5-day test window, 0 non-overlapping 30d blocks). | `evaluation_summary_FCLR-012-V.md` |
| **Gate 4 (Incremental Funding/Price)** | **EXPLORATORY EXECUTED (INCONCLUSIVE, NOT CONFIRMATORY)** — v4 20261109T004003Z: E vs A ΔQLIKE +0.488 CI [-0.042,1.197] spans 0; B/D unstable (split-3 blowups). **Next:** diagnose instability / prereg-scoped robustness (EXPLORATORY), versioned artifacts. | `results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md`; `research_state/gate4_v4_exploratory_exec/*` |
| **Forecast Gate** | **NOT ELIGIBLE** (Track C forward Gate 3 inconclusive; Track A blocked). No confirmatory promotion from v4 exploratory run. | frontier/negative results |

## 5. SINGLE HIGHEST-VALUE NEXT TASK
Execute **§0 Campaign**: diagnose B/D split-3 instability and produce prereg-scoped exploratory robustness/diagnostics for Gate 4 v4 (instrument LOO for E vs A, coefficient/prediction bounds, alignment checks) with versioned artifacts labeled **NOT CONFIRMATORY/NOT PROMOTABLE**; keep tests/Track A invariants green and root bound satisfied. If blocked, pivot to measurable Track A G1-G3 hardening with new tests.

## 6. PRECISE VERIFICATION COMMANDS
```bash
git --no-pager status --short
python -m unittest discover tests                         # expect >=950 OK
python scripts/tracka_resume_check.py                    # expect pass:true, 17/17, probes==2, network:false, root_md_json_bounded pass
python scripts/tracka_resume_gate.py --json              # expect BLOCKED, drift_preflight.pass:true, outcomes_inspected:false
python scripts/run_funding_ablations.py --help
# exec artifacts (completed 20261109T004003Z)
ls results/fclr_heavy001/gate4_v4_exploratory_exec_20261109T004003Z.md
ls research_state/gate4_v4_exploratory_exec/
```

## 7. BLOCKERS / CONSTRAINTS
| Blocker | Evidence | Allowed next route |
|---|---|---|
| Track A: no admissible liquidation labels | `track_a_deadend_map.md`, rubric NO-GO all 8 candidates; probes==2; 2026-11..2027-02 absent | **Only** if a genuinely new unauth source meets full rubric; else guard hardening only. No re-probe absent months. |
| Track C: forward panel ends 2026-11-02, 0 non-overlapping 30d test blocks | `fclr012v_coverage_audit.json`, FCLR-012-V inconclusive | New admissible panel with real volume, ≥3 non-overlapping 30d blocks; do not relax criteria. |
| Gate 4 v4: sealed-anchor conflict on 2024 slice | v4 prereg `confirmatory_claim_go:NO_GO` | Run as **EXPLORATORY only**, explicit labeling, no promotion. |
| Gate 4 v4 B/D instability | v4 exec 20261109T004003Z: split 3 B/D ΔQLIKE blowups | Diagnose with deterministic, versioned EXPLORATORY analysis; do not claim improvement. |
| Track A root md+json bound | `scripts/tracka_resume_check.py` cap 172 | Put new exploratory artifacts in subdirs/results; **do not weaken bound/check**. |
| Protected control plane | repo instructions | **No `.github/workflows` edits** without explicit maintainer authorization. |

## 8. DO NOT DO
- ❌ Re-probe 2026-11..2027-02 / create new probe/scan/wrapper/report families for Track A
- ❌ Workflows/schedulers/pollers/status-only files/controllers
- ❌ Track C/B new work (sealed/NOT_SUPPORTED) except documenting hard blockers
- ❌ Conflate observed/modeled/synthetic labels; no threshold-shopping/holdout reuse
- ❌ Commit `__pycache__/`, `research_state/ironflow_fastpath_cache.json`, large raw caches
- ❌ Weaken `root_md_json_bounded` or Track A invariants to accommodate artifacts
- ❌ Live/paper trading, order endpoints, credentials, bypassing access controls

## 9. SESSION START PROTOCOL (mandatory)
1. `git pull` + `git status`; read **this file** + `RESEARCH_PROMPT.md`.
2. Inspect `research_state/experiment_frontier.json`, latest manifests, tests, data cache state, and `research_state/gate4_v4_exploratory_exec/`.
3. Execute §0 (highest-value measurable task). Run cheapest checks first.
4. Update **this file** with exact changes/commands/results/evidence/gates/next task + blockers.

## 10. NEXT SESSION DELIVERABLE
Updated `AGENT_HANDOFF.md` with Gate 4 v4 exploratory diagnostic/robustness evidence (or hardening evidence), full suite + Track A invariant outcomes, artifact paths, root-bound compliance, and the next unfinished task. **Repo state must remain continuable without user repeating instructions.**

---
**END OF SINGLE DURABLE HANDOFF.**
