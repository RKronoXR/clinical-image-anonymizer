from __future__ import annotations

import gradio as gr

from src.webapp.callbacks import (
    inspect_uploaded_batch,
    inspect_uploaded_image,
    preview_all_single_views,
)
from src.webapp.rectangle_canvas import (
    render_rectangle_canvas,
    sync_canvas_rectangles,
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


def handle_add_rectangle(rectangles, file):
    updated = add_rectangle(rectangles)
    choices = rectangle_choices(updated)
    selected = choices[-1] if choices else None
    original, overlay, anonymized = preview_all_single_views(file, updated)
    canvas_html = render_rectangle_canvas(file, updated)

    return (
        updated,
        gr.update(choices=choices, value=selected),
        format_rectangles(updated),
        original,
        overlay,
        anonymized,
        canvas_html,
    )


def handle_update_rectangle(rectangles, label, x, y, width, height, file):
    index = selected_rectangle_index(label)
    updated = update_rectangle(rectangles, index, x, y, width, height)
    original, overlay, anonymized = preview_all_single_views(file, updated)
    canvas_html = render_rectangle_canvas(file, updated)

    return (
        updated,
        format_rectangles(updated),
        original,
        overlay,
        anonymized,
        canvas_html,
    )


def handle_canvas_payload(payload, rectangles, file):
    updated, rectangles_json = sync_canvas_rectangles(payload, rectangles)
    choices = rectangle_choices(updated)
    selected = choices[-1] if choices else None

    original, overlay, anonymized = preview_all_single_views(file, updated)
    latest = updated[-1] if updated else {"x": 0, "y": 0, "width": 100, "height": 100}

    return (
        updated,
        gr.update(choices=choices, value=selected),
        latest["x"],
        latest["y"],
        latest["width"],
        latest["height"],
        rectangles_json,
        original,
        overlay,
        anonymized,
        render_rectangle_canvas(file, updated),
    )


def build_main_layout():
    developer_mode = gr.Checkbox(
        label="Developer Mode",
        value=False,
    )

    processing_mode = gr.Dropdown(
        label="Processing mode",
        choices=["Single image", "Batch images"],
        value="Single image",
    )

    with gr.Group(visible=True) as single_group:
        single_file = gr.File(
            label="Input image file",
            file_types=["image"],
            type="filepath",
            height=80,
        )

        with gr.Tabs():
            with gr.Tab("Original"):
                original_preview = gr.Image(
                    label="Original image",
                    interactive=False,
                    height=420,
                )

            with gr.Tab("Draw Rectangles"):
                rectangle_canvas = gr.HTML(
                    label="Interactive rectangle editor",
                )

            with gr.Tab("Overlay"):
                overlay_preview = gr.Image(
                    label="Rectangle overlay preview",
                    interactive=False,
                    height=420,
                )

            with gr.Tab("Anonymized"):
                anonymized_preview = gr.Image(
                    label="Anonymized preview",
                    interactive=False,
                    height=420,
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

        batch_summary = gr.Textbox(
            label="Batch summary",
            interactive=False,
            value="No batch files selected.",
        )

        batch_metadata_html = gr.HTML(
            label="Batch metadata",
        )

    rectangle_state = gr.State([])

    rectangle_canvas_payload = gr.Textbox(
        label="Rectangle canvas payload",
        elem_id="rectangle_canvas_payload",
        visible=False,
    )

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

    update_rectangle_button = gr.Button(value="Update selected rectangle")

    rectangles_json = gr.Code(
        label="Rectangle coordinates",
        language="json",
        interactive=False,
        value="[]",
    )

    single_file.change(
        fn=preview_all_single_views,
        inputs=[single_file, rectangle_state],
        outputs=[original_preview, overlay_preview, anonymized_preview],
    )

    single_file.change(
        fn=render_rectangle_canvas,
        inputs=[single_file, rectangle_state],
        outputs=rectangle_canvas,
    )

    single_file.change(
        fn=inspect_uploaded_image,
        inputs=single_file,
        outputs=single_metadata_box,
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
        inputs=[rectangle_state, single_file],
        outputs=[
            rectangle_state,
            rectangle_selector,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
            rectangle_canvas,
        ],
    )

    rectangle_canvas_payload.change(
        fn=handle_canvas_payload,
        inputs=[rectangle_canvas_payload, rectangle_state, single_file],
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
            rectangle_canvas,
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
        ],
        outputs=[
            rectangle_state,
            rectangles_json,
            original_preview,
            overlay_preview,
            anonymized_preview,
            rectangle_canvas,
        ],
    )

    return {
        "developer_mode": developer_mode,
        "processing_mode": processing_mode,
        "single_file": single_file,
        "original_preview": original_preview,
        "rectangle_canvas": rectangle_canvas,
        "overlay_preview": overlay_preview,
        "anonymized_preview": anonymized_preview,
        "batch_files": batch_files,
        "batch_summary": batch_summary,
        "single_metadata_box": single_metadata_box,
        "batch_metadata_html": batch_metadata_html,
        "rectangle_state": rectangle_state,
        "rectangle_canvas_payload": rectangle_canvas_payload,
        "add_rectangle_button": add_rectangle_button,
        "rectangle_selector": rectangle_selector,
        "x_input": x_input,
        "y_input": y_input,
        "width_input": width_input,
        "height_input": height_input,
        "update_rectangle_button": update_rectangle_button,
        "rectangles_json": rectangles_json,
    }