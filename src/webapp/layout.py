from __future__ import annotations

import gradio as gr

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

    with gr.Group(elem_classes=["cia-card", "cia-initial-upload-card"]) as initial_upload_group:
        gr.Markdown("### Upload images")
        initial_batch_files = gr.Files(
            label="Drag and drop images here or click to browse",
            file_types=["image"],
            elem_classes=["cia-upload-dropzone"],
        )
        gr.Markdown(
            "Supported formats: JPG, PNG, TIFF, DICOM",
            elem_classes=["cia-muted"],
        )

    with gr.Group(visible=False, elem_classes=["cia-card"]) as export_group:
        with gr.Row(equal_height=True):
            export_output_folder = gr.Textbox(
                label="Output folder",
                value="outputs/anonymized",
                interactive=True,
                scale=4,
            )

            export_name_prefix = gr.Textbox(
                label="Output filename prefix",
                value="Anonymized_",
                interactive=True,
                scale=3,
            )

            export_randomize_order = gr.Checkbox(
                label="Randomize output image order",
                value=False,
                scale=2,
            )

            export_button = gr.Button(
                value="Export anonymized images",
                scale=2,
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

    with gr.Group(visible=False) as viewer_group:
        with gr.Row(equal_height=False):
            with gr.Column(scale=7, min_width=760):
                with gr.Group(elem_classes=["cia-card", "cia-top-panel"]):
                    with gr.Tabs(selected="original", elem_classes=["cia-image-tabs"]) as image_tabs:
                        with gr.Tab("Original", id="original"):
                            original_preview = gr.Image(
                                label="Current image",
                                interactive=False,
                                height=600,
                            )

                        with gr.Tab("Overlay", id="overlay"):
                            overlay_preview = gr.Image(
                                label="Rectangle overlay preview",
                                interactive=False,
                                height=600,
                            )

                        with gr.Tab("Anonymized", id="anonymized"):
                            anonymized_preview = gr.Image(
                                label="Anonymized preview",
                                interactive=False,
                                height=600,
                            )

                    with gr.Row(equal_height=True):
                        first_button = gr.Button(value="First")
                        previous_button = gr.Button(value="Previous")
                        batch_position = gr.Markdown(value=batch_status(None, None))
                        next_button = gr.Button(value="Next")
                        last_button = gr.Button(value="Last")

                    with gr.Group(elem_classes=["cia-tight-card"]):
                        show_grid_checkbox = gr.Checkbox(
                            label="Show pixel grid in Overlay",
                            value=False,
                        )

                        with gr.Row(equal_height=True):
                            grid_size_input = gr.Number(
                                label="Grid square size in pixels",
                                value=100,
                                precision=0,
                                scale=1,
                            )
                            grid_label_size_input = gr.Number(
                                label="Grid number size",
                                value=12,
                                precision=0,
                                scale=1,
                            )

            with gr.Column(scale=3, min_width=360, elem_classes=["cia-right-column"]):
                with gr.Group(elem_classes=["cia-card", "cia-top-panel"]):
                    with gr.Row(equal_height=True):
                        gr.Markdown(
                            "### Rectangles <span class='cia-muted'>(global for all images)</span>"
                        )
                        add_rectangle_button = gr.Button(
                            value="Add rectangle",
                            variant="secondary",
                            scale=0,
                            elem_classes=["cia-primary-action"],
                        )

                    rectangle_selector = gr.Dropdown(
                        label="Selected rectangle",
                        choices=[],
                        value=None,
                        interactive=True,
                    )

                    with gr.Row(equal_height=True):
                        x_input = gr.Number(label="X", value=0, precision=0)
                        y_input = gr.Number(label="Y", value=0, precision=0)

                    with gr.Row(equal_height=True):
                        width_input = gr.Number(
                            label="W",
                            value=DEFAULT_RECTANGLE_WIDTH,
                            precision=0,
                        )

                        height_input = gr.Number(
                            label="H",
                            value=DEFAULT_RECTANGLE_HEIGHT,
                            precision=0,
                        )

                    update_rectangle_button = gr.Button(
                        value="Update selected rectangle",
                        variant="secondary",
                        elem_classes=["cia-primary-action"],
                    )
                    delete_rectangle_button = gr.Button(value="Delete selected rectangle")

                    rectangles_json = gr.Code(
                        label="Rectangle coordinates",
                        language="json",
                        interactive=False,
                        value="[]",
                        elem_classes=["cia-json-card"],
                    )
        with gr.Row(equal_height=False):
            with gr.Column(scale=7, min_width=760):
                current_metadata_html = gr.HTML(
                    label="Current image metadata",
                    visible=False,
                    elem_classes=["cia-card", "cia-bottom-panel"],
                )

            with gr.Column(scale=3, min_width=360):
                with gr.Group(elem_classes=["cia-card", "cia-upload-panel", "cia-bottom-panel"]):
                    gr.Markdown("### Upload images")
                    side_batch_files = gr.Files(
                        label="Drag and drop images here or click to browse",
                        file_types=["image"],
                        elem_classes=["cia-upload-dropzone"],
                    )
                    gr.Markdown(
                        "Supported formats: JPG, PNG, TIFF, DICOM",
                        elem_classes=["cia-muted"],
                    )

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