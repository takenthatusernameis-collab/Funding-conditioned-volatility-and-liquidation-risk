# DELAY-ELIMINATION OVERRIDE — 2026-10-30

**Track A source status is already a documented structural block:** the admissible 2024 Binance liquidationSnapshot/forceOrders probes previously returned 404/451, and no other verified free source was established. Do not repeat the same Track A source sweep on every agent activation.

- Reuse the existing source-attempt evidence and local cache inventory. Re-check Track A only when a genuinely new free source/endpoint, dataset, provider-status change, or network context appears.
- Keep Track B (modeled boundary breaches) as the active path. Run the fast inference path first; preserve the cache and deterministic seed; profile the exact slow stage before attempting the full inference pipeline.
- Parallelize independent symbol/horizon/MMR/leverage/sides calculations only where deterministic outputs and shared-state isolation are preserved. Do not rerun completed cells.
- Run affected unit tests after local changes; run the full test suite after a coherent inference/code batch and at the final decision gate, not after every no-op handoff refresh.
- Do not refresh the timestamp or rewrite handoff-only metadata when no research state changed. A session with no new inference, source evidence, or code change should exit without manufacturing progress.

Do not shorten sample requirements, use paid/signup data, inspect sealed holdouts, or fabricate liquidation labels. A real structural blocker remains a blocker; the optimization is to avoid repeatedly rediscovering it while progressing the independent Track B work.

---

# AGENT HANDOFF — SINGLE DURABLE HANDOFF (LIQUIDATION-RISK CAMPAIGN)

UPDATED: 2026-10-30T22:04:43Z
HEAD: (current)
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY_SOURCE: Repository name inference (funding-conditioned **volatility and liquidation risk**)
DURABLE_HANDOFF: SINGLE_SOURCE_OF_TRUTH
SESSION_GOAL: LIQUIDATION_RISK_HEAVY_CAMPAIGN

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (COPY AND EXECUTE THIS VERBATIM)

**TASK_ID:** `HND-20261030-LIQUIDATION-RISK-003`
**PRIORITY:** P0
**MODE:** HEAVY RESEARCH + ENGINEERING. NO VERIFICATION-ONLY CLOSURE. NO STATUS-POLISHING.

You are continuing from this single handoff. Repository name prioritizes **liquidation risk**.

### CURRENT STATE (DECISION-GRADE)
- Track A (observed liquidation labels): Exhaustive unauthenticated probe of Binance public archive paths (liquidationSnapshot/forceOrders) returned 404/451; no other admissible free sources found with defensible provenance/coverage. Structural block documented.
- Track B (modeled boundary breaches), FCLR-H003-EXT-001: Extended grid (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT), horizons 72h/168h, MMR 0.004/0.005, lev 5x/10x, long/short separate completed. Artifacts: `research_state/protocol_FCLR-H003-EXT-001.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md` (now includes Inference section with block-bootstrap/LOO/Holm/calibration/intensity notes).
- Inference results: C2 (RV+funding+price-dislocation) does not show robust incremental skill over B0 (RV-only). Most ΔBrier CIs cross 0; no cell remains significant after Holm across the declared family. Intensity target blocked by missing OI/volume denominators.

### MANDATORY TASKS (DO IN ORDER)

#### STEP 1: LOCK DECISION ON TRACK B (P0)
1. Review `research_state/evaluation_summary_FCLR-H003-EXT-001.md` Inference section end-to-end. Ensure numbers are consistent with protocol.
2. Update `research_state/hypothesis_registry.json` for FCLR-H003-EXT-001 status to reflect decision-grade inconclusive/no-incremental-skill (or blocked by evidence), with rationale and evidence pointers.
3. Update `research_state/experiment_frontier.json` to mark this track closed with negative/inconclusive result and concrete lessons.
4. Run tests: `python -m unittest discover -s tests -v` (must pass).

#### STEP 2: DOCUMENT TRACK A IRREFUTABLE BLOCK (P0)
1. Create/update `research_state/liquidation_source_campaign.md` with exact sources tested (URLs/paths), methods, results (404/451), rejection reasons, and why no admissible free historical liquidation labels exist in this environment. Be explicit and irrefutable.
2. Ensure no fabricated labels. State "Track A: no admissible observed liquidation dataset found; structurally blocked for this repo/environment."

#### STEP 3: DURABLE HANDOFF UPDATE + NEXT CAMPAIGN (P0)
1. Update this AGENT_HANDOFF.md with updated state, exact commands run, files changed.
2. Propose next highest-value campaign if any remains (or state "campaign complete / no viable path forward without paid data/credentials" with evidence). Do not invent data sources.
3. Commit nothing merely for activity. Only commit if changes are meaningful and coherent.

### HARD CONSTRAINTS
- No credentials/manual inputs. No workflow changes without explicit maintainer auth. No trading/paper trading. Track separation strictly enforced.
- No re-tuning on holdouts. Preserve negative/inconclusive results.
- Do not fabricate data/labels.

### SUCCESS CRITERIA
Durable handoff updated with decision-grade conclusion on liquidation risk (Track B negative/inconclusive with inference), Track A irrefutable structural block documented, hypothesis/experiment frontier updated, tests passing.

**START NOW. FOCUS ON CLOSING LIQUIDATION RISK CAMPAIGN CLEANLY.**
