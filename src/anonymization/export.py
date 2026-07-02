from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageOps

from src.anonymization.image_writer import (
    safe_output_format,
    save_without_metadata,
)
from src.anonymization.mapping_csv import write_mapping_csv
from src.anonymization.rectangle_draw import (
    apply_black_rectangles,
)


ALL_IMAGES_FILENAME = "All_images"


@dataclass(frozen=True)
class ExportMapping:
    original_name: str
    new_name: str
    source_path: Path
    output_path: Path


def build_export_plan(
    image_paths: list[str | Path],
    output_dir: str | Path,
    prefix: str = "",
    randomize: bool = False,
) -> list[ExportMapping]:
    paths = [Path(path) for path in image_paths]
    if randomize:
        paths = paths.copy()
        random.shuffle(paths)

    output = Path(output_dir)
    plan: list[ExportMapping] = []

    for index, source in enumerate(paths, start=1):
        new_name = f"{prefix}{index:04d}{source.suffix.lower()}"
        destination = output / new_name
        plan.append(
            ExportMapping(
                original_name=source.name,
                new_name=new_name,
                source_path=source,
                output_path=destination,
            )
        )

    return plan

def _rectangle_filename(rectangle: dict) -> str:
    value = rectangle.get("filename") or rectangle.get("image_path") or ""
    if value == ALL_IMAGES_FILENAME:
        return ALL_IMAGES_FILENAME
    return Path(str(value)).name


def _rectangles_for_source(rectangles: list[dict] | None, source: Path) -> list[dict]:
    source_name = source.name
    return [
        rectangle
        for rectangle in rectangles or []
        if _rectangle_filename(rectangle) in {ALL_IMAGES_FILENAME, source_name}
    ]

def _check_existing_outputs(plan: Iterable[ExportMapping], csv_path: Path) -> None:
    existing = [item.output_path for item in plan if item.output_path.exists()]
    if csv_path.exists():
        existing.append(csv_path)

    if existing:
        names = ", ".join(path.name for path in existing[:5])
        raise FileExistsError(f"Export stopped. Existing output files found: {names}")


def export_anonymized_images(
    image_paths: list[str | Path],
    output_dir: str | Path,
    rectangles: list[dict] | None,
    prefix: str = "",
    randomize: bool = False,
    csv_name: str = "mapping.csv",
    overwrite: bool = False,
) -> list[ExportMapping]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    plan = build_export_plan(image_paths, output, prefix, randomize)
    csv_path = output / csv_name

    if not overwrite:
        _check_existing_outputs(plan, csv_path)

    for item in plan:
        with Image.open(item.source_path) as image:
            image = ImageOps.exif_transpose(image)
            image.load()

            image_rectangles = _rectangles_for_source(
                rectangles,
                item.source_path,
            )
            anonymized = apply_black_rectangles(image, image_rectangles)

            output_format = safe_output_format(
                item.source_path,
                image.format,
            )
            save_without_metadata(
                anonymized,
                item.output_path,
                output_format,
            )

    write_mapping_csv(plan, csv_path)

    return plan