from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_RECTANGLE_WIDTH = 50
DEFAULT_RECTANGLE_HEIGHT = 50
ALL_IMAGES_FILENAME = "All_images"


@dataclass(frozen=True)
class RectangleRegion:
    filename: str
    x: int
    y: int
    width: int
    height: int


def normalize_rectangle_filename(value: str | None) -> str:
    """Return only the filename stored for rectangle ownership."""
    if not value:
        return ""
    if value == ALL_IMAGES_FILENAME:
        return ALL_IMAGES_FILENAME
    return Path(str(value)).name


def rectangle_filename(rectangle: dict) -> str:
    """Read rectangle filename with backward compatibility for old image_path data."""
    return normalize_rectangle_filename(
        rectangle.get("filename") or rectangle.get("image_path") or ""
    )


def rectangle_applies_to_filename(rectangle: dict, filename: str | None) -> bool:
    owner = rectangle_filename(rectangle)
    current = normalize_rectangle_filename(filename)
    return owner == ALL_IMAGES_FILENAME or owner == current


def rectangles_for_filename(
    rectangles: list[dict] | None,
    filename: str | None,
) -> list[dict]:
    return [
        rectangle
        for rectangle in rectangles or []
        if rectangle_applies_to_filename(rectangle, filename)
    ]


def create_rectangle(
    filename: str = "",
    x: int = 0,
    y: int = 0,
    width: int = DEFAULT_RECTANGLE_WIDTH,
    height: int = DEFAULT_RECTANGLE_HEIGHT,
) -> dict:
    rectangle = RectangleRegion(
        filename=normalize_rectangle_filename(filename),
        x=max(0, int(x)),
        y=max(0, int(y)),
        width=max(1, int(width)),
        height=max(1, int(height)),
    )
    return asdict(rectangle)


def add_rectangle(
    rectangles: list[dict] | None,
    filename: str = "",
    x: int = 0,
    y: int = 0,
    width: int = DEFAULT_RECTANGLE_WIDTH,
    height: int = DEFAULT_RECTANGLE_HEIGHT,
) -> list[dict]:
    current = rectangles or []
    return [
        *current,
        create_rectangle(
            filename=filename,
            x=x,
            y=y,
            width=width,
            height=height,
        ),
    ]


def update_rectangle(
    rectangles: list[dict] | None,
    index: int | None,
    x: int,
    y: int,
    width: int,
    height: int,
) -> list[dict]:
    current = rectangles or []

    if index is None or index < 0 or index >= len(current):
        return current

    filename = rectangle_filename(current[index])

    updated = list(current)
    updated[index] = create_rectangle(
        filename=filename,
        x=x,
        y=y,
        width=width,
        height=height,
    )
    return updated


def delete_rectangle(rectangles: list[dict] | None, index: int | None) -> list[dict]:
    current = rectangles or []

    if index is None or index < 0 or index >= len(current):
        return current

    return [rect for i, rect in enumerate(current) if i != index]


def rectangle_choices(rectangles: list[dict] | None) -> list[str]:
    current = rectangles or []
    return [f"Rectangle {index + 1}" for index, _ in enumerate(current)]


def selected_rectangle_index(label: str | None) -> int | None:
    if not label:
        return None

    try:
        return int(label.replace("Rectangle ", "")) - 1
    except ValueError:
        return None


def get_rectangle_values(
    rectangles: list[dict] | None,
    label: str | None,
) -> tuple[int, int, int, int]:
    current = rectangles or []
    index = selected_rectangle_index(label)

    if index is None or index < 0 or index >= len(current):
        return 0, 0, DEFAULT_RECTANGLE_WIDTH, DEFAULT_RECTANGLE_HEIGHT

    rectangle = current[index]
    return (
        int(rectangle["x"]),
        int(rectangle["y"]),
        int(rectangle["width"]),
        int(rectangle["height"]),
    )


def _display_rectangle(rectangle: dict) -> dict:
    return {
        "filename": rectangle_filename(rectangle),
        "x": int(rectangle["x"]),
        "y": int(rectangle["y"]),
        "width": int(rectangle["width"]),
        "height": int(rectangle["height"]),
    }


def format_rectangles(rectangles: list[dict] | None) -> str:
    display_rectangles = {
        f"Rectangle {index + 1}": _display_rectangle(rectangle)
        for index, rectangle in enumerate(rectangles or [])
    }
    return json.dumps(display_rectangles, indent=4)
