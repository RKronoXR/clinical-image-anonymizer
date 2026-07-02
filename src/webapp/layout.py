from __future__ import annotations

import gradio as gr

from src.webapp.layout_components import (
    build_export_panel,
    build_initial_upload_panel,
    build_viewer_workspace,
)
from src.webapp.callbacks import (
    get_uploaded_file_paths,
    inspect_current_uploaded_image_html,
)
from src.webapp.preview_rendering import (
    render_censored_preview,
    render_original_preview,
    render_overlay_preview,
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
        return """
        <div style="
            height:42px;
            background:#5a5a66;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:600;
            border-radius:4px;
        ">
            No images loaded.
        </div>
        """

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    return f"""
    <div style="
        height:42px;
        background:#5a5a66;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:600;
        border-radius:4px;
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
    files_state = gr.State([])
    rectangle_state = gr.State([])
    batch_index_state = gr.State(0)

    initial_upload_components = build_initial_upload_panel()
    export_components = build_export_panel()
    workspace_components = build_viewer_workspace(
        initial_batch_status_html=batch_status(None, None),
    )

    initial_upload_group = initial_upload_components["upload_group"]
    initial_batch_files = initial_upload_components["batch_files"]

    export_group = export_components["export_group"]
    export_output_folder = export_components["export_output_folder"]
    export_name_prefix = export_components["export_name_prefix"]
    export_randomize_order = export_components["export_randomize_order"]
    export_button = export_components["export_button"]

    viewer_group = workspace_components["viewer_group"]
    image_tabs = workspace_components["image_tabs"]
    original_preview = workspace_components["original_preview"]
    overlay_preview = workspace_components["overlay_preview"]
    anonymized_preview = workspace_components["anonymized_preview"]

    first_button = workspace_components["first_button"]
    previous_button = workspace_components["previous_button"]
    batch_position = workspace_components["batch_position"]
    next_button = workspace_components["next_button"]
    last_button = workspace_components["last_button"]

    show_grid_checkbox = workspace_components["show_grid_checkbox"]
    grid_size_input = workspace_components["grid_size_input"]
    grid_label_size_input = workspace_components["grid_label_size_input"]

    add_rectangle_button = workspace_components["add_rectangle_button"]
    delete_rectangle_button = workspace_components["delete_rectangle_button"]
    rectangle_selector = workspace_components["rectangle_selector"]
    x_input = workspace_components["x_input"]
    y_input = workspace_components["y_input"]
    width_input = workspace_components["width_input"]
    height_input = workspace_components["height_input"]
    update_rectangle_button = workspace_components["update_rectangle_button"]
    rectangles_json = workspace_components["rectangles_json"]

    current_metadata_html = workspace_components["current_metadata_html"]
    side_batch_files = workspace_components["side_batch_files"]

    initial_batch_files.change(
        fn=handle_workspace_upload,
        inputs=[
            initial_batch_files,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            files_state,
            rectangle_state,
            batch_index_state,
            initial_upload_group,
            export_group,
            viewer_group,
            current_metadata_html,
            rectangle_selector,
            x_input,
            y_input,
            width_input,
            height_input,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
            batch_position,
            side_batch_files,
        ],
    )

    side_batch_files.change(
        fn=handle_workspace_upload,
        inputs=[
            side_batch_files,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            files_state,
            rectangle_state,
            batch_index_state,
            initial_upload_group,
            export_group,
            viewer_group,
            current_metadata_html,
            rectangle_selector,
            x_input,
            y_input,
            width_input,
            height_input,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
            batch_position,
            side_batch_files,
        ],
    )

    first_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "first", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            batch_index_state,
            original_preview,
            overlay_preview,
            anonymized_preview,
            current_metadata_html,
            batch_position,
        ],
    )

    previous_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "previous", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            batch_index_state,
            original_preview,
            overlay_preview,
            anonymized_preview,
            current_metadata_html,
            batch_position,
        ],
    )

    next_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "next", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            batch_index_state,
            original_preview,
            overlay_preview,
            anonymized_preview,
            current_metadata_html,
            batch_position,
        ],
    )

    last_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "last", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            batch_index_state,
            original_preview,
            overlay_preview,
            anonymized_preview,
            current_metadata_html,
            batch_position,
        ],
    )

    show_grid_checkbox.change(
        fn=handle_grid_change,
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    ).then(
        fn=lambda: gr.update(selected="overlay"),
        inputs=None,
        outputs=image_tabs,
    )

    grid_size_input.change(
        fn=handle_grid_change,
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    )

    grid_label_size_input.change(
        fn=handle_grid_change,
        inputs=[
            files_state,
            batch_index_state,
            rectangle_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    )

    add_rectangle_button.click(
        fn=handle_add_rectangle,
        inputs=[
            rectangle_state,
            files_state,
            batch_index_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            rectangle_state,
            rectangle_selector,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
            image_tabs,
        ],
    )

    rectangle_selector.change(
        fn=get_rectangle_values,
        inputs=[rectangle_state, rectangle_selector],
        outputs=[x_input, y_input, width_input, height_input],
    )

    update_rectangle_button.click(
        fn=handle_update_rectangle,
        inputs=[
            rectangle_state,
            rectangle_selector,
            x_input,
            y_input,
            width_input,
            height_input,
            files_state,
            batch_index_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            rectangle_state,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
        ],
    )

    delete_rectangle_button.click(
        fn=handle_delete_rectangle,
        inputs=[
            rectangle_state,
            rectangle_selector,
            files_state,
            batch_index_state,
            show_grid_checkbox,
            grid_size_input,
            grid_label_size_input,
        ],
        outputs=[
            rectangle_state,
            rectangle_selector,
            x_input,
            y_input,
            width_input,
            height_input,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
        ],
    )

    return {
        "files_state": files_state,
        "initial_batch_files": initial_batch_files,
        "side_batch_files": side_batch_files,
        "export_group": export_group,
        "viewer_group": viewer_group,
        "batch_index_state": batch_index_state,
        "original_preview": original_preview,
        "overlay_preview": overlay_preview,
        "anonymized_preview": anonymized_preview,
        "batch_position": batch_position,
        "current_metadata_html": current_metadata_html,
        "rectangle_state": rectangle_state,
        "add_rectangle_button": add_rectangle_button,
        "delete_rectangle_button": delete_rectangle_button,
        "rectangle_selector": rectangle_selector,
        "x_input": x_input,
        "y_input": y_input,
        "width_input": width_input,
        "height_input": height_input,
        "update_rectangle_button": update_rectangle_button,
        "show_grid_checkbox": show_grid_checkbox,
        "grid_size_input": grid_size_input,
        "grid_label_size_input": grid_label_size_input,
        "rectangles_json": rectangles_json,
        "export_output_folder": export_output_folder,
        "export_name_prefix": export_name_prefix,
        "export_randomize_order": export_randomize_order,
        "export_button": export_button,
    }
