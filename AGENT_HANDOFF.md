# AGENT HANDOFF — 2026-11-19T16:57:34Z (SOLE DURABLE HANDOFF)

> **Authority:** this file only. Every other handoff-like file under `research_state/` is tombstoned/historical and has no campaign authority. Verified this refresh: exactly one `AGENT_HANDOFF*` exists in the repo.
> **Repo priority:** the repository is `Funding-conditioned-volatility-and-liquidation-risk`; RISK-11 is COMPLETE (verdict NOT_MET-with-bound, `session_20261119T130817Z`); the highest-value unexecuted work is therefore the **RISK-12** campaign — a new pre-registered confirmatory question on the frozen Track A panel, not descriptive or audit replays.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION — READ THIS BEFORE ANY OTHER ACTION (timestamped 2026-11-19T16:57:34Z)

**Campaign `FCLR-LIQ-RISK-ESCALATION-12-20261119T165734Z` is LIVE and machine-enforced.** RISK-11 completed in `session_20261119T130817Z` with verdict **NOT_MET-with-bound** (power status UNDERPOWERED; all scored blocks' mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER=0.001; `n_discrepancies=0`; honest underpowered artifacts written; smallest defensible effect 0.002817725360790807). Do not replay RISK-11. Do not re-audit it. The interaction hypothesis is closed as not detectable at PLAUSIBLE_EFFECT_BRIER=0.001.

Repo priority (Funding-conditioned-volatility-and-liquidation-risk): RISK-11 → NOT_MET-with-bound closes the funded×RV×OI interaction family. Per the contingency ladder, the next heavy campaign pivots to a **new pre-registered confirmatory question on the frozen Track A panel** (do not manufacture a new funded-data source). HL_LABEL_EXTENSION remains OPEN (no post-`2026-10-31` observed-label source with ≥100-day depth appeared). GATE4_BRANCH_1 and EXPANSION_ROBUSTNESS_REDO remain external-trigger-only.

Your session's deliverable is **RISK-12**, in this exact order:

1. Create `research_state/session_<UTC>/` (UTC at session start, strictly > `20261119T165734Z`).
2. Write the **outcome-blind** prereg `fclr_risk12_prereg_<UTC>.{json,md}` and freeze it **before** touching any outcome. Contract: new confirmatory question on the frozen Track A panel — preregister the hypothesis, smallest defensible effect, MDE-by-instrument-count table (1–13 coins, block_2/block_3/pooled), decision rule (verdict SUPPORT / NOT_MET-with-bound / UNDERPOWERED), same three blocks (block_2, block_3, pooled; block_1 cold-start power only), Holm over family at α=0.05, same placebo (label-hour permutation, 1000 perms, seed `20261119`), same metrics. Do not slim and do not outcome-mine.
3. Run `fclr_risk12_power_<UTC>.{py,json,md}` with explicit `status` in `{POWERED, UNDERPOWERED}` (recompute MDE from frozen block sizes and panel base rate; `PLAUSIBLE_EFFECT_BRIER = 0.001` stays frozen).
4. Run `fclr_risk12_recompute_<UTC>.{py,json}`; require `n_discrepancies=0`.
5. Run `fclr_risk12_evaluation_<UTC>.{py,json,md}`: report per-block MDE table by instrument count, the preregistered decision, placebo p, Holm p, and an honest verdict.
6. Write `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json`.
7. Run every verification command in this file; all must PASS. Only then may you update this handoff (and you must bump the campaign id to RISK-13 per the ladder rule below).

`scripts/check_handoff_heavywork_gate.py` **fails closed** for any session dir stamped after `20261119T165734Z` that lacks the exact 11-file `fclr_risk12_*` package + non-empty `trigger_check_*.json`. A descriptive-only, trigger-check-only, gate-only, or arbitrary-`recompute_*` session cannot pass. Zero-byte artifacts fail. There is no cheaper legal session.

**Forbidden starts:** RISK-09 replay, RISK-10 replay, RISK-11 replay, `FCLR-LIQ-TRACKA-CONFIRMATORY-02` (precondition UNDERPOWERED; verdict was NOT_MET), `FCLR-LIQ-TRACKA-DATA-EXTENSION-02` (no post-`2026-10-31` labels with ≥100-day depth), RISK-05/06/07, ROBUST-05, Track C QLIKE, and reading sealed Binance months (`2024-10 … 2026-11`) for outcomes.

---

## UNBLOCKED PREFLIGHT — verified 2026-11-19T16:57:34Z (do NOT redo any of this)

The data bottleneck for RISK-11 is **already removed**. Everything needed is on disk (same frozen panel as RISK-08/09/10/11):

- Frozen panel: `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv`
- Shape: **113,880 coin-hours**, 13 coins (`BTC ETH BNB SOL XRP AVAX DOGE LINK SUI ARB OP APT ADA`), **12 complete months** (`2025-11 … 2026-10`).
- Columns: `coin,hour_utc,month,close,volume,funding_rate,premium,mark_price,open_interest_usd,liq_count,liq_long_count,liq_short_count,liq_fills,liq_notional_usd`.
- Non-null coverage: `funding_rate` **113,880/113,880**, `open_interest_usd` **113,035/113,880**, `liq_count` **113,880/113,880**.
- Bulk cache verified this refresh: `python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10` → **48 objects, 0 failures**.
- Extension verdict frozen **ADMISSIBLE**; **do not** re-run ingest, alignment, or admissibility.
- No new parquet read is required: build all features from the frozen CSV with stdlib `csv` + `math` + `statistics`.
- RISK-11 package (complete, in `session_20261119T130817Z`): `fclr_risk11_prereg/power/recompute/evaluation` + `evidence_audit` + `trigger_check`, verdict NOT_MET-with-bound, `n_discrepancies=0`.

### Frozen derivations (define in prereg, then implement verbatim — mirror `session_20261119T130817Z/fclr_risk11_evaluation_20261119T130817Z.py`)

- Outcome: `y = 1 if liq_count >= 1 else 0` per (coin, hour). A zero means "no event observed in the feed", not a confirmed no-liquidation hour — repeat this caveat in every outcome artifact.
- `ret_t = ln(close_t / close_{t-1})` within coin, ordered by `hour_utc`.
- `rv_lag` = sample std (`statistics.stdev`) of the trailing **24** hourly log returns ending at `t-1`, i.e. mean/std over `ret_{t-24..t-1}`.
- `funding_lag` = `funding_rate` at `t-1`; `premium_lag` = `premium` at `t-1`.
- `oi_change_lag` = `ln(open_interest_usd_{t-1} / open_interest_usd_{t-2})` (requires two lagged OI observations; if `t-2` missing, `oi_change_lag` is null).
- Common-sample rule (binding, prevents a fake paired-difference win): drop a coin-hour for *all* models whenever any of `rv_lag, funding_lag, oi_change_lag` is null. All family members and RV-only must be scored on the identical test rows.
- Standardize nothing ad hoc; fit logistic regression by stdlib IRLS (mirror `fit_logistic` in the RISK-11 evaluation module).

### Frozen design (mirror RISK-11; do not re-split)

- `block_1` test `2025-11-01..2025-12-31`, train none (cold-start anchor; power only).
- `block_2` test `2026-02-01..2026-04-30`, train `2025-11-01..2025-12-31`.
- `block_3` test `2026-06-01..2026-08-31`, train `2025-11-01..2026-01-31`.
- Purges `2026-01`, `2026-05`; reserve `2026-09..2026-10` untouched and never scored.
- Models: `intercept-only`, `RV-only` (`rv_lag`). RISK-12 tests a new confirmatory question on the frozen panel.
- Metrics: Brier (headline), log-loss, AUC, calibration OLS slope/intercept on test ps.
- Placebo: permute test labels **within hour across coins** (label-hour permutation), 1000 permutations, fixed seed `20261119`; report empirical p and 95th percentile of the null Brier difference.
- Multiplicity: Holm over family at `alpha=0.05`; Holm family declared in prereg before outcomes.
- Smallest defensible effect: 0.002817725360790807 (min pooled MDE from RISK-10/RISK-11, block_3 primary); effect defensible only if >= this MDE.

### Power gate (declare before evaluation)

- Recompute MDE from frozen block sizes and panel base rate only (mirror `run_power` in the RISK-11 evaluation module). `PLAUSIBLE_EFFECT_BRIER = 0.001` stays frozen.
- MDE-by-instrument-count table (1–13 coins) reproduced in prereg; the preregistered smallest-defensible-effect decision recorded before evaluation.
- If all scored blocks' `mde_brier_80pct > PLAUSIBLE_EFFECT_BRIER`, `status=UNDERPOWERED`, `models_run=false`, and write the honest underpowered artifacts anyway (still all 11 files, still non-empty).

### Definition of done (all must hold; gate + review)

| # | Requirement |
|---|---|
| 1 | New `research_state/session_<UTC>/` dir exists; UTC strictly greater than `20261119T165734Z` |
| 2 | `fclr_risk12_prereg_<UTC>.{json,md}` exist, non-empty, and JSON has `frozen_utc` + `outcome_blind=true` + full contract above |
| 3 | `fclr_risk12_power_<UTC>.{py,json,md}` exist, non-empty, JSON has explicit `status` |
| 4 | `fclr_risk12_recompute_<UTC>.{py,json}` exist, non-empty, JSON has `n_discrepancies: 0` |
| 5 | `fclr_risk12_evaluation_<UTC>.{py,json,md}` exist, non-empty, JSON has MDE-by-instrument-count table, preregistered decision, placebo p, Holm p, verdict |
| 6 | `evidence_audit_<UTC>.{json,md}` exist, non-empty, per `RESEARCH_PROMPT.md` §19 |
| 7 | `trigger_check_<UTC>.json` exists, non-empty, re-evaluates all 4 registry triggers |
| 8 | Every JSON embeds the campaign id `FCLR-LIQ-RISK-ESCALATION-12-20261119T165734Z` and the session UTC |
| 9 | Verification block below passes end-to-end |
| 10 | Handoff updated only after 9 passes, with campaign id bumped to RISK-13 per the ladder rule |

### Execution recipe

```bash
UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
# 1) prereg  -> freeze, hash it (sha256) into the power/evaluation JSON
# 2) power   -> require status=POWERED (or honest UNDERPOWERED with all 11 files)
# 3) recompute -> require n_discrepancies=0
# 4) evaluation -> verdict, MDE-by-instrument table, smallest-defensible-effect decision
# 5) evidence_audit + trigger_check
# 6) verification block, then handoff update
```

### Verification commands (all must PASS before touching this handoff)

```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 scripts/check_tracka_scope_registry_drift.py --json
python3 scripts/fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10
python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v
python3 -m unittest discover -s tests -p 'test_tracka_*.py'
```

### Ladder rule (this is how the gate keeps biting without deadlocking)

The artifact family is bound to the campaign number written in **this** file. So: after RISK-11's package exists, rewrite **both** the initial task message and the campaign line with `FCLR-LIQ-RISK-ESCALATION-12-<new UTC>`, and the next session must emit `fclr_risk12_*`. Never leave RISK-11 as the active campaign once its package exists, or the next honest session will be forced to duplicate it. After RISK-12 passes, bump to RISK-13 identically.

### Contingency ladder — pre-authorized heavy follow-ons (no idling allowed)

- **RISK-11 → NOT_MET-with-bound (current):** interaction hypothesis closed as not detectable at PLAUSIBLE_EFFECT_BRIER=0.001; next heavy campaign `RISK-12` = *new pre-registered confirmatory question on the frozen Track A panel* (do not manufacture a new funded-data source).
- **RISK-12 → any verdict:** if a new post-`2026-10-31` observed-label source appears (≥100-day depth), `HL_LABEL_EXTENSION` becomes eligible; refresh only via the `research_state/hl_label_extension_audit_<UTC>.{md,json}` contract. `GATE4_BRANCH_1` and `EXPANSION_ROBUSTNESS_REDO` remain external-trigger-only; never manufacture evidence for them.

---

## CURRENT STATE (verified 2026-11-19T16:57:34Z)

- **Campaign state:** `ACTIVE_CAMPAIGN`; Track A exploratory COMPLETE; 12-month extension COMPLETE / ADMISSIBLE; Track A confirmatory COMPLETE, verdict **NOT_MET**; RISK-08 COMPLETE, verdict **NOT_MET** (POWERED, `n_discrepancies=0`); RISK-09 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`); RISK-10 COMPLETE, verdict **UNDERPOWERED** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.0028); RISK-11 COMPLETE, verdict **NOT_MET-with-bound** (`n_discrepancies=0`, all six members NOT_MET, smallest defensible effect 0.002817725360790807); active campaign `FCLR-LIQ-RISK-ESCALATION-12-20261119T165734Z` (new pre-registered confirmatory question on frozen panel), gate-enforced, data preflight PASS.
- **Latest session on disk:** `research_state/session_20261119T130817Z` — RISK-11 complete package (`fclr_risk11_prereg/power/recompute/evaluation` + `evidence_audit` + `trigger_check`), verdict NOT_MET-with-bound.
- **Prior sessions:** `session_20261119T110653Z` (RISK-10); `session_20261119T095800Z` (RISK-09); `session_20261119T090239Z` (RISK-08 phase B/C bundle); `session_20261119T033443Z` (extension descriptive + audit + trigger check); `session_20261119T022824Z` (extension alignment ADMISSIBLE + confirmatory prereg).
- **Descriptive context (associational only):** 18.93% of coin-hours have ≥1 observed event (Wilson 95% CI 18.70%..19.16%); incidence rises monotonically across trailing-24h RV deciles (6.33% → 36.02%); funding deciles U-shaped (decile 4 16.36%, decile 10 22.90%).
- **Rank-0 triggers:** `NEW_OBSERVED_LIQUIDATION_SOURCE` = **FIRED**; `GATE4_BRANCH_1`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` = **OPEN**.
- **Root `research_state/` md+json count:** **498 / 500** (cap enforced by `test_tracka_hardening_125`). All new artifacts go under the new session dir. If a root registry must change, edit in place; never add.
- **Immutable:** `session_20261118T201919Z/*`, `session_20261118T132800Z/*`, `session_20261119T022824Z/*`, `session_20261119T033443Z/*`, `session_20261119T090239Z/*`, `session_20261119T095800Z/*`, `session_20261119T110653Z/*`, `session_20261119T130817Z/*`.

### Bottlenecks removed (do not redo)

1. **Data bottleneck gone** — bulk cache `candles_1h,funding,open_interest,liquidations` covers `2025-11 … 2026-10`, verify 48/48 OK.
2. **Events bottleneck gone** — `research_state/data_cache/ironflow_events/<YYYY-MM>.parquet` covers `2025-05 … 2026-10`.
3. **Admissibility/extension bottleneck gone** — 12-month panel + ADMISSIBLE verdict frozen.
4. **Confirmatory-registration bottleneck gone** — three-block design, label contract, lags, models, metrics, placebo, Holm frozen.
5. **Empty-session / stale-handoff bottleneck gone** — gate compares newest on-disk session to handoff; handoff now records `session_20261119T130817Z`.
6. **Confirmatory non-avoidance gate satisfied** by `session_20261119T095800Z` (RISK-09 evaluation, all six members NOT_MET under UNDERPOWERED).
7. **Escalation non-avoidance gate installed** — ladder rule bumps campaign number to bind artifact family (`fclr_risk12_*` for RISK-12).
8. **RISK-08/09 feature bottleneck removed** — panel already carries `funding_rate` (100% non-null) and `open_interest_usd` (99.26% non-null); RV is derivable from `close`; no ingest or parquet read required.
9. **Paired-sample trap removed** — binding common-sample rule for null `oi_change_lag`, so all comparisons vs RV-only are on identical rows.
10. **Post-RISK-11 deadlock removed** — explicit ladder rule to bump to `fclr_risk12_*`, plus a three-way contingency ladder so no verdict leads to idling.
11. **RISK-11 verdict finalized** — NOT_MET-with-bound; RISK-12 new pre-registered confirmatory question on frozen panel is the only authorized next campaign.

### Known structural traps (avoid them)

- `fclr_tracka_exploratory01_alignment_20261118T201919Z.py` hardcodes a 6-month window. **Do not edit it** (frozen). Copy into the new session dir if reuse is needed.
- `scripts/check_tracka_scope_registry_drift.py` compares `scripts/*.py` against `research_state/tracka_script_scope_registry.json` (196/196). Session-dir scripts are exempt; anything added under `scripts/` needs a registry entry in the same commit.
- `pandas`/`pyarrow` allowed only for parquet reads in ingest/alignment. Core statistics stay stdlib (`json/csv/statistics/random/hashlib/datetime`). No `statsmodels`, no `numpy` in the core path.
- Never emit a zero-byte artifact. Never write sealed Binance months for outcomes. Never conflate observed liquidation labels with modeled boundary breaches.
- Do not write to `.github/workflows`; do not install heavyweight stats packages.
- Do not spend the session on handoff refresh, gate-only work, descriptive replay, or re-auditing certified results.
- Root churn cap is tight (498/500 md+json on `research_state/` root). All new artifacts go under the new `session_<UTC>/` dir; never add root-level md/json files, or `test_tracka_hardening_125` and the gate fail closed.

---

## READ FIRST (exact files)

1. `RESEARCH_PROMPT.md` §1–§6, §9–§10, §13–§16, §18–§20
2. `research_state/session_20261119T130817Z/fclr_risk11_evaluation_20261119T130817Z.py` — executable pattern (stdlib IRLS, frozen design, 3 blocks, placebo 1000 perms, Holm, MDE-by-instrument-count) producing verdict NOT_MET-with-bound
3. `research_state/session_20261119T130817Z/fclr_risk11_power_20261119T130817Z.json` — block MDEs: block_2=0.0041, block_3=0.0039, pooled=0.0028 (all > 0.001); smallest defensible effect 0.002817725360790807
4. `research_state/session_20261119T130817Z/fclr_risk11_recompute_20261119T130817Z.json` — `n_discrepancies=0`
5. `research_state/session_20261119T130817Z/trigger_check_20261119T130817Z.json` — trigger definitions/status
6. `research_state/session_20261119T022824Z/fclr_tracka_extension01_panel_session_20261119T022824Z.csv` — frozen 12-month panel (the only input)
7. `scripts/check_handoff_heavywork_gate.py`, `scripts/check_tracka_scope_registry_drift.py`, `scripts/fclr_ironflow_bulk.py`
8. `research_state/resume_trigger_registry.json`, `research_state/data_source_registry.json`
9. `tests/test_tracka_hardening_143.py` — `TestRisk08CampaignGate` non-avoidance contracts (adapt for RISK-12)

## REOPEN TRIGGERS (machine-checkable)

- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`) — **OPEN**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: extension admissibility `status=ADMISSIBLE`, `observed_labels=true`, 13 instruments, 12 complete months — **FIRED**
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` post-2026-10-31 observed labels, ≥100-day depth — **OPEN**
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null) — **OPEN**

## VERIFICATION RECORD — 2026-11-19T16:57:34Z

- `check_handoff_heavywork_gate.py --json`: pending — will re-verify after RISK-12 artifacts exist
- `check_tracka_scope_registry_drift.py --json`: **PASS** (196/196).
- `fclr_ironflow_bulk.py verify --datasets all --months 2025-11..2026-10`: **48 objects, 0 failures**.
- `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125`: **PASS**.
- `python3 -m unittest discover -s tests -p 'test_tracka_*.py'`: **PASS**.
- Panel preflight: 113,880 rows, 13 coins, 12 months, `funding_rate` 100% non-null, `open_interest_usd` 113,035/113,880 non-null, `liq_count` 100% non-null.
- Single durable handoff confirmed: exactly one `AGENT_HANDOFF*` in the repo.
- RISK-11 package verified complete in `session_20261119T130817Z`: `fclr_risk11_prereg/power/recompute/evaluation` + `evidence_audit` + `trigger_check`, verdict NOT_MET-with-bound, `n_discrepancies=0`.
- Active campaign `FCLR-LIQ-RISK-ESCALATION-12-20261119T165734Z` (new pre-registered confirmatory question on frozen panel) LIVE; next session must emit `fclr_risk12_*`.