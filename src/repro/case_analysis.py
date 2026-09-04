from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy import stats

from .data import load_case_dataset, sha256_file, validate_ratings_against_cases
from .scoring import aggregate_weighted_scores, consensus_scores, validate_rating_table
from .statistics import average_measure_icc, clustered_bootstrap, paired_wilcoxon_table


SCORE_COLUMNS = ["score_binary", "score_graded", "score_overall"]


def _icc_for_group(scores: pd.DataFrame, score_column: str) -> dict[str, float]:
    data = scores.copy()
    target_case = data.get("_bootstrap_cluster", data["case_id"]).astype(str)
    data["target"] = target_case + "|" + data["answer_model"].astype(str)
    matrix = data.pivot(index="target", columns="evaluator_id", values=score_column)
    return average_measure_icc(matrix)


def _agreement(consensus: pd.DataFrame, score_column: str = "score_overall") -> dict[str, float]:
    data = consensus.copy()
    target_case = data.get("_bootstrap_cluster", data["case_id"]).astype(str)
    data["target"] = target_case + "|" + data["answer_model"].astype(str)
    matrix = data.pivot(index="target", columns="evaluator_group", values=score_column)
    matrix = matrix[["automated", "expert"]].dropna()
    icc = average_measure_icc(matrix)
    difference = matrix["automated"] - matrix["expert"]
    return {
        "icc_absolute_average": icc["icc_absolute_average"],
        "icc_consistency_average": icc["icc_consistency_average"],
        "mean_signed_difference": float(difference.mean()),
        "mean_absolute_error": float(difference.abs().mean()),
        "proportion_within_0_10": float((difference.abs() <= 0.10).mean()),
    }


def _descriptive(consensus: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (group, model), subset in consensus.groupby(["evaluator_group", "answer_model"]):
        for score_column in SCORE_COLUMNS:
            values = subset[score_column].dropna()
            rows.append(
                {
                    "evaluator_group": group,
                    "answer_model": model,
                    "score_type": score_column.removeprefix("score_"),
                    "n_cases": len(values),
                    "median": float(values.median()),
                    "q1": float(values.quantile(0.25)),
                    "q3": float(values.quantile(0.75)),
                    "mean": float(values.mean()),
                    "sd": float(values.std(ddof=1)),
                }
            )
    return pd.DataFrame(rows)


def analyze_case_ratings(
    ratings_path: str | Path,
    output_dir: str | Path,
    cases_path: str | Path | None = None,
    seed: int = 20260902,
    bootstrap_iterations: int = 2000,
) -> dict[str, Any]:
    ratings_path = Path(ratings_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ratings = validate_rating_table(pd.read_csv(ratings_path))
    if cases_path is not None:
        cases = load_case_dataset(cases_path)
        validate_ratings_against_cases(ratings, cases)

    evaluator_scores = aggregate_weighted_scores(ratings)
    consensus = consensus_scores(evaluator_scores)
    descriptive = _descriptive(consensus)
    tests: list[dict[str, Any]] = []
    pairwise_tables: list[pd.DataFrame] = []
    for group in sorted(consensus["evaluator_group"].unique()):
        subset = consensus[consensus["evaluator_group"] == group]
        for score_column in SCORE_COLUMNS:
            wide = subset.pivot(index="case_id", columns="answer_model", values=score_column).dropna()
            if wide.shape[1] < 3:
                continue
            friedman = stats.friedmanchisquare(*(wide[column] for column in wide.columns))
            tests.append(
                {
                    "evaluator_group": group,
                    "score_type": score_column.removeprefix("score_"),
                    "n_cases": len(wide),
                    "models": list(wide.columns),
                    "friedman_statistic": float(friedman.statistic),
                    "friedman_p": float(friedman.pvalue),
                }
            )
            pairwise = paired_wilcoxon_table(wide)
            pairwise.insert(0, "score_type", score_column.removeprefix("score_"))
            pairwise.insert(0, "evaluator_group", group)
            pairwise_tables.append(pairwise)

    reliability: dict[str, Any] = {}
    rng = np.random.default_rng(seed)
    for group in ["automated", "expert"]:
        group_scores = evaluator_scores[evaluator_scores["evaluator_group"] == group]
        if group_scores.empty:
            continue
        estimate = _icc_for_group(group_scores, "score_overall")
        intervals = clustered_bootstrap(
            group_scores,
            "case_id",
            lambda sample: {
                key: value
                for key, value in _icc_for_group(sample, "score_overall").items()
                if key.startswith("icc_")
            },
            rng,
            bootstrap_iterations,
        )
        reliability[group] = {"estimate": estimate, "confidence_intervals_95": intervals}

    agreement_estimate = _agreement(consensus)
    agreement_intervals = clustered_bootstrap(
        consensus,
        "case_id",
        _agreement,
        rng,
        bootstrap_iterations,
    )

    evaluator_scores.to_csv(output_dir / "evaluator_weighted_scores.csv", index=False)
    consensus.to_csv(output_dir / "consensus_scores.csv", index=False)
    descriptive.to_csv(output_dir / "descriptive_statistics.csv", index=False)
    pd.DataFrame(tests).to_csv(output_dir / "friedman_tests.csv", index=False)
    pairwise_output = pd.concat(pairwise_tables, ignore_index=True) if pairwise_tables else pd.DataFrame()
    pairwise_output.to_csv(output_dir / "pairwise_wilcoxon_holm.csv", index=False)

    summary = {
        "analysis": "case_ratings",
        "input": str(ratings_path),
        "input_sha256": sha256_file(ratings_path),
        "seed": seed,
        "bootstrap_iterations": bootstrap_iterations,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
        },
        "reliability": reliability,
        "automated_expert_agreement": {
            "estimate": agreement_estimate,
            "confidence_intervals_95": agreement_intervals,
        },
    }
    (output_dir / "analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary
