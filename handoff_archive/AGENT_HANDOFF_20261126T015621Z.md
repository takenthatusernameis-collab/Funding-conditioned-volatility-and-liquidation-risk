# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# AGENT_HANDOFF.md — FCLR-LIVE-ARCHIVE-01 Confirmatory Volatility Evaluation (repo-name rank-0)

**Timestamp:** 2026-11-26T01:56:21Z
**Session:** NEXT (to execute)
**Campaign:** FCLR-LIVE-ARCHIVE-01-20261125T074500Z (ACTIVE rank-0, READY_EXECUTE)
**Hypothesis:** FCLR-H001 (incremental 24-hour realized-variance forecasting; funding + price features vs RV-only baseline)
**Repo-name priority:** repository name leads with **Funding-conditioned-volatility** → rank-0 is the funding-conditioned mean-RV QLIKE campaign below.
**Status:** FROZEN_PANEL_EXHAUSTED | NEW_SOURCE_VERIFIED | COVERAGE_FROZEN | EXECUTION_NOT_STARTED

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **A timestamp-only rewrite is NOT progress and is forbidden as the next session's deliverable. The next session must materialize the heavy evaluation + recompute artifacts.**

---

## 0. RECONCILIATION — WHAT WAS STALE AND IS NOW FIXED (read first)

The previous live handoff (timestamp 2026-11-26T01:53:15Z) was **STALE and WRONG**: it told the next session to "execute the FCLR-009 confirmatory evaluation" as if it were NOT_STARTED. On-disk evidence contradicts that:

- `research_state/evaluation_summary_FCLR-009.md` EXISTS (generated 2026-11-10T00:18:07Z) and records the FCLR-009 gate verdict: **NOT_MET** (C2 vs B1 relative QLIKE −0.43%, 95% CI [−0.003120, 0.006165] includes zero; 5 instruments; 6 test blocks). FCLR-009 is CLOSED. **Do NOT re-run FCLR-009.**
- The accurate prior handoff is preserved at `handoff_archive/AGENT_HANDOFF_20261126T015039Z.md`; it correctly names the active campaign. This file supersedes the stale 01:53:15Z version and re-anchors to the on-disk frontier.

**Bottleneck removed:** the durable handoff no longer misroutes the next session to a completed experiment. Following the stale version would have wasted the session AND failed the heavy-work gate closed (the gate's live-archive binder demands `fclr_live_archive01_*` artifacts, which an FCLR-009 rerun would never produce).

**Frontier truth (authoritative):** `research_state/experiment_frontier.json` rank-0 = `FCLR-LIVE-ARCHIVE-01-20261125T074500Z`, status `READY_EXECUTE`, `session=null`, `completed_session=null`. All frozen-panel volatility arms (BROAD-01, CORR-01, STRESS-01, JUMP-01/02/03/04) and the liquidation-risk program are COMPLETED_VALIDATED. The live-archive campaign is the only open rank-0.

---

## 1. What Changed & Why

The frozen 18-month `ironflow_bulk` panel is exhausted for both halves of the program (Half 1 funding-conditioned volatility NOT_SUPPORTED on all arms; Half 2 liquidation risk confirmatory-exhausted). Per RESEARCH_PROMPT.md §16 (adaptive feasibility: three blocked routes → new materially-different experiment) and §10 (continuous priorities), the rank-0 frontier is a **new-source confirmatory test** on a verified, free, unauthenticated source that was never exploited: the **Binance public market-data archive** (S3 `data.binance.vision`, monthly `klines/markPriceKlines/indexPriceKlines/premiumIndexKlines/fundingRate`, 2021–2024). This directly attacks the repository-name-leading estimand (funding-conditioned mean-RV QLIKE) on a materially broader (4-year, multi-regime) source than the 18-month frozen panel.

This handoff re-anchors the next session to that campaign with a frozen, bounded, executable design so heavy work cannot be avoided.

---

## 2. What Was Actually Tested — Exact Outcomes (on-disk, authoritative)

| Artifact | Status | Evidence |
|----------|--------|----------|
| Frozen `ironflow_bulk` volatility arms | CLOSED NOT_SUPPORTED | BROAD-01 1.93% < 2% floor; CORR-01 materiality not met; STRESS-01 1.51%; JUMP-01..04 ≤0.30% (magnitude+direction) |
| Liquidation-risk program (frozen panel) | CONFIRMATORY-EXHAUSTED | Track A STRUCTURALLY_BLOCKED; Track B/C NOT_SUPPORTED; xsec SUPPORTED_GENERALIZATION but NOT_STABLE + floor NOT MET |
| `evaluation_summary_FCLR-009.md` | CLOSED NOT_MET | C2 vs B1 −0.43% rel QLIKE, CI incl. zero (2026-11-10) |
| Binance S3 monthly archive | VERIFIED REACHABLE | S3 delimiter catalog HTTP 200; 5 monthly source keys HTTP 200/206 (2026-11-25T12:52:23Z) |
| Frozen cohort coverage | FROZEN (outcome-blind) | 1,080 catalog symbols; 77 with 48/48 kline months (2021–2024); top five frozen 2026-11-26T01:05:14Z; all 25 symbol/source pairs 48/48 months, zero missing, `.CHECKSUM` sidecars present |
| FCLR-LIVE-ARCHIVE-01 evaluation | NOT_STARTED | No `fclr_live_archive01_*` artifact exists anywhere on disk (only an earlier campaign-02 set exists under `session_20261122T013000Z`) |

---

## 3. Evidence Added & Where

- `research_state/experiment_frontier.json` — rank-0 = live-archive campaign, READY_EXECUTE, full frozen design + blockers + verified roots.
- `handoff_archive/AGENT_HANDOFF_20261126T015039Z.md` — accurate prior handoff (provenance for the frozen cohort + coverage).
- `research_state/fclr009_coverage_audit.json`, `research_state/evaluation_summary_FCLR-009.md` — proof FCLR-009 is closed (do not reopen).
- This `AGENT_HANDOFF.md` — reconciled, timestamped, gate-compliant routing to the active campaign.

---

## 4. Current State of Each Research Gate

| Gate | Status | Evidence |
|------|--------|----------|
| Source feasibility (new archive) | DATA_READY | S3 monthly roots + funding keys HTTP 200/206; no auth; no payment |
| Coverage / cohort freeze | FROZEN | 5 symbols × 48 months, outcome-blind, 2026-11-26T01:05:14Z |
| Protocol freeze (live-archive) | PENDING (next session) | Must freeze outcome-blind prereg BEFORE target generation |
| Baseline / confirmatory evaluation | NOT_STARTED | No `fclr_live_archive01_*` artifacts |
| Forecast gate (§9) | NOT PASSED | Risk overlay remains ineligible |
| Heavy-work gate | PASS (grandfathered) | Latest on-disk session `session_20261125T060000Z` predates campaign start `20261125T074500Z`; next post-start session MUST satisfy `live_archive` |

---

## 5. Single Highest-Value Next Task

**Execute the full FCLR-LIVE-ARCHIVE-01 artifact set in ONE fresh `research_state/session_<UTC>/` (UTC strictly > `20261125T074500Z`), producing a heavy 3-block confirmatory mean-RV QLIKE evaluation + independent stdlib recompute + evidence audit + trigger check, with a valid `NOT_SUPPORTED` / `PROMOTED` / `INCONCLUSIVE` verdict.**

### Frozen execution design — DO NOT re-derive, expand, or threshold-shop

1. **Window & symbols (FROZEN):** 2021-01-01 → 2024-12-31 UTC. Use EXACTLY `1INCHUSDT`, `AAVEUSDT`, `ADAUSDT`, `ALGOUSDT`, `ALPHAUSDT`. Do NOT re-enumerate, re-rank, substitute a "better" coin, or inspect outcomes before freezing the prereg. Record the frozen 1,080-catalog / 77-complete / top-five coverage evidence in the source registry.
2. **Monthly sources only (S3 primary; CDN fallback only after S3 404):**
   - `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
   - `.../monthly/markPriceKlines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
   - `.../monthly/indexPriceKlines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
   - `.../monthly/premiumIndexKlines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
   - `.../monthly/fundingRate/<SYMBOL>/<SYMBOL>-fundingRate-YYYY-MM.zip`  ← funding has **NO `1h/` segment**
   - Enumeration catalog (provenance only, do NOT repeat): `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?prefix=data/futures/um/monthly/klines/&delimiter=/` (paginate `marker` until `IsTruncated=false`).
   - DO NOT USE: `data/spot/daily/*` (HTTP 404), `data.binance.vision` CDN for enumeration (JS-only HTML), `api.github.com` contents (HTTP 403). Daily metrics/OI are NOT needed.
3. **Budget & deps:** exactly 1,200 monthly zips + 1,200 `.CHECKSUM` files = 2,400 core requests (≤25 listing probes), ≤2 GiB, concurrency 4, max 4 retries + exponential backoff. Cache raw zips under `session_<UTC>/raw/`; verify every `.CHECKSUM` before parsing. **Stdlib ONLY:** `urllib.request`, `zipfile`, `csv`, `math`, `statistics`, `json`, `hashlib`. NO `pip install`; NO numpy/pandas/pyarrow/requests.
4. **Splits & embargo:** Freeze source registry + outcome-blind prereg BEFORE target generation (`outcome_data_inspected_before_freeze:false`). Splits from unique UTC timestamps: 60% train / 20% validation / 20% test; 7-calendar-day purge/embargo at all boundaries; test span → 3 equal non-overlapping blocks.
5. **Models (common panel, paired, train-only scaling + smearing):**
   - B0 = RV24 persistence.
   - B1 = OLS HAR on log RV1h / RV24h / RV168h → log next-24h RV.
   - C1 = B1 + signed funding + trailing 90-day absolute-funding percentile.
   - C2 = C1 + mark/index premium + mark/EMA24 distance.
   - Primary contrast: **C2 vs B1** on paired next-24h QLIKE. C1 vs B1 and C2 vs C1 = registered secondary contrasts (Holm across the family).
6. **Inference:** ≥2,000 deterministic block-bootstrap replicates (resample whole UTC time blocks jointly across symbols; seed fixed). Report absolute/relative QLIKE, MAE/RMSE, sample/event counts, coverage, exclusions, per-block + leave-one-symbol-out. Materiality floor: **≥2% relative QLIKE reduction**; uncertainty interval must support improvement.
7. **Verdict:** valid `NOT_SUPPORTED`, `PROMOTED`, or `INCONCLUSIVE` only when evidence supports it. Fabricated passes / zero-byte placeholders = FAIL CLOSED.

### Required artifacts — ALL under the SAME fresh `session_<UTC>/`, non-empty, `fclr_live_archive01_` infix MANDATORY

The gate's ladder-aware binder maps campaign `01` → infix `fclr_live_archive01_` (numberless `fclr_live_archive_*` names FAIL CLOSED):

- `fclr_live_archive01_source_registry_<UTC>.{json,md}` — enumeration, coverage-only selection, exact URLs, checksums, schemas, terms, rejections.
- `fclr_live_archive01_prereg_<UTC>.{json,md}` — outcome-blind design, hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`.
- `fclr_live_archive01_eval_<UTC>.{py,json,md}` — heavy 3-block confirmatory evaluation triad on downloaded archive data.
- `fclr_live_archive01_recompute_<UTC>.{py,json}` — independent stdlib recompute, `all_checks_match:true`.
- `fclr_live_archive01_evidence_audit_<UTC>.{json,md}` — evidence/leakage audit with `audit_pass` + `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — gate-critical alias (substantive, verdict matches the evidence audit).
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.

Every JSON must carry `experiment_id:"FCLR-LIVE-ARCHIVE-01"` and the real `session_id` (or `session_utc`). Use `session_<UTC>` as a literal placeholder in this handoff; the real session id is the directory you create.

---

## 6. Precise Command/Check to Verify Progress

```bash
# After the artifacts exist under the new session_<UTC>/:
python3 scripts/check_handoff_heavywork_gate.py --json
# Expect: pass=true, reason_code=OK, live_archive.required=true, live_archive.pass=true,
#         live_archive.artifact_family="live_archive01", failures=[]

python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
  tests.test_vol_jump_campaign_gate \
  tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate \
  tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 \
  tests.test_active_campaign_gate
```

Gate-pass condition for the live-archive binder (from `scripts/check_handoff_heavywork_gate.py` `_live_archive_state`): the latest on-disk `session_<UTC>` must have UTC > `20261125T074500Z` and contain all 13 required files above, each non-empty, plus a non-empty `trigger_check_*.json`. `missing_required_artifacts` and `empty_required_artifacts` must both be `[]`.

---

## 7. Blockers & Next Materially Different Free Route

**No external blockers.** Enumeration, coverage, funding layout, download budget, dependency (stdlib-only), artifact-naming, and post-campaign-session-selection bottlenecks are all resolved (see §8).

**If any step fails** (e.g., an index-price month missing for the premium feature): do NOT silently substitute or zero-fill. Record the exact shortfall in the source registry/evidence audit, emit the evaluation with the available feature set, and note the deviation. Missing features remain missing.

**Do NOT** re-run FCLR-009 or any closed volatility arm, re-open sealed holdouts, modify the frozen protocol, build a risk overlay, threshold-shop, wait for an observed-liquidation trigger, or relabel exploratory work as confirmatory. If the 2% floor is not met, preserve `NOT_SUPPORTED` — a null is a valid, publishable result.

---

## 8. Bottlenecks Removed (do not re-introduce)

- **RESOLVED — stale handoff misroute:** the prior live handoff pointed to completed FCLR-009; this file re-anchors to the active rank-0 campaign. Following the stale version would fail the gate closed.
- **RESOLVED — symbol enumeration/ranking:** S3 delimiter catalog is the only enumeration path (1,080 symbols; 77 with 48/48 months); top five frozen outcome-blind. The 404/JavaScript-only/CDN/GitHub paths are explicitly rejected.
- **RESOLVED — five-source coverage:** all 25 symbol/source pairs have 48/48 months, zero missing, one `.CHECKSUM` sidecar per zip, non-truncated listings (verified live 2026-11-26T01:04:39Z–01:05:14Z).
- **RESOLVED — funding layout mismatch:** funding objects are `fundingRate/<SYMBOL>/<SYMBOL>-fundingRate-YYYY-MM.zip` (no `1h/`); direct 2024-01 key HTTP 200.
- **RESOLVED — download budget:** 1,200 zips + 1,200 checksums + ≤25 probes < 3,000 requests, ≤2 GiB.
- **RESOLVED — dependency installs:** stdlib-only required artifacts remove numpy/pandas/pyarrow install failures.
- **RESOLVED — artifact-naming deadlock:** every required artifact uses the `fclr_live_archive01_` infix the gate's ladder-aware binder demands.
- **RESOLVED — root churn:** root `research_state/*.md|*.json` = 500/500 (AT CAP, fixed 2026-11-25T16:55:00Z). All new artifacts MUST go under `session_<UTC>/`; no root-level additions.
- **RESOLVED — grandfathered escape hatch:** the latest on-disk session `session_20261125T060000Z` predates the campaign start and is GRANDFATHERED (gate `live_archive.required=false` today). Using it would be verify-and-stop, not progress. The next session MUST create a FRESH `session_<UTC>/` with UTC > `20261125T074500Z` and populate it fully — never extend, reuse, or recreate `session_20261125T060000Z/`.
- **OPEN — execution:** the next session must download, freeze, evaluate, recompute, audit, and record the real session id without stopping at a probe, prereg, or audit.

---

## 9. NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- A timestamp-only rewrite is NOT progress and is forbidden as the next session's deliverable. The next session must materialize the heavy evaluation and recompute artifacts.
- Campaign start `20261125T074500Z` is in the past. Any new `session_<UTC>` immediately requires the full `fclr_live_archive01_*` set. There is no grace session and no verify-and-stop branch.
- Do NOT create a partial/empty session and leave it unrecorded. If you create `session_<UTC>/`, populate it fully and record its real id in this handoff after the artifacts exist. Do NOT write a future/non-existent session id (the gate fails `HEAVY_SESSION_DIR_MISSING` if the handoff's latest session id is not an existing directory).
- Root `research_state/*.md|*.json` is at 500/500 (AT CAP). All new artifacts go under `session_<UTC>/`.
- No empty files or zero-byte placeholders. JSON must be strict RFC 8259 and carry `experiment_id:"FCLR-LIVE-ARCHIVE-01"` plus the real `session_id`.
- Stdlib only for this campaign. No `pip install`; no numpy/pandas/pyarrow/requests in required artifacts.
- Do NOT modify `.github/workflows` or overwrite sealed prereg/eval artifacts, including `research_state/research_protocol.md` and `research_state/evaluation_summary_FCLR-009.md`.
- The ONLY timestamped campaign id permitted in this file is `FCLR-LIVE-ARCHIVE-01-20261125T074500Z`. Refer to closed campaigns by name only; another timestamped id would activate its binder and fail later sessions closed.

---

## 10. STATE OF THE WORK (read before acting)

- **Half 1 (funding-conditioned volatility), frozen `ironflow_bulk` panel:** exhausted NOT_SUPPORTED — BROAD-01 (mean QLIKE 1.93% < 2%), CORR-01 (correction-time/hazard), STRESS-01 (1.51%), JUMP-01/02/03/04 (magnitude+direction ≤0.30%).
- **Half 2 (liquidation risk), frozen panel:** exhausted — Track A structurally blocked; Track B/C not supported; cross-sectional not stable + floor not met.
- **FCLR-009 (2025 5-coin panel):** CLOSED NOT_MET (2026-11-10). Do not reopen.
- **Program closure:** completed under `session_20261125T060000Z` (name-only campaign, negative results preserved). Do not rerun.
- **Forecast gate (§9):** NOT PASSED. Risk overlay ineligible.
- **Root churn:** 500/500 (at cap, fixed 2026-11-25T16:55:00Z); nested session storage only going forward.

---

## 11. ON-DISK INPUTS (verified — do not re-derive)

| Path | Description |
|---|---|
| `research_state/experiment_frontier.json` | Rank-0 = live-archive campaign, READY_EXECUTE, full frozen design + verified roots. |
| `research_state/data_cache/ironflow_bulk/` | Frozen 18-month reference panel; read-only, NOT for new confirmatory work. |
| `research_state/session_20261125T060000Z/` | Latest complete closure session; GRANDFATHERED (predates campaign); historical evidence only — do NOT reuse. |
| `research_state/session_20261122T013000Z/` | Earlier live-archive campaign-02 set; historical evidence only — do NOT reuse or extend. |
| `research_state/negative_results_report.md` | Preserved nulls and failed routes. |
| `research_state/evaluation_summary_FCLR-009.md` | Proof FCLR-009 closed NOT_MET; do not reopen. |
| Binance monthly archive roots (§5.2) | Frozen cohort; all 25 source pairs 48/48 months, checksums present; exact S3 pattern and 2021–2024 scope frozen. |

Each downloaded zip must be checked against its `.CHECKSUM`; record URL, access time, status, byte count, SHA256, schema, coverage. Do not mutate frozen caches.

---

## 12. KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3/§7/§8/§9/§14/§16/§17/§19/§20 — hypothesis, features, leakage controls, starter model, adaptive feasibility, promotion, status contract.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` / `LIVE_ARCHIVE_REQUIRED` ladder-aware binder (campaign `01` → `fclr_live_archive01_`).
- `research_state/experiment_frontier.json` — rank-0 registry.
- `handoff_archive/AGENT_HANDOFF_20261126T015039Z.md` — accurate prior handoff (frozen cohort provenance).

---

## 13. SESSION CLOSE-OUT — 2026-11-26T01:56:21Z

**What changed and why (reconciliation + handoff repair, not new research):**
- Reconciled the durable handoff to on-disk truth: the prior live handoff (01:53:15Z) wrongly pointed to already-completed FCLR-009; this file re-anchors to the active rank-0 campaign FCLR-LIVE-ARCHIVE-01 and records the FCLR-009 closure evidence.
- Froze the next-session routing: exact cohort, S3 monthly source patterns, request budget, stdlib-only deps, splits/models/inference, `fclr_live_archive01_` artifact contract, and gate verification commands.

**What was actually tested:**
- `python3 scripts/check_handoff_heavywork_gate.py --json` → `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.required=false` (latest on-disk session `session_20261125T060000Z` predates campaign start `20261125T074500Z` and is GRANDFATHERED), `live_archive.pass=true`.
- Root `research_state/*.md|*.json` count = 500/500 (at cap).
- `research_state/experiment_frontier.json` rank-0 = `FCLR-LIVE-ARCHIVE-01-20261125T074500Z`, status `READY_EXECUTE`.
- No `fclr_live_archive01_*` artifact exists on disk (campaign genuinely unexecuted).

**Evidence added:** this handoff only; exact cohort, URLs/layout, request budget, artifact contract, and current gate state are now durable and correct.

**Current gate state:** `live_archive.required=false` ONLY because the latest on-disk session predates the campaign. **The next session with UTC > `20261125T074500Z` must have `live_archive.required=true`, `live_archive.pass=true`, and the complete non-empty `fclr_live_archive01_*` set.**

**Single highest-value next task:** execute the full FCLR-LIVE-ARCHIVE-01 artifact set in one fresh `session_<UTC>/` (UTC > `20261125T074500Z`) using the frozen cohort exactly as specified in §5.

**Source/engineering blockers:** none external. Enumeration, coverage, funding layout, download budget, dependency, artifact-naming, root-cap, and post-campaign-session-selection bottlenecks are resolved.

---

## 14. RESEARCH_PROMPT.md §19 ANSWERS (this session — 2026-11-26T01:56:21Z)

**What did the evidence support, contradict, or leave unknown?**
- Supported: the frozen panel is exhausted; the Binance monthly archive is reachable without authentication through the verified S3 catalog and direct S3 keys; a five-symbol, four-year monthly design fits the request budget.
- Contradicted: the stale claim that FCLR-009 was unfinished (it is closed NOT_MET); and the claim that no bounded heavy new-source design is executable.
- Unknown: whether funding + price features clear the 2% QLIKE floor on the new archive cohort.

**Strongest alternative explanation:** the frozen-panel nulls may reflect limited regime diversity and an 18-month sample; the 2021–2024 archive adds four years and multiple market regimes.

**Dominant limitation:** new-source data coverage and leakage-resistant inference; the next campaign audits both before producing a verdict.

**Concrete falsification test:** a paired 3-block QLIKE evaluation in which C2 beats B1 by <2% relative or the uncertainty interval does not support the floor preserves `NOT_SUPPORTED`; a stable, calibrated, multi-symbol improvement of ≥2% reopens promotion review.

**Highest information gain per free compute:** FCLR-LIVE-ARCHIVE-01, because it tests the repo-name-leading estimand on a materially broader source with bounded downloads and a fixed model.

**Exact artifact and command demonstrating progress:** one complete `research_state/session_<UTC>/` with every required artifact in §5; `python3 scripts/check_handoff_heavywork_gate.py --json` must return `reason=OK` with `live_archive.required=true` and `live_archive.pass=true`, followed by the six-module unittest command in §6.

**Latest completed session:** session_20261125T060000Z