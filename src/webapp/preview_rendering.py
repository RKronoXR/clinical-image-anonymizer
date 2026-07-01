from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


DEFAULT_CENSOR_COLOR = (0, 0, 0)
DEFAULT_OVERLAY_COLOR = (255, 0, 0)


def load_preview_image(file_path: str | Path | None) -> Image.Image | None:
    if file_path is None:
        return None

    with Image.open(file_path) as image:
        image = ImageOps.exif_transpose(image)
        image.load()
        return image.convert("RGB")


def render_overlay_preview(
    file_path: str | Path | None,
    rectangles: list[dict] | None,
) -> Image.Image | None:
    image = load_preview_image(file_path)
    if image is None:
        return None

    draw = ImageDraw.Draw(image)
    for rectangle in rectangles or []:
        x = int(rectangle["x"])
        y = int(rectangle["y"])
        width = int(rectangle["width"])
        height = int(rectangle["height"])
        draw.rectangle(
            [x, y, x + width, y + height],
            outline=DEFAULT_OVERLAY_COLOR,
            width=4,
        )

    return image


def render_censored_preview(
    file_path: str | Path | None,
    rectangles: list[dict] | None,
    color: tuple[int, int, int] = DEFAULT_CENSOR_COLOR,
) -> Image.Image | None:
    image = load_preview_image(file_path)
    if image is None:
        return None

    draw = ImageDraw.Draw(image)
    for rectangle in rectangles or []:
        x = int(rectangle["x"])
        y = int(rectangle["y"])
        width = int(rectangle["width"])
        height = int(rectangle["height"])
        draw.rectangle(
            [x, y, x + width, y + height],
            fill=color,
        )

    return image