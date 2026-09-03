from pathlib import Path

import pandas as pd

from yuhub_repro.case_analysis import analyze_case_ratings
from yuhub_repro.mcq_analysis import analyze_mcq
from yuhub_repro.usability import analyze_usability


def test_case_analysis_writes_reproducible_outputs(tmp_path: Path):
    rows = []
    models = ["A", "B", "C"]
    for case_index in range(3):
        for model_index, model in enumerate(models):
            for group in ["automated", "expert"]:
                for rater_index in range(3):
                    base = (case_index + model_index + rater_index) % 2
                    rows.extend(
                        [
                            {
                                "case_id": f"c{case_index}",
                                "answer_model": model,
                                "evaluator_group": group,
                                "evaluator_id": f"{group}_{rater_index}",
                                "criterion_kind": "binary",
                                "criterion_id": "S-1",
                                "criterion_instance": "B01:S-1",
                                "criterion_type": "safety",
                                "weight": 5,
                                "score": base,
                            },
                            {
                                "case_id": f"c{case_index}",
                                "answer_model": model,
                                "evaluator_group": group,
                                "evaluator_id": f"{group}_{rater_index}",
                                "criterion_kind": "graded",
                                "criterion_id": "E-1",
                                "criterion_instance": "G01:E-1",
                                "criterion_type": "effectiveness",
                                "weight": 3,
                                "score": [0.0, 0.6, 0.8, 1.0][(case_index + model_index + rater_index) % 4],
                            },
                        ]
                    )
    input_path = tmp_path / "ratings.csv"
    output_path = tmp_path / "case-results"
    pd.DataFrame(rows).to_csv(input_path, index=False)
    summary = analyze_case_ratings(input_path, output_path, bootstrap_iterations=10)
    assert summary["analysis"] == "case_ratings"
    assert (output_path / "analysis_summary.json").exists()
    assert (output_path / "pairwise_wilcoxon_holm.csv").exists()


def test_mcq_analysis_writes_outputs(tmp_path: Path):
    rows = []
    for question in range(1, 6):
        for run in range(1, 4):
            for model_index, model in enumerate(["A", "B", "C"]):
                correct = "A"
                selected = "A" if (question + run + model_index) % (model_index + 2) else "B"
                rows.append(
                    {
                        "question_id": str(question),
                        "model": model,
                        "run": run,
                        "selected_option": selected,
                        "correct_option": correct,
                    }
                )
    input_path = tmp_path / "mcq.csv"
    output_path = tmp_path / "mcq-results"
    pd.DataFrame(rows).to_csv(input_path, index=False)
    summary = analyze_mcq(
        input_path,
        output_path,
        permutations=100,
        bootstrap_iterations=10,
    )
    assert summary["analysis"] == "mcq"
    assert (output_path / "accuracy_summary.csv").exists()


def test_usability_analysis_writes_outputs(tmp_path: Path):
    rows = []
    for participant in ["p1", "p2"]:
        for item in range(1, 11):
            rows.append(
                {
                    "participant_id": participant,
                    "participant_group": "patient",
                    "instrument": "SUS",
                    "timepoint": "post",
                    "item_id": f"SUS{item}",
                    "score": 4 if item % 2 else 2,
                }
            )
        rows.append(
            {
                "participant_id": participant,
                "participant_group": "patient",
                "instrument": "NPS",
                "timepoint": "post",
                "item_id": "NPS1",
                "score": 9,
            }
        )
        for timepoint, value in [("pre", 2), ("post", 4)]:
            for item in range(1, 10):
                rows.append(
                    {
                        "participant_id": participant,
                        "participant_group": "patient",
                        "instrument": "FP_LITERACY",
                        "timepoint": timepoint,
                        "item_id": f"FP{item}",
                        "score": value,
                    }
                )
    input_path = tmp_path / "usability.csv"
    output_path = tmp_path / "usability-results"
    pd.DataFrame(rows).to_csv(input_path, index=False)
    summary = analyze_usability(input_path, output_path)
    assert summary["results"]["sus"]["overall"]["mean"] == 75.0
    assert summary["results"]["nps"]["patient"]["net_promoter_score"] == 100.0
    assert summary["results"]["literacy"]["mean_change"] == 18.0
