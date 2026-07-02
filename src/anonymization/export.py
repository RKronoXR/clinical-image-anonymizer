from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


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
    plan = []

    for index, source in enumerate(paths, start=1):
        new_name = f"{prefix}{index:04d}{source.suffix.lower()}"
        destination = output / new_name
        plan.append(ExportMapping(source.name, new_name, source, destination))

    return plan


def apply_black_rectangles(image: Image.Image, rectangles: list[dict]) -> Image.Image:
    output = image.convert("RGB").copy()
    draw = ImageDraw.Draw(output)

    for rectangle in rectangles or []:
        x = int(rectangle["x"])
        y = int(rectangle["y"])
        width = int(rectangle["width"])
        height = int(rectangle["height"])
        draw.rectangle([x, y, x + width, y + height], fill=(0, 0, 0))

    return output


def export_anonymized_images(
    image_paths: list[str | Path],
    output_dir: str | Path,
    rectangles: list[dict],
    prefix: str = "",
    randomize: bool = False,
    csv_name: str = "mapping.csv",
) -> list[ExportMapping]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    plan = build_export_plan(image_paths, output, prefix, randomize)
    csv_path = output / csv_name

    existing = [item.output_path for item in plan if item.output_path.exists()]
    if csv_path.exists():
        existing.append(csv_path)

    if existing:
        names = ", ".join(path.name for path in existing[:5])
        raise FileExistsError(f"Export stopped. Existing output files found: {names}")

    for item in plan:
        with Image.open(item.source_path) as image:
            image = ImageOps.exif_transpose(image)
            anonymized = apply_black_rectangles(image, rectangles)
            anonymized.save(item.output_path)

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["original_name", "new_name"])
        writer.writeheader()
        for item in plan:
            writer.writerow(
                {"original_name": item.original_name, "new_name": item.new_name}
            )

    return plan