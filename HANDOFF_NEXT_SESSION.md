# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, authoritative):** 2026-11-11T17:16:49Z
**Status:** AUTHORITATIVE. This is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. `AGENT_HANDOFF.md` is a redirect only. Any doc conflicting with this handoff is stale. Read fully before acting. **No status-only output.**

## INITIAL TASK MESSAGE (EXECUTE NOW) — 2026-11-11T17:16:49Z

**Mission (repo-prioritized):** Advance `Funding-conditioned-volatility-and-liquidation-risk` on **liquidation-risk forecasting co-equal with volatility forecasting**, using admissible unauthenticated data with verifiable provenance. Track A successor (2026-05..2026-10, 9 symbols, observed ironflow) is evaluated **NOT_MET** (closed for that prereg). Track B/C (2024) are closed negative. Gate 4 is externally blocked. **Do not idle, do not report status only, do not relitigate closed work. Execute the first applicable heavy-work branch below and leave substantive artifacts + consistent state updates.**

### Completed (do not relitigate)
- **Track A successor `TRACKA-HL-S-20261111T133430Z` (2026-05-01..2026-10-31):** RV bottleneck removed via bounded first-time unauthenticated Hyperliquid candleSnapshot acquisition (54 coin-months, cached), RV panel built/evaluated, **forecast gate NOT_MET** (C2 worse than B1). Verdict: `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`. Panel: `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`. Prior context-insufficient closure superseded: `research_state/evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md`.
- **Branch 2 gap audit completed (this session, no outcomes computed):** `research_state/next_panel_gap_audit_20261111T163229Z.json`, `research_state/next_panel_gap_audit_20261111T163229Z.md`. Confirms cached admissible assets (ironflow observed labels 2025-05..2026-10, 18 parquet files, ~2,848,413 rows, 468 markets; HL funding 9 coins ~2025-11-01..2026-10-31; HL 1h candles 9 coins 2026-05..2026-10 only) and identifies fillable Track-A gaps.
- **Closed negative / sealed:** Track B/C confirmatory (2024) NOT_SUPPORTED (H001/Track B). FCLR-002/003/Track B/C test sets immutable — **no reuse, no threshold-shopping**.

---

## REQUIRED HEAVY WORK — EXECUTE FIRST APPLICABLE BRANCH

### Branch 1 (CONDITIONAL, execute immediately if artifact exists): Gate 4 / Track C volatility unblocking
**Trigger:** valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, human/legal attestation.
**Actions (deterministic, in order):**
1. Run Gate 4 promotion/admissibility validators per tooling (`scripts/fclr016_v5_promotion_dryrun.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_preflight_summary.py` or repo equivalents) with `--expect-go` semantics where applicable.
2. Only on all-green GO, execute confirmatory Track C multi-split ablation on the frozen 2025+ panel (>=7d purge/embargo, train-only normalization, block-bootstrap ΔQLIKE CIs, pre-registered contrasts/thresholds) with frozen artifacts.
3. Emit verdict artifact(s) under `research_state/` and update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` atomically.
**If trigger absent:** Gate 4 remains `EXPLICIT_BLOCKER_UNRESOLVED` (current blocker: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `fabricated=false`). **Do NOT set `RESOLVED_VERIFIED` or `fabricated=true`; do NOT bypass/fabricate terms evidence. Proceed to Branch 2.**

### Branch 2 (DEFAULT, mandatory while Gate 4 blocked): New observed-liquidation Track A claim (PRIORITY)
**Selected campaign (from gap audit):** `GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1` — pre-register and evaluate a **new** funding-conditioned vs RV-only forecast of **observed Hyperliquid liquidation intensity** on an earlier admissible window where ironflow labels and HL funding are cached but RV/candle context is missing, disjoint in design from the evaluated NOT_MET 2026-05..2026-10 prereg.

**Execute in order (heavy, substantive artifacts required):**
1. **Freeze preregistration BEFORE any outcome computation/alignment for the new claim.** Create `research_state/tracka_prereg_hyperliquid_early_<UTC>.json` (and optional `.md`) fixing: hypothesis/claim, exact window and symbols (start from 9 coins with cached funding overlap: AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP), observed label definition/source (ironflow, Hyperliquid only) and aggregation horizon, predictor families (RV-only baseline B1 vs funding-conditioned C2), target/metric (e.g. QLIKE on next-24h liquidation intensity or justified alternative), train/val/test splits with >=7d purge/embargo, >=3 non-overlapping 30d test blocks and >=5 paired instruments minima (or explicit infeasibility rule), block-bootstrap CI spec, materiality threshold (>=2% where applicable), missingness/inclusion rules, and input provenance/checksums. Record git HEAD and freeze timestamp; do not inspect outcomes first.
2. **Bounded first-time unauthenticated acquisition (only missing inputs):** For prereg-specified coins/months lacking candles, fetch Hyperliquid `candleSnapshot` 1h with provenance and cache under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` (or documented equivalent). Record a fetch/provenance manifest (endpoint, params, access times UTC, status, checksums/sizes, unauthenticated/no-key/no-requester-pays/signature status). **Do NOT re-fetch 2026-05..2026-10**. Candidate fillable range to assess against funding+ironflow overlap: ~2025-11..2026-04 (confirm exact admissible intersection in prereg before fetch; fetch only what prereg specifies).
3. **Build deterministic RV-augmented panel from cached inputs:** emit `research_state/tracka_hl_*panel*<UTC>.parquet` and build report JSON/MD with hashes, coverage, leakage/embargo notes, symbol-month completeness, and label provenance (observed ironflow only).
4. **Run pre-registered evaluation only after (1)-(3) artifacts exist:** compute contrasts/splits per prereg, emit `research_state/evaluation_summary_TRACKA-HL-<UTC>.md` with verdict (MET/NOT_MET/INADMISSIBLE per prereg), bootstrap CIs, gate checks.
5. **Update state atomically:** `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (append addendum; preserve 2024 H001 and prior Track A records). Keep sealed records immutable.
6. **If prereg minima/admissible overlap cannot be satisfied (infeasibility):** emit a concrete infeasibility artifact citing exact evidence (coverage gaps, block/instrument shortfall) — not status-only — then pivot to `GAP-TRACKA-SYMBOL-EXPANSION-2026M05M10` (new prereg with frozen ex-ante symbol selection/event-adequacy rules, bounded first-time funding/candle acquisition for additional ironflow markets as needed) and execute same prereg→build→eval discipline.

**Secondary (only if Track A candidates exhausted with documented evidence):** `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` on admissible untested Hyperliquid data, pre-registered before outcomes, no Track C/Gate 4/2024 Binance conflation.

---

## Hard bans (binding)
- No outcome inspection before freeze/preregistration for any new claim.
- No Binance/2024 conflation with Hyperliquid; venue/data-source claims must match artifacts.
- No modeled/proxy/synthetic liquidation labels presented as observed (Track A = observed ironflow or equivalent with provenance).
- No threshold-shopping; no sealed-holdout reuse (FCLR-002/003/Track B/C).
- No `.github/workflows` edits.
- No redundant network polling (bounded first-time acquisition with caching/provenance is allowed and required where specified).
- No agent-set `RESOLVED_VERIFIED` or `fabricated=true`; no bypass of Gate 4 human/legal terms.
- **No status-only output:** every session must leave a substantive artifact (gap audit done this session; next must produce prereg/fetch-manifest/panel/eval or documented infeasibility + state updates).

## Key refs
- Handoff/audit: `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md`, `research_state/next_panel_gap_audit_20261111T163229Z.md|.json`
- Track A (closed): `research_state/evaluation_summary_TRACKA-HL-20261111T160124Z.md`, `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`, `research_state/tracka_hl_aligned_panel_with_rv_20261111T160124Z.parquet`, `research_state/tracka_hl_panel_with_rv_build_report_20261111T160124Z.json`
- Caches: `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/hyperliquid_candles/`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`, `scripts/fclr016_v5_promotion_dryrun.py`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`
- Checks: `python -m unittest discover -s tests -v` (as relevant)

**End of Handoff — Execute INITIAL TASK MESSAGE now: Branch 1 if Gate 4 resolved, else Branch 2 heavy campaign (GAP-TRACKA-EARLY-OBSERVED-2025H2_2026Q1).**
