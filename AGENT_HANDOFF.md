# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T17:13:43Z
**This file is the ONLY durable handoff.** It supersedes every earlier handoff version and all checkpoints. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are short redirects to this file.

**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file.

**START HERE (next agent):** execute bounded **alternative liquidation-label source discovery** campaign `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (§4). Track A observed-label `liq` on Hyperliquid 2025H1 is **CLOSED** by terminal structural stop `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` (robust bounded-feature GLM numerically stable but `NOT_MET`: rel +2.42%, 95% CI [-1.23,+0.85] crosses 0, Holm not rejected). Do **not** re-run or iterate estimator forms on that panel/splits/labels.

---

## 0. IMMEDIATE FIRST ACTION (do this now, in order)

1. Read only this file. Do not re-verify/re-run sealed campaigns (`rv` NOT_MET, early4h `liq` parent INCONCLUSIVE root-caused, robust `liq` NOT_MET terminal stop).
2. **Gate 4 check (bounded, no polling):** look for a valid `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation evidence. As of this handoff only `*_BLOCKED_*`/`*_UNRESOLVED_*` exist and `RESOLVED_VERIFIED` inside `fclr020_gate4_readiness_action_matrix_latest.json` is a readiness matrix string, **not** a trigger. If a valid trigger exists → execute Gate 4 Branch 1 per protocol; else proceed.
3. **Heavy work now:** run bounded alternative liquidation-label source discovery (§4). Requirement for claim-worthy consideration (RESEARCH_PROMPT §5/§16): **≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, unauthenticated, provenance/license documented, observed labels only, venue-consistent (no Binance/2024 conflation with Hyperliquid windows).**
4. If a source passes smoke test: perform §16 **admissibility audit BEFORE any preregistration/outcome computation** (`research_state/<source>_admissibility_audit_<UTC>.{md,json}`), then only if admissible freeze prereg → build/eval/verdict → atomic state updates under a **NEW** experiment ID. If no source passes: emit timestamped probe evidence with **exact failing minima per source**, update `experiment_frontier.json`, and clean stop. No repeated no-op probes.
5. Do **not** re-fetch/re-window sealed 2025H1 caches, do **not** alter sealed preregs/evals, do **not** poll/wait.

---

## 1. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary). **Answered/exhausted on admissible cached panels:** `rv` sealed `NOT_MET` (`evaluation_summary_EARLY4H-2025H1-20261112T145537Z.*`, panel `08c60803…`); other volatility campaigns sealed (see frontier/history). Do not re-litigate.
- **P2 — observed liquidation risk** (co-primary). **Closed on HL 2025H1 observed labels:** parent GLM `INCONCLUSIVE_NUMERICAL_INSTABILITY` (block-3 extrapolation, root-caused) → robust bounded-feature GLM `NOT_MET` with terminal structural stop. **Only path to advance P2 is a genuinely new admissible observed-label source** (or valid Gate 4 Branch 1 if triggered).
- **P3 — modeled boundary breaches** (Track B) sealed NOT_SUPPORTED across completed windows; not the next highest-EIG free-compute move vs. source discovery.

A session is successful only if it produces **heavy, claim-advancing evidence** (new admissible source → §16 audit → prereg/frozen test path advanced) or a **timestamped, evidenced stop** with exact failing minima per probed source. Status-only output, re-probing without new evidence angle, cosmetic edits, and handoff churn are banned.

---

## 2. VERIFIED STATE (as of 2026-11-12T17:13:43Z)

| Item | State |
|---|---|
| Robust `liq` campaign | **COMPLETE, NOT_MET.** `scripts/early4h_liq_glm_robust.py` (sha `33f917b2…`), eval `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` (sha `7f1f7edb…`), terminal stop `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` (sha `f5105524…`). Numerically stable (max row QLIKE 319≪1e6); gate fails (CI upper +0.85, Holm not rejected). |
| Corrected 2025H1 panel/preregs | Panel `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` sha `08c60803…`; sealed `rv`/parent prereg `134503Z` sha `fdd96bd1…`; robust prereg sha `f06060c7…`. All sealed — do not alter. |
| Label ceiling (hard) | Ironflow observed liquidation labels **2025-05-25 .. 2026-10-31** only (9 target coins). No labels before 2025-05-25; no verified post-2026-10-31 extension evidenced as admissible. |
| Gate 4 Branch 1 trigger | **ABSENT.** No `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (status=RESOLVED_VERIFIED, fabricated=false, human/legal attestation). Do not wait/poll. |
| Frontier rank-0 | `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`, `ACTIVE_HEAVY_CAMPAIGN` (`experiment_frontier.json`, last checked 2026-11-12T17:04:57Z). |
| Dependencies/tests (last green) | `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → 103 tests OK. Re-run only if artifact hashes fail or you change relevant code. |
| LFS pointer hazard | `run_manifest.json` is an unresolved Git LFS pointer in CI — do **not** read as JSON or depend on it. |
| Prior alt-source probes | `data_source_registry_alt_hunt.json`, `alt_source_deep_review_latest.md`, `url_probe_cache.json`, `hf_search_cache.json` exist (last deep review 20261112T075134Z). Treat as cached evidence; do not repeat identical no-op probes — extend with new source families/angles or clearly mark as unchanged with timestamps. |

---

## 3. BOTTLENECKS — REMOVED / REMAINING

| Bottleneck | Status / resolution |
|---|---|
| Stale handoff pointing to already-completed robust `liq` campaign | **Removed (this update):** START HERE now targets `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; robust campaign recorded as closed with artifacts. |
| `liq` estimator-form instability / re-diagnosis churn | **Removed:** root-caused and closed by robust eval + terminal structural stop. No further estimator iteration on same panel/splits/labels. |
| Competing handoff docs | **Removed:** this file sole durable handoff; root redirect files unchanged. |
| Dependency/install wall for agent loop | **Removed (bounded):** deps importable, named tests green. CI workflow provisioning caveat remains external — report only, do not patch `.github/workflows/*`. |
| HL 2025H1 observed-label exhaustion | **Structural (terminal for that design):** documented in terminal stop. |
| Gate 4 external/legal evidence | **External blocker (unchanged):** absent valid RESOLVED_VERIFIED trigger; do not wait/poll. |
| Verifiably admissible new liquidation-label source | **Open, highest-EIG:** requires bounded discovery + §16 audit evidence. |

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`

**Objective:** find and evidence-check a **new admissible observed-liquidation data source** that can support a preregistered funding-conditioned liquidation-risk test (P2), or produce a timestamped evidenced clean stop with exact failing minima per source family.

### Step 1 — Bounded discovery/probe (heavy, evidence-backed)
- Use/extend existing tooling: `scripts/hunt_alternative_liquidation_sources.py`, `scripts/deep_review_alt_sources.py` (and caches) to probe materially distinct unauthenticated source families/methods (per RESEARCH_PROMPT §16 — do not repeat identical failed probes without a new angle).
- For each candidate record: URL/path, auth/payment requirement, HTTP/result evidence, schema/sample fields if accessible, symbols/coverage window, completeness characterization (census vs sample), license/terms/provenance, and **explicit GO/NO-GO** with failing minima (e.g. `<5 symbols`, `<90d / <3×30d blocks`, no liquidation events, auth/paywalled, unknown license, modeled/proxy only).
- Persist/refresh evidence artifacts (timestamped): `research_state/data_source_registry_alt_hunt*.json`, `research_state/alt_source_deep_review*.md`, and/or a new `research_state/alt_source_probe_audit_<UTC>.{md,json}` capturing this session's deltas.

### Step 2 — §16 admissibility audit (BEFORE outcomes/prereg)
- If any candidate passes smoke test, create `research_state/<source>_admissibility_audit_<UTC>.{md,json}` covering: unauthenticated access, provenance/license, coverage (≥5 instruments, ≥3 non-overlapping 30d blocks or ≥1 complete month as applicable), observed-vs-modeled labels, venue consistency, timestamp/clock integrity, joinability to admissible features, and sealed-holdout separation. **No outcome inspection, no threshold shopping.**
- Only if admissible: freeze a new prereg (`research_state/tracka_prereg_<source>_<UTC>.{md,json}`) before any outcome computation, then build/eval/verdict and update `experiment_frontier.json` + `hypothesis_registry.json` atomically under a **NEW** experiment ID.

### Step 3 — If none admissible (expected unless new evidence appears)
- Emit/update a single timestamped evidenced summary of probed families with exact failing minima; ensure frontier remains accurate (`FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` or clean blocked/stop state as warranted by evidence, never fabricated). Stop cleanly — no polling.

### Step 4 — Close the session
- Append a dated `## SESSION LOG` entry to **this file** with the six §6 answers.
- Update `research_state/experiment_frontier.json` if state changed materially.
- Commit scripts/state/docs/manifests/verdicts as appropriate. **Never** commit raw data/caches or patch `.github/workflows/*`.

---

## 5. EXACT START COMMANDS

```bash
cd <repo>
# 1) Bounded preflight (only if hashes suspicious or relevant code changed)
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"
python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit

# 2) Gate 4 trigger check (must be a real RESOLVED file, not matrix text)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# 3) Heavy discovery (inspect CLI/help first; prefer cache-aware bounded runs)
python3 scripts/hunt_alternative_liquidation_sources.py --help 2>&1 | head -120 || python3 scripts/hunt_alternative_liquidation_sources.py
python3 scripts/deep_review_alt_sources.py --help 2>&1 | head -120 || true

# 4) After probes: record timestamped evidence in research_state/*alt_source* and update experiment_frontier.json if needed
```

Expected artifacts at session end (depending on outcome): timestamped probe/audit evidence (`*alt_source*` / `*admissibility_audit*`), and/or frozen prereg+eval for a truly admissible new source, plus a `## SESSION LOG` entry here and any necessary frontier update.

Known pre-existing unrelated failures (do **not** chase): `tests.test_tracka_hardening_099` drift-bound and CLI resume-gate test.

---

## 6. SESSION DEFINITION OF DONE (answer in the handoff)

- What did the evidence support, contradict, or leave unknown?
- Strongest alternative explanation?
- Which data/label/inference limitation dominates uncertainty?
- What concrete new test would falsify the current leading hypothesis?
- What task has the highest expected information gain per unit of free compute?
- Exact artifact and command/test demonstrating progress.

---

## 7. HARD BANS (no exceptions)

- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation with Hyperliquid windows; no venue mixing in one panel.
- No modeled/proxy/synthetic liquidation labels presented as observed.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass; no whole-tree grep for the trigger string.
- No reopening/relitigating/retuning sealed verdicts (Track B/C, FCLR-*, expansion/volatility campaigns, H2, early4h `rv`, early4h `liq` parent/robust).
- No polling/waiting; no status-only sessions; no redundant controllers, schedulers, wrappers, or polling loops.
- **Do not** iterate estimator forms on the sealed 2025H1 `liq` panel/splits/labels (terminal stop in force).
- **Do not** re-probe 1h candles to conclude "no early data" — use `4h`.
- **Do not** create a successor handoff or a second campaign doc. Update this file.
- **Do not** commit raw data/caches or patch `.github/workflows/*`.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §15 (honest label gate), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity), §19 (session DoD), §20 (status contract).
- `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` — Track A HL 2025H1 observed-label `liq` closed.
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` — robust `liq` null.
- `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` — current state/resume triggers.
- `scripts/hunt_alternative_liquidation_sources.py`, `scripts/deep_review_alt_sources.py` — discovery/probe tooling.
- Caches/evidence: `research_state/data_source_registry_alt_hunt.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`.
- Protocol/templates: `research_state/research_protocol_fclr010.md`, `scripts/create_forward_prereg.py`, `scripts/fclr010_harness.py` (note LFS manifest hazard).

---

## 9. SESSION LOG (append-only; newest first)

<!-- Format: ## <UTC> — <agent/session id> — <one-line outcome> ... -->

## 2026-11-12T17:17:29Z — Session state review complete; no work executed; next campaign reaffirmed as `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (rank-0, ACTIVE_HEAVY_CAMPAIGN)

- **Evidence supported/contradicted/unknown:** Supported — all sealed campaigns remain sealed (rv NOT_MET, parent liq INCONCLUSIVE_NUMERICAL_INSTABILITY root-caused, robust liq NOT_MET with terminal structural stop at 2026-11-12T17:04:57Z). Contradicted — no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` Gate 4 trigger exists; HL/ironflow observed-label path exhausted (labels only 2025-05-25..2026-10-31, no post-2026-10-31 extension). Unknown — whether any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, provenance/license, venue-consistent, no Binance/2024 conflation) exists.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce timestamped evidenced failing minima per source family only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk; or a valid Gate 4 Branch 1 trigger.
- **Highest expected info gain per free compute:** Bounded `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` discovery with timestamped GO/NO-GO evidence and, if any candidate passes smoke test, immediate §16 admissibility audit BEFORE prereg/outcomes.
- **Artifacts/commands:** Verified `AGENT_HANDOFF.md` is sole durable handoff (root redirect files unchanged); verified `research_state/experiment_frontier.json` rank-0 = `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; verified `research_state/data_source_registry_alt_hunt.json` (ironflow GO on sealed window; all other candidates NO-GO); verified `research_state/alt_source_deep_review_latest.md` (no new GO sources); verified `research_state/hf_search_cache.json` (13 candidates enumerated, none new GO); verified `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` present. No sealed verdicts modified; no raw data committed; no workflow changes.

**START HERE (next agent):** execute bounded `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` per §4 Steps 1-4. Gate 4 check first: `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"`. Then run discovery: `python3 scripts/hunt_alternative_liquidation_sources.py --help` then inspect/extend source families beyond cached NO-GO entries (do not repeat identical no-op probes). Any passing smoke-test source → `research_state/<source>_admissibility_audit_<UTC>.{md,json}` BEFORE outcomes. No source passes → timestamped evidenced stop with exact failing minima per source, update `experiment_frontier.json`, clean stop. Append dated `## SESSION LOG` entry to this file with six §6 answers.

## 2026-11-12T17:13:43Z — Handoff refreshed: LIQ-GLM-ROBUST closed; next campaign set to bounded alternative liquidation-label source discovery

- **Evidence supported/contradicted/unknown:** Supported — robust `liq` campaign completed NOT_MET with terminal structural stop (artifacts present, hashes verifiable) and frontier rank-0 is `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`. Contradicted — prior handoff START HERE still pointed to already-executed LIQ-GLM-ROBUST implementation. Unknown — existence of any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce evidenced failing minima only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima (≥5 instruments, ≥3×30d or ≥1 complete month, observed labels) dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk.
- **Highest expected info gain per free compute:** Bounded `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` discovery with timestamped GO/NO-GO evidence and, if any candidate passes smoke test, immediate §16 admissibility audit before outcomes.
- **Artifacts/commands:** Updated `AGENT_HANDOFF.md` (this file) to set START HERE/campaign/bottlenecks to `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; verified presence of `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` and `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`. No sealed verdicts modified; no raw data committed; no workflow changes.

## 2026-11-12T17:04:57Z — Executed `FCLR-EARLY4H-2025H1-LIQ-GLM-ROBUST v1`; bounded-feature GLM numerically STABLE (max row QLIKE 319 ≪ 1e6) but gate FAILS (CI upper +0.85, Holm not rejected) → NOT_MET; terminal structural stop emitted; Track A observed-label `liq` on HL 2025H1 CLOSED

- **Evidence supported/contradicted/unknown:** Supported — bounded-feature Poisson/quasi-Poisson GLM (clip+standardize to train [min,max]) eliminates the parent's extrapolation instability: B1/C1/C2 max row QLIKE 213/243/319 (all ≪ 1e6); all models converged. The mean QLIKE reduction is +2.42% (materiality PASS) but 95% CI [−1.23, +0.85] upper > 0 and Holm not rejected (gate FAIL). Block 3 (Oct-2025 spike) diff +1.13 (C2 worse); Block 1 diff −1.70 (C2 better); ETH −2.97, BTC +0.93. Label ceiling hard: ironflow labels only 2025-05-25..2026-10-31; no earlier labels exist. Power adequate (246-261 pos days/block, 1016 paired rows, 9 instruments). Contradicted — parent INCONCLUSIVE_NUMERICAL_INSTABILITY was a bounded-feature problem, not sample/label; robust estimator fixed it. Unknown — whether any admissible cached-data estimator can pass the gate on this source/design; the protocol was frozen, test executed, result is a valid null.
- **Strongest alternative explanation:** The funding/premium signal for liquidation intensity is either absent or too weak to detect with this sample/design under the declared gate (CI + Holm + materiality). The Oct-2025 spike (block 3) hurts C2; block 1 helps; net effect is noise.
- **Dominant limitation:** Out-of-sample uncertainty dominates (CI width ~2.1 QLIKE units on mean ~4.15). Secondary: BTC/ETH concentration (63.6% events / 83.6% notional); hard label ceiling (no pre-2025-05-25 observed labels). No dependency/data/source/pipeline blocker remains.
- **Falsifying next test:** A new admissible observed-liquidation source (≥5 symbols, ≥3 non-overlapping 30d blocks, unauthenticated, provenance/license) per RESEARCH_PROMPT §5/§16; or a valid Gate 4 Branch 1 trigger (fclr016_v5_terms_evidence_RESOLVED_<UTC>.json with status=RESOLVED_VERIFIED, fabricated=false, human/legal attestation). No estimator-form iteration on this panel/splits/labels (prereg forbids; structural stop documented).
- **Highest expected info gain per free compute:** Bounded alternative liquidation-label source discovery (§5) using `scripts/hunt_alternative_liquidation_sources.py` → `research_state/data_source_registry_alt_hunt.json`, `research_state/alt_source_deep_review_latest.md`. If a source passes smoke test: §16 admissibility audit BEFORE prereg/outcomes. If no source passes: timestamped probe evidence with exact failing minima per source, clean stop.
- **Artifacts/commands:** Implemented `scripts/early4h_liq_glm_robust.py`; produced `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` (NOT_MET); emitted `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`; updated `research_state/experiment_frontier.json` (new rank-0 entry: FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY); preflight green (deps OK; 103 tests OK; panel `08c60803…`; prereg `f06060c7…`). No sealed verdicts modified; no raw data committed; workflow not edited.

## 2026-11-12T16:52:59Z — Executed `FCLR-EARLY4H-2025H1-LIQ-GLM v1`; parent `liq` GLM INCONCLUSIVE (block-3 extrapolation); froze `LIQ-GLM-ROBUST v1` as the next campaign

- **Evidence supported/contradicted/unknown:** Supported — the parent log-link GLM is stable except for 1-2 block-3 rows; B1 0/1016 rows > 1e6, C1 1/1016 (block 3/SOL), C2 2/1016 (block 3/SOL,DOGE); block-3 funding/premium/ema_dist are 27.7×/12.5×/4.5× outside train range; every test block has 246-261 positive days (power adequate); labels exist only 2025-05-25..2026-10-31 (no pre-2025-05 labels); BTC+ETH 63.6% events / 83.6% notional. Contradicted — the parent verdict is a global numerical failure: it is localized. Unknown — whether a bounded-feature log-link GLM resolves `liq`.
- **Strongest alternative explanation:** The parent instability is out-of-support extrapolation of raw funding/premium/ema_dist in the Oct-2025 block, not sample size or label availability. Bounding features to the training range should remove it.
- **Dominant limitation:** Out-of-range feature extrapolation in block 3 dominates `liq` uncertainty; secondary BTC/ETH concentration and the 2025-05-25 label ceiling. No dependency/data/source/pipeline blocker remains.
- **Falsifying next test:** `scripts/early4h_liq_glm_robust.py` under the already-frozen prereg on the same panel; a stable `C2_vs_B1` with 95% CI excluding 0 and ≥2% rel QLIKE reduction falsifies "funding does not inform liquidation intensity"; a stable null or a second instability closes `liq` with a terminal stop.
- **Highest expected info gain per free compute:** §4 Steps 2-3 — implement `scripts/early4h_liq_glm_robust.py` (bounded-feature IRLS) → evaluate → adjudicate. No re-fetch, no re-window, no Gate 4, no new source.
- **Artifacts/commands:** Prereg `research_state/tracka_prereg_early2025h1_liq_glm_20261112T164838Z.{json,md}` (sha `d9ebb279…`); script `scripts/early4h_liq_glm.py`; eval `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.{md,json}`; Step 5 audit `research_state/tracka_liq_glm_step5_power_coverage_20261112T165210Z.{md,json}`; frozen robust prereg `research_state/tracka_prereg_early2025h1_liq_glm_robust_20261112T165234Z.{json,md}` (sha `f06060c7…`). Preflight green (deps OK; 103 tests OK; panel `08c60803…`). No sealed verdicts modified; no raw data committed; workflow not edited.

## 2026-11-12T15:54:27Z — Live state re-verified at session start — working tree clean; corrected panel `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet` SHA-256 `08c608035d179be8…` matches; frozen prereg `134503Z` unchanged (`fdd96bd1…`); valid eval `…145537Z` (`rv` NOT_MET, `liq` INCONCLUSIVE_NUMERICAL_INSTABILITY); `scripts/early4h_liq_glm.py` and no `*liq_glm*` prereg exist → campaign UNEXECUTED. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T15:47:45Z — Handoff re-verification + bottleneck sweep — no research outcomes. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T15:38:39Z — Preflight verification session — all preflight checks pass. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T14:56:44Z — Pipeline repair session — root-caused and fixed the degenerate EARLY4H eval; produced valid `rv` NOT_MET + `liq` INCONCLUSIVE; set next GLM campaign. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)

## 2026-11-12T14:37:52Z — Handoff consolidation — clarified state, surfaced degenerate EARLY4H eval, set next heavy task. (Superseded by the 2026-11-12T16:52:59Z entry; retained as history.)
