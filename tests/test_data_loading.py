from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_klines_sample_loads():
    p = ROOT / 'data/raw/btc/BTCUSDT-1h-2024-03-08.csv'
    assert p.exists()
    df = pd.read_csv(p)
    assert 'open_time' in df.columns
    assert 'close' in df.columns
    # ms timestamps
    ts = pd.to_datetime(df['open_time'], unit='ms', utc=True)
    assert ts.is_monotonic_increasing

def test_funding_sample_loads():
    p = ROOT / 'data/raw/btc_funding/BTCUSDT-fundingRate-2024-03.csv'
    assert p.exists()
    df = pd.read_csv(p)
    assert 'calc_time' in df.columns
    assert 'last_funding_rate' in df.columns
    ts = pd.to_datetime(df['calc_time'], unit='ms', utc=True)
    assert len(ts) > 0
