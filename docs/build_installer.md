# Build Installer

This document explains how to build the Windows executable and installer for Clinical Image Anonymizer.

## Requirements

Install development dependencies from the project root:

```powershell
pip install -r requirements-dev.txt
```

The Windows installer requires Inno Setup.

## Build the GUI executable

From the project root:

```powershell
Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue
pyinstaller --noconfirm clinical_image_anonymizer.spec
```

The GUI executable is created at:

```text
dist/Clinical Image Anonymizer/Clinical Image Anonymizer.exe
```

The GUI executable is built without a visible console window.

## Build the CLI executable

From the project root:

```powershell
pyinstaller --noconfirm clinical_image_anonymizer_cli.spec
```

The CLI executable is created at:

```text
dist/clinical-image-anonymizer.exe
```

The CLI executable supports:

```powershell
.\dist\clinical-image-anonymizer.exe --help
.\dist\clinical-image-anonymizer.exe --version
```

## Build both executables

From the project root:

```powershell
Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue
pyinstaller --noconfirm clinical_image_anonymizer.spec
pyinstaller --noconfirm clinical_image_anonymizer_cli.spec
```

## Gradio packaging note

Gradio 5 reads some of its own Python files as text at runtime.

For that reason, the GUI PyInstaller spec must include:

```python
collect_data_files("gradio", include_py_files=True)
```

Without this, the executable may fail with missing files such as:

```text
gradio/blocks_events.py
```

## Test the GUI executable

Run:

```powershell
.\dist\"Clinical Image Anonymizer"\"Clinical Image Anonymizer.exe"
```

Expected behavior:

- no console window remains visible;
- the browser opens automatically;
- the favicon uses the dental icon;
- closing the app process stops the local server;
- closing only the browser tab may leave the local server running.

## Test the CLI executable before installer build

Run:

```powershell
.\dist\clinical-image-anonymizer.exe --version
.\dist\clinical-image-anonymizer.exe --help
```

Expected behavior:

- `--version` shows version 1.0.0;
- `--version` shows the author and ACTA AI Lab;
- `--help` shows input, output, rectangles, workers, recursive mode, randomize mode, and dry run options;
- the help text states that original images are not modified.

## Build the Windows installer

Open Inno Setup and compile:

```text
installer/clinical_image_anonymizer.iss
```

The installer is created at:

```text
dist/installer/ClinicalImageAnonymizerSetup_v1.0.0.exe
```

## Installer behavior

The installer installs:

```text
Clinical Image Anonymizer.exe
clinical-image-anonymizer.exe
```

The installer can optionally add the installation folder to the user PATH.

After installation, a new PowerShell window should support:

```powershell
clinical-image-anonymizer --version
clinical-image-anonymizer --help
```

If the command is not recognized immediately, close PowerShell and open a new PowerShell window.

## Recommended use for large batches

For many images, prefer the CLI:

```powershell
clinical-image-anonymizer --input "C:\path\to\images" --output "C:\path\to\output" --workers 4 --recursive
```

The CLI is better for large batches because it supports path-based batch processing and worker configuration without loading all images into the GUI preview workflow.

## Final smoke test checklist

After installing from the generated installer, verify:

- desktop shortcut opens the GUI;
- browser opens automatically;
- favicon displays the dental icon;
- GUI About section shows version, author, organization, and repository;
- CLI works from PowerShell using `clinical-image-anonymizer --help`;
- CLI works from a folder outside the repository;
- exported outputs are new copies;
- original images remain unchanged;
- automated tests pass from the repository.
