"""Dep-light tests for Track C local panel-window planner/ranker."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_panel_window_planner import contiguous_sequences


class TestPanelWindowPlanner(unittest.TestCase):
    def test_contiguous_sequences(self):
        seqs = contiguous_sequences(["2024-01", "2024-02", "2024-03", "2024-05"])
        self.assertEqual(seqs, [["2024-01", "2024-02", "2024-03"], ["2024-05"]])

    def test_cli_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "cache"
            for sym in ("BTCUSDT", "ETHUSDT"):
                for month, day in (("2024-01", "2024-01-01"), ("2024-02", "2024-02-01")):
                    wh = month.replace("-", "_")
                    base = cache / f"{sym}_{wh}"
                    for series in ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines"):
                        d = base / f"{series}-1h-{day}"
                        d.mkdir(parents=True)
                        (d / f"{sym}-1h-{day}.csv").write_text("open_time\n")
                    fdir = base / f"{sym}-fundingRate-{month}"
                    fdir.mkdir(parents=True)
                    ms = 1704067200000 if month == "2024-01" else 1706745600000
                    (fdir / f"{sym}-fundingRate-{month}.csv").write_text(
                        f"calc_time,funding_interval_hours,last_funding_rate\n{ms},8,0.0001\n")
            out = td / "plan.json"
            root = Path(__file__).resolve().parents[1]
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_panel_window_planner.py"),
                 "--cache", str(cache), "--repo-root", str(td), "--symbols", "BTCUSDT,ETHUSDT",
                 "--min-symbols", "2", "--min-blocks", "0", "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=120)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["network_used"])
            self.assertFalse(r["summary"]["outcomes_computed"])
            self.assertFalse(r["summary"]["confirmatory_resume_ready"])
            self.assertGreaterEqual(len(r["candidates_ranked"]), 1)
            best = r["candidates_ranked"][0]
            self.assertTrue(best["all_required_series_complete_fast"])
            self.assertTrue(best["all_funding_month_ok"])

    def test_cli_existing_repo(self):
        root = Path(__file__).resolve().parents[1]
        cache = root / "research_state" / "data_cache"
        if not cache.exists():
            self.skipTest("data_cache missing")
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "plan.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_panel_window_planner.py"),
                 "--repo-root", str(root), "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=300)
            self.assertEqual(cp.returncode, 0, cp.stderr[-2000:] + cp.stdout[-2000:])
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["network_used"])
            self.assertFalse(r["summary"]["confirmatory_resume_ready"])
            self.assertIn("candidates_ranked", r)
            # Completeness-first ranking: a complete candidate must never be
            # outranked by a larger-but-incomplete candidate.
            ranked = r["candidates_ranked"]
            best = ranked[0]
            for c in ranked[1:]:
                if c["meets_local_data_signals_fast"]:
                    self.assertTrue(best["meets_local_data_signals_fast"],
                                    f"incomplete candidate ranked above complete one: {best['months']} vs {c['months']}")
            if r["summary"]["best_complete_candidate_months"]:
                self.assertEqual(best["months"], r["summary"]["best_complete_candidate_months"])

    def test_ranking_completeness_first(self):
        # Two contiguous windows: a complete short one and a larger incomplete one.
        # The complete window must rank first regardless of raw size.
        cache = Path(tempfile.mkdtemp()) / "cache"
        syms = ("BTCUSDT", "ETHUSDT")
        for sym in syms:
            for month, day in (("2024-01", "2024-01-01"), ("2024-02", "2024-02-01"),
                               ("2024-03", "2024-03-01"), ("2024-04", "2024-04-01")):
                wh = month.replace("-", "_")
                base = cache / f"{sym}_{wh}"
                for series in ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines"):
                    d = base / f"{series}-1h-{day}"
                    d.mkdir(parents=True)
                    (d / f"{sym}-1h-{day}.csv").write_text("open_time\n")
                fdir = base / f"{sym}-fundingRate-{month}"
                fdir.mkdir(parents=True)
                ms = 1704067200000 + 86400000 * (int(day.split("-")[2]) - 1)
                (fdir / f"{sym}-fundingRate-{month}.csv").write_text(
                    f"calc_time,funding_interval_hours,last_funding_rate\n{ms},8,0.0001\n")
            # strip index/premium for 2024-04 to make the 4-month window incomplete
            for series in ("indexPriceKlines", "premiumIndexKlines"):
                p = cache / f"{sym}_2024_04" / f"{series}-1h-2024-04-01"
                if p.exists():
                    import shutil
                    shutil.rmtree(p)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "plan.json"
            root = Path(__file__).resolve().parents[1]
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_panel_window_planner.py"),
                 "--cache", str(cache), "--repo-root", str(td), "--symbols", "BTCUSDT,ETHUSDT",
                 "--min-symbols", "2", "--min-blocks", "0", "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=120)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            ranked = r["candidates_ranked"]
            # 2024-01..2024-03 is complete; 2024-01..2024-04 is incomplete (larger).
            complete = next(c for c in ranked if c["months"] == ["2024-01", "2024-02", "2024-03"])
            incomplete = next(c for c in ranked if c["months"] == ["2024-01", "2024-02", "2024-03", "2024-04"])
            self.assertLess(complete["rank"], incomplete["rank"])
            self.assertTrue(complete["meets_local_data_signals_fast"])
            self.assertFalse(incomplete["meets_local_data_signals_fast"])
            self.assertEqual(r["summary"]["best_complete_candidate_months"], ["2024-01", "2024-02", "2024-03"])


if __name__ == "__main__":
    unittest.main()
