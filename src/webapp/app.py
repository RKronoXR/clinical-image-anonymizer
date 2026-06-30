"""Clinical Image Anonymizer web app."""

import gradio as gr


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Clinical Image Anonymizer") as app:
        gr.Markdown("# Clinical Image Anonymizer")
        gr.Markdown("Local-first tool for anonymizing common clinical image files.")
        gr.Markdown("Status: v0.1 development skeleton.")

    return app


if __name__ == "__main__":
    build_app().launch(
        server_name="0.0.0.0",
        server_port=7860,
    )
