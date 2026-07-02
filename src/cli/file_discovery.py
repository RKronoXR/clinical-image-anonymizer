from __future__ import annotations

from pathlib import Path

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}


def is_supported_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS


def discover_input_images(input_path: Path, recursive: bool = False) -> list[Path]:
    if input_path.is_file():
        if not is_supported_image(input_path):
            raise ValueError(f"Unsupported image format: {input_path}")
        return [input_path]

    if not input_path.is_dir():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    pattern = "**/*" if recursive else "*"
    images = sorted(path for path in input_path.glob(pattern) if is_supported_image(path))

    if not images:
        raise ValueError(f"No supported images found in: {input_path}")

    return images