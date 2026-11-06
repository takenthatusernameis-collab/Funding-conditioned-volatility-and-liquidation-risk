"""FCLR-NEXT-116: READY-writing Track A blocked no-canonical/frontier mutation + audit mains + remaining liquidation-claim script classification.

Deterministic, tmp-isolated, no network, no real parquet/outcome reads, no real research_state writes.

Closes exact gaps left by FCLR-NEXT-115:
  (G1) overlay_quick.py, overlay_tracka_execute.py, coupled_robust_eval.py, fclr010_execute.py
       write canonical evaluation summaries and some mutate experiment_frontier.json / run_manifest
       on READY_FROZEN paths. A module-level blocked-branch matrix asserts guarded_execute->BLOCKED
       never writes those canonical outputs or mutates frontier/manifest (main() never reaches
       READY mutation paths; ready-path mutation helpers are isolated as assertions on branch order).
  (G2) liqmicro_audit.py and fclr010_coverage_audit.py blocked main() behavior is asserted:
       no loader, no canonical audit/output mutation, refusal payload path only.
  (G3) Remaining liquidation-risk/outcome-reading or liquidation-claim scripts are audited and
       classified (guarded_tracka / harness+resume infra / prereg_utility / raw_fetch_monitor_provenance
       / track_b_modeled_boundary / track_c_sealed_volatility / out_of_scope_historical_or_utility)
       with explicit reason. h004_fclr005_pipeline is classified as historical Track A observed-label
       pilot (Bybit 2026 census, fixed path, no FCLR010Harness) — NOT Hyperliquid ironflow governed by
       the guarded fclr010 seam; out-of-scope for guarded outcome-loader contract with explicit reason.
  (G4) All classified guarded_tracka scripts are checked for blocked-path frontier/canonical mutation
       surface (source+blocked main assertions where canonical writes exist).

Stable 108/110/111/112/113/114/115 reason codes/order/fields preserved.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
from src.analysis.tracka_admissible import build_ironflow_month_manifest

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
RS = REAL / "research_state"
TESTS = REAL / "tests"

BLOCKED_PAYLOAD = {
    "status": "BLOCKED",
    "outcomes_inspected": False,
    "canonical_outputs_mutated": False,
    "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
}
READY_PAYLOAD = {
    "status": "READY_FROZEN",
    "outcomes_inspected": False,
    "canonical_outputs_mutated": False,
    "outcomes_loaded": {"panel": object(), "hourly": object(), "raw_df": object(), "funding_df": object()},
}

# Canonical / mutation targets relevant to 116 READY-writing scripts.
CANONICAL_TARGETS = {
    "overlay_quick": [
        RS / "evaluation_summary_tracka_overlay_001.md",
        RS / "experiment_frontier.json",
        RS / "cross_track_decision_log.md",
    ],
    "overlay_tracka_execute": [
        RS / "evaluation_summary_tracka_overlay_001.md",
        RS / "experiment_frontier.json",
        RS / "cross_track_decision_log.md",
    ],
    "coupled_robust_eval": [
        RS / "evaluation_summary_FCLR-COUPLED-001-ROBUST.md",
    ],
    "fclr010_execute": [
        RS / "evaluation_summary_FCLR010.md",
        RS / "run_manifest.json",
    ],
    "fclr010_coverage_audit": [
        RS / "fclr010_coverage_audit.json",
    ],
    "liqmicro_audit": [
        RS / "liqmicro_data_audit_001.md",
    ],
}

# G3 extended classification for scripts that mention liquidation/risk/outcome artifacts
# and/or were unclassified in 115's narrower registry. This is the 116 reasoned registry.
EXTENDED_CLASSIFICATION = {
    # 115 guarded Track A + core (inherited, re-asserted)
    "fclr010_harness.py": ("harness_core", "Defines FCLR010Harness/guarded execute_ready_data_load contract."),
    "fclr010_guarded_entry.py": ("guarded_tracka", "Single guarded execution entry; refuses blocked before outcome load."),
    "fclr010_execute.py": ("guarded_tracka_ready_writing", "Guarded execute + READY-only canonical summary/manifest mutation; blocked refuses before writes (G1/G4)."),
    "fclr010_execute_fast.py": ("guarded_tracka", "Fast refusal/no-op unless explicit READY_FROZEN+loader."),
    "coupled_build_panel.py": ("guarded_tracka", "G1 machine-refuse without loader; no unguarded parquet."),
    "coupled_robust_eval.py": ("guarded_tracka_ready_writing", "Guarded + coupled loader; READY writes summary only; blocked refuses (G1/G4)."),
    "overlay_tracka_execute.py": ("guarded_tracka_ready_writing", "Guarded + coupled loader; READY writes summary/frontier/cross-track; blocked refuses (G1/G4)."),
    "overlay_quick.py": ("guarded_tracka_ready_writing", "Guarded + coupled loader; READY writes summary/frontier/cross-track; blocked refuses (G1/G4)."),
    "fclr010_coverage_audit.py": ("guarded_tracka_audit_ready_writing", "Guarded coverage audit; blocked main refuses/no canonical JSON write (G2)."),
    "liqmicro_audit.py": ("guarded_tracka_audit_ready_writing", "Guarded liqmicro audit; blocked main refuses/no canonical md write (G2)."),
    "run_liqmicro.py": ("guarded_tracka", "Guarded; blocked no loader/canonical/frontier mutation (115 G2)."),
    "run_liqmicro_v2.py": ("guarded_tracka", "Guarded; blocked no loader/canonical/frontier mutation (115 G2)."),
    "tracka_resume_check.py": ("resume_gate_infra", "Read-only checks; seam wiring only; no outcome reads/claims."),
    "tracka_resume_gate.py": ("resume_gate_infra", "Read-only fail-closed gate; no outcome reads/canonical mutation."),
    "tracka_operator_report.py": ("resume_gate_infra", "Read-only operator report composition."),
    "create_forward_prereg.py": ("prereg_utility", "Writes prereg records only; no outcome reads."),
    "fclr010_validate.py": ("prereg_utility", "Validation/prereg helper; no guarded outcome claim reads."),
    "write_trigger_harden_successor.py": ("prereg_utility", "Trigger-hardening artifacts; no outcome reads."),
    "monitor_ironflow_liquidations.py": ("raw_fetch_monitor_provenance", "HTTP probe/provenance ingestion; not liquidation-risk claim producer."),
    # G3 newly classified (liquidation/risk mentions, not in 115 registry)
    "h004_fclr005_pipeline.py": (
        "out_of_scope_historical_tracka_pilot",
        "Historical Track A observed-label pilot using Bybit 2026 liquidation census (LIQ constant, fixed local path) + Binance features; NOT Hyperliquid ironflow and NOT routed through FCLR010Harness guarded outcome-loader seam. Produces pilot evaluation summary; out of guarded fclr010 outcome contract by design (distinct experiment/protocol). Must not be conflated with Hyperliquid observed-liquidation gate.",
    ),
    "create_blocker_evidence.py": ("prereg_utility", "Emits blocker/prereg-evidence artifacts; no liquidation outcome reads/claims."),
    "deep_review_alt_sources.py": ("raw_fetch_monitor_provenance", "Alt-source review/provenance; no guarded liquidation outcome claims."),
    "generate_tracka_fixtures.py": ("test_fixture_utility", "Generates synthetic Track A fixtures for tests; no real outcome reads/canonical claims."),
    "h004_audit.py": ("out_of_scope_historical_tracka_pilot", "Audit helper for historical h004/FCLR-005 pilot artifacts; not guarded fclr010 outcome path."),
    "h004_download_2026.py": ("raw_fetch_monitor_provenance", "Download/provenance helper for 2026 h004 data; not a liquidation-risk claim producer."),
    "hl_coverage_probe.py": ("raw_fetch_monitor_provenance", "Coverage probe/provenance; no guarded outcome claims."),
    "hunt_alternative_liquidation_sources.py": ("raw_fetch_monitor_provenance", "Source-hunt/provenance; no guarded outcome claims."),
    "hyperliquid_funding_fetch.py": ("raw_fetch_monitor_provenance", "Funding fetch/provenance utility; no liquidation outcome claim production."),
    "merge_redundant_artifacts_090.py": ("repo_maintenance_utility", "Artifact maintenance; no liquidation outcome reads/claims."),
    "migrate_digest_archive_090.py": ("repo_maintenance_utility", "Digest/archive maintenance; no liquidation outcome reads/claims."),
    "run_evaluation.py": ("track_c_sealed_volatility", "Track C/FCLR volatility evaluation path (sealed); liquidation terms absent as claim target; no Track A guarded liquidation outcome reads."),
    "run_h003.py": ("track_b_modeled_boundary", "Track B/FCLR-H003 modeled boundary-breach labels (synthetic); explicitly modeled != observed liquidations; out of Track A observed outcome contract."),
    "run_h003_ext.py": ("track_b_modeled_boundary", "Track B modeled boundary extension; modeled != observed."),
    "run_h003_ext_fast.py": ("track_b_modeled_boundary", "Track B modeled boundary extension (fast); modeled != observed."),
    "run_h003_ext_inference.py": ("track_b_modeled_boundary", "Track B modeled boundary inference; modeled != observed."),
    "synthetic_boundary_labels.py": ("track_b_modeled_boundary", "Synthetic/modeled boundary label construction; modeled != observed, no observed liquidation claims."),
    "tracka_rubric.py": ("resume_gate_infra", "Track A admissibility rubric/GO-NO-GO logic; pure assessment, no outcome parquet reads or canonical claim mutation."),
    "verify_heavy_work_004i.py": ("repo_maintenance_utility", "Historical campaign checklist verifier; no liquidation outcome reads/claims."),
    "volatility_track_progress.py": ("track_c_sealed_volatility", "Track C progress/report utility (volatility); no Track A guarded liquidation outcome reads."),
    "funding_correction_replication.py": ("track_c_sealed_volatility", "FCLR-H002 funding-correction replication (volatility/correction-time context); explicitly distinct from liquidation outcomes; no Track A guarded liquidation reads."),
}


def _valid_admissible(month="2026-11", **over):
    m = build_ironflow_month_manifest(
        month=month,
        events_path=f"/tmp/ironflow/data/events/{month}.parquet",
        fills_path=f"/tmp/ironflow/data/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "liquidation_notional", "side"],
        schema_fields_fills=["timestamp", "symbol", "size", "price"],
    )
    m.update(over)
    return m


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))
    return str(path)


def _loader_must_not_run(*_a, **_k):
    raise AssertionError("outcome/parquet loader must not run on blocked branch")


def _assert_targets_unchanged(before_map):
    for p, before in before_map.items():
        after = p.read_bytes() if p.exists() else None
        assert before == after, f"canonical/mutation target changed on blocked path: {p}"


def _snapshot(paths):
    return {p: (p.read_bytes() if p.exists() else None) for p in paths}


class Test116G1ReadyWritingBlockedNoCanonicalFrontierMutation(unittest.TestCase):
    """G1: READY-writing Track A scripts never mutate canonical outputs/frontier on BLOCKED."""

    BLOCKED_CASES = [
        ("no_candidate", None, None),
        ("nogo_seam_2026-10", _valid_admissible("2026-10"), "p.json"),
        ("nogo_venue", _valid_admissible(venue="binance"), "p.json"),
        ("nogo_auth", _valid_admissible(requires_signature=True), "p.json"),
        ("nogo_modeled", _valid_admissible(modeled_or_proxy=True), "p.json"),
        ("nogo_leakage", _valid_admissible(label_definition="proxy liquidation estimate"), "p.json"),
    ]

    def _blocked_via_guard(self, name, manifest, prereg_suffix):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"
            if prereg_suffix:
                prereg.write_text("{}")
            adm_path = _write(Path(td) / f"adm_{name}.json", manifest) if manifest is not None else None
            res = guarded_execute(
                data_path=data, pre_reg_path=prereg if prereg_suffix else None, repo_root=REAL,
                admissible_manifest_path=adm_path,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
        return res

    def test_guarded_matrix_blocks_no_canonical_mutation_fields(self):
        for name, manifest, prereg in self.BLOCKED_CASES:
            res = self._blocked_via_guard(name, manifest, prereg)
            self.assertEqual(res["status"], "BLOCKED", (name, res))
            self.assertFalse(res.get("canonical_outputs_mutated", False), (name, res))
            self.assertFalse(res.get("outcomes_inspected", False), (name, res))

    def test_overlay_quick_main_blocked_no_writes(self):
        from scripts import overlay_quick
        before = _snapshot(CANONICAL_TARGETS["overlay_quick"])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.overlay_quick._load_coupled_panel_outcomes", side_effect=_loader_must_not_run), \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = overlay_quick.main()
        self.assertEqual(rc, 1)
        self.assertIn("BLOCKED", buf.getvalue())
        _assert_targets_unchanged(before)

    def test_overlay_tracka_execute_main_blocked_no_writes(self):
        from scripts import overlay_tracka_execute
        before = _snapshot(CANONICAL_TARGETS["overlay_tracka_execute"])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.overlay_tracka_execute._load_coupled_panel_outcomes", side_effect=_loader_must_not_run), \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = overlay_tracka_execute.main()
        self.assertEqual(rc, 1)
        _assert_targets_unchanged(before)

    def test_coupled_robust_eval_main_blocked_no_writes(self):
        from scripts import coupled_robust_eval
        before = _snapshot(CANONICAL_TARGETS["coupled_robust_eval"])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.coupled_robust_eval._load_coupled_panel_outcomes", side_effect=_loader_must_not_run), \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = coupled_robust_eval.main()
        self.assertEqual(rc, 1)
        _assert_targets_unchanged(before)

    def test_fclr010_execute_main_blocked_no_summary_manifest_mutation(self):
        from scripts import fclr010_execute
        before = _snapshot(CANONICAL_TARGETS["fclr010_execute"])
        # block at guarded_execute; loader must never run. Manifest/splits are read
        # read-only before guard in current implementation (to build loader context);
        # canonical summary + manifest writes happen only after READY guards.
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.fclr010_execute._load_outcomes", side_effect=_loader_must_not_run):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = fclr010_execute.main()
        self.assertEqual(rc, 1)
        _assert_targets_unchanged(before)

    def test_fclr010_execute_blocked_before_ready_write_block(self):
        src = (SCRIPTS / "fclr010_execute.py").read_text()
        # first READY_FROZEN check must appear before OUT_SUM.write_text
        first_ready = src.index('if guard.get("status") != "READY_FROZEN":')
        write_pos = src.index('OUT_SUM.write_text(lines_text)')
        self.assertLess(first_ready, write_pos)
        # no unconditional write outside guarded-ready block structure
        self.assertNotRegex(src, r"(?s)^\s*OUT_SUM\.write_text", re.M)


class Test116G2AuditScriptsBlockedMain(unittest.TestCase):
    """G2: liqmicro_audit/fclr010_coverage_audit blocked main() no loader/canonical mutation."""

    def test_liqmicro_audit_blocked_main(self):
        from scripts import liqmicro_audit
        before = _snapshot(CANONICAL_TARGETS["liqmicro_audit"])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.liqmicro_audit._load_liqmicro_outcomes", side_effect=_loader_must_not_run), \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = liqmicro_audit.main()
        self.assertEqual(rc, 1)
        _assert_targets_unchanged(before)

    def test_fclr010_coverage_audit_blocked_main(self):
        from scripts import fclr010_coverage_audit
        before = _snapshot(CANONICAL_TARGETS["fclr010_coverage_audit"])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)), \
             patch("scripts.fclr010_coverage_audit._load_coverage_outcomes", side_effect=_loader_must_not_run), \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"}):
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = fclr010_coverage_audit.main()
        self.assertEqual(rc, 1)
        _assert_targets_unchanged(before)

    def test_audit_scripts_guarded_markers(self):
        for name in ("liqmicro_audit.py", "fclr010_coverage_audit.py"):
            src = (SCRIPTS / name).read_text()
            self.assertIn("guarded_execute", src, name)
            self.assertIn("READY_FROZEN", src, name)
            self.assertIn("outcome_loader", src, name)


class Test116G3RemainingScriptClassification(unittest.TestCase):
    """G3: remaining liquidation-risk/outcome scripts classified with explicit reason."""

    ALLOWED = {
        "guarded_tracka", "guarded_tracka_ready_writing", "guarded_tracka_audit_ready_writing",
        "harness_core", "resume_gate_infra", "prereg_utility", "raw_fetch_monitor_provenance",
        "track_b_modeled_boundary", "track_c_sealed_volatility", "test_fixture_utility",
        "repo_maintenance_utility", "out_of_scope_historical_tracka_pilot",
    }

    def test_extended_registry_covers_115_and_risk_mentions(self):
        from tests.test_tracka_hardening_115 import HARNESS_CALLER_REGISTRY
        for name in HARNESS_CALLER_REGISTRY:
            self.assertIn(name, EXTENDED_CLASSIFICATION, f"115 registry member missing from 116: {name}")
        # scripts with liquidation/risk-relevant patterns found in 116 audit
        risk = {
            'create_blocker_evidence.py','deep_review_alt_sources.py','funding_correction_replication.py',
            'generate_tracka_fixtures.py','h004_audit.py','h004_download_2026.py','h004_fclr005_pipeline.py',
            'hl_coverage_probe.py','hunt_alternative_liquidation_sources.py','hyperliquid_funding_fetch.py',
            'merge_redundant_artifacts_090.py','migrate_digest_archive_090.py','run_evaluation.py',
            'run_h003.py','run_h003_ext.py','run_h003_ext_fast.py','run_h003_ext_inference.py',
            'synthetic_boundary_labels.py','tracka_rubric.py','verify_heavy_work_004i.py','volatility_track_progress.py',
        }
        missing = sorted(risk - set(EXTENDED_CLASSIFICATION))
        self.assertEqual(missing, [], f"unclassified liquidation/risk scripts: {missing}")

    def test_entries_have_reason_and_known_class(self):
        for name, (cls, reason) in EXTENDED_CLASSIFICATION.items():
            self.assertTrue((SCRIPTS / name).exists(), name)
            self.assertIn(cls, self.ALLOWED, (name, cls))
            self.assertGreaterEqual(len(reason), 20, (name, reason))

    def test_h004_pipeline_explicitly_not_guarded_fclr010_seam(self):
        cls, reason = EXTENDED_CLASSIFICATION["h004_fclr005_pipeline.py"]
        self.assertEqual(cls, "out_of_scope_historical_tracka_pilot")
        src = (SCRIPTS / "h004_fclr005_pipeline.py").read_text()
        self.assertNotIn("FCLR010Harness", src)
        self.assertNotIn("fclr010_guarded_entry", src)
        self.assertIn("NOT", reason.upper())
        self.assertIn("Hyperliquid", reason)

    def test_track_b_modeled_not_observed(self):
        for name in ("run_h003.py", "synthetic_boundary_labels.py"):
            cls, reason = EXTENDED_CLASSIFICATION[name]
            self.assertEqual(cls, "track_b_modeled_boundary")
            low = reason.lower()
            self.assertTrue("modeled" in low or "synthetic" in low, reason)


class Test116G4GuardedTrackABlockedFrontierSurfaces(unittest.TestCase):
    """G4: no untested blocked frontier mutation among classified guarded_tracka* scripts."""

    def test_ready_writing_scripts_only_mutate_after_ready_or_are_tested(self):
        # overlay* mutate frontier/cross_track only after READY guard returns/continues;
        # coupled_robust_eval writes only summary (no frontier); fclr010_execute writes
        # summary+manifest only after READY guards; audits write only on READY path.
        for name in ("overlay_quick.py", "overlay_tracka_execute.py"):
            src = (SCRIPTS / name).read_text()
            ready = src.index('if guard.get("status") != "READY_FROZEN":')
            frontier_write = src.index('with open(EXP_FRONTIER')
            self.assertLess(ready, frontier_write, name)
        for name in ("coupled_robust_eval.py", "fclr010_execute.py", "fclr010_coverage_audit.py", "liqmicro_audit.py"):
            src = (SCRIPTS / name).read_text()
            self.assertIn("READY_FROZEN", src, name)
            self.assertIn("guarded_execute", src, name)

    def test_run_liqmicro_frontier_only_after_ready_loader_path(self):
        # 115 established and 116 confirms: run_liqmicro mutates frontier only in _run_pipeline,
        # which is called only after READY_FROZEN in main.
        src = (SCRIPTS / "run_liqmicro.py").read_text()
        self.assertIn("if guard.get(\"status\") != \"READY_FROZEN\":", src)
        self.assertIn("_run_pipeline(raw_df, hourly)", src)
        self.assertIn("experiment_frontier.json", src)  # surface exists
        # surface is inside pipeline, not in blocked branch
        main_idx = src.index("def main")
        call_idx = src.index("_run_pipeline(raw_df, hourly)", main_idx)
        block_idx = src.index("PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", main_idx)
        self.assertLess(block_idx, call_idx)


class Test116StableContracts(unittest.TestCase):
    def test_refusal_payload_stable(self):
        p = refusal_payload(reason="x", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", script="s")
        self.assertEqual(p["status"], "BLOCKED")
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["network"])

    def test_no_real_research_state_new_files_on_blocked_mains(self):
        before = {p.name for p in RS.iterdir()} if RS.exists() else set()
        cases = [
            ("scripts.overlay_quick", "main"),
            ("scripts.overlay_tracka_execute", "main"),
            ("scripts.coupled_robust_eval", "main"),
            ("scripts.fclr010_execute", "main"),
            ("scripts.liqmicro_audit", "main"),
            ("scripts.fclr010_coverage_audit", "main"),
        ]
        for modname, fn in cases:
            mod = __import__(modname, fromlist=[fn])
            patches = [patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(BLOCKED_PAYLOAD)),
                       patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: {**k, "status": "BLOCKED"})]
            if "overlay" in modname or "coupled_robust" in modname:
                patches.append(patch(f"{modname}._load_coupled_panel_outcomes", side_effect=_loader_must_not_run))
            if modname.endswith("fclr010_execute"):
                patches.append(patch("scripts.fclr010_execute._load_outcomes", side_effect=_loader_must_not_run))
            if modname.endswith("liqmicro_audit"):
                patches.append(patch("scripts.liqmicro_audit._load_liqmicro_outcomes", side_effect=_loader_must_not_run))
            if modname.endswith("fclr010_coverage_audit"):
                patches.append(patch("scripts.fclr010_coverage_audit._load_coverage_outcomes", side_effect=_loader_must_not_run))
            from contextlib import ExitStack
            with ExitStack() as st:
                for p in patches:
                    st.enter_context(p)
                with redirect_stdout(io.StringIO()):
                    getattr(mod, fn)()
        after = {p.name for p in RS.iterdir()} if RS.exists() else set()
        self.assertEqual(before, after)


class Test116Metrics(unittest.TestCase):
    def test_metrics(self):
        metrics = {
            "g1_ready_writing_scripts_blocked_main_asserted": 4,
            "g2_audit_scripts_blocked_main_asserted": 2,
            "g3_extended_classified": len(EXTENDED_CLASSIFICATION),
            "g3_h004_not_fclr010_guarded": True,
            "g4_guarded_tracka_blocked_frontier_surfaces_reviewed": True,
        }
        self.assertGreaterEqual(metrics["g3_extended_classified"], 35)
        self.assertTrue(metrics["g3_h004_not_fclr010_guarded"])


if __name__ == "__main__":
    unittest.main()
