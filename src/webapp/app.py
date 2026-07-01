from __future__ import annotations

import gradio as gr

from src.webapp.layout import build_main_layout


APP_TITLE = "Clinical Image Anonymizer"


def build_app() -> gr.Blocks:
    """Build the local Gradio interface."""
    with gr.Blocks(title=APP_TITLE) as demo:
        gr.Markdown(f"# {APP_TITLE}")
        gr.Markdown(
            "Local-first research prototype for clinical image anonymization."
        )

        build_main_layout()

        gr.Markdown(
            "Interface structure ready. Functional components will be added incrementally."
        )

    return demo


def main() -> None:
    app = build_app()
    app.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()