from __future__ import annotations

import gradio as gr


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

    input_image.change(
        fn=lambda img: img,
        inputs=input_image,
        outputs=preview_image,
    )

    return {
        "developer_mode": developer_mode,
        "input_image": input_image,
        "preview_image": preview_image,
        "batch_files": batch_files,
    }