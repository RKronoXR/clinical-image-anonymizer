from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RectangleRegion:
    x: int
    y: int
    width: int
    height: int


def create_rectangle(
    x: int = 0,
    y: int = 0,
    width: int = 100,
    height: int = 100,
) -> dict:
    rectangle = RectangleRegion(
        x=max(0, int(x)),
        y=max(0, int(y)),
        width=max(1, int(width)),
        height=max(1, int(height)),
    )
    return asdict(rectangle)


def add_rectangle(rectangles: list[dict] | None) -> list[dict]:
    current = rectangles or []
    return [*current, create_rectangle()]


def delete_rectangle(rectangles: list[dict] | None, index: int | None) -> list[dict]:
    current = rectangles or []

    if index is None:
        return current

    if index < 0 or index >= len(current):
        return current

    return [rect for i, rect in enumerate(current) if i != index]


def format_rectangles(rectangles: list[dict] | None) -> str:
    current = rectangles or []

    if not current:
        return "[]"

    import json

    return json.dumps(current, indent=4)