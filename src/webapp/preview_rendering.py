from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


DEFAULT_CENSOR_COLOR = (0, 0, 0)
DEFAULT_OVERLAY_COLOR = (255, 0, 0)
DEFAULT_GRID_COLOR = (255, 255, 0)
DEFAULT_GRID_LABEL_COLOR = (255, 255, 255)


def load_preview_image(file_path: str | Path | None) -> Image.Image | None:
    if file_path is None:
        return None

    with Image.open(file_path) as image:
        image = ImageOps.exif_transpose(image)
        image.load()
        return image.convert("RGB")


def _valid_grid_size(grid_size: int | float | None) -> int:
    if grid_size is None:
        return 100
    return max(10, int(grid_size))


def draw_grid(
    image: Image.Image,
    grid_size: int | float | None,
) -> Image.Image:
    output = image.convert("RGB").copy()
    draw = ImageDraw.Draw(output)
    width, height = output.size
    step = _valid_grid_size(grid_size)
    font = ImageFont.load_default()

    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=DEFAULT_GRID_COLOR, width=1)
        draw.text((x + 3, 3), str(x), fill=DEFAULT_GRID_LABEL_COLOR, font=font)

    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=DEFAULT_GRID_COLOR, width=1)
        draw.text((3, y + 3), str(y), fill=DEFAULT_GRID_LABEL_COLOR, font=font)

    return output


def render_original_preview(
    file_path: str | Path | None,
    show_grid: bool = False,
    grid_size: int | float | None = 100,
) -> Image.Image | None:
    image = load_preview_image(file_path)
    if image is None:
        return None
    if show_grid:
        return draw_grid(image, grid_size)
    return image


def render_overlay_preview(
    file_path: str | Path | None,
    rectangles: list[dict] | None,
    show_grid: bool = False,
    grid_size: int | float | None = 100,
) -> Image.Image | None:
    image = load_preview_image(file_path)
    if image is None:
        return None

    if show_grid:
        image = draw_grid(image, grid_size)

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