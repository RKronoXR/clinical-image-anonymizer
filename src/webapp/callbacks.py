from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

from src.anonymization.metadata import inspect_image_metadata


def get_uploaded_file_path(file: Any) -> str | None:
    if file is None:
        return None
    if isinstance(file, str):
        return file
    if isinstance(file, list) and file:
        return get_uploaded_file_path(file[0])
    if isinstance(file, dict):
        return file.get("path") or file.get("name")
    if hasattr(file, "path"):
        return str(file.path)
    if hasattr(file, "name"):
        return str(file.name)
    return None


def get_uploaded_file_paths(files: Any) -> list[str]:
    if not files:
        return []
    if not isinstance(files, list):
        files = [files]

    return [
        path
        for file in files
        if (path := get_uploaded_file_path(file)) is not None
    ]


def preview_uploaded_image(file: Any):
    file_path = get_uploaded_file_path(file)
    if file_path is None:
        return None

    with Image.open(file_path) as image:
        image = ImageOps.exif_transpose(image)
        image.load()
        return image.convert("RGB")


def inspect_uploaded_image(file: Any) -> str:
    file_path = get_uploaded_file_path(file)
    if file_path is None:
        return "No image loaded."

    try:
        metadata = inspect_image_metadata(Path(file_path))
        return json.dumps(metadata, indent=4, ensure_ascii=False, default=str)
    except Exception as exc:
        return json.dumps({"error": str(exc)}, indent=4, ensure_ascii=False)


def inspect_uploaded_batch(files: Any) -> str:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return "<p>No batch files selected.</p>"

    sections: list[str] = []

    for index, file_path in enumerate(file_paths, start=1):
        file_name = Path(file_path).name

        try:
            metadata = inspect_image_metadata(Path(file_path))
            content = json.dumps(metadata, indent=4, ensure_ascii=False, default=str)
        except Exception as exc:
            content = json.dumps({"error": str(exc)}, indent=4, ensure_ascii=False)

        sections.append(
            f"""
            <details>
                <summary><strong>{index}. {html.escape(file_name)}</strong></summary>
                <pre>{html.escape(content)}</pre>
            </details>
            """
        )

    return "\n".join(sections)