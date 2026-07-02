from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from src.anonymization.export import export_anonymized_images
from src.anonymization.metadata import (
    inspect_image_metadata,
    preview_anonymized_metadata,
)
from src.webapp.preview_rendering import (
    load_preview_image,
    render_censored_preview,
    render_overlay_preview,
)


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
    return load_preview_image(file_path)


def preview_all_single_views(file: Any, rectangles: list[dict] | None):
    file_path = get_uploaded_file_path(file)

    return (
        load_preview_image(file_path),
        render_overlay_preview(file_path, rectangles),
        render_censored_preview(file_path, rectangles),
    )


def inspect_uploaded_image(file: Any) -> str:
    file_path = get_uploaded_file_path(file)
    if file_path is None:
        return "No image loaded."

    try:
        metadata = inspect_image_metadata(Path(file_path))
        return json.dumps(metadata, indent=4, ensure_ascii=False, default=str)
    except Exception as exc:
        return json.dumps({"error": str(exc)}, indent=4, ensure_ascii=False)


def _format_metadata_block(title: str, metadata: dict[str, str]) -> str:
    content = json.dumps(metadata, indent=4, ensure_ascii=False, default=str)
    technical_note = """
        <div style="
            margin-top:6px;
            padding:6px 8px;
            border-left:3px solid #5aa9e6;
            background:rgba(90, 169, 230, 0.12);
            border-radius:4px;
            font-size:12px;
            line-height:1.25;
        ">
            <strong>ℹ Technical note:</strong>
            exported formats such as JPEG, TIFF, or PNG may add technical format metadata.
            These fields do not contain patient-identifying information.
        </div>
    """ if title == "Anonymized Metadata" else ""

    return f"""
    <div style="width:50%; padding:8px;">
        <h4>{html.escape(title)}</h4>
        <pre style="white-space:pre-wrap;">{html.escape(content)}</pre>
        {technical_note}
    </div>
    """


def inspect_current_uploaded_image_html(
    files: Any,
    index: int | float | None,
) -> str:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return "<p>No image loaded.</p>"

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    file_path = file_paths[safe_index]
    file_name = Path(file_path).name

    try:
        original_metadata = inspect_image_metadata(Path(file_path))
    except Exception as exc:
        original_metadata = {"error": str(exc)}

    try:
        anonymized_metadata = preview_anonymized_metadata(Path(file_path))
    except Exception as exc:
        anonymized_metadata = {"error": str(exc)}

    return f"""
    <h3>Metadata: {html.escape(file_name)}</h3>
    <div style="display:flex; gap:12px; align-items:flex-start;">
        {_format_metadata_block("Original Metadata", original_metadata)}
        {_format_metadata_block("Anonymized Metadata", anonymized_metadata)}
    </div>
    """


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


def format_export_status(message: str, is_error: bool = False) -> str:
    color = "#ff6666" if is_error else "#43d17a"
    symbol = "✗" if is_error else "✓"
    return f"""
    <div class="cia-export-status">
        <span class="cia-muted">Export status</span>
        <strong style="color:{color};">{symbol} {html.escape(message)}</strong>
    </div>
    """


def handle_export_batch(
    files: Any,
    rectangles: list[dict] | None,
    output_folder: str,
    prefix: str,
    randomize: bool,
) -> str:
    file_paths = get_uploaded_file_paths(files)

    if not file_paths:
        return format_export_status("No images loaded.", is_error=True)

    if not output_folder or not str(output_folder).strip():
        return format_export_status("Output folder is required.", is_error=True)

    try:
        exported = export_anonymized_images(
            image_paths=file_paths,
            output_dir=Path(output_folder),
            rectangles=rectangles or [],
            prefix=prefix or "",
            randomize=bool(randomize),
        )

        return format_export_status(
            f"Export completed successfully. {len(exported)} images exported.",
            is_error=False,
        )

    except Exception as exc:
        return format_export_status(str(exc), is_error=True)
