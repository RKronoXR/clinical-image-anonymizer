"""Configuration loading utilities."""

from __future__ import annotations

import os
from pathlib import Path

from src.common.config.settings import ProjectSettings


def load_settings() -> ProjectSettings:
    """Load settings from environment variables."""

    return ProjectSettings(
        project_name=os.getenv("PROJECT_NAME", "clinical-image-anonymizer"),
        environment=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        gradio_host=os.getenv("GRADIO_HOST", "0.0.0.0"),
        gradio_port=int(os.getenv("GRADIO_PORT", "7860")),
        data_dir=Path(os.getenv("DATA_DIR", "data")),
        outputs_dir=Path(os.getenv("OUTPUTS_DIR", "outputs")),
        runs_dir=Path(os.getenv("RUNS_DIR", "runs")),
    )