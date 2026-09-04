from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd


CASE_FIELDS = {
    "case_ID",
    "complexity",
    "disease",
    "case_detail",
    "patient_question",
    "scoring_rubric",
    "answers",
}
BINARY_FIELDS = {
    "check_id",
    "item",
    "type",
    "pass_criteria",
    "fail_criteria",
    "weight",
}
GRADED_FIELDS = {
    "rule_id",
    "item",
    "type",
    "score_5",
    "score_4",
    "score_3",
    "max_score",
    "weight",
}


class DataValidationError(ValueError):
    """Raised when a public study artifact is structurally invalid."""


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_case_dataset(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)
    validate_case_dataset(payload)
    return payload["merged_cases"]


def _missing(record: dict[str, Any], required: set[str]) -> set[str]:
    return required.difference(record)


def validate_case_dataset(payload: Any) -> None:
    errors: list[str] = []
    if not isinstance(payload, dict) or not isinstance(payload.get("merged_cases"), list):
        raise DataValidationError("Top level must be an object containing a merged_cases list.")

    cases = payload["merged_cases"]
    if not cases:
        errors.append("merged_cases is empty")
    ids: list[str] = []
    for position, case in enumerate(cases):
        prefix = f"merged_cases[{position}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} is not an object")
            continue
        missing = _missing(case, CASE_FIELDS)
        if missing:
            errors.append(f"{prefix} missing fields: {sorted(missing)}")
            continue
        ids.append(str(case["case_ID"]))
        if not isinstance(case["answers"], dict) or not case["answers"]:
            errors.append(f"{prefix}.answers must be a non-empty object")
        rubric = case["scoring_rubric"]
        if not isinstance(rubric, dict):
            errors.append(f"{prefix}.scoring_rubric must be an object")
            continue
        for kind, required in (
            ("binary_checks", BINARY_FIELDS),
            ("graded_rules", GRADED_FIELDS),
        ):
            items = rubric.get(kind)
            if not isinstance(items, list) or not items:
                errors.append(f"{prefix}.scoring_rubric.{kind} must be a non-empty list")
                continue
            for item_position, item in enumerate(items):
                item_prefix = f"{prefix}.scoring_rubric.{kind}[{item_position}]"
                if not isinstance(item, dict):
                    errors.append(f"{item_prefix} is not an object")
                    continue
                missing = _missing(item, required)
                if missing:
                    errors.append(f"{item_prefix} missing fields: {sorted(missing)}")
                    continue
                if item["type"] not in {"safety", "effectiveness"}:
                    errors.append(f"{item_prefix}.type must be safety or effectiveness")
                if not isinstance(item["weight"], (int, float)) or not 1 <= item["weight"] <= 5:
                    errors.append(f"{item_prefix}.weight must be between 1 and 5")
    if len(ids) != len(set(ids)):
        errors.append("case_ID values are not unique")
    if errors:
        raise DataValidationError("\n".join(errors))


def dataset_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    models = sorted({model for case in cases for model in case["answers"]})
    return {
        "case_count": len(cases),
        "case_ids": [case["case_ID"] for case in cases],
        "models": models,
        "response_count": sum(len(case["answers"]) for case in cases),
        "binary_criterion_count": sum(
            len(case["scoring_rubric"]["binary_checks"]) for case in cases
        ),
        "graded_criterion_count": sum(
            len(case["scoring_rubric"]["graded_rules"]) for case in cases
        ),
    }


def _criteria(case: dict[str, Any]) -> list[tuple[str, str, str, dict[str, Any]]]:
    binary = [
        ("binary", item["check_id"], f"B{position:02d}:{item['check_id']}", item)
        for position, item in enumerate(case["scoring_rubric"]["binary_checks"], start=1)
    ]
    graded = [
        ("graded", item["rule_id"], f"G{position:02d}:{item['rule_id']}", item)
        for position, item in enumerate(case["scoring_rubric"]["graded_rules"], start=1)
    ]
    return binary + graded


def ratings_template(cases: list[dict[str, Any]]) -> pd.DataFrame:
    evaluators = [
        ("automated", f"auto_{index:02d}") for index in range(1, 4)
    ] + [("expert", f"expert_{index:02d}") for index in range(1, 4)]
    rows: list[dict[str, Any]] = []
    for case in cases:
        for answer_model in case["answers"]:
            for evaluator_group, evaluator_id in evaluators:
                for criterion_kind, criterion_id, criterion_instance, item in _criteria(case):
                    rows.append(
                        {
                            "case_id": case["case_ID"],
                            "answer_model": answer_model,
                            "evaluator_group": evaluator_group,
                            "evaluator_id": evaluator_id,
                            "criterion_kind": criterion_kind,
                            "criterion_id": criterion_id,
                            "criterion_instance": criterion_instance,
                            "criterion_type": item["type"],
                            "weight": item["weight"],
                            "score": "",
                            "notes": "",
                        }
                    )
    return pd.DataFrame(rows)


def validate_ratings_against_cases(ratings: pd.DataFrame, cases: list[dict[str, Any]]) -> None:
    expected: dict[tuple[str, str], tuple[str, str, float, str]] = {}
    case_models: dict[str, set[str]] = {}
    for case in cases:
        case_id = case["case_ID"]
        case_models[case_id] = set(case["answers"])
        for kind, criterion_id, instance, item in _criteria(case):
            expected[(case_id, instance)] = (
                criterion_id,
                kind,
                float(item["weight"]),
                item["type"],
            )

    errors: list[str] = []
    for index, row in ratings.iterrows():
        key = (str(row["case_id"]), str(row["criterion_instance"]))
        if key not in expected:
            errors.append(f"row {index}: unknown case/criterion instance {key}")
            continue
        criterion_id, kind, weight, criterion_type = expected[key]
        if str(row["answer_model"]) not in case_models[key[0]]:
            errors.append(f"row {index}: unknown answer_model for {key[0]}")
        if str(row["criterion_kind"]) != kind:
            errors.append(f"row {index}: criterion_kind differs from case JSON")
        if str(row["criterion_id"]) != criterion_id:
            errors.append(f"row {index}: criterion_id differs from case JSON")
        if float(row["weight"]) != weight:
            errors.append(f"row {index}: weight differs from case JSON")
        if str(row["criterion_type"]) != criterion_type:
            errors.append(f"row {index}: criterion_type differs from case JSON")

    identity = ["case_id", "answer_model", "evaluator_group", "evaluator_id"]
    for values, group in ratings.groupby(identity, dropna=False):
        case_id = str(values[0])
        observed = set(group["criterion_instance"].astype(str))
        required = {instance for candidate_case, instance in expected if candidate_case == case_id}
        if observed != required:
            errors.append(
                f"rating unit {values} has incomplete criteria: "
                f"missing={sorted(required-observed)}, extra={sorted(observed-required)}"
            )
    if errors:
        raise DataValidationError("\n".join(errors[:50]))
