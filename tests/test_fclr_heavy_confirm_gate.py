#!/usr/bin/env python3
"""Definition-of-done gate tests for FCLR-HEAVY-CONFIRM-20261113T041200Z.

Fixtures are written to a temp research_state; the gate must fail closed until a
final verdict plus a complete evaluation and hash-matched panel exist, and must
refuse to accept INCONCLUSIVE as a final state.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import scripts.fclr_heavy_confirm_gate as gate

CHECKS = {
    "materiality_ge_2pct": True,
    "ci_excludes_zero": True,
    "instruments_ge_5": True,
    "blocks_ge_3": True,
    "loio_ge_4_of_5": True,
    "placebo_pass": True,
    "sensitivity_pass": True,
    "repro_011_pass": True,
}


def _write_fixture(root: Path, verdict: str = "CONFIRMED", *, drop_check: str | None = None,
                   corrupt_hash: bool = False) -> str:
    rs = root / "research_state"
    rs.mkdir(parents=True, exist_ok=True)
    (rs / "prereg_fclr_fwd_vol_011_confirm_20261113T041200Z.json").write_text(json.dumps({
        "status": "FROZEN_PRE_OUTCOMES", "outcome_data_inspected_before_freeze": False,
    }))
    (rs / "coverage_audit_binance_fwd_vol_20261113T041200Z.json").write_text(json.dumps({
        "symbols": {s: {} for s in ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT")},
    }))
    panel = rs / "tracka_fwd_vol_panel_20261113T041200Z.parquet"
    panel.write_bytes(b"panel-bytes")
    digest = hashlib.sha256(panel.read_bytes()).hexdigest()
    (rs / "tracka_fwd_vol_build_report_20261113T041200Z.json").write_text(json.dumps({
        "panel_sha256": ("0" * 64) if corrupt_hash else digest,
    }))
    checks = dict(CHECKS)
    if drop_check:
        checks.pop(drop_check)
    (rs / "evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z.json").write_text(json.dumps({
        "verdict": verdict, "checks": checks,
    }))
    return digest


class HeavyConfirmGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._orig_rs = gate.RS
        gate.RS = self.root / "research_state"

    def tearDown(self) -> None:
        gate.RS = self._orig_rs
        self._tmp.cleanup()

    def test_empty_state_fails(self):
        checks = gate.run_gate()
        self.assertFalse(all(c["ok"] for c in checks))

    def test_complete_confirmed_passes(self):
        _write_fixture(self.root, "CONFIRMED")
        self.assertTrue(all(c["ok"] for c in gate.run_gate()))

    def test_inconclusive_is_not_final(self):
        _write_fixture(self.root, "INCONCLUSIVE")
        by = {c["check"]: c for c in gate.run_gate()}
        self.assertFalse(by["final_verdict_recorded"]["ok"])

    def test_not_replicated_is_final(self):
        _write_fixture(self.root, "NOT_REPLICATED")
        self.assertTrue(all(c["ok"] for c in gate.run_gate()))

    def test_hash_mismatch_fails(self):
        _write_fixture(self.root, "CONFIRMED", corrupt_hash=True)
        by = {c["check"]: c for c in gate.run_gate()}
        self.assertFalse(by["build_report_hash_match"]["ok"])

    def test_missing_check_fails(self):
        _write_fixture(self.root, "CONFIRMED", drop_check="placebo_pass")
        by = {c["check"]: c for c in gate.run_gate()}
        self.assertFalse(by["eval_checks_complete"]["ok"])


if __name__ == "__main__":
    unittest.main()