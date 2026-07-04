# Developer Guide

This document explains how to clone, install, test, run, and modify the project from source code.

---

## Clone the repository

```powershell
cd C:\Users\rga580\KronoX-Projects

git clone https://github.com/RKronoXR/clinical-image-anonymizer.git

cd clinical-image-anonymizer
```

---

## Branch workflow

Recommended branch workflow:

```text
main                 stable branch
feature/<name>       short-lived feature branch
fix/<name>           short-lived fix branch
```

Example:

```powershell
git checkout main
git pull origin main
git checkout -b feature/my-change
```

Do not commit:

- Datasets
- Clinical images
- Processed images
- Output folders
- Models
- Checkpoints
- Secrets
- Private data
- Large generated artifacts

---

## Create a Python environment

Python 3.12 is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Optional editable install:

```powershell
pip install -e .
```

---

## Run tests

```powershell
python -m pytest
```

Run a specific test file:

```powershell
python -m pytest tests/test_api_smoke.py
```

---

## Run the GUI from source

```powershell
python -m src.webapp.app
```

The GUI opens a local browser interface.

---

## Run the CLI from source

```powershell
python -m src.cli.main --version
python -m src.cli.main --help
```

Example:

```powershell
python -m src.cli.main `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\dev_cli_test" `
  --prefix "Dev_" `
  --randomize `
  --workers 4
```

---

## Run the REST API from source

Localhost:

```powershell
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

See:

```text
docs/rest_api.md
```

for complete REST API documentation.

---

## Project structure

Important folders:

```text
src/
├── anonymization/      core anonymization logic
├── api/                FastAPI REST API
├── cli/                command-line interface
├── common/             reusable utilities
├── project_specific/   project-specific extension space
└── webapp/             Gradio GUI
```

Tests:

```text
tests/
```

Documentation:

```text
docs/
```

Installer files:

```text
installer/
clinical_image_anonymizer.spec
clinical_image_anonymizer_cli.spec
```

---

## Development principles

When modifying the project:

- Keep changes atomic.
- Reuse existing core modules.
- Avoid duplicating anonymization logic.
- Keep GUI, CLI, and API as thin interfaces over shared core functions.
- Add or update tests for new behavior.
- Keep user-facing errors clear.
- Keep private data out of Git.
- Run `python -m pytest` before committing.
- Prefer small commits with clear messages.

---

## Typical development loop

```powershell
git status
python -m pytest

# edit files

python -m pytest
git status
git add <changed-files>
git commit -m "type(scope): concise description"
```

Example commit messages:

```text
feat(api): add batch anonymization endpoint
fix(webapp): prevent file list update loop
docs(api): document REST API usage and safety
test(cli): add export smoke test
```

---

## Build from source

For installer build instructions, see:

```text
docs/build_installer.md
```

or:

```text
docs/installer_and_executables.md
```

depending on the documentation layout used in the repository.

---

## Privacy and safety

This project is local-first and designed for research workflows.

Before using with clinical data:

- Verify institutional approval.
- Verify data handling policy.
- Verify storage and transfer security.
- Verify anonymized outputs manually.
- Do not expose the REST API to public networks.
- Do not commit input or output images.
