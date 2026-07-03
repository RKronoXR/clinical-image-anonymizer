# Build Installer

This document explains how to build the Windows executable for Clinical Image Anonymizer.

## Requirements

Install development dependencies:

```powershell
pip install -r requirements-dev.txt
```

## Build executable

From the project root:

```powershell
Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue
pyinstaller --noconfirm clinical_image_anonymizer.spec
```

The executable is created at:

```text
dist/Clinical Image Anonymizer/Clinical Image Anonymizer.exe
```

## Gradio packaging note

Gradio 5 reads some of its own Python files as text at runtime.

For that reason, the PyInstaller spec must include:

```python
collect_data_files("gradio", include_py_files=True)
```

Without this, the executable may fail with missing files such as:

```text
gradio/blocks_events.py
```

## Test executable

Run:

```powershell
.\dist\"Clinical Image Anonymizer"\"Clinical Image Anonymizer.exe"
```
