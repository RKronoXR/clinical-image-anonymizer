# Future Features

Use this file for useful ideas that are intentionally outside the current milestone.

## Feature: Complex clinical image formats

- Status: idea
- Priority: high
- Reason: future versions should support more clinically relevant formats beyond common images.
- Possible implementation: add support for DICOM, multi-page TIFF, uncommon TIFF encodings, image series, and format-specific metadata handling.
- Dependencies: pydicom, tifffile, metadata validation utilities, test files without private data.
- Risks: accidental metadata retention, pixel data conversion, unsupported compression, private data exposure.

## Feature: OCR-assisted visible identifier review

- Status: idea
- Priority: medium
- Reason: visible text burned into pixels may contain patient identifiers that metadata removal cannot remove.
- Possible implementation: use OCR only to highlight suspicious text regions for human review, not for automatic final anonymization.
- Dependencies: OCR engine, review UI, false-positive and false-negative handling.
- Risks: OCR may miss identifiers, incorrectly flag anatomy or image markers, or create false confidence.

## Feature: Advanced anonymization validation report

- Status: idea
- Priority: medium
- Reason: batch anonymization should provide clear evidence of what was changed and what failed.
- Possible implementation: generate CSV or JSON reports with file path, format, metadata-before count, metadata-after count, censoring rectangles, processing time, and errors.
- Dependencies: batch logging, metadata verification, report writer.
- Risks: reports must not include private metadata values.

## Feature: Safer TIFF handling improvements

- Status: idea
- Priority: high
- Reason: TIFF files may be 16-bit or contain multiple pages, compression, or special metadata.
- Possible implementation: add explicit tests for bit-depth preservation, multi-page TIFF handling, and no unintended pixel conversion.
- Dependencies: tifffile, synthetic TIFF fixtures, validation tests.
- Risks: silent data changes if image arrays are converted incorrectly.

## Feature: GUI folder path batch input

- Status: idea
- Priority: medium
- Reason: Some users may prefer entering a folder path instead of manually selecting many image files.
- Possible implementation: Add a folder path textbox, a recursive search checkbox, and a reusable image-discovery helper that ignores non-image files and reports valid images found.
- Dependencies: safe path validation, supported image extension list, clear UI warnings.
- Risks: accidental processing of unintended nested private images if recursive mode is enabled without clear user confirmation.