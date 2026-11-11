# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, authoritative):** 2026-11-11T16:02:32Z
**Status:** AUTHORITATIVE. This is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. `AGENT_HANDOFF.md` is a redirect only. Any doc conflicting with this handoff is stale. Read fully before acting. **No status-only output.**

## INITIAL TASK MESSAGE (EXECUTE NOW) — 2026-11-11T16:02:32Z

**Mission (repo-prioritized):** `Funding-conditioned-volatility-and-liquidation-risk` requires **liquidation-risk forecasting co-equal with volatility forecasting**, on admissible unauthenticated data with provenance. Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0) has now been fully executed; Track B/C (2024) are closed negative; Gate 4 is external-blocked. Future agents must not idle or report status only — execute the first applicable heavy-work branch below and produce the required artifacts.

### Completed this session (do not relitigate / do not redo)
- **RV-context bottleneck removed (bounded, unauthenticated, first-time acquisition, not redundant polling):** Hyperliquid `candleSnapshot` 1h cached for 2026-05-01..2026-10-31, 9 symbols (BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI), 54 coin-months, 0 errors. Cache: `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json`. Fetch report: `research_state/tracka_hl_candle_fetch_report_20261111T160053Z.json`.
- **Track A successor prereg fully evaluated (Path b completed):** prereg `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` (TRACKA-HL-S-20261111T133430Z, frozen pre-outcomes). RV panel: `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet` (sha256 `503bda8c...`, 1656 buckets, 1647 w/ RV24h, 1434 w/ label, 1385 complete label+funding+RV, 9 symbols) + `research_state/tracka_hl_panel_with_rv_build_report_20261111T160124Z.json`.
- **Track A verdict (terminal for this prereg):** `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md` — **NOT_MET**. Primary contrast C2 vs B1 (QLIKE, next-24h observed liquidation intensity, 7d embargo, 3 non-overlapping 30d test blocks, block bootstrap 2000 reps seed 20261111): B1 mean 72.133883, C2 274.514250 (n=693, 9 instruments); diff (C2-B1) +202.380367, 95% CI [15.418948, 443.775055], rel reduction -280.56% (C2 worse); gate fails on reduction/CI direction, passes instrument/block counts. Prior context-insufficient closure: `research_state/evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md` (superseded by completed evaluation).
- **State updated atomically:** `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_liquidation_forecast → NOT_MET), `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum appended; 2024 H001 record preserved). Git HEAD at time of run recorded in manifest.

---

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH (no status-only output)

### Branch 1 (CONDITIONAL, execute immediately if artifact exists): Gate 4 / Track C volatility unblocking
**Trigger:** a valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and a human/legal reviewer attestation.
**Actions (deterministic, in order):**
1. Run promotion/dry-run and admissibility validators as specified by Gate 4 tooling (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or repo equivalents) with `--expect-go` semantics where applicable.
2. Only on all-green GO, execute confirmatory Track C multi-split ablation on the frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds) with frozen artifacts.
3. Emit verdict artifact(s) under `research_state/` and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If trigger absent:** Gate 4 remains `EXPLICIT_BLOCKER_UNRESOLVED` (current: `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, fabricated=false). **Agents must NOT set `RESOLVED_VERIFIED` or `fabricated=true` and must NOT bypass/fabricate terms evidence.** Proceed to Branch 2.

### Branch 2 (DEFAULT heavy campaign while Gate 4 blocked): New admissible liquidation/volatility evidence & claim-worthy panel
**Objective:** advance the repo’s core question on **liquidation-risk and/or volatility** without reusing sealed holds or blocked routes. This is mandatory heavy work (not a status check).
1. **Inventory & gap audit (bounded, concrete):** map cached admissible assets already present but unexploited for a *new* pre-registered claim (e.g. unused ironflow months/symbols beyond 2026-05..2026-10 where matching admissible decision-time predictors can be constituted; other observed liquidation datasets in `data_cache`/repo with verifiable unauthenticated provenance; existing Hyperliquid funding/candle coverage vs label coverage). Produce a short audit artifact `research_state/next_panel_gap_audit_<UTC>.md/json` citing exact paths/hashes/coverage windows.
2. **Source acquisition/provenance (if a candidate gap is fillable by admissible unauthenticated data):** fetch/cache first-time only (no redundant polling), record provenance (URL/access time/license/auth/API-key/requester-pays/signature status/checksums). Ironflow/Hyperliquid unauthenticated patterns are admissible precedents; Binance/2024 must not be conflated with Hyperliquid claims.
3. **Pre-register BEFORE any outcome computation:** freeze hypothesis, panel/window/symbols, label definition (observed only for Track A; clearly modeled/proxy only if Track B and labeled as such), features, splits/embargo, baselines/contrasts, metric, materiality gate, minima (>=5 paired instruments, >=3 non-overlapping test blocks where required) in `research_state/*prereg*<UTC>.json` and/or md with hashes.
4. **Build panel + evaluate + verdict:** deterministic build from cached inputs, leakage/embargo checks, run pre-registered evaluation, emit `research_state/evaluation_summary_*<verdict_id>.md` and update frontier/registry/manifest/final verdict atomically.
5. **If no claim-worthy admissible path exists after documented audit:** emit `research_state/next_panel_gap_audit_<UTC>.md` proving exhaustion (what was checked, why minima/provenance fail) and update frontier with precise resume triggers/new-source requirements — still a concrete artifact, not status-only.

**Priority:** Track A / liquidation-risk extensions on observed data first (repo name), then volatility extensions on admissible untested panels. Any new liquidation claim must use observed labels with verifiable provenance (no modeled/proxy presented as observed).

---

## Closed / do not relitigate
- Track A successor prereg `TRACKA-HL-S-20261111T133430Z` (2026-05-01..2026-10-31): **evaluated, NOT_MET** (`evaluation_summary_TRACKA-HL-20261111T160124Z.md`). Do not re-run without a new pre-registered design/data.
- Track B/C confirmatory (2024): closed negative (H001/Track B NOT_SUPPORTED). Sealed holds (FCLR-002/003/Track B/C test sets) immutable — **no reuse, no threshold-shopping**.
- Prior Track A terminal context-insufficient verdict: `evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md` (historical, superseded by completed eval).

## Hard bans (unchanged)
- No outcome inspection before freeze/preregistration.
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed (Track A requires observed ironflow or equivalent with provenance).
- No threshold-shopping; no sealed-holdout reuse.
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance is allowed).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no bypass of Gate 4 human/legal terms.
- **No status-only output:** every session must leave a substantive artifact (verdict, prereg, panel+report, or gap/exhaustion audit) and consistent state updates when work is performed.

## Key refs
- Track A: `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`, `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`, `research_state/tracka_hl_panel_with_rv_build_report_20261111T160124Z.json`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`
- Baseline checks (as relevant): `python -m unittest discover -s tests -v`

**End of Handoff — Execute the INITIAL TASK MESSAGE now (Branch 1 if Gate 4 resolved, else Branch 2 heavy campaign).**
