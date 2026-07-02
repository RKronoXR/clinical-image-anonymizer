from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

Rect = tuple[int, int, int, int]


def anonymize_image(
    input_path: Path,
    output_path: Path,
    rects: list[Rect] | None = None,
) -> None:
    rects = rects or []

    with Image.open(input_path) as image:
        clean_image = image.copy()

    draw = ImageDraw.Draw(clean_image)

    for x1, y1, x2, y2 in rects:
        draw.rectangle((x1, y1, x2, y2), fill=0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_image.save(output_path)