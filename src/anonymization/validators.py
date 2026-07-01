from pathlib import Path

from src.anonymization.image_io import SUPPORTED_IMAGE_EXTENSIONS


def validate_input_path(path: str | Path) -> Path:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")

    return path


def validate_output_directory(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_image_extension(path: str | Path) -> Path:
    path = Path(path)

    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(
            f"Unsupported image extension: {path.suffix}"
        )

    return path


def validate_non_empty_batch(image_paths: list[Path]) -> None:
    if not image_paths:
        raise ValueError("Image batch is empty.")