from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class HealthResponse(BaseModel):
    """Health-check response."""

    status: str = Field(..., examples=["ok"])
    service: str = Field(..., examples=["clinical-image-anonymizer-api"])


class VersionResponse(BaseModel):
    """Application version and project metadata."""

    name: str
    version: str
    author: str
    organization: str
    repository: str


class RectangleRequest(BaseModel):
    """Rectangle coordinates for API anonymization requests."""

    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    filename: str | None = None

    @model_validator(mode="before")
    @classmethod
    def from_coordinate_list(cls, value: Any) -> Any:
        """Accept [x, y, width, height] for simple global rectangles."""
        if isinstance(value, list):
            if len(value) != 4:
                raise ValueError("Rectangle lists must be [x, y, width, height].")
            return {
                "x": value[0],
                "y": value[1],
                "width": value[2],
                "height": value[3],
            }
        return value


class AnonymizeBatchRequest(BaseModel):
    """Batch anonymization request using local filesystem paths."""

    input_dir: Path
    output_dir: Path
    rectangles: list[RectangleRequest] = Field(default_factory=list)
    prefix: str = ""
    randomize: bool = False
    recursive: bool = False
    workers: int = Field(default=1, ge=1)
    overwrite: bool = False
    preserve_structure: bool = False

    @field_validator("input_dir", "output_dir", mode="before")
    @classmethod
    def expand_user_path(cls, value: Any) -> Any:
        if isinstance(value, str):
            return Path(value).expanduser()
        return value


class AnonymizeBatchResponse(BaseModel):
    """Batch anonymization response."""

    status: str
    processed: int
    output_dir: str
    mapping_csv: str
    exported_files: list[str]
