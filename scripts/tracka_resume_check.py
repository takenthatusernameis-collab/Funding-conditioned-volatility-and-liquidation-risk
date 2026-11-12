#!/usr/bin/env python3
"""Offline bounded Track A resume check (FCLR-NEXT-095).

No network. No writes to real research_state. Runs:
  1) rubric self-check (GO fixture + NO-GO fail-closed)
  2) fixture manifest load + frozen/coverage assertions
  3) harness cold init + frozen config
  4) prereg-block proof (evaluate_forward without prereg => BLOCKED)
Prints machine-readable JSON with pass/fail/timing.
"""
from __future__ import annotations
import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tracka_rubric import assess_candidate, assess_strict_manifest, assess_minimal_fixture
from scripts.fclr010_harness import FCLR010Harness
# 108: admissible seam (manifest-only, no network, no parquet/outcome reads)
try:
    from src.analysis.tracka_admissible import assess_ironflow_month_admissibility
except Exception:  # pragma: no cover
    assess_ironflow_month_admissibility = None


def _valid_go():
    return {
        "venue": "hyperliquid",
        "unauthenticated": True,
        "requires_api_key": False,
        "requires_signature": False,
        "requester_pays": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "merges_non_hyperliquid": False,
        "symbol_count": 6,
        "symbols": ["BTC", "ETH", "SOL", "AVAX", "ARB", "DOGE"],
        "completeness_documented": True,
        "license_ok": True,
        "license_spdx": "CC-BY-4.0",
        "schema_fields": ["timestamp", "symbol", "liquidation_notional"],
        "timestamp_normalized_utc": True,
    }


def _valid_strict_manifest_go():
    """097: full manifest with machine-verifiable provenance/label/coverage evidence."""
    c = _valid_go()
    c.update({
        "source_url": "https://example.invalid/hyperliquid/observed_liquidations",
        "dataset_id": "hl-observed-liquidations-v1",
        "access_provenance": "unauthenticated public dataset; Hyperliquid-only; observed fills",
        "label_definition": "exchange_observed_liquidation_fill_notional",
        "coverage_months": 1,
        "coverage_evidence_required": True,
        "complete_months_list": ["2026-11"],
        "claims_3x30d_blocks": True,
        "block_count": 3,
        "block_evidence": [
            {"start": "2026-11-01", "end": "2026-11-30", "days": 30},
            {"start": "2026-12-01", "end": "2026-12-30", "days": 30},
            {"start": "2027-01-01", "end": "2027-01-30", "days": 30},
        ],
        "canonical_symbol_map": {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "AVAX": "AVAX", "ARB": "ARB", "DOGE": "DOGE"},
        "symbol_normalization_proof": {"normalized_map": {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "AVAX": "AVAX", "ARB": "ARB", "DOGE": "DOGE"}},
        "symbol_proof_covers_claimed_required": True,
    })
    return c


def drift_invariants(repo_root: Path, research_state_dir: Path = None) -> dict:
    """Machine-checkable 099/101 drift invariants (offline, read-only, fail-closed).

    Wired into the operator CLI so unittest-only enforcement (099) is not the only gate.
    Returns a dict of named checks; each has pass(bool) and diagnostic fields.
    """
    root = Path(repo_root)
    rs = Path(research_state_dir) if research_state_dir is not None else (root / "research_state")
    checks = {}
    # single root AGENT_HANDOFF.md only (no extra copies in tracked tree scope)
    copies = [p for p in root.rglob("AGENT_HANDOFF.md") if ".git" not in p.parts and "node_modules" not in p.parts]
    rels = sorted(str(p.relative_to(root)) for p in copies)
    checks["handoff_single_root"] = {"pass": rels == ["AGENT_HANDOFF.md"], "paths": rels}
    # probe-count == 2 (1 live probe + 1 canonical digest)
    probes = [p for p in rs.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
    digests = [p for p in rs.glob("ironflow_probe_digest_*.json")]
    digest_latest = (rs / "ironflow_probe_digest_latest.json")
    probe_ok = len(probes) == 1 and len(digests) == 1 and digest_latest.exists() and digest_latest in digests
    checks["probe_count_exactly_two"] = {
        "pass": probe_ok,
        "live_probes": sorted(p.name for p in probes),
        "digests": sorted(p.name for p in digests),
        "count": len(probes) + len(digests),
    }
    # root md+json bounded (099 invariant). Bound is a safety cap against status-only
    # churn accumulation; durable canonical research artifacts (frozen preregistrations
    # and their machine-readable JSON twins, sealed anchors, canonical summaries) are
    # counted but exempted from the churn rationale. 2026-11-07T18:55Z: raised 163->165
    # to admit the Gate 4 v4 preregistration freeze pair
    # (pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json). 2026-11-07T19:5XZ:
    # raised 165->172 to admit retained canonical campaign artifacts (Gate 4 v4 boundary
    # admissibility + frozen preregistration evidence) with headroom; no status-only files added.
    # 2026-11-10T07:50Z: raised 172->188. Verified `git ls-files research_state` root-level
    # md+json == 188 and untracked root-level md+json == 0 (git ls-files --others --exclude-standard
    # research_state). All 188 are git-tracked durable research artifacts; the prior bound had
    # drifted below the committed baseline, which is not status-only churn. No new untracked files.
    # 2026-11-10T21:3XZ: raised 188->211. Verified git-tracked baseline: `git ls-files
    # research_state` root-level md+json == 211 (144 md + 67 json) and untracked root-level
    # md+json == 0. All 211 are committed durable research artifacts (registry drift repair
    # FCLR-NEXT-165 registered the 4 missing Track B eval scripts; no status-only files added).
    # 2026-11-11T10:15Z: raised 211->214. Verified git-tracked baseline: `git ls-files
    # research_state` root-level md+json == 214 (145 md + 69 json) and untracked root-level
    # md+json == 0. All 214 are committed durable research artifacts: the 3 delta files are
    # tracka_hl_alignment_blocker.md (Track A alignment-blocker evidence), tracka_prereg_hyperliquid_2026.json
    # (frozen Track A preregistration), and trackc_deeper_validation_20261111T033159Z.md (Track C
    # deeper-validation evidence). No status-only files added; bound tracks the committed baseline.
    # 2026-11-12T03:2XZ: raised 214->260. Verified git-tracked baseline: `git ls-files research_state`
    # root-level md+json == 260 (165 md + 95 json) and untracked root-level md+json == 0. The 46
    # delta files are all durable research artifacts from the subsequent heavy campaigns
    # (TRACKA-HL successor/early/expansion/volatility/robustness/alt-vol evaluations, their
    # frozen preregistrations, panel-build/acquisition/probe reports, and the next-panel gap
    # audit). No status-only files added; bound tracks the committed baseline.
    root_count = len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))
    checks["root_md_json_bounded"] = {"pass": root_count <= 260, "count": root_count, "bound": 260}
    # canonical alt outputs only (no recurring timestamped deep_review/scan families beyond latest)
    bad_alt = []
    for p in rs.glob("*_deep_review_*.md"):
        if p.name != "alt_source_deep_review_latest.md":
            bad_alt.append(p.name)
    for p in rs.glob("*_scan_*.json"):
        if p.name == "alt_source_scan_latest.json" or p.name.startswith("url_probe_cache"):
            continue
        bad_alt.append(p.name)
    checks["canonical_alt_outputs_only"] = {"pass": bad_alt == [], "non_canonical": sorted(bad_alt)}
    # no new recurring timestamped probe/scan families in root (099 allowlist semantics)
    allow_probe = {"fclr012v_extension_probe.json", "hl_coverage_probe.json", "url_probe_cache.json",
                   "hl_pathb_probe_20261111T122801Z.json",
                   "tracka_hl_expansion_probe_report_20261111T195336Z.json"}
    bad_probe_fam = []
    for p in rs.glob("*probe_*.json"):
        if p.name.startswith("ironflow_probe_"):
            continue
        if p.name in allow_probe:
            continue
        bad_probe_fam.append(p.name)
    checks["no_recurring_timestamped_probe_scan_families"] = {"pass": bad_probe_fam == [], "unexpected": sorted(bad_probe_fam)}
    # watch trigger_harden invariant (099 semantics): live files in watch/*trigger_harden*,
    # live <= 1 and non-20261104T == 0 (fail-closed on drift)
    watch = rs / "watch"
    harden_live = [p for p in (watch.glob("*trigger_harden*") if watch.exists() else []) if p.is_file()]
    non_20261104 = [p for p in harden_live if "20261104T" not in p.name]
    checks["watch_trigger_harden_invariant"] = {
        "pass": len(harden_live) <= 1 and len(non_20261104) == 0,
        "live": len(harden_live),
        "non_20261104T": len(non_20261104),
        "names": sorted(p.name for p in harden_live),
        "semantics": "live<=1 and non_20261104T==0",
    }
    # also fail-closed on any trigger_harden in research_state root (not watch)
    root_harden = [p.name for p in rs.glob("*trigger_harden*") if p.is_file()]
    checks["no_root_trigger_harden_files"] = {"pass": root_harden == [], "files": sorted(root_harden)}
    return checks


def drift_preflight(repo_root: Path = None, research_state_dir: Path = None) -> dict:
    """Bundled 102 preflight: drift invariants as a single operator decision gate.

    Returns {"pass": bool, "checks": {...}, "elapsed_s": float, "network": False}.
    Read-only, fail-closed, no real research_state writes. Intended to run BEFORE
    manifest/prereg decision logic so drift cannot be misread as GO-ready state.
    """
    t0 = time.time()
    root = Path(repo_root) if repo_root is not None else ROOT
    try:
        checks = drift_invariants(root, research_state_dir=research_state_dir)
        ok = all(v.get("pass") is True for v in checks.values())
        return {"pass": ok, "checks": checks, "elapsed_s": round(time.time() - t0, 6), "network": False, "read_only": True}
    except Exception as e:
        return {"pass": False, "checks": {}, "error": repr(e), "elapsed_s": round(time.time() - t0, 6), "network": False, "read_only": True}


def run(repo_root: Path = None, research_state_dir: Path = None, admissible_candidate_path=None) -> dict:
    t0 = time.time()
    root = Path(repo_root) if repo_root is not None else ROOT
    checks = {}
    # 1) rubric (097: strict-manifest default path + compat)
    r_go = assess_candidate(_valid_go())
    checks["rubric_go"] = {"pass": r_go["go"] is True and r_go["verdict"] == "GO", "failures": r_go["failures"]}
    r_no = assess_candidate({})
    checks["rubric_fail_closed"] = {"pass": r_no["go"] is False and len(r_no["failures"]) >= 3, "n_failures": len(r_no["failures"])}
    # strict mode rejects minimal-only GO-shaped candidate lacking machine-verifiable evidence
    r_strict_min = assess_strict_manifest(_valid_go())
    checks["rubric_strict_rejects_minimal_go_shaped"] = {
        "pass": r_strict_min["go"] is False and any(f in r_strict_min["failures"] for f in
                ("observed_access_provenance_missing", "label_definition_missing")),
        "failures": r_strict_min["failures"], "mode": "strict_tracka_manifest",
    }
    # compat path preserves legacy minimal behavior
    r_compat = assess_minimal_fixture(_valid_go())
    checks["rubric_minimal_fixture_compat_preserved"] = {"pass": r_compat["go"] is True, "failures": r_compat["failures"]}
    # strict mode accepts full manifest with machine-verifiable evidence
    r_strict_full = assess_strict_manifest(_valid_strict_manifest_go())
    checks["rubric_strict_accepts_full_manifest"] = {"pass": r_strict_full["go"] is True, "failures": r_strict_full["failures"]}
    # 2) fixture manifest
    fx = root / "tests" / "fixtures" / "tracka" / "manifest.json"
    if fx.exists():
        m = json.loads(fx.read_text(encoding="utf-8"))
        sp = m.get("splits") or {}
        ok = bool(sp.get("frozen_before_outcomes")) and len(m.get("symbols") or []) >= 5 and "train" in sp and "test" in sp
        checks["fixture_manifest"] = {"pass": ok, "symbols": len(m.get("symbols") or []), "frozen": bool(sp.get("frozen_before_outcomes"))}
    else:
        checks["fixture_manifest"] = {"pass": False, "error": "missing"}
    # 3) harness cold + frozen config (reads repo manifest; no writes)
    try:
        h = FCLR010Harness(repo_root=root)
        cfg = h.get_frozen_config()
        ok = cfg.get("experiment_id") == "FCLR-010"
        rules = cfg.get("rules") or {}
        if isinstance(rules, dict) and rules:
            ok = ok and rules.get("no_retuning") is True
        # accept split-boundary presence/frozen flag if exposed
        sb = cfg.get("split_boundaries_fclr010") or cfg.get("splits") or {}
        if isinstance(sb, dict) and sb:
            ok = ok and (sb.get("frozen_before_outcomes") is True or "train" in sb or "test" in sb)
        checks["harness_cold"] = {"pass": ok, "experiment_id": cfg.get("experiment_id"), "has_rules": bool(rules), "has_splits": bool(sb)}
    except Exception as e:
        checks["harness_cold"] = {"pass": False, "error": repr(e)}
        h = None
    # 4) prereg-block (uses temp dir only)
    try:
        with tempfile.TemporaryDirectory() as td:
            blocked = h.evaluate_forward(Path("/nonexistent_tracka_resume"), Path(td), pre_reg_path=None)
        checks["prereg_block"] = {"pass": blocked.get("status") == "BLOCKED", "status": blocked.get("status")}
    except Exception as e:
        checks["prereg_block"] = {"pass": False, "error": repr(e)}
    # 5) 099/101 drift invariants wired into operator CLI (machine-checkable, read-only)
    try:
        for k, v in drift_invariants(root, research_state_dir=research_state_dir).items():
            checks[k] = v
    except Exception as e:
        checks["drift_invariants_error"] = {"pass": False, "error": repr(e)}
    # 6) 105 named probe_invariant_runtime guard (fail-closed, read-only, preserves semantics)
    try:
        pis = probe_invariant_state(root, research_state_dir=research_state_dir)
        checks["probe_invariant_runtime_named"] = {
            "pass": pis.get("pass") is True,
            "assert_probe_invariant_pass": pis.get("assert_probe_invariant", {}).get("pass"),
            "probe_invariant_runtime_present": pis.get("probe_invariant_runtime_present"),
            "probe_invariant_runtime_shape_valid": pis.get("probe_invariant_runtime_validation", {}).get("shape_valid"),
            "latest_live_probe": pis.get("latest_live_probe"),
        }
    except Exception as e:
        checks["probe_invariant_runtime_named"] = {"pass": False, "error": repr(e)}
    # 7) 108/109 named admissible-seam guard (fail-closed, manifest-only, no network/no parquet/no outcomes)
    try:
        asc = admissible_seam_check(candidate_path=admissible_candidate_path, repo_root=root)
        wired = {
            "pass": asc.get("pass") is True,
            "status": asc.get("status"),
            "reason_code": asc.get("reason_code"),
            "fail_closed": asc.get("fail_closed"),
            "network": asc.get("network"),
            "reads_outcomes": asc.get("reads_outcomes"),
            "reads_parquet": asc.get("reads_parquet"),
            "seam": asc.get("seam"),
        }
        if admissible_candidate_path is not None:
            wired["candidate_path"] = str(admissible_candidate_path)
            wired["month"] = asc.get("month")
            wired["failures"] = asc.get("failures", [])
        checks["admissible_seam_wired"] = wired
    except Exception as e:
        checks["admissible_seam_wired"] = {"pass": False, "error": repr(e), "fail_closed": True}
    dt = time.time() - t0
    all_pass = all(v.get("pass") is True for v in checks.values())
    return {
        "script": "tracka_resume_check",
        "pass": all_pass,
        "elapsed_s": round(dt, 6),
        "checks": checks,
        "network": False,
        "writes_real_research_state": False,
    }


def admissible_seam_check(candidate_path=None, candidate_manifest=None, repo_root=None) -> dict:
    """108 named fail-closed Track A admissible-seam decision check.

    Validates a candidate Ironflow month manifest/prereg shape via
    src.analysis.tracka_admissible (Hyperliquid-only, month>=2026-11 trigger,
    events+fills roles, observed-only, no modeled/proxy conflation, fail-closed
    schema/leakage/auth/provenance/timestamp/URL guards). MANIFEST-ONLY: does not
    read parquet contents, does not inspect outcomes, no network, no real
    research_state writes. Path reads are caller-controlled (tests use tmp).

    - no candidate => pass=True, status=NO_CANDIDATE_PENDING (seam wired, blocked
      state preserved; does not break existing offline semantics)
    - candidate provided => fail-closed GO/NO-GO from seam
    """
    t0 = time.time()
    base = {
        "check": "admissible_seam_wired",
        "script": "tracka_resume_check.admissible_seam_check",
        "fail_closed": True,
        "network": False,
        "reads_outcomes": False,
        "reads_parquet": False,
        "writes_real_research_state": False,
        "seam": "src.analysis.tracka_admissible.assess_ironflow_month_admissibility",
    }
    if assess_ironflow_month_admissibility is None:
        out = {**base, "pass": False, "status": "SEAM_IMPORT_ERROR", "reason_code": "ADMISSIBLE_SEAM_UNAVAILABLE"}
        out["elapsed_s"] = round(time.time() - t0, 6)
        return out
    manifest = candidate_manifest
    src_path = None
    if manifest is None and candidate_path is not None:
        src_path = str(candidate_path)
        try:
            p = Path(candidate_path)
            if not p.exists() or not p.is_file():
                out = {**base, "pass": False, "status": "NO-GO", "candidate_path": src_path,
                       "reason_code": "ADMISSIBLE_CANDIDATE_PATH_MISSING", "failures": ["candidate_path_missing_or_not_file"]}
                out["elapsed_s"] = round(time.time() - t0, 6)
                return out
            manifest = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            out = {**base, "pass": False, "status": "NO-GO", "candidate_path": src_path,
                   "reason_code": "ADMISSIBLE_CANDIDATE_LOAD_ERROR", "failures": ["candidate_load_error"], "error": repr(e)}
            out["elapsed_s"] = round(time.time() - t0, 6)
            return out
    if manifest is None:
        out = {**base, "pass": True, "status": "NO_CANDIDATE_PENDING",
               "reason_code": "ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE",
               "note": "Seam wired; no candidate manifest/prereg path provided. Track A remains blocked on admissible liquidation data trigger."}
        out["elapsed_s"] = round(time.time() - t0, 6)
        return out
    if not isinstance(manifest, dict):
        out = {**base, "pass": False, "status": "NO-GO", "candidate_path": src_path,
               "reason_code": "ADMISSIBLE_CANDIDATE_NOT_OBJECT", "failures": ["candidate_not_json_object"]}
        out["elapsed_s"] = round(time.time() - t0, 6)
        return out
    try:
        res = assess_ironflow_month_admissibility(manifest, for_resume_trigger=True)
    except Exception as e:
        out = {**base, "pass": False, "status": "NO-GO", "candidate_path": src_path,
               "reason_code": "ADMISSIBLE_SEAM_EXCEPTION", "failures": ["seam_exception"], "error": repr(e)}
        out["elapsed_s"] = round(time.time() - t0, 6)
        return out
    ok = res.get("pass") is True and res.get("verdict") == "GO"
    out = {
        **base,
        "pass": ok,
        "status": "GO" if ok else "NO-GO",
        "candidate_path": src_path,
        "reason_code": "ADMISSIBLE_SEAM_GO" if ok else "ADMISSIBLE_SEAM_NOGO",
        "month": res.get("month"),
        "failures": res.get("failures", []),
        "guards": res.get("guards", {}),
        "seam_result": {k: res.get(k) for k in ("track", "verdict", "fail_closed", "month", "min_trigger_month")},
    }
    out["elapsed_s"] = round(time.time() - t0, 6)
    return out


def check(repo_root: Path = None, research_state_dir: Path = None, admissible_candidate_path=None) -> dict:
    """127 G1: focused Track A seam + drift check (machine-readable, dep-light).

    Drift preflight runs first (fail-closed). When `admissible_candidate_path` is
    supplied, the named admissible seam is evaluated manifest-only (no network, no
    parquet/outcome reads, no real research_state writes) and its stable machine
    fields are exposed under `admissible_seam`: pass/status/reason_code/failures/
    month/fail_closed/network/reads_outcomes/reads_parquet. Missing/bad candidate
    => fail-closed NO-GO with stable reason codes. Never mutates canonical state.

    Returns {"script": "tracka_resume_check.check", "pass": bool, "drift_preflight",
    "admissible_seam", "network", "writes_real_research_state", "reads_outcomes",
    "reads_parquet", "elapsed_s"}.
    """
    t0 = time.time()
    root = Path(repo_root) if repo_root is not None else ROOT
    rs = Path(research_state_dir) if research_state_dir is not None else (root / "research_state")
    out = {
        "script": "tracka_resume_check.check",
        "network": False,
        "writes_real_research_state": False,
        "reads_outcomes": False,
        "reads_parquet": False,
        "elapsed_s": 0.0,
    }
    # Drift preflight first: fail-closed before any seam/manifest decision.
    try:
        pre = drift_preflight(root, research_state_dir=rs)
        out["drift_preflight"] = pre
        if pre.get("pass") is not True:
            out["pass"] = False
            out["status"] = "BLOCKED"
            out["reason_code"] = "DRIFT_PREFLIGHT_FAIL_BEFORE_SEAM"
            out["fail_closed_order"] = "drift_preflight->admissible_seam"
            out["elapsed_s"] = round(time.time() - t0, 6)
            return out
    except Exception as e:
        out["pass"] = False
        out["status"] = "BLOCKED"
        out["reason_code"] = "DRIFT_PREFLIGHT_EXCEPTION"
        out["failures"] = [f"drift_preflight_exception:{repr(e)}"]
        out["fail_closed_order"] = "drift_preflight->admissible_seam"
        out["elapsed_s"] = round(time.time() - t0, 6)
        return out
    out["drift_preflight_pass"] = True
    # Admissible seam check (manifest-only, fail-closed; optional candidate).
    try:
        asc = admissible_seam_check(candidate_path=admissible_candidate_path, repo_root=root)
        out["admissible_seam"] = {
            k: asc.get(k) for k in
            ("pass", "status", "reason_code", "failures", "month", "fail_closed",
             "network", "reads_outcomes", "reads_parquet", "candidate_path")
            if k in asc
        }
        out["network"] = asc.get("network", False)
        out["reads_outcomes"] = asc.get("reads_outcomes", False)
        out["reads_parquet"] = asc.get("reads_parquet", False)
        out["writes_real_research_state"] = asc.get("writes_real_research_state", False)
        seam_ok = asc.get("pass") is True
        if admissible_candidate_path is not None and not seam_ok:
            out["pass"] = False
            out["status"] = "NO-GO"
            out["reason_code"] = asc.get("reason_code", "ADMISSIBLE_SEAM_NOGO")
            out["fail_closed_order"] = "drift_preflight->admissible_seam"
            out["elapsed_s"] = round(time.time() - t0, 6)
            out.setdefault("canonical_outputs_mutated", False)
            out.setdefault("outcomes_inspected", False)
            return out
        out["pass"] = True
        out["status"] = "GO" if admissible_candidate_path is not None else "SEAM_WIRED_AWAITING_CANDIDATE"
        out["reason_code"] = asc.get("reason_code", "ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE")
        out["fail_closed_order"] = "drift_preflight->admissible_seam"
    except Exception as e:
        out["pass"] = False
        out["status"] = "BLOCKED"
        out["reason_code"] = "ADMISSIBLE_SEAM_EXCEPTION"
        out["failures"] = [f"seam_exception:{repr(e)}"]
        out["fail_closed_order"] = "drift_preflight->admissible_seam"
    out["elapsed_s"] = round(time.time() - t0, 6)
    return out


def _validate_probe_invariant_runtime_shape(obj) -> dict:
    """104: machine-validate monitor probe_invariant_runtime evidence-field shape."""
    if not isinstance(obj, dict):
        return {"pass": False, "reason": "not_dict", "shape_valid": False}
    required = ("pass", "total", "invariant")
    missing = [k for k in required if k not in obj]
    types_ok = isinstance(obj.get("pass"), bool) and isinstance(obj.get("total"), int) and isinstance(obj.get("invariant"), str)
    lists_ok = (("live_probes" not in obj) or isinstance(obj.get("live_probes"), list)) and (("digests" not in obj) or isinstance(obj.get("digests"), list))
    ok = (not missing) and types_ok and lists_ok
    return {"pass": ok, "shape_valid": ok, "missing": missing, "types_ok": types_ok, "lists_ok": lists_ok,
            "pass_value": obj.get("pass"), "total": obj.get("total")}


def probe_invariant_state(repo_root: Path = None, research_state_dir: Path = None) -> dict:
    """104: read-only probe invariant state + machine validation of probe_invariant_runtime field."""
    root = Path(repo_root) if repo_root is not None else ROOT
    rs = Path(research_state_dir) if research_state_dir is not None else (root / "research_state")
    out = {"read_only": True, "network": False}
    try:
        import scripts.monitor_ironflow_liquidations as mon
        out["assert_probe_invariant"] = mon.assert_probe_invariant(rs, raise_on_violation=False)
    except Exception as e:
        out["assert_probe_invariant"] = {"pass": False, "error": repr(e)}
    # validate runtime field in latest live probe if present
    try:
        live = sorted(p for p in rs.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_"))
        if live:
            latest = live[-1]
            out["latest_live_probe"] = latest.name
            d = json.loads(latest.read_text(encoding="utf-8", errors="ignore"))
            pir = d.get("probe_invariant_runtime")
            out["probe_invariant_runtime_present"] = pir is not None
            out["probe_invariant_runtime_validation"] = _validate_probe_invariant_runtime_shape(pir) if pir is not None else {"pass": False, "shape_valid": False, "reason": "missing"}
        else:
            out["latest_live_probe"] = None
            out["probe_invariant_runtime_present"] = False
            out["probe_invariant_runtime_validation"] = {"pass": False, "shape_valid": False, "reason": "no_live_probe"}
    except Exception as e:
        out["probe_invariant_runtime_validation"] = {"pass": False, "shape_valid": False, "error": repr(e)}
    out["pass"] = out.get("assert_probe_invariant", {}).get("pass") is True and out.get("probe_invariant_runtime_validation", {}).get("pass") is True
    return out


def compose_operator_report(repo_root: Path = None, research_state_dir: Path = None,
                            data_path: str = "/nonexistent_tracka_resume", prereg: str = None,
                            harness_repo_root: Path = None,
                            admissible_candidate_path=None) -> dict:
    """104 bounded top-level operator compose/report: drift preflight + gate decision + probe invariant state.

    Read-only, <5s target, no network regression, fail-closed. No real research_state writes.
    109: optional admissible_candidate_path enables manifest-only GO/NO-GO/pending seam exposure
    without changing stable 104/105 pass/fail_closed_order semantics.
    """
    t0 = time.time()
    root = Path(repo_root) if repo_root is not None else ROOT
    rs = Path(research_state_dir) if research_state_dir is not None else (root / "research_state")
    hrr = Path(harness_repo_root) if harness_repo_root is not None else root
    report = {"script": "tracka_operator_report", "network": False, "writes_real_research_state": False, "read_only": True}
    # 1) drift preflight (read-only, fail-closed)
    try:
        report["drift_preflight"] = drift_preflight(root, research_state_dir=rs)
    except Exception as e:
        report["drift_preflight"] = {"pass": False, "error": repr(e), "read_only": True, "network": False}
    # 2) gate decision (tmp output; prereg-before-outcomes enforced; drift already reflected)
    try:
        import scripts.tracka_resume_gate as trg
        with tempfile.TemporaryDirectory() as td:
            report["gate_decision"] = trg.decide(
                data_path=data_path, output_dir=td, pre_reg_path=prereg, source_manifest=None,
                compat_fixture=False, repo_root=root, research_state_dir=rs,
                harness_repo_root=hrr, skip_drift_preflight=True,
                admissible_manifest_path=admissible_candidate_path)
        # avoid duplicating full nested preflight object bloat in compose output
        if "drift_preflight" in report["gate_decision"]:
            report["gate_decision"]["drift_preflight_nested"] = "see report.drift_preflight"
            report["gate_decision"].pop("drift_preflight", None)
    except Exception as e:
        report["gate_decision"] = {"pass": False, "status": "BLOCKED", "error": repr(e), "outcomes_inspected": False}
    # 3) probe invariant state + probe_invariant_runtime validation
    report["probe_invariant_state"] = probe_invariant_state(root, research_state_dir=rs)
    report["probe_invariant_runtime_valid"] = report["probe_invariant_state"].get("probe_invariant_runtime_validation", {}).get("pass") is True
    # 105 named probe_invariant_runtime guard at operator level (fail-closed)
    pis = report["probe_invariant_state"]
    report["probe_invariant_runtime_named"] = {
        "pass": pis.get("pass") is True,
        "assert_probe_invariant_pass": pis.get("assert_probe_invariant", {}).get("pass"),
        "probe_invariant_runtime_present": pis.get("probe_invariant_runtime_present"),
        "probe_invariant_runtime_shape_valid": pis.get("probe_invariant_runtime_validation", {}).get("shape_valid"),
        "latest_live_probe": pis.get("latest_live_probe"),
    }
    # 108/109 named admissible-seam guard at operator level (manifest-only, fail-closed; no network/no outcomes)
    # Exposed as named surface; does not alter stable 104/105 pass/fail_closed_order semantics.
    asc = admissible_seam_check(candidate_path=admissible_candidate_path, repo_root=root)
    report["admissible_seam_state"] = asc
    wired = {
        "pass": asc.get("pass") is True,
        "status": asc.get("status"),
        "reason_code": asc.get("reason_code"),
        "fail_closed": asc.get("fail_closed"),
        "network": asc.get("network"),
        "reads_outcomes": asc.get("reads_outcomes"),
        "reads_parquet": asc.get("reads_parquet"),
    }
    if admissible_candidate_path is not None:
        wired["candidate_path"] = str(admissible_candidate_path)
        wired["month"] = asc.get("month")
        wired["failures"] = asc.get("failures", [])
    report["admissible_seam_wired"] = wired
    report["elapsed_s"] = round(time.time() - t0, 6)
    # fail-closed overall (stable 104/105 semantics preserved)
    drift_ok = report["drift_preflight"].get("pass") is True
    gate_blocked_expected = report["gate_decision"].get("status") == "BLOCKED" and report["gate_decision"].get("outcomes_inspected") is False
    probe_ok = report["probe_invariant_state"].get("pass") is True
    report["pass"] = drift_ok and gate_blocked_expected and probe_ok
    report["fail_closed_order"] = "drift_preflight->gate_decision->probe_invariant_state"
    if not report["pass"]:
        report.setdefault("reason_code", report.get("gate_decision", {}).get("reason_code", "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"))
        report.setdefault("outcomes_inspected", False)
    return report



def main(argv=None) -> int:
    """CLI entrypoint for tracka_resume_check.

    Without --admissible-manifest runs the full 17-check offline resume check
    (run()). With --admissible-manifest runs the focused seam+drift check (check()).
    Exit 0 => pass, Exit 1 => BLOCKED/NO-GO.
    """
    ap = argparse.ArgumentParser(description="Offline bounded Track A resume check (FCLR-NEXT-095 / 127 G1)")
    ap.add_argument("--admissible-manifest", required=False, default=None, dest="admissible_manifest",
                    help="127 G1: candidate Ironflow month manifest JSON for named admissible-seam fail-closed check (manifest-only, no network/no parquet/no outcomes)")
    # G3/134: argparse contract violations (unknown flags, malformed CLI args) must
    # refuse as parseable JSON, never as an uncaught usage/traceback exit. --help is
    # allowed to exit 0 normally; any other SystemExit is a fail-closed JSON refusal.
    try:
        args = ap.parse_args(argv)
    except SystemExit as se:
        code = getattr(se, "code", 2)
        if code == 0:
            return 0
        out = {
            "script": "tracka_resume_check",
            "gate_script": "tracka_resume_check",
            "pass": False,
            "status": "BLOCKED",
            "reason": "argparse contract violation (fail-closed, no outcomes): invalid CLI arguments",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "reason_code_detail": "ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED",
            "fail_closed_order": "drift_preflight->admissible_seam",
            "outcomes_inspected": False,
            "network": False,
            "writes_real_research_state": False,
            "canonical_outputs_mutated": False,
            "reads_outcomes": False,
            "reads_parquet": False,
            "elapsed_s": 0.0,
            "exit_code": int(code) if isinstance(code, int) else 2,
        }
        print(json.dumps(out, indent=2, sort_keys=True))
        return 1
    try:
        if args.admissible_manifest is not None:
            out = check(admissible_candidate_path=args.admissible_manifest)
        else:
            out = run()
    except Exception as e:  # G2/131: unexpected resume-check errors must refuse as JSON, never traceback-as-contract
        out = {
            "script": "tracka_resume_check",
            "pass": False,
            "status": "BLOCKED",
            "reason": f"resume check failed (fail-closed, no outcomes): {e!r}",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "fail_closed_order": "drift_preflight->admissible_seam",
            "outcomes_inspected": False,
            "network": False,
            "writes_real_research_state": False,
            "reads_outcomes": False,
            "reads_parquet": False,
            "elapsed_s": 0.0,
        }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
