from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.ui_constants import (
    SUPPORTED_IMAGE_FILE_TYPES,
    SUPPORTED_IMAGE_FORMATS_TEXT,
    UPLOAD_LABEL,
)


def build_upload_panel(
    *,
    title: str = "Upload images",
    container_classes: list[str] | None = None,
    files_classes: list[str] | None = None,
) -> dict[str, Any]:
    """Build a reusable image upload panel."""
    with gr.Group(elem_classes=container_classes or ["cia-card"]) as upload_group:
        gr.Markdown(f"### {title}")
        batch_files = gr.Files(
            label=UPLOAD_LABEL,
            file_types=SUPPORTED_IMAGE_FILE_TYPES,
            elem_classes=files_classes or ["cia-upload-dropzone"],
        )
        gr.Markdown(
            SUPPORTED_IMAGE_FORMATS_TEXT,
            elem_classes=["cia-muted"],
        )

    return {
        "upload_group": upload_group,
        "batch_files": batch_files,
    }


def build_initial_upload_panel() -> dict[str, Any]:
    """Build the initial upload screen shown before images are loaded."""
    return build_upload_panel(
        container_classes=["cia-card", "cia-initial-upload-card"],
        files_classes=["cia-upload-dropzone"],
    )


def build_side_upload_panel() -> dict[str, Any]:
    """Build the upload panel shown beside metadata after images are loaded."""
    from src.webapp.ui_constants import RIGHT_COLUMN_MIN_WIDTH, RIGHT_COLUMN_SCALE

    with gr.Column(scale=RIGHT_COLUMN_SCALE, min_width=RIGHT_COLUMN_MIN_WIDTH):
        upload_components = build_upload_panel(
            container_classes=["cia-card", "cia-upload-panel", "cia-bottom-panel"],
            files_classes=["cia-upload-dropzone"],
        )

    return {
        "side_upload_group": upload_components["upload_group"],
        "side_batch_files": upload_components["batch_files"],
    }
