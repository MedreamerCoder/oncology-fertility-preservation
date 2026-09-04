import pandas as pd

from repro.scoring import aggregate_weighted_scores, consensus_scores


def test_weighted_scores_and_consensus():
    rows = []
    for evaluator, binary, graded in [("a", 1.0, 0.8), ("b", 0.0, 1.0)]:
        rows.extend(
            [
                {
                    "case_id": "c1",
                    "answer_model": "m1",
                    "evaluator_group": "expert",
                    "evaluator_id": evaluator,
                    "criterion_kind": "binary",
                    "criterion_id": "S-1",
                    "criterion_instance": "B01:S-1",
                    "criterion_type": "safety",
                    "weight": 5,
                    "score": binary,
                },
                {
                    "case_id": "c1",
                    "answer_model": "m1",
                    "evaluator_group": "expert",
                    "evaluator_id": evaluator,
                    "criterion_kind": "graded",
                    "criterion_id": "E-1",
                    "criterion_instance": "G01:E-1",
                    "criterion_type": "effectiveness",
                    "weight": 3,
                    "score": graded,
                },
            ]
        )
    scores = aggregate_weighted_scores(pd.DataFrame(rows))
    first = scores[scores["evaluator_id"] == "a"].iloc[0]
    assert first["score_binary"] == 1.0
    assert abs(first["score_graded"] - 0.8) < 1e-12
    assert abs(first["score_overall"] - (5 + 2.4) / 8) < 1e-12
    consensus = consensus_scores(scores)
    assert consensus.iloc[0]["evaluator_count"] == 2
    assert consensus.iloc[0]["score_binary"] == 0.5
