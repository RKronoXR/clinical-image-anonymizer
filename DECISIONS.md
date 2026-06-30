# Architecture Decisions

This file records important technical decisions for the project.

## ADR-001: Use Gradio local web interface

- Status: accepted
- Date: 2026-06-30
- Decision: use Gradio as the local web interface for v0.1.
- Reason: fast local GUI development, simple upload/download workflow, good for demos.
- Consequence: not a native desktop app.

## ADR-002: Add CLI for technical and batch workflows

- Status: accepted
- Date: 2026-06-30
- Decision: provide a CLI in addition to the GUI.
- Reason: batch anonymization needs reproducible path-based execution.
- Consequence: CLI and GUI must share the same reusable anonymization core.

## ADR-003: Limit v0.1 to common image formats

- Status: accepted
- Date: 2026-06-30
- Decision: support JPG, PNG, TIFF/TIF in v0.1.
- Reason: reduce scope and deliver a usable first version.
- Consequence: DICOM and complex clinical formats are future features.

## ADR-004: Preserve TIFF bit depth

- Status: accepted
- Date: 2026-06-30
- Decision: TIFF processing must avoid unintended conversion, especially for 16-bit images.
- Reason: clinical image data must not be silently altered.
- Consequence: TIFF handling requires dedicated tests.

## ADR-005: Manual rectangle censoring only in v0.1

- Status: accepted
- Date: 2026-06-30
- Decision: visible identifiers are censored using user-defined rectangles.
- Reason: safer and more transparent than automatic OCR for v0.1.
- Consequence: OCR remains a future feature.

## ADR-006: Use configurable Docker port

- Status: accepted
- Date: 2026-06-30
- Decision: expose Gradio through GRADIO_SERVER_PORT.
- Reason: multiple local projects may run at the same time.
- Consequence: .env.example must document the port.
