from pathlib import Path
from PIL import Image


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def validate_supported_image_path(image_path: str | Path) -> Path:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image extension: {path.suffix}")

    return path


def load_image_safely(image_path: str | Path) -> Image.Image:
    path = validate_supported_image_path(image_path)

    with Image.open(path) as image:
        return image.copy()


def save_image_safely(image: Image.Image, output_path: str | Path, image_format: str | None = None) -> Path:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format=image_format)
    return destination