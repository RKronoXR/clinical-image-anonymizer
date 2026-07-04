from __future__ import annotations

from fastapi import APIRouter

from src.api.schemas import HealthResponse, VersionResponse


API_SERVICE_NAME = "clinical-image-anonymizer-api"
APP_NAME = "Clinical Image Anonymizer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Ricardo Eugenio Gonzalez Valenzuela"
APP_ORGANIZATION = "ACTA AI Lab"
APP_REPOSITORY = "https://github.com/RKronoXR/clinical-image-anonymizer"


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return a lightweight health check for monitoring and smoke tests."""
    return HealthResponse(status="ok", service=API_SERVICE_NAME)


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    """Return version and project metadata."""
    return VersionResponse(
        name=APP_NAME,
        version=APP_VERSION,
        author=APP_AUTHOR,
        organization=APP_ORGANIZATION,
        repository=APP_REPOSITORY,
    )
