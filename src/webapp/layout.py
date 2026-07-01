from __future__ import annotations

import gradio as gr

from src.webapp.callbacks import (
    get_uploaded_file_path,
    get_uploaded_file_paths,
    inspect_uploaded_batch,
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
    format_rectangles,
    get_rectangle_values,
    rectangle_choices,
    selected_rectangle_index,
    update_rectangle,
)


def summarize_batch_files(files) -> str:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return "No images loaded."

    lines = [f"Loaded images: {len(file_paths)}"]
    lines.extend(f"{index}. {path}" for index, path in enumerate(file_paths, start=1))
    return "\n".join(lines)


def get_current_batch_path(files, index: int | float | None) -> str | None:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return None

    safe_index = max(0, min(int(index or 0), len(file_paths) - 1))
    return file_paths[safe_index]


def batch_status(files, index: int | float | None) -> str:
    file_paths = get_uploaded_file_paths(files)
    if not file_paths:
        return "No images loaded."

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


def rectangles_for_current_image(rectangles, current_path: str | None) -> list[dict]:
    if current_path is None:
        return []

    return [
        rectangle
        for rectangle in rectangles or []
        if rectangle.get("image_path", current_path) == current_path
    ]


def preview_current_batch_image(
    files,
    index,
    rectangles,
    show_grid,
    grid_size,
    grid_label_size,
):
    file_path = get_current_batch_path(files, index)
    visible_rectangles = rectangles_for_current_image(rectangles, file_path)

    return (
        render_original_preview(file_path),
        render_overlay_preview(
            file_path=file_path,
            rectangles=visible_rectangles,
            show_grid=show_grid,
            grid_size=grid_size,
            grid_label_size=grid_label_size,
        ),
        render_censored_preview(file_path, visible_rectangles),
    )


def handle_batch_upload(files, show_grid, grid_size, grid_label_size):
    rectangles: list[dict] = []
    index = 0
    original, overlay, anonymized = preview_current_batch_image(
        files,
        index,
        rectangles,
        show_grid,
        grid_size,
        grid_label_size,
    )

    has_files = len(get_uploaded_file_paths(files)) > 0

    return (
        rectangles,
        index,
        gr.update(visible=has_files),
        gr.update(choices=[], value=None),
        0,
        0,
        DEFAULT_RECTANGLE_WIDTH,
        DEFAULT_RECTANGLE_HEIGHT,
        "[]",
        original,
        overlay,
        anonymized,
        summarize_batch_files(files),
        inspect_uploaded_batch(files),
        batch_status(files, index),
    )


def navigate_batch(files, current_index, direction, rectangles, show_grid, grid_size, grid_label_size):
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
        batch_status(files, index),
    )


def handle_add_rectangle(rectangles, files, index, show_grid, grid_size, grid_label_size):
    image_path = get_current_batch_path(files, index) or ""
    updated = add_rectangle(rectangles, image_path=image_path)
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
    rectangle_state = gr.State([])
    batch_index_state = gr.State(0)

    batch_files = gr.Files(
        label="Upload images",
        file_types=["image"],
    )

    with gr.Group(visible=False) as workspace_group:
        with gr.Row():
            with gr.Column(scale=5):
                with gr.Tabs(selected="original") as image_tabs:
                    with gr.Tab("Original", id="original"):
                        original_preview = gr.Image(
                            label="Current image",
                            interactive=False,
                            height=620,
                        )

                    with gr.Tab("Overlay", id="overlay"):
                        overlay_preview = gr.Image(
                            label="Rectangle overlay preview",
                            interactive=False,
                            height=620,
                        )

                    with gr.Tab("Anonymized", id="anonymized"):
                        anonymized_preview = gr.Image(
                            label="Anonymized preview",
                            interactive=False,
                            height=620,
                        )

                with gr.Row():
                    first_button = gr.Button(value="First")
                    previous_button = gr.Button(value="Previous")
                    batch_position = gr.Markdown(
                        value="<div style='text-align:center; font-weight:600;'>No images loaded.</div>"
                    )
                    next_button = gr.Button(value="Next")
                    last_button = gr.Button(value="Last")

            with gr.Column(scale=1):
                add_rectangle_button = gr.Button(value="Add rectangle")

                rectangle_selector = gr.Dropdown(
                    label="Selected rectangle",
                    choices=[],
                    value=None,
                    interactive=True,
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        x_input = gr.Number(label="X", value=0, precision=0)
                    with gr.Column(scale=1):
                        y_input = gr.Number(label="Y", value=0, precision=0)

                with gr.Row():
                    with gr.Column(scale=1):
                        width_input = gr.Number(
                            label="W",
                            value=DEFAULT_RECTANGLE_WIDTH,
                            precision=0,
                        )
                    with gr.Column(scale=1):
                        height_input = gr.Number(
                            label="H",
                            value=DEFAULT_RECTANGLE_HEIGHT,
                            precision=0,
                        )

                update_rectangle_button = gr.Button(value="Update selected rectangle")

                show_grid_checkbox = gr.Checkbox(
                    label="Show pixel grid in Overlay",
                    value=False,
                )

                grid_size_input = gr.Number(
                    label="Grid square size in pixels",
                    value=100,
                    precision=0,
                )

                grid_label_size_input = gr.Number(
                    label="Grid number size",
                    value=12,
                    precision=0,
                )

                rectangles_json = gr.Code(
                    label="Rectangle coordinates",
                    language="json",
                    interactive=False,
                    value="[]",
                )

        batch_summary = gr.Textbox(
            label="Loaded image list",
            interactive=False,
            lines=6,
            value="No images loaded.",
        )

        batch_metadata_html = gr.HTML(label="Batch metadata")

    batch_files.change(
        fn=handle_batch_upload,
        inputs=[batch_files, show_grid_checkbox, grid_size_input, grid_label_size_input],
        outputs=[
            rectangle_state,
            batch_index_state,
            workspace_group,
            rectangle_selector,
            x_input,
            y_input,
            width_input,
            height_input,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
            batch_summary,
            batch_metadata_html,
            batch_position,
        ],
    )

    first_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "first", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            batch_files,
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
            batch_position,
        ],
    )

    previous_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "previous", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            batch_files,
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
            batch_position,
        ],
    )

    next_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "next", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            batch_files,
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
            batch_position,
        ],
    )

    last_button.click(
        fn=lambda files, index, rectangles, show_grid, grid_size, grid_label_size: navigate_batch(
            files, index, "last", rectangles, show_grid, grid_size, grid_label_size
        ),
        inputs=[
            batch_files,
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
            batch_position,
        ],
    )

    show_grid_checkbox.change(
        fn=handle_grid_change,
        inputs=[
            batch_files,
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
            batch_files,
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
            batch_files,
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
            batch_files,
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
            batch_files,
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

    return {
        "batch_files": batch_files,
        "workspace_group": workspace_group,
        "batch_index_state": batch_index_state,
        "original_preview": original_preview,
        "overlay_preview": overlay_preview,
        "anonymized_preview": anonymized_preview,
        "batch_position": batch_position,
        "batch_summary": batch_summary,
        "batch_metadata_html": batch_metadata_html,
        "rectangle_state": rectangle_state,
        "add_rectangle_button": add_rectangle_button,
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
    }