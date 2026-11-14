# SINGLE DURABLE HANDOFF — 2026-11-14T12:33:25Z (initial task for next agentic session)

## Repository / mission
- **Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation risk; Binance 5-symbol Track C + Hyperliquid/Track A frontier). Forecast validation only; no trading/overlay promotion.
- **Program state (verified this session):** `scripts/next_campaign_status.py` → no frozen preregs without evaluation artifacts; Binance 5-symbol 3-block design exhausted; Hyperliquid 2026-01-18..2026-04-30 forward-reduced (60/7/3×10) region is **no longer untouched** (forward liq-xsec and vol-forward executed). `scripts/fclr_campaign_gate.py --arm all` **19/19 PASS**. Gate 4 blocker pipeline **27/27 PASS**. Final structural closure **5/5 PASS**. Reconciliation tests **10/10 PASS**. Track A hardening (140,142) **PASS**.

## Completed / terminal (do not reopen or re-execute)
- **FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z — COMPLETE, EXPLAINED_BY_ESTIMATOR (EXPLORATORY_ONLY, promotable=false).** 2×2 audit on identical 1,472 (coin,ts) keys: sealed+sealed 19.0371%, recompute+sealed 19.0371%, sealed+recompute 6.19%, recompute+recompute 6.19% C2_vs_B1 QLIKE reduction. Gap fully explained by estimator (raw/unscaled, fill-missing-0 vs z-scored train-only scaling, drop-missing), not data. Artifacts: `prereg_tracka_liq_expansion_reconciliation_20261114T083642Z.{json,md}`, `evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T113226Z.{json,md}` (latest), `scripts/fclr_liq_expansion_reconcile.py`, `tests/test_fclr_liq_expansion_reconcile.py`. Sealed verdicts unchanged.
- **TRACKA-HL-EXPANSION (2026-05..2026-10, 8-symbol, observed liq):** prereg frozen/executed; sealed PASS 19.04% (`tracka_hl_expansion_eval_result_20261111T202344Z.json`) but robustness **FRAGILE** (LOIO 4/8, placebo FAIL); independent recompute **INCONCLUSIVE** (6.19%); reconciliation above explains estimator delta. Panel/build/eval artifacts exist — **do not re-acquire, rebuild, or re-evaluate**.
- **TRACKA-VOL-FULLHIST (2025-06-01..2026-01-17):** `evaluation_summary_TRACKA-VOL-FULLHIST-2026-11-13T02:44:48Z.json` **NOT_MET** (terminal).
- **Forward 2026Q1Q2 (2026-01-18..2026-04-30, Hyperliquid bulk):** `TRACKA-LIQ-XSEC-FORWARD` **EXPLORATORY_NULL** (`evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json`), `TRACKA-VOL-FORWARD` **EXPLORATORY_NULL/VALID_EXPLORATORY** (`evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T03:30:40Z.json`). Both complete; region no longer available for a fresh forward claim.
- **Track C volatility cross-period:** FCLR-011 sealed PASS (2026-05..2026-08) does not generalize (2024Q4/2025/2025H2/2025Q1Q2/forward confirm all NOT_REPLICATED). H1_primary NOT_SUPPORTED (terminal). Gate 4 Branch 1 (terms/legal) **EXTERNAL_BLOCKED** — agent must not set `RESOLVED_VERIFIED` or `fabricated=true`.

## CURRENT BOTTLENECK (blocking new confirmatory/heavy execution)
- No unfrozen/unexecuted preregistered heavy cell remains on cached/admissible data; Binance and Hyperliquid 2026Q1Q2 forward designs are exhausted/tested; no valid Gate 4 trigger; no verified new observed-liquidation source meeting §16 minima (≥5 instruments, ≥3 non-overlapping 30-day blocks or equivalent complete-month design as preregistered, unauthenticated, provenance/license, observed-only labels, venue-consistent, joinable).
- **Stale directives removed:** prior handoffs instructed "Execute Step 1 of TRACKA-HL-EXPANSION" — that campaign is already acquired/built/evaluated/reconciled; do not repeat.

## NEXT HEAVY WORK CAMPAIGN (mandatory; no status-only session) — 2026-11-14T12:33:25Z
**Campaign:** `FCLR-NEW-ADMISSIBLE-SOURCE-AUDIT-20261114T123325Z` (bounded, one-shot, fail-closed)

1. **External trigger check (deterministic, local):** search `research_state/` for any `fclr016_v5_terms_evidence_RESOLVED_*.json` with `status==RESOLVED_VERIFIED`, `fabricated==false`, and human/legal attestation fields present. If **present and valid** → immediately execute Gate 4 Branch 1 path per existing gate scripts/tests (no outcome peeking beyond prereg) and record verdict/evidence. If **absent** → record `NO_VALID_GATE4_TRIGGER` with exact glob/result and proceed to (2).
2. **Admissibility re-audit of any untested candidate (heavy, evidence-first):** review `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/data_source_registry*.json`, and `scripts/hunt_alternative_liquidation_sources.py` outputs. Identify **zero or more** candidates not previously terminally rejected for §16 minima. For each: perform a **bounded unauthenticated probe** (no credentials, no payment, no manual download, honor rate limits, single pass with backoff cap) to verify access, schema/fields, observed-vs-modeled label nature, history depth, instrument count, and license/provenance. Emit `research_state/new_data_admissibility_audit_<UTC>.{json,md}` with per-candidate PASS/FAIL and exact failing minima.
3. **Branch on result:**
   - **If any candidate passes §16 minima:** freeze a NEW prereg (`FROZEN_PRE_OUTCOMES`, before outcomes) specifying design/splits/estimand/gates, then execute acquisition→panel build→evaluation→verdict with hashes and gate tests. Update `experiment_frontier.json`/`hypothesis_registry.json`/`run_manifest.json`/`final_confirmatory_verdict.md` atomically. This is the highest-value executable path.
   - **If none pass:** emit timestamped `research_state/structural_exhaustion_confirmation_<UTC>.md` citing exact probe evidence, failing minima per source, and confirming no agent-removable heavy work remains; set frontier/task state to bounded terminal/trigger-only. **Do not poll or repeat identical probes.**

## Forbidden / regression guards
- No "campaign exhausted/closed" claim without citing this handoff's verified probe evidence for the specific UTC.
- No reading sealed/terminal windows for new claims; no outcome inspection before prereg freeze; no threshold shopping.
- No `.github/workflows` edits; no fabricated `RESOLVED_VERIFIED`; no modeled/synthetic labels labeled observed.
- Preserve all sealed artifacts (FCLR-002/003/011, Track A/B/C records).

## Immediate action now
Run step (1) trigger check, then step (2) bounded re-audit/probes against existing registry/scan artifacts; produce the required timestamped audit/report and, if admissible, freeze+execute new prereg in-session. Record commands, hashes, and verdict in an addendum to this handoff or linked `research_state/` artifacts.
