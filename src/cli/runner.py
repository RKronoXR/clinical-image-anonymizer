from __future__ import annotations

from dataclasses import dataclass

from src.anonymization.pipeline import Rect, anonymize_image
from src.common.export_plan import ExportPlanItem


@dataclass(frozen=True)
class ExportRunSummary:
    processed: int
    failed: int
    errors: list[str]


def run_export_plan(
    export_plan: list[ExportPlanItem],
    rects: list[Rect] | None = None,
    overwrite: bool = False,
) -> ExportRunSummary:
    processed = 0
    errors: list[str] = []

    for item in export_plan:
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
            errors.append(f"{item.input_path} -> {item.output_path}: {exc}")

    return ExportRunSummary(
        processed=processed,
        failed=len(errors),
        errors=errors,
    )