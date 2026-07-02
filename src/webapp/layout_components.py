from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.panels.export_panel import build_export_panel
from src.webapp.panels.metadata_panel import build_metadata_panel
from src.webapp.panels.rectangle_panel import build_rectangle_panel
from src.webapp.panels.upload_panel import (
    build_initial_upload_panel,
    build_side_upload_panel,
)
from src.webapp.panels.viewer_panel import build_image_viewer_panel


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
