from __future__ import annotations

from fastapi import FastAPI

from src.api.routes import router


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(
        title="Clinical Image Anonymizer API",
        version="1.0.0",
        description=(
            "Local-first REST API for clinical image anonymization. "
            "Research prototype, not for diagnosis or clinical decision-making."
        ),
    )
    app.include_router(router)
    return app


app = create_app()
