from __future__ import annotations

from pathlib import Path

from PIL import Image


def safe_output_format(
    source: Path,
    image_format: str | None,
) -> str | None:
    suffix = source.suffix.lower()

    if suffix in {".jpg", ".jpeg"}:
        return "JPEG"

    if suffix in {".tif", ".tiff"}:
        return "TIFF"

    if suffix == ".png":
        return "PNG"

    return image_format


def save_without_metadata(
    image: Image.Image,
    destination: Path,
    image_format: str | None,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    clean_image = image.convert("RGB")

    save_kwargs: dict = {}

    if image_format == "JPEG":
        save_kwargs["quality"] = 95
        save_kwargs["optimize"] = True

    elif image_format == "PNG":
        save_kwargs["optimize"] = True

    elif image_format == "TIFF":
        save_kwargs["compression"] = "raw"

    clean_image.save(
        destination,
        format=image_format,
        **save_kwargs,
    )