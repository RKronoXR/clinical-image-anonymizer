# Future Features and Roadmap

Clinical Image Anonymizer v1.0.0 is intentionally focused on safe local 2D image anonymization with metadata removal, manual rectangular pixel censoring, GUI usage, CLI usage, and Windows installation.

This document collects future-version ideas. These features are not implemented in v1.0.0.

## Current v1.0.0 Limitations

- Version 1.0.0 supports 2D images only.
- Version 1.0.0 does not support 3D volumes such as CBCT, CT, MRI, or other volumetric formats.
- Version 1.0.0 does not perform automatic OCR.
- Version 1.0.0 does not automatically detect identifiable text inside image pixels.
- Version 1.0.0 is not a clinical or diagnostic tool.
- Version 1.0.0 is a research prototype for local-first image anonymization workflows.

## Recommended Workflow for Large Batches

For large image batches, users should prefer the CLI instead of the GUI.

The CLI is recommended for large batches because:

- it is designed for path-based batch processing;
- it can use parallelization parameters;
- it does not need to load all images into the GUI preview workflow;
- it is more suitable for long-running or repeated anonymization jobs.

The GUI is recommended for visual inspection, manual rectangle placement, and smaller interactive workflows.

---

## Documentation

### Feature: Mermaid diagrams across documentation

- Status: idea
- Priority: medium
- Reason: diagrams can make the project easier to understand for users, collaborators, reviewers, and future ACTA AI Lab projects.
- Possible implementation: add Mermaid diagrams where they add practical value.
- Dependencies: stable documentation structure.
- Risks: diagrams may become outdated if not maintained.

Potential diagrams:

- architecture;
- GUI workflow;
- CLI workflow;
- API workflow;
- anonymization pipeline;
- project structure;
- Git workflow;
- release process;
- export sequence;
- installer build workflow.

---

## Anonymization

### Feature: 3D image support

- Status: idea
- Priority: high
- Reason: clinical imaging workflows may include CBCT, CT, MRI, and other volumetric data.
- Possible implementation: add support for 3D formats and slice-based or volume-based censoring.
- Dependencies: format support, memory-safe processing, 3D visualization strategy.
- Risks: high complexity, large memory requirements, privacy risks if partial slices are missed.

### Feature: Freehand drawing

- Status: idea
- Priority: medium
- Reason: some visible identifiers may not fit rectangular regions well.
- Possible implementation: add freehand mask drawing in the GUI.
- Dependencies: interactive drawing component, mask-to-output pipeline.
- Risks: inconsistent masks, UI complexity.

### Feature: Polygons

- Status: idea
- Priority: medium
- Reason: polygonal regions can provide more precise anonymization than rectangles.
- Possible implementation: allow users to draw and edit polygon vertices.
- Dependencies: polygon editor, mask rasterization.
- Risks: usability complexity.

### Feature: Censoring brush

- Status: idea
- Priority: medium
- Reason: brush-based censoring may be easier for small labels or irregular regions.
- Possible implementation: add a brush tool that paints censoring masks.
- Dependencies: image editor support, mask storage.
- Risks: accidental overpainting or underpainting.

### Feature: Undo and redo

- Status: idea
- Priority: high
- Reason: users need safe correction while editing censoring regions.
- Possible implementation: maintain an edit history stack for rectangles, masks, and drawing operations.
- Dependencies: state management.
- Risks: complex state synchronization in GUI.

### Feature: OCR text detection

- Status: idea
- Priority: high
- Reason: OCR can help find visible text or burned-in annotations for review.
- Possible implementation: run OCR locally and show candidate text regions for user confirmation.
- Dependencies: local OCR engine, language configuration, confidence thresholding.
- Risks: OCR can miss identifiers or create false positives.

### Feature: Automatic suggested censoring regions

- Status: idea
- Priority: high
- Reason: suggested rectangles can speed up anonymization while keeping user verification.
- Possible implementation: convert OCR or detection results into editable suggested rectangles.
- Dependencies: OCR or detection module, review UI.
- Risks: users may overtrust automatic suggestions.

### Feature: OCR language configuration

- Status: idea
- Priority: medium
- Reason: multilingual clinical images may contain identifiers in different languages.
- Possible implementation: expose OCR language settings in Developer Mode or CLI.
- Dependencies: OCR engine language packs.
- Risks: installation complexity.

### Feature: Burned-in annotation detection

- Status: idea
- Priority: high
- Reason: text embedded in image pixels may contain patient or institutional identifiers.
- Possible implementation: combine OCR, image heuristics, and optional detection models to flag likely annotation areas.
- Dependencies: OCR and validation dataset.
- Risks: false negatives can create privacy risk.

### Feature: Reusable anonymization templates

- Status: idea
- Priority: medium
- Reason: repeated datasets may require censoring the same regions across images.
- Possible implementation: save and load templates containing rectangles, colors, and batch settings.
- Dependencies: template schema and validation.
- Risks: applying templates to mismatched image sizes may cause incomplete censoring.

---

## Interface

### Feature: More modern icon-based interface

- Status: idea
- Priority: medium
- Reason: icons can make the GUI friendlier for non-technical users.
- Possible implementation: add clear iconography for upload, inspect, draw, export, reset, and help actions.
- Dependencies: UI redesign and icon assets.
- Risks: icons may confuse users if labels are removed.

### Feature: Light and dark themes

- Status: idea
- Priority: medium
- Reason: users may prefer different display modes.
- Possible implementation: add theme selection to the GUI.
- Dependencies: CSS variables and theme testing.
- Risks: contrast and accessibility issues.

### Feature: Full color standardization

- Status: idea
- Priority: medium
- Reason: consistent colors improve maintainability and visual identity.
- Possible implementation: define a small design token set for colors, spacing, borders, and states.
- Dependencies: CSS refactor.
- Risks: visual regressions.

### Feature: Lightweight animations

- Status: idea
- Priority: low
- Reason: subtle animations can improve perceived usability.
- Possible implementation: animate panel transitions, loading states, and success indicators.
- Dependencies: CSS support.
- Risks: unnecessary complexity.

### Feature: Better visual feedback

- Status: idea
- Priority: high
- Reason: users need clear confirmation when loading, inspecting, drawing, and exporting images.
- Possible implementation: add progress messages, status badges, and export summaries.
- Dependencies: GUI state management.
- Risks: excessive UI noise.

### Feature: Improved drag and drop

- Status: idea
- Priority: medium
- Reason: drag and drop can make image loading easier.
- Possible implementation: refine file upload and batch upload interactions.
- Dependencies: Gradio component capabilities.
- Risks: browser-specific behavior.

### Feature: Direct navigation by image number

- Status: idea
- Priority: high
- Reason: large batches are easier to review when users can jump directly to a specific image.
- Possible implementation: add an input box for image index navigation.
- Dependencies: batch state and validation.
- Risks: invalid index handling.

### Feature: Navigation by clicking the image list

- Status: idea
- Priority: high
- Reason: clicking a listed image is faster than stepping one image at a time.
- Possible implementation: make the image list interactive.
- Dependencies: GUI component support.
- Risks: state synchronization issues.

### Feature: Thumbnails

- Status: idea
- Priority: medium
- Reason: thumbnails help users navigate batches visually.
- Possible implementation: generate low-resolution thumbnails for loaded images.
- Dependencies: preview generation and caching.
- Risks: increased memory usage.

### Feature: Zoom and pan

- Status: idea
- Priority: high
- Reason: users may need to inspect small text or details before censoring.
- Possible implementation: add zoom and pan controls to the image viewer.
- Dependencies: image viewer component support.
- Risks: coordinate mapping errors between preview and original image.

### Feature: Automatic contrast adjustment

- Status: idea
- Priority: medium
- Reason: radiographs may need better contrast for visual inspection.
- Possible implementation: add preview-only contrast adjustment without changing source images.
- Dependencies: preview rendering.
- Risks: users may confuse preview adjustment with output modification.

### Feature: Keyboard shortcuts

- Status: idea
- Priority: medium
- Reason: shortcuts can speed up expert review workflows.
- Possible implementation: shortcuts for next image, previous image, add rectangle, delete rectangle, export, undo, and redo.
- Dependencies: frontend event handling.
- Risks: browser conflicts.

### Feature: GUI export parallelization

- Status: idea
- Priority: high
- Reason: large image batches can be slow in GUI workflows.
- Possible implementation: add configurable parallel processing to GUI export while keeping memory use controlled.
- Dependencies: batch engine, safe file I/O, progress reporting, cancellation support.
- Risks: excessive memory use, UI freezing, difficult error reporting for failed files.

---

## Performance

### Feature: Low-resolution editing previews

- Status: idea
- Priority: high
- Reason: full-resolution clinical images can make GUI interaction slower and memory-heavy.
- Possible implementation: generate low-resolution previews for drawing and apply final anonymization on original-resolution images.
- Dependencies: accurate coordinate scaling.
- Risks: coordinate mismatch between preview and original.

### Feature: Apply final anonymization on original images

- Status: idea
- Priority: high
- Reason: previews should not reduce final output quality.
- Possible implementation: store transformations from preview space and apply them to original-resolution copies.
- Dependencies: robust coordinate transform logic.
- Risks: incorrect scaling can leave identifiers uncensored.

### Feature: Partial component reloads

- Status: idea
- Priority: medium
- Reason: updating only affected GUI components can improve responsiveness.
- Possible implementation: refactor callbacks to avoid full interface refresh where possible.
- Dependencies: Gradio callback capabilities.
- Risks: complex state handling.

### Feature: Intelligent caching

- Status: idea
- Priority: medium
- Reason: caching previews and metadata can reduce repeated computation.
- Possible implementation: cache previews, dimensions, and metadata inspection results during a session.
- Dependencies: cache invalidation rules.
- Risks: stale state if files change.

### Feature: Better parallelization for large batches

- Status: idea
- Priority: high
- Reason: batch processing should scale to large datasets without overloading the computer.
- Possible implementation: improve worker configuration, progress reporting, and safe failure handling.
- Dependencies: batch engine and CLI/GUI settings.
- Risks: high CPU or memory use.

---

## Exportation

### Feature: Graphical destination folder selector

- Status: idea
- Priority: high
- Reason: choosing an output folder through the GUI is easier than typing a path.
- Possible implementation: add a folder picker or supported alternative.
- Dependencies: framework support or desktop wrapper.
- Risks: browser security limitations.

### Feature: More output formats

- Status: idea
- Priority: medium
- Reason: users may need different image formats.
- Possible implementation: allow configurable export formats.
- Dependencies: format-specific metadata removal verification.
- Risks: inconsistent metadata behavior across formats.

### Feature: Automatic ZIP export

- Status: idea
- Priority: medium
- Reason: ZIP export simplifies sharing anonymized outputs.
- Possible implementation: create a ZIP after export.
- Dependencies: export summary and safe temporary handling.
- Risks: large ZIP files and storage use.

### Feature: PDF report

- Status: idea
- Priority: medium
- Reason: a PDF report can document anonymization actions.
- Possible implementation: generate a report with file counts, settings, and verification results.
- Dependencies: report template and PDF library.
- Risks: report must not include private data.

### Feature: HTML report

- Status: idea
- Priority: medium
- Reason: HTML reports are easy to inspect locally.
- Possible implementation: generate local HTML with export summary and verification checks.
- Dependencies: report template.
- Risks: report must not expose private paths or identifiers.

### Feature: Detailed export log

- Status: idea
- Priority: high
- Reason: users need traceability for batch anonymization.
- Possible implementation: write structured logs with processed files, output names, applied rectangles, and failures.
- Dependencies: logging schema.
- Risks: logs must not expose sensitive metadata.

---

## Batch Processing

### Feature: Automatic image size compatibility check

- Status: idea
- Priority: high
- Reason: applying the same rectangles to different image sizes can produce partial or missing censoring.
- Possible implementation: check image dimensions before batch export.
- Dependencies: batch metadata inspection.
- Risks: users may ignore warnings.

### Feature: Clear same-size or mixed-size status

- Status: idea
- Priority: high
- Reason: users need to know whether all images share the same dimensions.
- Possible implementation: show a compatibility summary before export.
- Dependencies: dimension scan.
- Risks: cluttered UI.

### Feature: Mixed-size rectangle impact preview

- Status: idea
- Priority: high
- Reason: users should know exactly what happens when rectangles fall outside image boundaries.
- Possible implementation: report whether each rectangle is fully applied, partially applied, or skipped.
- Dependencies: rectangle-boundary validation.
- Risks: long reports for large batches.

### Feature: Batch compatibility preview before export

- Status: idea
- Priority: high
- Reason: users should review risks before producing outputs.
- Possible implementation: add a pre-export validation step.
- Dependencies: validation engine and UI summary.
- Risks: workflow becomes slower.

---

## Automation

### Feature: Fully automatic OCR-assisted anonymization

- Status: idea
- Priority: medium
- Reason: automation can speed up repeated workflows.
- Possible implementation: detect text regions and automatically apply censoring after user-approved settings.
- Dependencies: robust OCR and validation.
- Risks: unsafe if users skip review.

### Feature: Semi-automatic anonymization mode

- Status: idea
- Priority: high
- Reason: semi-automatic mode balances speed and user control.
- Possible implementation: propose regions, require confirmation, then export.
- Dependencies: OCR or detection module.
- Risks: user overreliance.

### Feature: Anonymization profiles

- Status: idea
- Priority: medium
- Reason: profiles can store repeated settings.
- Possible implementation: save color, rectangles, workers, export format, and naming rules.
- Dependencies: profile schema.
- Risks: applying wrong profile to wrong dataset.

### Feature: Watched-folder processing

- Status: idea
- Priority: low
- Reason: automated folder processing can support repeated local workflows.
- Possible implementation: monitor a folder and process new files.
- Dependencies: file watcher and safe queue.
- Risks: accidental processing of wrong files.

### Feature: Background processing

- Status: idea
- Priority: medium
- Reason: large jobs should not block the GUI.
- Possible implementation: add a local job queue with progress tracking.
- Dependencies: task queue or process pool.
- Risks: cancellation and error handling complexity.

---

## API

### Feature: REST API

- Status: idea
- Priority: medium
- Reason: external tools may need to call the anonymization engine.
- Possible implementation: add a local-only FastAPI service.
- Dependencies: API schema and security defaults.
- Risks: accidental network exposure.

### Feature: OpenAPI documentation

- Status: idea
- Priority: medium
- Reason: API users need clear machine-readable documentation.
- Possible implementation: expose local OpenAPI docs.
- Dependencies: REST API.
- Risks: documentation drift.

### Feature: Python client

- Status: idea
- Priority: low
- Reason: a client can simplify integration in scripts.
- Possible implementation: create a small package wrapper for API or core functions.
- Dependencies: stable API.
- Risks: additional maintenance burden.

### Feature: CLI client for API workflows

- Status: idea
- Priority: low
- Reason: a CLI can expose API workflows consistently.
- Possible implementation: add API-backed CLI commands if REST API is implemented.
- Dependencies: REST API.
- Risks: duplicate CLI behavior.

### Feature: Docker deployment

- Status: idea
- Priority: medium
- Reason: Docker can make deployment more reproducible.
- Possible implementation: package GUI, CLI, and optional API in Docker Compose.
- Dependencies: stable ports and configuration.
- Risks: local file access and privacy configuration.

---

## Security

### Feature: Digital signing for installer

- Status: idea
- Priority: medium
- Reason: signing improves user trust and Windows reputation.
- Possible implementation: sign the installer with a valid code-signing certificate.
- Dependencies: certificate management.
- Risks: certificate cost and maintenance.

### Feature: Digital signing for executable

- Status: idea
- Priority: medium
- Reason: signing the executable can reduce warnings and improve provenance.
- Possible implementation: sign the built executable during release.
- Dependencies: build pipeline and certificate.
- Risks: certificate cost and release complexity.

### Feature: Official SHA256 hash per release

- Status: idea
- Priority: high
- Reason: users can verify downloaded installers.
- Possible implementation: publish SHA256 hashes in GitHub Releases.
- Dependencies: release checklist.
- Risks: hash mismatch if artifacts are rebuilt without version changes.

### Feature: Integrity verification

- Status: idea
- Priority: medium
- Reason: users may need to confirm release artifacts were not modified.
- Possible implementation: publish checksums and optional signature verification instructions.
- Dependencies: release automation.
- Risks: extra user complexity.

---

## Quality

### Feature: GitHub Actions

- Status: idea
- Priority: high
- Reason: CI can automatically run tests before merges and releases.
- Possible implementation: add workflow for setup, linting, tests, and build checks.
- Dependencies: stable dependency installation.
- Risks: Windows installer builds may require special runners.

### Feature: Test coverage

- Status: idea
- Priority: medium
- Reason: coverage helps identify untested logic.
- Possible implementation: add coverage reporting for core modules.
- Dependencies: pytest configuration.
- Risks: coverage targets may become distracting if too strict too early.

### Feature: Linter

- Status: idea
- Priority: high
- Reason: linting helps keep code consistent and detect issues.
- Possible implementation: add Ruff checks.
- Dependencies: configuration in `pyproject.toml`.
- Risks: large initial lint cleanup.

### Feature: Formatter

- Status: idea
- Priority: high
- Reason: formatting improves consistency.
- Possible implementation: use Ruff format or Black.
- Dependencies: chosen formatter configuration.
- Risks: large formatting-only diff.

### Feature: Static typing

- Status: idea
- Priority: medium
- Reason: typing improves maintainability and reuse.
- Possible implementation: add mypy or pyright for selected modules.
- Dependencies: type annotations.
- Risks: third-party typing issues.

### Feature: Performance benchmark

- Status: idea
- Priority: medium
- Reason: batch anonymization speed should be measurable.
- Possible implementation: add benchmark scripts for small, medium, and large batches.
- Dependencies: safe synthetic test images.
- Risks: benchmark results vary by machine.

---

## Internationalization

### Feature: English interface

- Status: idea
- Priority: high
- Reason: English is useful for international research users.
- Possible implementation: keep English as default language.
- Dependencies: text catalog.
- Risks: none significant.

### Feature: Spanish interface

- Status: idea
- Priority: medium
- Reason: Spanish support can help ACTA AI Lab collaborators and broader users.
- Possible implementation: add translation strings.
- Dependencies: internationalization system.
- Risks: translation maintenance.

### Feature: Dutch interface

- Status: idea
- Priority: medium
- Reason: Dutch support is useful for local ACTA and Netherlands-based users.
- Possible implementation: add translation strings.
- Dependencies: internationalization system.
- Risks: translation maintenance.

### Feature: Translation system

- Status: idea
- Priority: medium
- Reason: a translation system avoids hardcoded UI text.
- Possible implementation: centralize UI text in language files.
- Dependencies: UI refactor.
- Risks: added complexity.

---

## Integrations

### Feature: DICOM support

- Status: idea
- Priority: high
- Reason: clinical workflows often use DICOM images.
- Possible implementation: add DICOM metadata inspection, anonymization, and output rules.
- Dependencies: DICOM library and strict metadata policy.
- Risks: high privacy and compliance complexity.

### Feature: PACS integration

- Status: idea
- Priority: low
- Reason: PACS integration could support clinical research workflows.
- Possible implementation: connect to approved local PACS systems.
- Dependencies: institutional approval and DICOM networking.
- Risks: privacy, security, and regulatory complexity.

### Feature: Orthanc integration

- Status: idea
- Priority: low
- Reason: Orthanc can provide local DICOM server workflows.
- Possible implementation: add export/import support with Orthanc.
- Dependencies: Orthanc setup and security configuration.
- Risks: accidental exposure of sensitive data.

### Feature: Medical export formats

- Status: idea
- Priority: medium
- Reason: research workflows may require medical imaging formats.
- Possible implementation: support selected safe export formats.
- Dependencies: format-specific metadata controls.
- Risks: incomplete anonymization if format metadata is not fully handled.

### Feature: Plugin system

- Status: idea
- Priority: low
- Reason: plugins could allow future ACTA AI Lab extensions.
- Possible implementation: define a limited plugin interface.
- Dependencies: stable core architecture.
- Risks: security and maintenance burden.

---

## Research

### Feature: Associated scientific publication

- Status: idea
- Priority: medium
- Reason: the tool may support research on local-first image anonymization workflows.
- Possible implementation: document design, validation, and usability outcomes.
- Dependencies: stable release and evaluation.
- Risks: requires formal study design.

### Feature: Public anonymized dataset

- Status: idea
- Priority: low
- Reason: a safe public dataset could support benchmarking.
- Possible implementation: release only fully anonymized and legally approved data.
- Dependencies: permissions, licenses, privacy review.
- Risks: privacy and legal risk.

### Feature: Benchmark against other tools

- Status: idea
- Priority: medium
- Reason: comparison can clarify strengths and limitations.
- Possible implementation: define functional benchmark tasks.
- Dependencies: selected comparator tools.
- Risks: unfair comparison if workflows differ.

### Feature: Usability evaluation

- Status: idea
- Priority: medium
- Reason: user feedback can improve GUI and workflow design.
- Possible implementation: conduct a small structured user study.
- Dependencies: study protocol and participants.
- Risks: time and ethical review requirements.

---

## ACTA AI Lab Reuse

### Feature: Reusable anonymization module

- Status: idea
- Priority: high
- Reason: anonymization logic can be reused in future ACTA AI Lab projects.
- Possible implementation: extract stable functions into a shared module or package.
- Dependencies: stable APIs and tests.
- Risks: premature abstraction.

### Feature: Reusable metadata module

- Status: idea
- Priority: high
- Reason: metadata inspection and removal are common requirements.
- Possible implementation: isolate metadata reading, reporting, and cleaning.
- Dependencies: format-specific validation.
- Risks: metadata behavior differs by format.

### Feature: Reusable export module

- Status: idea
- Priority: high
- Reason: safe file output and mapping reports are useful across tools.
- Possible implementation: extract naming, mapping CSV, overwrite protection, and output validation.
- Dependencies: generic path handling.
- Risks: too much project-specific logic.

### Feature: Reusable GUI components

- Status: idea
- Priority: medium
- Reason: upload, preview, status, and export panels can help future Gradio apps.
- Possible implementation: extract UI helper components after the workflow stabilizes.
- Dependencies: stable GUI layout patterns.
- Risks: Gradio version changes.

### Feature: Reusable installer template

- Status: idea
- Priority: medium
- Reason: future ACTA AI Lab tools may need local Windows installers.
- Possible implementation: generalize PyInstaller and Inno Setup configuration.
- Dependencies: release discipline and icon/version metadata.
- Risks: Windows-specific assumptions.

---

## Prioritization Summary

### High priority

- CLI recommendation for large batches.
- GUI export parallelization.
- Low-resolution previews with original-resolution final export.
- Undo and redo.
- OCR text detection for user review.
- Suggested censoring rectangles.
- Burned-in annotation detection.
- Direct image navigation by number.
- Image list click navigation.
- Zoom and pan.
- Detailed export log.
- Batch size compatibility checks.
- Mixed-size rectangle impact report.
- GitHub Actions.
- Linter and formatter.
- Reusable anonymization, metadata, and export modules.

### Medium priority

- Mermaid diagrams.
- Freehand drawing.
- Polygons.
- Censoring brush.
- OCR language configuration.
- Modern icon-based GUI.
- Light and dark themes.
- Color standardization.
- Better drag and drop.
- Thumbnails.
- Automatic contrast adjustment.
- ZIP, PDF, and HTML reports.
- REST API.
- Docker deployment.
- Digital signing.
- Static typing.
- Internationalization.
- DICOM support.
- Research publication and usability evaluation.

### Low priority

- Lightweight animations.
- Watched-folder processing.
- Python API client.
- PACS integration.
- Orthanc integration.
- Plugin system.
- Public anonymized dataset.
