# AGENT HANDOFF — 2026-11-22T23:49:00Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

**Rank-0 campaign:** `FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z` — status `READY_EXECUTE`, program `ACTIVE`. Campaign start UTC `20261122T225107Z` has **ELAPSED**. Your new `session_<UTC>/` MUST have UTC **> `20261122T225107Z`** and MUST be recorded in this handoff (append the literal id `session_<UTC>`) before the gate will pass.

**This campaign is machine-enforced by the gate, and — as of this handoff — the gate now also requires the HEAVY QUANTITATIVE EVALUATION in the SAME session, not just a prereg.** `scripts/check_handoff_heavywork_gate.py::_tracks01_state` binds the `fclr_tracks01_*` artifact family to `FCLR-TRACKA-SOURCE-AUDIT-(N)`. A post-start session that stops at the source audit + pivot prereg (the old prereg-only escape hatch) now FAILS closed with `TRACKA_SOURCE_AUDIT_ARTIFACTS_MISSING`. It must produce the full artifact set below, including `fclr_tracks01_eval_*` (heavy evaluation) and `fclr_tracks01_recompute_*` (independent stdlib recompute). Zero-byte placeholders do not count.

**Why this campaign and nothing else (priority by repo name + frontier):**
The repo name is **Funding-conditioned-volatility-and-liquidation-risk**. The primary question (§3.2) has two halves:
1. **Volatility forecasting (Track C)** — CLOSED leakage-robust: `FCLR-POOLED-ROBUST-002` returned `NOT_SUPPORTED_LEAKAGE_ROBUST_NULL` (C2−B1 QLIKE = +1.011%, Holm primary p=0.6365 vs α₂=0.00833).
2. **Liquidation-risk forecasting** — Track A (observed liquidations) evaluated in `FCLR-LIQ-RISK-ESCALATION-09` → `NOT_SUPPORTED` (+0.149% rel QLIKE, fails -2% floor, CI95 includes zero, Holm p=0.6365). Track B (modeled breach) evaluated in `FCLR-POOLED-001`, `FCLR-POOLED-ROBUST-002`, `FCLR-LIVE-ARCHIVE-01/02` → all `NOT_SUPPORTED`.

**Three materially distinct routes, two+ source families, same gate blocked.** Per RESEARCH_PROMPT.md §16: "If the same gate remains blocked after three materially distinct documented routes spanning at least two independent source families/methods... create the smallest useful alternative experiment with a new ID." Per §5: "Do not prematurely conclude that no liquidation labels exist. Enumerate, test, and rank admissible sources." Per §10 priority #2: "Source feasibility map: test small unauthenticated requests for... direct liquidation history. Publish exact evidence of what is accessible."

**The single highest-value unfinished work is a formal Track A source viability audit FOLLOWED BY a heavy evaluation in the same session** — the ONLY path to either (a) unlock Track A with a new viable observed-liquidation source and confirm it, or (b) formally close Track A and pivot to Track B with a new frozen protocol AND run that heavy evaluation. This is NOT a re-run of any terminal campaign. It is a new experiment (FCLR-TRACKA-SOURCE-AUDIT-01) with a new ID.

**Blockers: None.** No external trigger, no network required for the heavy evaluation; source enumeration uses stdlib + pyarrow only. The audit AND the heavy evaluation are feasible TODAY on the on-disk ironflow bulk panels (18 months, 342 coins) plus cached knowledge of free sources.

---

## FOCUS CAMPAIGN (Mandatory — heavy work, non-avoidable, gate-enforced)

Execute **FCLR-TRACKA-SOURCE-AUDIT-01** in three phases, all in ONE `session_<UTC>/`:

1. **SOURCE_ENUMERATION_PROBE** — Enumerate, test, and rank ALL admissible free sources for observed liquidation labels per RESEARCH_PROMPT.md §5, §15. Candidate families: Binance public archive (liquidationSnapshot?), Bybit public archive, OKX public archive, Hyperliquid (if any public historical liquidation endpoint), public GitHub/Zenodo/Hugging Face/institutional archives, Ironflow (already used — document why the capped-sample design makes it incomplete per §15). For each: verify unauthenticated download path, actual history depth, schema, licensing, earliest/latest timestamp, cadence, symbol/venue coverage, known gaps, file hashes/ETags, rejection reason if inadmissible. Record in the source registry artifact + per-source probe artifacts.

2. **VIABILITY_DECISION_AND_PIVOT** — Based on audit evidence, make a frozen viability decision BEFORE inspecting any outcome:
   - **If a new viable Track A source is found:** freeze a new confirmatory protocol (FCLR-TRACKA-SOURCE-AUDIT-01-V2) with outcome-blind prereg, then execute the heavy evaluation on that source.
   - **If NO viable Track A source exists (structural impossibility per §16):** formally close Track A with evidence, then freeze a new Track B (modeled boundary-breach) protocol with a new experiment ID, using the BEST available free mark-price + margin-parameter data (Binance archive klines/mark/index/premium, Ironflow candles/funding/OI), and execute the heavy evaluation. Track B must be clearly labeled as modeled proxy per §15.

3. **HEAVY_EVALUATION_AND_RECOMPUTE** — Run the heavy quantitative evaluation selected by the viability decision and record it as `fclr_tracks01_eval_*` (py + json + md), plus an independent stdlib recompute `fclr_tracks01_recompute_*` (py + json). This is the phase the gate now refuses to let you skip.

### Required Artifact Set (ALL non-empty, under `research_state/session_<UTC>/`, UTC > 20261122T225107Z)

The gate binds the artifact family to the campaign number (`FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z` → prefix `fclr_tracks01_`). Produce every file below. Zero-byte placeholders fail closed.

| # | Artifact (prefix + suffix) | Purpose |
|---|----------------------------|---------|
| 1 | `fclr_tracks01_source_registry_<UTC>.json` **and** `.md` | Complete source registry: every candidate free source for observed liquidations tested, with access proof (HTTP status, ETag/sha256, earliest/latest, schema, gaps, license, rejection reason). Ironflow bulk documented with capped-sample incompleteness per §15. |
| 2 | `fclr_tracks01_probe_<UTC>.py` **and** `.json` **and** `.md` | Automated probe script + results for each candidate source (stdlib + pyarrow; no auth; bounded requests). Proves what is actually accessible without credentials. |
| 3 | `fclr_tracks01_viability_decision_<UTC>.json` **and** `.md` | Frozen viability decision BEFORE outcome inspection: either (a) NEW_TRACK_A_SOURCE_FOUND → name, access method, coverage, next protocol ID; or (b) TRACK_A_STRUCTURALLY_BLOCKED → evidence, Track B pivot protocol ID. Must include `outcome_data_inspected_before_freeze:false` and input sha256 assertions. |
| 4 | `fclr_tracks01_pivot_prereg_<UTC>.json` **and** `.md` | **If Track A blocked:** outcome-blind prereg for new Track B experiment (modeled breach on best free mark-price data). Hypotheses, targets (hourly breach probability per coin, long/short separate), features (funding + RV + price-dislocation per §7), splits (chronological, 48h purge+embargo, non-overlapping 168h blocks), baselines (RV-only vs funding-conditioned), materiality floor (2% rel QLIKE/Brier), Holm family, alpha-spending. **If Track A viable:** prereg for confirmatory Track A on the new source. |
| 5 | `fclr_tracks01_eval_<UTC>.py` **and** `.json` **and** `.md` | **HEAVY EVALUATION (gate-critical).** The actual quantitative evaluation the pivot prereg froze: Track A confirmatory on the new source, or Track B modeled-breach evaluation on the frozen bulk panel. Must report the pre-registered metrics (QLIKE/Brier, materiality floor, Holm-adjusted p, CI) and an honest verdict. |
| 6 | `fclr_tracks01_recompute_<UTC>.py` **and** `.json` | Independent stdlib recompute of the headline statistic(s) in artifact 5, from the same frozen inputs (no shared code path with the eval). Proves the result is reproducible. |
| 7 | `evidence_audit_<UTC>.json` | Gate-critical alias — required by the generic new-heavy-session check (`evidence_audit_` prefix). |
| 8 | `trigger_check_<UTC>.json` | Non-empty trigger check (required by the tracks01 family). |

### Carry-Forward Bundles (pristine copies from `session_20261122T224500Z/`)
Copy these into your new `session_<UTC>/` so older gate bindings stay satisfied:
- `fclr_risk09_*` (7 artifacts)
- `fclr_pooled001_*` (13 artifacts)
- `fclr_pooled_audit001_*` (11 artifacts)
- `fclr_pooled_robust002_*` (11 artifacts)
- `evidence_audit_20261122T190000Z.json`, `trigger_check_20261122T190000Z.json`
- `evidence_audit_20261122T224500Z.json`, `trigger_check_20261122T224500Z.json`

---

## ROOT CONSTRAINTS (hard)

- Root md+json count: **499/500** — at cap. ALL new artifacts MUST go under `session_<UTC>/`. Do NOT add any root-level `research_state/*.md|*.json`.
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax the materiality floor after outcomes.
- Preserve nulls honestly: verdict may be `NEW_TRACK_A_SOURCE_FOUND`, `TRACK_A_STRUCTURALLY_BLOCKED`, or `INCONCLUSIVE` (with evidence).
- Do NOT re-run any terminal campaign (POOLED-001, POOLED-AUDIT-001, POOLED-ROBUST-002, LIVE-ARCHIVE-01/02, LIQ-CONTAGION-001/002, PANEL-FE-001, STARTER-001, RISK-ESCALATION-09, etc.).
- Do NOT build a risk overlay (§9: forecast gate did not pass on ANY primary target).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md`.
- Stdlib + pyarrow only; no network for heavy evaluation (source probes only); no new source without provenance; no overlay.
- Do NOT track-adulterate: never describe Track B (modeled breach) or Track C (volatility) as proof of observed liquidation forecast; never claim a complete observed-liquidation census from a capped feed.
- **Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`** — cannot fire on frozen data; not a valid excuse to idle (§16, §19). The audit + heavy evaluation IS the action.

---

## VERIFICATION (run before declaring done)

```bash
# 1. Heavy-work gate must return reason=OK (not VERIFY_AND_STOP, not BLOCKED)
python3 scripts/check_handoff_heavywork_gate.py --json

# 2. Campaign gate unittests must pass
python3 -m unittest \
  tests.test_active_campaign_gate \
  tests.test_fclr_starter_001_campaign_gate \
  tests.test_fclr_campaign_gate \
  tests.test_fclr_heavy_confirm_gate \
  tests.test_pooled_robust_002_campaign_gate \
  tests.test_tracka_hardening_143

# 3. Frozen 3-block domains exhausted (expected; not a blocker for tracks01)
python3 scripts/next_campaign_status.py
```

The gate fails closed if: this handoff lacks the markers, the newest on-disk session is not recorded here, the newest session lacks the full `fclr_tracks01_*` family (including `fclr_tracks01_eval_*` and `fclr_tracks01_recompute_*`) + `evidence_audit_*.json` + `trigger_check_*.json`, or any required file is zero bytes.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|------|-------------|
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2.85M rows, 2025-05..2026-10. **Capped-sample feed** — not a complete census (per §15). Market values like `BTC-PERP`, `xyz:KIOXIA-PERP`. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet, 3.64M rows, 2025-05..2026-10 |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet, 4.10M rows |
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet, 3.98M rows |
| Binance public archive | `https://data.binance.vision` — HTTP 200 unauthenticated. Metrics (OI + taker flow) 2020-09..2026-11, fundingRate 2020-01..2026-10, klines/markPriceKlines/indexPriceKlines/premiumIndexKlines. **No liquidationSnapshot in public archive.** |
| Hyperliquid / other venues | No verified unauthenticated historical liquidation endpoint with deep history. |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.

---

## KEY FILES TO READ BEFORE STARTING

- `research_state/experiment_frontier.json` — rank-0 entry is `FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z` (status READY_EXECUTE, last_verdict NOT_STARTED).
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement (`TRACKA_SOURCE_AUDIT_CAMPAIGN_RE`; `_tracks01_state`; `fclr_tracks01_*` required set incl. `fclr_tracks01_eval_*` + `fclr_tracks01_recompute_*`; `tracks01` payload key).
- `RESEARCH_PROMPT.md` §5 (source discovery), §15 (label admissibility), §16 (adaptive feasibility), §10 priority #2 (source feasibility map), §3.2 (primary question two halves).
- `research_state/session_20261122T224500Z/fclr_risk09_evaluation_20261122T224500Z.md` — Track A result NOT_SUPPORTED.
- `research_state/session_20261122T190000Z/fclr_pooled_robust002_evidence_audit_20261122T190000Z.md` — Track C result NOT_SUPPORTED_LEAKAGE_ROBUST_NULL.
- `research_state/data_source_registry.json` — if exists, update; if not, create under `session_<UTC>/`.

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **No** prose-only / trigger-only / source-probe-only / audit-only / **prereg-only** / verify-and-stop / placeholder sessions.
- **The heavy evaluation (`fclr_tracks01_eval_*`) and independent recompute (`fclr_tracks01_recompute_*`) MUST be in the SAME session** — the gate fails a prereg-only session closed.
- **No** empty session directories.
- **Do NOT** write a future `session_<UTC>` id into this handoff before that directory exists.
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- **Do NOT** claim completion without the full `fclr_tracks01_*` heavy artifact set under a new `session_<UTC>/` (UTC > 20261122T225107Z).
- **Do NOT** threshold-shop or relax the materiality floor after outcomes; preserve nulls honestly.
- **Do NOT** re-run any terminal campaign.
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE` — cannot fire on frozen data; not a valid excuse to idle.
- **Do NOT** build a risk overlay (§9: forecast gate did not pass).
- **Do NOT** track-adulterate.

---

## SESSION CLOSE-OUT REQUIREMENTS

Before finishing, update THIS file with:
1. What changed and why
2. Exact test outcomes with paths
3. Evidence added and full paths
4. State of each research gate
5. Single highest-value next task (if any)
6. Precise verifying command
7. Any blocker with next materially different route

Then record your `session_<UTC>/` id in this handoff (append the id string `session_<UTC>` so `_latest_handoff_session` picks it up).

---

## BOTTLENECK RESOLUTION (this handoff)

- **Resolved (primary bottleneck):** The prior handoff declared `FCLR-TRACKA-SOURCE-AUDIT-01` "gate-enforced", but `check_handoff_heavywork_gate.py` had **no binder** for it — no `TRACKA_SOURCE_AUDIT` regex, no `_tracks01_state`, no `fclr_tracks01_*` required set. A future agent could skip the entire heavy Track A source audit and the gate would still return `OK`. The previous refresh added the missing binder (`TRACKA_SOURCE_AUDIT_CAMPAIGN_RE`, `_tracks01_state`, `fclr_tracks01_*`, `tracks01` payload key, enforcement block, `fclr_tracks` in `NEW_QUANT_PREFIXES`).
- **Resolved (this refresh — last remaining escape hatch):** Even with the binder, a post-start session could stop at the **pivot prereg** and defer the actual heavy quantitative evaluation to a later session — an audit-only / prereg-only escape hatch. This refresh extends `TRACKA_SOURCE_AUDIT_REQUIRED` with `fclr_tracks01_eval_` (py+json+md) and `fclr_tracks01_recompute_` (py+json), so the heavy evaluation and its independent recompute MUST run in the same session. Verified in an isolated temp repo: a prereg-only session now fails `TRACKA_SOURCE_AUDIT_ARTIFACTS_MISSING` (missing `fclr_tracks01_eval_*` + `fclr_tracks01_recompute_*`); the full heavy set passes.
- **Resolved:** The previous handoff's "Single highest-value next task: None" / "Reopen only on NEW_OBSERVED_LIQUIDATION_SOURCE" prose/probe-only escape hatch (contradicting §16 adaptive feasibility and §19) is replaced by the mandatory, gate-enforced source viability audit + heavy evaluation that either unlocks Track A or formally closes it and pivots to Track B.
- **Resolved:** Root md+json count 499/500 at cap — all new artifacts go under `session_<UTC>/` only.
- No campaign blockers; no external triggers pending; source enumeration and the heavy evaluation are feasible TODAY. Heavy work proceeds without idling.

---

## HANDOFF GENERATED: 2026-11-22T23:49:00Z
**Next session must use UTC > 20261122T225107Z** (campaign start gate).
**Latest handoff session: session_20261122T224500Z** (completed risk09)
**Rank-0 campaign: FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z** (this handoff; gate-enforced via `_tracks01_state`, now including the same-session heavy evaluation `fclr_tracks01_eval_*` + `fclr_tracks01_recompute_*`)