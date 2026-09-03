from __future__ import annotations

import numpy as np
import pandas as pd

from .data import DataValidationError


RATING_COLUMNS = {
    "case_id",
    "answer_model",
    "evaluator_group",
    "evaluator_id",
    "criterion_kind",
    "criterion_id",
    "criterion_instance",
    "criterion_type",
    "weight",
    "score",
}


def validate_rating_table(frame: pd.DataFrame) -> pd.DataFrame:
    missing = RATING_COLUMNS.difference(frame.columns)
    if missing:
        raise DataValidationError(f"Rating table missing columns: {sorted(missing)}")
    data = frame.copy()
    if data["score"].isna().any() or (data["score"].astype(str).str.strip() == "").any():
        raise DataValidationError("Rating table contains blank scores.")
    data["score"] = pd.to_numeric(data["score"], errors="raise")
    data["weight"] = pd.to_numeric(data["weight"], errors="raise")
    if not data["evaluator_group"].isin(["automated", "expert"]).all():
        raise DataValidationError("evaluator_group must be automated or expert")
    if not data["criterion_kind"].isin(["binary", "graded"]).all():
        raise DataValidationError("criterion_kind must be binary or graded")
    if not data["criterion_type"].isin(["safety", "effectiveness"]).all():
        raise DataValidationError("criterion_type must be safety or effectiveness")
    binary = data["criterion_kind"].eq("binary")
    graded = data["criterion_kind"].eq("graded")
    if not data.loc[binary, "score"].isin([0.0, 1.0]).all():
        raise DataValidationError("Binary scores must be 0 or 1")
    if not data.loc[graded, "score"].isin([0.0, 0.6, 0.8, 1.0]).all():
        raise DataValidationError("Graded scores must be 0, 0.6, 0.8, or 1")
    if not data["weight"].between(1, 5).all():
        raise DataValidationError("Weights must be between 1 and 5")
    key = [
        "case_id",
        "answer_model",
        "evaluator_group",
        "evaluator_id",
        "criterion_instance",
    ]
    if data.duplicated(key).any():
        raise DataValidationError("Duplicate evaluator scores found for the same atomic criterion")
    return data


def aggregate_weighted_scores(ratings: pd.DataFrame) -> pd.DataFrame:
    data = validate_rating_table(ratings)
    data["weighted_points"] = data["score"] * data["weight"]
    identity = ["case_id", "answer_model", "evaluator_group", "evaluator_id"]
    rows: list[dict[str, object]] = []
    for values, group in data.groupby(identity, sort=True):
        record = dict(zip(identity, values, strict=True))
        for label, subset in (
            ("binary", group[group["criterion_kind"] == "binary"]),
            ("graded", group[group["criterion_kind"] == "graded"]),
            ("overall", group),
        ):
            denominator = float(subset["weight"].sum())
            record[f"score_{label}"] = (
                float(subset["weighted_points"].sum() / denominator)
                if denominator
                else np.nan
            )
            record[f"weight_{label}"] = denominator
        rows.append(record)
    return pd.DataFrame(rows)


def consensus_scores(evaluator_scores: pd.DataFrame) -> pd.DataFrame:
    score_columns = ["score_binary", "score_graded", "score_overall"]
    identity = ["case_id", "answer_model", "evaluator_group"]
    consensus = evaluator_scores.groupby(identity, as_index=False)[score_columns].mean()
    counts = (
        evaluator_scores.groupby(identity, as_index=False)["evaluator_id"]
        .nunique()
        .rename(columns={"evaluator_id": "evaluator_count"})
    )
    return consensus.merge(counts, on=identity, validate="one_to_one")
