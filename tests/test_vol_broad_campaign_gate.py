#!/usr/bin/env python3
"""FCLR-VOL-BROAD-01 handoff heavy-work gate regression.

tmp-isolated, read-only, no network, no parquet/outcome reads, no real
research_state writes. Pins the binder for the ACTIVE rank-0 campaign: once
FCLR-VOL-BROAD-01 starts, a post-start session cannot dodge the heavy
broad-panel funding-conditioned volatility work with a trigger-only,
prose-only, audit-only, prereg-only, verify-and-stop, or arbitrary
recompute_* session. It must emit the on-disk source registry, the
outcome-blind prereg, the HEAVY walk-forward evaluation triad
(fclr_volbroad01_eval_ py+json+md), the independent stdlib recompute
(fclr_volbroad01_recompute_ py+json), the gate-critical evidence_audit_ alias,
and a trigger check, with no zero-byte placeholders. Sessions predating the
campaign are grandfathered so the refresh that announces it stays green.

Without these tests a refactor or a future agent could silently drop
fclr_volbroad01_eval_ / fclr_volbroad01_recompute_ from the required set and
re-open the prereg-only / verify-and-stop escape hatch.
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


class TestVolBroadCampaignGate(unittest.TestCase):
    START = "20261124T035500Z"

    def _repo(self, latest_sid="session_20261124T040000Z"):
        tmp = Path(tempfile.mkdtemp(prefix="fclr143vb_"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        sdir = repo / "research_state" / latest_sid
        sdir.mkdir(parents=True)
        (repo / "AGENT_HANDOFF.md").write_text(
            "# AGENT HANDOFF\n\n## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION\n"
            f"Campaign FCLR-VOL-BROAD-01-{self.START}\n"
            f"Latest session: research_state/{latest_sid}/\n"
        )
        return repo, sdir

    def _write_family(self, sdir, sid, skip=(), content=None):
        payloads = {}
        for prefix, suffix in gate.VOL_BROAD_REQUIRED:
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
                "experiment_id": "FCLR-VOL-BROAD-01",
                "session_id": f"session_{sid}",
            }
            if prefix == "fclr_volbroad01_source_registry_":
                payload = {
                    **common,
                    "datasets": {
                        "candles_1h": {"files": 18},
                        "funding": {"files": 18},
                        "open_interest": {"files": 18},
                    },
                    "sha256_sidecars_asserted": True,
                    "input_integrity": {
                        "sha256_all_match": True,
                        "sha256_verified_bad": 0,
                    },
                    "files": [
                        {
                            "path": f"research_state/data_cache/ironflow_bulk/{i % 3}/part-{i}.parquet",
                            "sha256": hashlib.sha256(
                                f"volbroad-file-{i}".encode()
                            ).hexdigest(),
                            "sha_match": True,
                        }
                        for i in range(54)
                    ],
                }
            elif prefix == "fclr_volbroad01_prereg_":
                registry = payloads["fclr_volbroad01_source_registry_"]
                payload = {
                    **common,
                    "frozen_before_outcomes": True,
                    "outcome_data_inspected_before_freeze": False,
                    "design": {
                        "kind": "walk_forward",
                        "train_frac": 0.60,
                        "purge_embargo_h": 48,
                        "block_h": 168,
                    },
                    "train_frac": 0.60,
                    "purge_embargo_h": 48,
                    "materiality_floor_rel_qlike": 0.02,
                    "source_registry_sha256": hashlib.sha256(
                        registry["path"].read_bytes()
                    ).hexdigest(),
                }
            elif prefix == "fclr_volbroad01_eval_":
                payload = {
                    **common,
                    "status": "NOT_SUPPORTED",
                    "holdout_opened": True,
                    "n_forecasts": 1000,
                    "n_test_blocks": 30,
                    "metrics": {
                        "baseline": {"qlike": 0.25, "mse": 0.02},
                        "candidate": {"qlike": 0.25, "mse": 0.02},
                    },
                    "materiality_met": False,
                    "verdict": "NOT_SUPPORTED",
                }
            elif prefix == "fclr_volbroad01_recompute_":
                payload = {**common, "all_checks_match": True, "n_checks": 12}
            elif prefix == "fclr_volbroad01_evidence_audit_":
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
        prefixes = [p for p, _ in gate.VOL_BROAD_REQUIRED]
        self.assertIn("fclr_volbroad01_eval_", prefixes)
        self.assertIn("fclr_volbroad01_recompute_", prefixes)

    def test_binder_requires_gate_alias_and_trigger_check(self):
        prefixes = [p for p, _ in gate.VOL_BROAD_REQUIRED]
        self.assertIn("evidence_audit_", prefixes)
        self.assertIn("trigger_check_", prefixes)

    def test_post_start_source_probe_only_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(
            sdir, "20261124T040000Z",
            skip=("fclr_volbroad01_eval_", "fclr_volbroad01_recompute_"),
        )
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_broad"]["required"])
        missing = res["vol_broad"]["missing_required_artifacts"]
        self.assertTrue(any("fclr_volbroad01_eval_" in m for m in missing))
        self.assertTrue(any("fclr_volbroad01_recompute_" in m for m in missing))
        self.assertTrue(any(f.startswith("VOL_BROAD_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_missing_eval_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z",
                           skip=("fclr_volbroad01_eval_",))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_broad"]["required"])
        self.assertTrue(any("fclr_volbroad01_eval_" in m
                            for m in res["vol_broad"]["missing_required_artifacts"]))
        self.assertTrue(any(f.startswith("VOL_BROAD_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_missing_recompute_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z",
                           skip=("fclr_volbroad01_recompute_",))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_broad"]["required"])
        self.assertTrue(any("fclr_volbroad01_recompute_" in m
                            for m in res["vol_broad"]["missing_required_artifacts"]))
        self.assertTrue(any(f.startswith("VOL_BROAD_ARTIFACTS_MISSING")
                            for f in res["failures"]))

    def test_post_start_missing_trigger_check_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z",
                           skip=("trigger_check_",))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_broad"]["required"])
        self.assertFalse(res["vol_broad"]["has_trigger_check"])
        self.assertTrue(any(f.startswith("VOL_BROAD_TRIGGER_CHECK_MISSING")
                            for f in res["failures"]))

    def test_post_start_empty_files_fail_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z", content="")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_broad"]["required"])
        self.assertTrue(res["vol_broad"]["empty_required_artifacts"])
        self.assertTrue(any(f.startswith("VOL_BROAD_ARTIFACTS_EMPTY")
                            for f in res["failures"]))

    def test_post_start_nonempty_placeholders_fail_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z", content="x")
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertTrue(res["vol_broad"]["content_failures"])
        self.assertTrue(any(f.startswith("VOL_BROAD_CONTENT_INVALID")
                            for f in res["failures"]))

    def test_post_start_unmatched_recompute_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z")
        recompute = next(sdir.glob("fclr_volbroad01_recompute_*.json"))
        payload = json.loads(recompute.read_text())
        payload["all_checks_match"] = False
        recompute.write_text(json.dumps(payload))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertIn("RECOMPUTE_NOT_MATCHED", res["vol_broad"]["content_failures"])

    def test_post_start_unfrozen_prereg_fails_closed(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z")
        prereg = next(sdir.glob("fclr_volbroad01_prereg_*.json"))
        payload = json.loads(prereg.read_text())
        payload["outcome_data_inspected_before_freeze"] = True
        prereg.write_text(json.dumps(payload))
        res = gate.check(repo)
        self.assertFalse(res["pass"])
        self.assertIn(
            "PREREG_OUTCOME_INSPECTION_FLAG",
            res["vol_broad"]["content_failures"],
        )

    def test_post_start_full_heavy_set_passes(self):
        repo, sdir = self._repo()
        self._write_family(sdir, "20261124T040000Z")
        res = gate.check(repo)
        self.assertTrue(res["pass"], res["failures"])
        self.assertTrue(res["vol_broad"]["required"])
        self.assertTrue(res["vol_broad"]["pass"])
        self.assertEqual(res["vol_broad"]["missing_required_artifacts"], [])
        self.assertEqual(res["vol_broad"]["empty_required_artifacts"], [])
        self.assertEqual(res["vol_broad"]["content_failures"], [])

    def test_pre_start_session_is_grandfathered(self):
        repo, sdir = self._repo(latest_sid="session_20261124T010000Z")
        (sdir / "evidence_audit_x.md").write_text("x")
        (sdir / "recompute_generic_x.json").write_text("{}")
        res = gate.check(repo)
        self.assertFalse(res["vol_broad"]["required"])
        self.assertTrue(res["pass"], res["failures"])


if __name__ == "__main__":
    unittest.main()