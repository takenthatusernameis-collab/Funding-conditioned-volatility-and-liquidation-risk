# HANDOFF: Next Agentic Work Session — SINGLE DURABLE HANDOFF
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Timestamp (UTC, authoritative):** 2026-11-11T13:45:00Z
**Status:** AUTHORITATIVE. This is the only task message to execute. `FOCUS_CAMPAIGN.md` and `NEXT_SESSION_TASK.md` must point here. `AGENT_HANDOFF.md` is a redirect only. Any other doc claiming Track A closed without a verdict artifact or conflicting with this handoff is stale. Read fully before acting. **No status-only output.**

## INITIAL TASK MESSAGE (EXECUTE NOW) — 2026-11-11T13:45:00Z

**Mission (repo-prioritized):** `Funding-conditioned-volatility-and-liquidation-risk` requires **liquidation-risk forecasting** co-equal with volatility forecasting, on admissible unauthenticated data with provenance. **Track A (observed Hyperliquid liquidations, ironflow CC BY 4.0, unauthenticated)** is the only computable Track A path.

### Track A status — TERMINALLY CLOSED this session (Path c)
Track A was terminally closed as `NOT_SUPPORTED` (context insufficient / claim-worthy minima unmet on cached admissible inputs). **Do not relitigate; do not re-open without new admissible data.**
- Verdict artifact: `research_state/evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md`
- Successor prereg (frozen pre-outcomes): `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json` (window `2026-05-01..2026-10-31`, 9 *-PERP symbols, input SHA256 checksums)
- Aligned panel built from cache: `research_state/tracka_hl_aligned_panel_20261111T133430Z.parquet` (sha256 `7a7c431b...`, 1656 buckets, all 9 symbols labeled, funding 100%)
- Build report: `research_state/tracka_hl_panel_build_report_20261111T133430Z.json`
- State updated atomically: `experiment_frontier.json`, `hypothesis_registry.json` (`H_tracka_hl_liquidation_forecast` → NOT_SUPPORTED), `run_manifest.json` (runs[2]), `final_confirmatory_verdict.md` (Track A addendum)

**Why Path (c):** the pre-registered primary contrast C2 vs B1 (QLIKE vs RV-only baseline) requires mark-price/RV context. That context is **not in cached admissible inputs** (only ironflow labels + Hyperliquid funding are cached; no mark-price/klines/index/premium cache). Handoff rule: "Build aligned panel deterministically from cached admissible inputs only (no redundant network polling)." Minimum claim-worthy test unmet → no outcome computed.

---

### REQUIRED HEAVY WORK THIS SESSION — Remove the binding bottleneck, then finish Track A

**Binding bottleneck (remove it):** mark-price/RV context for `2026-05-01..2026-10-31` is not cached. It IS available via the live **unauthenticated** Hyperliquid `candleSnapshot` endpoint (probe `hl_pathb_probe_20261111T122801Z.json` confirmed ~720-744 hourly rows/month for 2026-05..2026-10 across BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI; minor gaps: AVAX 2026-09 429, BNB 2026-06 429, SUI funding 2026-07 429). Fetching it now is **first-time acquisition, not redundant polling**, and is the bottleneck-removal step.

**Execute in order:**
1. **Acquire mark-price 1h candleSnapshot** for `2026-05-01..2026-10-31` for the 9 symbols via `scripts/tracka_hl_pathb_probe.py` logic (or a dedicated bounded fetcher): `POST https://api.hyperliquid.xyz/info {"type":"candleSnapshot","req":{"coin":"<COIN>","interval":"1h","startTime":<ms>,"endTime":<ms>}}`. Save raw responses under `research_state/data_cache/hyperliquid_candles/<COIN>/<YYYY-MM>.json` (or parquet) with SHA256 checksums and access timestamps. Bounded: 9 coins × 6 months, ~182s probe baseline; use retries/backoff, honor 429s, stop on persistent errors. Do NOT re-fetch months already valid.
2. **Rebuild the aligned panel** with RV: join ironflow labels (notional_usd-weighted intensity per symbol per 24h UTC bucket) + funding + mark-price returns → trailing RV (RV1h/RV24h/RV168h) per symbol per bucket, all causal (data ending no later than bucket start). Save panel + build report with hashes, row counts, coverage, missingness/gap report under `research_state/`.
3. **Execute the pre-registered successor evaluation** per `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`: C2 vs B1 primary contrast (QLIKE on next-24h liquidation intensity), leakage/embargo checks (≥7d embargo, 3 non-overlapping test blocks, ≥5 paired instruments), materiality gate (≥2% relative QLIKE reduction, CI excludes zero). Emit `research_state/evaluation_summary_TRACKA-HL-<verdict_id>.md` with explicit verdict.
4. **Update state atomically:** `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` (Track A addendum — do not erase 2024 H001 record).
5. **Acceptance:** a new `evaluation_summary_TRACKA-HL-*` verdict artifact + consistent state updates. Anything less is incomplete.

If, after acquiring RV context, the pre-registered minima still cannot be met (≥3 test blocks / ≥5 paired instruments / RV computable), emit `evaluation_summary_TRACKA-HL-terminal-<UTC>.md` (Path c) with evidence and atomic state closure — but only after the RV fetch has been attempted and documented.

---

### Gate 4 / Track C (Binance 2025+ volatility extension): EXTERNAL BLOCKER
**Status:** `EXPLICIT_BLOCKER_UNRESOLVED` (human/legal Binance terms evidence). `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` (`fabricated=false`).
**Conditional rule ONLY:** if a valid `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears with all 8 verifiable fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and a human/legal reviewer attestation: run deterministic promotion then `--expect-go` validators; only on all-green GO execute confirmatory Track C multi-split ablation (≥7d purge/embargo, train-only normalization, block bootstrap ΔQLIKE CIs) with frozen artifacts. Otherwise **do not touch Gate 4**. Agents must NOT set `RESOLVED_VERIFIED` or `fabricated=true`.

---

### Hard bans (unchanged)
- No outcome inspection before prereg freeze; no Binance/2024 conflation (Hyperliquid only, Track A); no modeled/proxy/synthetic liquidation labels (observed ironflow only); no threshold-shopping; no sealed-holdout reuse; no `.github/workflows` edits; no redundant network polling beyond the bounded first-time candle acquisition above; no agent-set `RESOLVED_VERIFIED` / `fabricated=true`; no status-only output without a Track A verdict artifact (or newly valid resolved terms artifact + executed promotion chain).

### Bottleneck removal (this session)
- Binding bottleneck identified: missing cached mark-price/RV context for Track A overlap window.
- Removal action: bounded first-time unauthenticated `candleSnapshot` acquisition for `2026-05-01..2026-10-31` (9 symbols), then rebuild panel + execute successor C2 vs B1 evaluation → Track A verdict.
- Track A already terminalized Path (c) this session; do not re-open unless new admissible data appears.
- Gate 4 isolated to prevent spin; Track B/C 2024 closed & sealed.

### Key refs
- Track A: `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`, `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/tracka_alignment_patha_audit_20261111T125022Z.md`, `research_state/tracka_hl_alignment_blocker.md`, `research_state/hl_pathb_probe_20261111T122801Z.json`, `research_state/data_cache/ironflow_events/`, `research_state/data_cache/hyperliquid_funding/`, `scripts/tracka_hl_pathb_probe.py`, `scripts/hyperliquid_funding_fetch.py`, `src/analysis/tracka_admissible.py`
- Gate 4: `research_state/fclr016_local_audit/fclr016_v5_*`, `scripts/fclr016_v5_preflight_summary.py`, `scripts/fclr016_validate_v5_admissibility.py`
- Baseline checks: `python -m unittest discover -s tests -v` (as relevant)

**End of Handoff — Execute the INITIAL TASK MESSAGE now. Remove the RV-context bottleneck, then complete Track A (Path b retry with verdict, or documented Path c).**
