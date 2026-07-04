from __future__ import annotations

import os
import socket
import sys
import urllib.request
import webbrowser
from pathlib import Path

import gradio as gr

from src.webapp.layout import build_main_layout


APP_TITLE = "Clinical Image Anonymizer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Ricardo Eugenio Gonzalez Valenzuela"
APP_ORGANIZATION = "ACTA AI Lab"
APP_REPOSITORY = "https://github.com/RKronoXR/clinical-image-anonymizer"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7860
LOCAL_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def resource_path(relative_path: str) -> Path:
    """Return resource path for local Python and PyInstaller builds."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base_path / relative_path


def ensure_standard_streams() -> None:
    """Prevent uvicorn logging failure when PyInstaller runs without a console."""
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")
    if sys.stdin is None:
        sys.stdin = open(os.devnull, "r", encoding="utf-8")


def is_port_in_use(host: str, port: int) -> bool:
    """Return True when the local Gradio port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        return probe.connect_ex((host, port)) == 0


def is_local_app_available() -> bool:
    """Return True when a local web app responds at the configured URL."""
    try:
        with urllib.request.urlopen(LOCAL_URL, timeout=0.8) as response:
            return 200 <= response.status < 500
    except Exception:
        return False


def _load_app_css() -> str:
    return resource_path("src/webapp/styles.css").read_text(encoding="utf-8")


def build_about_html() -> str:
    """Return the user-facing About block."""
    return f"""
    <div class="cia-about-card">
        <h3>About</h3>
        <p><strong>Clinical Image Anonymizer</strong></p>
        <p><strong>Version:</strong> 1.0.0</p>
        <p><strong>Author:</strong> {APP_AUTHOR}</p>
        <p><strong>Organization:</strong> {APP_ORGANIZATION}</p>
        <p><strong>Repository:</strong> <a href="{APP_REPOSITORY}" target="_blank">{APP_REPOSITORY}</a></p>
        <p><strong>Original file safety:</strong> the software is designed to write anonymized copies to an output folder and not modify, move, crop, overwrite, rename, delete, or replace original input images.</p>
        <p><strong>Disclaimer:</strong> research prototype, non-clinical tool, not a medical device, not for diagnosis, and not for clinical decision-making. Users remain responsible for verifying anonymization before sharing or using exported images.</p>
        <p><strong>Large batches:</strong> for many images, prefer the CLI because it supports path-based batch processing and worker configuration without loading all images into the GUI preview workflow.</p>
    </div>
    """


def build_app() -> gr.Blocks:
    """Build the local Gradio interface."""
    ensure_standard_streams()

    with gr.Blocks(title=APP_TITLE, css=_load_app_css()) as demo:
        gr.Markdown(f"# {APP_TITLE}", elem_classes=["cia-title"])

        with gr.Group(visible=True) as about_group:
            gr.HTML(build_about_html())

        build_main_layout(about_group=about_group)

    return demo


def main() -> None:
    ensure_standard_streams()

    if is_local_app_available() or is_port_in_use(SERVER_HOST, SERVER_PORT):
        webbrowser.open(LOCAL_URL)
        return

    app = build_app()
    app.launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        favicon_path=str(resource_path("assets/icons/clinical_image_anonymizer.ico")),
        inbrowser=True,
    )


if __name__ == "__main__":
    main()
