# Evidence Audit — session_20261118T114500Z

- **Timestamp (UTC):** 20261118T114500Z
- **Campaign:** `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` (breach-forecast heavy execution; triggers all OPEN)
- **Network used:** none. No installs, no `git lfs pull`, no HF probes.
- **Writes:** session dir only + `AGENT_HANDOFF.md` (sole durable handoff). No root `research_state/*.md|json` added (root 500/500 at cap).

## Tracks completed
### Track C — Design A exploratory forecast (carried forward from session 093031Z)
- Artifacts: `trackc_design_a_forecast_20261118T093031Z.{py,json,md}`.
- Headline: funding-trail features improve QLIKE vs RV-only (mean delta -0.3579, CI95 [-0.4980, -0.1932]); label EXPLORATORY/PILOT.

### Track B — Modeled boundary-breach labels (carried forward from session 093031Z)
- Artifacts: `trackb_breach_labels_20261118T093031Z.{py,json,md}`; `recompute_trackb_breach_labels_20261118T093031Z.json`.
- Label type `synthetic_modeled_boundary_breach`; observed_liquidation_labels=false. Rows: 41760; breached: 1418; overall breach rate: 0.03395593869731801.

### Track B/C breach-forecast (executed this session)
- Artifacts: `trackbc_breach_prereg_20261118T114500Z.{json,md}`; `trackbc_breach_forecast_20261118T114500Z.{py,json,md}`; `recompute_trackbc_breach_forecast_20261118T114500Z.json`.
- RV-only baseline vs funding-conditioned candidate, 2024-04, 2 chronological splits, block bootstrap seed 12345. Pooled mean Delta AUC -0.0661; materiality floor (Delta AUC >= +0.01, CI95 lo > 0) NOT met; funding-conditioned did NOT improve breach discrimination. EXPLORATORY/PILOT; no confirmatory claim.

## Trigger check
- `trigger_check_20261118T114500Z.json`: all four reopen triggers OPEN; none fired; no network.

## Fresh quantitative artifact
- `recompute_trackbc_breach_forecast_20261118T114500Z.json` (new-style heavy: evidence audit + fresh quant).

## Prohibitions respected
- No sealed re-score, no network, no root `research_state/*.md|json`, no sealed-artifact/workflow mutation.

## Honest status
- EXPLORATORY/PILOT. Execution campaign satisfied with substantive artifacts; negative funding-conditioned result reported as-is; no confirmatory promotion claimed.
