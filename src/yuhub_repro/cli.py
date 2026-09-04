from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .case_analysis import analyze_case_ratings
from .data import dataset_summary, load_case_dataset, ratings_template, sha256_file
from .mcq_analysis import analyze_mcq
from .usability import analyze_usability


def _write_csv_template(path: Path, columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(columns=columns).to_csv(path, index=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OncoFert-LLM study reproducibility utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate the public case JSON")
    validate.add_argument("cases")

    summarize = subparsers.add_parser("summarize", help="summarize the public case JSON")
    summarize.add_argument("cases")

    ratings = subparsers.add_parser("make-ratings-template", help="create atomic rating rows")
    ratings.add_argument("cases")
    ratings.add_argument("output")

    mcq_template = subparsers.add_parser("make-mcq-template", help="create an MCQ response template")
    mcq_template.add_argument("output")

    case_analysis = subparsers.add_parser("analyze-cases", help="analyze atomic case ratings")
    case_analysis.add_argument("ratings")
    case_analysis.add_argument("output_dir")
    case_analysis.add_argument("--cases")
    case_analysis.add_argument("--seed", type=int, default=20260902)
    case_analysis.add_argument("--bootstrap", type=int, default=2000)

    mcq = subparsers.add_parser("analyze-mcq", help="analyze MCQ response runs")
    mcq.add_argument("responses")
    mcq.add_argument("output_dir")
    mcq.add_argument("--seed", type=int, default=20260902)
    mcq.add_argument("--permutations", type=int, default=100_000)
    mcq.add_argument("--bootstrap", type=int, default=2000)

    usability = subparsers.add_parser("analyze-usability", help="analyze SUS, NPS, and literacy")
    usability.add_argument("records")
    usability.add_argument("output_dir")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        cases = load_case_dataset(args.cases)
        print(json.dumps({"valid": True, "sha256": sha256_file(args.cases), **dataset_summary(cases)}, ensure_ascii=False, indent=2))
    elif args.command == "summarize":
        print(json.dumps(dataset_summary(load_case_dataset(args.cases)), ensure_ascii=False, indent=2))
    elif args.command == "make-ratings-template":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        ratings_template(load_case_dataset(args.cases)).to_csv(output, index=False)
        print(output)
    elif args.command == "make-mcq-template":
        output = Path(args.output)
        _write_csv_template(
            output,
            [
                "question_id",
                "model",
                "run",
                "selected_option",
                "correct_option",
                "is_correct",
                "provider_model_id",
                "temperature",
                "seed",
                "run_timestamp_utc",
            ],
        )
        print(output)
    elif args.command == "analyze-cases":
        result = analyze_case_ratings(
            args.ratings,
            args.output_dir,
            cases_path=args.cases,
            seed=args.seed,
            bootstrap_iterations=args.bootstrap,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "analyze-mcq":
        result = analyze_mcq(
            args.responses,
            args.output_dir,
            seed=args.seed,
            permutations=args.permutations,
            bootstrap_iterations=args.bootstrap,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "analyze-usability":
        result = analyze_usability(args.records, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
