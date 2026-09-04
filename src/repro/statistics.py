from __future__ import annotations

import itertools
from collections.abc import Callable

import numpy as np
import pandas as pd
from scipy import stats


def holm_adjust(p_values: list[float]) -> list[float]:
    values = np.asarray(p_values, dtype=float)
    order = np.argsort(values)
    adjusted = np.empty_like(values)
    running = 0.0
    count = len(values)
    for rank, position in enumerate(order):
        candidate = (count - rank) * values[position]
        running = max(running, candidate)
        adjusted[position] = min(running, 1.0)
    return adjusted.tolist()


def average_measure_icc(matrix: pd.DataFrame | np.ndarray) -> dict[str, float]:
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 2:
        raise ValueError("ICC requires at least two targets and two raters")
    if np.isnan(values).any():
        raise ValueError("ICC matrix contains missing values")
    n_targets, n_raters = values.shape
    grand = values.mean()
    target_means = values.mean(axis=1)
    rater_means = values.mean(axis=0)
    ss_target = n_raters * np.square(target_means - grand).sum()
    ss_rater = n_targets * np.square(rater_means - grand).sum()
    residual = values - target_means[:, None] - rater_means[None, :] + grand
    ss_error = np.square(residual).sum()
    ms_target = ss_target / (n_targets - 1)
    ms_rater = ss_rater / (n_raters - 1)
    ms_error = ss_error / ((n_targets - 1) * (n_raters - 1))
    absolute_denominator = ms_target + (ms_rater - ms_error) / n_targets
    absolute = (ms_target - ms_error) / absolute_denominator
    consistency = (ms_target - ms_error) / ms_target
    return {
        "icc_absolute_average": float(absolute),
        "icc_consistency_average": float(consistency),
        "n_targets": int(n_targets),
        "n_raters": int(n_raters),
    }


def paired_wilcoxon_table(wide: pd.DataFrame) -> pd.DataFrame:
    models = list(wide.columns)
    rows: list[dict[str, float | str | int]] = []
    for left, right in itertools.combinations(models, 2):
        pair = wide[[left, right]].dropna()
        difference = pair[left] - pair[right]
        if np.allclose(difference, 0):
            statistic, p_value = 0.0, 1.0
        else:
            result = stats.wilcoxon(pair[left], pair[right], alternative="two-sided", method="auto")
            statistic, p_value = float(result.statistic), float(result.pvalue)
        rows.append(
            {
                "model_a": left,
                "model_b": right,
                "n_pairs": len(pair),
                "median_difference_a_minus_b": float(np.median(difference)),
                "statistic": statistic,
                "p_value": p_value,
            }
        )
    adjusted = holm_adjust([float(row["p_value"]) for row in rows])
    for row, value in zip(rows, adjusted, strict=True):
        row["p_holm"] = value
    return pd.DataFrame(rows)


def paired_signflip_test(
    differences: np.ndarray,
    rng: np.random.Generator,
    permutations: int = 100_000,
) -> tuple[float, str]:
    values = np.asarray(differences, dtype=float)
    values = values[~np.isclose(values, 0)]
    if len(values) == 0:
        return 1.0, "all-zero"
    observed = abs(values.mean())
    if len(values) <= 20:
        signs = np.asarray(list(itertools.product([-1.0, 1.0], repeat=len(values))))
        statistics = np.abs((signs * values).mean(axis=1))
        return float(np.mean(statistics >= observed - 1e-15)), "exact"
    batch = 10_000
    extreme = 0
    completed = 0
    while completed < permutations:
        size = min(batch, permutations - completed)
        signs = rng.choice(np.array([-1.0, 1.0]), size=(size, len(values)))
        simulated = np.abs((signs * values).mean(axis=1))
        extreme += int(np.sum(simulated >= observed - 1e-15))
        completed += size
    return float((extreme + 1) / (permutations + 1)), "monte-carlo"


def percentile_interval(values: list[float], confidence: float = 0.95) -> list[float]:
    alpha = 1 - confidence
    return [
        float(np.quantile(values, alpha / 2)),
        float(np.quantile(values, 1 - alpha / 2)),
    ]


def clustered_bootstrap(
    frame: pd.DataFrame,
    cluster_column: str,
    statistic: Callable[[pd.DataFrame], dict[str, float]],
    rng: np.random.Generator,
    iterations: int,
) -> dict[str, list[float]]:
    clusters = frame[cluster_column].drop_duplicates().tolist()
    collected: dict[str, list[float]] = {}
    for _ in range(iterations):
        sample = rng.choice(clusters, size=len(clusters), replace=True)
        pieces = []
        for position, cluster in enumerate(sample):
            piece = frame[frame[cluster_column] == cluster].copy()
            piece["_bootstrap_cluster"] = f"{position}:{cluster}"
            pieces.append(piece)
        result = statistic(pd.concat(pieces, ignore_index=True))
        for key, value in result.items():
            if np.isfinite(value):
                collected.setdefault(key, []).append(float(value))
    return {key: percentile_interval(values) for key, values in collected.items()}
