from __future__ import annotations

import gradio as gr

from src.webapp.app import build_app
from src.webapp.layout import build_main_layout


EXPECTED_LAYOUT_KEYS = {
    "files_state",
    "initial_batch_files",
    "side_batch_files",
    "export_group",
    "viewer_group",
    "batch_index_state",
    "original_preview",
    "overlay_preview",
    "anonymized_preview",
    "batch_position",
    "current_metadata_html",
    "rectangle_state",
    "add_rectangle_button",
    "delete_rectangle_button",
    "rectangle_selector",
    "x_input",
    "y_input",
    "width_input",
    "height_input",
    "update_rectangle_button",
    "show_grid_checkbox",
    "grid_size_input",
    "grid_label_size_input",
    "rectangles_json",
    "export_output_folder",
    "export_name_prefix",
    "export_randomize_order",
    "export_button",
}


def test_build_app_returns_gradio_blocks() -> None:
    """The Gradio app should build without launching a server."""
    app = build_app()

    assert isinstance(app, gr.Blocks)



def test_build_main_layout_returns_expected_components() -> None:
    """The main layout should expose the components required by event wiring."""
    with gr.Blocks():
        components = build_main_layout()

    assert isinstance(components, dict)
    assert EXPECTED_LAYOUT_KEYS.issubset(components.keys())



def test_core_webapp_components_are_present() -> None:
    """Smoke check for the main UI sections without using private images."""
    with gr.Blocks():
        components = build_main_layout()

    assert components["initial_batch_files"] is not None
    assert components["side_batch_files"] is not None
    assert components["export_group"] is not None
    assert components["viewer_group"] is not None
    assert components["current_metadata_html"] is not None
    assert components["rectangle_selector"] is not None
    assert components["rectangles_json"] is not None
