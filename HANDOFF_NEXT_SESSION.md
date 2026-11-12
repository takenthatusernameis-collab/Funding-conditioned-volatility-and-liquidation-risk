# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized; neither track subordinated to the other)
**Handoff timestamp (UTC):** 2026-11-12T07:52:10Z (supersedes 2026-11-12T07:47:40Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Progress snapshot (this session — heavy work completed, evidenced)

- **Offline verification:** `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v` → 103 tests OK. Codebase in working order before any network work.
- **Gate 4 Branch 1 trigger:** ABSENT (rechecked 2026-11-12T07:31:59Z; no `research_state/fclr016_local_audit/*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). External/legal blocker — not agent-removable. Do not wait/poll. Branch 1 executes only on a valid RESOLVED trigger.
- **Bounded new-data monitor probe (prior session 2026-11-12T07:31:59Z):** `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` — ineligible now, evidenced; `new_claim_worthy_experiment_eligible_now=false`.
  - ironflow/hyperliquid-liquidations: `lastModified=2026-11-07T10:18:25Z`, latest event month `2026-10`, no verified post-2026-10-31 observed liquidation labels.
  - Hyperliquid 2026-11+ depth: BTC 1d candles 12 rows (~12.0d), BTC funding 272 rows (~11.29d). << 100d reprobe threshold and << 90d for ≥3×30d test blocks.
- **FCLR-NEXT Step 2 executed THIS session (2026-11-12T07:50:45Z → 2026-11-12T07:51:34Z):** Bounded alternative liquidation-label source discovery per RESEARCH_PROMPT §5.
  - Hunt enumeration: `scripts/hunt_alternative_liquidation_sources.py` → `research_state/alt_source_scan_latest.json` (generated_utc=20261112T075045Z, 22 candidates incl. 14 live HF-discovered).
  - Deep review probes: `scripts/deep_review_alt_sources.py` → `research_state/alt_source_deep_review_latest.md` (TIMESTAMP=20261112T075134Z, 14 fresh probes, 0 cache hits).
  - **Result: NO NEW GO sources identified.** All tested unauthenticated sources either require auth (CoinAPI, Kaiko, Glassnode, Coinglass), return 404/403 (Bybit archive paths, Tardis, Binance liquidationSnapshot), are libraries not datasets (cryptofeed), or are HTML pages without structured liquidation census data (Laevitas, CryptoDataDownload).
  - Ironflow/hyperliquid-liquidations on HF (CC BY 4.0, unauthenticated) remains the ONLY known admissible Track A source found to date — but it is EXHAUSTED for claim-worthy work (data through 2026-10 only; HL 2026-11+ ~12d < 100d threshold).
- **Sealed determinations unchanged:** metpie 2025Q2 §16 audit = INADMISSIBLE (block-feasibility ~65d < 90d); TRACKA-HL-EARLY-4H = INCONCLUSIVE_PILOT_SHORTFALL; all cached-data Track A/B/C/H1 designs sealed/exhausted (Track A expansion PASS but robustness FRAGILE; vol family NOT_MET; alt vol NOT_MET; Track B TB1/TB2 NOT_SUPPORTED; Track C/H1 NOT_SUPPORTED).

## Bottlenecks — status and removal action (2026-11-12T07:52:10Z)

| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms evidence) | BLOCKED, not agent-removable | ISOLATED: execute Branch 1 only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Agent does NOT create/attest it. Do NOT wait/poll. All other work proceeds without it. No session is held up by this. |
| HL 2026-11+ ~12d; no verified post-2026-10-31 observed labels | OPEN, not eligible now (evidenced) | REMOVED as blocking path: do NOT re-probe HL/ironflow endpoints. Attack exclusively via NEW source discovery (campaign step 2 below). Reprobe HL/ironflow only when plausibly eligible (HL ≥100d AND verified post-2026-10-31 observed labels). No polling. |
| Cached-data designs exhausted/sealed | EXHAUSTED | REMOVED as candidate path: no relitigation/retune of sealed verdicts. Only a genuinely new admissible source/window per RESEARCH_PROMPT §16 can open a claim-worthy experiment. |
| No new admissible liquidation-label source found | EVIDENCED THIS SESSION | REMOVED as candidate path: this session's hunt+deep_review (22 candidates, 14 fresh probes) produced timestamped evidence of exact failing minima per source. No repeated no-op probes. Next session stops cleanly unless Gate 4 trigger appears or HL/ironflow becomes plausibly eligible. |
| H2_shek_replication registry status "proposed" although `research_state/h002_replication_report.md` documents completed PARTIAL replication | INCONSISTENT | REMOVED: registry corrected to EXPLORATORY_ONLY/PARTIAL with evidence pointer; no re-run, no promotion. |

## NEXT FOCUS CAMPAIGN — FCLR-NEXT: checkpoint-only (heavy work DONE this session; next session checks triggers only)

**This campaign's heavy work (source discovery + deep review) was completed THIS session.** The next session MUST NOT repeat the hunt/deep-review probes. Every session must deliver ONE of: (a) Gate 4 Branch 1 (if triggered), OR (b) a §16 admissibility audit (+ prereg/build/eval/verdict if a source passes), OR (c) evidenced infeasibility + state update + clean stop, OR (d) bounded probe evidence + ineligibility documentation. Future agents cannot skip this campaign; each probe must add new evidence or stop.

1. **Gate 4 check (FIRST, every session):** if valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears → execute Branch 1 immediately per campaign rules. (Absent now. Absence is not a reason to stop — proceed to step 2.)
2. **HL/ironflow eligibility re-check (BOUNDED, no polling):** only when plausibly eligible (HL 2026-11+ depth ≥100d AND verifiable post-2026-10-31 observed liquidation labels, or other evidenced new source). Not eligible now (~12.0d). Do not poll; re-check only when wall-clock time or new evidence makes eligibility plausible.
3. **New source discovery:** ONLY if a materially new candidate appears in `hf_search_cache.json` (TTL 24h) or `data_source_registry_alt_hunt.json` that was NOT probed in `alt_source_deep_review_latest.md` (TIMESTAMP=20261112T075134Z). Do NOT re-probe already-tested URLs.
4. **If a NEW source passes smoke test:** run full §16 admissibility audit → emit timestamped determination + artifacts (`research_state/<source>_admissibility_audit_<UTC>.{md,json}`) BEFORE any preregistration or outcome computation. If admissible → freeze prereg → build panel → evaluate → verdict → atomic state updates under a NEW experiment ID. Never inspect outcomes before prereg freeze.
5. **If no new source passes and no trigger is met:** emit timestamped checkpoint documenting that no new evidence was found, update `experiment_frontier.json` if needed, and STOP CLEANLY. No repeated no-op probes; each session must add new evidence or stop.

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE

- `TRACKA-HL-EARLY-20261111T191958Z` = INADMISSIBLE (1h candles). Sealed.
- `TRACKA-HL-EARLY-4H-20261112T054737Z` = INCONCLUSIVE_PILOT_SHORTFALL (<3 test blocks). Sealed.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = PASS; robustness `TRACKA-EXP-ROBUST-20261112T015119Z` = FRAGILE (LOIO 4/8 < 6; placebo FAIL; bootstrap PASS). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = NOT_MET. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = NOT_MET; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = NOT_MET (Holm, 12 comparisons). Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = NOT_MET (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED. 2024 Binance confirmatory FCLR-003 = NOT_SUPPORTED (`research_state/final_confirmatory_verdict.md`). Immutable.
- metpie 2025-03-22..2025-05-25 §16 audit = INADMISSIBLE. Sealed.
- H2 Shek correction-time replication = PARTIAL/exploratory (`research_state/h002_replication_report.md`; SSRN 403; direction reproduced p=0.079, not significant; correction time ≠ forecast skill/liquidation evidence). No promotion.

## HARD BANS (BINDING)

- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation; no modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session delivers concrete heavy work or evidenced ineligibility + clean stop (per campaign rule above).
- Do not relitigate or retune sealed verdicts.
- **Do NOT re-run `hunt_alternative_liquidation_sources.py` or `deep_review_alt_sources.py` unless a materially new candidate URL appears that was not probed in `alt_source_deep_review_latest.md` (20261112T075134Z).**

## KEY REFERENCES

- Eligibility evidence (prior session): `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`.
- This session's source discovery: `research_state/alt_source_scan_latest.json` (generated_utc=20261112T075045Z); `research_state/alt_source_deep_review_latest.md` (TIMESTAMP=20261112T075134Z).
- H2 completed PARTIAL: `research_state/h002_replication_report.md`; `research_state/h002_replication_blocker.md`.
- Protocol: `RESEARCH_PROMPT.md` (§5 source families; §16 admissibility/adaptive feasibility).
- State: `research_state/experiment_frontier.json`; `research_state/hypothesis_registry.json`; `research_state/fclr016_local_audit/`.

## Execution contract

- First action: Gate 4 check → absent → HL/ironflow eligibility re-check (bounded, no polling) → not eligible → check for new unprobed candidates in HF cache/registry → none → STOP CLEANLY with timestamped checkpoint.
- Deliverable: timestamped checkpoint documenting no new evidence found, or Gate 4 Branch 1 execution, or §16 admissibility audit of a genuinely new source.
- Verification: inspect `research_state/alt_source_deep_review_latest.md` (TIMESTAMP=20261112T075134Z) for probe evidence; any new §16 audit carries `generated_utc`, endpoint evidence, and acceptance/rejection rationale. Offline check before any network probes: `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v`.

(End of file - total 66 lines)