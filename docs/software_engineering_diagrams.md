# Software Engineering Diagrams

This document provides engineering-oriented diagrams for Clinical Image Anonymizer.

The diagrams use Mermaid syntax and are intended for developers, reviewers, maintainers, and future ACTA AI Lab projects that may reuse modules from this repository.

---

## 1. System context

```mermaid
flowchart LR
    User["User / Researcher"]
    GUI["Gradio GUI"]
    CLI["Command-line interface"]
    API["FastAPI REST API"]
    Core["Anonymization Core"]
    FS["Local filesystem"]
    Docs["Documentation"]

    User --> GUI
    User --> CLI
    User --> API
    User --> Docs

    GUI --> Core
    CLI --> Core
    API --> Core

    Core --> FS
    GUI --> FS
    CLI --> FS
    API --> FS

    FS --> Input["Input images"]
    FS --> Output["Anonymized output images"]
    FS --> Mapping["mapping.csv"]
```

Key point: GUI, CLI, and REST API are thin interfaces over the shared anonymization core.

---

## 2. High-level architecture

```mermaid
flowchart TB
    subgraph Interfaces
        Webapp["src/webapp<br/>Gradio GUI"]
        CLI["src/cli<br/>CLI entrypoint"]
        API["src/api<br/>FastAPI REST API"]
    end

    subgraph Core
        Anonymization["src/anonymization<br/>Core image anonymization"]
        Common["src/common<br/>Reusable utilities"]
    end

    subgraph External
        PIL["Pillow"]
        OpenCV["OpenCV"]
        TIFF["tifffile"]
        PyInstaller["PyInstaller"]
        Inno["Inno Setup"]
    end

    Webapp --> Anonymization
    CLI --> Anonymization
    API --> Anonymization

    Webapp --> Common
    CLI --> Common
    API --> Common
    Anonymization --> Common

    Anonymization --> PIL
    Anonymization --> OpenCV
    Anonymization --> TIFF

    PyInstaller --> Webapp
    PyInstaller --> CLI
    Inno --> PyInstaller
```

Design rule: project-specific interfaces should not duplicate anonymization logic.

---

## 3. Main module dependency diagram

```mermaid
flowchart LR
    API["src/api"]
    Webapp["src/webapp"]
    CLI["src/cli"]

    Export["src/anonymization/export.py"]
    Plan["src/anonymization/export_plan.py"]
    Draw["src/anonymization/rectangle_draw.py"]
    Filter["src/anonymization/rectangle_filter.py"]
    Metadata["src/anonymization/metadata.py"]
    Writer["src/anonymization/image_writer.py"]
    CSV["src/anonymization/mapping_csv.py"]

    Discovery["src/cli/file_discovery.py"]

    API --> Discovery
    API --> Export
    CLI --> Discovery
    CLI --> Export
    Webapp --> Export
    Webapp --> Metadata

    Export --> Plan
    Export --> Draw
    Export --> Filter
    Export --> Writer
    Export --> CSV
```

The REST API intentionally reuses CLI file discovery and the shared export pipeline.

---

## 4. Use case diagram

```mermaid
flowchart TB
    Researcher["Researcher / User"]
    Developer["Developer"]
    InstallerUser["Windows user"]
    Maintainer["Maintainer"]

    subgraph System["Clinical Image Anonymizer"]
        UC1["Install application"]
        UC2["Open GUI"]
        UC3["Upload image batch"]
        UC4["Inspect metadata"]
        UC5["Draw or define censoring rectangles"]
        UC6["Preview anonymized images"]
        UC7["Export anonymized images"]
        UC8["Run CLI batch export"]
        UC9["Run REST API batch export"]
        UC10["Run tests"]
        UC11["Build installer"]
        UC12["Update documentation"]
    end

    InstallerUser --> UC1
    Researcher --> UC2
    Researcher --> UC3
    Researcher --> UC4
    Researcher --> UC5
    Researcher --> UC6
    Researcher --> UC7
    Researcher --> UC8
    Researcher --> UC9

    Developer --> UC10
    Developer --> UC11
    Developer --> UC12
    Maintainer --> UC10
    Maintainer --> UC11
    Maintainer --> UC12
```

---

## 5. GUI batch anonymization sequence

```mermaid
sequenceDiagram
    actor User
    participant GUI as Gradio GUI
    participant State as UI State
    participant Metadata as Metadata Inspector
    participant Preview as Preview Renderer
    participant Export as Export Pipeline
    participant FS as Local Filesystem

    User->>GUI: Upload images
    GUI->>State: Store file paths and batch index
    GUI->>Metadata: Inspect current image metadata
    Metadata-->>GUI: Original and anonymized metadata preview
    GUI->>Preview: Render original/anonymized preview
    Preview-->>GUI: Preview images

    User->>GUI: Add censoring rectangles
    GUI->>State: Store rectangle state
    GUI->>Preview: Re-render preview with rectangles
    Preview-->>GUI: Updated preview

    User->>GUI: Export
    GUI->>Export: export_anonymized_images(paths, output, rectangles)
    Export->>FS: Write anonymized image copies
    Export->>FS: Write mapping.csv
    Export-->>GUI: Export status
    GUI-->>User: Show success or error message
```

---

## 6. CLI batch anonymization sequence

```mermaid
sequenceDiagram
    actor User
    participant CLI as CLI
    participant Discovery as File Discovery
    participant Export as Export Pipeline
    participant Core as Anonymization Core
    participant FS as Local Filesystem

    User->>CLI: Run clinical-image-anonymizer command
    CLI->>Discovery: discover_input_images(input, recursive)
    Discovery-->>CLI: Supported image paths
    CLI->>Export: export_anonymized_images(...)
    Export->>Core: Apply rectangles and remove metadata
    Core-->>Export: Anonymized image data
    Export->>FS: Save renamed output images
    Export->>FS: Save mapping.csv
    Export-->>CLI: Export summary
    CLI-->>User: Print result
```

---

## 7. REST API batch anonymization sequence

```mermaid
sequenceDiagram
    actor Client
    participant API as FastAPI REST API
    participant Service as API Service
    participant Discovery as File Discovery
    participant Export as Export Pipeline
    participant FS as Server Filesystem

    Client->>API: POST /anonymize-batch
    API->>API: Validate request schema
    API->>Service: anonymize_batch(request)
    Service->>Discovery: discover_input_images(input_dir, recursive)
    Discovery-->>Service: Image paths
    Service->>Export: export_anonymized_images(...)
    Export->>FS: Save anonymized images
    Export->>FS: Save mapping.csv
    Export-->>Service: Export mappings
    Service-->>API: Response model
    API-->>Client: JSON response
```

Important: API paths are interpreted on the server machine, not the client machine.

---

## 8. Export pipeline activity diagram

```mermaid
flowchart TD
    Start([Start export])
    ValidateInput["Validate input paths"]
    Discover["Discover supported image files"]
    BuildPlan["Build export plan"]
    CheckExisting["Check existing outputs"]
    OpenImage["Open image"]
    ExifTranspose["Apply EXIF transpose"]
    FilterRects["Select rectangles for image"]
    DrawRects["Apply black rectangles"]
    RemoveMetadata["Save image without metadata"]
    WriteCSV["Write mapping.csv"]
    Finish([Finish])

    Start --> ValidateInput
    ValidateInput --> Discover
    Discover --> BuildPlan
    BuildPlan --> CheckExisting
    CheckExisting --> OpenImage
    OpenImage --> ExifTranspose
    ExifTranspose --> FilterRects
    FilterRects --> DrawRects
    DrawRects --> RemoveMetadata
    RemoveMetadata --> WriteCSV
    WriteCSV --> Finish
```

---

## 9. Output naming and mapping flow

```mermaid
flowchart LR
    Input["Original image paths"]
    Randomize{"Randomize?"}
    Prefix["Optional prefix"]
    Numbering["Sequential numbering<br/>0001, 0002, ..."]
    OutputNames["Output file names"]
    Mapping["mapping.csv"]

    Input --> Randomize
    Randomize --> Numbering
    Prefix --> OutputNames
    Numbering --> OutputNames
    Input --> Mapping
    OutputNames --> Mapping
```

The mapping file links original filenames to anonymized output filenames.

---

## 10. Rectangle application logic

```mermaid
flowchart TD
    Rectangles["Rectangle list"]
    Image["Current source image"]
    Filename["Image filename"]
    Global["Global rectangles<br/>All_images"]
    Specific["Image-specific rectangles"]
    Apply["Apply black censoring"]
    Output["Anonymized image"]

    Rectangles --> Global
    Rectangles --> Specific
    Image --> Filename
    Filename --> Specific
    Global --> Apply
    Specific --> Apply
    Image --> Apply
    Apply --> Output
```

Rectangles can apply to all images or only to a named image.

---

## 11. REST API deployment modes

```mermaid
flowchart TB
    subgraph Recommended["Recommended v1.0.0"]
        Localhost["127.0.0.1<br/>localhost only"]
        SameMachine["Client and server on same machine"]
    end

    subgraph Experimental["Experimental LAN mode"]
        LANHost["0.0.0.0<br/>listen on network"]
        LANClient["Client on trusted LAN"]
        Firewall["Firewall allows selected port"]
        ServerPaths["Paths exist on server machine"]
    end

    subgraph NotSupported["Not supported"]
        Internet["Public internet exposure"]
        ClinicalProd["Clinical production deployment"]
        NoAuth["No authentication"]
        NoTLS["No HTTPS/TLS"]
    end

    Localhost --> SameMachine

    LANHost --> LANClient
    LANClient --> Firewall
    Firewall --> ServerPaths

    Internet -. avoid .-> NoAuth
    ClinicalProd -. requires hardening .-> NoTLS
```

The REST API can be used on a network only under the user's responsibility and only with appropriate privacy/security controls.

---

## 12. Build and release flow

```mermaid
flowchart TD
    Dev["Development branch"]
    Tests["Run pytest"]
    Merge["Merge stable changes to main"]
    PyGUI["Build GUI with PyInstaller"]
    PyCLI["Build CLI with PyInstaller"]
    Inno["Build installer with Inno Setup"]
    Install["Install on clean test environment"]
    Smoke["Smoke test GUI, CLI, API"]
    Tag["Create release tag"]
    Release["GitHub release"]

    Dev --> Tests
    Tests --> Merge
    Merge --> PyGUI
    PyGUI --> PyCLI
    PyCLI --> Inno
    Inno --> Install
    Install --> Smoke
    Smoke --> Tag
    Tag --> Release
```

Release tags should be created only after GUI, CLI, REST API, installer, documentation, and final smoke tests pass.

---

## 13. Component responsibility matrix

| Component | Responsibility | Should not do |
|---|---|---|
| `src/anonymization` | Core image anonymization, metadata handling, export plan, mapping CSV | Own GUI/API/CLI behavior |
| `src/webapp` | Gradio UI and user interaction | Duplicate anonymization logic |
| `src/cli` | Terminal interface and file discovery | Implement separate export logic |
| `src/api` | HTTP request validation and REST endpoints | Implement separate image processing |
| `src/common` | Reusable utilities | Contain project-specific UI flow |
| `installer/` | Windows installer script | Contain application logic |
| `docs/` | User, developer, API, and installer documentation | Store generated outputs or private data |

---

## 14. Future architecture extensions

```mermaid
flowchart LR
    Current["v1.0.0<br/>2D local-first anonymizer"]
    ThreeD["Future: 3D volume support"]
    OCR["Future: OCR-assisted detection"]
    Drawing["Future: freehand and editable rectangle UI"]
    Queue["Future: API job queue"]
    Auth["Future: API authentication"]
    Audit["Future: audit logging policy"]

    Current --> ThreeD
    Current --> OCR
    Current --> Drawing
    Current --> Queue
    Queue --> Auth
    Auth --> Audit
```

Future features should remain modular and should reuse existing core abstractions where possible.
