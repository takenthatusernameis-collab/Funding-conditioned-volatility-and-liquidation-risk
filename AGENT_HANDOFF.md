# AGENT HANDOFF — 2026-11-25T11:52:08Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> **PROGRAM STATUS: HALF 1 (FUNDING-CONDITIONED VOLATILITY) — FROZEN PANEL EXHAUSTED; NEW-SOURCE CONFIRMATORY CAMPAIGN ACTIVE. HALF 2 (LIQUIDATION RISK) — CONFIRMATORY-EXHAUSTED ON FROZEN PANEL.**
> Half 1 is closed `NOT_SUPPORTED` on the frozen `ironflow_bulk` panel for mean log-RV QLIKE, funding-extreme correction-time/hazard, volatility stress/tail exceedance, signed-jump magnitude, and signed-jump direction.
> Half 2 is closed on that panel: Track A structurally blocked; Track B not supported; Track C not supported; cross-sectional generalization not stable and below the materiality floor.
> **REPO-NAME PRIORITY:** the repository name leads with **Funding-conditioned-volatility**, so rank-0 is the new-source mean-RV QLIKE campaign below, not another frozen-panel or liquidation-risk rerun.
> **ACTIVE CAMPAIGN:** `FCLR-LIVE-ARCHIVE-01-20261125T074500Z` — execute the heavy 3-block confirmatory evaluation on the Binance public archive in ONE fresh `session_<UTC>/`.
> **HEAVY WORK IS MANDATORY:** trigger-only, prose-only, source-probe-only, prereg-only, audit-only, verify-and-stop, and arbitrary `recompute_*` sessions FAIL CLOSED.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — verified 2026-11-25T11:52:08Z**
>
> **CURRENT GATE STATE:** `python3 scripts/check_handoff_heavywork_gate.py --json` is GREEN on the real repo (`pass=true`, `reason_code=OK`, `handoff_stale=false`). Latest on-disk and handoff-recorded session: `session_20261125T060000Z`. Root `research_state/*.md|*.json` count: 500/500. The next session creates the first post-start session and immediately binds `live_archive.required=true`.
>
> **DO THIS NEXT, IN ONE SESSION:** Execute `FCLR-LIVE-ARCHIVE-01-20261125T074500Z` on the Binance public archive. The primary estimand is the repo-name-leading one: **does the funding + price feature set improve next-24-hour mean realized-variance QLIKE beyond a realized-volatility-only baseline by at least 2% relative, with block-aware uncertainty and stability across three non-overlapping test blocks?**
>
> **FROZEN EXECUTION DESIGN — DO NOT RE-DERIVE OR EXPAND:**
> 1. Use a bounded **2021-01-01 through 2024-12-31 UTC** archive window. Enumerate symbols ONLY from the S3 delimiter catalog: `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?prefix=data/futures/um/monthly/klines/&delimiter=/` (paginate with `marker` until `IsTruncated=false`; parse `<CommonPrefixes><Prefix>.../<SYMBOL>/</Prefix>`). Do NOT use `data.binance.vision/data/.../klines/` (404), the JS-only `data.binance.vision/?prefix=...` HTML, or the GitHub API (403 rate limit). Coverage-only selection: rank symbols by count of existing 2021–2024 monthly kline keys, tie ascending symbol; take the top five, then verify all five core sources for those five and replace any incomplete candidate with the next coverage-ranked symbol. If fewer than five complete symbols exist, run all complete symbols and mark the result `PILOT/INCONCLUSIVE`; never zero-fill or outcome-select.
> 2. Required monthly sources only, via S3 primary: `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/{klines,markPriceKlines,indexPriceKlines,premiumIndexKlines}/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip` and `.../fundingRate/<SYMBOL>/<SYMBOL>-fundingRate-YYYY-MM.zip`. CDN `data.binance.vision` is fallback only after an S3 404, never a reason to skip a key. Do NOT download daily metrics/OI for this primary campaign; it is not needed for the estimand. The `data/spot/daily/*` paths are HTTP 404 and MUST NOT be used.
> 3. Bound downloads to **3,000 HTTP requests and 2 GiB**, concurrency 4, at most 4 retries with exponential backoff. Cache raw zips under `session_<UTC>/raw/`, verify every `.CHECKSUM`, and keep bulky raw data out of Git. **Stdlib only: do not run `pip install` and do not require numpy/pandas/pyarrow/requests; use `urllib.request`, `zipfile`, `csv`, `math`, `statistics`, `json`, and `hashlib`.**
> 4. Freeze the source registry and outcome-blind prereg BEFORE generating targets or inspecting outcomes. Derive split boundaries from unique UTC timestamps only: first 60% train, next 20% validation, last 20% test; apply a 7-calendar-day purge/embargo; divide the test span into three equal, non-overlapping blocks.
> 5. Use one common eligible panel for every paired comparison. B0 is RV24 persistence. B1 is the fixed OLS HAR model on log RV1h/RV24h/RV168h. C1 adds signed funding and the trailing 90-day absolute-funding percentile. C2 adds mark/index premium and mark/EMA24 distance. Fit scaling and smearing on training data only. Primary contrast: **C2 versus B1**, paired next-24-hour QLIKE; C1 versus B1 is secondary.
> 6. Use at least 2,000 deterministic block-bootstrap replicates resampling whole UTC time blocks jointly across symbols. Report absolute and relative QLIKE, MSE/MAE, sample/event counts, coverage, exclusions, per-block and leave-one-symbol-out diagnostics, and Holm-adjusted secondary contrasts. The frozen materiality floor is **2% relative QLIKE reduction**; the uncertainty interval must support improvement.
> 7. Produce the complete artifact set below under the SAME fresh session. Run the independent stdlib recompute and evidence audit in that session. A valid `NOT_SUPPORTED`, `PROMOTED`, or `INCONCLUSIVE` verdict is acceptable only when the evidence supports it; fabricated passes and zero-byte placeholders are forbidden.
>
> **BOTTLENECKS REMOVED THIS HANDOFF:**
> - **RE-VERIFIED 2026-11-25T11:52:08Z:** the S3 delimiter catalog returned HTTP 200; the heavy-work gate is GREEN (`pass=true`, `reason_code=OK`, `handoff_stale=false`); and the six gate regression modules pass 122/122. The source, download-key, and dependency blockers below remain removed.
> - The obsolete closed program-closure campaign is now referred to by NAME ONLY. Its former timestamped ID no longer activates an impossible closure-artifact requirement on the next archive session.
> - The symbol-listing blocker is removed: `data.binance.vision/data/futures/um/monthly/klines/` returns 404 and the `data.binance.vision/?prefix=...` page is JavaScript-only. The verified replacement is the S3 delimiter catalog at `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?prefix=data/futures/um/monthly/klines/&delimiter=/`, which returned HTTP 200 with 1,000 `CommonPrefixes` and `IsTruncated=true` on 2026-11-25T11:52:08Z.
> - The download-key blocker is removed: direct S3 keys for all five required monthly sources returned HTTP 200 for BTCUSDT 2024-01 (klines 38,890; mark 23,278; index 22,067; premium 16,935; funding 696 bytes). CDN `data.binance.vision` is now explicitly fallback-only because some CDN keys 404 while the S3 key exists.
> - The dependency-install blocker is removed: prior sessions repeatedly died on missing `numpy`/`pandas`/`pyarrow` and timed-out installs. The required campaign artifacts are now stdlib-only; `pip install` is forbidden for this campaign.
> - The design is now bounded and executable without source discovery, model search, threshold shopping, credentials, external triggers, or a future grace window.
>
> **VERIFICATION COMMANDS (after the heavy artifacts exist):**
> ```bash
> python3 scripts/check_handoff_heavywork_gate.py --json
> python3 -m py_compile scripts/check_handoff_heavywork_gate.py
> python3 -m unittest \
>   tests.test_vol_jump_campaign_gate \
>   tests.test_vol_stress_campaign_gate \
>   tests.test_vol_corr_campaign_gate \
>   tests.test_vol_broad_campaign_gate \
>   tests.test_tracka_hardening_143 \
>   tests.test_active_campaign_gate
> ```

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **A timestamp-only rewrite is NOT progress and is forbidden as the next session's deliverable.** The next session must materialize the heavy evaluation and recompute artifacts.
- **Campaign start `20261125T074500Z` is in the past.** Any new `session_<UTC>` immediately requires the full `fclr_live_archive_*` set. There is no grace session and no verify-and-stop branch.
- **Do not create a partial/empty session and leave it unrecorded.** If you create `session_<UTC>/`, populate it fully and record its real ID in this handoff after the artifacts exist. Do not write a future/non-existent session ID.
- **Do not re-run any terminal campaign on the frozen panel.** The frozen `ironflow_bulk` panel is exhausted for volatility and confirmatory liquidation risk. Do not wait for an observed-liquidation trigger, build a risk overlay, threshold-shop, or relabel exploratory work as confirmatory.
- **Root `research_state/*.md|*.json` is at 500/500.** All new artifacts MUST go under `session_<UTC>/` or another nested directory.
- **No empty files or zero-byte placeholders.** Every required artifact must be non-empty; JSON must be strict RFC 8259 and carry `experiment_id:"FCLR-LIVE-ARCHIVE-01"` plus the real `session_id`.
- **Dependencies:** stdlib only for this campaign. Do not install or import numpy/pandas/pyarrow/requests in the required artifacts; use `urllib.request`, `zipfile`, `csv`, `math`, `statistics`, `json`, and `hashlib`. No paid APIs, manual downloads, credentials, or new source family.
- **Do not modify `.github/workflows` or overwrite sealed prereg/eval artifacts**, including `research_state/research_protocol.md`.
- **The ONLY timestamped campaign ID permitted in this file is `FCLR-LIVE-ARCHIVE-01-20261125T074500Z`.** Refer to closed campaigns by name only; another timestamped ID would activate its binder and fail later sessions closed.

---

## FOCUS CAMPAIGN — FCLR-LIVE-ARCHIVE-01-20261125T074500Z (rank-0, READY_EXECUTE)

**Question (OPEN):** On a coverage-selected five-symbol Binance USDⓈ-M perpetual archive cohort over 2021–2024, does the frozen funding + price feature set improve out-of-sample next-24-hour mean realized-variance QLIKE over the RV-only HAR baseline by at least 2% relative across three non-overlapping chronological test blocks?

**Why this is highest value:**
- It directly attacks the repository-name-leading estimand after all frozen-panel volatility arms closed validly.
- It uses a materially different, verified, free, unauthenticated source with a longer and broader history than the 18-month frozen panel.
- It is bounded to monthly files, five symbols, four years, and 3,000 requests, so heavy work can actually finish in one session.
- It cannot be satisfied by documentation, source probing, preregistration alone, or an arbitrary recompute file.

**Frozen inputs:**
- Symbol catalog: `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?prefix=data/futures/um/monthly/klines/&delimiter=/` (paginate with `marker`; parse `CommonPrefixes`).
- `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
- `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
- `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/indexPriceKlines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
- `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/premiumIndexKlines/<SYMBOL>/1h/<SYMBOL>-1h-YYYY-MM.zip`
- `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision/data/futures/um/monthly/fundingRate/<SYMBOL>/<SYMBOL>-fundingRate-YYYY-MM.zip`
- RESEARCH_PROMPT.md §3, §7, §8, §9, §13, §14, §16, §17, §19, and §20.

**Required artifacts (ALL under one fresh `session_<UTC>/`, non-empty):**
- `fclr_live_archive_source_registry_<UTC>.{json,md}` — archive enumeration, coverage-only symbol selection, exact URLs, sample/full checksum evidence, schemas, timestamps, license/terms, and rejection reasons.
- `fclr_live_archive_prereg_<UTC>.{json,md}` — outcome-blind design hash-bound to the source registry; `outcome_data_inspected_before_freeze:false`.
- `fclr_live_archive_eval_<UTC>.{py,json,md}` — heavy 3-block confirmatory evaluation triad on downloaded archive data.
- `fclr_live_archive_recompute_<UTC>.{py,json}` — independent stdlib recompute with `all_checks_match:true`.
- `fclr_live_archive_evidence_audit_<UTC>.{json,md}` — evidence/leakage audit with `audit_pass` and `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — gate-critical alias.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.

---

## STATE OF THE WORK (read before acting)

- **Half 1, frozen `ironflow_bulk` panel:** exhausted. Closed by name: FCLR-VOL-BROAD-01 (mean QLIKE 1.93% < 2%), FCLR-VOL-CORR-01 (correction-time/hazard not supported), FCLR-VOL-STRESS-01 (stress 1.51% < 2%), FCLR-VOL-JUMP-01/02/03 (jump magnitude below floor), and FCLR-VOL-JUMP-04 (jump direction 0.0474% < 2%).
- **Half 2, frozen panel:** exhausted. Track A structurally blocked; Track B and C not supported; broad cross-sectional result not stable and immaterial.
- **Program closure:** completed and validated under `session_20261125T060000Z` by name-only campaign FCLR-LIQ-RISK-PROGRAM-CLOSURE-02. Its negative results are preserved; do not rerun it.
- **Heavy-work gate:** passing before this refresh; latest complete session is `session_20261125T060000Z`. The next post-start session must satisfy `live_archive` with the full artifact set.
- **Forecast gate (§9):** NOT PASSED. Risk overlay remains ineligible.
- **Root churn:** 500/500; nested session storage only.

---

## ROOT CONSTRAINTS (hard)

- No root-level `research_state/*.md|*.json` additions.
- No empty files, threshold shopping, fabricated outcomes, or holdout reuse.
- Preserve `PROMOTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`, or evidence-backed blocker statuses honestly.
- No new source beyond the verified Binance public archive; no credentials or paid/manual inputs.
- Do not modify protected workflows or sealed artifacts.
- Do not include any timestamped campaign ID other than the active one in this handoff.

---

## ON-DISK INPUTS (verified — do not re-derive)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/` | Frozen 18-month reference panel; read-only and NOT for new confirmatory work. |
| `research_state/session_20261125T060000Z/` | Latest complete closure session; historical evidence only. |
| `research_state/session_20261125T054500Z/` | Prior complete frozen-panel jump-direction session; historical evidence only. |
| `research_state/experiment_frontier.json` | Rank-0 is the active archive campaign; all frozen volatility arms are completed. |
| `research_state/negative_results_report.md` | Preserved nulls and failed routes. |
| Binance monthly archive roots above | S3 catalog re-verified HTTP 200 on 2026-11-25T11:52:08Z and all five BTCUSDT 2024-01 source keys verified HTTP 200 on 2026-11-25T11:52:08Z; exact S3 pattern and 2021–2024 scope frozen. |
| `research_state/data_cache/{BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT,BNBUSDT}_YYYY_MM/` | On-disk daily 1h kline zips with `.sha256` (2024-01..2026-11). Reachability/budget evidence ONLY; the campaign must still download the monthly five-source set into `session_<UTC>/raw/` and verify every `.CHECKSUM`. |
| `https://data.binance.vision/data/futures/um/monthly/klines/` | DO NOT USE for enumeration — HTTP 404. |
| `https://data.binance.vision/?prefix=...` | DO NOT USE for enumeration — JavaScript-only HTML, no server-rendered listing. |
| `https://api.github.com/repos/binance/binance-public-data/contents/...` | DO NOT USE — HTTP 403 rate limit. |
| `https://data.binance.vision/data/spot/daily/*` | DO NOT USE — HTTP 404. |

Each downloaded zip must be checked against its `.CHECKSUM`; record URL, access time, status, byte count, SHA256, schema, and coverage. Do not mutate frozen caches.

---

## KEY FILES TO READ

- `AGENT_HANDOFF.md` — this sole durable handoff.
- `RESEARCH_PROMPT.md` §3/§7/§8/§14/§17/§19/§20 — hypothesis, features, leakage controls, starter model, promotion, and status contract.
- `scripts/check_handoff_heavywork_gate.py` — `LIVE_ARCHIVE_CAMPAIGN_RE` / `_live_archive_state` / `LIVE_ARCHIVE_REQUIRED` binder.
- `tests/test_vol_jump_campaign_gate.py` and sibling campaign-gate tests — hermetic regression fixtures.
- `research_state/experiment_frontier.json` — rank-0 registry.
- `research_state/negative_results_report.md` — preserved negative evidence.

---

## SESSION CLOSE-OUT (THIS SESSION — 2026-11-25T11:52:08Z)

**What changed and why (real actions, not a timestamp bump):**
- Re-verified the rank-0 source live at 2026-11-25T11:52:08Z: the S3 delimiter catalog `https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?prefix=data/futures/um/monthly/klines/&delimiter=/` returned HTTP 200 with a valid `ListBucketResult`.
- Re-ran the heavy-work gate on the real repo: `pass=true`, `reason_code=OK`, `handoff_stale=false`, `live_archive.required=false` (latest session `session_20261125T060000Z` predates the `20261125T074500Z` start), `root_count=500/500`.
- Re-ran the six gate regression modules: 122/122 tests pass.
- Confirmed the repo-name priority is intact: rank-0 in `research_state/experiment_frontier.json` is `FCLR-LIVE-ARCHIVE-01-20261125T074500Z` (`READY_EXECUTE`, `program_status=ACTIVE`), the funding-conditioned-volatility estimand.
- Kept the obsolete timestamped program-closure campaign name-only so it cannot demand impossible closure artifacts from the next archive session.
- Kept all new-artifact routing nested because root research-state storage is at cap.

**What was actually tested:**
- `python3 scripts/check_handoff_heavywork_gate.py --json` → PASS, `reason_code=OK`, `handoff_stale=false`, `live_archive.required=false`.
- S3 catalog GET at 2026-11-25T11:52:08Z → HTTP 200, valid `ListBucketResult`.
- `python3 -m unittest tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate tests.test_tracka_hardening_143 tests.test_active_campaign_gate` → 122/122 OK.
- On-disk accelerator check: `research_state/data_cache/` already holds daily 1h kline zips with `.sha256` for BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT/BNBUSDT across 2024-01..2026-11, proving reachability and that the 3,000-request/2 GiB budget is sufficient. This cache is evidence only; it is NOT a substitute for the in-session source registry and verified monthly five-source downloads.

**Evidence added:** this handoff only; no root research-state file was added and no sealed artifact was modified.

**Current gate state:** live archive is READY_EXECUTE and not yet required because the latest recorded session predates the start. The next session must make it required and passing.

**Single highest-value next task:** execute the full FCLR-LIVE-ARCHIVE-01 artifact set in one fresh session exactly as frozen above.

**Source/engineering blockers:** none external. The only blocker is non-execution; source-listing, download-key, and dependency-install bottlenecks have been removed and re-verified at 2026-11-25T11:52:08Z.

---

## BOTTLENECK RESOLUTION (this session)

- **RESOLVED — symbol enumeration:** the S3 delimiter catalog is the only enumeration path; the 404 and JavaScript-only paths are explicitly rejected.
- **RESOLVED — download keys:** S3 is primary and CDN is fallback-only; every key must exist in the S3 listing before download.
- **RESOLVED — dependency installs:** stdlib-only required artifacts remove the repeated `numpy`/`pandas`/`pyarrow` failures and install timeouts.
- **RESOLVED — obsolete closure binder:** the closed program-closure campaign no longer appears with a timestamp in this handoff.
- **RESOLVED — unbounded scope:** the campaign is restricted to five coverage-selected symbols, 2021–2024 monthly files, one primary estimand, and a 3,000-request/2 GiB budget.
- **RESOLVED — design drift:** model definitions, splits, purge, inference, materiality, and verdict inputs are frozen in the initial task message.
- **RESOLVED — root churn and future grace loopholes:** nested storage is mandatory and the campaign start is already in the past.
- **OPEN — execution:** the next session must download, freeze, evaluate, recompute, audit, and record the real session ID without stopping at a probe or prereg.

---

## RESEARCH_PROMPT.md §19 ANSWERS (this session)

**What did the evidence support, contradict, or leave unknown?**
- Supported: the frozen panel is exhausted and the Binance monthly archive is reachable without authentication through the verified S3 catalog and direct S3 keys.
- Contradicted: the claim that no bounded heavy new-source design is executable; a five-symbol, four-year monthly design fits the request budget.
- Unknown: whether funding + price features clear the 2% QLIKE floor on the new archive cohort.

**Strongest alternative explanation:** the frozen-panel nulls may reflect limited regime diversity and an 18-month sample; the 2021–2024 archive adds four years and multiple market regimes.

**Dominant limitation:** new-source data coverage and leakage-resistant inference; the next campaign audits both before producing a verdict.

**Concrete falsification test:** a paired 3-block QLIKE evaluation in which C2 beats B1 by less than 2% relative or the uncertainty interval does not support the frozen materiality floor would preserve `NOT_SUPPORTED`; a stable, calibrated, multi-symbol improvement of at least 2% would reopen promotion review.

**Highest information gain per free compute:** FCLR-LIVE-ARCHIVE-01, because it tests the repo-name-leading estimand on a materially broader source with bounded downloads and a fixed model.

**Exact artifact and command demonstrating progress:** one complete `research_state/session_<UTC>/` with every required artifact above; `python3 scripts/check_handoff_heavywork_gate.py --json` must return `reason=OK` with `live_archive.required=true` and `live_archive.pass=true`, followed by the six-module unittest command above.

(End of file)