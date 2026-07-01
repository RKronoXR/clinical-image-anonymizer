from __future__ import annotations

import gradio as gr

from src.webapp.callbacks import (
    inspect_uploaded_batch,
    inspect_uploaded_image,
    preview_uploaded_image,
)

from src.webapp.rectangle_state import add_rectangle, format_rectangles

def summarize_batch_files(files) -> str:
    if not files:
        return "No batch files selected."

    return f"Selected batch files: {len(files)}"


def switch_processing_mode(mode: str):
    is_single = mode == "Single image"

    return (
        gr.update(visible=is_single),
        gr.update(visible=is_single),
        gr.update(visible=not is_single),
        gr.update(visible=not is_single),
        gr.update(visible=is_single),
        gr.update(visible=not is_single),
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

    single_file = gr.File(
        label="Input image file",
        file_types=["image"],
        type="filepath",
        height=80,
        visible=True,
    )

    single_preview = gr.Image(
        label="Input image preview",
        interactive=False,
        height=420,
        visible=True,
    )

    batch_files = gr.Files(
        label="Batch images",
        file_types=["image"],
        visible=False,
    )

    batch_summary = gr.Textbox(
        label="Batch summary",
        interactive=False,
        value="No batch files selected.",
        visible=False,
    )

    single_metadata_box = gr.Code(
        label="Single image metadata",
        language="json",
        interactive=False,
        visible=True,
    )

    batch_metadata_html = gr.HTML(
        label="Batch metadata",
        visible=False,
    )

    rectangle_state = gr.State([])

    add_rectangle_button = gr.Button(
        value="Add rectangle",
    )

    rectangles_json = gr.Code(
        label="Rectangle coordinates",
        language="json",
        interactive=False,
        value="[]",
    )

    add_rectangle_button.click(
        fn=lambda rectangles: (
            add_rectangle(rectangles),
            format_rectangles(add_rectangle(rectangles)),
        ),
        inputs=rectangle_state,
        outputs=[rectangle_state, rectangles_json],
    )

    single_file.change(
        fn=preview_uploaded_image,
        inputs=single_file,
        outputs=single_preview,
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
            single_file,
            single_preview,
            batch_files,
            batch_summary,
            single_metadata_box,
            batch_metadata_html,
        ],
    )

    return {
        "developer_mode": developer_mode,
        "processing_mode": processing_mode,
        "single_file": single_file,
        "single_preview": single_preview,
        "batch_files": batch_files,
        "batch_summary": batch_summary,
        "single_metadata_box": single_metadata_box,
        "batch_metadata_html": batch_metadata_html,
        "rectangle_state": rectangle_state,
        "add_rectangle_button": add_rectangle_button,
        "rectangles_json": rectangles_json,
    }