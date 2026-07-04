# Clinical Image Anonymizer

Local-first tool for anonymizing common 2D clinical image files.

Clinical Image Anonymizer helps users create anonymized image copies by:

- Removing image metadata where supported.
- Applying black censoring rectangles over visible identifiers.
- Exporting renamed anonymized copies.
- Creating a `mapping.csv` file linking original names to exported names.
- Supporting GUI, CLI, and REST API workflows.

This project is developed as part of ACTA AI Lab.

---

## Status

Current target release: **v1.0.0**

Supported in this version:

- 2D image anonymization.
- Local graphical interface.
- Command-line interface.
- Windows installer.
- Local-first REST API.
- Batch export.
- Optional randomized output order.
- Mapping CSV generation.
- Metadata inspection and anonymized metadata preview.

Not supported in v1.0.0:

- 3D image volumes.
- Automatic OCR-based identifier detection.
- Clinical diagnosis.
- Clinical decision-making.
- Production clinical deployment.

---

## Important safety notice

Clinical Image Anonymizer is a research prototype.

It is **not** a medical device, **not** a clinical diagnostic tool, and **not** intended for clinical decision-making.

Users remain responsible for verifying that every exported image is sufficiently anonymized before sharing, publishing, uploading, or using it in research.

The software is designed to write anonymized copies to an output folder. It should not modify, move, rename, overwrite, crop, delete, or replace original input images.

See [`DISCLAIMER.md`](DISCLAIMER.md) for the full disclaimer.

---

## Privacy and data handling

The project is local-first. The GUI, CLI, and default REST API workflow are designed to run locally.

Do not commit or upload:

- Clinical images.
- Datasets.
- Processed datasets.
- Exported anonymized outputs unless explicitly approved.
- Mapping files containing private study information.
- Secrets or credentials.
- Trained models or large generated artifacts.

The REST API can technically be exposed on a local network, but this is experimental and must be used only under the user's responsibility with appropriate privacy and security safeguards. Un-anonymized clinical images should not travel over a network without careful institutional and technical controls.

---

## Main features

| Feature | Status |
|---|---|
| GUI image anonymization | Supported |
| CLI batch anonymization | Supported |
| REST API batch anonymization | Supported |
| Windows installer | Supported |
| Metadata inspection | Supported |
| Metadata removal on export | Supported |
| Black rectangle censoring | Supported |
| Batch output renaming | Supported |
| Randomized output order | Supported |
| `mapping.csv` export | Supported |
| 3D images | Future work |
| OCR-assisted censoring | Future work |

---

## Quick start for normal users

Install the Windows application using the installer:

```text
ClinicalImageAnonymizerSetup_v1.0.0.exe
```

Then open:

```text
Clinical Image Anonymizer
```

from the Windows Start Menu or Desktop shortcut.

For details, see:

```text
docs/installer_and_executables.md
```

---

## Quick start for CLI users

After installing the application with the PATH option enabled, open a new PowerShell terminal:

```powershell
clinical-image-anonymizer --version
clinical-image-anonymizer --help
```

Example:

```powershell
clinical-image-anonymizer `
  --input "C:\path\to\images" `
  --output "C:\path\to\output" `
  --rects "[[10,20,220,90]]" `
  --prefix "Anon_" `
  --randomize `
  --workers 4
```

For more CLI examples, see:

```text
docs/installer_and_executables.md
```

---

## Quick start for REST API users

Start the API locally:

```powershell
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

For endpoint details, PowerShell examples, curl examples, localhost/LAN guidance, and safety notes, see:

```text
docs/rest_api.md
```

---

## Quick start for developers

Clone the repository:

```powershell
git clone https://github.com/RKronoXR/clinical-image-anonymizer.git
cd clinical-image-anonymizer
```

Create and activate a Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run tests:

```powershell
python -m pytest
```

Run the GUI from source:

```powershell
python -m src.webapp.app
```

Run the CLI from source:

```powershell
python -m src.cli.main --help
```

Run the REST API from source:

```powershell
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

For full development instructions, see:

```text
docs/developer_guide.md
```

---

## Documentation

Main documentation pages:

| Document | Purpose |
|---|---|
| [`docs/getting_started.md`](docs/getting_started.md) | Quick start for users, CLI, API, and developers |
| [`docs/installer_and_executables.md`](docs/installer_and_executables.md) | Windows installer, GUI, and CLI usage |
| [`docs/build_installer.md`](docs/build_installer.md) | Build PyInstaller executables and Inno Setup installer |
| [`docs/rest_api.md`](docs/rest_api.md) | REST API usage, LAN notes, and safety guidance |
| [`docs/developer_guide.md`](docs/developer_guide.md) | Clone, environment setup, testing, and source-code development |
| [`docs/future_features.md`](docs/future_features.md) | Planned future features |
| [`docs/legal_and_citation.md`](docs/legal_and_citation.md) | License, citation, and disclaimer guidance |

Additional root documentation:

| Document | Purpose |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Architecture overview |
| [`TESTING.md`](TESTING.md) | Testing notes |
| [`PRIVACY_AND_DATA_POLICY.md`](PRIVACY_AND_DATA_POLICY.md) | Privacy and data handling policy |
| [`CHANGELOG.md`](CHANGELOG.md) | Change history |
| [`DISCLAIMER.md`](DISCLAIMER.md) | Full disclaimer |
| [`LICENSE`](LICENSE) | License text |
| [`CITATION.cff`](CITATION.cff) | Citation metadata |

---

## Project structure

```text
src/
├── anonymization/      core anonymization logic
├── api/                FastAPI REST API
├── cli/                command-line interface
├── common/             reusable utilities
├── project_specific/   project-specific extension space
└── webapp/             Gradio GUI

tests/                  automated tests
docs/                   user, developer, installer, and API documentation
installer/              Inno Setup installer script
```

The GUI, CLI, and REST API are intended to remain thin interfaces over the shared anonymization core.

---

## Build the installer

The Windows installer is built from PyInstaller outputs using Inno Setup.

Full instructions:

```text
docs/build_installer.md
```

Short version:

```powershell
python -m pytest

Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue

pyinstaller --noconfirm clinical_image_anonymizer.spec
pyinstaller --noconfirm clinical_image_anonymizer_cli.spec

& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\installer\clinical_image_anonymizer.iss
```

---

## License

Clinical Image Anonymizer is distributed under the **ACTA AI Lab Attribution License v1.0**.

You may copy, use, modify, publish, distribute, sublicense, and sell copies of the software, provided that attribution to the original project is preserved.

Required attribution:

- Project: Clinical Image Anonymizer
- Author: Ricardo Eugenio Gonzalez Valenzuela
- Organization: ACTA AI Lab
- Repository: https://github.com/RKronoXR/clinical-image-anonymizer

See [`LICENSE`](LICENSE) for the full license text.

---

## Citation

If you use Clinical Image Anonymizer for research, teaching, datasets, reports, presentations, theses, preprints, or publications, please cite the project.

Recommended acknowledgement:

> This work used Clinical Image Anonymizer v1.0.0, developed by Ricardo Eugenio Gonzalez Valenzuela at ACTA AI Lab, for local-first clinical image anonymization.

Citation metadata is available in [`CITATION.cff`](CITATION.cff).

---

## Repository

```text
https://github.com/RKronoXR/clinical-image-anonymizer
```
