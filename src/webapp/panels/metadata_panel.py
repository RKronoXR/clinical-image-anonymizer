from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.ui_constants import LEFT_COLUMN_MIN_WIDTH, LEFT_COLUMN_SCALE


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
