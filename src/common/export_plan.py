from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExportPlanItem:
    input_path: Path
    output_path: Path
    output_index: int


def build_export_plan(
    input_images: list[Path],
    output_root: Path,
    prefix: str = "",
    randomize: bool = False,
    overwrite: bool = False,
    input_root: Path | None = None,
    preserve_structure: bool = False,
) -> list[ExportPlanItem]:
    if not input_images:
        raise ValueError("No input images were provided.")

    output_root = output_root.resolve()
    ordered_images = list(input_images)

    if randomize:
        random.shuffle(ordered_images)
    else:
        ordered_images = sorted(ordered_images)

    plan: list[ExportPlanItem] = []

    for index, input_path in enumerate(ordered_images, start=1):
        input_path = input_path.resolve()
        filename = f"{prefix}{index:04d}{input_path.suffix.lower()}"

        if preserve_structure:
            if input_root is None:
                raise ValueError("input_root is required when preserve_structure=True.")

            relative_parent = input_path.parent.relative_to(input_root.resolve())
            output_path = output_root / relative_parent / filename
        else:
            output_path = output_root / filename

        if output_path.exists() and not overwrite:
            raise FileExistsError(
                f"Output file already exists: {output_path}. Use --overwrite to replace it."
            )

        plan.append(
            ExportPlanItem(
                input_path=input_path,
                output_path=output_path,
                output_index=index,
            )
        )

    return plan