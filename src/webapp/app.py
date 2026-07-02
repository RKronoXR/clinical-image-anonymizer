from __future__ import annotations

from pathlib import Path

import gradio as gr

from src.webapp.layout import build_main_layout


APP_TITLE = "Clinical Image Anonymizer"


APP_CSS_PATH = "src/webapp/styles.css"


def _load_app_css() -> str:
    return Path(APP_CSS_PATH).read_text(encoding="utf-8")




def build_app() -> gr.Blocks:
    """Build the local Gradio interface."""
    with gr.Blocks(title=APP_TITLE, css=_load_app_css()) as demo:
        gr.Markdown(f"# {APP_TITLE}", elem_classes=["cia-title"])
        gr.Markdown(
            "Local-first research prototype for clinical image anonymization.",
            elem_classes=["cia-subtitle"],
        )

        build_main_layout()

    return demo


def main() -> None:
    app = build_app()
    app.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
