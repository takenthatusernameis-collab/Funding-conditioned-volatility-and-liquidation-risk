#!/usr/bin/env python3
"""Exhaustive unauthenticated Binance probe for post-2026-11-02 data (bottleneck removal).

Probes data.binance.vision and github.com/binance/binance-public-data for:
  klines/1h, markPriceKlines/1h, indexPriceKlines/1h, premiumIndexKlines/1h, fundingRate
Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
Dates: 2026-11-03, 2026-11-04, 2026-11-05, 2026-11-06 (and funding monthly 2026-11)

For every candidate: method, URL, HTTP status, bytes, Content-Type, parsed first/last timestamps.
CRITICAL: sum(volume, taker_buyQuoteVolume, taker_buyBaseVolume) > 0 for klines.
Writes complete probe table with rejection rationale to research_state/watch/.
"""
import json
import os
import re
import sys
import time
import zipfile
import io
import urllib.request
import urllib.error
from datetime import datetime, timezone, date, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, 'research_state', 'watch')
os.makedirs(OUT_DIR, exist_ok=True)
ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']
DAYS = ['2026-11-03', '2026-11-04', '2026-11-05', '2026-11-06']
KINDS_DAILY = ['klines', 'markPriceKlines', 'indexPriceKlines', 'premiumIndexKlines']
FUNDING_MONTH = '2026-11'

BINANCE_VISION = 'https://data.binance.vision/data/futures/um/daily'
BINANCE_VISION_MONTHLY = 'https://data.binance.vision/data/futures/um/monthly'
GITHUB_RAW = 'https://raw.githubusercontent.com/binance/binance-public-data/master/data/futures/um/daily'
GITHUB_RAW_MONTHLY = 'https://raw.githubusercontent.com/binance/binance-public-data/master/data/futures/um/monthly'
TIMEOUT = 45


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'kilo-research/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read()
            return {
                'url': url, 'method': 'GET', 'status': r.status, 'ok': True,
                'bytes': len(body), 'ctype': r.headers.get('Content-Type'),
                'error': None,
            }, body
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b''
        return {
            'url': url, 'method': 'GET', 'status': e.code, 'ok': False,
            'bytes': len(body), 'ctype': e.headers.get('Content-Type') if e.headers else None,
            'error': str(e),
        }, body
    except Exception as e:
        return {
            'url': url, 'method': 'GET', 'status': None, 'ok': False,
            'bytes': 0, 'ctype': None, 'error': str(e),
        }, b''


def validate_klines_body(body, symbol, day, kind):
    """Parse zip body, return first/last timestamps and volume sums."""
    result = {'first_ts': None, 'last_ts': None, 'n_rows': 0,
              'sum_volume': None, 'sum_taker_buy_base': None, 'sum_taker_buy_quote': None,
              'volume_all_zero': None, 'header': None, 'parse_error': None}
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as z:
            names = z.namelist()
            if not names:
                result['parse_error'] = 'empty zip'
                return result
            data = z.read(names[0]).decode()
    except Exception as e:
        result['parse_error'] = f'zip read failed: {e}'
        return result
    lines = [l for l in data.split('\n') if l.strip()]
    if not lines:
        result['parse_error'] = 'no lines'
        return result
    result['header'] = lines[0]
    if len(lines) < 2:
        result['parse_error'] = 'header only, no data rows'
        return result
    try:
        cols = lines[1].split(',')
        result['first_ts'] = int(cols[0]) if len(cols) > 0 else None
    except Exception:
        result['first_ts'] = None
    try:
        cols = lines[-1].split(',')
        result['last_ts'] = int(cols[0]) if len(cols) > 0 else None
    except Exception:
        result['last_ts'] = None
    result['n_rows'] = len(lines) - 1
    vol_sum = 0.0
    tb_base_sum = 0.0
    tb_quote_sum = 0.0
    all_zero = True
    n_vol = 0
    for l in lines[1:]:
        c = l.split(',')
        try:
            v = float(c[5]) if len(c) > 5 else 0.0
        except Exception:
            v = 0.0
        vol_sum += v
        if v != 0:
            all_zero = False
        n_vol += 1
        try:
            tb_base_sum += float(c[9]) if len(c) > 9 else 0.0
        except Exception:
            pass
        try:
            tb_quote_sum += float(c[10]) if len(c) > 10 else 0.0
        except Exception:
            pass
    result['sum_volume'] = vol_sum
    result['sum_taker_buy_base'] = tb_base_sum
    result['sum_taker_buy_quote'] = tb_quote_sum
    result['volume_all_zero'] = all_zero
    return result


def validate_funding_body(body, symbol, month):
    result = {'first_ts': None, 'last_ts': None, 'n_rows': 0,
              'sum_funding_rate_abs': None, 'parse_error': None}
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as z:
            names = z.namelist()
            if not names:
                result['parse_error'] = 'empty zip'
                return result
            data = z.read(names[0]).decode()
    except Exception as e:
        result['parse_error'] = f'zip read failed: {e}'
        return result
    lines = [l for l in data.split('\n') if l.strip()]
    if not lines:
        result['parse_error'] = 'no lines'
        return result
    result['header'] = lines[0]
    if len(lines) < 2:
        result['parse_error'] = 'header only, no data rows'
        return result
    result['n_rows'] = len(lines) - 1
    try:
        result['first_ts'] = int(lines[1].split(',')[0])
    except Exception:
        pass
    try:
        result['last_ts'] = int(lines[-1].split(',')[0])
    except Exception:
        pass
    abs_sum = 0.0
    n = 0
    for l in lines[1:]:
        c = l.split(',')
        try:
            abs_sum += abs(float(c[2])) if len(c) > 2 else 0.0
            n += 1
        except Exception:
            pass
    result['sum_funding_rate_abs'] = abs_sum
    return result


def main():
    probe_table = []
    summary = {'total': 0, 'available_2xx': 0, 'admissible_volume_gt0': 0,
               'inadmissible_zero_volume': 0, 'not_found': 0, 'errors': 0}

    for sym in SYMBOLS:
        for day in DAYS:
            for kind in KINDS_DAILY:
                # data.binance.vision
                url = f'{BINANCE_VISION}/{kind}/{sym}/1h/{sym}-1h-{day}.zip'
                info, body = fetch(url)
                info['source'] = 'data.binance.vision'
                info['symbol'] = sym
                info['day'] = day
                info['kind'] = kind
                info['endpoint_type'] = 'daily_kline'
                if info['ok'] and kind != 'fundingRate':
                    v = validate_klines_body(body, sym, day, kind)
                    info.update(v)
                    if v.get('volume_all_zero') is True:
                        info['admissible'] = False
                        info['rejection_rationale'] = 'all volume == 0 (placeholder synthetic)'
                        summary['inadmissible_zero_volume'] += 1
                    elif v.get('sum_volume') is not None and v['sum_volume'] > 0:
                        info['admissible'] = True
                        info['rejection_rationale'] = None
                        summary['admissible_volume_gt0'] += 1
                    else:
                        info['admissible'] = False
                        info['rejection_rationale'] = 'unparseable or zero volume'
                        summary['inadmissible_zero_volume'] += 1
                elif info['ok'] and kind == 'fundingRate':
                    v = validate_funding_body(body, sym, day)
                    info.update(v)
                    info['admissible'] = v.get('n_rows', 0) > 0
                    info['rejection_rationale'] = None if info['admissible'] else 'no funding rows'
                else:
                    info['admissible'] = False
                    info['rejection_rationale'] = f"HTTP {info['status']}" if info['status'] else info.get('error')
                    if info['status'] == 404:
                        summary['not_found'] += 1
                    elif info['status'] == 200:
                        summary['available_2xx'] += 1
                    else:
                        summary['errors'] += 1
                probe_table.append(info)
                summary['total'] += 1
                if info['status'] == 200:
                    summary['available_2xx'] += 1

        # Monthly fundingRate on data.binance.vision
        url = f'{BINANCE_VISION_MONTHLY}/fundingRate/{sym}/{sym}-fundingRate-{FUNDING_MONTH}.zip'
        info, body = fetch(url)
        info['source'] = 'data.binance.vision'
        info['symbol'] = sym
        info['day'] = FUNDING_MONTH
        info['kind'] = 'fundingRate'
        info['endpoint_type'] = 'monthly_funding'
        if info['ok']:
            v = validate_funding_body(body, sym, FUNDING_MONTH)
            info.update(v)
            info['admissible'] = v.get('n_rows', 0) > 0
            info['rejection_rationale'] = None if info['admissible'] else 'no funding rows'
            summary['available_2xx'] += 1
        else:
            info['admissible'] = False
            info['rejection_rationale'] = f"HTTP {info['status']}" if info['status'] else info.get('error')
            if info['status'] == 404:
                summary['not_found'] += 1
            else:
                summary['errors'] += 1
        probe_table.append(info)
        summary['total'] += 1

    # GitHub raw mirror for same targets
    for sym in SYMBOLS:
        for day in DAYS:
            for kind in KINDS_DAILY:
                url = f'{GITHUB_RAW}/{kind}/{sym}/1h/{sym}-1h-{day}.zip'
                info, body = fetch(url)
                info['source'] = 'github.com/binance/binance-public-data (raw)'
                info['symbol'] = sym
                info['day'] = day
                info['kind'] = kind
                info['endpoint_type'] = 'daily_kline'
                if info['ok'] and kind != 'fundingRate':
                    v = validate_klines_body(body, sym, day, kind)
                    info.update(v)
                    if v.get('volume_all_zero') is True:
                        info['admissible'] = False
                        info['rejection_rationale'] = 'all volume == 0 (placeholder synthetic)'
                        summary['inadmissible_zero_volume'] += 1
                    elif v.get('sum_volume') is not None and v['sum_volume'] > 0:
                        info['admissible'] = True
                        info['rejection_rationale'] = None
                        summary['admissible_volume_gt0'] += 1
                    else:
                        info['admissible'] = False
                        info['rejection_rationale'] = 'unparseable or zero volume'
                        summary['inadmissible_zero_volume'] += 1
                else:
                    info['admissible'] = False
                    info['rejection_rationale'] = f"HTTP {info['status']}" if info['status'] else info.get('error')
                    if info['status'] == 404:
                        summary['not_found'] += 1
                    elif info['status'] == 200:
                        summary['available_2xx'] += 1
                    else:
                        summary['errors'] += 1
                probe_table.append(info)
                summary['total'] += 1

        url = f'{GITHUB_RAW_MONTHLY}/fundingRate/{sym}/{sym}-fundingRate-{FUNDING_MONTH}.zip'
        info, body = fetch(url)
        info['source'] = 'github.com/binance/binance-public-data (raw)'
        info['symbol'] = sym
        info['day'] = FUNDING_MONTH
        info['kind'] = 'fundingRate'
        info['endpoint_type'] = 'monthly_funding'
        if info['ok']:
            v = validate_funding_body(body, sym, FUNDING_MONTH)
            info.update(v)
            info['admissible'] = v.get('n_rows', 0) > 0
            info['rejection_rationale'] = None if info['admissible'] else 'no funding rows'
            summary['available_2xx'] += 1
        else:
            info['admissible'] = False
            info['rejection_rationale'] = f"HTTP {info['status']}" if info['status'] else info.get('error')
            if info['status'] == 404:
                summary['not_found'] += 1
            else:
                summary['errors'] += 1
        probe_table.append(info)
        summary['total'] += 1

    out = {
        'timestamp_utc': ts,
        'probe_summary': summary,
        'admissible_count': summary['admissible_volume_gt0'],
        'probe_table': probe_table,
        'conclusion': 'NO_ADMISSIBLE_POST_2026_11_02_DATA' if summary['admissible_volume_gt0'] == 0 else 'ADMISSIBLE_DATA_FOUND',
        'next_probe_schedule': 'every 60 minutes',
    }
    out_path = os.path.join(OUT_DIR, f'exhaustive_binance_probe_{ts}.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f'Wrote {out_path}')
    print(json.dumps(summary, indent=2))
    print(f'Admissible (volume>0): {summary["admissible_volume_gt0"]}')
    return 0 if summary['admissible_volume_gt0'] > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
