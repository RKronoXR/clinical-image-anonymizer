from __future__ import annotations

from pathlib import Path

from src.anonymization.export import export_anonymized_images
from src.anonymization.rectangle_filter import ALL_IMAGES_FILENAME
from src.api.schemas import AnonymizeBatchRequest, AnonymizeBatchResponse
from src.cli.file_discovery import discover_input_images


def _api_rectangles_to_core_rectangles(
    request: AnonymizeBatchRequest,
) -> list[dict]:
    """Convert API rectangle models into the core rectangle dictionary format."""
    rectangles: list[dict] = []

    for rectangle in request.rectangles:
        rectangles.append(
            {
                "filename": rectangle.filename or ALL_IMAGES_FILENAME,
                "x": rectangle.x,
                "y": rectangle.y,
                "width": rectangle.width,
                "height": rectangle.height,
            }
        )

    return rectangles


def anonymize_batch(request: AnonymizeBatchRequest) -> AnonymizeBatchResponse:
    """Run batch anonymization using the shared core export pipeline."""
    input_path = Path(request.input_dir)
    output_dir = Path(request.output_dir)

    image_paths = discover_input_images(
        input_path=input_path,
        recursive=request.recursive,
    )

    exported = export_anonymized_images(
        image_paths=image_paths,
        output_dir=output_dir,
        rectangles=_api_rectangles_to_core_rectangles(request),
        prefix=request.prefix,
        randomize=request.randomize,
        overwrite=request.overwrite,
        workers=request.workers,
        input_root=input_path if input_path.is_dir() else input_path.parent,
        preserve_structure=request.preserve_structure,
    )

    mapping_csv = output_dir / "mapping.csv"

    return AnonymizeBatchResponse(
        status="success",
        processed=len(exported),
        output_dir=str(output_dir),
        mapping_csv=str(mapping_csv),
        exported_files=[str(item.output_path) for item in exported],
    )
