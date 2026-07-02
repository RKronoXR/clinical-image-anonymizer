from __future__ import annotations

from PIL import Image, ImageDraw


def rectangle_box(rectangle: dict) -> tuple[int, int, int, int]:
    x = int(rectangle["x"])
    y = int(rectangle["y"])
    width = int(rectangle["width"])
    height = int(rectangle["height"])

    return (
        x,
        y,
        x + width,
        y + height,
    )


def apply_black_rectangles(
    image: Image.Image,
    rectangles: list[dict] | None,
) -> Image.Image:
    output = image.convert("RGB").copy()

    draw = ImageDraw.Draw(output)

    for rectangle in rectangles or []:
        draw.rectangle(
            rectangle_box(rectangle),
            fill=(0, 0, 0),
        )

    return output