from __future__ import annotations

import json
from dataclasses import asdict, dataclass


DEFAULT_RECTANGLE_WIDTH = 50
DEFAULT_RECTANGLE_HEIGHT = 50


@dataclass(frozen=True)
class RectangleRegion:
    image_path: str
    x: int
    y: int
    width: int
    height: int


def create_rectangle(
    image_path: str = "",
    x: int = 0,
    y: int = 0,
    width: int = DEFAULT_RECTANGLE_WIDTH,
    height: int = DEFAULT_RECTANGLE_HEIGHT,
) -> dict:
    rectangle = RectangleRegion(
        image_path=str(image_path or ""),
        x=max(0, int(x)),
        y=max(0, int(y)),
        width=max(1, int(width)),
        height=max(1, int(height)),
    )
    return asdict(rectangle)


def add_rectangle(
    rectangles: list[dict] | None,
    image_path: str = "",
) -> list[dict]:
    current = rectangles or []
    return [*current, create_rectangle(image_path=image_path)]


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

    image_path = str(current[index].get("image_path", ""))

    updated = list(current)
    updated[index] = create_rectangle(
        image_path=image_path,
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


def format_rectangles(rectangles: list[dict] | None) -> str:
    return json.dumps(rectangles or [], indent=4)