# FCLR CAMPAIGN NEXT (EXECUTABLE) — 2026-11-06T20:27:26Z (Track A lockdown reference)
**RECONCILED 2026-11-07T00:15:23Z:** Root durable handoff `AGENT_HANDOFF.md` is authoritative. Repo-priority P0 = **Phase 3 funding-conditioned volatility ablations (Gate 4)** using local data (measurable, unblocked). Track A remains **blocked/no trigger** (no re-probe); follow Track A guarded protocol below **only** if trigger appears or a specific gap is hardened with tmp-isolated tests. `FCLR-NEXT-139` numbering retained as Track A campaign marker; do not create status-only churn.

Handoff: `AGENT_HANDOFF.md` (single durable) | Track A ref: FCLR-NEXT-139 | Repo P0: Phase 3/Gate 4

## CURRENT STATE (VERIFIED, Track A guard)
- Trigger: NO TRIGGER (data_through 2026-10; 2026-11..2027-02 absent). Probes==2. Do NOT re-probe.
- Regression: 709 OK, 0 failures, 0 errors
- Drift: pass:true (17/17), network:false, writes_real_research_state:false
- Bounds: root md+json 143/163, no new timestamped probe/sweep/scan/wrapper/report families
- Canonical: frontier/manifest/eval_FCLR010 byte-identical on refusal paths

## IF TRIGGER APPEARS (ADMISSIBLE)
PREREG BEFORE INSPECTING OUTCOMES. Root bound preserved. Only Hyperliquid. Never conflate observed/modeled.
1. Verify admissible manifest + prereg exists/valid (fail-closed)
2. Load only after drift+admissible_seam pass
3. Inspect outcomes with provenance; record blockers
4. Update run_manifest with hashes/timestamps
5. Tests + checks; evidence in AGENT_HANDOFF

## IF TRIGGER DOES NOT APPEAR (DEFAULT - HEAVY WORK)
Lockdown/hardening only. No status files.
1. Extend seam tests: empty/unreadable data path under valid prereg -> blocked with stable reason codes
2. Bulletproof CLI argparse contract on all 3 CLIs (edge cases)
3. Cross-CLI parity + canonical output integrity
4. Add/extend tests (legitimate hardening) keeping regression >=709 OK
5. Verify invariants (17/17, bounds, probes)

## VERIFICATION COMMANDS
```bash
pip install -r requirements.txt
python -m unittest discover tests
python scripts/tracka_resume_check.py
python scripts/tracka_resume_gate.py --bogus --json 2>&1 | head -c 200
python scripts/tracka_resume_check.py --bogus 2>&1 | head -c 200
python scripts/tracka_operator_report.py --bogus --json 2>&1 | head -c 200
```

## ACCEPTANCE CRITERIA
- All tests pass
- Refusals parseable JSON, no tracebacks, exit!=0, canonical outputs unchanged
- Drift 17/17 pass
- Bounds respected, no new families
