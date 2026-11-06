import unittest
import pandas as pd
from pathlib import Path

FIX = Path(__file__).resolve().parent / "fixtures"

class TestTimestampParsing(unittest.TestCase):
    def test_klines_utc(self):
        df = pd.read_csv(FIX / "BTCUSDT-1h-2024-01-02.csv")
        ts = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        self.assertEqual(str(ts.dt.tz), "UTC")
        self.assertTrue(ts.is_monotonic_increasing)
        self.assertGreater(len(df), 0)

    def test_funding_utc(self):
        df = pd.read_csv(FIX / "BTCUSDT-fundingRate-2024-01.csv")
        ts = pd.to_datetime(df["calc_time"], unit="ms", utc=True)
        self.assertEqual(str(ts.dt.tz), "UTC")
        self.assertTrue(ts.is_monotonic_increasing)

if __name__ == "__main__":
    unittest.main()
