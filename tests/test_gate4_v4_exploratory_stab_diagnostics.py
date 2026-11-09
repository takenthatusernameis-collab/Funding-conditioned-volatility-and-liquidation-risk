"""Synthetic tests for Gate 4 v4 exploratory stab diagnostic-field propagation.

No network, no real research_state writes.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scripts.run_gate4_v4_exploratory_stab import LABEL, make_interpretation, write_md  # noqa: E402


def _ci(point=-0.01, lo=-0.02, hi=-0.001, n_obs=1000, n_blocks=10, *, eff=None, flags=None, valid=True):
    eff = n_blocks if eff is None else eff
    flags = [] if flags is None else flags
    return {
        "point": point, "ci_low": lo, "ci_high": hi, "n_obs": n_obs, "n_blocks": n_blocks,
        "n_reps": 200, "seed": 12345, "block_hours": 24, "alpha": 0.05,
        "effective_block_count": eff, "regime_flags": flags, "ci_accounting_valid": valid,
        "degenerate": False, "inference_ok": True,
    }


def _minimal_payload():
    v_ci = {"B_rv_signed": _ci(), "C_rv_abs": _ci(), "D_rv_signed_abs": _ci(lo=-0.01, hi=0.01), "E_rv_funding_trails": _ci(lo=-0.01, hi=0.01)}
    vres = {"contrasts_vs_A": v_ci, "split_results": [{"split_id": 3, "ablations": {
        "A_rv_only": {"metrics": {"qlike": 1.0}, "per_symbol": []},
        "B_rv_signed": {"metrics": {"qlike": 1.1}, "per_symbol": [{"status": "OK", "symbol": "BTCUSDT", "metrics": {"qlike": 1.1}, "raw_pred": {"n_neg_raw": 0, "n_finite": 10}, "coef_max_abs": 0.1, "floor_rule": "v1"}]},
        "D_rv_signed_abs": {"metrics": {"qlike": 1.0}, "per_symbol": []},
        "E_rv_funding_trails": {"metrics": {"qlike": 1.0}, "per_symbol": []},
    }}]}
    payload = {
        "label": LABEL, "ts": "20990101T000000Z", "git_sha": "abc",
        "json_path": "research_state/x.json",
        "variants": {"V1_primary": vres, "V2_scale_ridge": vres, "V3_scale_ridge_target_floor": vres, "V4_winsor_train": vres},
        "loo_e_vs_a_v3": {"all": _ci(lo=-0.01, hi=0.01), "drop_BTCUSDT": _ci(lo=-0.01, hi=0.01, eff=9, flags=["low_effective_replicates"])},
    }
    payload["interpretation"] = make_interpretation(payload)
    return payload


class TestGate4V4ExploratoryStabDiagnostics(unittest.TestCase):
    def test_write_md_includes_diagnostic_columns(self):
        payload = _minimal_payload()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "stab.md"
            write_md(path, payload)
            txt = path.read_text(encoding="utf-8")
        self.assertIn("| eff_blocks | ci_valid | regime_flags |", txt)
        self.assertIn("| LOO | Point | CI low | CI high | n_obs | eff_blocks | ci_valid | regime_flags |", txt)
        self.assertIn("| ok |", txt)  # empty flags render as ok
        self.assertIn("low_effective_replicates", txt)
        self.assertIn(LABEL, txt)

    def test_write_md_handles_missing_diagnostic_fields(self):
        payload = _minimal_payload()
        # simulate legacy CI dict lacking new fields
        for v in payload["variants"].values():
            for ci in v["contrasts_vs_A"].values():
                ci.pop("effective_block_count", None)
                ci.pop("regime_flags", None)
                ci.pop("ci_accounting_valid", None)
        for ci in payload["loo_e_vs_a_v3"].values():
            ci.pop("effective_block_count", None)
            ci.pop("regime_flags", None)
            ci.pop("ci_accounting_valid", None)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "stab.md"
            write_md(path, payload)
            txt = path.read_text(encoding="utf-8")
        self.assertIn("eff_blocks", txt)
        self.assertIn("regime_flags", txt)
        # falls back to n_blocks; ci_valid missing renders as None
        self.assertIn("| 10 | 10 | None | ok |", txt)

    def test_bootstrap_json_shape_additive(self):
        ci = _ci()
        for k in ("point", "ci_low", "ci_high", "n_obs", "n_blocks", "n_reps", "seed", "block_hours"):
            self.assertIn(k, ci)
        self.assertEqual(ci["effective_block_count"], ci["n_blocks"])
        self.assertEqual(ci["regime_flags"], [])
        self.assertIs(ci["ci_accounting_valid"], True)


if __name__ == "__main__":
    unittest.main()
