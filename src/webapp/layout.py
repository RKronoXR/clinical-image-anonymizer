from __future__ import annotations

from pathlib import Path

import gradio as gr

from src.webapp.callbacks import (
    get_uploaded_file_paths,
    handle_export_batch,
    inspect_current_uploaded_image_html,
)
from src.webapp.event_registry import register_callbacks
from src.webapp.layout_components import build_viewer_workspace
from src.webapp.panels.export_panel import build_export_panel
from src.webapp.panels.upload_panel import build_initial_upload_panel
from src.webapp.preview_rendering import (
    render_censored_preview,
    render_overlay_preview,
)
from src.webapp.rectangle_state import (
    ALL_IMAGES_FILENAME,
    DEFAULT_RECTANGLE_HEIGHT,
    DEFAULT_RECTANGLE_WIDTH,
    add_rectangle,
    delete_rectangle,
    format_rectangles,
    get_rectangle_values,
    rectangle_choices,
    rectangles_for_filename,
    selected_rectangle_index,
    update_rectangle,
)
from src.webapp.ui_components import StateComponents, UIComponents
from src.webapp.ui_constants import (
    BATCH_STATUS_BACKGROUND,
    BATCH_STATUS_BORDER_RADIUS_PX,
    BATCH_STATUS_HEIGHT_PX,
)


def get_current_batch_path(files, index: int | float | None) -> str | None:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return None

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    return file_paths[safe_index]


def get_current_batch_filename(files, index: int | float | None) -> str | None:
    file_path = get_current_batch_path(files, index)
    if file_path is None:
        return None
    return Path(file_path).name


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


def navigation_button_updates(files, index: int | float | None):
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return (
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
        )

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    last_index = len(file_paths) - 1

    return (
        gr.update(interactive=safe_index > 0),
        gr.update(interactive=safe_index > 0),
        gr.update(interactive=safe_index < last_index),
        gr.update(interactive=safe_index < last_index),
    )


def filter_rectangles_for_files(
    rectangles: list[dict] | None,
    file_paths: list[str],
) -> list[dict]:
    """Keep global rectangles and rectangles that still belong to loaded files."""
    loaded_filenames = {Path(path).name for path in file_paths}
    kept: list[dict] = []

    for rectangle in rectangles or []:
        filename = rectangle.get("filename") or rectangle.get("image_path") or ""
        filename = Path(str(filename)).name if filename else ""

        if filename == ALL_IMAGES_FILENAME or filename in loaded_filenames:
            kept.append(rectangle)

    return kept


def preview_current_batch_image(
    files,
    index,
    rectangles,
    show_grid,
    grid_size,
    grid_label_size,
):
    file_path = get_current_batch_path(files, index)
    filename = Path(file_path).name if file_path else None
    visible_rectangles = rectangles_for_filename(rectangles, filename)

    return (
        render_overlay_preview(
            file_path=file_path,
            rectangles=visible_rectangles,
            show_grid=show_grid,
            grid_size=grid_size,
            grid_label_size=grid_label_size,
        ),
        render_censored_preview(
            file_path=file_path,
            rectangles=visible_rectangles,
            show_grid=show_grid,
            grid_size=grid_size,
            grid_label_size=grid_label_size,
        ),
    )


def handle_workspace_upload(
    files,
    rectangles,
    current_index,
    show_grid,
    grid_size,
    grid_label_size,
):
    file_paths = get_uploaded_file_paths(files)
    updated_rectangles = filter_rectangles_for_files(rectangles, file_paths)

    has_files = len(file_paths) > 0
    index = 0 if not has_files else max(0, min(int(current_index or 0), len(file_paths) - 1))

    original, anonymized = preview_current_batch_image(
        file_paths,
        index,
        updated_rectangles,
        show_grid,
        grid_size,
        grid_label_size,
    )

    metadata_html = inspect_current_uploaded_image_html(file_paths, index)
    nav_updates = navigation_button_updates(file_paths, index)
    choices = rectangle_choices(updated_rectangles)
    selected = choices[-1] if choices else None
    x, y, width, height = get_rectangle_values(updated_rectangles, selected)
    has_selection = selected is not None

    return (
        file_paths,
        updated_rectangles,
        index,
        gr.update(visible=not has_files),
        gr.update(visible=not has_files),
        gr.update(visible=has_files),
        gr.update(visible=has_files),
        gr.update(visible=has_files, value=metadata_html),
        gr.update(choices=choices, value=selected),
        gr.update(value=True),
        x,
        y,
        width,
        height,
        format_rectangles(updated_rectangles),
        original,
        anonymized,
        batch_status(file_paths, index),
        *nav_updates,
        gr.update(value=file_paths),
        gr.update(interactive=has_selection),
        gr.update(interactive=has_selection),
    )


def handle_clear_upload():
    return (
        [],
        [],
        0,
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False, value=""),
        gr.update(choices=[], value=None),
        gr.update(value=True),
        0,
        0,
        DEFAULT_RECTANGLE_WIDTH,
        DEFAULT_RECTANGLE_HEIGHT,
        format_rectangles([]),
        None,
        None,
        batch_status(None, None),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(value=[]),
        gr.update(value=[]),
        gr.update(interactive=False),
        gr.update(interactive=False),
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

    original, anonymized = preview_current_batch_image(
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
        anonymized,
        inspect_current_uploaded_image_html(files, index),
        batch_status(files, index),
        *navigation_button_updates(files, index),
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


def handle_grid_visibility_change(
    files,
    index,
    rectangles,
    show_grid,
    grid_size,
    grid_label_size,
):
    original, anonymized = preview_current_batch_image(
        files,
        index,
        rectangles,
        show_grid,
        grid_size,
        grid_label_size,
    )
    return (
        original,
        anonymized,
        gr.update(interactive=bool(show_grid)),
        gr.update(interactive=bool(show_grid)),
        gr.update(interactive=bool(show_grid)),
    )


def handle_rectangle_selection(rectangles, label):
    x, y, width, height = get_rectangle_values(rectangles, label)
    has_selection = selected_rectangle_index(label) is not None
    return (
        x,
        y,
        width,
        height,
        gr.update(interactive=has_selection),
        gr.update(interactive=has_selection),
    )


def handle_add_rectangle(
    rectangles,
    x,
    y,
    width,
    height,
    apply_all_images,
    files,
    index,
    show_grid,
    grid_size,
    grid_label_size,
):
    current_filename = get_current_batch_filename(files, index) or ""
    rectangle_filename = ALL_IMAGES_FILENAME if apply_all_images else current_filename
    updated = add_rectangle(
        rectangles,
        filename=rectangle_filename,
        x=x,
        y=y,
        width=width,
        height=height,
    )
    choices = rectangle_choices(updated)
    selected = choices[-1] if choices else None

    original, anonymized = preview_current_batch_image(
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
        anonymized,
        gr.update(selected="original"),
        gr.update(interactive=True),
        gr.update(interactive=True),
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

    original, anonymized = preview_current_batch_image(
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
    has_selection = selected is not None

    original, anonymized = preview_current_batch_image(
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
        anonymized,
        gr.update(interactive=has_selection),
        gr.update(interactive=has_selection),
    )


def build_main_layout(about_group=None):
    state_components = StateComponents(
        files_state=gr.State([]),
        rectangle_state=gr.State([]),
        batch_index_state=gr.State(0),
    )

    initial_upload_components = build_initial_upload_panel()
    export_components = build_export_panel()
    workspace_components = build_viewer_workspace(
        initial_batch_status_html=batch_status(None, None),
    )

    components = UIComponents.from_component_maps(
        state=state_components,
        initial_upload_components=initial_upload_components,
        export_components=export_components,
        workspace_components=workspace_components,
        about_group=about_group,
    )

    register_callbacks(
        components=components,
        handle_workspace_upload=handle_workspace_upload,
        navigate_batch=navigate_batch,
        handle_grid_change=handle_grid_change,
        handle_grid_visibility_change=handle_grid_visibility_change,
        handle_rectangle_selection=handle_rectangle_selection,
        handle_add_rectangle=handle_add_rectangle,
        handle_update_rectangle=handle_update_rectangle,
        handle_delete_rectangle=handle_delete_rectangle,
        handle_clear_upload=handle_clear_upload,
    )

    export_button = export_components["export_button"]
    output_folder = export_components["export_output_folder"]
    filename_prefix = export_components["export_name_prefix"]
    randomize_output = export_components["export_randomize_order"]
    export_status = export_components.get("export_status")

    export_button.click(
        fn=handle_export_batch,
        inputs=[
            state_components.files_state,
            state_components.rectangle_state,
            output_folder,
            filename_prefix,
            randomize_output,
        ],
        outputs=[export_status] if export_status is not None else None,
    )

    return components.public_component_map()
