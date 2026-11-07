#!/usr/bin/env python3
"""Deterministic fast repro-check of canonical research artifacts (<1s, no compute, no network).

Verifies that the sealed/negative confirmatory artifacts have not been overwritten,
timestamp-regenerated, or outcome-altered, and that their key metrics/gate verdicts
remain as recorded. This is the per-session integrity gate for the closed-negative
confirmatory program (H001 NOT_SUPPORTED; overlay INELIGIBLE). Additive only: no
prior artifact is modified, no outcomes are computed, no network/creds used.
"""
import hashlib, json, unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
RS = ROOT / "research_state"

# Canonical anchors (committed, outcome-free). If any hash changes, the artifact was
# regenerated/overwritten and must be reverted before any further work.
CANONICAL = {
    "FCLR-003": {
        "path": RS / "evaluation_summary_FCLR003.md",
        "sha256": "a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2",
        "metrics": [
            "Mean diff (modelA - modelB), QLIKE: 0.044013",
            "95% CI [0.001487, 0.093225]",
            "Relative reduction (QLIKE): -10.98%",
            "Forecast gate (all criteria): NOT_MET",
        ],
    },
    "FCLR-013": {
        "path": RS / "evaluation_summary_FCLR-013.md",
        "sha256": "107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a",
        "metrics": [
            "Mean diff (modelA - modelB), QLIKE: 0.005953",
            "95% CI [-0.011716, 0.022101]",
            "Relative reduction (QLIKE): -1.32%",
            "Forecast gate (all criteria): NOT_MET",
        ],
    },
    "V3": {
        "path": RS / "run_manifest_funding_v3_30d.json",
        "sha256": "9fd540bd5391f59ad8d3f8e7c9cd48aa6c542e400d3284d4ed2f33217a48c56e",
        "metrics": [
            '"qlike": 0.798319018412711',
            '"point": 0.4879023125556385',
            '"n_obs": 12969',
            '"n_blocks": 120',
        ],
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestCanonicalArtifactsIntegrity(unittest.TestCase):
    def test_all_canonical_hashes_unchanged(self):
        for label, spec in CANONICAL.items():
            self.assertTrue(spec["path"].exists(), f"{label} artifact missing: {spec['path']}")
            actual = _sha256(spec["path"])
            self.assertEqual(
                actual,
                spec["sha256"],
                f"{label} artifact sha256 changed (timestamp-only regen or overwrite): "
                f"expected {spec['sha256']}, got {actual}",
            )

    def test_key_metrics_and_gate_verdicts_preserved(self):
        for label, spec in CANONICAL.items():
            text = spec["path"].read_text()
            for metric in spec["metrics"]:
                self.assertIn(
                    metric, text,
                    f"{label}: key metric/gate string missing or altered: {metric!r}",
                )

    def test_no_outcome_promotion_in_negative_artifacts(self):
        # Confirmatory-negative artifacts must not contain overlay eligibility or gate pass.
        fclr013 = CANONICAL["FCLR-013"]["path"].read_text()
        self.assertIn("Forecast gate (all criteria): NOT_MET", fclr013)
        self.assertNotIn("overlay eligible", fclr013.lower())
        self.assertNotIn("risk overlay eligible", fclr013.lower())
        fclr003 = CANONICAL["FCLR-003"]["path"].read_text()
        self.assertIn("Forecast gate (all criteria): NOT_MET", fclr003)


if __name__ == "__main__":
    unittest.main()
