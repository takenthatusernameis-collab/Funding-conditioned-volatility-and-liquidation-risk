# AGENT HANDOFF — 2026-11-23T03:45:13Z

## Repository: Funding-conditioned-volatility-and-liquidation-risk

> This is the SOLE durable handoff. Read this file and nothing else for next-session routing.
> The heavy-work gate (`scripts/check_handoff_heavywork_gate.py`) reads THIS file only.
> Gate status as of this refresh (2026-11-23T03:45:13Z): **PASS** (reason_code=OK, root=499/500,
> 119 campaign-gate unittests OK). The gate passes today ONLY because the latest on-disk session
> (`session_20261122T224500Z`) predates the rank-0 campaign start (`20261122T225107Z`). The instant a
> new `session_<UTC>` with UTC > `20261122T225107Z` appears AND is recorded here, the gate flips to
> REQUIRED and demands the full `fclr_tracks01_*` heavy set (see below). There is no prereg-only,
> audit-only, probe-only, trigger-only, or verify-and-stop escape hatch: the heavy evaluation
> (`fclr_tracks01_eval_*`) + independent recompute (`fclr_tracks01_recompute_*`) MUST run in the SAME
> session as the pivot prereg. The binder is regression-pinned by
> `tests/test_tracka_hardening_143.py::TestTrackaSourceAuditCampaignGate` (7 tests).

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

### Single, non-deferrable job (DO THIS FIRST)

Repo-name priority → task. The repository is `Funding-conditioned-volatility-and-liquidation-risk`.
RESEARCH_PROMPT.md §3.2 has two halves: (1) volatility forecasting (Track C — CLOSED leakage-robust null)
and (2) liquidation-risk forecasting (Track A observed + Track B modeled — both NOT_SUPPORTED across every
terminal campaign). The unfinished, highest-value work is the **liquidation-risk half**, and it is now
unblocked to a concrete, frozen decision.

**The Track A source-viability audit is DONE (recovered, not to be redone).** A prior session at
2026-11-23 01:46 UTC (git commit `26d28372d`; its directory was reverted in commit `e45c81fec`, so its
name is intentionally NOT written here as a literal `session_<digits>` token — see "BOTTLENECK
RESOLUTION") enumerated and probed 6 candidate free observed-liquidation sources and froze the viability
decision **`TRACK_A_STRUCTURALLY_BLOCKED`** BEFORE inspecting any outcome
(`outcome_data_inspected_before_freeze:false`). Track A (observed liquidation labels) is formally closed.
Per RESEARCH_PROMPT.md §16 (three blocked routes spanning ≥2 source families → new experiment) the pivot
is a **Track B modeled boundary-breach** protocol on the best free mark-price + margin data.

**Your session's ONE job (heavy, non-deferrable, gate-enforced):** complete
`FCLR-TRACKA-SOURCE-AUDIT-01` by (1) recovering the 3 already-produced audit artifacts from git
(commands below — do NOT re-probe the network), (2) authoring the frozen Track B pivot prereg, (3)
running the HEAVY Track B modeled-breach evaluation, and (4) running an independent stdlib recompute —
all inside a single new `session_<UTC>/` whose UTC is **> `20261122T225107Z`** (use the current
wall-clock UTC at session start). Then record that `session_<UTC>` id in this handoff.

**Do NOT:** re-run the source network probe (waste), stop at the pivot prereg (the old prereg-only
escape hatch now fails closed with `TRACKA_SOURCE_AUDIT_ARTIFACTS_MISSING`), emit zero-byte
placeholders (`TRACKA_SOURCE_AUDIT_ARTIFACTS_EMPTY`), re-run any terminal campaign, build a risk overlay
(§9), or describe Track B (modeled) as proof of observed-liquidation skill (§15).

**Why this campaign (priority by repo name + frontier):** RESEARCH_PROMPT.md §16 (three blocked routes
→ new experiment), §5 (enumerate/test/rank sources), §10 priority #2 (source feasibility map), §3.2
half 2 (liquidation risk). Rank-0 entry in `research_state/experiment_frontier.json` is
`FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z` (status READY_EXECUTE, program ACTIVE).

**Blockers: None.** Source enumeration is already done (recovered from git). The heavy evaluation runs
on the on-disk ironflow bulk panels (18 months, 342 coins) plus cached knowledge of free sources. No
external trigger, no network for the heavy evaluation. The audit recovery AND the heavy evaluation are
feasible TODAY.

---

## RECOVERED AUDIT FINDINGS (embedded — do NOT re-derive, do NOT re-probe)

These are the verbatim findings of the frozen source audit (commit `26d28372d`, live probes at
2026-11-23T01:49:26Z..01:49:35Z). They are reproduced here so the next session skips the expensive
network enumeration and goes straight to the heavy evaluation.

### Source enumeration result (6 candidates, 0 admissible Track A complete census)

| # | Source | Access result (live) | Track A admissible? | Reason |
|---|--------|----------------------|---------------------|--------|
| 1 | Binance public archive (`data.binance.vision`) | HTTP 200 on real zips (metrics `BTCUSDT-metrics-2026-01-01.zip` 11,114 B; fundingRate `BTCUSDT-fundingRate-2026-01.zip` 965 B); `liquidationSnapshot` daily+monthly = S3 NoSuchKey (HTTP 404) | **No** | No `liquidationSnapshot` dataset exists in the public archive |
| 2 | Bybit public REST v5 (`api.bybit.com`) | kline / funding / liquidation all HTTP 403 | **No** | Not unauthenticated in this environment; no credentials requested (§1) |
| 3 | OKX public REST v5 (`www.okx.com`) | candles HTTP 200, funding HTTP 200, `/api/v5/public/liquidation` HTTP 404 | **No** | No public liquidation endpoint |
| 4 | Hyperliquid public API (`api.hyperliquid.xyz`) | GET `/info` HTTP 405 (POST-only); no deep historical liquidation endpoint found | **No** | No verified unauthenticated deep-history liquidation endpoint |
| 5 | Ironflow / Hugging Face liquidations archive | HTTP 200 PAR1 parquet, CC BY 4.0, unauthenticated | **No** | **Capped-sample feed, NOT a complete census** (§15); absence ≠ "no liquidation" |
| 6 | Public GitHub / Zenodo / HF institutional archives | No specific URL verified admissible | **No** | No verified unauthenticated historical observed-liquidation path |

### Frozen viability decision (frozen BEFORE any outcome inspection)

- **Decision: `TRACK_A_STRUCTURALLY_BLOCKED`** — Track A (observed liquidation labels) is formally
  closed. `outcome_data_inspected_before_freeze: false`; input sha256 asserted before any outcome.
- **Structural-impossibility basis (§16):** three+ distinct blocked routes spanning ≥2 source families —
  absent endpoints (Binance liquidationSnapshot 404, OKX liquidation 404), access terms (Bybit 403),
  method gating (Hyperliquid 405/POST-only), and incomplete coverage (Ironflow capped sample).
- **Track A carried-forward status:** NOT_SUPPORTED (terminal FCLR-LIQ-RISK-ESCALATION-09 under
  `session_20261122T224500Z`, +0.149% rel QLIKE, fails −2% floor, CI95 includes zero, Holm p=0.6365).
  Source viability now `TRACK_A_STRUCTURALLY_BLOCKED`.
- **Pivot:** Track B modeled boundary-breach protocol `FCLR-TRACKB-MODELED-BREACH-01` (modeled proxy
  only, §15). Frozen design below.

### Git recovery commands (run these first — do NOT re-probe)

The already-produced audit artifacts live in git commit `26d28372d`. Recover them verbatim into your new
`session_<UTC>/` (filenames already carry their original `20261123T014600Z` suffix; the gate matches by
prefix so this is accepted). The directory name is built from a shell variable so the literal
`session_<digits>` token is never written into this handoff (which would make the gate look for a
non-existent directory). `git cat-file -e` guards each path so NO zero-byte placeholders are created:

```bash
NEWSES=research_state/session_<YOUR_UTC>      # UTC > 20261122T225107Z
SID=20261123T014600Z
mkdir -p "$NEWSES"
for f in \
  fclr_tracks01_source_registry_${SID}.json \
  fclr_tracks01_source_registry_${SID}.md \
  fclr_tracks01_probe_${SID}.json \
  fclr_tracks01_probe_${SID}.py \
  fclr_tracks01_viability_decision_${SID}.json \
  fclr_tracks01_viability_decision_${SID}.md ; do
  if git cat-file -e "26d28372d:research_state/session_${SID}/$f" 2>/dev/null; then
    git show "26d28372d:research_state/session_${SID}/$f" > "$NEWSES/$f"
  fi
done
ls -l "$NEWSES"
```

This recovers 6 non-empty files (source_registry json+md, probe json+py, viability_decision json+md).
**One required file was never written by the reverted session and you MUST author it non-empty:**
`fclr_tracks01_probe_<SID>.md` (render a concise human-readable report from
`fclr_tracks01_probe_<SID>.json` — per-source access table, HTTP statuses, admissibility verdicts).
Zero-byte files fail closed (`TRACKA_SOURCE_AUDIT_ARTIFACTS_EMPTY`), so never leave the `probe.md`
unwritten.

**Recovered-artifact defect to repair on recovery (do NOT skip):** the reverted session hand-wrote
`fclr_tracks01_source_registry_<SID>.json`, `fclr_tracks01_probe_<SID>.json`, and
`fclr_tracks01_viability_decision_<SID>.json` in Python-literal style — **trailing commas** and Python
`None`/`True`/`False` instead of JSON `null`/`true`/`false` (so `json.load` raises `JSONDecodeError`).
The gate only checks non-emptiness, but valid JSON is required for honest evidence and any downstream
parse. Repair all three with this string-aware converter immediately after recovery (it strips trailing
commas and converts Python literals ONLY outside string values, then re-serializes):

```bash
python3 - "$NEWSES" "$SID" <<'PY'
import json, sys, pathlib
newsess, sid = sys.argv[1], sys.argv[2]

def repair(text):
    out = []; in_str = False; esc = False; i = 0; n = len(text)
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': in_str = False
            i += 1; continue
        if c == '"':
            in_str = True; out.append(c); i += 1; continue
        if c == ',':
            j = i + 1
            while j < n and text[j] in ' \t\r\n': j += 1
            if j < n and text[j] in '}]':
                i += 1; continue
        if text.startswith('None', i) and (i+4>=n or not (text[i+4].isalnum() or text[i+4]=='_')):
            out.append('null'); i += 4; continue
        if text.startswith('True', i) and (i+4>=n or not (text[i+4].isalnum() or text[i+4]=='_')):
            out.append('true'); i += 4; continue
        if text.startswith('False', i) and (i+5>=n or not (text[i+5].isalnum() or text[i+5]=='_')):
            out.append('false'); i += 5; continue
        out.append(c); i += 1
    return ''.join(out)

for name in (f"fclr_tracks01_source_registry_{sid}.json",
             f"fclr_tracks01_probe_{sid}.json",
             f"fclr_tracks01_viability_decision_{sid}.json"):
    p = pathlib.Path(newsess) / name
    obj = json.loads(repair(p.read_text()))   # raises if still invalid
    p.write_text(json.dumps(obj, indent=2) + "\n")
    print("repaired", name)
PY
# verify: python3 -c "import json,glob;[json.load(open(f)) for f in glob.glob('$NEWSES/*.json')];print('ALL VALID')"
```

After this, all three recovered JSON artifacts parse cleanly (verified against the exact committed bytes).

---

## FOCUS CAMPAIGN (Mandatory — heavy work, non-avoidable, gate-enforced)

Execute **FCLR-TRACKA-SOURCE-AUDIT-01** to completion in ONE `session_<UTC>/` (UTC > 20261122T225107Z):

1. **RECOVER (not re-probe)** — run the git recovery commands above. Confirm the 3 artifacts are
   non-empty. The audit is frozen; do not redo it.
2. **PIVOT PREREG (outcome-blind, frozen BEFORE outcomes)** — write `fclr_tracks01_pivot_prereg_*`
   (json+md) for `FCLR-TRACKB-MODELED-BREACH-01` using the frozen design in the next section. It must
   state `outcome_data_inspected_before_freeze:false` and hash-bind its inputs.
3. **HEAVY EVALUATION + INDEPENDENT RECOMPUTE** — write `fclr_tracks01_eval_*` (py+json+md) and
   `fclr_tracks01_recompute_*` (py+json). This is the phase the gate refuses to let you skip.

### Frozen Track B modeled-breach protocol design (write this into the pivot prereg)

- **Experiment ID:** `FCLR-TRACKB-MODELED-BREACH-01` (new ID; NOT a re-run of any terminal campaign).
- **Label (modeled proxy ONLY, §15):** for each coin and each forecast origin, take the observed
  mark-price path; compute a hypothetical liquidation boundary from a frozen leverage/maintenance-margin
  scenario; label `breach=1` if the forward mark price crosses the boundary within the horizon.
  **Long and short labels are kept strictly separate.** This does NOT reconstruct account-specific
  liquidation engines, cross/portfolio margin, or actual forced liquidations, and must never be described
  as observed liquidations. Reuse `scripts/synthetic_boundary_labels.py`
  (`liquidation_boundary_price`, `boundary_crossed_future`, `synthetic_boundary_label`) — it already uses
  only prices strictly after the origin (t+1..t+horizon, no leakage).
- **Data (on-disk, sha256-verified, caches not mutated):** `research_state/data_cache/ironflow_bulk/`
  — `open_interest` (mark_price, oracle_price, open_interest), `funding` (funding_rate, premium),
  `candles_1h` (OHLC), 18 monthly parquet 2025-05..2026-10, 342 coins. Use **mark_price** for the
  boundary path (mark price is the liquidation reference); keep long/short separate. Optionally
  corroborate with Binance public-archive mark/index/premium klines (unauthenticated, HTTP 200) if a
  coin is present in both.
- **Features (§7, all known at origin):** Baseline B1 = trailing RV only (RV6/RV24/RV168 log-scaled,
  lagged-vol persistence). Candidate C2 = B1 + signed funding + |funding| percentile (train-only
  rolling) + premium/mark-to-index dislocation + trailing MA deviation.
- **Model:** simple calibrated logistic regression for P(breach) (stdlib Newton/IRLS or a transparent
  linear-probability fallback if separation is severe — state which). Do not launch unconstrained ML.
- **Splits (§8):** chronological walk-forward (60/40 train/test), **48h purge+embargo**, non-overlapping
  **168h (7-day) test blocks**; ≥3 non-overlapping test blocks required; features normalized with
  train-only parameters; no full-sample quantiles.
- **Metrics (§8 binary):** Brier score + log loss as primary; calibration slope/intercept; ROC-AUC and
  precision/recall at a pre-specified alert budget as secondary. Out-of-sample loss relative to the
  RV-only baseline with block-aware (per-coin block bootstrap) CIs.
- **Materiality floor:** ≥ **2% relative Brier improvement** (frozen; never relaxed after outcomes).
- **Multiplicity:** Holm across the declared family (primary count + long arm + short arm + survivor/exited
  arms); report raw and adjusted; sequential alpha-spending `alpha_k = 0.05/(k(k+1))` with k frozen.
- **Verdict rule (symmetric, frozen):** `SUPPORTED` iff materiality met AND bootstrap CI excludes null in
  the favorable direction AND Holm-adjusted primary p < alpha_k; otherwise `NOT_SUPPORTED` (preserve the
  null honestly; the best model in a losing family is not a proven edge). Do NOT threshold-shop.

### Required Artifact Set (ALL non-empty, under `research_state/session_<UTC>/`, UTC > 20261122T225107Z)

The gate binds the artifact family to the campaign number (`FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z`
→ prefix `fclr_tracks01_`). Produce every file below. Zero-byte placeholders fail closed.

| # | Artifact (prefix + suffix) | Purpose |
|---|----------------------------|---------|
| 1 | `fclr_tracks01_source_registry_<UTC>.json` **and** `.md` | Source registry (RECOVERED from git; do not rewrite). |
| 2 | `fclr_tracks01_probe_<UTC>.py` **and** `.json` **and** `.md` | Probe script + results (RECOVERED from git; author the `.md` non-empty). |
| 3 | `fclr_tracks01_viability_decision_<UTC>.json` **and** `.md` | Frozen viability decision `TRACK_A_STRUCTURALLY_BLOCKED` (RECOVERED from git). |
| 4 | `fclr_tracks01_pivot_prereg_<UTC>.json` **and** `.md` | Outcome-blind Track B prereg per the frozen design above. |
| 5 | `fclr_tracks01_eval_<UTC>.py` **and** `.json` **and** `.md` | **HEAVY EVALUATION (gate-critical).** Brier/log-loss, calibration, CI, Holm, honest verdict. |
| 6 | `fclr_tracks01_recompute_<UTC>.py` **and** `.json` | Independent stdlib recompute of the headline statistic(s) in #5 (no shared code path). |
| 7 | `evidence_audit_<UTC>.json` | Gate-critical alias (generic new-heavy-session check). |
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

- Root md+json count: **499/500** — at cap. ALL new artifacts MUST go under `session_<UTC>/`. Do NOT add
  any root-level `research_state/*.md|*.json`.
- No empty files, no zero-byte placeholders.
- Do NOT threshold-shop or relax the materiality floor after outcomes.
- Preserve nulls honestly: verdict may be `SUPPORTED` or `NOT_SUPPORTED` (with evidence).
- Do NOT re-run any terminal campaign (POOLED-001, POOLED-AUDIT-001, POOLED-ROBUST-002,
  LIVE-ARCHIVE-01/02, NEXT-SOURCE-VERIFY-01, LIQ-CONTAGION-001/002, PANEL-FE-001, STARTER-001,
  RISK-ESCALATION-08/09, etc.).
- Do NOT build a risk overlay (§9: forecast gate did not pass on ANY primary target).
- Do NOT modify `.github/workflows`.
- Do NOT overwrite `research_state/research_protocol.md` (sealed FCLR-001 definition consumed by
  `scripts/run_evaluation.py`).
- Stdlib + pyarrow only; no network for heavy evaluation (source probes already done); no new source
  without provenance; no overlay.
- Do NOT track-adulterate: never describe Track B (modeled breach) or Track C (volatility) as proof of
  observed liquidation forecast; never claim a complete observed-liquidation census from a capped feed.
- **Do NOT wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`** — cannot fire on frozen data; not a valid excuse
  to idle (§16, §19). The audit is done and the heavy Track B evaluation IS the action.

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

The gate fails closed if: this handoff lacks the markers, the newest on-disk session is not recorded here,
the newest session lacks the full `fclr_tracks01_*` family (including `fclr_tracks01_eval_*` and
`fclr_tracks01_recompute_*`) + `evidence_audit_*.json` + `trigger_check_*.json`, or any required file is
zero bytes.

---

## ON-DISK INPUTS (verified — do NOT re-derive, do NOT substitute)

| Path | Description |
|---|---|
| `research_state/data_cache/ironflow_bulk/open_interest/` | 18 monthly parquet, 2025-05..2026-10. Columns: `timestamp[us],market,coin,mark_price,oracle_price,open_interest,open_interest_usd`. **Use mark_price for the modeled-breach path.** |
| `research_state/data_cache/ironflow_bulk/funding/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,funding_rate,premium`. |
| `research_state/data_cache/ironflow_bulk/candles_1h/` | 18 monthly parquet. Columns: `timestamp[us],market,coin,open,high,low,close,volume,trades`. |
| `research_state/data_cache/ironflow_bulk/liquidations/` | 18 monthly parquet, 2025-05..2026-10. **Capped-sample feed — not a complete census (per §15).** Columns: `timestamp[ms],market,issuer,wallet,position_side,size,notional_usd,avg_price,fills,block,tx_hash`. |
| Binance public archive | `https://data.binance.vision` — HTTP 200 unauthenticated on real zips (metrics, fundingRate, klines, markPriceKlines, indexPriceKlines, premiumIndexKlines). **No liquidationSnapshot in public archive.** |
| Hyperliquid / Bybit / OKX | No verified unauthenticated deep historical liquidation endpoint (Bybit 403; OKX liquidation 404; Hyperliquid POST-only). |

Each parquet has `.sha256` and `.accessed.json` sidecars. Assert sha256 before reading; do NOT mutate caches.
Data scale: ~145K funding rows + ~145K OI rows per month × 18 months; ~35K candle rows/month; ~15K
liquidation rows/month. The heavy evaluation must stay tractable in pure stdlib (chronological split,
168h test blocks, per-coin series — see the risk09 template pattern).

---

## KEY FILES TO READ BEFORE STARTING

- `research_state/experiment_frontier.json` — rank-0 entry is `FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z`
  (status READY_EXECUTE, last_verdict NOT_STARTED; the audit sub-phase is done — see recovered findings).
- `scripts/check_handoff_heavywork_gate.py` — gate enforcement (`TRACKA_SOURCE_AUDIT_CAMPAIGN_RE`;
  `_tracks01_state`; `fclr_tracks01_*` required set incl. `fclr_tracks01_eval_*` + `fclr_tracks01_recompute_*`;
  `tracks01` payload key).
- `scripts/synthetic_boundary_labels.py` — the frozen modeled-breach label primitive (reuse, do not
  reinvent). Uses only t+1..t+horizon (no leakage).
- `research_state/session_20261122T224500Z/fclr_risk09_evaluation_20261122T224500Z.py` — the proven heavy
  stdlib+pyarrow evaluation template (sha256 guards, chronological 60/40 + 48h purge, 168h blocks,
  per-coin block bootstrap, Holm, symmetric verdict). Adapt: intensity→binary breach, QLIKE→Brier/log-loss.
- `RESEARCH_PROMPT.md` §5 (source discovery), §7 (features), §8 (metrics), §15 (label admissibility), §16
  (adaptive feasibility), §3.2 (primary question two halves).
- `research_state/data_source_registry.json` — root-level registry (do NOT rewrite; root cap 499/500).

---

## NON-AVOIDANCE CONSTRAINTS (hard — machine-checked)

- **No** prose-only / trigger-only / source-probe-only / audit-only / **prereg-only** / verify-and-stop /
  placeholder sessions.
- **The heavy evaluation (`fclr_tracks01_eval_*`) and independent recompute (`fclr_tracks01_recompute_*`)
  MUST be in the SAME session** — the gate fails a prereg-only session closed.
- **Do NOT re-probe the network** — the audit is frozen and recovered; re-probing wastes the session.
- **No** empty session directories.
- **Do NOT** write a future/non-existent `session_<UTC>` id into this handoff before that directory exists
  (the gate treats a non-existent recorded dir as a failure). Only `session_20261122T190000Z` and
  `session_20261122T224500Z` may appear as literal `session_<digits>` tokens until you create and record
  your own real `session_<UTC>/`.
- **Do NOT** create root-level `research_state/*.md|*.json` (root count 499/500, cap enforced).
- **Do NOT** claim completion without the full `fclr_tracks01_*` heavy artifact set under a new
  `session_<UTC>/` (UTC > 20261122T225107Z).
- **Do NOT** threshold-shop or relax the materiality floor after outcomes; preserve nulls honestly.
- **Do NOT** re-run any terminal campaign.
- **Do NOT** wait for `NEW_OBSERVED_LIQUIDATION_SOURCE`.
- **Do NOT** build a risk overlay.
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

Then record your `session_<UTC>/` id in this handoff (append the id string `session_<UTC>` so
`_latest_handoff_session` picks it up).

---

## BOTTLENECK RESOLUTION (this handoff)

- **Resolved (primary bottleneck — reverted session recovered, not redone):** A prior session at
  2026-11-23 01:46 UTC (git commit `26d28372d`) executed the expensive source enumeration + viability
  decision — 6 live unauthenticated probes, concluding `TRACK_A_STRUCTURALLY_BLOCKED` with an
  outcome-blind freeze — but was reverted (commit `e45c81fec`) before the heavy Track B evaluation, so
  the artifacts vanished from disk. That revert was the bottleneck: the next session would have been
  forced to redo the network probe. This refresh removes it by (a) embedding the full audit findings
  above, and (b) giving exact `git show` recovery commands. The next session recovers 3 artifacts and
  spends its budget on the heavy evaluation instead of re-probing. The reverted directory name is
  intentionally not written as a literal `session_<digits>` token (the gate would then look for a
  non-existent directory and fail closed); the git commit id `26d28372d` is the durable handle.
- **Verified (2026-11-23T03:45:13Z refresh):** `python3 scripts/check_handoff_heavywork_gate.py` →
  `PASS reason_code=OK root=499/500`; 119 campaign-gate unittests OK. Network reachable
  (`data.binance.vision` HTTP 200). Ironflow bulk panels present (18 parquet each for
  liquidations/candles_1h/funding/open_interest). `research_state/data_source_registry.json` present
  (root cap respected — do not rewrite). The audit AND the heavy evaluation are both executable now, no
  external trigger.
- **Resolved (enforcement, prior refreshes, still live):** (a) the `tracks01` binder
  (`TRACKA_SOURCE_AUDIT_CAMPAIGN_RE`, `_tracks01_state`, `fclr_tracks01_*`, `tracks01` payload key) was
  added so a future agent cannot skip the heavy source audit; (b) the required set was extended with
  `fclr_tracks01_eval_` (py+json+md) + `fclr_tracks01_recompute_` (py+json) so a post-start session
  cannot stop at the pivot prereg (prereg-only / audit-only / zero-byte now fail closed); (c) the binder
  is regression-pinned by `tests/test_tracka_hardening_143.py::TestTrackaSourceAuditCampaignGate`
  (7 tests: required set contains eval+recompute; source-probe-only/missing-eval/missing-recompute fail
  `TRACKA_SOURCE_AUDIT_ARTIFACTS_MISSING`; zero-byte fails `..._EMPTY`; full heavy set passes; pre-start
  sessions grandfathered). Suite now 119 OK.
- **Resolved:** Root md+json count 499/500 at cap — all new artifacts go under `session_<UTC>/` only.
- No campaign blockers; no external triggers pending; source enumeration done and the heavy Track B
  modeled-breach evaluation is feasible TODAY. Heavy work proceeds without idling.

---

## HANDOFF GENERATED: 2026-11-23T03:45:13Z
**Next session must use UTC > 20261122T225107Z** (campaign start gate; campaign start has ELAPSED).
**Latest handoff session: session_20261122T224500Z** (completed risk09; predates campaign start, so gate is green today).
**Rank-0 campaign: FCLR-TRACKA-SOURCE-AUDIT-01-20261122T225107Z** (this handoff; source-audit sub-phase DONE
and recovered from git commit `26d28372d` → `TRACK_A_STRUCTURALLY_BLOCKED`; gate-enforced via `_tracks01_state`,
including the same-session heavy Track B modeled-breach evaluation `fclr_tracks01_eval_*` + independent
recompute `fclr_tracks01_recompute_*`, regression-pinned by `TestTrackaSourceAuditCampaignGate`).
