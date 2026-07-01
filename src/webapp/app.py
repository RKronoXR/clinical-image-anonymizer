# src/webapp/app.py

from __future__ import annotations

import gradio as gr


APP_TITLE = "Clinical Image Anonymizer"


def build_app() -> gr.Blocks:
    """Build the minimal local Gradio interface."""
    with gr.Blocks(title=APP_TITLE) as demo:
        gr.Markdown(f"# {APP_TITLE}")
        gr.Markdown(
            "Local-first research prototype for clinical image anonymization."
        )

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

        with gr.Row():
            preview_image = gr.Image(
                label="Preview",
                interactive=False,
            )

        input_image.change(
            fn=lambda img: img,
            inputs=input_image,
            outputs=preview_image,
        )

        gr.Markdown("Interface structure ready. Functional components will be added incrementally.")

    return demo


def main() -> None:
    app = build_app()
    app.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()