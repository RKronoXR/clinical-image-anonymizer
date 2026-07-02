from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.ui_constants import (
    DEFAULT_GRID_LABEL_SIZE,
    DEFAULT_GRID_SIZE,
    GRID_LABEL_SIZE_PRECISION,
    GRID_SIZE_PRECISION,
    LEFT_COLUMN_MIN_WIDTH,
    LEFT_COLUMN_SCALE,
    VIEWER_IMAGE_HEIGHT,
)


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

                with gr.Tab("Anonymized", id="anonymized"):
                    anonymized_preview = gr.Image(
                        label="Anonymized preview",
                        interactive=False,
                        height=VIEWER_IMAGE_HEIGHT,
                    )

            with gr.Row(equal_height=True):
                first_button = gr.Button(value="First", interactive=False)
                previous_button = gr.Button(value="Previous", interactive=False)
                batch_position = gr.Markdown(value=initial_batch_status_html)
                next_button = gr.Button(value="Next", interactive=False)
                last_button = gr.Button(value="Last", interactive=False)

            with gr.Group(elem_classes=["cia-tight-card"]):
                show_grid_checkbox = gr.Checkbox(
                    label="Show pixel grid",
                    value=False,
                )

                with gr.Row(equal_height=True):
                    gr.HTML(
                        "<div class='cia-inline-grid-label'>Grid square size in pixels</div>",
                    )

                    grid_size_input = gr.Number(
                        label="Grid square size in pixels",
                        value=DEFAULT_GRID_SIZE,
                        precision=GRID_SIZE_PRECISION,
                        interactive=False,
                        show_label=False,
                        scale=2,
                    )

                    gr.HTML(
                        "<div class='cia-inline-grid-label'>Grid number size</div>",
                    )

                    grid_label_size_input = gr.Number(
                        label="Grid number size",
                        value=DEFAULT_GRID_LABEL_SIZE,
                        precision=GRID_LABEL_SIZE_PRECISION,
                        interactive=False,
                        show_label=False,
                        scale=2,
                    )

                    update_grid_button = gr.Button(
                        value="Apply grid",
                        interactive=False,
                        scale=1,
                    )

    return {
        "image_tabs": image_tabs,
        "original_preview": original_preview,
        "overlay_preview": original_preview,
        "anonymized_preview": anonymized_preview,
        "first_button": first_button,
        "previous_button": previous_button,
        "batch_position": batch_position,
        "next_button": next_button,
        "last_button": last_button,
        "show_grid_checkbox": show_grid_checkbox,
        "grid_size_input": grid_size_input,
        "grid_label_size_input": grid_label_size_input,
        "update_grid_button": update_grid_button,
    }
