"""Tests for scripts/fclr023_gate4_blocker_resolution_action_plan.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr023_gate4_blocker_resolution_action_plan.py"
FORBIDDEN_TRUE = [
    '"satisfied": true',
    '"satisfaction_inferred": true',
    '"confirmatory_outcomes_go": true',
    '"packet_ready_for_human_or_prereg_action": true',
    '"group_ready_for_action": true',
    '"authorizes_confirmatory_outcomes": true',
]
FORBIDDEN_COMMAND_TOKENS = [
    "--expect-go",
    "curl",
    "wget",
    "http",
    "https",
    "network",
    "confirmatory",
    "outcome",
    "freeze",
    "promote",
    "seal",
]


def run_script(out_dir: Path, f22: Path, extra=()):
    cmd = [sys.executable, str(SCRIPT), "--fclr022", str(f22), "--out", str(out_dir), *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    doc_path = out_dir / "fclr023_gate4_blocker_resolution_action_plan_latest.json"
    doc = json.loads(doc_path.read_text()) if doc_path.exists() else None
    return p, doc, doc_path


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return path


def row(window, prerequisite, current_state="present_blocker", gate_class="provenance_manifest_evidence",
        evidence_ref=None, reason=None, missing_action_class=None, evidence_present=False,
        read_state="no_path_cited", sha256=None, bytes_=0, resolution_ready=False):
    return {
        "window": window,
        "prerequisite": prerequisite,
        "current_state": current_state,
        "gate_class": gate_class,
        "evidence_ref": evidence_ref,
        "reason": reason or f"{prerequisite} blocked",
        "missing_action_class": missing_action_class or gate_class,
        "evidence_present": evidence_present,
        "read_state": read_state,
        "sha256": sha256,
        "bytes": bytes_,
        "resolution_ready": resolution_ready,
    }


def f22_doc(rows):
    return {
        "script": "fclr022_gate4_blocker_resolution_evidence_preflight.py",
        "draft_only": True, "no_confirmatory_outcomes": True, "exploratory_only": True,
        "no_network": True, "not_go_for_confirmatory_outcomes": True,
        "confirmatory_ready_now": False, "confirmatory_outcomes_go": False,
        "authorizes_confirmatory_outcomes": False, "satisfied": False, "satisfaction_inferred": False,
        "resolution_readiness_rows": rows,
    }


class TestFclr023BlockerResolutionActionPlan(unittest.TestCase):
    def _assert_draft_metadata(self, doc):
        self.assertTrue(doc["draft_only"])
        self.assertTrue(doc["no_confirmatory_outcomes"])
        self.assertTrue(doc["exploratory_only"])
        self.assertTrue(doc["no_network"])
        self.assertTrue(doc["not_go_for_confirmatory_outcomes"])
        self.assertFalse(doc["confirmatory_ready_now"])
        self.assertFalse(doc["confirmatory_outcomes_go"])
        self.assertFalse(doc["authorizes_confirmatory_outcomes"])
        self.assertFalse(doc["satisfied"])
        self.assertFalse(doc["satisfaction_inferred"])
        self.assertFalse(doc["packet_ready_for_human_or_prereg_action"])
        blob = json.dumps(doc)
        for f in FORBIDDEN_TRUE:
            self.assertNotIn(f, blob)

    def _assert_packet_fields(self, packet):
        self.assertEqual(packet["packet_ready_for_human_or_prereg_action"], False)
        snap = packet["evidence_snapshot"]
        for k in ["window", "prerequisite", "current_state", "gate_class", "evidence_ref",
                  "evidence_present", "read_state", "sha256", "bytes", "reason_copied_from_index",
                  "missing_action_class", "resolution_ready"]:
            self.assertIn(k, snap)
        self.assertIsInstance(packet["local_verification_commands"], list)
        self.assertGreaterEqual(len(packet["local_verification_commands"]), 1)
        self.assertIsInstance(packet["artifact_target_hint"], str)
        self.assertGreater(len(packet["artifact_target_hint"]), 0)
        for cmd in packet["local_verification_commands"]:
            low = cmd.lower()
            for tok in FORBIDDEN_COMMAND_TOKENS:
                self.assertNotIn(tok, low, f"forbidden token {tok!r} in command {cmd!r}")
        if not snap["evidence_present"]:
            self.assertIsNone(snap["sha256"])

    def test_grouping_and_field_completeness(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            rows = [
                row("w1", "identity_provenance_range", gate_class="provenance_manifest_evidence"),
                row("w1", "manifest_terms_evidence", gate_class="terms_legal_evidence_resolution"),
                row("w2", "identity_provenance_range", gate_class="provenance_manifest_evidence"),
                row("w1", "manifest_terms_evidence", gate_class="terms_legal_evidence_resolution",
                    current_state="present_blocker"),  # same group as row 2
            ]
            f22 = write_json(root / "f22.json", f22_doc(rows))
            p, doc, latest = run_script(out_dir, f22)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self.assertTrue(latest.exists())
            self._assert_draft_metadata(doc)
            groups = doc["action_plan_packets"]
            self.assertEqual(doc["group_count"], 3)
            self.assertEqual(doc["row_count"], 4)
            self.assertEqual(len(groups), 3)
            by_key = {(g["window"], g["gate_class"], g["prerequisite"]): g for g in groups}
            self.assertEqual(len(by_key[("w1", "terms_legal_evidence_resolution", "manifest_terms_evidence")]["packets"]), 2)
            for g in groups:
                self.assertTrue(g["group_all_packet_ready_false"])
                for pkt in g["packets"]:
                    self._assert_packet_fields(pkt)
            warnings = doc["action_plan_warnings"]
            self.assertEqual(len(warnings), 4)
            for w in warnings:
                self.assertEqual(w["type"], "action_plan_warning")

    def test_human_legal_required_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            rows = [
                row("w1", "manifest_terms_evidence.terms_evidence", gate_class="terms_legal_evidence_resolution"),
                row("w1", "identity_provenance_range", gate_class="provenance_manifest_evidence"),
                row("w1", "fresh_frozen_prereg_before_outcomes_required", gate_class="fresh_frozen_prereg_before_outcomes"),
                row("w1", "admissibility_package_status.completeness_leakage_audit",
                    gate_class="admissibility_completeness_leakage_evidence"),
                row("w1", "leakage_sufficiency_gates", gate_class="leakage_sufficiency_gates"),
            ]
            f22 = write_json(root / "f22.json", f22_doc(rows))
            p, doc, _ = run_script(out_dir, f22)
            self.assertEqual(p.returncode, 0, p.stderr)
            by_prereq = {}
            for g in doc["action_plan_packets"]:
                for pkt in g["packets"]:
                    by_prereq[pkt["prerequisite"]] = pkt
            self.assertTrue(by_prereq["manifest_terms_evidence.terms_evidence"]["human_legal_required"])
            self.assertFalse(by_prereq["identity_provenance_range"]["human_legal_required"])
            self.assertTrue(by_prereq["fresh_frozen_prereg_before_outcomes_required"]["fresh_frozen_prereg_required"])
            self.assertFalse(by_prereq["identity_provenance_range"]["fresh_frozen_prereg_required"])
            self.assertFalse(by_prereq["admissibility_package_status.completeness_leakage_audit"]["human_legal_required"])
            self.assertFalse(by_prereq["leakage_sufficiency_gates"]["fresh_frozen_prereg_required"])

    def test_evidence_present_still_draft_and_not_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            present = root / "evidence.json"
            present.write_text('{"ok": true}', encoding="utf-8")
            rows = [
                row("w1", "manifest_terms_evidence.terms_evidence", gate_class="terms_legal_evidence_resolution",
                    evidence_ref=str(present), evidence_present=True, read_state="ok",
                    sha256="deadbeef", bytes_=13, resolution_ready=False),
            ]
            f22 = write_json(root / "f22.json", f22_doc(rows))
            p, doc, _ = run_script(out_dir, f22)
            self.assertEqual(p.returncode, 0, p.stderr)
            pkt = doc["action_plan_packets"][0]["packets"][0]
            self.assertTrue(pkt["evidence_snapshot"]["evidence_present"])
            self.assertFalse(pkt["packet_ready_for_human_or_prereg_action"])
            self.assertTrue(pkt["human_legal_required"])
            self.assertFalse(doc["confirmatory_outcomes_go"])
            self.assertFalse(doc["satisfied"])

    def test_missing_unreadable_input_handling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            p, doc, _ = run_script(out_dir, root / "nope.json")
            self.assertEqual(p.returncode, 0, p.stderr)
            self._assert_draft_metadata(doc)
            self.assertNotEqual(doc["input_state"], "ok")
            self.assertTrue(any(w["type"] == "input_unavailable" for w in doc["action_plan_warnings"]))
            self.assertEqual(doc["group_count"], 0)
            self.assertEqual(doc["row_count"], 0)

    def test_no_fabrication_packet_ready_always_false_and_no_created_artifact_hint(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); out_dir = root / "out"
            present = root / "evidence.json"
            present.write_text('{"ok": true}', encoding="utf-8")
            f22 = write_json(root / "f22.json", f22_doc([row("w1", "p1", evidence_ref=str(present),
                evidence_present=True, read_state="ok", sha256="x", bytes_=1)]))
            p, doc, _ = run_script(out_dir, f22)
            self.assertEqual(p.returncode, 0, p.stderr)
            pkt = doc["action_plan_packets"][0]["packets"][0]
            self.assertTrue(pkt["evidence_snapshot"]["evidence_present"])
            self.assertFalse(pkt["packet_ready_for_human_or_prereg_action"])
            self.assertIn("not created or marked present", pkt["artifact_target_hint"])
            self.assertFalse(doc["authorizes_confirmatory_outcomes"])

    def test_draft_only_metadata_and_no_sealed_overwrite(self):
        real = REPO / "research_state" / "fclr022_local_audit" / "fclr022_gate4_blocker_resolution_evidence_preflight_latest.json"
        if not real.exists():
            self.skipTest("real fclr022 latest not present")
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "out"
            p, doc, _ = run_script(out_dir, real)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self._assert_draft_metadata(doc)
            self.assertGreater(doc["group_count"], 0)
            self.assertGreater(doc["row_count"], 0)
            for g in doc["action_plan_packets"]:
                self.assertFalse(g["group_ready_for_action"])
                self.assertTrue(g["group_all_packet_ready_false"])
                for pkt in g["packets"]:
                    self._assert_packet_fields(pkt)
                    self.assertFalse(pkt["packet_ready_for_human_or_prereg_action"])
            self.assertTrue((out_dir / "fclr023_gate4_blocker_resolution_action_plan_latest.json").exists())


if __name__ == "__main__":
    unittest.main()
