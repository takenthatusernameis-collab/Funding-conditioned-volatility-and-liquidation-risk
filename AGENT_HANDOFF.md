# AGENT HANDOFF — 2026-11-19T19:06:54Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file under `research_state/` is tombstoned/historical and has no campaign authority. Verified this refresh: exactly one `AGENT_HANDOFF*` exists in the repo.
> **Refresh kind:** maintenance refresh — **campaign 13 is still LIVE and unexecuted**. No session directory newer than `session_20261119T180650Z` exists on disk and none is recorded here. Campaign numbering is therefore **not** bumped in this refresh; the next (post-RISK-13) refresh bumps to RISK-14.
> **Repo priority:** the repository is `Funding-conditioned-volatility-and-liquidation-risk`. The funding-level and funding-shock transmission families are closed (RISK-11 NOT_MET-with-bound; RISK-12 UNDERPOWERED). The highest-value unexecuted, repo-name-aligned work is the **liquidation-risk pillar**: the **RISK-13** campaign — an outcome-blind, pre-registered confirmatory test of the **liquidation-hazard persistence family (`liq_count` state)** on the frozen Track A panel. Do not substitute descriptive, audit, or re-split work.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T19:06:54Z)

**Campaign `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` is LIVE, fully specified, and machine-enforced. It has NOT been executed.** Your session is the RISK-13 session. There is no legal alternative task in this repo right now. Do not replay RISK-08/09/10/11/12, do not re-audit certified results, do not refresh the handoff instead of doing the work, and do not run a trigger-check-only or gate-only session.

The single deliverable, in this exact order:

1. `UTC=$(date -u +%Y%m%dT%H%M%SZ)`; create `research_state/session_$UTC/` (strictly > `20261119T185144Z`).
2. Write the **outcome-blind** prereg `fclr_risk13_prereg_$UTC.{json,md}` and freeze it **before** computing or touching any outcome. Use the exact RISK-13 contract below. Do not slim the 6-member family. Record `frozen_utc`, `outcome_blind=true`, the member table with declared directions, `blocks`, `metrics`, `placebo`, `multiplicity`, `common_sample_rule`, and `panel_sha256 = 0448a56a676eaadc7094d0e42a6b90a5f407a80502da0da74e5141547725e7d9`.
3. Emit `fclr_risk13_power_$UTC.{py,json,md}`. Recompute the MDE-by-instrument-count table from the **RISK-13 common sample only**; `PLAUSIBLE_EFFECT_BRIER = 0.001` stays frozen; `status` ∈ {`POWERED`,`UNDERPOWERED`}. Embed the sha256 of the frozen prereg in the power JSON.
4. Emit `fclr_risk13_recompute_$UTC.{py,json}`; require `n_discrepancies = 0`.
5. Emit `fclr_risk13_evaluation_$UTC.{py,json,md}`: per-block MDE-by-instrument-count table, preregistered decision, placebo p, Holm p, per-member coefficient signs vs declared directions, honest verdict.
6. Emit `evidence_audit_$UTC.{json,md}` (per `RESEARCH_PROMPT.md` §19) and `trigger_check_$UTC.json` (re-evaluate all 4 registry triggers).
7. Run every verification command in this file; all must PASS.
8. **Only then** update this handoff: record `session_$UTC`, bump the campaign to **RISK-14**, and set the RISK-14 start timestamp to the handoff refresh UTC (strictly greater than `$UTC`). See "Ladder rule".

`scripts/check_handoff_heavywork_gate.py` **fails closed for the session this handoff records** once that session's UTC is after the campaign start: the recorded session must contain the exact 11-file `fclr_risk13_*` package + non-empty `trigger_check_*.json`. A descriptive-only, trigger-check-only, gate-only, or arbitrary-`recompute_*` session cannot pass. Zero-byte artifacts fail. There is no cheaper legal session. A session dir that exists on disk but is not recorded here also fails (`HANDOFF_STALE_LATEST_SESSION`), so artifacts cannot be skipped by leaving the handoff stale.

**Forbidden starts:** RISK-09 replay, RISK-10 replay, RISK-11 replay, RISK-12 replay, `FCLR-LIQ-TRACKA-CONFIRMATORY-02` (precondition UNDERPOWERED; verdict was NOT_MET), `FCLR-LIQ-TRACKA-DATA-EXTENSION-02` (no post-`2026-10-31` labels with ≥100-day depth), RISK-05/06/07, ROBUST-05, Track C QLIKE replay, and reading sealed Binance months (`2024-10 … 2026-11`) for outcomes.

### ZERO-RAMP-UP START — copy-paste bootstrap (outcome-blind up to step 3)

```bash
UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
# Power template (port constants + features; see porting map):
cp research_state/session_20261119T180650Z/fclr_risk12_power_20261119T180650Z.py \
   research_state/session_$UTC/fclr_risk13_power_$UTC.py
# Recompute template:
cp research_state/session_20261119T180650Z/fclr_risk12_recompute_20261119T180650Z.py \
   research_state/session_$UTC/fclr_risk13_recompute_$UTC.py
# Evaluation template — USE RISK-11 (full IRLS fit + placebo + Holm), NOT RISK-12:
cp research_state/session_20261119T130817Z/fclr_risk11_evaluation_20261119T130817Z.py \
   research_state/session_$UTC/fclr_risk13_evaluation_$UTC.py
# Audit + trigger templates:
cp research_state/session_20261119T180650Z/trigger_check_20261119T180650Z.json \
   research_state/session_$UTC/trigger_check_$UTC.json
```

Then edit `SESSION`, `CAMPAIGN` (`FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z`), and the family/feature blocks per the porting map below. Do **not** run the copied scripts before the prereg is frozen.

### RISK-13 porting map (exact change points — do not re-derive)

| File (template → target) | Required edits |
|---|---|
| `fclr_risk12_power_*.py` → `fclr_risk13_power_*.py` | `SESSION`/`CAMPAIGN`; `FAMILY_MEMBERS` not used here; in `build_features` add `liq_count_lag_1h/8h/24h`, `liq_count_ma_8h/24h`, `liq_count_lag_1h_x_rv` (within coin, on `liq_count` ordered by `hour_utc`); **replace** the `funding_change_24h` requirement in `apply_common_sample` with `liq_count_lag_24h`; change output filename prefix to `fclr_risk13_power_`; add `prereg_sha256`. Keep `expected` panel-integrity constants unchanged (rows 113880, coins 13, months 12, `funding_rate_nonnull` 113880, `liq_count_nonnull` 113880, `open_interest_usd_nonnull` 113035). |
| `fclr_risk12_recompute_*.py` → `fclr_risk13_recompute_*.py` | Same feature/common-sample edits; change prefix to `fclr_risk13_recompute_`; assert `n_discrepancies == 0`. |
| `fclr_risk11_evaluation_*.py` → `fclr_risk13_evaluation_*.py` | `SESSION`/`CAMPAIGN`; replace `FAMILY_MEMBERS` with the RISK-13 six; replace `funding_lag`/`funding_change_*` derivations with the `liq_count` state family; swap the common-sample rule; replace the hardcoded `SMALLEST_DEFENSIBLE_EFFECT` constant with the value read from the RISK-13 power JSON (never reuse RISK-12's number); keep IRLS/log-loss/AUC/calibration, 1000 label-hour permutations seed `20261119`, Holm over family × {block_2, block_3, pooled} at α=0.05; change output prefixes to `fclr_risk13_evaluation_`. |
| `trigger_check_*.json` | `campaign_id`, `session_utc`; re-verify the 4 registry predicates (below). |
| `evidence_audit_*.{json,md}` | Mirror the RISK-12 schema; campaign/session/verdict/family/MDE table/member verdicts/artifacts list. |

---

## RISK-13 CAMPAIGN CONTRACT — liquidation-hazard persistence family (`liq_count`-at-`t-1` state)

Family name: **`liquidation-hazard persistence family (liq_count state)`**; `n_family_members = 6`; no slimming.

### Frozen derivations (same panel, same outcome, same blocks)

- Input (only): `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` (113,880 coin-hours, 13 coins, 12 complete months `2025-11 … 2026-10`, verdict ADMISSIBLE, sha256 `0448a56a676eaadc7094d0e42a6b90a5f407a80502da0da74e5141547725e7d9`).
- Outcome: `y = 1 if liq_count >= 1 else 0` per (coin, hour). A zero means "no event observed in the feed", not a confirmed no-liquidation hour — repeat this caveat in every outcome artifact.
- `ret_t = ln(close_t / close_{t-1})` within coin, ordered by `hour_utc`.
- `rv_lag` = `statistics.stdev` of the trailing **24** hourly log returns ending at `t-1`.
- `funding_lag` = `funding_rate` at `t-1`; `premium_lag` = `premium` at `t-1`.
- `oi_change_lag` = `ln(open_interest_usd_{t-1} / open_interest_usd_{t-2})`; null if `t-2` missing.
- Liquidity-hazard state features (within coin, on `liq_count` ordered by `hour_utc`):
  - `liq_count_lag_1h = liq_count_{t-1}` (prior-hour observed liquidation count)
  - `liq_count_lag_8h = liq_count_{t-8}` (8-hour lag)
  - `liq_count_lag_24h = liq_count_{t-24}` (24-hour lag)
  - `liq_count_ma_8h = mean(liq_count_{t-8..t-1})` (trailing 8-hour mean)
  - `liq_count_ma_24h = mean(liq_count_{t-24..t-1})` (trailing 24-hour mean)
  - `liq_count_lag_1h_x_rv = liq_count_{t-1} * rv_lag` (prior-hour hazard amplified in high-RV)
  - If any required lagged `liq_count` observation is missing, the derived feature is null.
- **RISK-13 common-sample rule (binding):** drop a coin-hour for *all* models whenever any of `rv_lag`, `funding_lag`, `oi_change_lag`, `liq_count_lag_24h` is null (the 24h lag requires `t-24`, so it is the strictest requirement). All six members, the positive-control member, and RV-only are scored on the identical test rows.

### Family members (all added to the RV-only baseline; Holm family is declared here, before outcomes)

| id | term | declared direction |
|---|---|---|
| `member_1` | `funding_lag` (level) — positive control / replication anchor | no direction (prior campaigns found this not detectable at 0.001; it exists so the new state features are interpretable against the closed level result) |
| `member_2` | `liq_count_lag_1h` (prior-hour liquidation count) | > 0 |
| `member_3` | `liq_count_lag_8h` (8-hour lagged liquidation count) | > 0 |
| `member_4` | `liq_count_lag_24h` (24-hour lagged liquidation count) | > 0 |
| `member_5` | `liq_count_ma_24h` (trailing 24-hour mean liquidation count) | > 0 |
| `member_6` | `liq_count_lag_1h_x_rv` (prior-hour hazard × RV amplification) | > 0 |

Directional predictions are recorded but do **not** replace the two-sided decision rule; direction agreement is reported descriptively per member.

### Frozen design (mirror RISK-12; do not re-split)

- `block_1` test `2025-11-01..2025-12-31`, train none (cold-start anchor; power only).
- `block_2` test `2026-02-01..2026-04-30`, train `2025-11-01..2025-12-31`.
- `block_3` test `2026-06-01..2026-08-31`, train `2025-11-01..2026-01-31` (primary block for the headline claim).
- `pooled` test = block_2 + block_3 rows, train `2025-11-01..2026-01-31`.
- Purges `2026-01`, `2026-05`; reserve `2026-09..2026-10` untouched and never scored.
- Models: `intercept-only`, `RV-only` (`rv_lag`), `RV-only + each family member`.
- Metrics: Brier (headline), log-loss, AUC, calibration OLS slope/intercept on test probabilities.
- Placebo: permute test labels **within hour across coins** (label-hour permutation), 1000 permutations, fixed seed `20261119`; report empirical p and 95th percentile of the null Brier difference per member.
- Multiplicity: Holm over family = {member_1..member_6} × {block_2, block_3, pooled} at `alpha=0.05`, declared in the prereg before outcomes.
- Per-member verdict: SUPPORT iff block_3 Brier improvement > 0, `p_raw < 0.05`, `p_holm < 0.05`, and placebo 95th percentile < observed improvement; otherwise NOT_MET.
- Overall verdict: SUPPORT if any member passes; NOT_MET if all powered members fail; UNDERPOWERED if the power gate fails for all.

### Power gate (declare before evaluation)

- Recompute MDE from the **RISK-13 common sample** block sizes and panel base rate only (mirror `block_mde`/`mde_brier` in the power module). `PLAUSIBLE_EFFECT_BRIER = 0.001` stays frozen.
- MDE-by-instrument-count table (1–13 coins, fixed alphabetical order `BTC ETH BNB SOL XRP AVAX DOGE LINK SUI ARB OP APT ADA`) reproduced in the prereg. The RISK-12 smallest defensible effect `0.0028144136231997873` is a **reference only, not a hardcoded value**: `smallest_defensible_effect` must be recomputed and frozen from the RISK-13 power output before evaluation, under the rule *min `mde_brier_80pct` across scored blocks at full 13 coins (block_3 primary)*.
- If all scored blocks' `mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER`, `status=UNDERPOWERED`, `models_run=false`, and write the honest underpowered artifacts anyway (still all 11 files, still non-empty). Underpowered is still a full legal session.

### Definition of done (all must hold; gate + review)

| # | Requirement |
|---|---|
| 1 | New `research_state/session_<UTC>/` dir exists; UTC strictly greater than `20261119T185144Z` |
| 2 | `fclr_risk13_prereg_<UTC>.{json,md}` exist, non-empty; JSON has `frozen_utc`, `outcome_blind=true`, the 6-member family table above, `blocks`, `metrics`, `placebo`, `multiplicity`, `common_sample_rule`, `panel_sha256` |
| 3 | `fclr_risk13_power_<UTC>.{py,json,md}` exist, non-empty; JSON has explicit `status`, the MDE-by-instrument-count table, and `prereg_sha256` |
| 4 | `fclr_risk13_recompute_<UTC>.{py,json}` exist, non-empty; JSON has `n_discrepancies: 0` |
| 5 | `fclr_risk13_evaluation_<UTC>.{py,json,md}` exist, non-empty; JSON has per-block MDE-by-instrument table, preregistered decision, placebo p, Holm p, per-member signs, verdict |
| 6 | `evidence_audit_<UTC>.{json,md}` exist, non-empty, per `RESEARCH_PROMPT.md` §19 |
| 7 | `trigger_check_<UTC>.json` exists, non-empty, re-evaluates all 4 registry triggers |
| 8 | Every JSON embeds campaign id `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` and the session UTC |
| 9 | Verification block below passes end-to-end |
| 10 | Handoff updated only after 9 passes: your session id recorded, campaign bumped to RISK-14, new campaign start = handoff refresh UTC (> your session UTC) |

### Execution recipe

```bash
UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
# 1) prereg  -> freeze FIRST, hash it (sha256) into the power/evaluation JSON
# 2) power   -> require status=POWERED (or honest UNDERPOWERED with all 11 files)
# 3) recompute -> require n_discrepancies=0
# 4) evaluation -> verdict, MDE-by-instrument table, smallest-defensible-effect decision, per-member signs
# 5) evidence_audit + trigger_check
# 6) verification block, then handoff update (record session id; bump campaign to 14; start=now)
```

### Verification commands (all must PASS before touching this handoff)

```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 scripts/check_tracka_scope_registry_drift.py --json
python3 scripts/check_ironflow_cache_integrity.py --json
python3 -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v
python3 -m unittest discover -s tests -p 'test_tracka_*.py'
```

`check_ironflow_cache_integrity.py` is the mandatory data check: hash-only (stdlib `hashlib`), offline, no parquet content read, 48/48 objects OK. `scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10` is an **optional** extra when `pyarrow` is installed; do not let a missing `pyarrow`/`pandas` fail the session.

### Ladder rule (how the gate keeps biting without deadlocking)

The gate binds the artifact family `fclr_riskNN_*` to the **campaign number in this file**, and applies it to the **latest session id recorded in this file** once that session's UTC is after the campaign start. A handoff refresh that closes campaign N must: (a) record the just-finished session id, (b) bump the campaign to N+1, and (c) set the N+1 start timestamp to the **handoff refresh UTC**, which is strictly later than the finished session-dir UTC. The finished session is then grandfathered (`latest_utc <= campaign_start`) and the *next* session is bound to `fclr_risk(N+1)_*`. A **maintenance refresh** (this one) is the exception: it records no new session and keeps the campaign number and start unchanged, so the next session is still bound to `fclr_risk13_*`. Never bump the number while keeping an older start timestamp, and never leave campaign N as the active campaign once its package exists.

### Contingency ladder — pre-authorized heavy follow-ons (no idling allowed)

- **RISK-13 → any verdict:** if a new post-`2026-10-31` observed-label source appears (≥100-day depth), `HL_LABEL_EXTENSION` becomes eligible; refresh only via the `research_state/hl_label_extension_audit_<UTC>.{md,json}` contract. `GATE4_BRANCH_1` and `EXPANSION_ROBUSTNESS_REDO` remain external-trigger-only; never manufacture evidence for them.
- **If RISK-13 is UNDERPOWERED or NOT_MET:** do not silently repeat it. The next campaign must be a *distinct* mechanism on the frozen panel, pre-registered the same way. Candidate queue, in order: (i) within-hour cross-sectional funding-intensity contrast; (ii) UTC-hour / market-wide-RV conditioning of the funding effect; (iii) liquidation-hazard **state-transition** family (e.g. `liq_count` spike decay / survival hazard) — new mechanism only, never a re-split of RISK-13. Bump the campaign number per the ladder rule.
- **If RISK-13 is SUPPORT:** the next campaign is the preregistered replication/robustness of the supported member only (same direction, disjoint test window from `2026-09..2026-10` reserve at the earliest legal reuse), then a promotion review. Bump the campaign number per the ladder rule.

---

## CURRENT STATE (verified 2026-11-19T19:06:54Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; Track A exploratory COMPLETE; 12-month extension COMPLETE / ADMISSIBLE; Track A confirmatory COMPLETE, verdict **NOT_MET**; RISK-08 COMPLETE, verdict **NOT_MET** (POWERED, `n_discrepancies=0`); RISK-09 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`); RISK-10 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.0028); RISK-11 COMPLETE, verdict **NOT_MET-with-bound** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.002817725360790807); RISK-12 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.0028144136231997873); active campaign `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` (liquidation-hazard persistence family on the frozen panel), gate-enforced, data preflight PASS, **unexecuted**.
- **Latest session on disk:** `research_state/session_20261119T180650Z` — RISK-12 complete package (`fclr_risk12_prereg/power/recompute/evaluation` + `evidence_audit` + `trigger_check`), verdict UNDERPOWERED. This session predates the campaign-13 start and is grandfathered; the gate therefore reports `risk_08.required=false` until a post-start session exists. That is correct, not a bypass: the first post-`20261119T185144Z` session is bound to `fclr_risk13_*`.
- **Prior sessions:** `session_20261119T130817Z` (RISK-11, full IRLS fit + placebo + Holm — the evaluation template); `session_20261119T110653Z` (RISK-10); `session_20261119T095800Z` (RISK-09); `session_20261119T090239Z` (RISK-08 phase B/C bundle); `session_20261119T033443Z` (extension descriptive + audit + trigger check); `session_20261119T022824Z` (extension alignment ADMISSIBLE + confirmatory prereg + frozen panel).
- **Descriptive context (associational only):** 18.93% of coin-hours have ≥1 observed event (Wilson 95% CI 18.70%..19.16%); incidence rises monotonically across trailing-24h RV deciles (6.33% → 36.02%); funding deciles U-shaped (decile 4 16.36%, decile 10 22.90%).
- **Rank-0 triggers:** `NEW_OBSERVED_LIQUIDATION_SOURCE` = **FIRED**; `GATE4_BRANCH_1`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` = **OPEN**.
- **Root `research_state/` md+json count:** **498 / 500** (cap enforced by `test_tracka_hardening_125` and the gate). All new artifacts go under the new session dir. If a root registry must change, edit in place; never add.
- **Immutable:** `session_20261118T201919Z/*`, `session_20261118T132800Z/*`, `session_20261119T022824Z/*`, `session_20261119T033443Z/*`, `session_20261119T090239Z/*`, `session_20261119T095800Z/*`, `session_20261119T110653Z/*`, `session_20261119T130817Z/*`, `session_20261119T180650Z/*`.

### Bottlenecks removed (do not redo)

1. **Data bottleneck gone** — bulk cache `candles_1h,funding,open_interest,liquidations` covers `2025-11 … 2026-10`, 48/48 objects OK.
2. **Events bottleneck gone** — `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` covers `2025-05 … 2026-10`.
3. **Admissibility/extension bottleneck gone** — 12-month panel + ADMISSIBLE verdict frozen.
4. **Confirmatory-registration bottleneck gone** — three-block design, label contract, lags, models, metrics, placebo, Holm frozen.
5. **Empty-session / stale-handoff bottleneck gone** — gate compares newest on-disk session to handoff; handoff records `session_20261119T180650Z`.
6. **Confirmatory non-avoidance gate satisfied** by `session_20261119T095800Z` (RISK-09 evaluation, all six members NOT_MET under UNDERPOWERED).
7. **Escalation non-avoidance gate installed** — ladder rule bumps campaign number to bind artifact family (`fclr_risk13_*` for RISK-13).
8. **RISK-08/09 feature bottleneck removed** — panel already carries `funding_rate` (100% non-null) and `open_interest_usd` (99.26% non-null); RV is derivable from `close`; no ingest or parquet read required.
9. **Paired-sample trap removed** — binding common-sample rule keeps all comparisons vs RV-only on identical rows.
10. **Post-RISK-11 deadlock removed** — explicit ladder rule + three-way contingency ladder so no verdict leads to idling.
11. **RISK-11 verdict finalized** — NOT_MET-with-bound; RISK-12 fully specified and executed.
12. **Environment + registry drift bottleneck removed (2026-11-19T17:55:57Z)** — `check_ironflow_cache_integrity.py` registered in `tracka_script_scope_registry.json` (197/197) and `tests/test_tracka_hardening_117.SCRIPT_REGISTRY`.
13. **Ladder sequencing ambiguity removed** — campaign start timestamp must be the handoff refresh UTC (later than the finished session).
14. **Incomplete-session bottleneck removed (2026-11-19T18:51:44Z)** — `session_20261119T180650Z` completed to all 11 RISK-12 artifacts.
15. **Wrong-template bottleneck removed (2026-11-19T19:06:54Z)** — the old READ FIRST pointed at `fclr_risk12_evaluation_*.py`, which is a `models_run=false` underpowered **stub with no fitting code**. A RISK-13 session that turned out POWERED would have had to reconstruct IRLS/metrics/placebo/Holm from scratch. READ FIRST and the porting map now name `session_20261119T130817Z/fclr_risk11_evaluation_*.py` as the complete fitting template.
16. **Re-derivation bottleneck removed (2026-11-19T19:06:54Z)** — the porting map above gives the exact constants, feature list, common-sample swap, output filenames, and hardcoded panel-integrity numbers, so the next session spends its budget on the science, not on rediscovering file structure.
17. **Campaign-state ambiguity removed (2026-11-19T19:06:54Z)** — this refresh explicitly records that campaign 13 is unexecuted and that the gate's `required=false` is grandfathering, not permission to skip. It also closes the "refresh instead of work" loophole by naming the next refresh as post-RISK-13 only.

### Known structural traps (avoid them)

- `fclr_risk12_power_*.py` and `fclr_risk12_recompute_*.py` hardcode `funding_change_24h` in `apply_common_sample`. Copied verbatim, RISK-13 will silently use the wrong sample and the wrong null counts. Swap to `liq_count_lag_24h` and re-check the printed `common_sample dropped/kept`.
- `fclr_risk12_power_*.py` hardcodes `expected` panel-integrity numbers (113880 / 13 / 12 / 113880 / 113880 / 113035). Those are correct for the frozen panel — keep them; do not "fix" them to RISK-13 sample sizes.
- `fclr_risk11_evaluation_*.py` hardcodes `SMALLEST_DEFENSIBLE_EFFECT = 0.002817725360790807`. That is RISK-11's value. RISK-13 must read the freshly recomputed value from its own power JSON.
- `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` hardcodes a 6-month window. **Do not edit it** (frozen).
- `scripts/check_tracka_scope_registry_drift.py` compares `scripts/*.py` against `research_state/tracka_script_scope_registry.json` (197/197) **and** `test_tracka_hardening_117.SCRIPT_REGISTRY` must agree. Session-dir scripts are exempt; anything added under `scripts/` needs a registry entry in the JSON **and** in 117 in the same commit.
- `pandas`/`pyarrow` allowed only for parquet reads in ingest/alignment. Core statistics stay stdlib (`json/csv/statistics/random/hashlib/datetime`). No `statsmodels`, no `numpy` in the core path.
- Never emit a zero-byte artifact. Never write sealed Binance months for outcomes. Never conflate observed liquidation labels with modeled boundary breaches.
- Do not write to `.github/workflows`; do not install heavyweight stats packages.
- Do not spend the session on handoff refresh, gate-only work, descriptive replay, or re-auditing certified results.
- Root churn cap is tight (498/500 md+json on `research_state/` root). All new artifacts go under the new `session_<UTC>/` dir; never add root-level md/json files, or `test_tracka_hardening_125` and the gate fail closed.
- Do **not** write any new `session_<UTC>` token into this handoff unless that directory actually exists: the gate takes the lexicographically latest such token as the session to audit.

---

## READ FIRST (exact files)

1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261119T130817Z/fclr_risk11_evaluation_20261119T130817Z.py` — **the complete evaluation template** (stdlib IRLS logistic fit, Brier/log-loss/AUC/calibration, 1000 label-hour permutations, Holm, MDE-by-instrument-count). Use this for RISK-13 `models_run=true` readiness.
3. `research_state/session_20261119T180650Z/fclr_risk12_evaluation_20261119T180650Z.py` — the **underpowered-stub** pattern only (`models_run=false`); useful for the honest UNDERPOWERED artifact wording, not for fitting.
4. `research_state/session_20261119T180650Z/fclr_risk12_power_20261119T180650Z.py` — power/MDE template to port (hardcodes funding features; see traps).
5. `research_state/session_20261119T180650Z/fclr_risk12_recompute_20261119T180650Z.py` — independent recompute template to port.
6. `research_state/session_20261119T180650Z/fclr_risk12_prereg_20261119T180650Z.json` — prereg schema to mirror (swap in the RISK-13 family).
7. `research_state/session_20261119T180650Z/trigger_check_20261119T180650Z.json` + `evidence_audit_20261119T180650Z.{json,md}` — audit/trigger schemas.
8. `research_state/session_20261119T180650Z/fclr_risk12_power_20261119T180650Z.json` — prior block MDEs: block_2=0.004080, block_3=0.003882, pooled=0.002814 (all > 0.001); prior smallest defensible effect 0.0028144136231997873 (reference only — recompute on the RISK-13 sample).
9. `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` — frozen 12-month panel (the only input).
10. `scripts/check_handoff_heavywork_gate.py`, `scripts/check_tracka_scope_registry_drift.py`, `scripts/check_ironflow_cache_integrity.py`, `scripts/fclr_ironflow_bulk.py`
11. `research_state/resume_trigger_registry.json`, `research_state/data_source_registry.json`, `research_state/tracka_script_scope_registry.json`
12. `tests/test_tracka_hardening_143.py` — `TestRisk08CampaignGate` non-avoidance contracts (the RISK-13 session is bound by the same mechanism).

## REOPEN TRIGGERS (machine-checkable)

- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`) — **OPEN**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: extension admissibility `status=ADMISSIBLE`, `observed_labels=true`, 13 instruments, 12 complete months — **FIRED**
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` post-2026-10-31 observed labels, ≥100-day depth — **OPEN**
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null) — **OPEN**

## VERIFICATION RECORD — 2026-11-19T19:06:54Z

- `check_handoff_heavywork_gate.py --json`: **PASS** (no failures; `handoff_stale=false`; root count 498/500; `risk_08.campaign_id=FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z`, `required=false` because latest recorded session is grandfathered).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`pass=true`, `failures=[]`, 197/197).
- `check_ironflow_cache_integrity.py --json`: **PASS** (`passed=true`, 48 objects, 0 failures).
- `python3 -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119`: **PASS** (48 tests, `OK`).
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **PASS** (69 tests, `OK`).
- Panel preflight: 113,880 rows, 13 coins (`ADA APT ARB AVAX BNB BTC DOGE ETH LINK OP SOL SUI XRP`), 12 months `2025-11..2026-10`, `close`/`funding_rate`/`premium`/`liq_count` 100% non-null, `open_interest_usd` 113,035/113,880 non-null. Panel sha256 `0448a56a676eaadc7094d0e42a6b90a5f407a80502da0da74e5141547725e7d9`.
- Single durable handoff confirmed: exactly one `AGENT_HANDOFF*` in the repo.
- RISK-12 package verified complete in `session_20261119T180650Z`: 11 required artifacts, verdict UNDERPOWERED, `n_discrepancies=0`.
- No post-campaign session exists on disk; active campaign `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` remains LIVE and unexecuted; the next session must emit `fclr_risk13_*` in a dir stamped after `20261119T185144Z`.

## FIRST 10 MINUTES OF THE NEXT SESSION (checklist)

1. Read this file top-to-bottom, then `RESEARCH_PROMPT.md` §16/§19.
2. `UTC=$(date -u +%Y%m%dT%H%M%SZ)`; `mkdir -p research_state/session_$UTC`.
3. Write and freeze the RISK-13 prereg (outcome-blind), sha256 it.
4. Copy the three templates per the bootstrap block; apply the porting map.
5. Run power. If UNDERPOWERED, continue anyway — all 11 files are still required.
6. Run recompute → evaluation → evidence_audit → trigger_check.
7. Run the full verification block; fix failures in the session dir, never by editing frozen inputs.
8. Only after green: record the new session, bump the campaign to RISK-14, set its start to the refresh UTC.
