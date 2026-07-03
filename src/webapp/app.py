from __future__ import annotations

import sys
from pathlib import Path

import gradio as gr

from src.webapp.layout import build_main_layout


APP_TITLE = "Clinical Image Anonymizer"


def resource_path(relative_path: str) -> Path:
    """Return resource path for local Python and PyInstaller builds."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base_path / relative_path


def _load_app_css() -> str:
    return resource_path("src/webapp/styles.css").read_text(encoding="utf-8")


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
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        favicon_path=str(resource_path("assets/icons/clinical_image_anonymizer.ico")),
    )


if __name__ == "__main__":
    main()