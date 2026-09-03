from __future__ import annotations

import itertools
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy import stats

from .data import DataValidationError, sha256_file
from .statistics import holm_adjust, paired_signflip_test, percentile_interval


REQUIRED_COLUMNS = {"question_id", "model", "run", "selected_option", "correct_option"}


def _prepare(path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(path, dtype={"question_id": str, "selected_option": str, "correct_option": str})
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise DataValidationError(f"MCQ response table missing columns: {sorted(missing)}")
    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise DataValidationError("MCQ response table contains blanks in required columns")
    data["is_correct"] = (
        data["selected_option"].str.strip().str.upper()
        == data["correct_option"].str.strip().str.upper()
    ).astype(int)
    key = ["question_id", "model", "run"]
    if data.duplicated(key).any():
        raise DataValidationError("Duplicate question/model/run rows found")
    return data


def analyze_mcq(
    input_path: str | Path,
    output_dir: str | Path,
    seed: int = 20260902,
    permutations: int = 100_000,
    bootstrap_iterations: int = 2000,
) -> dict[str, Any]:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = _prepare(input_path)
    per_run = (
        data.groupby(["model", "run"], as_index=False)
        .agg(correct=("is_correct", "sum"), n_items=("is_correct", "size"), accuracy=("is_correct", "mean"))
    )
    aggregate = (
        per_run.groupby("model", as_index=False)
        .agg(mean_accuracy=("accuracy", "mean"), sd_accuracy=("accuracy", "std"), runs=("run", "nunique"))
    )
    stability = (
        data.groupby(["model", "question_id"])["selected_option"]
        .nunique()
        .eq(1)
        .groupby("model")
        .mean()
        .rename("proportion_identical_across_runs")
        .reset_index()
    )

    data["unit"] = data["question_id"].astype(str) + "|" + data["run"].astype(str)
    wide = data.pivot(index="unit", columns="model", values="is_correct").dropna()
    if wide.shape[1] < 3:
        raise DataValidationError("Friedman analysis requires at least three complete model columns")
    friedman = stats.friedmanchisquare(*(wide[column] for column in wide.columns))
    rng = np.random.default_rng(seed)
    pairwise: list[dict[str, Any]] = []
    for model_a, model_b in itertools.combinations(wide.columns, 2):
        differences = (wide[model_a] - wide[model_b]).to_numpy(dtype=float)
        p_value, method = paired_signflip_test(differences, rng, permutations)
        bootstrap_differences: list[float] = []
        for _ in range(bootstrap_iterations):
            sample = rng.choice(differences, size=len(differences), replace=True)
            bootstrap_differences.append(float(sample.mean()))
        pairwise.append(
            {
                "model_a": model_a,
                "model_b": model_b,
                "n_pairs": len(differences),
                "accuracy_difference_a_minus_b": float(differences.mean()),
                "confidence_interval_95": percentile_interval(bootstrap_differences),
                "p_value": p_value,
                "permutation_method": method,
            }
        )
    adjusted = holm_adjust([row["p_value"] for row in pairwise])
    for row, value in zip(pairwise, adjusted, strict=True):
        row["p_holm"] = value

    per_run.to_csv(output_dir / "accuracy_by_run.csv", index=False)
    aggregate.to_csv(output_dir / "accuracy_summary.csv", index=False)
    stability.to_csv(output_dir / "answer_stability.csv", index=False)
    pd.DataFrame(pairwise).to_csv(output_dir / "paired_permutation_holm.csv", index=False)
    summary = {
        "analysis": "mcq",
        "input": str(input_path),
        "input_sha256": sha256_file(input_path),
        "seed": seed,
        "permutations": permutations,
        "bootstrap_iterations": bootstrap_iterations,
        "friedman": {
            "statistic": float(friedman.statistic),
            "p_value": float(friedman.pvalue),
            "n_paired_question_runs": len(wide),
            "models": list(wide.columns),
        },
        "pairwise": pairwise,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
        },
    }
    (output_dir / "analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary
