# Build the Windows Installer

This document explains how to build the Windows GUI executable, CLI executable, and installer.

---

## Prerequisites

Install:

- Python 3.12
- Project dependencies
- PyInstaller
- Inno Setup 6

Recommended Inno Setup locations:

```text
C:\Program Files (x86)\Inno Setup 6\ISCC.exe
C:\Program Files\Inno Setup 6\ISCC.exe
```

---

## Start from a clean repository state

From the project root:

```powershell
cd C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer

git status
```

Expected:

```text
nothing to commit, working tree clean
```

Run tests:

```powershell
python -m pytest
```

---

## Remove previous build artifacts

```powershell
Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue
```

---

## Build the GUI executable

```powershell
pyinstaller --noconfirm clinical_image_anonymizer.spec
```

Expected GUI output:

```text
dist\Clinical Image Anonymizer\Clinical Image Anonymizer.exe
dist\Clinical Image Anonymizer\_internal\
```

This is a PyInstaller `onedir` build. The `_internal` folder is required.

Test GUI:

```powershell
.\dist\"Clinical Image Anonymizer"\"Clinical Image Anonymizer.exe"
```

---

## Build the CLI executable

```powershell
pyinstaller --noconfirm clinical_image_anonymizer_cli.spec
```

Expected CLI output:

```text
dist\clinical-image-anonymizer.exe
```

Test CLI:

```powershell
.\dist\clinical-image-anonymizer.exe --version
.\dist\clinical-image-anonymizer.exe --help
```

---

## Build the installer with Inno Setup

Use one of these commands depending on where Inno Setup is installed:

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\installer\clinical_image_anonymizer.iss
```

or:

```powershell
& "C:\Program Files\Inno Setup 6\ISCC.exe" .\installer\clinical_image_anonymizer.iss
```

Expected installer output:

```text
dist\installer\ClinicalImageAnonymizerSetup_v1.0.0.exe
```

---

## What the installer includes

The installer includes:

- GUI executable:

```text
Clinical Image Anonymizer.exe
```

- CLI executable:

```text
clinical-image-anonymizer.exe
```

- PyInstaller internal dependencies:

```text
_internal\
```

- Start Menu shortcut.
- Optional Desktop shortcut.
- Optional user PATH entry for CLI use.

---

## Test the installed application

After installing:

### GUI

Open from Start Menu:

```text
Clinical Image Anonymizer
```

or:

```powershell
& "C:\Program Files\Clinical Image Anonymizer\Clinical Image Anonymizer.exe"
```

### CLI

Open a new PowerShell terminal:

```powershell
clinical-image-anonymizer --version
clinical-image-anonymizer --help
```

If PATH was not enabled:

```powershell
& "C:\Program Files\Clinical Image Anonymizer\clinical-image-anonymizer.exe" --version
```

---

## Installer verification checklist

Before release, verify:

- GUI opens from installed shortcut.
- CLI works from a new terminal when PATH option is enabled.
- CLI works from direct installed path.
- GUI can upload images.
- GUI can add rectangles.
- GUI can export anonymized images.
- CLI can export a test batch.
- `mapping.csv` is created.
- The installer uninstalls cleanly.
- No datasets, outputs, private data, or generated build artifacts are committed to Git.

---

## Notes on one-file executables

The current recommended build is:

```text
PyInstaller onedir + Inno Setup installer
```

A PyInstaller `onefile` portable executable is possible, but it can start more slowly because Windows must extract bundled files at runtime. For v1.0.0, the installer is the recommended distribution format.
