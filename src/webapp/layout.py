from __future__ import annotations

import gradio as gr

from src.webapp.event_registry import register_callbacks
from src.webapp.layout_components import build_viewer_workspace
from src.webapp.panels.export_panel import build_export_panel
from src.webapp.panels.upload_panel import build_initial_upload_panel
from src.webapp.callbacks import (
    get_uploaded_file_paths,
    inspect_current_uploaded_image_html,
)
from src.webapp.preview_rendering import (
    render_censored_preview,
    render_original_preview,
    render_overlay_preview,
)
from src.webapp.ui_constants import (
    BATCH_STATUS_BACKGROUND,
    BATCH_STATUS_BORDER_RADIUS_PX,
    BATCH_STATUS_HEIGHT_PX,
)
from src.webapp.rectangle_state import (
    DEFAULT_RECTANGLE_HEIGHT,
    DEFAULT_RECTANGLE_WIDTH,
    add_rectangle,
    delete_rectangle,
    format_rectangles,
    get_rectangle_values,
    rectangle_choices,
    selected_rectangle_index,
    update_rectangle,
)


def get_current_batch_path(files, index: int | float | None) -> str | None:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return None

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    return file_paths[safe_index]


def batch_status(files, index: int | float | None) -> str:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return f"""
        <div style="
            height:{BATCH_STATUS_HEIGHT_PX}px;
            background:{BATCH_STATUS_BACKGROUND};
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:600;
            border-radius:{BATCH_STATUS_BORDER_RADIUS_PX}px;
        ">
            No images loaded.
        </div>
        """

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    return f"""
    <div style="
        height:{BATCH_STATUS_HEIGHT_PX}px;
        background:{BATCH_STATUS_BACKGROUND};
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:600;
        border-radius:{BATCH_STATUS_BORDER_RADIUS_PX}px;
    ">
        Image {safe_index + 1} of {len(file_paths)}
    </div>
    """


def preview_current_batch_image(
    files,
    index,
    rectangles,
    show_grid,
    grid_size,
    grid_label_size,
):
    file_path = get_current_batch_path(files, index)

    return (
        render_original_preview(file_path),
        render_overlay_preview(
            file_path=file_path,
            rectangles=rectangles,
            show_grid=show_grid,
            grid_size=grid_size,
            grid_label_size=grid_label_size,
        ),
        render_censored_preview(file_path, rectangles),
    )


def handle_workspace_upload(files, show_grid, grid_size, grid_label_size):
    file_paths = get_uploaded_file_paths(files)
    rectangles: list[dict] = []
    index = 0
    original, overlay, anonymized = preview_current_batch_image(
        file_paths,
        index,
        rectangles,
        show_grid,
        grid_size,
        grid_label_size,
    )

    has_files = len(file_paths) > 0
    metadata_html = inspect_current_uploaded_image_html(file_paths, index)

    return (
        file_paths,
        rectangles,
        index,
        gr.update(visible=not has_files),
        gr.update(visible=has_files),
        gr.update(visible=has_files),
        gr.update(visible=has_files, value=metadata_html),
        gr.update(choices=[], value=None),
        0,
        0,
        DEFAULT_RECTANGLE_WIDTH,
        DEFAULT_RECTANGLE_HEIGHT,
        "[]",
        original,
        overlay,
        anonymized,
        batch_status(file_paths, index),
        gr.update(value=file_paths),
    )


def navigate_batch(
    files,
    current_index,
    direction,
    rectangles,
    show_grid,
    grid_size,
    grid_label_size,
):
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        index = 0
    else:
        current = int(current_index or 0)
        last = len(file_paths) - 1

        if direction == "first":
            index = 0
        elif direction == "previous":
            index = max(0, current - 1)
        elif direction == "next":
            index = min(last, current + 1)
        elif direction == "last":
            index = last
        else:
            index = current

    original, overlay, anonymized = preview_current_batch_image(
        files,
        index,
        rectangles,
        show_grid,
        grid_size,
        grid_label_size,
    )

    return (
        index,
        original,
        overlay,
        anonymized,
        inspect_current_uploaded_image_html(files, index),
        batch_status(files, index),
    )


def handle_add_rectangle(rectangles, files, index, show_grid, grid_size, grid_label_size):
    updated = add_rectangle(rectangles)
    choices = rectangle_choices(updated)
    selected = choices[-1] if choices else None

    original, overlay, anonymized = preview_current_batch_image(
        files,
        index,
        updated,
        show_grid,
        grid_size,
        grid_label_size,
    )

    return (
        updated,
        gr.update(choices=choices, value=selected),
        format_rectangles(updated),
        original,
        overlay,
        anonymized,
        gr.update(selected="overlay"),
    )


def handle_update_rectangle(
    rectangles,
    label,
    x,
    y,
    width,
    height,
    files,
    index,
    show_grid,
    grid_size,
    grid_label_size,
):
    rectangle_index = selected_rectangle_index(label)
    updated = update_rectangle(rectangles, rectangle_index, x, y, width, height)

    original, overlay, anonymized = preview_current_batch_image(
        files,
        index,
        updated,
        show_grid,
        grid_size,
        grid_label_size,
    )

    return (
        updated,
        format_rectangles(updated),
        original,
        overlay,
        anonymized,
    )


def handle_delete_rectangle(
    rectangles,
    label,
    files,
    index,
    show_grid,
    grid_size,
    grid_label_size,
):
    rectangle_index = selected_rectangle_index(label)
    updated = delete_rectangle(rectangles, rectangle_index)
    choices = rectangle_choices(updated)
    selected = choices[min(rectangle_index or 0, len(choices) - 1)] if choices else None
    x, y, width, height = get_rectangle_values(updated, selected)

    original, overlay, anonymized = preview_current_batch_image(
        files,
        index,
        updated,
        show_grid,
        grid_size,
        grid_label_size,
    )

    return (
        updated,
        gr.update(choices=choices, value=selected),
        x,
        y,
        width,
        height,
        format_rectangles(updated),
        original,
        overlay,
        anonymized,
    )


def handle_grid_change(files, index, rectangles, show_grid, grid_size, grid_label_size):
    return preview_current_batch_image(
        files,
        index,
        rectangles,
        show_grid,
        grid_size,
        grid_label_size,
    )



def build_main_layout():
    components = {
        "files_state": gr.State([]),
        "rectangle_state": gr.State([]),
        "batch_index_state": gr.State(0),
    }

    initial_upload_components = build_initial_upload_panel()
    export_components = build_export_panel()
    workspace_components = build_viewer_workspace(
        initial_batch_status_html=batch_status(None, None),
    )

    components.update(
        {
            "initial_upload_group": initial_upload_components["upload_group"],
            "initial_batch_files": initial_upload_components["batch_files"],
            **export_components,
            **workspace_components,
        }
    )

    register_callbacks(
        components=components,
        handle_workspace_upload=handle_workspace_upload,
        navigate_batch=navigate_batch,
        handle_grid_change=handle_grid_change,
        handle_add_rectangle=handle_add_rectangle,
        handle_update_rectangle=handle_update_rectangle,
        handle_delete_rectangle=handle_delete_rectangle,
    )

    return {
        "files_state": components["files_state"],
        "initial_batch_files": components["initial_batch_files"],
        "side_batch_files": components["side_batch_files"],
        "export_group": components["export_group"],
        "viewer_group": components["viewer_group"],
        "batch_index_state": components["batch_index_state"],
        "original_preview": components["original_preview"],
        "overlay_preview": components["overlay_preview"],
        "anonymized_preview": components["anonymized_preview"],
        "batch_position": components["batch_position"],
        "current_metadata_html": components["current_metadata_html"],
        "rectangle_state": components["rectangle_state"],
        "add_rectangle_button": components["add_rectangle_button"],
        "delete_rectangle_button": components["delete_rectangle_button"],
        "rectangle_selector": components["rectangle_selector"],
        "x_input": components["x_input"],
        "y_input": components["y_input"],
        "width_input": components["width_input"],
        "height_input": components["height_input"],
        "update_rectangle_button": components["update_rectangle_button"],
        "show_grid_checkbox": components["show_grid_checkbox"],
        "grid_size_input": components["grid_size_input"],
        "grid_label_size_input": components["grid_label_size_input"],
        "rectangles_json": components["rectangles_json"],
        "export_output_folder": components["export_output_folder"],
        "export_name_prefix": components["export_name_prefix"],
        "export_randomize_order": components["export_randomize_order"],
        "export_button": components["export_button"],
    }
