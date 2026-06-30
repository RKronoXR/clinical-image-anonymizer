"""Reusable custom exceptions."""

from __future__ import annotations


class ClinicalImageAnonymizerError(Exception):
    """Base exception for the project."""


class ConfigurationError(ClinicalImageAnonymizerError):
    """Configuration-related error."""


class FileOperationError(ClinicalImageAnonymizerError):
    """File system operation error."""


class ValidationError(ClinicalImageAnonymizerError):
    """Input validation error."""


class ImageProcessingError(ClinicalImageAnonymizerError):
    """Image processing error."""


class MetadataError(ClinicalImageAnonymizerError):
    """Metadata processing error."""