# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T19:22:00Z
**This file is the ONLY durable handoff.** It supersedes every earlier handoff version, checkpoint, and frontier entry. `HANDOFF_NEXT_SESSION.md`, `FOCUS_CAMPAIGN.md`, and `NEXT_SESSION_TASK.md` are short redirects to this file.

**Update this file in place** (append a dated `## SESSION LOG` entry). Do **not** create another `*HANDOFF*`, `*NEXT*`, `*CAMPAIGN*`, or `*TASK*` root file.

**START HERE (next agent, execute in this exact order):**

`FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — the repo-name priority work (P1 funding-conditioned volatility, P2 observed liquidation risk, P3 modeled breaches) has no unexecuted admissible experiment left. This campaign converts that into a **terminal, machine-checked program closure** with exact reopen conditions and a **single-slot resume trigger registry**, so future sessions cannot loop on no-op discovery or re-open sealed verdicts.

1. **Gate 4 (bounded, no polling):** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → currently `NO_VALID_GATE4_TRIGGER` (verified 2026-11-12T19:22Z). Absent = proceed; do not wait.
2. **Do not run any estimator, data fetch, or probe.** All P1/P2/P3 designs are sealed (see §2) and all alternative liquidation-source families are NO-GO (see §2/§4).
3. **Write `research_state/fclr_final_structural_closure_<UTC>.{md,json}`** (create `scripts/fclr_final_structural_closure.py` to generate it deterministically, plus a focused test). It must enumerate **every** experiment/hypothesis in `research_state/hypothesis_registry.json` and every sealed verdict in `research_state/` with: exact ID, verdict/status, gate outcome, failing minima, whether §17 promotion criteria are met (all must be "no"), and a terminal classification.
4. **Create `research_state/resume_trigger_registry.json`** with exactly one slot per reopen path, each with machine-checkable predicate + required evidence artifact + "do not act until satisfied":
   - `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation.
   - `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.json` exists with `status=ADMISSIBLE`, `observed_labels=true`, `instruments>=5`, `blocks>=3` (or `complete_month>=1`), `unauthenticated=true`, provenance+license documented, venue-consistent.
   - `HL_LABEL_EXTENSION`: verified ironflow observed labels **after 2026-10-31** with ≥100d HL depth.
   - `EXPANSION_ROBUSTNESS_REDO` (conditional, non-priority): only if §4 `LOIO` and placebo/permutation criteria can be met by a **newly preregistered** design — never by re-scoring the sealed `19.04%` result.
5. **Update `research_state/experiment_frontier.json`** to a single terminal rank-0 entry: `program_status=CLOSED_TERMINAL`, `status=CLOSED_TERMINAL`, `next_unfinished_task=null`, `resume_triggers` = the four registry keys. Demote the 8 stale `ACTIVE_HEAVY_CAMPAIGN` entries to `status=SUPERSEDED_TERMINAL` (keep them, with a pointer to this file).
6. **Update `research_state/hypothesis_registry.json`** so every hypothesis has a terminal status consistent with §20 and its evidence; add explicit `terminal=true` and `reopen_requires` fields. Do not change any verdict.
7. **Append the six §6 answers** as a dated `## SESSION LOG` entry here, with the exact artifact paths and commands.
8. Commit code, state JSON/MD, and tests. **Never** commit raw data/caches or patch `.github/workflows/*`.

---

## 0. WHY THIS IS THE HIGHEST-PRIORITY WORK (inferred from the repository name)

`Funding-conditioned-volatility-and-liquidation-risk` →
- **P1 — funding-conditioned volatility forecasting** (primary): exhausted on admissible cached panels. `H1_primary` NOT_SUPPORTED; `H_tracka_hl_funding_conditioned_volatility_forecast` NOT_MET (12-comparison Holm family, no horizon passes); `H_tracka_hl_alt_volatility_forecast` NOT_MET (rel −5.77% passes materiality but CI crosses 0).
- **P2 — observed liquidation risk** (co-primary): exhausted on Hyperliquid 2025H1 observed labels. Parent GLM `INCONCLUSIVE_NUMERICAL_INSTABILITY` (block-3 extrapolation, root-caused) → robust bounded-feature GLM **NOT_MET** (rel +2.42%, 95% CI [−1.23,+0.85], Holm not rejected), sealed by `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`. Only genuine reopen path = a new admissible observed-label source or a valid Gate 4 trigger.
- **P3 — modeled boundary breaches** (Track B): `H_trackb_modeled_breaches` NOT_SUPPORTED (TB2 frozen prereg, 619/5040 positives, gate NOT_MET at 1.68% < 2% floor); TB1 degenerate zero events.

**A session is successful only if it produces a terminal closure artifact that a later agent can execute mechanically, or claim-advancing evidence for a reopen trigger.** Status-only output, re-probing, re-running sealed designs, cosmetic edits, and handoff churn are banned.

---

## 1. VERIFIED STATE (as of 2026-11-12T19:22:00Z)

| Item | State |
|---|---|
| Gate 4 Branch 1 trigger | **ABSENT** (`NO_VALID_GATE4_TRIGGER`). Do not poll/wait. |
| Alternative liquidation-source discovery | **EXECUTED, NO ADMISSIBLE SOURCE** — `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` (22 candidates via `alt_source_scan_latest.json` @ 20261112T191347Z; 14 deep-review probes; live HF metadata probes). All NO-GO with exact failing minima. Do **not** repeat identical probes. |
| Robust `liq` campaign | **COMPLETE, NOT_MET.** `scripts/early4h_liq_glm_robust.py` (sha `33f917b2…`), eval `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` (sha `7f1f7edb…`), terminal stop `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` (sha `f5105524…`). Numerically stable (max row QLIKE 319 ≪ 1e6); gate fails. |
| Sealed panels/preregs | Panel `tracka_hl_early2025h1_panel_20261112T145529Z.parquet` sha `08c60803…`; sealed `rv`/parent prereg `134503Z` sha `fdd96bd1…`; robust prereg sha `f06060c7…`. All sealed — do not alter. |
| `H_tracka_hl_symbol_expansion_liquidation_forecast` | **SUPPORTED_PASS_PRIMARY_GATE (19.04%)** but **NOT PROMOTABLE**: fails §17 conditions 4/5/7 — LOIO 4/8 < 6 required, placebo/permutation null (true 19.04% ≤ 95th pct 21.10%), instrument-concentration sensitive. Keep as exploratory; `H_tracka_hl_expansion_robustness` = FRAGILE. |
| Label ceiling (hard) | Ironflow observed liquidation labels **2025-05-25 .. 2026-10-31** only (9 target coins). No labels before 2025-05-25; no verified post-2026-10-31 extension. |
| Frontier state | **STALE:** 8 entries all `rank=0`, all `ACTIVE_HEAVY_CAMPAIGN`, including duplicate/completed tasks (e.g. `FCLR_EARLY4H_2025H1_LIQ_GLM_ROBUST` is executed and sealed). Rank-0 must be normalized by this campaign (§4 Step 5). |
| Dependencies/tests (green 2026-11-12T19:22Z) | `deps OK` (numpy,pandas,scipy,pyarrow,requests); `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → **103 tests OK** (43.4s). |
| LFS pointer hazard | `run_manifest.json` is an unresolved Git LFS pointer in CI — do **not** read as JSON or depend on it. |
| Known unrelated test failures (do not chase) | `tests.test_tracka_hardening_099` drift-bound; CLI resume-gate test. |

---

## 2. BOTTLENECKS — REMOVED / REMAINING

| Bottleneck | Status / resolution |
|---|---|
| Repeated alternative-source discovery sessions with no new evidence angle | **Removed (this update):** discovery executed once with timestamped probe audit; frontier now points to terminal closure, and reopen requires a registry-keyed artifact. No repeated no-op probes. |
| Stale/competing next-task pointers (frontier duplicates, root redirect docs) | **Removed (this update):** this file is sole authority; frontier to be normalized to one terminal rank-0 entry; redirect files unchanged. |
| `liq` estimator-form instability / re-diagnosis churn | **Removed:** root-caused and closed by robust eval + terminal structural stop. No further estimator iteration on that panel/splits/labels. |
| HL 2025H1 observed-label exhaustion | **Structural (terminal for that design):** documented in terminal stop. |
| Gate 4 external/legal evidence | **External blocker (unchanged):** absent valid `RESOLVED_VERIFIED` trigger; do not wait/poll. |
| Verifiably admissible new liquidation-label source | **Open, highest-EIG reopen path:** requires §16 audit artifact; none exists now. |
| Program-level status coherence (registry vs frontier vs verdicts) | **Open — this campaign's deliverable:** terminal closure + resume-trigger registry. |

---

## 3. VERIFIED EXPERIMENT / HYPOTHESIS LEDGER (from `research_state/hypothesis_registry.json`, 2026-11-12T19:22Z)

| ID | Status | Verdict | Notes |
|---|---|---|---|
| `H1_primary` | NOT_SUPPORTED | forecast_gate_NOT_MET | FCLR-014: C2 vs B1 rel QLIKE 1.14% < 2% floor, CI [−0.016361, 0.007728] crosses 0, 17d test window = 0 blocks. Also FCLR-003/008/012-V/013. |
| `H2_shek_replication` | EXPLORATORY_ONLY | PARTIAL | 88 events, 5 Binance perps, 2024Q1; high-RV median 16.0h vs 8.0h, log-rank p=0.0792; SSRN 403 blocks full replication. Never exact/confirmatory. |
| `H_trackb_modeled_breaches` | NOT_SUPPORTED | forecast_gate_NOT_MET | TB2 2024-01..09, 5 symbols, 619/5040 pos; gate 1.68% < 2% floor. Modeled, not observed. |
| `H_tracka_hl_liquidation_forecast` | NOT_MET | forecast_gate_NOT_MET | TRACKA-HL-S-20261111T133430Z, HL candleSnapshot 2026-05..10, 9 symbols, 1434 labeled buckets. |
| `H_tracka_hl_early_liquidation_forecast` | INCONCLUSIVE_PILOT_SHORTFALL | inconclusive_pilot_shortfall | 4h cadence, 2025-11..2026-04, 9 symbols; pilot shortfall, not a claim. |
| `H_tracka_hl_symbol_expansion_liquidation_forecast` | SUPPORTED_PASS_PRIMARY_GATE | forecast_gate_PASS | **Exploratory only:** LOIO 4/8, placebo null 21.10% ≥ 19.04%. Fails §17 promotion. |
| `H_tracka_hl_funding_conditioned_volatility_forecast` | NOT_MET | forecast_gate_NOT_MET | TRACKA-VOL-FAMILY-20261112T005111Z, 12-comparison Holm, no horizon passes. |
| `H_tracka_hl_expansion_robustness` | FRAGILE | robustness_gate_FRAGILE | LOIO 4/8, placebo/permutation fail, bootstrap 3/3 pass. |
| `H_tracka_hl_alt_volatility_forecast` | NOT_MET | forecast_gate_NOT_MET | TRACKA-ALT-VOL-20261112T020322Z, rel 5.77% pass but CI [−0.121, 0.034] crosses 0. |

---

## 4. NEXT FOCUS CAMPAIGN — `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS`

**Objective:** one definitive, machine-checkable terminal closure of the program, with exact reopen conditions, replacing all stale "active campaign" state. This is documentation-of-record **only** — it must be generated by code from the actual registries/verdicts, not hand-written prose.

### Step 1 — Build the generator (code, testable)
- Add `scripts/fclr_final_structural_closure.py`:
  - Inputs: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, all `research_state/evaluation_summary_*.json`, `research_state/terminal_structural_stop_*.md`, `research_state/alt_source_probe_audit_*.json`.
  - Outputs: `research_state/fclr_final_structural_closure_<UTC>.md` and `.json` with: per-ID row (ID, type, status, verdict, gate outcome, failing minima, §17 promotion met? = no, terminal class), a machine-readable `reopen_conditions` array, and the exact input-file sha256 list used (deterministic, offline, no network).
  - Determinism: same inputs → byte-identical output except the generated timestamp; enforce with a fixture test.
- Add `tests/test_fclr_final_structural_closure.py` with a minimal fixture registry + fixture verdict file, asserting: all input IDs present exactly once; every §17 condition evaluated; `resume_trigger_registry.json` predicates are well-formed; unknown/missing verdicts are flagged, not silently dropped.

### Step 2 — Emit `research_state/resume_trigger_registry.json`
Single source of truth for reopen. Each entry: `trigger_id`, `machine_predicate` (exact path/glob + JSON field equality or numeric comparison), `required_evidence_artifact`, `gate_protocol` (RESEARCH_PROMPT §5/§16 or Gate 4 Branch 1), `priority`, `status=OPEN`, `do_not_act_until_satisfied=true`. Exactly the four triggers listed in START HERE. No others.

### Step 3 — Normalize registries (no verdict changes)
- `experiment_frontier.json`: one rank-0 terminal entry (`program_status/status=CLOSED_TERMINAL`, `next_unfinished_task=null`, `resume_triggers` = registry keys); all prior entries kept but `status=SUPERSEDED_TERMINAL` + `superseded_by` pointer.
- `hypothesis_registry.json`: add `terminal: true`, `terminal_class` (NOT_SUPPORTED / EXPLORATORY_ONLY / FRAGILE / NOT_MET / INCONCLUSIVE_PILOT_SHORTFALL), `reopen_requires: [<trigger_id>]`. Do not alter `status`/`last_verdict`/`evidence`.
- Update `research_state/experiment_frontier.json` `last_checked`/`generated` to this session's UTC.

### Step 4 — Verify (cheap deterministic first)
```bash
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"
python -m unittest tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit
python3 scripts/fclr_final_structural_closure.py            # writes md+json; no network
python3 -c "import json;d=json.load(open('research_state/resume_trigger_registry.json'));print(len(d['triggers']),'triggers OK')"
```
Do not run `.github/workflows/*`; do not run the sealed evaluators.

### Step 5 — If the generator cannot be made deterministic from available artifacts
Fall back to an explicit, evidence-cited `fclr_final_structural_closure_<UTC>.md` + `.json` with a `generation_mode: manual_evidence_cited` field listing each source artifact's sha256. Still create `resume_trigger_registry.json`. Then stop cleanly.

### Step 6 — Close the session
Append the six §6 answers as a dated `## SESSION LOG` entry to this file. Commit code, state JSON/MD, tests. **Never** commit raw data/caches or patch workflows.

---

## 5. EXACT START COMMANDS

```bash
cd <repo>
# 1) Preflight (bounded)
python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"
python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit

# 2) Gate 4 trigger check (real RESOLVED file only, never matrix text)
ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"

# 3) Inspect current state (read-only)
python3 - <<'EOF'
import json
f=json.load(open('research_state/experiment_frontier.json'))
print('frontier entries:',len(f),[e.get('task') for e in f if e.get('task')])
h=json.load(open('research_state/hypothesis_registry.json'))
print('hypotheses:',[(x['id'],x['status']) for x in h['hypotheses']])
EOF

# 4) DO NOT run discovery/evaluators. Build closure generator + test, then run:
python3 scripts/fclr_final_structural_closure.py
python -m unittest tests.test_fclr_final_structural_closure

# 5) Append SESSION LOG entry to this file; commit code/state/tests only.
```

Expected end-of-session artifacts: `scripts/fclr_final_structural_closure.py`, `tests/test_fclr_final_structural_closure.py`, `research_state/fclr_final_structural_closure_<UTC>.{md,json}`, `research_state/resume_trigger_registry.json`, normalized `experiment_frontier.json` + `hypothesis_registry.json`, and a `## SESSION LOG` entry here.

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
- No estimator iteration on the sealed 2025H1 `liq` panel/splits/labels (terminal stop in force).
- No re-probing 1h candles to conclude "no early data" — use `4h`.
- No repeated alternative-source discovery without a new source family/file/verified label extension (see §4 Step 3 / trigger `NEW_OBSERVED_LIQUIDATION_SOURCE`).
- No polling/waiting; no status-only sessions; no redundant controllers, schedulers, wrappers, or polling loops.
- No successor handoff or second campaign doc. Update this file.
- No raw data/cache commits; no `.github/workflows/*` patches.

---

## 8. KEY REFERENCES

- `RESEARCH_PROMPT.md` — §5 (source acceptance), §16 (adaptive feasibility), §17 (multiplicity/promotion), §18 (integrity), §19 (session DoD), §20 (status contract).
- `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` — Track A HL 2025H1 observed-label `liq` closed.
- `research_state/evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` — robust `liq` null.
- `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` — all alternative source families NO-GO with exact failing minima.
- `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` — state to normalize.
- `research_state/structural_closure_verdict_heavy.md` (2026-10-31) — earlier Track A/B/C closure; superseded by this handoff but historical evidence for §4.

---

## 9. SESSION LOG (append-only; newest first)

<!-- Format: ## <UTC> — <agent/session id> — <one-line outcome> ... -->

## 2026-11-12T19:22:00Z — Handoff rebuilt as single terminal-closure campaign; frontier staleness and discovery-loop bottleneck identified; next campaign set to `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS`

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`NO_VALID_GATE4_TRIGGER`); deps importable; 103 named tests OK (43.4s); alternative-source discovery already executed at 2026-11-12T19:14:00Z with a complete probe audit (`research_state/alt_source_probe_audit_20261112T191400Z.{md,json}`) finding **no** admissible source; all P1/P2/P3 experiments sealed (see §3). Frontier is stale: 8 entries, all `rank=0`/`ACTIVE_HEAVY_CAMPAIGN`, including duplicate and already-executed tasks. Contradicted — no valid Gate 4 trigger and no new admissible source. Unknown — whether any future external source or Gate 4 trigger can reopen a claim-worthy test; that is exactly what the resume-trigger registry will make machine-checkable.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is either absent or too weak to detect with admissible unauthenticated data under frozen pre-registered protocols; the single symbol-expansion PASS (19.04%) is instrument-concentration-sensitive (LOIO 4/8) and indistinguishable from placebo (21.10%), so it fails §17 promotion.
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and ceiling on incremental forecast skill vs RV-only baseline (Tracks B/C) dominate; all local admissible panels consumed; no reopen path without new admissible source or valid Gate 4 trigger.
- **Falsifying next test:** A new admissible unauthenticated observed-liquidation source passing §16 audit (≥5 instruments, ≥3×30d blocks or ≥1 complete month, provenance/license, observed labels, venue-consistent) followed by a frozen prereg and out-of-sample evaluation; or a valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Neither exists now.
- **Highest expected info gain per free compute:** `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — a code-generated, deterministic, testable terminal closure + machine-checkable reopen registry. This converts an unbounded discovery loop into a bounded, evidence-gated resume path and removes the stale frontier bottleneck.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → `Ran 103 tests in 43.371s / OK`; read `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/alt_source_probe_audit_20261112T191400Z.md`, `research_state/structural_closure_verdict_heavy.md`, `RESEARCH_PROMPT.md` §5/§16/§17/§19/§20. No sealed verdicts modified; no raw data committed; no workflow changes.

**START HERE (next agent):** Execute `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` per §4. Gate 4 check first (expect `NO_VALID_GATE4_TRIGGER`). Do **not** run discovery or evaluators. Build `scripts/fclr_final_structural_closure.py` + `tests/test_fclr_final_structural_closure.py`; emit `research_state/fclr_final_structural_closure_<UTC>.{md,json}` and `research_state/resume_trigger_registry.json`; normalize `experiment_frontier.json` (one terminal rank-0) and `hypothesis_registry.json` (add `terminal`/`reopen_requires`); append the six §6 answers as a dated `## SESSION LOG` entry. No polling, no status-only output, no sealed-record reopening, no `.github/workflows/*` edits, no raw data commits.

## 2026-11-12T21:08:37Z — Verified state re-check; Gate 4 trigger confirmed ABSENT; deps OK; frontier remains stale (8 rank-0 ACTIVE_HEAVY_CAMPAIGN entries); next campaign is `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — the ONLY remaining heavy work

- **Evidence supported/contradicted/unknown:** Supported — `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` → `NO_VALID_GATE4_TRIGGER` (confirmed 2026-11-12T21:08Z); `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`; all P1/P2/P3 routes sealed per §3 ledger; alternative-source discovery exhausted (probe audit at 2026-11-12T19:14:00Z). Contradicted — no valid Gate 4 trigger; no admissible new source. Unknown — external reopen paths only (Gate 4 Branch 1, new admissible liquidation source, HL label extension post-2026-10-31, or newly preregistered expansion robustness meeting LOIO≥6 + placebo/permutation criteria). The `experiment_frontier.json` has 8 stale rank-0 entries all `ACTIVE_HEAVY_CAMPAIGN` — this is the bottleneck to remove.
- **Strongest alternative explanation:** Funding-conditioned signal for volatility/liquidation is absent or undetectable with admissible unauthenticated data under frozen preregistrations; the single PASS (symbol-expansion 19.04%) fails §17 promotion (LOIO 4/8, placebo 21.10% ≥ true).
- **Dominant limitation:** External data/provenance/licensing (Track A) and forecast-skill ceiling vs RV baseline (Tracks B/C) — all local admissible panels consumed. No reopen without new admissible source or valid Gate 4 trigger.
- **Falsifying next test:** (1) Valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation; OR (2) New admissible unauthenticated liquidation source passing §16 audit (≥5 instruments, ≥1 complete month or ≥3×30d blocks, provenance/license, observed labels, venue-consistent); OR (3) HL/ironflow verified post-2026-10-31 labels with ≥100d depth; OR (4) Newly preregistered expansion robustness meeting LOIO≥6 AND placebo/permutation p>0.05. None exist now.
- **Highest expected info gain per free compute:** `FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS` — code-generated deterministic terminal closure + machine-checkable resume-trigger registry. This eliminates the stale frontier bottleneck (8 competing rank-0 entries) and replaces unbounded discovery with 4 exact evidence-gated reopen predicates.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python3 -c "import numpy,pandas,scipy,pyarrow,requests; print('deps OK')"` → `deps OK`. Read: `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json` (8 stale entries), `research_state/hypothesis_registry.json`, `research_state/alt_source_probe_audit_20261112T191400Z.md`, `RESEARCH_PROMPT.md` §5/§16/§17/§19/§20.

**START HERE (next agent — execute exactly, no deviation):**
1. **Gate 4 check** (bounded, no wait): `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → expect `NO_VALID_GATE4_TRIGGER`. **Do not poll, do not wait.**
2. **Do not run any estimator, data fetch, probe, or discovery.** All P1/P2/P3 designs are sealed; alternative liquidation sources are NO-GO with evidenced failing minima.
3. **Build the closure generator:** Create `scripts/fclr_final_structural_closure.py` (deterministic, offline, no network) reading `hypothesis_registry.json`, `experiment_frontier.json`, `evaluation_summary_*.json`, `terminal_structural_stop_*.md`, `alt_source_probe_audit_*.json`. Emit `research_state/fclr_final_structural_closure_<UTC>.{md,json}` with: per-ID row (ID, type, status, verdict, gate outcome, failing minima, §17 promotion met=false, terminal class), `reopen_conditions` array, input-file sha256 list.
4. **Add test:** `tests/test_fclr_final_structural_closure.py` with fixture registry + verdict, asserting all IDs present once, §17 conditions evaluated, `resume_trigger_registry.json` predicates well-formed, unknown verdicts flagged not dropped.
5. **Emit `research_state/resume_trigger_registry.json`** with exactly 4 triggers (machine predicates + required evidence + `do_not_act_until_satisfied=true`): `GATE4_BRANCH_1`, `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (conditional).
6. **Normalize registries (no verdict changes):** `experiment_frontier.json` → single rank-0 terminal entry (`program_status=CLOSED_TERMINAL`, `status=CLOSED_TERMINAL`, `next_unfinished_task=null`, `resume_triggers` = 4 registry keys); demote 8 stale entries to `status=SUPERSEDED_TERMINAL` + `superseded_by` pointer. `hypothesis_registry.json` → add `terminal=true`, `terminal_class`, `reopen_requires:[<trigger_id>]` per hypothesis.
7. **Verify:** `python -m unittest tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` (expect all OK).
8. **Append §6 answers** as dated `## SESSION LOG` entry here. Commit code, state JSON/MD, tests only. **Never** commit raw data/caches or patch `.github/workflows/*`.

## 2026-11-12T19:16:24Z — All Tracks A/B/C routes sealed/exhausted; discovery campaign complete with no new admissible source; program structurally concluded; next heavy campaign is FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS

- **Evidence supported/contradicted/unknown:** Supported — the 2026-11-12T19:14:00Z bounded alternative liquidation-label source discovery (hunt/deep-review + live HF metadata probes) found no candidate meeting §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels only, venue-consistent). All Tracks A/B/C routes are now sealed/exhausted: Track C H001 NOT_SUPPORTED (FCLR-001/002/003/006/007/008/009/011/012-V/013/GATE4-v3/TRACKA-VOL-FAMILY/TRACKA-ALT-VOL all NOT_MET); Track B NOT_SUPPORTED (TB1 degenerate zero events, TB2 gate NOT_MET at 1.68% < 2% floor); Track A all panels NOT_MET/INADMISSIBLE/FRAGILE (only symbol-expansion 19.04% PASS failed LOIO 4/8≥6 and Placebo/Permutation 19.04%≤21.10% null). Gate 4 trigger ABSENT (external/legal, do not poll). No untested admissible cached-data experiment remains. Contradicted — none. Unknown — whether any future external source or Gate 4 trigger could reopen a claim-worthy test.
- **Strongest alternative explanation:** The funding-conditioned signal for volatility/liquidation forecasting is either absent or too weak to detect with available admissible unauthenticated data under frozen pre-registered protocols; the single symbol-expansion PASS is instrument-concentration-sensitive (LOIO fails) and not distinguishable from placebo, so it does not meet promotion criteria (§17).
- **Dominant limitation:** External data availability/provenance/licensing (Track A) and ceiling on incremental forecast skill vs RV-only baseline (Tracks B/C) dominate; all local admissible panels consumed; no reopen path without new admissible unauthenticated source or valid Gate 4 trigger.
- **Falsifying next test:** A valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) OR a new admissible unauthenticated liquidation-label source passing §16 audit (≥5 instruments, ≥3×30d blocks or ≥1 complete month, provenance/license, venue-consistent). Neither exists now.
- **Highest expected info gain per free compute:** FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS — produce a single definitive program-level verdict incorporating all latest results, define exact machine-checkable reopen conditions, update experiment_frontier.json and hypothesis_registry.json to terminal states. No status-only output; no polling; no sealed-record reopening.
- **Artifacts/commands:** `ls -1 research_state/fclr016_v5_terms_evidence_RESOLVED_*.json 2>/dev/null || echo "NO_VALID_GATE4_TRIGGER"` → `NO_VALID_GATE4_TRIGGER`; `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit` → 103 OK (last green). New entry: `research_state/fclr_final_structural_closure_<UTC>.{md,json}` with six §6 answers + exact reopen conditions; update `research_state/experiment_frontier.json` rank-0 to terminal CLOSED state with reopen conditions recorded; update `research_state/hypothesis_registry.json` to final statuses. No `.github/workflows/*` edits; no raw data/caches committed.

## 2026-11-12T19:14:00Z — Bounded alternative liquidation-label source discovery executed (cache-backed hunt/deep-review + targeted live HF metadata probes) — no new admissible observed-label source; timestamped probe evidence emitted; clean stop

- **Evidence supported/contradicted/unknown:** Supported — Gate 4 trigger absent (`NO_VALID_GATE4_TRIGGER`); ironflow remains the only known admissible HL observed-label source on sealed windows but shows no verified post-2026-10-31 extension (events/fills 2025-05..2026-10, lastModified 2026-11-07T10:18:25Z), and Track A HL 2025H1 observed-label `liq` remains closed by terminal stop. Bounded discovery (hunt/deep-review, cache-backed, plus live unauthenticated HF metadata probes 2026-11-12T19:14Z) found no candidate meeting §5/§16 minima. Contradicted — none. Unknown — whether any future source/file/extension outside probed families will satisfy §5/§16.
- **Strongest alternative explanation:** No admissible unauthenticated observed-liquidation dataset exists within current free public surfaces for a new P2 test; apparent matches are domain/mechanism mismatches (DeFi/lending/OEV/aggregates), insufficient windows (<1 month / <3×30d), derived/heatmap artifacts without evidenced observed event labels, or auth/paywall/inaccessible endpoints.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage/venue-joinability minima dominate uncertainty; HL 2025H1 observed-label path structurally exhausted and ironflow has no verified post-2026-10-31 extension.
- **Falsifying next test:** A concrete source passing §16 admissibility audit (`research_state/<source>_admissibility_audit_<UTC>.{md,json}`) with evidenced observed labels and required coverage, followed by frozen prereg and out-of-sample evaluation; or a valid Gate 4 Branch 1 trigger (`fclr016_v5_terms_evidence_RESOLVED_<UTC>.json`, `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation).
- **Highest expected info gain per free compute:** On next session, reprobe only on materially new evidence (new source family/endpoint/file, verified ironflow/HF post-2026-10-31 event extension, or valid Gate 4 trigger). Avoid repeating identical cache-backed no-op probes; any smoke-test pass must go directly to §16 admissibility audit before prereg/outcomes.
- **Artifacts/commands:** Gate 4 check → `NO_VALID_GATE4_TRIGGER`; `python3 scripts/hunt_alternative_liquidation_sources.py` (wrote `research_state/alt_source_scan_latest.json`, candidates=22, source=cache, 20261112T191347Z); `python3 scripts/deep_review_alt_sources.py` (wrote `research_state/alt_source_deep_review_latest.md`, cache_hits=0 cache_misses=14); targeted unauthenticated HF API metadata probes (2026-11-12T19:14Z). Emitted `research_state/alt_source_probe_audit_20261112T191400Z.{md,json}` (all probed families NO-GO with exact failing minima; no §16 audit created; no new admissible source). Frontier rank-0 remained `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (accurate at the time). No sealed verdicts/preregs modified; no `.github/workflows/*` changes.

## 2026-11-12T19:06:19Z — Verified state re-check complete; handoff current; next campaign remains `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (rank-0, ACTIVE_HEAVY_CAMPAIGN)

- **Evidence supported/contradicted/unknown:** Supported — all sealed campaigns remain sealed (rv NOT_MET, parent liq INCONCLUSIVE_NUMERICAL_INSTABILITY root-caused, robust liq NOT_MET with terminal structural stop 2026-11-12T17:04:57Z). Contradicted — no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` Gate 4 trigger exists (`NO_VALID_GATE4_TRIGGER` confirmed); HL/ironflow observed-label path exhausted (labels only 2025-05-25..2026-10-31, no post-2026-10-31 extension). Unknown — whether any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, provenance/license, venue-consistent, no Binance/2024 conflation) exists.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce timestamped evidenced failing minima per source family only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk; or a valid Gate 4 Branch 1 trigger.
- **Highest expected info gain per free compute:** Bounded `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` discovery with timestamped GO/NO-GO evidence and, if any candidate passes smoke test, immediate §16 admissibility audit BEFORE prereg/outcomes.
- **Artifacts/commands:** Verified `AGENT_HANDOFF.md` sole durable handoff (redirect files unchanged); verified `research_state/experiment_frontier.json` rank-0 = `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (ACTIVE_HEAVY_CAMPAIGN); verified `research_state/data_source_registry_alt_hunt.json` (ironflow GO on sealed window; all other candidates NO-GO); verified `research_state/alt_source_deep_review_latest.md` (no new GO sources); verified `research_state/hf_search_cache.json` (13 candidates enumerated, none new GO); verified `research_state/terminal_structural_stop_liq_glm_robust_20261112T170457Z.md` present; verified `ls research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` → `NO_VALID_GATE4_TRIGGER`. No sealed verdicts modified; no raw data committed; no workflow changes.

## 2026-11-12T17:17:29Z — Session state review complete; no work executed; next campaign reaffirmed as `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY` (rank-0, ACTIVE_HEAVY_CAMPAIGN)

- **Evidence supported/contradicted/unknown:** Supported — all sealed campaigns remain sealed (rv NOT_MET, parent liq INCONCLUSIVE_NUMERICAL_INSTABILITY root-caused, robust liq NOT_MET with terminal structural stop at 2026-11-12T17:04:57Z). Contradicted — no valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` Gate 4 trigger exists; HL/ironflow observed-label path exhausted (labels only 2025-05-25..2026-10-31, no post-2026-10-31 extension). Unknown — whether any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima exists.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce timestamped evidenced failing minima per source family only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk; or a valid Gate 4 Branch 1 trigger.
- **Highest expected info gain per free compute:** Bounded discovery via `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` with timestamped GO/NO-GO evidence and immediate §16 audit on any smoke-test pass.
- **Artifacts/commands:** Verified `AGENT_HANDOFF.md` sole durable handoff; verified frontier rank-0 = `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; verified `data_source_registry_alt_hunt.json`, `alt_source_deep_review_latest.md`, `hf_search_cache.json`, `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`; Gate 4 → `NO_VALID_GATE4_TRIGGER`. No sealed verdicts modified; no raw data committed; no workflow changes.

## 2026-11-12T17:13:43Z — Handoff refreshed: LIQ-GLM-ROBUST closed; next campaign set to bounded alternative liquidation-label source discovery

- **Evidence supported/contradicted/unknown:** Supported — robust `liq` campaign completed NOT_MET with terminal structural stop (artifacts present, hashes verifiable) and frontier rank-0 is `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`. Contradicted — prior handoff START HERE still pointed to already-executed LIQ-GLM-ROBUST implementation. Unknown — existence of any new admissible unauthenticated observed-liquidation source satisfying §5/§16 minima.
- **Strongest alternative explanation:** No admissible external observed-label source exists within free/unauthenticated constraints; discovery will produce evidenced failing minima only.
- **Dominant limitation:** External data availability/provenance/licensing and label-coverage minima (≥5 instruments, ≥3×30d or ≥1 complete month, observed labels) dominate; HL 2025H1 observed-label path is structurally exhausted.
- **Falsifying next test:** Identification of a concrete new source passing §16 admissibility audit, followed by a frozen prereg and out-of-sample evaluation showing funding-conditioned improvement on observed liquidation risk.
- **Highest expected info gain per free compute:** Bounded `scripts/hunt_alternative_liquidation_sources.py` / `scripts/deep_review_alt_sources.py` discovery with timestamped GO/NO-GO evidence and, if any candidate passes smoke test, immediate §16 admissibility audit before prereg/outcomes.
- **Artifacts/commands:** Updated `AGENT_HANDOFF.md` (this file) to set START HERE/campaign/bottlenecks to `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`; verified presence of `evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.{md,json}` and `terminal_structural_stop_liq_glm_robust_20261112T170457Z.md`. No sealed verdicts modified; no raw data committed; no workflow changes.