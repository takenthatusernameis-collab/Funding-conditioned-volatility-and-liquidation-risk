import csv
from pathlib import Path
import pytest

def test_btc_klines_timestamp_ms():
    p = Path('data/raw/BTCUSDT-1h-2024-01-01.csv')
    assert p.exists()
    with p.open() as f:
        r = next(csv.DictReader(f))
    assert int(r['open_time']) > 10**12  # ms

def test_btc_funding_timestamp_ms():
    p = Path('data/raw/BTCUSDT-fundingRate-2024-01.csv')
    assert p.exists()
    with p.open() as f:
        r = next(csv.DictReader(f))
    assert int(r['calc_time']) > 10**12
