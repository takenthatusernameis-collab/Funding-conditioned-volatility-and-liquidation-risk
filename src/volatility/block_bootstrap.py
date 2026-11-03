from __future__ import annotations

import math
import random
from typing import Callable, List, Tuple


def circular_block_bootstrap_indices(n: int, block_size: int, num_reps: int, seed: int = 12345) -> List[List[int]]:
    rng = random.Random(seed)
    if n == 0:
        return []
    if block_size <= 0:
        block_size = 1
    num_blocks = int(math.ceil(n / block_size))
    reps = []
    for _ in range(num_reps):
        idx = []
        for _b in range(num_blocks):
            start = rng.randint(0, n - 1)
            for j in range(block_size):
                idx.append((start + j) % n)
                if len(idx) >= n:
                    break
            if len(idx) >= n:
                break
        reps.append(idx[:n])
    return reps


def block_bootstrap_ci(
    y: List[float],
    yhat_base: List[float],
    yhat_alt: List[float],
    metric_fn: Callable[[List[float], List[float]], float],
    block_size: int = 24,
    num_reps: int = 2000,
    alpha: float = 0.05,
    seed: int = 12345,
) -> Tuple[float, float, float]:
    """Return (diff_mean, ci_low, ci_high) where diff = metric(alt) - metric(base) if alt better?
    For QLIKE, lower is better, so improvement means alt_base_diff negative? Or we report relative improvement.
    """
    diffs = []
    n = len(y)
    if n == 0:
        return (0.0, 0.0, 0.0)
    reps = circular_block_bootstrap_indices(n, block_size, num_reps, seed)
    base_full = metric_fn(y, yhat_base)
    alt_full = metric_fn(y, yhat_alt)
    full_diff = alt_full - base_full  # negative if alt better for QLIKE
    for rep_idx in reps:
        y_r = [y[i] for i in rep_idx]
        b_r = [yhat_base[i] for i in rep_idx]
        a_r = [yhat_alt[i] for i in rep_idx]
        try:
            mb = metric_fn(y_r, b_r)
            ma = metric_fn(y_r, a_r)
            if mb is None or ma is None or (isinstance(mb, float) and (math.isnan(mb) or math.isinf(mb))) or (isinstance(ma, float) and (math.isnan(ma) or math.isinf(ma))):
                continue
            diffs.append(ma - mb)
        except Exception:
            continue
    if not diffs:
        return (full_diff, full_diff, full_diff)
    diffs_sorted = sorted(diffs)
    lo = diffs_sorted[int(math.floor((alpha / 2.0) * len(diffs_sorted)))]
    hi = diffs_sorted[int(math.ceil((1.0 - alpha / 2.0) * len(diffs_sorted))) - 1]
    return (full_diff, lo, hi)
