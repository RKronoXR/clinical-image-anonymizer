# Architecture and Roadmap

## Project
Clinical Image Anonymizer

## Version Target
v0.1.0

## Goal
Build a local-first tool for anonymizing common clinical image files by removing metadata and optionally censoring visible identifiers with manual rectangles.

## v0.1 Scope
- Common image formats: JPG, PNG, TIFF
- Preserve TIFF bit depth, including 16-bit TIFF
- Single-image metadata inspection before anonymization
- Batch metadata removal without per-image confirmation
- Manual rectangle-based pixel censoring
- Preserve original format when possible
- Preserve folder structure during batch processing
- Gradio local web interface
- CLI for technical and batch use
- Windows laptop as first development platform

## Architecture

### Reusable Core
- src/common/: config, paths, logging, safe I/O
- src/anonymization/: metadata inspection, metadata removal, rectangle censoring, verification
- src/cli/: path-based anonymization commands
- src/webapp/: local Gradio GUI
- src/project_specific/: ACTA-specific text and configuration

### Data Flow
1. User selects image or folder.
2. Software reads file safely.
3. Metadata is inspected.
4. For single image, metadata is shown before confirmation.
5. For batch mode, metadata is removed automatically.
6. Optional manual rectangles are applied.
7. Output is written to outputs/.
8. Verification checks metadata after export.
9. Logs report success, warnings, and failed files.

## Roadmap

### v0.1.0
Minimum usable anonymizer:
- repo skeleton
- Docker skeleton
- metadata inspection
- metadata removal
- manual rectangle censoring
- single-image workflow
- batch workflow
- CLI
- basic Gradio UI
- basic tests
- privacy documentation

### v0.2.0
Improved usability:
- better batch logs
- richer Developer Mode
- safer previews
- downloadable reports
- more robust TIFF handling
- better error messages

### v1.0.0
Portfolio-ready release:
- clean documentation
- tested Docker flow
- validated anonymization examples
- stable CLI
- stable GUI
- final quality checklist
- GitHub-ready code without private data

## Out of Scope for v0.1
- DICOM
- OCR-assisted text detection
- automatic anonymization of burned-in labels
- ML models
- cloud processing
- clinical-use claims

## Key Risks
- TIFF 16-bit data corruption
- metadata differences across formats
- accidental private data in screenshots
- batch overwrite mistakes
- hidden metadata not removed by libraries

## Mitigations
- Preserve bit depth when editing pixels.
- Never overwrite original files.
- Save outputs separately.
- Verify metadata after export.
- Keep private images out of GitHub.
- Use safe public or synthetic examples for documentation.
