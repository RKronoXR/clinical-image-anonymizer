from collections import Counter
from pathlib import Path

from PIL import Image

from src.anonymization.image_io import validate_supported_image_path


def inspect_batch_dimensions(image_paths: list[str | Path]) -> dict[Path, tuple[int, int]]:
    dimensions = {}

    for image_path in image_paths:
        path = validate_supported_image_path(image_path)

        with Image.open(path) as image:
            dimensions[path] = image.size

    return dimensions


def all_images_same_size(
    dimensions: dict[Path, tuple[int, int]],
) -> bool:
    return len(set(dimensions.values())) <= 1


def batch_dimension_summary(
    dimensions: dict[Path, tuple[int, int]],
) -> dict[tuple[int, int], int]:
    return dict(Counter(dimensions.values()))