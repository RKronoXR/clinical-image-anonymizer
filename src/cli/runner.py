from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from src.anonymization.pipeline import Rect, anonymize_image
from src.common.export_plan import ExportPlanItem


@dataclass(frozen=True)
class ExportRunSummary:
    processed: int
    failed: int
    errors: list[str]
    csv_path: Path


def run_export_plan(
    export_plan: list[ExportPlanItem],
    rects: list[Rect] | None = None,
    overwrite: bool = False,
    csv_path: Path | None = None,
) -> ExportRunSummary:
    processed = 0
    errors: list[str] = []

    if not export_plan:
        raise ValueError("Export plan is empty.")

    if csv_path is None:
        csv_path = export_plan[0].output_path.parents[0] / "anonymization_report.csv"

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "output_index",
                "input_path",
                "output_path",
                "status",
                "error",
            ],
        )
        writer.writeheader()

        for item in export_plan:
            status = "success"
            error = ""

            try:
                if item.output_path.exists() and not overwrite:
                    raise FileExistsError(
                        f"Output file already exists: {item.output_path}"
                    )

                anonymize_image(
                    input_path=item.input_path,
                    output_path=item.output_path,
                    rects=rects,
                )
                processed += 1

            except Exception as exc:
                status = "failed"
                error = str(exc)
                errors.append(f"{item.input_path} -> {item.output_path}: {exc}")

            writer.writerow(
                {
                    "output_index": item.output_index,
                    "input_path": str(item.input_path),
                    "output_path": str(item.output_path),
                    "status": status,
                    "error": error,
                }
            )

    return ExportRunSummary(
        processed=processed,
        failed=len(errors),
        errors=errors,
        csv_path=csv_path,
    )