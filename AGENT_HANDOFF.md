# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-29T19:45:19Z
Default branch: main
Current HEAD: `da10c7fa500daaeedcc696059d740fec2feb88a8` on `main` (branch up to date with origin/main). Working tree clean apart from untracked `__pycache__` under `scripts/` and `tests/`. No commit made this session (working-tree update only).

## Mission (unchanged)
Read and follow `RESEARCH_PROMPT.md`. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

## Current verified state (INCONCLUSIVE)
- **FCLR-001 (BTCUSDT-only pilot)**: NOT_MET / PILOT/INCONCLUSIVE. C2 vs B1 -2.50% with CI crossing zero; evaluated panel BTCUSDT-only (1634 eval rows) so >=5-instrument gate never met. See `research_state/evaluation_summary.md`, `research_state/gate_assessment.md`, `research_state/coverage_audit_recheck.md`.
- **FCLR-002 (5-symbol panel)**: NOT_MET / INCONCLUSIVE. Primary contrast C2 vs B1 numerically passes (-9.28% relative QLIKE, 95% CI [-0.097648, -0.008788] excludes zero) and was independently reproduced byte-identical (`research_state/evaluation_summary_FCLR002_REPRO.md`, `scripts/_repro_run_evaluation.py`). **Blocker:** minimum claim-worthy test requires >=3 non-overlapping 30-day evaluation blocks across >=5 instruments; test window is 70 days (2024-07-23..2024-09-30) = only 2 blocks + remainder. Holdout NOT opened per `research_state/research_protocol.md` §6/§9 and must not be reopened/recomputed.
- **FCLR-H003 (synthetic boundary breach, Track B)**: INCONCLUSIVE on both panels, no incremental skill over volatility-only baseline. Labels are synthetic/modeled proxies, not observed liquidations (`research_state/evaluation_summary_h003.md`, `research_state/evaluation_summary_h003_FCLR002.md`).
- **FCLR-H002 (Shek funding-correction)**: PARTIAL_REPLICATION — full paper methodology not independently reconstructible from public sources alone.
- **FCLR-H004 (observed liquidation outcomes, Track A)**: BLOCKED/NOT VIABLE — no complete unauthenticated public liquidation census found (`research_state/liquidation_sources_enumeration.md`). Track B/C remain the only admissible paths for liquidation-related stress proxies.
- **Risk-overlay**: INELIGIBLE until a forecast gate passes.
- **Tests**: `python3 -m pytest tests/ -q` → **51 passed**, 1.20s (Python 3.12.3, /usr/bin/python3). Frozen artifacts/splits/protocols unchanged.

## Bottlenecks (remove or route around)
1. **FCLR-002 block-count gate (hard blocker)**: 70-day test window yields only 2 non-overlapping 30-day blocks. Cannot claim pass under pre-registered criterion. Cannot extend by opening/reusing holdout or changing frozen splits.
2. **Track A unavailable**: No admissible complete census; do not infer zeros.
3. **FCLR-001 underpowered/coverage-limited**: BTCUSDT-only panel never met >=5-instrument gate.
4. **Handoff churn / agent loop friction**: Prior sessions hit edit-tool argument errors and timeout churn (see `research_state/workflow_run_diagnostics.jsonl`). Treat as process debt to avoid.

## Initial task message for next agent (SINGLE DURABLE HANDOFF)
```
[2026-10-29T19:45:19Z] FOCUS CAMPAIGN: "Extend the claim-worthy test window without touching frozen artifacts"

Repo: Funding-conditioned-volatility-and-liquidation-risk. Priority = volatility forecasting first (gates), liquidation stress only via Track B/C.

READ FIRST (in order): AGENT_HANDOFF.md, RESEARCH_PROMPT.md, research_state/research_protocol.md (FCLR-001/FCLR-002), research_state/fclr002_coverage_audit.json, research_state/evaluation_summary_FCLR002_REPRO.md, research_state/liquidation_sources_enumeration.md.

CONSTRAINTS (NON-NEGOTIABLE): No paid services/trials/keys/manual files/user intervention/live/paper trading. Do not modify .github/workflows. Do not open/reuse sealed holdouts, do not change frozen splits/protocols/evaluations. Do not fabricate results. Preserve negative/inconclusive results.

HEAVY WORK OBJECTIVE (do not stop at "no valid step"):
Pre-register FCLR-003 as a NEW experiment (separate from frozen FCLR-001/FCLR-002). Goal: construct a longer common 5-symbol panel (BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT) that yields >=3 non-overlapping 30-day blocks in test/holdout while using identical features/baselines/contrasts/metrics/block-bootstrap/multiplicity as FCLR-002.

EXECUTE THIS CAMPAIGN:

1. VERIFY STATE
   - git rev-parse HEAD -> da10c7fa500daaeedcc696059d740fec2feb88a8
   - python3 -m pytest tests/ -q -> 51 passed
   - Read coverage audits and confirm frozen boundaries.

2. MAP AVAILABLE COVERAGE (HEAVY DATA WORK)
   - Inventory all hourly mark/index/funding/premium data under repo (including zips like BNBUSDT-1h-*.zip). Build a coverage matrix: per symbol, earliest/latest, contiguous ranges, gaps.
   - Compute common intersection across all 5 symbols for 2024 (and extend if needed) to find a window with >=90 days of contiguous/common coverage post-train/val embargo structure.
   - Document in research_state/fclr003_coverage_audit.md (new artifact). Do NOT overwrite fclr002_coverage_audit.json.

3. PRE-REGISTER FCLR-003 (BEFORE ANY EVALUATION)
   - Create research_state/research_protocol_fclr003.md (v1.0) freezing: universe, targets (24h RV primary), B0/B1/C1/C2, splits with 7-day embargo, >=3 non-overlapping 30-day test blocks, materiality >=2%, Holm, block-bootstrap >=2000 reps, block_hours~24h. Explicitly state "no reuse of FCLR-001/FCLR-002 sealed holdouts".
   - Register hypotheses if needed in hypothesis registry (append only, no edits to frozen entries).
   - Get leakage-audit checklist ready for FCLR-003 panel.

4. BUILD PIPELINE EXTENSION (ENGINEERING HEAVY)
   - Extend data loading to support the FCLR-003 window. Add fixtures/tests for new window logic.
   - Implement evaluation path that reads ONLY FCLR-003 protocol/splits (never hardcode FCLR-002 boundaries). Add unit tests.
   - Ensure all feature computations remain causal (training-only stats). No tuning on test.

5. RUN & REPORT (ONLY IF FULLY PRE-REGISTERED)
   - If >=3 blocks exist with clean coverage/embargo: run FCLR-003 evaluation (log hashes/config). Write research_state/evaluation_summary_FCLR003.md with full uncertainty, block breakdown, leave-one-instrument-out, multiplicity. Update gate assessment.
   - If coverage is insufficient for >=3 blocks despite extending search: document exact shortfall, list every admissible unauthenticated source tried (with URLs/status), and conclude INCONCLUSIVE with concrete next data path that does NOT violate constraints. Do NOT stretch blocks or change criterion.

PARALLEL TRACK (if blocked on data volume):
- Tighten Track B (synthetic boundary) robustness for FCLR-003 panel: calibration, rare-event metrics, horizon sensitivity, assumption disclosure. Keep clearly labeled as modeled proxy.
- Strengthen leakage audit with automated checks (timestamp alignment, embargo enforcement) as reusable tests.

BOTTLENECK REMOVAL RULES:
- Do not re-run or "verify" frozen FCLR-002 holdout. Treat as complete evidence for that criterion.
- Do not create wrapper scripts that just reprint old results.
- Every commit of work must be measurable (new artifact, tests, coverage matrix, pre-registration).
- If you hit agent-loop friction (edit tool errors/timeouts), fix the smallest root cause in scripts/tests (outside .github/workflows) or work around deterministically.

ACCEPTANCE AT END: Update AGENT_HANDOFF.md with HEAD, test results, exact files created/modified, coverage findings, FCLR-003 pre-registration status, evaluation status (ran/not possible), blockers, and a single clear initial task message for the next agent. State remains INCONCLUSIVE until FCLR-003 passes gate; do not claim pass for FCLR-002.
```
