from pathlib import Path

from PIL import Image


def inspect_image_metadata(image_path: str | Path) -> dict[str, str]:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    with Image.open(path) as image:
        metadata = {
            "format": str(image.format),
            "mode": str(image.mode),
            "width": str(image.width),
            "height": str(image.height),
        }

        for key, value in image.info.items():
            metadata[str(key)] = str(value)

        exif = image.getexif()
        for key, value in exif.items():
            metadata[f"exif:{key}"] = str(value)

    return metadata


def preview_anonymized_metadata(image_path: str | Path) -> dict[str, str]:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    with Image.open(path) as image:
        return {
            "format": str(image.format),
            "mode": str(image.mode),
            "width": str(image.width),
            "height": str(image.height),
        }


def remove_image_metadata(input_path: str | Path, output_path: str | Path) -> Path:
    source = Path(input_path)
    destination = Path(output_path)

    if not source.exists():
        raise FileNotFoundError(f"Image not found: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as image:
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(list(image.getdata()))
        clean_image.save(destination, format=image.format)

    return destination