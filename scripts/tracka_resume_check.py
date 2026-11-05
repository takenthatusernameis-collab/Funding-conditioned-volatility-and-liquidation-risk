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
    # root md+json bounded (099 invariant)
    root_count = len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))
    checks["root_md_json_bounded"] = {"pass": root_count <= 163, "count": root_count, "bound": 163}
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
    allow_probe = {"fclr012v_extension_probe.json", "hl_coverage_probe.json", "url_probe_cache.json"}
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


def run(repo_root: Path = None, research_state_dir: Path = None) -> dict:
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
                            harness_repo_root: Path = None) -> dict:
    """104 bounded top-level operator compose/report: drift preflight + gate decision + probe invariant state.

    Read-only, <5s target, no network regression, fail-closed. No real research_state writes.
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
                harness_repo_root=hrr, skip_drift_preflight=True)
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
    report["elapsed_s"] = round(time.time() - t0, 6)
    # fail-closed overall
    drift_ok = report["drift_preflight"].get("pass") is True
    gate_blocked_expected = report["gate_decision"].get("status") == "BLOCKED" and report["gate_decision"].get("outcomes_inspected") is False
    probe_ok = report["probe_invariant_state"].get("pass") is True
    report["pass"] = drift_ok and gate_blocked_expected and probe_ok
    report["fail_closed_order"] = "drift_preflight->gate_decision->probe_invariant_state"
    return report



if __name__ == "__main__":
    out = run()
    print(json.dumps(out, indent=2, sort_keys=True))
    sys.exit(0 if out["pass"] else 1)
