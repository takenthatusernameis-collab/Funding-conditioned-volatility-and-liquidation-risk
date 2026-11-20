# FCLR-STARTER-001 evidence audit (20261120T024217Z)

{
  "experiment_id": "FCLR-STARTER-001-20261120T024217Z",
  "utc": "20261120T024217Z",
  "campaign": "FCLR-STARTER-001-20261119T231806Z",
  "step": 1,
  "title": "FCLR-STARTER-001 Step 1: protocol freeze + panel hash + B0/B1 baselines",
  "actions": [
    "Froze RESEARCH_PROMPT.md \u00a714 verbatim to research_state/protocol_fclr_starter_001_<UTC>.md (not the sealed research_state/research_protocol.md)",
    "Reused frozen panel research_state/fclr011_recompute_panel_20261115T234700Z.parquet; recorded panel_sha256 and source hashes before any target generation",
    "Ran B0 persistence (RV24h) and B1 HAR-OLS baselines on development/validation; holdout not opened"
  ],
  "artifacts": [
    "research_state/protocol_fclr_starter_001_20261120T024217Z.md",
    "research_state/session_20261120T024217Z/fclr_starter001_protocol_freeze_20261120T024217Z.json",
    "research_state/session_20261120T024217Z/fclr_starter001_panel_freeze_20261120T024217Z.json",
    "research_state/session_20261120T024217Z/fclr_starter001_baselines_20261120T024217Z.json",
    "research_state/session_20261120T024217Z/trigger_check_20261120T024217Z.json"
  ],
  "baseline_summary": {
    "B0_qlike": 0.5742793328125579,
    "B1_qlike": 0.5413234132343385,
    "n_obs": 2799,
    "holdout_opened": false
  }
}
