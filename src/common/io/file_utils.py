"""Reusable file-system utilities."""

from __future__ import annotations

from pathlib import Path

from src.common.exceptions import FileOperationError

SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
    ".dcm",
}


def ensure_directory(path: Path) -> Path:
    """Create a directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_supported_image(path: Path) -> bool:
    """Return True if the file extension is supported."""
    return path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS


def list_images(directory: Path) -> list[Path]:
    """Return supported images inside a directory."""
    return sorted(
        p
        for p in directory.iterdir()
        if p.is_file() and is_supported_image(p)
    )


def ensure_file_exists(path: Path) -> Path:
    """Validate that a file exists."""
    if not path.exists():
        raise FileOperationError(f"File not found: {path}")
    return path