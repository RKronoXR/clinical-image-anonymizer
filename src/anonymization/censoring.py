from pathlib import Path
from PIL import Image, ImageDraw

from src.anonymization.image_io import load_image_safely, save_image_safely


Rectangle = tuple[int, int, int, int]
RGBColor = tuple[int, int, int]


def validate_rectangle(rectangle: Rectangle, image_size: tuple[int, int]) -> Rectangle:
    x1, y1, x2, y2 = rectangle
    width, height = image_size

    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        raise ValueError(f"Rectangle is outside image bounds: {rectangle}")

    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Invalid rectangle coordinates: {rectangle}")

    return rectangle


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
        validate_rectangle(rectangle, censored.size)
        draw.rectangle(rectangle, fill=color)

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