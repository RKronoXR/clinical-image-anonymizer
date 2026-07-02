from __future__ import annotations

from src.anonymization.mapping_csv import write_mapping_csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageOps
from src.anonymization.mapping_csv import write_mapping_csv

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


def _rectangle_box(rectangle: dict) -> tuple[int, int, int, int]:
    x = int(rectangle["x"])
    y = int(rectangle["y"])
    width = int(rectangle["width"])
    height = int(rectangle["height"])
    return x, y, x + width, y + height


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


def apply_black_rectangles(image: Image.Image, rectangles: list[dict] | None) -> Image.Image:
    output = image.convert("RGB").copy()
    draw = ImageDraw.Draw(output)

    for rectangle in rectangles or []:
        draw.rectangle(_rectangle_box(rectangle), fill=(0, 0, 0))

    return output


def _safe_output_format(source: Path, image_format: str | None) -> str | None:
    suffix = source.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "JPEG"
    if suffix in {".tif", ".tiff"}:
        return "TIFF"
    if suffix == ".png":
        return "PNG"
    return image_format


def _save_without_metadata(image: Image.Image, destination: Path, image_format: str | None) -> None:
    """Save an image without carrying source metadata into the output file."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    clean_image = image.convert("RGB")
    save_kwargs: dict = {}

    if image_format == "JPEG":
        save_kwargs["quality"] = 95
        save_kwargs["optimize"] = True
    elif image_format == "PNG":
        save_kwargs["optimize"] = True
    elif image_format == "TIFF":
        save_kwargs["compression"] = "raw"

    clean_image.save(destination, format=image_format, **save_kwargs)


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
            image_rectangles = _rectangles_for_source(rectangles, item.source_path)
            anonymized = apply_black_rectangles(image, image_rectangles)
            output_format = _safe_output_format(item.source_path, image.format)
            _save_without_metadata(anonymized, item.output_path, output_format)

    write_mapping_csv(plan, csv_path)

    return plan
