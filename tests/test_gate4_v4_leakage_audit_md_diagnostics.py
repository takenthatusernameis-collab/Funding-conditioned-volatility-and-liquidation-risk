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
    write_md,
)


def _ci(*, point=0.1, lo=-0.05, hi=0.25, n_obs=1000, n_blocks=120, eff=None,
        flags=None, valid=True, with_diag=True):
    eff = n_blocks if eff is None else eff
    flags = [] if flags is None else list(flags)
    ci = {
        "point": point, "ci_low": lo, "ci_high": hi, "n_obs": n_obs, "n_blocks": n_blocks,
        "n_reps": 2000, "seed": 20261109, "block_hours": 24, "alpha": 0.05,
    }
    if with_diag:
        ci["effective_block_count"] = eff
        ci["regime_flags"] = flags
        ci["ci_accounting_valid"] = valid
        ci["degenerate"] = False
        ci["inference_ok"] = True
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
        })
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "leak_legacy.md"
            write_md(path, payload)
            txt = path.read_text(encoding="utf-8")
        # eff_blocks falls back to n_blocks (120); ci_valid renders as None; flags render ok
        self.assertIn("| 120 | 120 | None | ok |", txt)

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


if __name__ == "__main__":
    unittest.main()