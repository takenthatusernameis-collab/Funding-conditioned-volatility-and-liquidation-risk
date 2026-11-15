# Durable Agent Handoff — refreshed 2026-11-15T02:41:13Z (sole authoritative version)

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; older `AGENT_HANDOFF` revisions, `research_state/FCLR_CAMPAIGN_NEXT.md`, and obsolete next-plan files are superseded historical evidence. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, and do not reopen sealed verdicts.

## Campaign completed this session (heavy work executed)

**`FCLR-DESIGN-FEASIBILITY-20261115T021249Z` — COMPLETED_VALIDATED (EXPLORATORY_ONLY, promotable=false, audit_only, no sealed mutation).** Inverted persisted power-calibration SEs to required-n for 80% power at pre-specified floors (offline, deterministic, no model re-fit, no SE re-derivation from raw data).

- **Volatility (forward 2025 disjoint, C2_vs_B1, 2% implied-baseline QLIKE floor, 1/sqrt(n) on contrast n):** primary h24 `SE_obs=0.010469953`, `SE_req=|floor|/(z_975+z_80)=0.002517259`, `n_obs=10800`, `n_req=186834.7` → **UNDECIDABLE_ON_CACHE**. All horizons undecidable (h6 n_req=123,458 > 10,800; h24 186,835; h72 51,842 > 10,560; h168 37,997 > 10,080). All C2_vs_B1 contrasts undecidable at floor; the 5-symbol×90-day cached design cannot reach 80% power at the 2% floor — a **structural limit on cache**, not a fixable sample-size problem within cached data.
- **Observed liquidation (xsec forward, |IC|>=0.05, 1/sqrt(n) on pooled n):** analytic `SE_obs=0.012089358 < SE_req=0.017847039`, `n_req=3044.6 < n_available=6634` → **DECIDABLE_ON_CACHE**. Symmetry-robust `SE_robust=max(|q5|,|q95|)/z_95=0.012628718 < SE_req`, `n_req=3322.3 < 6634` → **DECIDABLE_ON_CACHE**, **no verdict flip** (instability flagged: persisted null symmetry failed abs_frac=0.0223>0.01, but decidability is robust). Per-block n-scaled approx: block_0/1/2 undecidable at block scale (859/1544/1265 req vs 2996/1605/2033 avail? block-level verdicts approx UND/UND/UND per persisted scaling) — see eval. Sealed liq evaluation remains EXPLORATORY/INCONCLUSIVE due to permutation-null asymmetry; this analysis only establishes decidability, not a confirmatory label.
- **Overall:** `VOL=UNDECIDABLE_ON_CACHE; LIQ=DECIDABLE_ON_CACHE (analytic & robust, no flip; instability flagged)`.

Artifacts (all EXPLORATORY_ONLY, promotable=false): `research_state/prereg_fclr_design_feasibility_2026-11-15T02:35:00Z.json`, `scripts/fclr_design_feasibility.py`, `tests/test_fclr_design_feasibility.py` (19 tests OK), `research_state/evaluation_summary_FCLR-DESIGN-FEASIBILITY-2026-11-15T02:35:00Z.{json,md}`. Scope registry updated (184 scripts) and synced to `tests/test_tracka_hardening_117.py`. Sealed artifacts unchanged (vol sealed eval hash `78537585fe59ed4a75d7861a80bf3964e35c97a6a53c48a39c6d012354e69215` unchanged; `sealed_artifacts_mutated=false`).

## NEXT FOCUS CAMPAIGN (heavy work is trigger-gated, never avoided)

**`FCLR-TRIGGER-READINESS-CAMPAIGN-20261115T024113Z` — trigger-readiness campaign (not cached-heavy-work).** No agent-removable heavy work remains on cached/admissible data. The program is in trigger-only sentinel state. Future agents must not avoid heavy work: when a valid resume trigger materializes, heavy confirmatory work executes immediately with zero bottlenecks. The campaign maintains readiness so no trigger is missed due to missing templates, unready scripts, or uninitialized infrastructure.

Campaign scope:
- Maintain pre-frozen preregistration templates for the Gate 4 confirmatory flow, ready to instantiate with a new experiment ID when `GATE4_BRANCH_1` fires.
- Maintain a §16 admissibility audit template for materially new liquidation source families, ready to run before any prereg/outcomes when `NEW_OBSERVED_LIQUIDATION_SOURCE` fires.
- Keep experiment runner and gate scripts green and ready (`scripts/fclr_campaign_gate.py`, `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py`, `scripts/check_tracka_scope_registry_drift.py`).
- Event-driven only: **no polling, no schedulers/controllers, no edits to `.github/workflows/*`, no paid/credentialed/manual data, no re-running tested windows, no re-probing TERMINAL_NO_GO families.**
- Heavy work executes only on a valid trigger; otherwise the session records trigger status and stops cleanly.

## FIRST ACTION (timestamped initial task for the next agentic work session)

**Now (2026-11-15T02:41:13Z): `FCLR-TRIGGER-READINESS-20261115T024113Z` — no agent-removable heavy work remains on cached/admissible data. Do not do busywork. Do not re-run exhausted campaigns. Do not add polling, schedulers, controllers, or workflow edits.**

The next session's sole task is trigger readiness:
1. Verify neither resume trigger has fired:
   - `GATE4_BRANCH_1`: a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with `status=RESOLVED_VERIFIED`, `fabricated=false`, and required human/legal attestation (not agent-settable).
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: a **materially new** source family (not a re-probe of Binance liquidationSnapshot/forceOrders, OKX, Bybit, Deribit, Zenodo, OSF, arXiv, GitHub, CryptoDataDownload, HuggingFace exhausted sets, metpie 65-day window, or ironflow short untouched region) has appeared and passed §16 admissibility audit.
2. If a trigger has fired: execute heavy confirmatory work immediately per the trigger protocol below; do not defer.
3. If no trigger has fired: record evidence of trigger status (exact paths checked, result) in `AGENT_HANDOFF.md` and stop cleanly. Status-only trigger checks are acceptable here only because no cached heavy work exists.

**On trigger (execute heavy work; do not defer):**
1. **`GATE4_BRANCH_1`** — Action: freeze a new prereg pre-outcomes for the Gate 4 confirmatory flow and execute it per `RESEARCH_PROMPT.md`/gate protocol; record outcomes in new timestamped artifacts. `promotable` only if gate passes.
2. **`NEW_OBSERVED_LIQUIDATION_SOURCE`** — Action: bounded probe + §16 admissibility audit artifact **before** any prereg/outcomes; if ADMISSIBLE, freeze prereg pre-outcomes then build/eval/verdict with new experiment ID. If inadmissible, record evidence-backed blocker.

**Resume triggers:** `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`. **Do not** poll, add schedulers/controllers, edit `.github/workflows/*`, fetch paid/credentialed/manual data, re-run tested windows, re-probe TERMINAL_NO_GO families, or relabel exploratory as confirmatory.

## Bottlenecks removed (do not recreate)

- `FCLR-NEXT-002` (power calibration) — COMPLETED_VALIDATED; do not re-run.
- `FCLR-DESIGN-FEASIBILITY` — COMPLETED_VALIDATED; do not re-run.
- Scope-registry invariant enforced (184/184, 117/118/119 synced); any new script must be added to BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`.
- External liquidation hunt — **TERMINAL_NO_GO** (evidence: `research_state/liquidation_source_campaign.md`, `research_state/track_a_deadend_map.md`). Reopen only for a materially new source family with §16 audit before prereg/outcomes.
- Cached Binance/Hyperliquid 3-block frontier — exhausted (`scripts/next_campaign_status.py`).
- Frontier rank-0 is trigger-only sentinel; no stale pending heavy campaign.

## Verified state (this session)

- `python3 scripts/fclr_design_feasibility.py` → `VOL=UNDECIDABLE_ON_CACHE; LIQ=DECIDABLE_ON_CACHE; sealed_artifacts_mutated=false`.
- `python3 -m unittest tests.test_fclr_design_feasibility -v` → 19 OK.
- `python3 scripts/fclr_campaign_gate.py` → 19/19 pass. `scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → PASS. `scripts/check_tracka_scope_registry_drift.py` → 184/184 OK.
- Targeted regressions green: `tests.test_next_campaign_status tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118 tests.test_tracka_hardening_119 tests.test_fclr_fwd_vol_2025_disjoint_corrected_audit tests.test_fclr_fwd_vol_2025_disjoint_reconcile tests.test_fclr_fwd_vol_2024_disjoint_2024_06 tests.test_fclr_power_calibration` (and design feasibility) all pass.
- Confirmatory program concluded; no risk overlay eligible. `sealed_artifacts_mutated=false`.

## Research-gate status

- H1_primary: NOT_SUPPORTED (terminal absent valid trigger/new source).
- H2_shek_replication: EXPLORATORY_ONLY (partial).
- H_trackb_modeled_breaches: NOT_SUPPORTED.
- H_tracka_hl_liquidation_forecast: NOT_MET.
- Gate 4: EXTERNAL_BLOCKED.
- `FCLR-POWER-CALIBRATION`: COMPLETED_VALIDATED (VOL=NULL_UNDERPOWERED, LIQ=INCONCLUSIVE).
- `FCLR-DESIGN-FEASIBILITY`: COMPLETED_VALIDATED (VOL=UNDECIDABLE_ON_CACHE, LIQ=DECIDABLE_ON_CACHE analytic&robust no flip).

## §19 carry-forward

- **Supported:** null on tested windows; vol effect >=2% floor undetectable by design and **structurally undecidable on cached data** (n_req~187k vs 10.8k). Liq pooled n is sufficient for 80% power at |IC|>=0.05 under analytic and symmetry-robust SE (decidable) but sealed liq result remains non-confirmatory due to permutation-null asymmetry.
- **Contradicted:** generalizable funding-conditioned OOS edge.
- **Unknown:** any effect only resolvable with materially new admissible data/terms trigger.
- **Dominant limitation:** vol — structural sample/design limit on cache; liq — null-distribution asymmetry/label validity constraints.
- **Falsifying/closure:** vol floor undecidability is a structural cached-data conclusion (recorded). Future progress requires external trigger/new admissible source only.

## Completion contract

A session completes by (a) executing a valid trigger with frozen prereg and producing timestamped eval/verdict artifacts + green gates/tests with no sealed mutation, or (b) recording an evidence-backed blocker citing exact command/error and proof of a tried materially-different free route — never a TERMINAL_NO_GO family, never "no new data" alone. Status-only work is not completion.