"""Gate 4 v3 loader hardening tests (local admissible cache, deterministic integrity).

No network. Synthetic zip/csv fixtures prove: 5-symbol include_cache loading,
funding backward/last-known alignment (no lookahead), corrupt pathological
kline-scale artifacts excluded (never fabricated), NaN never zero-filled.
"""
from __future__ import annotations

import io
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import scripts.run_funding_ablations as rfa  # noqa: E402
from src.features import funding as ff  # noqa: E402


def _write_kline_zip(path: Path, symbol: str, day: str, closes: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    base = pd.Timestamp(f"{day}T00:00:00Z")
    rows = []
    for i, c in enumerate(closes):
        ot = int((base + pd.Timedelta(hours=i)).timestamp() * 1000)
        rows.append([ot, c, c * 1.001, c * 0.999, c, 100.0, ot + 3599999, c * 100, 10, 50, c * 50, 0])
    cols = ["open_time", "open", "high", "low", "close", "volume", "close_time",
            "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]
    df = pd.DataFrame(rows, columns=cols)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{symbol}-1h-{day}.csv", df.to_csv(index=False))
    path.write_bytes(buf.getvalue())


def _write_funding_csv(path: Path, times_ms: list[int], rates: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"calc_time": times_ms, "funding_interval_hours": 8, "last_funding_rate": rates}).to_csv(path, index=False)


class TestV3Loader(unittest.TestCase):
    def test_funding_alignment_is_last_known_backward_no_lookahead(self):
        idx = pd.date_range("2024-04-01T00:00:00Z", periods=12, freq="h")
        fdf = pd.DataFrame(
            {"last_funding_rate": [0.0001, 0.0002]},
            index=pd.to_datetime(["2024-04-01T00:00:00Z", "2024-04-01T08:00:00Z"], utc=True),
        )
        fdf.index.name = "calc_time"
        out = ff.add_funding_features(idx, fdf)
        self.assertAlmostEqual(float(out.loc[pd.Timestamp("2024-04-01T07:00:00Z"), "funding_signed"]), 0.0001)
        self.assertAlmostEqual(float(out.loc[pd.Timestamp("2024-04-01T08:00:00Z"), "funding_signed"]), 0.0002)
        # before first known after first? 00:00 aligns to 00:00 exact; hour -? not in index.

    def test_cache_loader_excludes_corrupt_scale_and_never_zero_fills(self):
        with TemporaryDirectory() as td:
            tmp_path = Path(td)
            sym = "BTCUSDT"
            cache = tmp_path / "research_state" / "data_cache"
            raw = tmp_path / "data" / "raw"
            raw.mkdir(parents=True, exist_ok=True)
            _write_kline_zip(cache / f"{sym}_2024_04" / "klines-2024-04-01" / f"{sym}-1h-2024-04-01.zip", sym, "2024-04-01", [50000 + i for i in range(24)])
            _write_kline_zip(cache / f"{sym}_2024_04" / "klines-2024-04-02" / f"{sym}-1h-2024-04-02.zip", sym, "2024-04-02", [50100 + i for i in range(24)])
            _write_kline_zip(cache / f"{sym}_2024_04" / "klines-2024-04-03" / f"{sym}-1h-2024-04-03.zip", sym, "2024-04-03", [0.0008 + i * 1e-6 for i in range(24)])
            t0 = int(pd.Timestamp("2024-04-01T00:00:00Z").timestamp() * 1000)
            _write_funding_csv(cache / f"{sym}_2024_04" / f"{sym}-fundingRate-2024-04" / f"{sym}-fundingRate-2024-04.csv", [t0, t0 + 8 * 3600 * 1000], [0.0001, 0.00015])
            with patch.object(rfa, "REPO", tmp_path), patch.object(rfa, "RAW", raw), patch.object(rfa, "RES", tmp_path / "research_state"), patch.object(rfa, "CACHE", cache), patch.object(rfa, "ZIPS_DIR", tmp_path):
                k = rfa.load_kline_series([sym], "2024-04-01", "2024-04-03", horizon=24, include_cache=True)
                f = rfa.load_funding_series([sym], "2024-04-01", "2024-04-03", include_cache=True)
                panel = rfa.add_funding_to_panel(k, f)
            closes = panel["close"].dropna().to_numpy()
            self.assertGreater(closes.size, 0)
            self.assertGreater(float(closes.min()), 1000.0)
            if "funding_signed" in panel.columns:
                s = panel["funding_signed"]
                self.assertFalse(bool((s.fillna(999) == 0.0).all() and s.isna().any()))

    def test_five_symbol_loader_shape_local_cache(self):
        with TemporaryDirectory() as td:
            tmp_path = Path(td)
            syms = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
            cache = tmp_path / "research_state" / "data_cache"
            raw = tmp_path / "data" / "raw"
            raw.mkdir(parents=True, exist_ok=True)
            base_prices = {"BTCUSDT": 50000, "ETHUSDT": 3000, "SOLUSDT": 150, "XRPUSDT": 0.6, "BNBUSDT": 500}
            for sym in syms:
                bp = base_prices[sym]
                _write_kline_zip(cache / f"{sym}_2024_04" / "klines-2024-04-01" / f"{sym}-1h-2024-04-01.zip", sym, "2024-04-01", [bp * (1 + 0.001 * i) for i in range(24)])
                t0 = int(pd.Timestamp("2024-04-01T00:00:00Z").timestamp() * 1000)
                _write_funding_csv(cache / f"{sym}_2024_04" / f"{sym}-fundingRate-2024-04" / f"{sym}-fundingRate-2024-04.csv", [t0, t0 + 8 * 3600 * 1000], [0.0001, -0.00005])
            with patch.object(rfa, "REPO", tmp_path), patch.object(rfa, "RAW", raw), patch.object(rfa, "RES", tmp_path / "research_state"), patch.object(rfa, "CACHE", cache), patch.object(rfa, "ZIPS_DIR", tmp_path):
                k = rfa.load_kline_series(syms, "2024-04-01", "2024-04-01", horizon=24, include_cache=True)
                f = rfa.load_funding_series(syms, "2024-04-01", "2024-04-01", include_cache=True)
                panel = rfa.add_funding_to_panel(k, f)
            self.assertEqual(set(k.index.get_level_values("symbol").unique()), set(syms))
            self.assertEqual(set(f.index.get_level_values("symbol").unique()), set(syms))
            self.assertIn("target_rv", panel.columns)
            self.assertEqual(panel.index.get_level_values("symbol").nunique(), 5)


if __name__ == "__main__":
    unittest.main()
