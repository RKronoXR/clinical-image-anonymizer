from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.ui_constants import (
    EXPORT_BUTTON_SCALE,
    EXPORT_NAME_PREFIX_DEFAULT,
    EXPORT_NAME_PREFIX_SCALE,
    EXPORT_OUTPUT_FOLDER_DEFAULT,
    EXPORT_OUTPUT_FOLDER_SCALE,
    EXPORT_RANDOMIZE_ORDER_SCALE,
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
