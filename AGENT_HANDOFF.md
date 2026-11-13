# AGENT HANDOFF — 2026-11-13T16:27:42Z

## PROJECT: Funding-conditioned volatility and liquidation risk

**Repository**: `Funding-conditioned-volatility-and-liquidation-risk`
**State**: ALL cached-data experiments EXHAUSTED. Every frozen prereg executed. All campaigns SUPERSEDED_TERMINAL.
**Active Campaign**: `FCLR-NEXT-CAMPAIGN-20261113T091500Z` (rank 0) — six cells COMPLETED, all GATE PASS, all verdicts terminal.

---

## WHAT IS DONE (irreversible, sealed)

| Track | Experiment | Verdict | Key Evidence |
|-------|------------|---------|--------------|
| **Track C / H1** | FCLR-011 (2026-05..2026-08) | **PASS** (4.94% rel QLIKE, CI excludes zero, 5 instr, 3 blocks) | `evaluation_summary_FCLR-011.md` |
|  | FWD-VOL-011-CONFIRM (2026-08..2026-10) | **NOT_REPLICATED** (rel -5.55%, CI favours B1, repro δ=0.044pp) | `evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T061555Z.json` |
|  | FWD-VOL-2025-CROSS (2025-02..2025-05) | **NOT_REPLICATED** (rel +0.29%, CI crosses zero) | `evaluation_summary_FCLR-FWD-VOL-2025-CROSS-20261113T081147Z.json` |
|  | FWD-VOL-2024Q4-CROSS (2024 H2) | **NOT_REPLICATED** (rel -20.77%, LOIO 0/5, placebo fail) | `evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.json` |
|  | FWD-VOL-2025H2-CROSS (2025-07..2025-10) | **NOT_REPLICATED** (rel -8.97%, CI excludes zero favouring B1) | `evaluation_summary_FCLR-FWD-VOL-2025H2-CROSS-20261113T102240Z.json` |
|  | FWD-VOL-2025Q1Q2-CROSS (2026-01..2026-04) | **NOT_REPLICATED** (rel +0.23%, CI crosses zero, LOIO 0/5) | `evaluation_summary_FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111712Z.json` |
| **Track A (Observed Liq)** | LIQ-010-CONFIRM (17 funded HL symbols) | **NOT_REPLICATED** (rel 0.501% < 2% floor, LOIO 0/17, placebo fail) | `evaluation_summary_FCLR-LIQ-010-CONFIRM-20261113T065953Z.json` |
|  | TRACKA-HL-EXPANSION (8 symbols, 2026-05..2026-10) | **PASS PRIMARY** (19.04%, CI [-5.09, -0.48]) | `evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md` |
|  | TRACKA-EXP-ROBUST / EXP-ROBUST-REDO | **FRAGILE** (LOIO 4/8 < 6; placebo true ≤ p95 null) | `evaluation_summary_FCLR-EXP-ROBUST-REDO-20261113T080456Z.json` |
|  | 9-symbol 2026-05..2026-10 (RV) | **NOT_MET** (C2 worse, CI wrong direction) | `evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md` |
| **Track B (Modeled Proxy)** | TB2 (2024, synthetic breach) | **NOT_MET** (rel 1.68% < 2%, 2 blocks < 3) | `evaluation_summary_trackb_TB2_20261110T190405Z.md` |

**Hypothesis Registry**: 31 hypotheses — all `terminal: true` with `terminal_class` ∈ {NOT_SUPPORTED, NOT_MET, NOT_REPLICATED, FRAGILE, EXPLORATORY_ONLY, INCONCLUSIVE_PILOT_SHORTFALL, SUPPORTED_PASS_PRIMARY_GATE}.

**Experiment Frontier**: Rank 0 = `FCLR-NEXT-CAMPAIGN-20261113T091500Z` (ACTIVE_HEAVY_CAMPAIGN, all cells COMPLETED). All prior campaigns demoted to SUPERSEDED_TERMINAL.

**Tests**: 100+ test files guard against false closures, leakage, threshold-shopping, re-running terminal cells, status-only sessions.

---

## WHAT IS BLOCKED (cannot be unblocked by agent action)

| Blocker | Type | Resolution Required |
|---------|------|---------------------|
| **Gate 4 Branch 1** | External/Legal | `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED`, `fabricated=false`, **human/legal attestation**. Never agent-set. Never bypassed. |
| **New observed-liquidation source** | Data availability | Must pass §16 admissibility audit: **≥5 instruments**, **≥1 complete month OR ≥3 non-overlapping 30-day blocks**, **unauthenticated**, **provenance/license**, **venue-consistent**, **observed labels only** (no modeled/proxy). |
| **HL label extension** | Data availability | Verified post-2026-10-31 ironflow labels, **min_depth_days ≥ 100**. Currently ~12 days. No polling. |
| **Expansion robustness redo** | Design | Newly preregistered design meeting **LOIO ≥ 6/8** AND **placebo: true > 95th percentile**. Forbidden: re-scoring sealed 19.04%. |

**All four resume triggers in `resume_trigger_registry.json` have `"do_not_act_until_satisfied": true`.**

---

## THE ONLY FORWARD PATH (heavy work that cannot be avoided)

**Execute bounded alternative liquidation-label source discovery per RESEARCH_PROMPT §5/§16:**

```bash
# 1. Hunt candidate sources (bounded, timestamped)
python3 scripts/hunt_alternative_liquidation_sources.py
# → research_state/data_source_registry_alt_hunt.json
# → research_state/alt_source_deep_review_latest.md
# → research_state/url_probe_cache.json
# → research_state/hf_search_cache.json

# 2. For EACH candidate that passes smoke test: §16 ADMISSIBILITY AUDIT BEFORE OUTCOMES
#    Audit template: research_state/<source>_admissibility_audit_<UTC>.{md,json}
#    Required fields: instruments≥5, blocks≥3 (or complete_month≥1), unauthenticated=true,
#    observed_labels=true, provenance, license, venue_consistent, status=ADMISSIBLE

# 3. IF admissible: FREEZE PREREG PRE-OUTCOMES → build/eval/verdict → atomic state updates
#    New experiment ID. No cherry-picking. No threshold-shopping.

# 4. IF NO source passes: timestamped probe evidence with EXACT failing minima per source,
#    experiment_frontier update, CLEAN STOP — no repeated no-op probes.
```

**Do NOT:**
- Re-run any terminal cell (all have GATE PASS artifacts)
- Re-open sealed verdicts (hypothesis_registry.json is terminal)
- Wait/poll for Gate 4 (external/legal, not agent-removable)
- Poll HL/ironflow (reprobe ONLY when ≥100d depth AND verified post-2026-10-31 labels)
- Produce status-only output

---

## INITIAL TASK FOR NEXT SESSION (timestamped, unambiguous)

> **TASK-20261113T162742Z**: Execute `scripts/hunt_alternative_liquidation_sources.py` to completion. Produce `research_state/alt_source_deep_review_latest.md` with timestamped evidence for EVERY candidate probed, documenting exact failing minima (instruments, blocks, provenance, license, authentication, label type, venue). If ANY candidate passes smoke test → immediately execute §16 admissibility audit (freeze prereg BEFORE outcomes). If ZERO candidates pass → emit timestamped `experiment_frontier.json` update with `blockers: "No admissible observed-liquidation source found; cache frontier exhausted"` and STOP. No status-only session. No re-running terminal cells. No Gate 4 polling.

**Success criteria**: `alt_source_deep_review_latest.md` exists with ≥14 fresh probes (matching 2026-11-13T09:01:19Z baseline), each with pass/fail against §16 minima, OR an admissibility audit artifact with `status=ADMISSIBLE` exists.

**Failure mode**: Session produces only "no candidates found" without timestamped per-source evidence → BLOCKED (violates RESEARCH_PROMPT §16).

---

## KEY FILES TO READ FIRST

1. `research_state/hypothesis_registry.json` — all 31 terminal hypotheses
2. `research_state/experiment_frontier.json` — rank 0 = FCLR-NEXT-CAMPAIGN (all cells done)
3. `research_state/resume_trigger_registry.json` — 4 triggers, all OPEN, do_not_act_until_satisfied
4. `scripts/hunt_alternative_liquidation_sources.py` — the ONLY executable heavy work
5. `tests/test_active_campaign_gate.py` — guards against false terminal closure
6. `tests/test_fclr_final_structural_closure.py` — guards structural closure integrity

---

## COMMANDS TO VERIFY STATE

```bash
# Verify all tests pass (should be 119+ OK)
python -m unittest tests.test_active_campaign_gate tests.test_fclr_final_structural_closure tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit tests.test_fclr_heavy_confirm_gate -v

# Verify hypothesis registry is terminal
python -c "import json; h=json.load(open('research_state/hypothesis_registry.json')); print('Terminal:', all(x.get('terminal') for x in h['hypotheses']), 'Count:', len(h['hypotheses']))"

# Verify frontier rank 0 is FCLR-NEXT-CAMPAIGN with all cells COMPLETED
python -c "import json; f=json.load(open('research_state/experiment_frontier.json')); r0=[x for x in f if x.get('rank')==0]; print(r0[0]['task'], r0[0]['status'], [c['status'] for c in r0[0]['cells']])"
```

---

**This handoff is durable. The next agent MUST start with the hunt script and produce timestamped per-source evidence. There is no other work.**