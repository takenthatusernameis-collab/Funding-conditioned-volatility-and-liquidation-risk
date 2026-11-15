# Durable Agent Handoff — refreshed 2026-11-15T02:58:10Z (sole authoritative version)

**SOLE DURABLE HANDOFF — START HERE.** `NEXT_SESSION_HANDOFF.md` is a tombstone; older `AGENT_HANDOFF` revisions, `research_state/FCLR_CAMPAIGN_NEXT.md` (self-superseded historical ref), and obsolete next-plan files are superseded evidence. This file is the only active handoff. Do not write status-only notes, do not re-probe exhausted families, and do not reopen sealed verdicts.

## Trigger verification (this session, 2026-11-15T02:58:10Z)

- `GATE4_BRANCH_1`: `glob research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` → **none found**. No `status=RESOLVED_VERIFIED`/`fabricated=false` + required human/legal attestation artifact present. **NOT FIRED.**
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: no new materially different admissible liquidation source artifact found in repo; exhausted/terminal families remain closed (Binance liquidationSnapshot/forceOrders, OKX, Bybit, Deribit, Zenodo, OSF, arXiv, GitHub, CryptoDataDownload, HuggingFace exhausted sets, metpie 65-day window, ironflow short untouched region) per `research_state/liquidation_source_campaign.md`, `research_state/track_a_deadend_map.md`. `python3 scripts/next_campaign_status.py` → **no feasible 3-block design in ANY domain**. **NOT FIRED.**
- Readiness gates (cached, no re-probe): `python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py` → PASS; `python3 scripts/check_tracka_scope_registry_drift.py` → 184/184 OK. `python3 scripts/fclr_campaign_gate.py` → 18/19 pass, blocking `A0` (historical fullhistory bulk-cache verification context; not an agent-removable cached heavy-work item absent trigger/new admissible bulk cache change).

## Campaign completed prior session (sealed, do not rerun)

**`FCLR-DESIGN-FEASIBILITY-20261115T021249Z` — COMPLETED_VALIDATED (EXPLORATORY_ONLY, promotable=false, audit_only, no sealed mutation).**
- Vol (forward 2025 disjoint, C2_vs_B1, 2% implied-baseline QLIKE, 1/sqrt(n)): primary h24 `n_req=186,835 > n_available=10,800` → **UNDECIDABLE_ON_CACHE** (all horizons/contrasts undecidable at floor for C2_vs_B1-relevant scale) — structural cached-data limit.
- Liq (xsec forward, |IC|>=0.05, 1/sqrt(n)): analytic & symmetry-robust `n_req < 6,634` → **DECIDABLE_ON_CACHE** (no verdict flip; instability flagged from persisted null asymmetry). Sealed liq remains non-confirmatory (permutation-null asymmetry), decidability only.
Artifacts: `research_state/prereg_fclr_design_feasibility_2026-11-15T02:35:00Z.json`, `scripts/fclr_design_feasibility.py`, `tests/test_fclr_design_feasibility.py`, `research_state/evaluation_summary_FCLR-DESIGN-FEASIBILITY-2026-11-15T02:35:00Z.{json,md}`. `sealed_artifacts_mutated=false`.

## NEXT FOCUS CAMPAIGN (heavy work is trigger-gated, never avoided)

**`FCLR-TRIGGER-READINESS-CAMPAIGN-20261115T025810Z` — trigger-only sentinel (not cached-heavy-work).** No agent-removable heavy work remains on cached/admissible data. Future agents must not avoid heavy work: **when a valid resume trigger materializes, execute heavy confirmatory work immediately with zero bottlenecks.**

- Maintain readiness: pre-frozen prereg templates for Gate 4 confirmatory flow ready to instantiate on `GATE4_BRANCH_1`; §16 admissibility-audit template/readiness for materially new liquidation source families before any prereg/outcomes on `NEW_OBSERVED_LIQUIDATION_SOURCE`. Keep runners/gates/scope green.
- Event-driven only: **no polling, no schedulers/controllers, no edits to `.github/workflows/*`, no paid/credentialed/manual data, no re-running tested windows, no re-probing TERMINAL_NO_GO families.**

## FIRST ACTION (timestamped, mandatory for next agentic work session)

**Now: `FCLR-TRIGGER-CHECK-20261115T025810Z` (execute on session start).**
1. Re-verify triggers (exact checks, record paths/results in this file if materially changed):
   - `GATE4_BRANCH_1`: look for `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and required human/legal attestation (not agent-settable).
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: materially new source family (not a re-probe of exhausted/terminal families listed above) that can pass §16 admissibility audit.
2. **If `GATE4_BRANCH_1` fired (HEAVY):** immediately freeze a new prereg pre-outcomes for Gate 4 confirmatory flow and execute per `RESEARCH_PROMPT.md`/gate protocol; produce timestamped eval/verdict artifacts + green gates/tests, no sealed mutation. `promotable` only if gate passes.
3. **If `NEW_OBSERVED_LIQUIDATION_SOURCE` fired (HEAVY):** immediately run bounded probe + §16 admissibility audit artifact **before** any prereg/outcomes; if ADMISSIBLE, freeze prereg pre-outcomes then build/eval/verdict with new experiment ID; if inadmissible, record evidence-backed blocker. Do not relabel exploratory as confirmatory.
4. **If neither fired:** do not do busywork or status churn; stop cleanly after confirming readiness artifacts/scripts are intact. Cached heavy-work frontier is exhausted — absence of a trigger is the only blocker.

**Resume triggers:** `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`. **Forbidden:** polling, schedulers/controllers, `.github/workflows/*` edits, paid/credentialed/manual data, re-running tested windows, re-probing TERMINAL_NO_GO families, reopening sealed verdicts.

## Bottlenecks removed (do not recreate)

- `FCLR-NEXT-002` (power calibration) — COMPLETED_VALIDATED; do not re-run.
- `FCLR-DESIGN-FEASIBILITY` — COMPLETED_VALIDATED; do not re-run.
- Scope-registry invariant enforced (184/184, 117/118/119 synced); new scripts must be added to BOTH `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py` `SCRIPT_REGISTRY`.
- External liquidation hunt — **TERMINAL_NO_GO**; reopen only for materially new source family with §16 audit before prereg/outcomes.
- Cached Binance/Hyperliquid 3-block frontier — exhausted (`scripts/next_campaign_status.py`).

## Research-gate / §19 carry-forward (unchanged)

- H1_primary: NOT_SUPPORTED (terminal absent valid trigger/new source). H2_shek_replication: EXPLORATORY_ONLY (partial). H_trackb_modeled_breaches: NOT_SUPPORTED. H_tracka_hl_liquidation_forecast: NOT_MET. Gate 4: EXTERNAL_BLOCKED.
- `FCLR-POWER-CALIBRATION`: COMPLETED_VALIDATED (VOL=NULL_UNDERPOWERED, LIQ=INCONCLUSIVE). `FCLR-DESIGN-FEASIBILITY`: COMPLETED_VALIDATED (VOL=UNDECIDABLE_ON_CACHE, LIQ=DECIDABLE_ON_CACHE analytic&robust no flip).
- **Supported:** null on tested windows; vol effect >=2% structurally undecidable on cached data (n_req~187k vs 10.8k). Liq decidable at pooled n but sealed non-confirmatory (null asymmetry). **Contradicted:** generalizable funding-conditioned OOS edge. **Unknown:** effects resolvable only with new admissible data/terms trigger. **Dominant limitation:** vol structural cache/design; liq null-distribution asymmetry/label validity.

## Completion contract

Complete by (a) executing a valid trigger with frozen prereg and producing timestamped eval/verdict artifacts + green gates/tests with no sealed mutation, or (b) recording an evidence-backed blocker citing exact command/error and proof of a tried materially-different free route — never a TERMINAL_NO_GO family, never "no new data" alone. Status-only work is not completion.
