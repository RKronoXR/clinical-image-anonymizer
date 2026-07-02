from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.rectangle_state import (
    DEFAULT_RECTANGLE_HEIGHT,
    DEFAULT_RECTANGLE_WIDTH,
)
from src.webapp.ui_constants import (
    DEFAULT_GRID_LABEL_SIZE,
    DEFAULT_GRID_SIZE,
    EXPORT_BUTTON_SCALE,
    EXPORT_NAME_PREFIX_DEFAULT,
    EXPORT_NAME_PREFIX_SCALE,
    EXPORT_OUTPUT_FOLDER_DEFAULT,
    EXPORT_OUTPUT_FOLDER_SCALE,
    EXPORT_RANDOMIZE_ORDER_SCALE,
    GRID_LABEL_SIZE_PRECISION,
    GRID_SIZE_PRECISION,
    LEFT_COLUMN_MIN_WIDTH,
    LEFT_COLUMN_SCALE,
    RECTANGLE_BUTTON_SCALE,
    RECTANGLE_INPUT_PRECISION,
    RIGHT_COLUMN_MIN_WIDTH,
    RIGHT_COLUMN_SCALE,
    SUPPORTED_IMAGE_FILE_TYPES,
    SUPPORTED_IMAGE_FORMATS_TEXT,
    UPLOAD_LABEL,
    VIEWER_IMAGE_HEIGHT,
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


def build_export_panel() -> dict[str, Any]:
    """Build the export controls panel."""
    with gr.Group(visible=False, elem_classes=["cia-card"]) as export_group:
        with gr.Row(equal_height=True):
            export_output_folder = gr.Textbox(
                label="Output folder",
                value=EXPORT_OUTPUT_FOLDER_DEFAULT,
                interactive=True,
                scale=EXPORT_OUTPUT_FOLDER_SCALE,
            )

            export_name_prefix = gr.Textbox(
                label="Output filename prefix",
                value=EXPORT_NAME_PREFIX_DEFAULT,
                interactive=True,
                scale=EXPORT_NAME_PREFIX_SCALE,
            )

            export_randomize_order = gr.Checkbox(
                label="Randomize output image order",
                value=False,
                scale=EXPORT_RANDOMIZE_ORDER_SCALE,
            )

            export_button = gr.Button(
                value="Export anonymized images",
                scale=EXPORT_BUTTON_SCALE,
                variant="secondary",
                elem_classes=["cia-primary-action"],
            )

            gr.HTML(
                """
                <div class="cia-export-status">
                    <span class="cia-muted">Export status</span>
                    <strong>✓ Ready to export</strong>
                </div>
                """,
            )

    return {
        "export_group": export_group,
        "export_output_folder": export_output_folder,
        "export_name_prefix": export_name_prefix,
        "export_randomize_order": export_randomize_order,
        "export_button": export_button,
    }


def build_image_viewer_panel(
    *,
    initial_batch_status_html: str,
) -> dict[str, Any]:
    """Build image preview tabs, navigation, and grid controls."""
    with gr.Column(scale=LEFT_COLUMN_SCALE, min_width=LEFT_COLUMN_MIN_WIDTH):
        with gr.Group(elem_classes=["cia-card", "cia-top-panel"]):
            with gr.Tabs(selected="original", elem_classes=["cia-image-tabs"]) as image_tabs:
                with gr.Tab("Original", id="original"):
                    original_preview = gr.Image(
                        label="Current image",
                        interactive=False,
                        height=VIEWER_IMAGE_HEIGHT,
                    )

                with gr.Tab("Overlay", id="overlay"):
                    overlay_preview = gr.Image(
                        label="Rectangle overlay preview",
                        interactive=False,
                        height=VIEWER_IMAGE_HEIGHT,
                    )

                with gr.Tab("Anonymized", id="anonymized"):
                    anonymized_preview = gr.Image(
                        label="Anonymized preview",
                        interactive=False,
                        height=VIEWER_IMAGE_HEIGHT,
                    )

            with gr.Row(equal_height=True):
                first_button = gr.Button(value="First")
                previous_button = gr.Button(value="Previous")
                batch_position = gr.Markdown(value=initial_batch_status_html)
                next_button = gr.Button(value="Next")
                last_button = gr.Button(value="Last")

            with gr.Group(elem_classes=["cia-tight-card"]):
                show_grid_checkbox = gr.Checkbox(
                    label="Show pixel grid in Overlay",
                    value=False,
                )

                with gr.Row(equal_height=True):
                    grid_size_input = gr.Number(
                        label="Grid square size in pixels",
                        value=DEFAULT_GRID_SIZE,
                        precision=GRID_SIZE_PRECISION,
                        scale=1,
                    )
                    grid_label_size_input = gr.Number(
                        label="Grid number size",
                        value=DEFAULT_GRID_LABEL_SIZE,
                        precision=GRID_LABEL_SIZE_PRECISION,
                        scale=1,
                    )

    return {
        "image_tabs": image_tabs,
        "original_preview": original_preview,
        "overlay_preview": overlay_preview,
        "anonymized_preview": anonymized_preview,
        "first_button": first_button,
        "previous_button": previous_button,
        "batch_position": batch_position,
        "next_button": next_button,
        "last_button": last_button,
        "show_grid_checkbox": show_grid_checkbox,
        "grid_size_input": grid_size_input,
        "grid_label_size_input": grid_label_size_input,
    }


def build_rectangle_panel() -> dict[str, Any]:
    """Build global rectangle controls."""
    with gr.Column(scale=RIGHT_COLUMN_SCALE, min_width=RIGHT_COLUMN_MIN_WIDTH, elem_classes=["cia-right-column"]):
        with gr.Group(elem_classes=["cia-card", "cia-top-panel"]):
            with gr.Row(equal_height=True):
                gr.Markdown(
                    "### Rectangles <span class='cia-muted'>(global for all images)</span>"
                )
                add_rectangle_button = gr.Button(
                    value="Add rectangle",
                    variant="secondary",
                    scale=RECTANGLE_BUTTON_SCALE,
                    elem_classes=["cia-primary-action"],
                )

            rectangle_selector = gr.Dropdown(
                label="Selected rectangle",
                choices=[],
                value=None,
                interactive=True,
            )

            with gr.Row(equal_height=True):
                x_input = gr.Number(label="X", value=0, precision=RECTANGLE_INPUT_PRECISION)
                y_input = gr.Number(label="Y", value=0, precision=RECTANGLE_INPUT_PRECISION)

            with gr.Row(equal_height=True):
                width_input = gr.Number(
                    label="W",
                    value=DEFAULT_RECTANGLE_WIDTH,
                    precision=RECTANGLE_INPUT_PRECISION,
                )

                height_input = gr.Number(
                    label="H",
                    value=DEFAULT_RECTANGLE_HEIGHT,
                    precision=RECTANGLE_INPUT_PRECISION,
                )

            update_rectangle_button = gr.Button(
                value="Update selected rectangle",
                variant="secondary",
                elem_classes=["cia-primary-action"],
            )
            delete_rectangle_button = gr.Button(value="Delete selected rectangle")

            rectangles_json = gr.Code(
                label="Rectangle coordinates",
                language="json",
                interactive=False,
                value="[]",
                elem_classes=["cia-json-card"],
            )

    return {
        "add_rectangle_button": add_rectangle_button,
        "delete_rectangle_button": delete_rectangle_button,
        "rectangle_selector": rectangle_selector,
        "x_input": x_input,
        "y_input": y_input,
        "width_input": width_input,
        "height_input": height_input,
        "update_rectangle_button": update_rectangle_button,
        "rectangles_json": rectangles_json,
    }


def build_metadata_panel() -> dict[str, Any]:
    """Build the current image metadata panel."""
    with gr.Column(scale=LEFT_COLUMN_SCALE, min_width=LEFT_COLUMN_MIN_WIDTH):
        current_metadata_html = gr.HTML(
            label="Current image metadata",
            visible=False,
            elem_classes=["cia-card", "cia-bottom-panel"],
        )

    return {
        "current_metadata_html": current_metadata_html,
    }


def build_side_upload_panel() -> dict[str, Any]:
    """Build the upload panel shown beside metadata after images are loaded."""
    with gr.Column(scale=RIGHT_COLUMN_SCALE, min_width=RIGHT_COLUMN_MIN_WIDTH):
        upload_components = build_upload_panel(
            container_classes=["cia-card", "cia-upload-panel", "cia-bottom-panel"],
            files_classes=["cia-upload-dropzone"],
        )

    return {
        "side_upload_group": upload_components["upload_group"],
        "side_batch_files": upload_components["batch_files"],
    }


def build_viewer_workspace(
    *,
    initial_batch_status_html: str,
) -> dict[str, Any]:
    """Build the main workspace shown after images are loaded."""
    components: dict[str, Any] = {}

    with gr.Group(visible=False) as viewer_group:
        with gr.Row(equal_height=False):
            components.update(
                build_image_viewer_panel(
                    initial_batch_status_html=initial_batch_status_html,
                )
            )
            components.update(build_rectangle_panel())

        with gr.Row(equal_height=False):
            components.update(build_metadata_panel())
            components.update(build_side_upload_panel())

    components["viewer_group"] = viewer_group
    return components
