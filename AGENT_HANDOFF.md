# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T123000Z
Git SHA (HEAD): dd188ea1
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T123000Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: SOURCE-REOPEN + GUARDRAIL HOLD

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-052-SOURCE-REOPEN-AND-GUARDRAIL-HOLD
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY | NO SEALED RE-RUN | NO THRESHOLD SHOPPING | NO TRADING)
CAMPAIGN: FCLR-NEXT-052-SOURCE-REOPEN-CAMPAIGN
TIMESTAMP (UTC): 20261104T123000Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk — Track C (funding-conditioned volatility) is the repo-name priority, but its confirmatory program is CLOSED (H001 NOT_SUPPORTED). Track A (observed liquidations) FCLR-010 gate PASSED/SEALED; overlay HYPOTHETICAL_ONLY. Track B CLOSED_NEGATIVE. H002 PERMANENT_BLOCKED (SSRN 403).
OBJECTIVE: Keep the program alive and guardrails intact. Execute NON-SKIPPABLE HEAVY WORK every session. The ONLY resume trigger that reopens confirmatory execution is NEW admissible unauthenticated data passing the full rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK, unauthenticated/no_keys) PLUS a fresh pre-registration written BEFORE any outcome inspection. Until that trigger fires, do NOT re-run sealed cells, do NOT tune on holdouts, do NOT threshold-shop, do NOT fabricate data, do NOT merge tracks, do NOT touch .github/workflows.

MANDATORY PER-SESSION HEAVY WORK (EXECUTE ALL, EVERY TURN — NO SKIPPING):
(1) CHECK FOR NEW EVIDENCE
    - Read research_state/ironflow_monitor_state.json: last_probe, new_files_found, data_through, consecutive_absent.
    - Probe Binance archive head for klines/1h, markPriceKlines/1h, indexPriceKlines/1h, premiumIndexKlines/1h, fundingRate beyond 2026-11-02 (data.binance.vision + github mirror). Record method, URL, HTTP status, bytes, Content-Type, first/last timestamps; sum(volume,taker_buyQuoteVolume,taker_buyBaseVolume)>0 required for klines; reject zero-volume placeholders and HTTP 206 partials without full validation.
    - If new_files_found non-empty for month >= 2026-11 (Track A) OR admissible Binance panel beyond 2026-11-02 with real mark/index/premium volume >= 3 non-overlapping 30-day blocks (Track C) -> go to (2).
    - Otherwise -> go to (3) BLOCKED PATH.

(2) NEW DATA PATH (only on verified new admissible data)
    - CREATE fresh pre-registration BEFORE inspecting outcomes (new experiment ID, protocol ref, frozen splits/metrics/gate/embargo/block-bootstrap, pre_registered_before_outcomes=true).
    - Run the corresponding frozen harness immediately (scripts/fclr010_harness.py for Track A; Track C run per new pre-registration).
    - Write research_state/evaluation_summary_<NEW_EXPERIMENT>_<UTC>.md with calibration/Brier, LOO, concentration, block-bootstrap CIs (>=2000 reps), Holm multiplicity, gate assessment.
    - Update research_state/experiment_frontier.json; commit evidence (code/manifests/reports only, no raw data).

(3) BLOCKED PATH — MANDATORY HEAVY WORK (EXPECTED CASE — NO NEW DATA). Complete ALL four sub-items. A session that skips any sub-item FAILS.
    3A STRENGTHEN AUTOMATION (cannot skip): improve scripts/monitor_ironflow_liquidations.py and/or scripts/hunt_alternative_liquidation_sources.py — retry/backoff, broader unauthenticated probes, smarter failure classification, ETag/state-aware diff, wider lookahead. Evidence: modified script + fresh probe output.
    3B ADD TESTS (cannot skip): extend tests/ covering state-diff, ETag caching, month-window, classification, pagination, missing-history, duplicates, delistings, symbol mapping, forward-label leakage, split embargoes. Run: python -m unittest discover -s tests -v (must stay green, >=117).
    3C UPDATE BLOCKER DOC (cannot skip): write research_state/watch/gap_analysis_<UTC>.md with complete probe tables (all URLs tried, status codes, headers, body previews), exact resume conditions (paths/patterns/URLs/months to watch), concrete timestamps, next probe schedule (every 30-120 min).
    3D UPDATE FRONTIER (cannot skip): update research_state/experiment_frontier.json with precise resume triggers and refreshed blocked-cell status.

(4) INTEGRITY ENFORCEMENT (cannot skip)
    - git diff --name-only .github/workflows MUST be empty.
    - Verify sealed experiments unchanged: FCLR-001/002/003/006/007/008/010/011 (hash-check against manifests).
    - Firewall intact: Hyperliquid ironflow (Track A) ONLY; no Binance<->Hyperliquid mixing; modeled != observed; volatility skill != liquidation predictability.
    - Delete scripts/__pycache__/*.pyc and tests/__pycache__/*.pyc.
    - No sealed re-runs, no threshold-shopping, no fabricated data, no trading, no holdout reuse.

(5) PERSIST ARTIFACTS (MANDATORY)
    - Write research_state/watch/trigger_harden_<UTC>.json with: inventory_diff, probes_table (with rejection rationale), prereg_status, execution_status (FIRED|BLOCKED_BY_GAP), gap_analysis (if blocked), gating_proof, integrity_hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands, bottleneck_remediation_plan.
    - Update AGENT_HANDOFF.md if state changed (keep this as the single durable handoff).
    - Research note only when it adds information/changes priorities/records a decision.

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed deterministic. Holm correction. No workflow changes. No trading. Track C > Track A > Track B by repo name. Firewalls enforced. Negative/inconclusive preserved. Bottlenecks removed via concrete actions, not status updates. Every session MUST produce measurable progress.
```

## 1) Current Verified State (20261104T123000Z)
- Tests: 117/117 OK (`python -m unittest discover -s tests -v`)
- Git HEAD: dd188ea1; working tree clean except __pycache__ (delete per step 4)
- Repo focus by name: Track C (funding-conditioned volatility) PRIORITY — but confirmatory CLOSED
- Track C (H001): NOT_SUPPORTED, CONFIRMATORY_CLOSED. All powered confirmatory runs gate NOT_MET (FCLR-003 +4.30% CI crosses zero; FCLR-006/-69.90%; FCLR-007/-3.42%; FCLR-008 +4.30% CI crosses zero; FCLR-011 gate PASSED numerically but program closed). FCLR-012-V forward (2026-08-07..2026-11-02) INCONCLUSIVE: 5-day test window = 0 non-overlapping 30-day blocks, CI spans zero. Binance archive effectively ends ~2026-11-02/03 (HTTP 404 beyond); 2026-11-03 klines have real volume but markPriceKlines/indexPriceKlines/premiumIndexKlines are zero-volume placeholders (inadmissible). No 3-block mark-price panel exists.
- Track A (observed liquidations, ironflow Hyperliquid): FCLR-010 gate PASSED (SEALED, n=199, 5 blocks), overlay FCLR-OVERLAY-001 EXECUTED hypothetical-only. data_through=2026-10; no post-2026-10 monthly parquet; resume trigger = new ironflow data/events/YYYY-MM.parquet month >= 2026-11 with HTTP 200 unauthenticated.
- Track B (modeled boundary breaches): CLOSED_NEGATIVE (H003-EXT-001, 16 cells, Holm).
- H002 (Shek replication): PERMANENT_BLOCKED (SSRN HTTP 403).
- Structural closure verdict (2026-10-31): NO FURTHER confirmatory execution possible without NEW admissible unauthenticated data. All confirmatory campaigns complete negative/inconclusive. Bottlenecks removed to the extent data allows; remaining blocker is structural data absence.

## 2) Bottleneck & Remediation
- BOTTLENECK: Confirmatory reopen requires NEW admissible unauthenticated data (Track A: ironflow >=2026-11 parquet; Track C: Binance mark/index/premium panel beyond 2026-11-02 with >=3 non-overlapping 30-day blocks). Retrying dead endpoints (data.binance.vision 2026-11-04+ = 404) without new evidence is forbidden non-progress.
- REMEDIATION: Stop dead-end retries. Replace with scheduled lightweight probing every 30-120 min (step 1), maintain ironflow monitor, keep alternative-source discovery warm per research_state/next_data_discovery_plan.md (8 source families, all previously NO-GO; re-check only as materially distinct routes). Execute mandatory heavy work (3A-3D) every blocked session so the program does not idle.

## 3) Resume Trigger (concrete, checkable — the only way to unblock confirmatory)
Ironflow publishes research_state/data/events/YYYY-MM.parquet (or data/fills/) for any month >= 2026-11 with HTTP 200 on unauthenticated GET (verified by scripts/monitor_ironflow_liquidations.py, state-aware, reports genuinely new files), OR a NEW admissible unauthenticated source passes the strict rubric (>=5 symbols, >=3 non-overlapping 30-day blocks or >=1 complete month, documented completeness/coverage, permissive license, unauthenticated no keys/signed/requester-pays, schema compatible with frozen protocol). In either case: pre-register new experiment ID BEFORE outcome inspection, then execute frozen harness.

## 4) Definition of Done
- New timestamped trigger_harden artifact with complete probe table
- Tests >=117 green, no workflow changes, sealed unchanged, firewall intact, __pycache__ deleted
- Either: new-data path executed (pre-registration -> harness -> evaluation summary -> frontier update) OR blocked-path heavy work (3A-3D) fully executed with fresh blocker doc + frontier + AGENT_HANDOFF update
- No fabricated data; inconclusive/negative preserved; measurable progress recorded with exact commands and evidence
