"""Dep-light tests for Track C per-candidate deep-audit orchestrator (stdlib, no network, no outcomes)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_panel_deep_audit_orchestrator import (  # noqa: E402
    _expand_hints,
    _is_contiguous,
    _parse_month_hint,
)

REQUIRED_SERIES = ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines")
SYMS = ("BTCUSDT", "ETHUSDT")
FIXED_UTC = "2026-11-10T03:15:27Z"
ROOT = Path(__file__).resolve().parents[1]


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _add_sidecar(p: Path):
    Path(str(p) + ".sha256").write_text(_sha256_file(p) + "\n")


def _mk_window(cache, sym, month, days, with_funding=True, with_sidecars=False):
    window = month.replace("-", "_")
    base = cache / f"{sym}_{window}"
    for day in days:
        for s in REQUIRED_SERIES:
            d = base / f"{s}-1h-{day}"
            d.mkdir(parents=True, exist_ok=True)
            csv_p = d / f"{sym}-1h-{day}.csv"
            csv_p.write_text("open_time,open\n0,1\n")
            (d / f"{sym}-1h-{day}.zip").write_bytes(b"PK")
            if with_sidecars:
                _add_sidecar(csv_p)
    if with_funding:
        fdir = base / f"{sym}-fundingRate-{month}"
        fdir.mkdir(parents=True, exist_ok=True)
        ms = int(
            datetime.strptime(days[0], "%Y-%m-%d")
            .replace(tzinfo=timezone.utc)
            .timestamp()
            * 1000
        )
        funding_p = fdir / f"{sym}-fundingRate-{month}.csv"
        funding_p.write_text(
            f"calc_time,funding_interval_hours,last_funding_rate\n{ms},8,0.0001\n"
        )
        if with_sidecars:
            _add_sidecar(funding_p)
    return base


def _run_orchestrator(cache, out, hints, extra=None):
    cmd = [
        sys.executable,
        str(ROOT / "scripts/trackc_panel_deep_audit_orchestrator.py"),
        "--cache",
        str(cache),
        "--repo-root",
        str(ROOT),
        "--symbols",
        "BTCUSDT,ETHUSDT",
        "--window-hint",
        hints,
        "--min-symbols",
        "2",
        "--min-blocks",
        "0",
        "--out",
        str(out),
    ]
    if extra:
        cmd.extend(extra)
    env = os.environ.copy()
    env["TRACKC_ORCHESTRATOR_UTC"] = FIXED_UTC
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=120, env=env)


class TestPanelDeepAuditOrchestrator(unittest.TestCase):
    def test_parse_and_hint_helpers(self):
        self.assertEqual(_parse_month_hint("2024_10"), "2024-10")
        self.assertEqual(_parse_month_hint("2024-10"), "2024-10")
        with self.assertRaises(ValueError):
            _parse_month_hint("not-a-month")
        self.assertEqual(_expand_hints(["2024_02", "2024_01", "2024_01"]), ["2024-01", "2024-02"])
        self.assertTrue(_is_contiguous(["2024-01", "2024-02", "2024-03"]))
        self.assertFalse(_is_contiguous(["2024-01", "2024-03"]))
        self.assertTrue(_is_contiguous([]))

    def test_cli_scoped_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            days = [f"2024-01-{d:02d}" for d in range(1, 6)] + [
                f"2024-02-{d:02d}" for d in range(1, 6)
            ]
            for sym in SYMS:
                _mk_window(cache, sym, "2024-01", days[:5])
                _mk_window(cache, sym, "2024-02", days[5:])
            out = td / "out.json"
            cp = _run_orchestrator(cache, out, "2024_01,2024_02")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["network_used"])
            self.assertFalse(r["summary"]["outcomes_computed"])
            self.assertFalse(r["summary"]["confirmatory_resume_ready"])
            self.assertEqual(r["candidate"]["months"], ["2024-01", "2024-02"])
            self.assertTrue(r["candidate"]["contiguous"])
            self.assertEqual(set(r["candidate"]["per_symbol"].keys()), set(SYMS))
            for sym, rep in r["candidate"]["per_symbol"].items():
                self.assertTrue(rep["required_series_complete"], sym)
                self.assertEqual(rep["days"], 10)
                self.assertFalse(rep["funding"]["months_missing_for_range"], sym)
            self.assertIn("PROVENANCE_NOT_MACHINE_VERIFIED", r["blockers_global"])
            self.assertIn("CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES", r["blockers_global"])
            out_sum = json.loads(cp.stdout)
            self.assertFalse(out_sum["network_used"])
            self.assertFalse(out_sum["outcomes_computed"])

    def test_series_gap_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            days = [f"2024-01-{d:02d}" for d in range(1, 6)]
            for sym in SYMS:
                base = _mk_window(cache, sym, "2024-01", days)
                shutil.rmtree(base / "markPriceKlines-1h-2024-01-03")
            out = td / "out.json"
            cp = _run_orchestrator(cache, out, "2024_01")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["confirmatory_resume_ready"])
            self.assertIn("REQUIRED_SERIES_GAPS_OR_MISSING", r["blockers_global"])
            for sym, rep in r["candidate"]["per_symbol"].items():
                self.assertFalse(rep["required_series_complete"], sym)
                self.assertGreater(rep["series_gaps"]["markPriceKlines"]["missing_days_vs_mark_union"], 0)
                self.assertIn("REQUIRED_SERIES_GAPS_OR_MISSING", rep["blockers"])

    def test_missing_funding_month_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            days = [f"2024-01-{d:02d}" for d in range(1, 6)]
            for sym in SYMS:
                _mk_window(cache, sym, "2024-01", days, with_funding=False)
            out = td / "out.json"
            cp = _run_orchestrator(cache, out, "2024_01")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["confirmatory_resume_ready"])
            self.assertIn("MISSING_FUNDING_MONTH_FILE", r["blockers_global"])
            for sym, rep in r["candidate"]["per_symbol"].items():
                self.assertIn("2024-01", rep["funding"]["months_missing_for_range"])
                self.assertIn("MISSING_FUNDING_MONTH_FILE", rep["blockers"])

    def test_confirmatory_ready_true_when_all_prereqs_met(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            days = [f"2024-01-{d:02d}" for d in range(1, 11)]
            for sym in SYMS:
                _mk_window(cache, sym, "2024-01", days, with_sidecars=True)
            out = td / "out.json"
            prereg = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
            cp = _run_orchestrator(cache, out, "2024_01", extra=["--prereg-hash", prereg])
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertTrue(r["summary"]["confirmatory_resume_ready"])
            self.assertTrue(r["candidate"]["confirmatory_resume_ready"])
            self.assertTrue(r["summary"]["provenance_verified"])
            self.assertEqual(r["candidate"]["prereg_hash"], prereg)
            self.assertNotIn("PROVENANCE_NOT_MACHINE_VERIFIED", r["blockers_global"])
            self.assertNotIn("MISSING_FUNDING_MONTH_FILE", r["blockers_global"])
            self.assertNotIn("REQUIRED_SERIES_GAPS_OR_MISSING", r["blockers_global"])
            out_sum = json.loads(cp.stdout)
            self.assertTrue(out_sum["confirmatory_resume_ready"])

    def test_deterministic_output(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            days = [f"2024-01-{d:02d}" for d in range(1, 6)]
            for sym in SYMS:
                _mk_window(cache, sym, "2024-01", days)
            outs = []
            for i in range(2):
                out = td / f"out{i}.json"
                cp = _run_orchestrator(cache, out, "2024_01")
                self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
                outs.append(json.loads(out.read_text()))
        self.assertEqual(outs[0], outs[1])

    def test_scoped_only_hinted_months(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            for sym in SYMS:
                _mk_window(cache, sym, "2024-01", [f"2024-01-{d:02d}" for d in range(1, 6)])
                _mk_window(cache, sym, "2024-02", [f"2024-02-{d:02d}" for d in range(1, 6)])
                _mk_window(cache, sym, "2024-03", [f"2024-03-{d:02d}" for d in range(1, 6)])
            out = td / "out.json"
            cp = _run_orchestrator(cache, out, "2024_01")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertEqual(r["candidate"]["months"], ["2024-01"])
            for sym, rep in r["candidate"]["per_symbol"].items():
                self.assertEqual(rep["days"], 5)
                self.assertEqual(rep["months"], ["2024-01"])

    def test_non_contiguous_window_reported(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache"
            days = [f"2024-01-{d:02d}" for d in range(1, 6)]
            for sym in SYMS:
                _mk_window(cache, sym, "2024-01", days)
                _mk_window(cache, sym, "2024-03", days)
            out = td / "out.json"
            cp = _run_orchestrator(cache, out, "2024_01,2024_03")
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["candidate"]["contiguous"])
            self.assertEqual(r["candidate"]["months"], ["2024-01", "2024-03"])


if __name__ == "__main__":
    unittest.main()
