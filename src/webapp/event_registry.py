from __future__ import annotations

from collections.abc import Callable
from typing import Any

import gradio as gr

from src.webapp.ui_components import UIComponents


NAVIGATION_DIRECTIONS = {
    "first_button": "first",
    "previous_button": "previous",
    "next_button": "next",
    "last_button": "last",
}


def _workspace_upload_inputs(components: UIComponents, file_component: Any) -> list[Any]:
    return [
        file_component,
        components.state.rectangle_state,
        components.state.batch_index_state,
        components.viewer.show_grid_checkbox,
        components.viewer.grid_size_input,
        components.viewer.grid_label_size_input,
    ]


def _workspace_upload_outputs(
    components: UIComponents,
    *,
    include_side_upload: bool,
) -> list[Any]:
    outputs = [
        components.state.files_state,
        components.state.rectangle_state,
        components.state.batch_index_state,
        components.upload.initial_upload_group,
        components.export.export_group,
        components.viewer.viewer_group,
        components.metadata.current_metadata_html,
        components.rectangle.rectangle_selector,
        components.rectangle.apply_all_images_checkbox,
        components.rectangle.x_input,
        components.rectangle.y_input,
        components.rectangle.width_input,
        components.rectangle.height_input,
        components.rectangle.rectangles_json,
        *components.viewer.preview_outputs,
        components.viewer.batch_position,
        *components.viewer.navigation_buttons,
    ]

    if include_side_upload:
        outputs.append(components.upload.side_batch_files)

    outputs.extend(components.rectangle.selection_buttons)
    return outputs


def _clear_upload_outputs(
    components: UIComponents,
    *,
    include_side_upload: bool,
) -> list[Any]:
    outputs = [
        components.state.files_state,
        components.state.rectangle_state,
        components.state.batch_index_state,
        components.upload.initial_upload_group,
        components.export.export_group,
        components.viewer.viewer_group,
        components.metadata.current_metadata_html,
        components.rectangle.rectangle_selector,
        components.rectangle.apply_all_images_checkbox,
        components.rectangle.x_input,
        components.rectangle.y_input,
        components.rectangle.width_input,
        components.rectangle.height_input,
        components.rectangle.rectangles_json,
        *components.viewer.preview_outputs,
        components.viewer.batch_position,
        *components.viewer.navigation_buttons,
        components.upload.initial_batch_files,
    ]

    if include_side_upload:
        outputs.append(components.upload.side_batch_files)

    outputs.extend(components.rectangle.selection_buttons)
    return outputs


def _drop_side_upload_from_workspace_result(result: Any) -> tuple[Any, ...]:
    values = tuple(result)
    return values[:-3] + values[-2:]


def _drop_side_upload_from_clear_result(result: Any) -> tuple[Any, ...]:
    values = tuple(result)
    return values[:-3] + values[-2:]


def _shared_preview_inputs(components: UIComponents) -> list[Any]:
    return [
        components.state.files_state,
        components.state.batch_index_state,
        components.state.rectangle_state,
        components.viewer.show_grid_checkbox,
        components.viewer.grid_size_input,
        components.viewer.grid_label_size_input,
    ]


def _navigation_outputs(components: UIComponents) -> list[Any]:
    return [
        components.state.batch_index_state,
        *components.viewer.preview_outputs,
        components.metadata.current_metadata_html,
        components.viewer.batch_position,
        *components.viewer.navigation_buttons,
    ]


def _add_rectangle_inputs(components: UIComponents) -> list[Any]:
    return [
        components.state.rectangle_state,
        *components.rectangle.coordinate_inputs,
        components.rectangle.apply_all_images_checkbox,
        components.state.files_state,
        components.state.batch_index_state,
        components.viewer.show_grid_checkbox,
        components.viewer.grid_size_input,
        components.viewer.grid_label_size_input,
    ]


def _add_rectangle_outputs(components: UIComponents) -> list[Any]:
    return [
        components.state.rectangle_state,
        components.rectangle.rectangle_selector,
        components.rectangle.rectangles_json,
        *components.viewer.preview_outputs,
        components.viewer.image_tabs,
        *components.rectangle.selection_buttons,
    ]


def _update_rectangle_inputs(components: UIComponents) -> list[Any]:
    return [
        components.state.rectangle_state,
        components.rectangle.rectangle_selector,
        *components.rectangle.coordinate_inputs,
        components.state.files_state,
        components.state.batch_index_state,
        components.viewer.show_grid_checkbox,
        components.viewer.grid_size_input,
        components.viewer.grid_label_size_input,
    ]


def _update_rectangle_outputs(components: UIComponents) -> list[Any]:
    return [
        components.state.rectangle_state,
        components.rectangle.rectangles_json,
        *components.viewer.preview_outputs,
    ]


def _delete_rectangle_inputs(components: UIComponents) -> list[Any]:
    return [
        components.state.rectangle_state,
        components.rectangle.rectangle_selector,
        components.state.files_state,
        components.state.batch_index_state,
        components.viewer.show_grid_checkbox,
        components.viewer.grid_size_input,
        components.viewer.grid_label_size_input,
    ]


def _delete_rectangle_outputs(components: UIComponents) -> list[Any]:
    return [
        components.state.rectangle_state,
        components.rectangle.rectangle_selector,
        *components.rectangle.coordinate_inputs,
        components.rectangle.rectangles_json,
        *components.viewer.preview_outputs,
        *components.rectangle.selection_buttons,
    ]


def _navigation_button(components: UIComponents, button_key: str) -> Any:
    return getattr(components.viewer, button_key)


def register_callbacks(
    *,
    components: UIComponents,
    handle_workspace_upload: Callable[..., Any],
    navigate_batch: Callable[..., Any],
    handle_grid_change: Callable[..., Any],
    handle_grid_visibility_change: Callable[..., Any],
    handle_rectangle_selection: Callable[..., Any],
    handle_add_rectangle: Callable[..., Any],
    handle_update_rectangle: Callable[..., Any],
    handle_delete_rectangle: Callable[..., Any],
    handle_clear_upload: Callable[..., Any],
) -> None:
    """Wire Gradio UI events without self-triggering file-list updates."""
    components.upload.initial_batch_files.change(
        fn=handle_workspace_upload,
        inputs=_workspace_upload_inputs(components, components.upload.initial_batch_files),
        outputs=_workspace_upload_outputs(components, include_side_upload=True),
    )
    components.upload.initial_batch_files.clear(
        fn=handle_clear_upload,
        inputs=None,
        outputs=_clear_upload_outputs(components, include_side_upload=True),
    )

    components.upload.side_batch_files.change(
        fn=lambda *args: _drop_side_upload_from_workspace_result(
            handle_workspace_upload(*args)
        ),
        inputs=_workspace_upload_inputs(components, components.upload.side_batch_files),
        outputs=_workspace_upload_outputs(components, include_side_upload=False),
    )
    components.upload.side_batch_files.clear(
        fn=lambda: _drop_side_upload_from_clear_result(handle_clear_upload()),
        inputs=None,
        outputs=_clear_upload_outputs(components, include_side_upload=False),
    )

    for button_key, direction in NAVIGATION_DIRECTIONS.items():
        _navigation_button(components, button_key).click(
            fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size, direction=direction: navigate_batch(
                files,
                index,
                direction,
                rectangles,
                show_grid,
                grid_size,
                grid_label_size,
            ),
            inputs=_shared_preview_inputs(components),
            outputs=_navigation_outputs(components),
        )

    components.viewer.show_grid_checkbox.change(
        fn=handle_grid_visibility_change,
        inputs=_shared_preview_inputs(components),
        outputs=[
            *components.viewer.preview_outputs,
            components.viewer.grid_size_input,
            components.viewer.grid_label_size_input,
            components.viewer.update_grid_button,
        ],
    ).then(
        fn=lambda: gr.update(selected="original"),
        inputs=None,
        outputs=components.viewer.image_tabs,
    )

    components.viewer.update_grid_button.click(
        fn=handle_grid_change,
        inputs=_shared_preview_inputs(components),
        outputs=components.viewer.preview_outputs,
    )

    components.rectangle.add_rectangle_button.click(
        fn=handle_add_rectangle,
        inputs=_add_rectangle_inputs(components),
        outputs=_add_rectangle_outputs(components),
    )

    components.rectangle.rectangle_selector.change(
        fn=handle_rectangle_selection,
        inputs=[components.state.rectangle_state, components.rectangle.rectangle_selector],
        outputs=[
            *components.rectangle.coordinate_inputs,
            *components.rectangle.selection_buttons,
        ],
    )

    components.rectangle.update_rectangle_button.click(
        fn=handle_update_rectangle,
        inputs=_update_rectangle_inputs(components),
        outputs=_update_rectangle_outputs(components),
    )

    components.rectangle.delete_rectangle_button.click(
        fn=handle_delete_rectangle,
        inputs=_delete_rectangle_inputs(components),
        outputs=_delete_rectangle_outputs(components),
    )
