from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from src.api.schemas import (
    AnonymizeBatchRequest,
    AnonymizeBatchResponse,
    HealthResponse,
    VersionResponse,
)
from src.api.services import anonymize_batch


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


@router.post("/anonymize-batch", response_model=AnonymizeBatchResponse)
def anonymize_batch_endpoint(
    request: AnonymizeBatchRequest,
) -> AnonymizeBatchResponse:
    """Anonymize a local batch of images using the shared export pipeline."""
    try:
        return anonymize_batch(request)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except FileExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
