#!/usr/bin/env python3
from typing import List, Tuple
import numpy as np
from scipy import stats

class LiqMicroStats:
    def __init__(self):
        pass

    def benjamini_hochberg(self, pvals: List[float], q: float = 0.05) -> Tuple[List[float], List[bool]]:
        pvals = np.array(pvals)
        n = len(pvals)
        if n == 0:
            return [], []
        # Sort
        order = np.argsort(pvals)
        ranks = np.empty_like(order)
        ranks[order] = np.arange(1, n + 1)
        # Compute adjusted p-values
        pvals_sorted = pvals[order]
        qvals_sorted = np.minimum(1.0, pvals_sorted * n / ranks[order])
        # Enforce monotonicity
        qvals_sorted = np.minimum.accumulate(qvals_sorted[::-1])[::-1]
        # Map back
        qvals = np.empty_like(qvals_sorted)
        qvals[order] = qvals_sorted
        reject = qvals < q
        return qvals.tolist(), reject.tolist()

    def bootstrap_ci(self, data, func, n_boot=1000, ci=0.95):
        if len(data) == 0:
            return (np.nan, np.nan)
        boot_results = []
        for _ in range(n_boot):
            sample = np.random.choice(data, size=len(data), replace=True)
            try:
                boot_results.append(func(sample))
            except:
                continue
        if not boot_results:
            return (np.nan, np.nan)
        alpha = 1 - ci
        lower = np.percentile(boot_results, alpha/2 * 100)
        upper = np.percentile(boot_results, (1 - alpha/2) * 100)
        return (lower, upper)
