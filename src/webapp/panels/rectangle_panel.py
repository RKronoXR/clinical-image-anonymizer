from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.rectangle_state import (
    DEFAULT_RECTANGLE_HEIGHT,
    DEFAULT_RECTANGLE_WIDTH,
)
from src.webapp.ui_constants import (
    RECTANGLE_BUTTON_SCALE,
    RECTANGLE_INPUT_PRECISION,
    RIGHT_COLUMN_MIN_WIDTH,
    RIGHT_COLUMN_SCALE,
)


def build_rectangle_panel() -> dict[str, Any]:
    """Build rectangle controls."""
    with gr.Column(
        scale=RIGHT_COLUMN_SCALE,
        min_width=RIGHT_COLUMN_MIN_WIDTH,
        elem_classes=["cia-right-column"],
    ):
        with gr.Group(elem_classes=["cia-card", "cia-top-panel"]):
            with gr.Row(equal_height=True):
                gr.Markdown("### Rectangles")
                add_rectangle_button = gr.Button(
                    value="Add rectangle",
                    variant="secondary",
                    scale=RECTANGLE_BUTTON_SCALE,
                    elem_classes=["cia-primary-action"],
                )

            with gr.Row(equal_height=True):
                rectangle_selector = gr.Dropdown(
                    label="Selected rectangle",
                    choices=[],
                    value=None,
                    interactive=True,
                    scale=2,
                )
                apply_all_images_checkbox = gr.Checkbox(
                    label="Apply to all images",
                    value=True,
                    interactive=True,
                    scale=1,
                )

            with gr.Row(equal_height=True):
                x_input = gr.Number(label="X", value=0, precision=RECTANGLE_INPUT_PRECISION)
                y_input = gr.Number(label="Y", value=0, precision=RECTANGLE_INPUT_PRECISION)

            with gr.Row(equal_height=True):
                width_input = gr.Number(
                    label="Width",
                    value=DEFAULT_RECTANGLE_WIDTH,
                    precision=RECTANGLE_INPUT_PRECISION,
                )

                height_input = gr.Number(
                    label="Height",
                    value=DEFAULT_RECTANGLE_HEIGHT,
                    precision=RECTANGLE_INPUT_PRECISION,
                )

            with gr.Row(equal_height=True):
                update_rectangle_button = gr.Button(
                    value="Update selected rectangle",
                    variant="secondary",
                    elem_classes=["cia-primary-action"],
                )
                delete_rectangle_button = gr.Button(
                    value="Delete selected rectangle",
                    variant="secondary",
                )

            rectangles_json = gr.Code(
                label="Rectangle coordinates",
                language="json",
                interactive=False,
                value="[]",
                lines=16,
                elem_classes=["cia-json-card"],
            )

    return {
        "add_rectangle_button": add_rectangle_button,
        "delete_rectangle_button": delete_rectangle_button,
        "rectangle_selector": rectangle_selector,
        "apply_all_images_checkbox": apply_all_images_checkbox,
        "x_input": x_input,
        "y_input": y_input,
        "width_input": width_input,
        "height_input": height_input,
        "update_rectangle_button": update_rectangle_button,
        "rectangles_json": rectangles_json,
    }
