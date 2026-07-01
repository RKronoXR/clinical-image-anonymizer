from __future__ import annotations

import gradio as gr

from src.webapp.callbacks import (
    get_uploaded_file_path,
    inspect_uploaded_batch,
    inspect_uploaded_image,
)
from src.webapp.preview_rendering import (
    render_censored_preview,
    render_original_preview,
    render_overlay_preview,
)
from src.webapp.rectangle_state import (
    add_rectangle,
    format_rectangles,
    get_rectangle_values,
    rectangle_choices,
    selected_rectangle_index,
    update_rectangle,
)


def summarize_batch_files(files) -> str:
    if not files:
        return "No batch files selected."
    return f"Selected batch files: {len(files)}"


def switch_processing_mode(mode: str):
    is_single = mode == "Single image"
    return (
        gr.update(visible=is_single),
        gr.update(visible=not is_single),
        gr.update(visible=is_single),
        gr.update(visible=not is_single),
    )


def preview_all_single_views_with_grid(file, rectangles, show_grid, grid_size):
    file_path = get_uploaded_file_path(file)
    return (
        render_original_preview(file_path, show_grid, grid_size),
        render_overlay_preview(file_path, rectangles, show_grid, grid_size),
        render_censored_preview(file_path, rectangles),
    )


def handle_add_rectangle(rectangles, file, show_grid, grid_size):
    updated = add_rectangle(rectangles)
    choices = rectangle_choices(updated)
    selected = choices[-1] if choices else None
    original, overlay, anonymized = preview_all_single_views_with_grid(
        file,
        updated,
        show_grid,
        grid_size,
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


def handle_update_rectangle(rectangles, label, x, y, width, height, file, show_grid, grid_size):
    index = selected_rectangle_index(label)
    updated = update_rectangle(rectangles, index, x, y, width, height)
    original, overlay, anonymized = preview_all_single_views_with_grid(
        file,
        updated,
        show_grid,
        grid_size,
    )

    return (
        updated,
        format_rectangles(updated),
        original,
        overlay,
        anonymized,
    )


def build_main_layout():
    processing_mode = gr.Dropdown(
        label="Processing mode",
        choices=["Single image", "Batch images"],
        value="Single image",
    )

    rectangle_state = gr.State([])

    with gr.Group(visible=True) as single_group:
        with gr.Row():
            with gr.Column(scale=5):
                with gr.Tabs(selected="original") as image_tabs:
                    with gr.Tab("Original", id="original"):
                        single_file = gr.File(
                            label="Input image file",
                            file_types=["image"],
                            type="filepath",
                            height=180,
                        )

                        original_preview = gr.Image(
                            label="Original image",
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

            with gr.Column(scale=1):
                add_rectangle_button = gr.Button(value="Add rectangle")

                rectangle_selector = gr.Dropdown(
                    label="Selected rectangle",
                    choices=[],
                    value=None,
                    interactive=True,
                )

                with gr.Row():
                    x_input = gr.Number(label="X", value=0, precision=0)
                    y_input = gr.Number(label="Y", value=0, precision=0)

                with gr.Row():
                    width_input = gr.Number(label="Width", value=100, precision=0)
                    height_input = gr.Number(label="Height", value=100, precision=0)

                update_rectangle_button = gr.Button(
                    value="Update selected rectangle"
                )

                show_grid_checkbox = gr.Checkbox(
                    label="Show pixel grid",
                    value=False,
                )

                grid_size_input = gr.Number(
                    label="Grid square size in pixels",
                    value=100,
                    precision=0,
                )

                rectangles_json = gr.Code(
                    label="Rectangle coordinates",
                    language="json",
                    interactive=False,
                    value="[]",
                )

        single_metadata_box = gr.Code(
            label="Single image metadata",
            language="json",
            interactive=False,
        )

    with gr.Group(visible=False) as batch_group:
        batch_files = gr.Files(
            label="Batch images",
            file_types=["image"],
        )

        batch_mode = gr.Radio(
            label="Batch rectangle mode",
            choices=[
                "Apply the same rectangles to all images",
                "Custom rectangles per image (future)",
            ],
            value="Apply the same rectangles to all images",
        )

        batch_summary = gr.Textbox(
            label="Batch summary",
            interactive=False,
            value="No batch files selected.",
        )

        batch_metadata_html = gr.HTML(
            label="Batch metadata",
        )

    single_file.change(
        fn=preview_all_single_views_with_grid,
        inputs=[single_file, rectangle_state, show_grid_checkbox, grid_size_input],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    )

    single_file.change(
        fn=inspect_uploaded_image,
        inputs=single_file,
        outputs=single_metadata_box,
    )

    show_grid_checkbox.change(
        fn=preview_all_single_views_with_grid,
        inputs=[single_file, rectangle_state, show_grid_checkbox, grid_size_input],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    )

    grid_size_input.change(
        fn=preview_all_single_views_with_grid,
        inputs=[single_file, rectangle_state, show_grid_checkbox, grid_size_input],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    )

    batch_files.change(
        fn=summarize_batch_files,
        inputs=batch_files,
        outputs=batch_summary,
    )

    batch_files.change(
        fn=inspect_uploaded_batch,
        inputs=batch_files,
        outputs=batch_metadata_html,
    )

    processing_mode.change(
        fn=switch_processing_mode,
        inputs=processing_mode,
        outputs=[
            single_group,
            batch_group,
            single_metadata_box,
            batch_metadata_html,
        ],
    )

    add_rectangle_button.click(
        fn=handle_add_rectangle,
        inputs=[
            rectangle_state,
            single_file,
            show_grid_checkbox,
            grid_size_input,
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
            single_file,
            show_grid_checkbox,
            grid_size_input,
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
        "processing_mode": processing_mode,
        "single_file": single_file,
        "original_preview": original_preview,
        "overlay_preview": overlay_preview,
        "anonymized_preview": anonymized_preview,
        "batch_files": batch_files,
        "batch_mode": batch_mode,
        "batch_summary": batch_summary,
        "single_metadata_box": single_metadata_box,
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
        "rectangles_json": rectangles_json,
    }