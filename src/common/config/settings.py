"""Reusable project settings."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class ProjectSettings(BaseModel):
    """Global project settings."""

    project_name: str = Field(default="clinical-image-anonymizer")
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    gradio_host: str = Field(default="0.0.0.0")
    gradio_port: int = Field(default=7860)

    data_dir: Path = Field(default=Path("data"))
    outputs_dir: Path = Field(default=Path("outputs"))
    runs_dir: Path = Field(default=Path("runs"))