# AGENT HANDOFF — 2026-11-19T18:51:44Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file under `research_state/` is tombstoned/historical and has no campaign authority. Verified this refresh: exactly one `AGENT_HANDOFF*` exists in the repo.
> **Repo priority:** the repository is `Funding-conditioned-volatility-and-liquidation-risk`; RISK-12 is COMPLETE (verdict UNDERPOWERED, `session_20261119T180650Z`); the highest-value unexecuted work is therefore the **RISK-13** campaign — a new pre-registered confirmatory question on the frozen Track A panel per the contingency ladder (distinct mechanism: liquidation-hazard persistence `liq_count`-at-`t-1` state family), not descriptive or audit replays.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T18:51:44Z)

**Campaign `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` is LIVE, fully specified, and machine-enforced.** RISK-12 completed in `session_20261119T180650Z` with verdict **UNDERPOWERED** (power status UNDERPOWERED; all scored blocks' `mde_brier_80pct` > `PLAUSIBLE_EFFECT_BRIER=0.001`; `n_discrepancies=0`; smallest defensible effect 0.0028144136231997873). The funding-shock transmission family is closed as not detectable at 0.001. Do not replay, re-audit, or re-split it.

Per the contingency ladder, since RISK-12 is UNDERPOWERED, the next campaign must be a **distinct mechanism on the frozen panel**. The candidate queue (in order) is: (i) liquidation-hazard persistence `liq_count`-at-`t-1` state family — authorized as RISK-13; (ii) within-hour cross-sectional funding-intensity contrast; (iii) UTC-hour / market-wide-RV conditioning of the funding effect. RISK-13 = candidate (i). Do not skip ahead.

Your session's deliverable is **RISK-13**, in this exact order:

1. Create `research_state/session_<UTC>/` (UTC at session start, strictly > `20261119T185144Z`).
2. Write the **outcome-blind** prereg `fclr_risk13_prereg_<UTC>.{json,md}` and freeze it **before** touching any outcome, using the exact RISK-13 contract in the next section. Do not slim the family and do not outcome-mine.
3. Run `fclr_risk13_power_<UTC>.{py,json,md}` with explicit `status` in `{POWERED, UNDERPOWERED}`; recompute MDE from the RISK-13 common sample only; `PLAUSIBLE_EFFECT_BRIER = 0.001` stays frozen.
4. Run `fclr_risk13_recompute_<UTC>.{py,json}`; require `n_discrepancies=0`.
5. Run `fclr_risk13_evaluation_<UTC>.{py,json,md}`: per-block MDE-by-instrument-count table, preregistered decision, placebo p, Holm p, per-member coefficient signs vs declared directions, honest verdict.
6. Write `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json`.
7. Run every verification command in this file; all must PASS.
8. Then — and only then — update this handoff: add your `session_<UTC>` id, bump the campaign number to RISK-14, and set the new campaign start timestamp to the handoff refresh UTC (must be strictly greater than your session-dir UTC). See "Ladder rule" for why that ordering matters.

`scripts/check_handoff_heavywork_gate.py` **fails closed for the session this handoff records** once that session's UTC is after the campaign start: it must contain the exact 11-file `fclr_risk13_*` package + non-empty `trigger_check_*.json`. A descriptive-only, trigger-check-only, gate-only, or arbitrary-`recompute_*` session cannot pass. Zero-byte artifacts fail. There is no cheaper legal session. A session dir that exists on disk but is not recorded here also fails (`HANDOFF_STALE_LATEST_SESSION`), so artifacts cannot be skipped by leaving the handoff stale.

**Forbidden starts:** RISK-09 replay, RISK-10 replay, RISK-11 replay, RISK-12 replay, `FCLR-LIQ-TRACKA-CONFIRMATORY-02` (precondition UNDERPOWERED; verdict was NOT_MET), `FCLR-LIQ-TRACKA-DATA-EXTENSION-02` (no post-`2026-10-31` labels with ≥100-day depth), RISK-05/06/07, ROBUST-05, Track C QLIKE replay, and reading sealed Binance months (`2024-10 … 2026-11`) for outcomes.

---

## RISK-13 CAMPAIGN CONTRACT — liquidation-hazard persistence family (`liq_count`-at-`t-1` state)

Family name: **`liquidation-hazard persistence family (liq_count state)`**; `n_family_members = 6`; no slimming.

### Frozen derivations (same panel, same outcome, same blocks)

- Input (only): `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` (113,880 coin-hours, 13 coins, 12 complete months `2025-11 … 2026-10`, verdict ADMISSIBLE).
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
| `member_1` | `funding_lag` (level) — positive control / replication anchor | prior campaigns found this not detectable at 0.001; it exists so the new state features are interpretable against the closed level result |
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

- Recompute MDE from the **RISK-13 common sample** block sizes and panel base rate only (mirror `run_power` in the RISK-11 evaluation module). `PLAUSIBLE_EFFECT_BRIER = 0.001` stays frozen.
- MDE-by-instrument-count table (1–13 coins, fixed alphabetical order `BTC ETH BNB SOL XRP AVAX DOGE LINK SUI ARB OP APT ADA`) reproduced in the prereg. The RISK-12 smallest defensible effect `0.0028144136231997873` is a **reference only, not a hardcoded value**: `smallest_defensible_effect` must be recomputed and frozen from the RISK-13 power output before evaluation, under the rule *min `mde_brier_80pct` across scored blocks at full 13 coins (block_3 primary)*.
- If all scored blocks' `mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER`, `status=UNDERPOWERED`, `models_run=false`, and write the honest underpowered artifacts anyway (still all 11 files, still non-empty). Underpowered is still a full legal session.

### Definition of done (all must hold; gate + review)

| # | Requirement |
|---|---|
| 1 | New `research_state/session_<UTC>/` dir exists; UTC strictly greater than `20261119T185144Z` |
| 2 | `fclr_risk13_prereg_<UTC>.{json,md}` exist, non-empty; JSON has `frozen_utc`, `outcome_blind=true`, the 6-member family table above, `blocks`, `metrics`, `placebo`, `multiplicity`, and `common_sample_rule` |
| 3 | `fclr_risk13_power_<UTC>.{py,json,md}` exist, non-empty; JSON has explicit `status` and the MDE-by-instrument-count table |
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
# 1) prereg  -> freeze, hash it (sha256) into the power/evaluation JSON
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

`check_ironflow_cache_integrity.py` is the mandatory data check: hash-only (stdlib `hashlib`), offline, no parquet content read, 48/48 objects OK. `scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10` is an **optional** extra when `pyarrow` is installed; do not let a missing `pyarrow`/`pandas` fail the session (that environment trap is now removed).

### Ladder rule (how the gate keeps biting without deadlocking)

The gate binds the artifact family `fclr_riskNN_*` to the **campaign number in this file**, and applies it to the **latest session id recorded in this file** once that session's UTC is after the campaign start. Therefore the handoff refresh that closes campaign N must: (a) record the just-finished session id, (b) bump the campaign to N+1, and (c) set the N+1 start timestamp to the **handoff refresh UTC**, which is strictly later than the finished session-dir UTC. The finished session is then grandfathered (`latest_utc <= campaign_start`) and the *next* session is bound to `fclr_risk(N+1)_*`. Never bump the number while keeping an older start timestamp, and never leave campaign N as the active campaign once its package exists — either error forces an honest session to duplicate completed work or impossible filenames.

### Contingency ladder — pre-authorized heavy follow-ons (no idling allowed)

- **RISK-13 → any verdict:** if a new post-`2026-10-31` observed-label source appears (≥100-day depth), `HL_LABEL_EXTENSION` becomes eligible; refresh only via the `research_state/hl_label_extension_audit_<UTC>.{md,json}` contract. `GATE4_BRANCH_1` and `EXPANSION_ROBUSTNESS_REDO` remain external-trigger-only; never manufacture evidence for them.
- **If RISK-13 is UNDERPOWERED:** do not silently repeat it. Next campaign must be a *distinct* mechanism on the frozen panel, pre-registered the same way (candidate queue, in order: (i) within-hour cross-sectional funding-intensity contrast; (ii) UTC-hour / market-wide-RV conditioning of the funding effect). Bump the campaign number per the ladder rule.

---

## CURRENT STATE (verified 2026-11-19T18:51:44Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; Track A exploratory COMPLETE; 12-month extension COMPLETE / ADMISSIBLE; Track A confirmatory COMPLETE, verdict **NOT_MET**; RISK-08 COMPLETE, verdict **NOT_MET** (POWERED, `n_discrepancies=0`); RISK-09 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`); RISK-10 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.0028); RISK-11 COMPLETE, verdict **NOT_MET-with-bound** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.002817725360790807); RISK-12 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.0028144136231997873); active campaign `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` (liquidation-hazard persistence family on the frozen panel), gate-enforced, data preflight PASS.
- **Latest session on disk:** `research_state/session_20261119T180650Z` — RISK-12 complete package (`fclr_risk12_prereg/power/recompute/evaluation` + `evidence_audit` + `trigger_check`), verdict UNDERPOWERED.
- **Prior sessions:** `session_20261119T130817Z` (RISK-11); `session_20261119T110653Z` (RISK-10); `session_20261119T095800Z` (RISK-09); `session_20261119T090239Z` (RISK-08 phase B/C bundle); `session_20261119T033443Z` (extension descriptive + audit + trigger check); `session_20261119T022824Z` (extension alignment ADMISSIBLE + confirmatory prereg).
- **Descriptive context (associational only):** 18.93% of coin-hours have ≥1 observed event (Wilson 95% CI 18.70%..19.16%); incidence rises monotonically across trailing-24h RV deciles (6.33% → 36.02%); funding deciles U-shaped (decile 4 16.36%, decile 10 22.90%).
- **Rank-0 triggers:** `NEW_OBSERVED_LIQUIDATION_SOURCE` = **FIRED**; `GATE4_BRANCH_1`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` = **OPEN**.
- **Root `research_state/` md+json count:** **498 / 500** (cap enforced by `test_tracka_hardening_125`). All new artifacts go under the new session dir. If a root registry must change, edit in place; never add.
- **Immutable:** `session_20261118T201919Z/*`, `session_20261118T132800Z/*`, `session_20261119T022824Z/*`, `session_20261119T033443Z/*`, `session_20261119T090239Z/*`, `session_20261119T095800Z/*`, `session_20261119T110653Z/*`, `session_20261119T130817Z/*`, `session_20261119T180650Z/*`.

### Bottlenecks removed (do not redo)

1. **Data bottleneck gone** — bulk cache `candles_1h,funding,open_interest,liquidations` covers `2025-11 … 2026-10`, 48/48 objects OK.
2. **Events bottleneck gone** — `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` covers `2025-05 … 2026-10`.
3. **Admissibility/extension bottleneck gone** — 12-month panel + ADMISSIBLE verdict frozen.
4. **Confirmatory-registration bottleneck gone** — three-block design, label contract, lags, models, metrics, placebo, Holm frozen.
5. **Empty-session / stale-handoff bottleneck gone** — gate compares newest on-disk session to handoff; handoff now records `session_20261119T180650Z` (was stale at `session_20261119T130817Z`, causing `HANDOFF_STALE_LATEST_SESSION`).
6. **Confirmatory non-avoidance gate satisfied** by `session_20261119T095800Z` (RISK-09 evaluation, all six members NOT_MET under UNDERPOWERED).
7. **Escalation non-avoidance gate installed** — ladder rule bumps campaign number to bind artifact family (`fclr_risk13_*` for RISK-13).
8. **RISK-08/09 feature bottleneck removed** — panel already carries `funding_rate` (100% non-null) and `open_interest_usd` (99.26% non-null); RV is derivable from `close`; no ingest or parquet read required.
9. **Paired-sample trap removed** — binding common-sample rule, extended for RISK-12 to require `funding_change_24h` (hence `t-25`), so all comparisons vs RV-only are on identical rows.
10. **Post-RISK-11 deadlock removed** — explicit ladder rule to bump to `fclr_risk12_*`, plus a three-way contingency ladder so no verdict leads to idling.
11. **RISK-11 verdict finalized** — NOT_MET-with-bound; RISK-12 (funding-shock transmission) fully specified and executed.
12. **Environment + registry drift bottleneck removed (2026-11-19T17:55:57Z)** — `check_ironflow_cache_integrity.py` registered in `tracka_script_scope_registry.json` (197/197) and `tests/test_tracka_hardening_117.SCRIPT_REGISTRY`; drift is green again.
13. **Ladder sequencing ambiguity removed** — explicit rule that the campaign start timestamp must be the handoff refresh UTC (later than the finished session).
14. **Incomplete-session bottleneck removed (2026-11-19T18:51:44Z)** — `session_20261119T180650Z` existed on disk with only prereg + power (missing recompute/evaluation/evidence_audit/trigger_check/power.md); all 11 RISK-12 artifacts now complete, handoff records the session, `HANDOFF_STALE_LATEST_SESSION` cleared.

### Known structural traps (avoid them)

- `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` hardcodes a 6-month window. **Do not edit it** (frozen). Copy into the new session dir if reuse is needed.
- `scripts/check_tracka_scope_registry_drift.py` compares `scripts/*.py` against `research_state/tracka_script_scope_registry.json` (197/197) **and** `test_tracka_hardening_117.SCRIPT_REGISTRY` must agree. Session-dir scripts are exempt; anything added under `scripts/` needs a registry entry in the JSON **and** in 117 in the same commit.
- `pandas`/`pyarrow` allowed only for parquet reads in ingest/alignment. Core statistics stay stdlib (`json/csv/statistics/random/hashlib/datetime`). No `statsmodels`, no `numpy` in the core path.
- Never emit a zero-byte artifact. Never write sealed Binance months for outcomes. Never conflate observed liquidation labels with modeled boundary breaches.
- Do not write to `.github/workflows`; do not install heavyweight stats packages.
- Do not spend the session on handoff refresh, gate-only work, descriptive replay, or re-auditing certified results.
- Root churn cap is tight (498/500 md+json on `research_state/` root). All new artifacts go under the new `session_<UTC>/` dir; never add root-level md/json files, or `test_tracka_hardening_125` and the gate fail closed.

---

## READ FIRST (exact files)

1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261119T180650Z/fclr_risk12_evaluation_20261119T180650Z.py` — executable pattern (stdlib IRLS, frozen design, 3 blocks, placebo 1000 perms, Holm, MDE-by-instrument-count) producing verdict UNDERPOWERED
3. `research_state/session_20261119T180650Z/fclr_risk12_prereg_20261119T180650Z.json` — prereg schema to mirror (swap in the RISK-13 family)
4. `research_state/session_20261119T180650Z/fclr_risk12_power_20261119T180650Z.json` — prior block MDEs: block_2=0.004080, block_3=0.003882, pooled=0.002814 (all > 0.001); prior smallest defensible effect 0.0028144136231997873 (reference only — recompute on the RISK-13 sample)
5. `research_state/session_20261119T180650Z/fclr_risk12_recompute_20261119T180650Z.json` — `n_discrepancies=0`
6. `research_state/session_20261119T180650Z/trigger_check_20261119T180650Z.json` — trigger definitions/status
7. `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` — frozen 12-month panel (the only input)
8. `scripts/check_handoff_heavywork_gate.py`, `scripts/check_tracka_scope_registry_drift.py`, `scripts/check_ironflow_cache_integrity.py`, `scripts/fclr_ironflow_bulk.py`
9. `research_state/resume_trigger_registry.json`, `research_state/data_source_registry.json`, `research_state/tracka_script_scope_registry.json`
10. `tests/test_tracka_hardening_143.py` — `TestRisk08CampaignGate` non-avoidance contracts (the RISK-13 session is bound by the same mechanism)

## REOPEN TRIGGERS (machine-checkable)

- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`) — **OPEN**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: extension admissibility `status=ADMISSIBLE`, `observed_labels=true`, 13 instruments, 12 complete months — **FIRED**
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` post-2026-10-31 observed labels, ≥100-day depth — **OPEN**
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null) — **OPEN**

## VERIFICATION RECORD — 2026-11-19T18:51:44Z

- `check_handoff_heavywork_gate.py --json`: **PASS** (no failures; `handoff_stale=false`; root count 498/500).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (197/197) after registering `check_ironflow_cache_integrity.py`.
- `check_ironflow_cache_integrity.py --json`: **PASS** (`passed=true`, 48 objects, 0 failures, `requires_pyarrow=false`).
- `fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10`: **48 objects, 0 failures** (pyarrow present in this runner; optional).
- `python3 -m unittest tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119`: **PASS** (48 tests).
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **PASS** (69 tests).
- `python3 -m unittest discover -s tests -p 'test_tracka_*.py'`: **PASS**.
- Panel preflight: 113,880 rows, 13 coins, 12 months, `funding_rate` 100% non-null, `open_interest_usd` 113,035/113,880 non-null, `liq_count` 100% non-null.
- Single durable handoff confirmed: exactly one `AGENT_HANDOFF*` in the repo.
- RISK-12 package verified complete in `session_20261119T180650Z`: `fclr_risk12_prereg/power/recompute/evaluation` + `evidence_audit` + `trigger_check`, verdict UNDERPOWERED, `n_discrepancies=0`.
- Active campaign `FCLR-LIQ-RISK-ESCALATION-13-20261119T185144Z` (liquidation-hazard persistence family) LIVE; next session must emit `fclr_risk13_*` in a dir stamped after `20261119T185144Z`.
