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