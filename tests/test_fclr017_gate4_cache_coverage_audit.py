"""Tests for scripts/fclr017_gate4_cache_coverage_audit.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr017_gate4_cache_coverage_audit.py"


def _mk_zip(path: Path, inner_name: str, payload: bytes = b"ok\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(inner_name, payload)


def _mk_csv(path: Path, payload: bytes = b"ts,open,high,low,close\n1,1,1,1,1\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def build_month(cache: Path, sym: str, ym: str, days, kinds=("klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"), funding=True):
    d = cache / f"{sym}_{ym.replace('-', '_')}"
    d.mkdir(parents=True, exist_ok=True)
    for kind in kinds:
        for day in days:
            kd = d / f"{kind}-{day}"
            kd.mkdir(parents=True, exist_ok=True)
            _mk_zip(kd / f"{sym}-1h-{day}.zip", f"{sym}-1h-{day}.csv")
    if funding:
        fzip = d / f"{sym}-fundingRate-{ym}.zip"
        _mk_zip(fzip, f"{sym}-fundingRate-{ym}.csv", b"ts,rate\n1,0.0001\n")
        fdir = d / f"{sym}-fundingRate-{ym}"
        _mk_csv(fdir / f"{sym}-fundingRate-{ym}.csv", b"ts,rate\n1,0.0001\n")


def run_audit(cache: Path, out_dir: Path, symbols, months, extra=()):
    cmd = [
        sys.executable, str(SCRIPT),
        "--cache-root", str(cache),
        "--out-dir", str(out_dir),
        "--symbols", ",".join(symbols),
        "--months", ",".join(months),
        "--json-name", "audit.json",
        "--md-name", "audit.md",
        *extra,
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return p, json.loads((out_dir / "audit.json").read_text()) if (out_dir / "audit.json").exists() else None


class TestFclr017Gate4CacheAudit(unittest.TestCase):
    def test_complete_fixture_no_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cache = root / "cache"
            out_dir = root / "out"
            syms = ["BTCUSDT", "ETHUSDT"]
            months = ["2024-04", "2024-05"]
            for sym in syms:
                build_month(cache, sym, "2024-04", [f"2024-04-{d:02d}" for d in range(1, 31)])
                build_month(cache, sym, "2024-05", [f"2024-05-{d:02d}" for d in range(1, 32)])
            p, doc = run_audit(cache, out_dir, syms, months, extra=["--no-content-hash"])
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self.assertTrue(doc["no_confirmatory_outcomes"])
            self.assertTrue(doc["exploratory_only"])
            self.assertTrue(doc["no_network"])
            self.assertTrue(doc["not_go_for_confirmatory_outcomes"])
            self.assertTrue(doc["summary"]["global_all_months_ok"])
            self.assertEqual(doc["v3_30d_consistency"]["status"], "CONSISTENT")
            for sym in syms:
                ps = doc["summary"]["per_symbol"][sym]
                self.assertTrue(ps["all_months_ok"])
                self.assertEqual(ps["funding_months_with_expected_source"], 2)
                for kind in ("klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"):
                    self.assertEqual(ps["missing_days_by_kind"][kind], 0)
            self.assertTrue((out_dir / "fclr017_gate4_cache_audit_latest.json").exists())

    def test_missing_day_and_month_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cache = root / "cache"
            out_dir = root / "out"
            days = [f"2024-04-{d:02d}" for d in range(1, 31) if d != 15]
            build_month(cache, "BTCUSDT", "2024-04", days)
            # 2024-05 month dir missing entirely
            p, doc = run_audit(cache, out_dir, ["BTCUSDT"], ["2024-04", "2024-05"], extra=["--no-content-hash"])
            self.assertEqual(p.returncode, 0, p.stderr)
            ps = doc["summary"]["per_symbol"]["BTCUSDT"]
            self.assertEqual(ps["missing_month_dirs"], ["2024-05"])
            self.assertEqual(ps["missing_days_by_kind"]["klines"], 1)
            self.assertFalse(ps["all_months_ok"])
            self.assertEqual(doc["v3_30d_consistency"]["status"], "GAPS_OR_ANOMALIES_DOCUMENTED")
            inv = doc["inventory"]["BTCUSDT"]["2024-04"]["kinds"]["klines"]
            self.assertIn("2024-04-15", inv["missing_days"])
            types = [a["type"] for a in doc["inventory"]["BTCUSDT"]["2024-05"]["anomalies"]]
            self.assertIn("missing_month_dir", types)

    def test_quarantine_placeholder_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cache = root / "cache"
            out_dir = root / "out"
            build_month(cache, "BTCUSDT", "2024-04", ["2024-04-01"])
            # inject quarantine-like path inside a day dir
            q = cache / "BTCUSDT_2024_04" / "klines-2024-04-01" / "BTCUSDT-1h-2024-04-01_placeholder.zip"
            _mk_zip(q, "x.csv", b"x")
            p, doc = run_audit(cache, out_dir, ["BTCUSDT"], ["2024-04"], extra=["--no-content-hash"])
            self.assertEqual(p.returncode, 0, p.stderr)
            ps = doc["summary"]["per_symbol"]["BTCUSDT"]
            self.assertGreater(ps["quarantine_or_placeholder_anomaly_count"], 0)
            self.assertFalse(ps["all_months_ok"])

    def test_missing_funding_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cache = root / "cache"
            out_dir = root / "out"
            build_month(cache, "BTCUSDT", "2024-04", ["2024-04-01"], funding=False)
            p, doc = run_audit(cache, out_dir, ["BTCUSDT"], ["2024-04"], extra=["--no-content-hash"])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(doc["summary"]["per_symbol"]["BTCUSDT"]["funding_months_with_expected_source"], 0)
            types = [a["type"] for a in doc["inventory"]["BTCUSDT"]["2024-04"]["anomalies"]]
            self.assertIn("missing_funding", types)

    def test_default_scope_constants(self):
        # script default scope must match v3-30d design window/symbols relevant to 2024-04..09
        import importlib.util
        spec = importlib.util.spec_from_file_location("fclr017", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.MONTHS_DEFAULT, ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"])
        self.assertEqual(set(mod.SYMBOLS_DEFAULT), {"BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"})
        self.assertTrue(mod.V3_30D_DESIGN["sealed_expected_primary"]["ci_spans_0"])

    def test_content_hashes_present_when_enabled(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cache = root / "cache"
            out_dir = root / "out"
            build_month(cache, "BTCUSDT", "2024-04", ["2024-04-01"])
            p, doc = run_audit(cache, out_dir, ["BTCUSDT"], ["2024-04"])
            self.assertEqual(p.returncode, 0, p.stderr)
            files = doc["inventory"]["BTCUSDT"]["2024-04"]["kinds"]["klines"]["days"]["2024-04-01"]["files"]
            self.assertTrue(files)
            self.assertIn("sha256", files[0])
            self.assertEqual(len(files[0]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
