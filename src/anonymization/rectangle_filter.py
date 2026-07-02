from __future__ import annotations

from pathlib import Path

ALL_IMAGES_FILENAME = "All_images"


def rectangle_filename(rectangle: dict) -> str:
    value = rectangle.get("filename") or rectangle.get("image_path") or ""

    if value == ALL_IMAGES_FILENAME:
        return ALL_IMAGES_FILENAME

    return Path(str(value)).name


def rectangles_for_source(
    rectangles: list[dict] | None,
    source: Path,
) -> list[dict]:
    source_name = source.name

    return [
        rectangle
        for rectangle in rectangles or []
        if rectangle_filename(rectangle)
        in {
            ALL_IMAGES_FILENAME,
            source_name,
        }
    ]