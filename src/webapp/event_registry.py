from __future__ import annotations

from collections.abc import Callable
from typing import Any

import gradio as gr

from src.webapp.rectangle_state import get_rectangle_values


NAVIGATION_DIRECTIONS = {
    "first_button": "first",
    "previous_button": "previous",
    "next_button": "next",
    "last_button": "last",
}


def _workspace_upload_inputs(components: dict[str, Any], file_component: Any) -> list[Any]:
    return [
        file_component,
        components["show_grid_checkbox"],
        components["grid_size_input"],
        components["grid_label_size_input"],
    ]


def _workspace_upload_outputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["files_state"],
        components["rectangle_state"],
        components["batch_index_state"],
        components["initial_upload_group"],
        components["export_group"],
        components["viewer_group"],
        components["current_metadata_html"],
        components["rectangle_selector"],
        components["x_input"],
        components["y_input"],
        components["width_input"],
        components["height_input"],
        components["rectangles_json"],
        components["original_preview"],
        components["overlay_preview"],
        components["anonymized_preview"],
        components["batch_position"],
        components["side_batch_files"],
    ]


def _navigation_inputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["files_state"],
        components["batch_index_state"],
        components["rectangle_state"],
        components["show_grid_checkbox"],
        components["grid_size_input"],
        components["grid_label_size_input"],
    ]


def _navigation_outputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["batch_index_state"],
        components["original_preview"],
        components["overlay_preview"],
        components["anonymized_preview"],
        components["current_metadata_html"],
        components["batch_position"],
    ]


def _grid_inputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["files_state"],
        components["batch_index_state"],
        components["rectangle_state"],
        components["show_grid_checkbox"],
        components["grid_size_input"],
        components["grid_label_size_input"],
    ]


def _preview_outputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["original_preview"],
        components["overlay_preview"],
        components["anonymized_preview"],
    ]


def _add_rectangle_inputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["rectangle_state"],
        components["files_state"],
        components["batch_index_state"],
        components["show_grid_checkbox"],
        components["grid_size_input"],
        components["grid_label_size_input"],
    ]


def _add_rectangle_outputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["rectangle_state"],
        components["rectangle_selector"],
        components["rectangles_json"],
        components["original_preview"],
        components["overlay_preview"],
        components["anonymized_preview"],
        components["image_tabs"],
    ]


def _update_rectangle_inputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["rectangle_state"],
        components["rectangle_selector"],
        components["x_input"],
        components["y_input"],
        components["width_input"],
        components["height_input"],
        components["files_state"],
        components["batch_index_state"],
        components["show_grid_checkbox"],
        components["grid_size_input"],
        components["grid_label_size_input"],
    ]


def _update_rectangle_outputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["rectangle_state"],
        components["rectangles_json"],
        components["original_preview"],
        components["overlay_preview"],
        components["anonymized_preview"],
    ]


def _delete_rectangle_inputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["rectangle_state"],
        components["rectangle_selector"],
        components["files_state"],
        components["batch_index_state"],
        components["show_grid_checkbox"],
        components["grid_size_input"],
        components["grid_label_size_input"],
    ]


def _delete_rectangle_outputs(components: dict[str, Any]) -> list[Any]:
    return [
        components["rectangle_state"],
        components["rectangle_selector"],
        components["x_input"],
        components["y_input"],
        components["width_input"],
        components["height_input"],
        components["rectangles_json"],
        components["original_preview"],
        components["overlay_preview"],
        components["anonymized_preview"],
    ]


def register_callbacks(
    *,
    components: dict[str, Any],
    handle_workspace_upload: Callable[..., Any],
    navigate_batch: Callable[..., Any],
    handle_grid_change: Callable[..., Any],
    handle_add_rectangle: Callable[..., Any],
    handle_update_rectangle: Callable[..., Any],
    handle_delete_rectangle: Callable[..., Any],
) -> None:
    """Wire Gradio UI events without owning callback implementation logic."""
    for file_component in (
        components["initial_batch_files"],
        components["side_batch_files"],
    ):
        file_component.change(
            fn=handle_workspace_upload,
            inputs=_workspace_upload_inputs(components, file_component),
            outputs=_workspace_upload_outputs(components),
        )

    for button_key, direction in NAVIGATION_DIRECTIONS.items():
        components[button_key].click(
            fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size, direction=direction: navigate_batch(
                files,
                index,
                direction,
                rectangles,
                show_grid,
                grid_size,
                grid_label_size,
            ),
            inputs=_navigation_inputs(components),
            outputs=_navigation_outputs(components),
        )

    components["show_grid_checkbox"].change(
        fn=handle_grid_change,
        inputs=_grid_inputs(components),
        outputs=_preview_outputs(components),
    ).then(
        fn=lambda: gr.update(selected="overlay"),
        inputs=None,
        outputs=components["image_tabs"],
    )

    for grid_component_key in ("grid_size_input", "grid_label_size_input"):
        components[grid_component_key].change(
            fn=handle_grid_change,
            inputs=_grid_inputs(components),
            outputs=_preview_outputs(components),
        )

    components["add_rectangle_button"].click(
        fn=handle_add_rectangle,
        inputs=_add_rectangle_inputs(components),
        outputs=_add_rectangle_outputs(components),
    )

    components["rectangle_selector"].change(
        fn=get_rectangle_values,
        inputs=[components["rectangle_state"], components["rectangle_selector"]],
        outputs=[
            components["x_input"],
            components["y_input"],
            components["width_input"],
            components["height_input"],
        ],
    )

    components["update_rectangle_button"].click(
        fn=handle_update_rectangle,
        inputs=_update_rectangle_inputs(components),
        outputs=_update_rectangle_outputs(components),
    )

    components["delete_rectangle_button"].click(
        fn=handle_delete_rectangle,
        inputs=_delete_rectangle_inputs(components),
        outputs=_delete_rectangle_outputs(components),
    )
