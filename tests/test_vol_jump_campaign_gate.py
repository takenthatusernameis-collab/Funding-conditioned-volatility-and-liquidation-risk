#!/usr/bin/env python3
"""FCLR-VOL-JUMP-01 handoff heavy-work gate regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes. Pins the binder for the ACTIVE rank-0 campaign: once
FCLR-VOL-JUMP-01 (the broad-panel funding-conditioned signed-jump /
semivariance-asymmetry forecast, RESEARCH_PROMPT.md section 3.1 / section 7
target 1) starts, a post-start session cannot dodge the heavy jump study with a
trigger-only, prose-only, audit-only, prereg-only, verify-and-stop,
source-probe-only, or arbitrary recompute_* session. It must emit the on-disk
source registry, the outcome-blind prereg, the HEAVY jump-forecast evaluation
triad (fclr_voljump01_eval_ py+json+md), the independent stdlib recompute
(fclr_voljump01_recompute_ py+json), the gate-critical evidence_audit_ alias,
and a trigger check, with no zero-byte placeholders. Sessions predating the
campaign are grandfathered so the refresh that announces it stays green.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REAL / "scripts"))

import check_handoff_heavywork_gate as gate  # noqa: E402


class TestVolJumpCampaignGate(unittest.TestCase):
    START = "20261124T223000Z"

    def _repo(self, latest_sid="session_20261124T230000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclrvoljump_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-VOL-JUMP-01-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _write_family(self, sdir, sid, skip=(), content=None):
        payloads = {}
        for prefix, suffix in gate.VOL_JUMP_REQUIRED:
            if any(prefix == s for s in skip):
                continue
            path = sdir / f"{prefix}{sid}{suffix}"
            if content is not None:
                path.write_text(content)
                continue
            if suffix != ".json":
                path.write_text("x")
                continue
            common = {
                "experiment_id": "FCLR-VOL-JUMP-01",
                "session_id": f"session_{sid}",
            }
            if prefix == "fclr_voljump01_source_registry_":
                payload = {
                    **common,
                    "datasets": {
                        "candles_1h": {"files": 18},
                        "funding": {"files": 18},
                        "open_interest": {"files": 18},
                    },
                    "input_integrity": {
                        "sha256_all_match": True,
                        "sha256_verified_bad": 0,
                    },
                    "files": [
                        {
                            "path": f"research_state/data_cache/ironflow_bulk/{i % 3}/part-{i}.parquet",
                            "sha256": hashlib.sha256(
                                f"voljump-file-{i}".encode()
                            ).hexdigest(),
                            "sha_match": True,
                        }
                        for i in range(54)
                    ],
                }
            elif prefix == "fclr_voljump01_prereg_":
                registry = payloads["fclr_voljump01_source_registry_"]
                payload = {
                    **common,
                    "frozen_before_outcomes": True,
                    "outcome_data_inspected_before_freeze": False,
                    "design": {
                        "kind": "walk_forward_classification_jump_asymmetry",
                        "target": "next-24h signed-jump / semivariance-asymmetry tail exceedance (train-only high quantile)",
                    },
                    "materiality_floor_rel": 0.02,
                    "source_registry_sha256": hashlib.sha256(
                        registry["path"].read_bytes()
                    ).hexdigest(),
                }
            elif prefix == "fclr_voljump01_eval_":
                payload = {
                    **common,
                    "status": "NOT_SUPPORTED",
                    "holdout_opened": True,
                    "n_events": 5000,
                    "metrics": {
                        "baseline": {"brier": 0.20},
                        "candidate": {"brier": 0.20},
                    },
                    "materiality_met": False,
                    "verdict": "NOT_SUPPORTED",
                }
            elif prefix == "fclr_voljump01_recompute_":
                payload = {**common, "all_checks_match": True, "n_checks": 12}
            elif prefix == "fclr_voljump01_evidence_audit_":
                payload = {
                    **common,
                    "audit_pass": True,
                    "unresolved_blockers": [],
                    "verdict": "NOT_SUPPORTED",
                }
            elif prefix == "evidence_audit_":
                payload = {
                    **common,
                    "audit_pass": True,
                    "verdict": "NOT_SUPPORTED",
                }
            elif prefix == "trigger_check_":
                payload = {
                    **common,
                    "external_trigger_required": False,
                    "trigger_source": "FROZEN_IRONFLOW_BULK",
                    "fired": False,
                }
            else:
                payload = common
            path.write_text(json.dumps(payload))
            payloads[prefix] = {"path": path, "payload": payload}

    def test_binder_pins_eval_and_recompute_in_required_set(self):
        prefixes = [p for p, _ in gate.VOL_JUMP_REQUIRED]
        self.assertIn("fclr_voljump01_eval_", prefixes)
        self.assertIn("fclr_voljump01_recompute_", prefixes)

    def test_binder_requires_gate_alias_and_trigger_check(self):
        prefixes = [p for p, _ in gate.VOL_JUMP_REQUIRED]
        self.assertIn("evidence_audit_", prefixes)
        self.assertIn("trigger_check_", prefixes)

    def test_prestart_session_grandfathered_green(self):
        repo, sdir = self._repo(latest_sid="session_20261124T120000Z")
        self._write_family(sdir, "20261124T120000Z")
        res = gate.check(repo)
        self.assertFalse(res["vol_jump"]["required"])
        self.assertTrue(res["vol_jump"]["pass"])

    def test_post_start_full_heavy_set_passes(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z")
        res = gate.check(repo)
        self.assertTrue(res["vol_jump"]["required"], res["vol_jump"])
        self.assertTrue(res["vol_jump"]["pass"], res["vol_jump"]["content_failures"])
        self.assertFalse(any(f.startswith("VOL_JUMP") for f in res["failures"]))

    def test_post_start_missing_eval_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z", skip=("fclr_voljump01_eval_",))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any("fclr_voljump01_eval_" in m
                            for m in res["vol_jump"]["missing_required_artifacts"]))
        self.assertTrue(any(f.startswith("VOL_JUMP_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_missing_recompute_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z", skip=("fclr_voljump01_recompute_",))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(any("fclr_voljump01_recompute_" in m
                            for m in res["vol_jump"]["missing_required_artifacts"]))

    def test_post_start_missing_trigger_check_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z", skip=("trigger_check_",))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertFalse(res["vol_jump"]["has_trigger_check"])
        self.assertTrue(any(f.startswith("VOL_JUMP_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_post_start_invalid_json_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z")
        ev = sdir / "fclr_voljump01_eval_20261124T230000Z.json"
        ev.write_text('{"experiment_id": "FCLR-VOL-JUMP-01", "metrics": {},}')
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_jump"]["required"])
        self.assertIn("EVAL_JSON_INVALID", res["vol_jump"]["content_failures"])

    def test_post_start_total_variance_tail_design_rejected(self):
        # The closed total-variance tail-exceedance / mean-QLIKE family must not
        # satisfy the jump binder.
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z")
        pre = sdir / "fclr_voljump01_prereg_20261124T230000Z.json"
        data = json.loads(pre.read_text())
        data["design"]["kind"] = "walk_forward_classification_stress_tail_exceedance"
        pre.write_text(json.dumps(data))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertIn("PREREG_DESIGN_KIND", res["vol_jump"]["content_failures"])

    def test_post_start_promotion_without_materiality_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T230000Z")
        ev = sdir / "fclr_voljump01_eval_20261124T230000Z.json"
        data = json.loads(ev.read_text())
        data["verdict"] = "PROMOTED"
        data["materiality_met"] = False
        ev.write_text(json.dumps(data))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertIn("EVAL_PROMOTION_WITHOUT_MATERIALITY",
                      res["vol_jump"]["content_failures"])


if __name__ == "__main__":
    unittest.main()