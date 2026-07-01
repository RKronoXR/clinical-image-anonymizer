from pathlib import Path
from PIL import Image, ImageDraw

from src.anonymization.image_io import load_image_safely, save_image_safely


Rectangle = tuple[int, int, int, int]
RGBColor = tuple[int, int, int]


def clip_rectangle_to_image(
    rectangle: Rectangle,
    image_size: tuple[int, int],
) -> Rectangle | None:
    x1, y1, x2, y2 = rectangle
    width, height = image_size

    clipped = (
        max(0, x1),
        max(0, y1),
        min(width, x2),
        min(height, y2),
    )

    cx1, cy1, cx2, cy2 = clipped

    if cx2 <= cx1 or cy2 <= cy1:
        return None

    return clipped


def validate_rgb_color(color: RGBColor) -> RGBColor:
    if len(color) != 3:
        raise ValueError(f"RGB color must have exactly 3 values: {color}")

    if any(channel < 0 or channel > 255 for channel in color):
        raise ValueError(f"RGB values must be between 0 and 255: {color}")

    return color


def censor_rectangles(
    image: Image.Image,
    rectangles: list[Rectangle],
    color: RGBColor = (0, 0, 0),
) -> Image.Image:
    validate_rgb_color(color)

    censored = image.copy().convert("RGB")
    draw = ImageDraw.Draw(censored)
    
    for rectangle in rectangles:
        clipped_rectangle = clip_rectangle_to_image(rectangle, censored.size)
        if clipped_rectangle is not None:
            draw.rectangle(clipped_rectangle, fill=color)

    return censored


def censor_image_file(
    input_path: str | Path,
    output_path: str | Path,
    rectangles: list[Rectangle],
    color: RGBColor = (0, 0, 0),
) -> Path:
    image = load_image_safely(input_path)
    censored = censor_rectangles(image=image, rectangles=rectangles, color=color)
    return save_image_safely(censored, output_path)