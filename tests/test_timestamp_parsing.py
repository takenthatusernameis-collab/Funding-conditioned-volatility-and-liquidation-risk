import pandas as pd
from pathlib import Path

def test_klines_timestamp_normalized():
    p = Path('data/raw/BTCUSDT-1h-2024-01-02.csv')
    df = pd.read_csv(p)
    # open_time is ms
    ts = pd.to_datetime(df['open_time'], unit='ms', utc=True)
    assert ts.is_monotonic_increasing
    assert str(ts.iloc[0])[:4] == '2024'

def test_funding_timestamp_normalized():
    p = Path('data/raw/BTCUSDT-fundingRate-2024-01.csv')
    df = pd.read_csv(p)
    ts = pd.to_datetime(df['calc_time'], unit='ms', utc=True)
    assert len(ts) > 0
