# AGENT_HANDOFF.md — SINGLE DURABLE HANDOFF (NEXT SESSION)

**INITIAL TASK MESSAGE (UTC 2026-11-07T11:33:00Z, git `22747332`, working tree clean):** Repo **Funding-conditioned-volatility-and-liquidation-risk**. Repo-name priority (P0 → P2): **Track C funding-conditioned volatility = P0** (Phase 3 / Gate 4 funding-ablations on LOCAL data — measurable, unblocked, per `research_state/FCLR_CAMPAIGN_NEXT.md`) **> Track B (closed/inconclusive) > Track A (BLOCKED/NO TRIGGER — ironflow `data_through=2026-10`; 2026-11..2027-02 confirmed absent 404; do NOT re-probe).** Confirmatory program CLOSED NEGATIVE on all executed claim-worthy panels (H001 NOT_SUPPORTED; overlay INELIGIBLE; Track B closed/inconclusive; Track A BLOCKED/NO TRIGGER). **FCLR-013 (2026 Q3 5-symbol panel, prereg frozen git `08193dd3`) EXECUTED/COMMITTED: gate NOT_MET; Track C funding-conditioned volatility stays closed negative on current admissible data.** Gate 4 v3 (30-day blocks, 5 instruments, 4 non-overlapping blocks) EXECUTED/COMMITTED: data-sufficiency MET but primary contrast E vs A ΔQLIKE +0.4879, CI [-0.0422, 1.1973] spans 0 → NOT claim-worthy statistically; preserved, outcome-free.

**MANDATORY HEAVY-WORK CAMPAIGN (no status-only churn; every session must produce measurable committed progress; future agents may not skip or defer):**

Run in order. Stop cleanly with evidence if any gate fails; do not proceed past a red gate.

**(1) Integrity gates (required, run first — deterministic, <1 min, no network):**
- `pip install -r requirements.txt` → exit 0
- `python -B -m unittest discover -s tests -t .` → **732/732 OK**
- `python -B -m unittest tests.test_fclr_canonical_artifacts -v` → **3/3 OK in <1s**
- `python -B scripts/tracka_resume_check.py` → **pass:true, network:false, writes_real_research_state:false**
Revert any timestamp-only regen (incl. `research_state/ironflow_fastpath_cache.json` `last_tree_ts`). Keep tree clean (`__pycache__` untracked, `.gitignore` covers it). No `.github/workflows` edits. No status-only files.

**(2) Preserve & verify FCLR-013 negative (required, deterministic):** confirm `research_state/evaluation_summary_FCLR-013.md` sha256 **`107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a**` unchanged; C2 vs B1 diff **+0.005953**, CI **[-0.011716, 0.022101]** crosses 0, relative QLIKE reduction **-1.32%** (< 2% floor), gate **NOT_MET**; claim-worthiness NOT_MET (5 instruments PASS; test 36 days = 1 non-overlapping 30-day block < 3). Do NOT overwrite, re-run to change outcomes, threshold-shop, or promote secondary C1-vs-B1 (3.32%, secondary only); no overlay.

**(3) Verify canonical anchors unchanged (required):** `research_state/evaluation_summary_FCLR003.md` sha256 **`a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2**` (C2 vs B1 diff **+0.044013**, CI **[0.001487, 0.093225]**, RR **-10.98%**, NOT_MET). `research_state/run_manifest_funding_v3_30d.json` sha256 **`9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e**` (A_rv_only **0.798319018412711**; E vs A **+0.4879023125556385** CI **[-0.042160777324701186, 1.1973379300276015]** spans 0, n=12969, 120 blocks).

**(4) Reopen-watch / data discovery (the ONLY path to reopen confirmatory — execute, do not merely plan):** Search `research_state/data_cache` and admissible local sources for **NEW** unauthenticated data per `research_state/next_data_discovery_plan.md` GO checklist (≥5 symbols, ≥3 non-overlapping 30-day blocks, provenance/license/schema/coverage OK). Candidate families: alternative Binance paths (liquidations/, liquidationHistory/, forceLiquidation/), OKX/Bybit/Deribit public archives, Zenodo/OSF/arXiv/GitHub/HuggingFace datasets. **NO fetch, NO credentials/paid/manual/API keys/auth bypass, NO network in claim runs.**
- **GO (new admissible source):** PREREG *before any outcome inspection*; run leakage-resistant confirmatory analysis (chronological, purge/embargo≥max horizon, train-only normalization, missing!=0); update manifests/leakage audit/negative report; preserve negatives.
- **NO-GO (no new data — expected default):** commit **one substantive hardening/improvement** (e.g., extend seam tests so empty/unreadable data path under valid prereg blocks with stable reason codes; bulletproof CLI argparse contract on all 3 CLIs; cross-CLI parity + canonical output integrity; add regression tests). Keep 732+ tests + tracka green. Record work in a dated `## SESSION VERIFICATION` note and stop: *"no new admissible unauthenticated data; confirmatory program remains closed negative; no overlay eligible; awaiting NEW admissible unauthenticated data per RESEARCH_PROMPT.md §16."*

**Canonical anchors (committed, outcome-free):**
- FCLR-003: `evaluation_summary_FCLR003.md` sha256 `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2`
- FCLR-013: `evaluation_summary_FCLR-013.md` sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a`
- v3: `run_manifest_funding_v3_30d.json` sha256 `9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e`
- `split_boundaries_fclr003` / `split_boundaries_fclr013` frozen in `research_state/run_manifest.json` — **do not alter**; `frozen_before_outcomes=true`.

**Bottleneck state (2026-11-07T11:33:00Z):** None active in integrity (732 OK, tracka all pass, network:false, writes_real_research_state:false). Tree clean; timestamp-cache churn reverted (`last_tree_ts` → `2026-11-07T10:32:05Z`). **Main blocker (external, not agent-removable):** no **NEW** admissible unauthenticated data meeting the GO checklist (FCLR-013 consumed the 2026 Q3 GO-candidate; 2024 root zips/partial dirs insufficient alone for ≥3×30d/≥5-symbol confirmatory reopen). Track A remains BLOCKED/NO TRIGGER — no liquidation labels; do not re-probe. Bottlenecks removed this session: timestamp-cache churn reverted, `__pycache__` untracked, canonical-artifacts regression test present (3/3), tree clean.

**Guardrails:** PREREG before outcomes for any confirmatory/trigger/instrument-set change. Chronological splits; purge/embargo ≥ max horizon; train-only normalization; missing != 0. Never label modeled breaches as observed liquidations. No overlays/threshold shopping on sealed holdouts. Preserve negative/inconclusive results. No `.github/workflows` edits. No status-only churn. Track A/B/C separation enforced.

**EXPECTED END STATE:** Dated `## SESSION VERIFICATION` in `AGENT_HANDOFF.md` with (a) FCLR-013 negative preserved (hash+metrics), (b) canonical anchors unchanged, (c) tests + tracka pass, (d) hardening gate 3/3 OK, (e) reopen-watch result (GO → preregged confirmatory run; NO-GO → one substantive hardening committed + evidence). If NO-GO: *"no new admissible unauthenticated data; confirmatory program remains closed negative; no overlay eligible; awaiting NEW admissible unauthenticated data per RESEARCH_PROMPT.md §16."* Record exact command outputs, hashes, acceptance outcomes — prose alone is not evidence.

**TIMESTAMP (UTC):** 2026-11-07T11:33:00Z
**REPO (priority):** `Funding-conditioned-volatility-and-liquidation-risk` — Track C funding-conditioned volatility (P0) > Track B (closed) > Track A (BLOCKED/NO TRIGGER).
**AUTHORITY:** This file is the **only** root durable handoff. If `research_state/FCLR_CAMPAIGN_NEXT.md` or stale notes conflict, follow this file and record reconciliation in durable artifacts (not status-only files).

## SESSION VERIFICATION (2026-11-07T11:33:00Z, git `22747332`, working tree clean)
- (a) FCLR-013 negative preserved: sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a`; C2 vs B1 diff +0.005953, CI [-0.011716,0.022101] crosses 0, RR -1.32%, gate NOT_MET.
- (b) Canonical anchors unchanged: FCLR-003 `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2`; v3 `9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e`.
- (c) Integrity: `python -B -m unittest discover -s tests -t .` → 732/732 OK; `python -B scripts/tracka_resume_check.py` → pass:true, network:false, writes_real_research_state:false; deps numpy/pandas/scipy installed.
- (d) Hardening gate: `tests/test_fclr_canonical_artifacts.py` 3/3 OK in <1s (deterministic fast repro-check).
- (e) Bottlenecks removed: timestamp cache churn reverted; `__pycache__` untracked; tree clean; no `.github/workflows` edits; no status-only files. Main blocker: no NEW admissible unauthenticated data (external). Next session must execute campaign items (1)-(4) above and record a new `## SESSION VERIFICATION`.
