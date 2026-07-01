from __future__ import annotations

import json

from src.anonymization.metadata import inspect_image_metadata


def inspect_uploaded_image(image) -> str:
    """
    Returns formatted metadata for the uploaded image.
    """

    if image is None:
        return "No image loaded."

    metadata = inspect_image_metadata(image)

    return json.dumps(
        metadata,
        indent=4,
        ensure_ascii=False,
        default=str,
    )