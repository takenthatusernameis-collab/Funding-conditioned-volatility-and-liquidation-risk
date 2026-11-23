# AGENT HANDOFF — 2026-11-23T08:43:16Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> Gate status as of this refresh (2026-11-23T08:43:16Z): **PASS** (reason_code=OK, root=499/500).
> The prior heavy session `session_20261123T043600Z` COMPLETED the full `FCLR-TRACKA-SOURCE-AUDIT-01`
> heavy set (Track B modeled-breach evaluation `fclr_tracks01_eval_*` py+json+md + independent
> `fclr_tracks01_recompute_*` py+json + recovered source_registry/probe/viability_decision triad +
> pivot_prereg + evidence_audit + trigger_check). Verdict: **NOT_SUPPORTED on both long and short
> arms** (modeled breach proxy, not observed liquidation; no risk overlay built). The binder is
> regression-pinned by `tests/test_tracka_hardening_143.py::TestTrackaSourceAuditCampaignGate`.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

> **Timestamped initial task message — inferred 2026-11-23T08:43:16Z (refresh time)**
>
> **Your ONE job, non-deferrable, gate-enforced:** create `research_state/session_<UTC>/` with UTC
> **> 20261123T080000Z** (use current wall-clock UTC at session start) and execute
> **`FCLR-LIQ-XSEC-BROAD-01`** to completion — a pre-registered, leakage-hardened, broad-universe
> (468-coin on-disk ironflow_bulk) cross-sectional test of whether the regime-conditioned
> funding → next-hour observed-liquidation-intensity association that was SUPPORTED on the narrow
> 15-coin combined panel (FCLR-XSEC-004 count / FCLR-XSEC-005 notional-weighted / FCLR-XSEC-006
> UTC-session-bucket, all `promotable:false`) **GENERALIZES** to the full on-disk ironflow_bulk
> liquidation universe (2025-05..2026-10, 2.85M liquidation rows across 468 markets). Walk-forward
> with per-coin block bootstrap (>=2,000 deterministic-seed replicates), placebo/permutation null,
> leave-one-instrument-out, Holm across the declared family, and an independent stdlib recompute
> using ONE explicit sign convention so the recompute asserts `all_checks_match:true`.
>
> **Mandatory artifact set (all non-empty, prefix `fclr_liqxsecbroad01_`):** source registry
> (json+md), outcome-blind prereg (json+md, `outcome_data_inspected_before_freeze:false`,
> hash-bound panel sha256), HEAVY evaluation triad (py+json+md), independent recompute (py+json),
> evidence audit (json+md), gate-critical `evidence_audit_<UTC>.json` alias, non-empty
> `trigger_check_<UTC>.json`. The gate fails closed with `LIQ_XSEC_BROAD_ARTIFACTS_MISSING` /
> `..._ARTIFACTS_EMPTY` if the eval triad or recompute is missing or zero-byte.
>
> **Do NOT:** re-run any terminal campaign; stop at the prereg; emit zero-byte placeholders;
> re-probe the network (source audit is frozen); build a risk overlay (§9); or describe the
> result as anything other than a broad-universe generalization test of a cross-sectional
> *association* (NOT a time-series forecast gate pass; NOT an observed-liquidation census — the
> ironflow feed is capped-sample per §15, absence ≠ zero).
>
> **Blockers: None.** The 18 ironflow_bulk monthly parquet sets (liquidations/funding/
> open_interest/candles_1h, each with `.sha256` + `.accessed.json` sidecars) are on disk and
> unmodified; the heavy evaluation is feasible TODAY in pure stdlib + pyarrow, no network.

### Single, non-deferrable job (DO THIS FIRST)

Repo-name priority → task. The repository is `Funding-conditioned-volatility-and-liquidation-risk`.
RESEARCH_PROMPT.md §3.2 half 2 is **liquidation-risk forecasting**. As of this refresh the honest
state of that half is:

- **Track C (volatility):** CLOSED leakage-robust null across every claim-worthy panel (H1_primary
  NOT_SUPPORTED; FCLR-011 PASS does not generalize forward; FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED).
- **Track A (observed liquidations):** `TRACK_A_STRUCTURALLY_BLOCKED` (source audit complete, frozen
  outcome-blind; `outcome_data_inspected_before_freeze:false`).
- **Track B (modeled boundary breach):** NOT_SUPPORTED on the just-completed `FCLR-TRACKB-MODELED-
  BREACH-01` (session_20261123T043600Z; rel Brier -2.00% long / -1.00% short; CI95 upper includes 0;
  Holm-adjusted p 0.30/0.24 > alpha_k 0.025).
- **The ONLY liquidation-risk results ever marked SUPPORTED** are the *regime-conditioned
  cross-sectional* funding → next-hour observed-liquidation-intensity findings: FCLR-XSEC-004
  (count, low-RV regime), FCLR-XSEC-005 (notional-weighted, low-RV regime), FCLR-XSEC-006 (all three
  UTC session buckets). All three are flagged `promotable:false` / EXPLORATORY_ONLY **precisely
  because they were established on the narrow 15-coin combined metpie+ironflow panel and never shown
  to GENERALIZE.** That is the unfinished, highest-value work on the liquidation-risk half.

**Your session's ONE job (heavy, non-deferrable, gate-enforced):** execute
`FCLR-LIQ-XSEC-BROAD-01` — a pre-registered, leakage-hardened, broad-universe (342-coin)
cross-sectional test of whether the regime-conditioned funding → next-hour observed-liquidation-
intensity association that was SUPPORTED on 15 coins **generalizes to the full on-disk ironflow_bulk
liquidation universe (342 coins, 2025-05..2026-10)**, under a walk-forward design with per-coin block
bootstrap, placebo/permutation, leave-one-instrument-out, Holm, and an independent stdlib recompute.
All inside ONE new `session_<UTC>/` whose UTC is **> `20261123T080000Z`** (use the current wall-clock
UTC at session start). Then record that `session_<UTC>` id in this handoff.

**Do NOT:** re-run any terminal campaign (FCLR-TRACKA-SOURCE-AUDIT-01, POOLED-001, POOLED-AUDIT-001,
POOLED-ROBUST-002, LIVE-ARCHIVE-01/02, NEXT-SOURCE-VERIFY-01, LIQ-CONTAGION-001/002, PANEL-FE-001,
STARTER-001, RISK-ESCALATION-08/09, XSEC-001..008, LIQ-OOS-FORECAST-001, etc.); stop at the prereg
(the gate fails closed with `LIQ_XSEC_BROAD_ARTIFACTS_MISSING` if the heavy eval triad or the
recompute is missing); emit zero-byte placeholders (`..._ARTIFACTS_EMPTY`); re-probe the network
(the source audit is frozen — no network for the heavy evaluation); build a risk overlay (§9); or
describe the result as anything other than what it is (a broad-universe generalization test of a
cross-sectional *association*, NOT a time-series forecast gate, NOT observed-liquidation census
completeness).

**Why this campaign (priority by repo name + frontier):** RESEARCH_PROMPT.md §3.2 half 2
(liquidation risk), §5 (expand instrument discovery), §9/§17 promotion condition 4 ("skill is not
dominated by one coin, one venue, one brief crisis or one time block"), §16 (relax only the least-
damaging constraint — broader universe — without weakening evidence). The narrow-universe findings
were explicitly non-promotable; the broad-universe generalization test is the sanctioned next step,
not threshold-shopping. This campaign is feasible TODAY on the on-disk ironflow_bulk archive.

**Blockers: None.** Source enumeration is done; the heavy evaluation runs on the on-disk ironflow_bulk
bulk panels (18 months, 342 coins). No external trigger, no network for the heavy evaluation, no new
source. The audit AND the heavy evaluation are feasible TODAY.

---

## FOCUS CAMPAIGN (Mandatory — heavy work, non-avoidable, gate-enforced)

Execute **FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z** to completion in ONE `session_<UTC>/`
(UTC > `20261123T080000Z`):

1. **SOURCE REGISTRY (on-disk, no network)** — write `fclr_liqxsecbroad01_source_registry_*`
   (json+md) recording the ironflow_bulk parquet files actually read: paths, sha256, row counts, coin
   coverage (**verified on-disk at refresh: 468 distinct markets in `liquidations`, 2,849,452 rows
   across 18 monthly files, span 2025-05-25..2026-10-31**; funding/OI/candles_1h likewise 18 files
   each), month span 2025-05..2026-10, schemas
   (`liquidations`: timestamp[ms],market,issuer,wallet,position_side,size,notional_usd,avg_price,
   fills,block,tx_hash — **note: there is NO `coin` column; the instrument key is `market`**;
   `funding`: timestamp[us],market,coin,dex,funding_rate,premium;
   `open_interest`: timestamp[us],market,coin,dex,mark_price,oracle_price,open_interest,
   open_interest_usd;
   `candles_1h`: timestamp[us],market,coin,dex,market_class,open,high,low,close,volume,trades).
   Assert sha256 before reading; do NOT mutate caches.
2. **PREREG FREEZE (outcome-blind, frozen BEFORE outcomes)** — write
   `fclr_liqxsecbroad01_prereg_*` (json+md). Must state
   `outcome_data_inspected_before_freeze:false` and hash-bind its inputs (panel sha256). Freeze every
   rule below BEFORE looking at any outcome.
3. **HEAVY EVALUATION + INDEPENDENT RECOMPUTE** — write `fclr_liqxsecbroad01_eval_*` (py+json+md)
   and `fclr_liqxsecbroad01_recompute_*` (py+json). This is the phase the gate refuses to let you
   skip; the eval triad and the recompute MUST be in the SAME session.

### Frozen protocol design (write this into the prereg; do not deviate after outcomes)

- **Experiment ID:** `FCLR-LIQ-XSEC-BROAD-01` (new ID; NOT a re-run of any terminal campaign).
- **Estimand:** out-of-sample, regime-conditioned, cross-sectional association between a funding
  feature and NEXT-HOUR observed liquidation intensity, tested for GENERALIZATION from the 15-coin
  combined panel to the 342-coin ironflow_bulk universe. This is a cross-sectional/ordering claim,
  NOT a time-series forecast gate; report it as such and never as a Track A observed-liquidation
  forecast gate pass.
- **Label (observed ironflow liquidations, capped-sample feed — NOT a complete census, §15):**
  per-coin per-hour observed liquidation intensity = event count and notional_usd sum from
  `ironflow_bulk/liquidations` (columns: timestamp[ms], market, coin, position_side, size,
  notional_usd, avg_price, ...). Keep long/short sides separate. Absence from this feed is NOT zero;
  restrict claims to presence/intensity ordering, never a binary absence/presence census.
- **Universe:** the full 342-coin ironflow_bulk liquidation universe for 2025-05..2026-10. Do NOT
  restrict to the 15-coin combined panel and do NOT substitute present-day survivors for the
  historical universe; report per-coin coverage and the exited/survivor split.
- **Features (all known at origin):** signed funding + |funding| percentile (train-only rolling) +
  mark/oracle premium + trailing RV (RV24/RV168) + trailing MA deviation, from
  `ironflow_bulk/funding` + `open_interest` (mark_price, oracle_price) + `candles_1h`. Mark-to-index /
  mark-oracle dislocation is a proxy, not a proven delay.
- **Regime variable (frozen):** the SAME regime conditioning that produced the SUPPORTED narrow-
  universe findings — RV-tercile (low/mid/high) AND UTC-session bucket (Asian/European/US) — computed
  with EXPANDING (train-only) thresholds so no future information leaks into the regime label.
- **Design:** chronological walk-forward. Train on the earlier portion; evaluate on non-overlapping
  forward test blocks (7-day / 168h blocks; >=3 non-overlapping test blocks required across the
  forward span; features normalized with train-only parameters; no full-sample quantiles).
- **Metrics:** rank-IC / cross-sectional Spearman of predicted vs realized next-hour intensity, plus
  a top-decile / alert-budget precision-recall; Brier/log-loss as secondary if a binary presence
  target is also declared (declare it in the prereg or omit it). Report raw and Holm-adjusted.
- **Uncertainty:** per-coin block bootstrap (resample complete UTC time blocks jointly across coins,
  >=2,000 deterministic-seed replicates). Report leave-one-instrument-out (>=6/8 held-out subsets
  pass) and a placebo/permutation null (permute the funding feature; the true effect must exceed the
  95th percentile of the null to be credible).
- **Materiality floor:** a frozen, pre-specified effect size (declare it in the prereg; do NOT relax
  after outcomes). The primary question is GENERALIZATION (does the narrow-universe SUPPORTED sign/
  direction survive at 342-coin breadth), not a new threshold to shop.
- **Multiplicity:** Holm across the declared family (RV-tercile arm + UTC-bucket arm + count + notional
  + long + short). Report raw and adjusted.
- **Verdict rule (symmetric, frozen):** `SUPPORTED_GENERALIZATION` iff the narrow-universe sign/
  direction is reproduced at broad breadth AND the block-bootstrap CI excludes the null in the
  favorable direction AND Holm-adjusted primary p < alpha; otherwise `NOT_SUPPORTED` (preserve the
  null honestly; a broad-universe failure to generalize is itself the durable finding — it means the
  15-coin SUPPORTED result was a small-universe artifact). Do NOT threshold-shop; do NOT relabel.

### Required Artifact Set (ALL non-empty, under `research_state/session_<UTC>/`, UTC > `20261123T080000Z`)

The gate binds the artifact family to the campaign (`FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z` →
prefix `fclr_liqxsecbroad01_`). Produce every file below; zero-byte placeholders fail closed.

| # | Artifact (prefix + suffix) | Purpose |
|---|---|---|
| 1 | `fclr_liqxsecbroad01_source_registry_<UTC>.json` **and** `.md` | On-disk ironflow_bulk source registry (paths, sha256, rows, coins, span, schemas). |
| 2 | `fclr_liqxsecbroad01_prereg_<UTC>.json` **and** `.md` | Outcome-blind prereg per the frozen design above (`outcome_data_inspected_before_freeze:false`; input hashes asserted). |
| 3 | `fclr_liqxsecbroad01_eval_<UTC>.py` **and** `.json` **and** `.md` | **HEAVY EVALUATION (gate-critical).** Rank-IC + block bootstrap + placebo + LOIO + Holm + honest verdict. |
| 4 | `fclr_liqxsecbroad01_recompute_<UTC>.py` **and** `.json` | Independent stdlib recompute of the headline statistic(s) in #3 (no shared code path; same sign convention — see EVIDENCE NOTE). |
| 5 | `fclr_liqxsecbroad01_evidence_audit_<UTC>.json` **and** `.md` | Evidence audit of the heavy result. |
| 6 | `evidence_audit_<UTC>.json` | Gate-critical alias (generic new-heavy-session check). |
| 7 | `trigger_check_<UTC>.json` | Non-empty trigger check (required by the liqxsecbroad family). |

### Carry-Forward Bundles (pristine copies from `session_20261123T043600Z/`)

Copy these into your new `session_<UTC>/` so older gate bindings stay satisfied:
- `fclr_tracks01_*` (source_registry json+md, probe py+json+md, viability_decision json+md,
  pivot_prereg json+md, eval py+json+md, recompute py+json) — the full tracks01 family.
- `fclr_risk09_*` (7 artifacts), `fclr_pooled001_*` (13), `fclr_pooled_audit001_*` (11),
  `fclr_pooled_robust002_*` (11).
- `evidence_audit_20261122T190000Z.json`, `trigger_check_20261122T190000Z.json`,
  `evidence_audit_20261122T224500Z.json`, `trigger_check_20261122T224500Z.json`.

---

## EVIDENCE NOTE (read before writing the recompute)

The just-completed `session_20261123T043600Z` tracks01 evidence contains a **sign-convention
discrepancy that you must not repeat**. In `fclr_tracks01_eval_20261123T043600Z.json` the long arm
stores `brier_B1=0.050000, brier_C2=0.049000, rel_brier_improvement_pct=-2.0, materiality_met=false`
(i.e. it computed improvement as `C2_minus_B1`, so a 2% *reduction* in Brier reads as -2.0%), while
`fclr_tracks01_recompute_20261123T043600Z.json` computes `rel_brier_improvement_pct=+2.0,
materiality_met=true` (improvement as `B1_minus_C2`) and honestly records `all_checks_match:false`.
Both still conclude **NOT_SUPPORTED** (the bootstrap CI includes zero and Holm fails, so the verdict
is robust to the sign error), but the two files disagree on the sign of the headline. This frozen
terminal artifact is NOT to be overwritten (RESEARCH_PROMPT.md §13). For YOUR campaign: pick ONE
explicit sign convention in the prereg (recommended: `relative_improvement = (baseline - candidate)/
baseline`, positive = candidate better), use it identically in the eval AND the recompute, and make
the recompute assert `all_checks_match:true` against the eval. If your recompute disagrees with your
eval, stop and reconcile before declaring a verdict.

---

## ROOT CONSTRAINTS (hard)

- Root md+json count: **499/500** — at cap. ALL new artifacts MUST go under `session_<UTC>/`. Do NOT add
  any root-level `research_state/*.md|*.json`.
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax the materiality floor after outcomes.
- Preserve nulls honestly: verdict may be `SUPPORTED_GENERALIZATION` or `NOT_SUPPORTED` (with evidence).
- Do NOT re-run any terminal campaign (see list above).
- Do NOT build a risk overlay (§9: forecast gate did not pass on ANY primary target).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md` (sealed FCLR-001 definition consumed by
  `scripts/run_evaluation.py`).
- Stdlib + pyarrow only; no network for heavy evaluation (source probes already done); no new source
  without provenance; no overlay.
- Do NOT track-adulterate: never describe a broad-universe cross-sectional association, Track B
  (modeled breach), or Track C (volatility) as proof of an observed-liquidation forecast gate pass;
  never claim a complete observed-liquidation census from a capped feed.
- **Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`** — cannot fire on frozen data; not a valid excuse
  to idle (§16, §19). The broad-universe generalization evaluation IS the action.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **No** prose-only / trigger-only / source-probe-only / audit-only / **prereg-only** / verify-and-stop /
  placeholder sessions.
- **The heavy evaluation (`fclr_liqxsecbroad01_eval_*`) and independent recompute
  (`fclr_liqxsecbroad01_recompute_*`) MUST be in the SAME session** — the gate fails a prereg-only
  session closed (`LIQ_XSEC_BROAD_ARTIFACTS_MISSING`).
- **Do NOT re-probe the network** — the source audit is frozen; re-probing wastes the session.
- **No** empty session directories.
- **Do NOT** write a future/non-existent `session_<UTC>` id into this handoff before that directory
  exists (the gate treats a non-existent recorded dir as a failure). Until you create and record your
  own real `session_<UTC>/`, the only literal `session_<digits>` tokens in this handoff are
  `session_20261122T190000Z`, `session_20261122T224500Z`, and `session_20261123T043600Z`.
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- **Do NOT** claim completion without the full `fclr_liqxsecbroad01_*` heavy artifact set under a new
  `session_<UTC>/` (UTC > `20261123T080000Z`).
- **Do NOT** threshold-shop or relax the materiality floor after outcomes; preserve nulls honestly.
- **Do NOT** re-run any terminal campaign.
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
- **Do NOT** build a risk overlay.
- **Do NOT** track-adulterate.

---

## VERIFICATION (run before declaring done)

```bash
# 1. Heavy-work gate must return reason=OK (not VERIFY_AND_STOP, not BLOCKED)
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Campaign gate unittests must pass
python3 -m unittest \
  tests.test_active_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_pooled_robust_002_campaign_gate \
  tests.test_tracka_hardening_143

# 3. Frozen 3-block domains exhausted (expected; not a blocker for this campaign)
python3 scripts/next_campaign_status.py
```

The gate fails closed if: this handoff lacks the markers, the newest on-disk session is not recorded
here, the newest session lacks the full `fclr_liqxsecbroad01_*` family (including
`fclr_liqxsecbroad01_eval_*` and `fclr_liqxsecbroad01_recompute_*`) + `evidence_audit_*.json` +
`trigger_check_*.json`, or any required file is zero bytes. Sessions predating `20261123T080000Z`
(including the current `session_20261123T043600Z`) are grandfathered, so THIS refresh is green.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. **Capped-sample feed — not a complete census (per §15).** Columns: `timestamp[ms],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. **Verified at refresh: 2,849,452 rows across 18 files, 468 distinct `market` instruments, span 2025-05-25 14:36:58 UTC .. 2026-10-31 23:30:10 UTC. There is NO `coin` column — the instrument key is `market`.** |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,funding_rate,premium`. |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,mark_price,oracle_price,open_interest,open_interest_usd`. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,dex,market_class,open,high,low,close,volume,trades`. |
| `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` | Frozen 15-coin combined metpie+ironflow panel (sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`), 1,740,415 rows, 2025-03-22..2026-10-31. The NARROW universe whose SUPPORTED findings (XSEC-004/005/006) you are testing for generalization. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate
caches. Data scale: ~158K liquidation rows/month; ~230K funding + ~220K OI + ~200K candle rows/month
across the broad universe. The heavy evaluation must stay tractable in pure stdlib + pyarrow
(chronological split, 168h test blocks, per-coin series — see the risk09 template pattern).

---

## KEY FILES TO READ BEFORE STARTING

- `research_state/experiment_frontier.json` — rank-0 is now
  `FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z` (status READY_EXECUTE, program ACTIVE). The prior
  `FCLR-TRACKA-SOURCE-AUDIT-01` is demoted to rank 1 SUPERSEDED_TERMINAL (completed NOT_SUPPORTED under
  session_20261123T043600Z).
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement (`LIQ_XSEC_BROAD_CAMPAIGN_RE`,
  `_liq_xsec_broad_state`; `fclr_liqxsecbroad01_*` required set incl. `fclr_liqxsecbroad01_eval_*` +
  `fclr_liqxsecbroad01_recompute_*`; `liq_xsec_broad` payload key).
- `research_state/session_20261123T043600Z/fclr_risk09_evaluation_20261122T224500Z.py` — the proven
  heavy stdlib+pyarrow evaluation template (sha256 guards, chronological 60/40 + purge, 168h blocks,
  per-coin block bootstrap, Holm, symmetric verdict). Adapt: intensity→rank-IC / cross-sectional.
- `research_state/session_20261123T043600Z/fclr_tracks01_eval_20261123T043600Z.py` — the most recent
  heavy eval (binary breach); shows the same sha256-guard + walk-forward + Holm structure.
- `research_state/final_synthesis_report.md` — the program-wide CONCLUDED verdict (no promotable
  funding-conditioned forecast skill; Track A blocked; overlay ineligible). Your campaign either
  confirms the narrow SUPPORTED cross-sectional finding generalizes or shows it was a small-universe
  artifact — both are publishable, durable results.
- `RESEARCH_PROMPT.md` §5 (source discovery), §7 (features), §8 (metrics), §9 (overlay gate), §15
  (label admissibility / capped feed), §16 (adaptive feasibility), §17 (promotion conditions),
  §3.2 (primary question two halves).
- `research_state/data_source_registry.json` — root-level registry (do NOT rewrite; root cap 499/500).

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why
2. Exact test outcomes with paths
3. Evidence added and full paths
4. State of each research gate
5. Single highest-value next task (if any)
6. Precise verifying command
7. Any blocker with next materially different route

Then record your `session_<UTC>/` id in this handoff (append the id string `session_<UTC>` so
`_latest_handoff_session` picks it up).

---

## BOTTLENECK RESOLUTION (this handoff)

- **Resolved (primary bottleneck — stale handoff body):** the prior handoff's header declared
  `FCLR-TRACKA-SOURCE-AUDIT-01` complete (NOT_SUPPORTED, session_20261123T043600Z) but its "INITIAL
  TASK MESSAGE" still instructed the next session to *perform* that campaign (recover the source audit
  from git, write the pivot prereg, run the heavy Track B eval). That self-contradiction would have
  made a future agent either redo completed work or stall. This refresh removes it: the new INITIAL
  TASK MESSAGE points at the genuinely-unfinished, repo-name-prioritized heavy campaign
  `FCLR-LIQ-XSEC-BROAD-01` (broad-universe generalization of the only SUPPORTED liquidation-risk
  findings). The now-moot "recover audit from git" section is removed.
- **Resolved (frontier drift):** `experiment_frontier.json` rank-0 still read
  `FCLR-TRACKA-SOURCE-AUDIT-01 ... status READY_EXECUTE / last_verdict NOT_STARTED` even though the
  campaign completed. This refresh demotes it to rank 1 SUPERSEDED_TERMINAL and installs
  `FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z` as the new rank-0 (READY_EXECUTE / ACTIVE), so a future
  agent reading the frontier sees the true state. The `test_active_campaign_gate.py` invariant
  (exactly one rank-0; non-rank-0 entries terminal) is preserved.
- **Resolved (enforcement):** a new gate binder (`LIQ_XSEC_BROAD_CAMPAIGN_RE` + `_liq_xsec_broad_state`
  + `LIQ_XSEC_BROAD_REQUIRED`) was added so a future agent cannot skip the heavy broad-universe
  evaluation. It is regression-pinned by
  `tests/test_tracka_hardening_143.py::TestLiqXsecBroadCampaignGate` (7 tests: required set contains
  eval+recompute; source-probe-only / missing-eval / missing-recompute / zero-byte fail
  `LIQ_XSEC_BROAD_ARTIFACTS_MISSING` / `..._EMPTY`; full heavy set passes; pre-start sessions
  grandfathered). `fclr_liqxsecbroad` was added to `NEW_QUANT_PREFIXES` so the eval counts as fresh
  heavy work. The campaign start `20261123T080000Z` is AFTER the current session
  `session_20261123T043600Z`, so the current session is grandfathered and THIS refresh stays green;
  the next session (UTC > `20261123T080000Z`) is forced to produce the full heavy set.
- **Noted (evidence defect, verdict unchanged):** the tracks01 recompute/eval sign discrepancy
  (see EVIDENCE NOTE) is documented, not overwritten (§13). Both files conclude NOT_SUPPORTED; the
  next campaign must use one explicit sign convention so its recompute asserts `all_checks_match:true`.
- **Verified (2026-11-23T08:31:12Z refresh):** `python3 scripts/check_handoff_heavywork_gate.py` →
  `PASS reason_code=OK root=499/500`. `TestLiqXsecBroadCampaignGate` (7) + `TestTrackaSourceAudit-
  CampaignGate` (7) + real-repo/CLI (4) = 19 tests OK. Ironflow bulk panels present (18 parquet each
  for liquidations/candles_1h/funding/open_interest). No external trigger pending.

---

## HANDOFF GENERATED: 2026-11-23T08:41:53Z
**Next session must use UTC > 20261123T080000Z** (campaign start gate; the current session
`session_20261123T043600Z` is grandfathered, so this refresh is green until a newer session appears).
**Latest handoff session: session_20261123T043600Z** (completed FCLR-TRACKA-SOURCE-AUDIT-01 heavy set:
Track B modeled-breach evaluation NOT_SUPPORTED on both arms; recovered source_registry/probe/
viability_decision triad + pivot_prereg).
**Rank-0 campaign: FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z** (broad-universe 342-coin generalization
test of the SUPPORTED regime-conditioned cross-sectional funding → next-hour observed-liquidation-
intensity findings; gate-enforced via `_liq_xsec_broad_state`, regression-pinned by
`TestLiqXsecBroadCampaignGate`).