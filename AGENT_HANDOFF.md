# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# EXECUTE FCLR-LIVE-ARCHIVE-05 — funding-conditioned SIGNED-JUMP / realized-semivariance ASYMMETRY

**Timestamp:** 2026-11-26T07:19:22Z
**Session:** NEXT (routing only; no heavy artifact is claimed by this refresh)
**Active campaign (machine-bound):** `FCLR-LIVE-ARCHIVE-05-20261126T071922Z` — `READY_EXECUTE`
**Latest completed heavy session:** `session_20261126T061929Z`
**Repo-name priority:** the repository name leads with **Funding-conditioned-volatility**, so rank-0 is the funding-conditioned volatility program. The Binance-archive mean-RV, stress/tail, and quantile/full-distribution arms are closed `NOT_SUPPORTED`. The untested repo-name estimand is **signed-jump / realized-semivariance asymmetry**: upside versus downside next-24h realized variance.

> This is the SOLE durable handoff for next-session routing. The heavy-work gate reads this file only.
> **A timestamp-only rewrite is not progress. Creating a new `session_<UTC>/` without the complete `fclr_live_archive05_*` heavy set is a FAILURE. There is no probe-only, prereg-only, audit-only, source-registry-only, verify-and-stop, or no-new-session branch.**

---

## 1. FIRST ACTIONS — EXECUTE IN THIS ORDER

1. Run `export UTC=$(date -u +%Y%m%dT%H%M%SZ)` and `mkdir -p research_state/session_$UTC`. The new id MUST be lexicographically greater than `20261126T071922Z`; do not reuse an older session.
2. Reuse the verified raw cache read-only: `research_state/session_20261126T042519Z/raw/` (1,200 monthly zips). Do not re-download unless a file is missing.
3. Copy and adapt `research_state/session_20261126T061929Z/fclr_live_archive04_eval_20261126T061929Z.py`. Keep its deterministic stdlib MM/IRLS and block-bootstrap patterns; replace the quantile target with the frozen asymmetry target in §3.
4. Produce every artifact in §4 under that ONE new `session_$UTC/`. Every file must be non-empty and every JSON must carry `experiment_id:"FCLR-LIVE-ARCHIVE-05"` and the real `session_id`.
5. Record the real session id in §8 and synchronize `research_state/experiment_frontier.json` only after the artifacts exist. Then run §5 until the gate reports `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive05"`, and `failures=[]`.

If you are about to rewrite this file without a new heavy session, stop: that is the forbidden refresh loop. Execute the evaluation.

---

## 2. FRONTIER RECONCILIATION — READ BEFORE ACTING

- **FCLR-LIVE-ARCHIVE-01 — CLOSED `NOT_SUPPORTED`:** mean log-RV QLIKE; C2 versus B1 relative reduction 0.840%, below the 2% floor.
- **FCLR-LIVE-ARCHIVE-03 — CLOSED `NOT_SUPPORTED`:** next-24h variance stress/tail exceedance; relative Brier reduction 0.458%, 95% CI includes zero.
- **FCLR-LIVE-ARCHIVE-04 — CLOSED `NOT_SUPPORTED`:** quantile/full-distribution volatility; relative average-pinball reduction -1.102%, 95% CI [-1.233%, -0.969%]. Heavy artifacts and independent recompute are under `session_20261126T061929Z`; `all_checks_match=true`.
- **FCLR-009 — CLOSED `NOT_MET`.**
- **Liquidation-risk program on the frozen panel — CLOSED.** Do not reopen.
- **Active rank-0:** `FCLR-LIVE-ARCHIVE-05-20261126T071922Z`, `READY_EXECUTE`. No `fclr_live_archive05_*` artifact exists yet.

**Bottleneck removed in this refresh:** the campaign start and frontier were rebound from the stale `20261126T061929Z` routing point to this handoff's `20261126T071922Z` start. The artifact family and frozen scientific design are unchanged; only the stale session boundary was repaired. This prevents an older post-start session from being mistaken for the current execution target.

**Why the gate is green today:** the latest on-disk session equals the prior completed heavy session (`session_20261126T061929Z`), which predates the rebound campaign start, so the grandfather clause applies. The instant any newer `session_<UTC>/` exists, the complete campaign-05 artifact set becomes mandatory in that same session.

---

## 3. FROZEN EXECUTION DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort:** 2021-01-01 through 2024-12-31 UTC; exactly `1INCHUSDT`, `AAVEUSDT`, `ADAUSDT`, `ALGOUSDT`, `ALPHAUSDT`. Do not substitute coins or re-enumerate the cohort.
2. **Primary target:** next-24h realized-semivariance asymmetry
   `A = log((RV_plus + eps) / (RV_minus + eps))`,
   where `RV_plus` sums squared positive 1h log-returns and `RV_minus` sums squared negative 1h log-returns over the next 24 hours. Use a fixed positive `eps`, train-only scaling, and no test-set outcome fitting.
3. **Features:** B1 is HAR of signed components: log RV1h/RV24h/RV168h plus log RV_plus/RV_minus at 24h/168h. C2 is B1 plus signed funding(24h), trailing 90-day absolute-funding percentile, mark/index premium, and mark/EMA24 distance. All scaling is train-only.
4. **Split and leakage controls:** 60/20/20 by unique UTC timestamp; 168-hour purge/embargo; test split divided into three chronological blocks. Do not open sealed holdouts.
5. **Models:** fixed-form linear regression for B1 and C2 using the same deterministic stdlib MM/IRLS or coordinate-descent procedure. Also report a secondary downside-dominance sign classifier on the same split; the continuous asymmetry MSE contrast remains primary.
6. **Inference:** out-of-sample MSE and R² (primary), sign accuracy (secondary), at least 2,000 deterministic block-bootstrap replicates with a fixed seed, per-block diagnostics, and leave-one-symbol-out diagnostics.
7. **Materiality and verdict:** `PROMOTED` requires at least a 2% relative test-MSE reduction for C2 versus B1 and a 95% block-bootstrap CI lower bound above zero. Otherwise preserve `NOT_SUPPORTED`; use `INCONCLUSIVE` only if the evidence cannot support either conclusion. A valid null is acceptable; fabricated passes and placeholders fail closed.

---

## 4. REQUIRED ARTIFACTS — ALL UNDER THE SAME FRESH SESSION

- `fclr_live_archive05_source_registry_<UTC>.{json,md}` — exact source URLs, cache checksums, coverage, and read-only reuse statement.
- `fclr_live_archive05_prereg_<UTC>.{json,md}` — outcome-blind and hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`.
- `fclr_live_archive05_eval_<UTC>.{py,json,md}` — heavy three-block evaluation triad implementing §3.
- `fclr_live_archive05_recompute_<UTC>.{py,json}` — independent stdlib recompute with `all_checks_match:true` and reproduced verdict.
- `fclr_live_archive05_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass` and `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — substantive gate-critical alias matching the verdict.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.

No zero-byte placeholders. Stdlib only; do not install packages. Do not add root-level `research_state/*.md` or `*.json` files: the root is at its 500-file cap. Do not modify workflows or overwrite sealed artifacts.

---

## 5. VERIFICATION COMMANDS

```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
tests.test_tracka_hardening_143 tests.test_active_campaign_gate
```

Required gate result after the heavy session: top-level `pass=true`, `reason_code=OK`, `failures=[]`; `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive05"`, and empty missing/empty artifact lists.

---

## 6. INPUTS AND REUSABLE IMPLEMENTATIONS

| Path | Use |
|---|---|
| `research_state/session_20261126T042519Z/raw/` | 1,200 verified monthly zips; reuse read-only. |
| `research_state/session_20261126T061929Z/fclr_live_archive04_eval_20261126T061929Z.py` | Stdlib parser, MM/IRLS, split, and bootstrap template. |
| `research_state/session_20261126T061929Z/fclr_live_archive04_recompute_20261126T061929Z.py` | Independent-recompute pattern. |
| `research_state/experiment_frontier.json` | Rank-0 registry; update only after artifacts exist. |
| `RESEARCH_PROMPT.md` §3/§7/§8/§9/§16/§17/§19/§20 | Research constraints and reporting requirements. |

If a feature month is missing, do not silently substitute or zero-fill. Record the exact shortfall in the source registry and evidence audit, run with the available feature set, and disclose the deviation.

---

## 7. NON-AVOIDANCE CONSTRAINTS

- Do not re-run closed campaigns or relabel exploratory work as confirmatory.
- Do not build a risk overlay; the forecast gate is not passed.
- Do not stop at a source probe, prereg, audit, trigger check, or handoff refresh.
- Do not create an empty/partial session and leave it unrecorded.
- The next session must leave a complete heavy artifact set, a reproduced verdict, and a synchronized frontier.

---

## 8. SESSION CLOSE-OUT — 2026-11-26T07:19:22Z

**What changed:** the sole durable handoff was refreshed to the current timestamp; campaign 05's start was rebound to `20261126T071922Z`; the rank-0 frontier was synchronized to the same campaign id; the prior handoff was archived at `handoff_archive/AGENT_HANDOFF_20261126T070100Z.md`.

**What was tested this session:** no new quantitative campaign was executed and no heavy artifact is claimed. Baseline verification passed: the heavy-work gate returned `pass=true`, `reason_code=OK`, `failures=[]`; `python3 -m py_compile scripts/check_handoff_heavywork_gate.py` passed; the six-module unittest command in §5 passed 122 tests. The latest completed heavy session remains `session_20261126T061929Z`.

**Single highest-value next task:** execute the complete campaign-05 asymmetry evaluation, independent recompute, evidence audit, gate alias, and trigger check in one fresh session strictly newer than `20261126T071922Z`.

**Latest completed session:** `session_20261126T061929Z`

---

## 9. RESEARCH_PROMPT §19 ANSWERS

**Supported:** funding and price features have not cleared the 2% materiality floor for mean-RV, stress/tail, or quantile/full-distribution volatility on the verified Binance archive.

**Contradicted:** claims that no next repo-name campaign exists or that a refresh-only session is acceptable.

**Unknown:** whether funding and price features improve signed-jump / realized-semivariance asymmetry forecasts.

**Strongest alternative explanation:** HAR may already capture most symmetric predictable variation; asymmetry can detect directional variance shape missed by mean, tail, and quantile metrics.

**Dominant limitation:** only five symbols are available, so per-block and leave-one-symbol-out diagnostics are mandatory.

**Concrete falsification test:** C2 improves relative test MSE by less than 2%, or the 95% block-bootstrap CI lower bound is not above zero.

**Highest information gain per free compute:** campaign 05 uses an unexploited estimand, a verified local cache, and a proven stdlib numerical template.

**Exact progress artifact:** the complete `fclr_live_archive05_*` set under one fresh session, followed by a green heavy-work gate and the six-module unittest command.

(End of file)