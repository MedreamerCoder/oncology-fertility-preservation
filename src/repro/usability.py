from __future__ import annotations

import json
import platform
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy import stats

from .data import DataValidationError, sha256_file


REQUIRED_COLUMNS = {
    "participant_id",
    "participant_group",
    "instrument",
    "timepoint",
    "item_id",
    "score",
}


def _item_number(value: Any) -> int:
    match = re.search(r"(\d+)$", str(value))
    if not match:
        raise DataValidationError(f"Cannot determine item number from {value!r}")
    return int(match.group(1))


def analyze_usability(input_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(input_path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise DataValidationError(f"Usability table missing columns: {sorted(missing)}")
    data["score"] = pd.to_numeric(data["score"], errors="raise")
    summaries: dict[str, Any] = {}

    sus = data[data["instrument"].str.upper() == "SUS"].copy()
    if not sus.empty:
        sus["item_number"] = sus["item_id"].map(_item_number)
        if not sus["score"].between(1, 5).all():
            raise DataValidationError("SUS item scores must be between 1 and 5")
        sus["contribution"] = np.where(
            sus["item_number"] % 2 == 1,
            sus["score"] - 1,
            5 - sus["score"],
        )
        item_counts = sus.groupby("participant_id")["item_number"].nunique()
        if not item_counts.eq(10).all():
            raise DataValidationError("Every SUS participant must have exactly 10 distinct items")
        sus_scores = (
            sus.groupby(["participant_id", "participant_group"], as_index=False)["contribution"]
            .sum()
            .rename(columns={"contribution": "sus_score"})
        )
        sus_scores["sus_score"] *= 2.5
        sus_scores.to_csv(output_dir / "sus_participant_scores.csv", index=False)
        summaries["sus"] = {
            group: {
                "n": int(len(values)),
                "mean": float(values.mean()),
                "sd": float(values.std(ddof=1)),
            }
            for group, values in sus_scores.groupby("participant_group")["sus_score"]
        }
        overall = sus_scores["sus_score"]
        summaries["sus"]["overall"] = {
            "n": int(len(overall)),
            "mean": float(overall.mean()),
            "sd": float(overall.std(ddof=1)),
        }

    nps = data[data["instrument"].str.upper() == "NPS"].copy()
    if not nps.empty:
        if not nps["score"].between(0, 10).all():
            raise DataValidationError("NPS recommendation scores must be between 0 and 10")
        summaries["nps"] = {}
        for group, subset in nps.groupby("participant_group"):
            scores = subset.groupby("participant_id")["score"].first()
            promoter = float((scores >= 9).mean())
            detractor = float((scores <= 6).mean())
            summaries["nps"][group] = {
                "n": int(len(scores)),
                "mean_recommendation_score": float(scores.mean()),
                "sd_recommendation_score": float(scores.std(ddof=1)),
                "promoter_proportion": promoter,
                "passive_proportion": float(((scores >= 7) & (scores <= 8)).mean()),
                "detractor_proportion": detractor,
                "net_promoter_score": float(100 * (promoter - detractor)),
            }

    literacy = data[data["instrument"].str.upper() == "FP_LITERACY"].copy()
    if not literacy.empty:
        if not literacy["score"].between(1, 5).all():
            raise DataValidationError("FP_LITERACY item scores must be between 1 and 5")
        totals = (
            literacy.groupby(["participant_id", "timepoint"], as_index=False)["score"]
            .sum()
            .pivot(index="participant_id", columns="timepoint", values="score")
        )
        if not {"pre", "post"}.issubset(totals.columns):
            raise DataValidationError("FP_LITERACY records require pre and post timepoints")
        paired = totals[["pre", "post"]].dropna().copy()
        paired["change"] = paired["post"] - paired["pre"]
        paired.reset_index().to_csv(output_dir / "literacy_participant_scores.csv", index=False)
        t_test = stats.ttest_rel(paired["post"], paired["pre"])
        summaries["literacy"] = {
            "n_paired": int(len(paired)),
            "pre_mean": float(paired["pre"].mean()),
            "pre_sd": float(paired["pre"].std(ddof=1)),
            "post_mean": float(paired["post"].mean()),
            "post_sd": float(paired["post"].std(ddof=1)),
            "mean_change": float(paired["change"].mean()),
            "paired_t": float(t_test.statistic),
            "paired_p": float(t_test.pvalue),
        }

    summary = {
        "analysis": "usability_and_literacy",
        "input": str(input_path),
        "input_sha256": sha256_file(input_path),
        "results": summaries,
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
