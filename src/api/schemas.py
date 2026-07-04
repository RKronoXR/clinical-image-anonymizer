from __future__ import annotations

from pydantic import BaseModel, Field


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
