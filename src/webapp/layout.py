from __future__ import annotations

import gradio as gr

from src.webapp.callbacks import inspect_uploaded_image


def summarize_batch_files(files) -> str:
    if not files:
        return "No batch files selected."

    return f"Selected batch files: {len(files)}"


def build_main_layout():
    with gr.Row():
        developer_mode = gr.Checkbox(
            label="Developer Mode",
            value=False,
        )

    with gr.Row():
        input_image = gr.Image(
            label="Input image",
            type="pil",
        )

        preview_image = gr.Image(
            label="Preview",
            interactive=False,
        )

    with gr.Row():
        batch_files = gr.Files(
            label="Batch images",
            file_types=["image"],
        )

    batch_summary = gr.Textbox(
        label="Batch summary",
        interactive=False,
        value="No batch files selected.",
    )

    metadata_box = gr.Code(
        label="Metadata",
        language="json",
        interactive=False,
    )

    input_image.change(
        fn=lambda img: img,
        inputs=input_image,
        outputs=preview_image,
    )

    input_image.change(
        fn=inspect_uploaded_image,
        inputs=input_image,
        outputs=metadata_box,
    )

    batch_files.change(
        fn=summarize_batch_files,
        inputs=batch_files,
        outputs=batch_summary,
    )

    return {
        "developer_mode": developer_mode,
        "input_image": input_image,
        "preview_image": preview_image,
        "batch_files": batch_files,
        "batch_summary": batch_summary,
        "metadata_box": metadata_box,
    }