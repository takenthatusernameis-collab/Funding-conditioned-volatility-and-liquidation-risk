"""Synthetic tests for Gate 4 v4 EXPLORATORY leakage-audit markdown diagnostic propagation.

No network, no real research_state writes, no heavy data passes. Exercises the
serializer helpers (`_diag_field`, `_flags_str`, `write_md`) against additive
bootstrap diagnostic fields (`effective_block_count`, `regime_flags`,
`ci_accounting_valid`) and legacy-fallback payloads.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scripts.run_gate4_v4_leakage_audit import (  # noqa: E402
    LABEL,
    _diag_field,
    _flags_str,
    extract_additive_diag,
    write_md,
)


def _ci(*, point=0.1, lo=-0.05, hi=0.25, n_obs=1000, n_blocks=120, eff=None,
        flags=None, valid=True, with_diag=True, degenerate=False, inference_ok=True,
        n_reps_effective=2000, n_obs_finite=None):
    eff = n_blocks if eff is None else eff
    flags = [] if flags is None else list(flags)
    n_obs_finite = n_obs if n_obs_finite is None else n_obs_finite
    ci = {
        "point": point, "ci_low": lo, "ci_high": hi, "n_obs": n_obs, "n_blocks": n_blocks,
        "n_reps": 2000, "seed": 20261109, "block_hours": 24, "alpha": 0.05,
    }
    if with_diag:
        ci["effective_block_count"] = eff
        ci["regime_flags"] = flags
        ci["ci_accounting_valid"] = valid
        ci["degenerate"] = degenerate
        ci["inference_ok"] = inference_ok
        ci["n_reps_effective"] = n_reps_effective
        ci["n_obs_finite"] = n_obs_finite
    return ci


def _minimal_payload(bb=None):
    bb = bb or {
        "run1": _ci(), "run2": _ci(), "seed": 20261109, "identical_on_rerun": True,
    }
    return {
        "label": LABEL, "ts": "20990101T000000Z", "git_sha": "abc",
        "prereg_v4": "prereg.json", "confirmatory_claim_go": "NO_GO",
        "json_path": "research_state/x.json", "md_state_path": "research_state/x.md",
        "md_results_path": "results/x.md",
        "variant_audits": [],
        "leakage_invariance_all": True,
        "block_bootstrap_reproducibility": bb,
        "interpretation": "EXPLORATORY ONLY.",
    }


class TestLeakageAuditMdDiagnostics(unittest.TestCase):
    def test_diag_field_additive_present(self):
        ci = _ci(eff=100, flags=["low_effective_replicates"], valid=False)
        self.assertEqual(_diag_field(ci, "effective_block_count"), 100)
        self.assertEqual(_diag_field(ci, "ci_accounting_valid"), False)
        self.assertEqual(_diag_field(ci, "regime_flags"), ["low_effective_replicates"])

    def test_diag_field_legacy_fallback(self):
        # legacy CI dict without additive fields falls back gracefully
        legacy = {"point": 0.1, "ci_low": -0.05, "ci_high": 0.25, "n_obs": 1000, "n_blocks": 120}
        self.assertEqual(_diag_field(legacy, "effective_block_count"), 120)
        self.assertIsNone(_diag_field(legacy, "ci_accounting_valid"))
        self.assertEqual(_diag_field(legacy, "regime_flags", []), [])

    def test_diag_field_none_payload(self):
        self.assertIsNone(_diag_field(None, "effective_block_count"))
        self.assertEqual(_diag_field(None, "regime_flags", []), [])

    def test_flags_str_rendering(self):
        self.assertEqual(_flags_str([]), "ok")
        self.assertEqual(_flags_str(None), "ok")
        self.assertEqual(_flags_str(["too_few_blocks"]), "too_few_blocks")
        self.assertEqual(_flags_str(["a", "b"]), "a;b")

    def test_write_md_includes_diagnostic_columns(self):
        payload = _minimal_payload()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "leak.md"
            write_md(path, payload)
            txt = path.read_text(encoding="utf-8")
        self.assertIn("| eff_blocks | ci_valid | regime_flags |", txt)
        self.assertIn("effective_block_count", txt)
        self.assertIn("ci_accounting_valid", txt)
        self.assertIn("regime_flags", txt)
        self.assertIn("EXPLORATORY ONLY", txt)

    def test_write_md_legacy_ci_fallback(self):
        legacy_run = {"point": 0.1, "ci_low": -0.05, "ci_high": 0.25, "n_obs": 1000, "n_blocks": 120}
        payload = _minimal_payload({
            "run1": legacy_run, "run2": legacy_run, "seed": 20261109, "identical_on_rerun": True,
            "run1_diagnostics": {"effective_block_count": 120, "ci_accounting_valid": None,
                                 "regime_flags": [], "degenerate": None, "inference_ok": None,
                                 "n_reps_effective": None, "n_obs_finite": None},
            "run2_diagnostics": {"effective_block_count": 120, "ci_accounting_valid": None,
                                 "regime_flags": [], "degenerate": None, "inference_ok": None,
                                 "n_reps_effective": None, "n_obs_finite": None},
            "diagnostics_identical_on_rerun": True,
        })
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "leak_legacy.md"
            write_md(path, payload)
            txt = path.read_text(encoding="utf-8")
        # eff_blocks falls back to n_blocks (120); ci_valid renders as None; flags render ok.
        # Per-metric reproducibility row carries the fallback values for both runs.
        self.assertIn("| n_blocks | 120 | 120 | True | 120 | None | ok |", txt)
        self.assertIn("| effective_block_count | 120 | 120 | True | - | - | - |", txt)
        self.assertIn("| ci_accounting_valid | None | None | True | - | - | - |", txt)
        self.assertIn("| regime_flags | ok | ok | True | - | - | - |", txt)
        self.assertIn("**Effective blocks: 120**", txt)
        self.assertIn("**CI accounting valid: None**", txt)
        self.assertIn("**Regime flags: ok**", txt)

    def test_write_md_surfaces_regime_flags(self):
        run1 = _ci(eff=2, flags=["too_few_blocks", "low_effective_replicates"], valid=False)
        run2 = _ci(eff=2, flags=["too_few_blocks", "low_effective_replicates"], valid=False)
        payload = _minimal_payload({
            "run1": run1, "run2": run2, "seed": 20261109, "identical_on_rerun": True,
        })
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "leak_flags.md"
            write_md(path, payload)
            txt = path.read_text(encoding="utf-8")
        self.assertIn("too_few_blocks;low_effective_replicates", txt)
        self.assertIn("**Effective blocks: 2**", txt)
        self.assertIn("**CI accounting valid: False**", txt)


class TestLeakageAuditJsonDiagnostics(unittest.TestCase):
    """Verifies the persisted JSON payload (not just markdown) carries additive
    bootstrap diagnostics explicitly, so leakage audits can read them without
    re-running the bootstrap."""

    def test_extract_additive_diag_full(self):
        ci = _ci(eff=100, flags=["low_effective_replicates"], valid=False,
                 degenerate=False, inference_ok=True, n_reps_effective=1500, n_obs_finite=900)
        d = extract_additive_diag(ci)
        self.assertEqual(d["effective_block_count"], 100)
        self.assertEqual(d["ci_accounting_valid"], False)
        self.assertEqual(d["regime_flags"], ["low_effective_replicates"])
        self.assertEqual(d["degenerate"], False)
        self.assertEqual(d["inference_ok"], True)
        self.assertEqual(d["n_reps_effective"], 1500)
        self.assertEqual(d["n_obs_finite"], 900)

    def test_extract_additive_diag_legacy(self):
        legacy = {"point": 0.1, "ci_low": -0.05, "ci_high": 0.25, "n_obs": 1000, "n_blocks": 120}
        d = extract_additive_diag(legacy)
        self.assertEqual(d["effective_block_count"], 120)
        self.assertIsNone(d["ci_accounting_valid"])
        self.assertEqual(d["regime_flags"], [])
        self.assertIsNone(d["degenerate"])
        self.assertIsNone(d["inference_ok"])

    def test_extract_additive_diag_none(self):
        d = extract_additive_diag(None)
        self.assertIsNone(d["effective_block_count"])
        self.assertIsNone(d["ci_accounting_valid"])
        self.assertEqual(d["regime_flags"], [])

    def test_payload_json_carries_additive_diagnostics(self):
        """The serialized payload must expose run1_diagnostics/run2_diagnostics and
        diagnostics_identical_on_rerun so JSON consumers can audit CI accounting."""
        run1 = _ci(eff=80, flags=["too_few_blocks"], valid=False, degenerate=True, inference_ok=False)
        run2 = _ci(eff=80, flags=["too_few_blocks"], valid=False, degenerate=True, inference_ok=False)
        payload = _minimal_payload({
            "run1": run1, "run2": run2, "seed": 20261109, "identical_on_rerun": True,
            "run1_diagnostics": extract_additive_diag(run1),
            "run2_diagnostics": extract_additive_diag(run2),
            "diagnostics_identical_on_rerun": True,
        })
        bb = payload["block_bootstrap_reproducibility"]
        self.assertIn("run1_diagnostics", bb)
        self.assertIn("run2_diagnostics", bb)
        self.assertTrue(bb["diagnostics_identical_on_rerun"])
        self.assertEqual(bb["run1_diagnostics"]["effective_block_count"], 80)
        self.assertEqual(bb["run1_diagnostics"]["ci_accounting_valid"], False)
        self.assertEqual(bb["run1_diagnostics"]["regime_flags"], ["too_few_blocks"])
        self.assertEqual(bb["run1_diagnostics"]["degenerate"], True)
        self.assertEqual(bb["run1_diagnostics"]["inference_ok"], False)

    def test_interpretation_mentions_additive_diagnostics(self):
        run1 = _ci(eff=80, flags=[], valid=True)
        payload = _minimal_payload({
            "run1": run1, "run2": run1, "seed": 20261109, "identical_on_rerun": True,
            "run1_diagnostics": extract_additive_diag(run1),
            "run2_diagnostics": extract_additive_diag(run1),
            "diagnostics_identical_on_rerun": True,
        })
        from scripts.run_gate4_v4_leakage_audit import make_interpretation
        interp = make_interpretation(payload)
        self.assertIn("Additive diagnostics reproducible", interp)
        self.assertIn("effective_block_count", interp)


if __name__ == "__main__":
    unittest.main()