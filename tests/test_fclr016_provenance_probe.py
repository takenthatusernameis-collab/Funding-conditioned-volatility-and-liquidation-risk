"""FCLR-016: provenance probe canonical-path guardrails (no network)."""
import os, sys, tempfile, unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import fclr016_verify_cache_provenance_2025plus as mod


class TestFclr016CanonicalPaths(unittest.TestCase):
    def setUp(self):
        self._orig_cache = mod.CACHE
        self.tmp = tempfile.TemporaryDirectory()
        mod.CACHE = Path(self.tmp.name)

    def tearDown(self):
        mod.CACHE = self._orig_cache
        self.tmp.cleanup()

    def test_daily_top_level_placeholder_not_canonical(self):
        sym, ym, kind, day = "BNBUSDT", "2025-08", "klines", "2025-08-01"
        d = mod.CACHE / f"{sym}_{ym.replace('-', '_')}"
        d.mkdir(parents=True)
        (d / f"{sym}-1h-{day}.zip").write_bytes(b"placeholder")
        self.assertIsNone(mod.local_zip(sym, ym, kind, day))
        dups = mod.placeholder_duplicate_paths(sym, ym, day)
        self.assertEqual([p.name for p in dups], [f"{sym}-1h-{day}.zip"])

    def test_daily_canonical_subdir_selected(self):
        sym, ym, kind, day = "BTCUSDT", "2025-08", "klines", "2025-08-01"
        d = mod.CACHE / f"{sym}_{ym.replace('-', '_')}" / f"{kind}-{day}"
        d.mkdir(parents=True)
        canon = d / f"{sym}-1h-{day}.zip"
        canon.write_bytes(b"canonical")
        got = mod.local_zip(sym, ym, kind, day)
        self.assertEqual(got, canon)

    def test_funding_rate_uses_monthly_file(self):
        sym, ym = "BTCUSDT", "2025-08"
        d = mod.CACHE / f"{sym}_{ym.replace('-', '_')}"
        d.mkdir(parents=True)
        fr = d / f"{sym}-fundingRate-{ym}.zip"
        fr.write_bytes(b"fr")
        self.assertEqual(mod.local_zip(sym, ym, "fundingRate", None), fr)


if __name__ == "__main__":
    unittest.main()
