# Architecture

## Version Target
v0.1.0

## Scope
Local-first anonymization tool for common image files.

## Initial Formats
- JPG
- PNG
- TIFF

Important: TIFF files may be 16-bit. The anonymization pipeline must preserve bit depth and avoid unnecessary pixel conversion.

## Interfaces
- Gradio local web interface
- CLI for technical and batch workflows

## Processing Rules
- Single image: show metadata first and ask user confirmation before removing it.
- Batch mode: remove metadata automatically.
- Pixel censoring: manual rectangles only.
- Output: preserve original image format when possible.
- Batch folders: preserve original folder structure.

## Main Modules
- src/common/: reusable utilities
- src/anonymization/: metadata and pixel anonymization logic
- src/cli/: command-line interface
- src/webapp/: local Gradio interface
- src/project_specific/: ACTA-specific project text or configuration

## Out of Scope for v0.1
- DICOM
- OCR-assisted detection
- automatic text detection
- ML models
