# Installer, GUI, and CLI Usage

This document explains how to use the Windows installer, the graphical interface, and the command-line interface.

---

## Recommended distribution for normal users

For normal users, distribute the Windows installer:

```text
ClinicalImageAnonymizerSetup_v1.0.0.exe
```

The installer packages:

- The graphical user interface.
- The command-line executable.
- Required internal application files.
- Optional Start Menu and Desktop shortcuts.
- Optional user PATH configuration for the CLI.

Users should not receive only:

```text
Clinical Image Anonymizer.exe
```

from the PyInstaller `dist` folder, because the GUI executable depends on the `_internal` folder when built in PyInstaller `onedir` mode.

---

## Install the application

Run the installer:

```text
ClinicalImageAnonymizerSetup_v1.0.0.exe
```

During installation, optional tasks may include:

- Create a desktop shortcut.
- Add the Clinical Image Anonymizer CLI to the user PATH.

For CLI use, enable:

```text
Add Clinical Image Anonymizer CLI to the user PATH
```

After installation, open a new terminal before testing the CLI, because Windows only reloads PATH for new terminal sessions.

---

## Open the GUI

Use one of these options:

1. Start Menu shortcut:

```text
Clinical Image Anonymizer
```

2. Desktop shortcut, if selected during installation.

3. Installed executable:

```powershell
& "C:\Program Files\Clinical Image Anonymizer\Clinical Image Anonymizer.exe"
```

The GUI opens a local browser interface.

---

## GUI workflow

Basic workflow:

1. Open the GUI.
2. Upload one or more images.
3. Inspect metadata.
4. Add black rectangles over regions that must be censored.
5. Preview the anonymized result.
6. Choose an output folder.
7. Choose an optional filename prefix.
8. Enable or disable randomized output order.
9. Export anonymized copies.

The software is designed to write anonymized copies to the output folder. It should not modify, move, rename, overwrite, crop, delete, or replace original input files.

---

## Closing the GUI

The GUI runs a local Gradio server. Closing the browser tab may not always immediately stop the local server process.

If the server remains active, opening the application again should reuse the existing local server instead of starting a duplicate server.

---

## Run the CLI from PATH

Open a new PowerShell terminal.

Check version:

```powershell
clinical-image-anonymizer --version
```

Show help:

```powershell
clinical-image-anonymizer --help
```

---

## Run the CLI directly from installation folder

If PATH was not enabled during installation:

```powershell
& "C:\Program Files\Clinical Image Anonymizer\clinical-image-anonymizer.exe" --version
```

---

## CLI examples

### Export a folder without rectangles

```powershell
clinical-image-anonymizer `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\cli_test_01"
```

### Export with prefix

```powershell
clinical-image-anonymizer `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\cli_test_prefix" `
  --prefix "Anon_"
```

### Export with random order

```powershell
clinical-image-anonymizer `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\cli_test_random" `
  --prefix "Random_" `
  --randomize
```

### Export with rectangles

```powershell
clinical-image-anonymizer `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\cli_test_rectangles" `
  --rects "[[10,20,220,90],[250,40,480,140],[40,180,180,320]]" `
  --prefix "Rect_" `
  --workers 4
```

### Full CLI test

```powershell
clinical-image-anonymizer `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\cli_test_full" `
  --rects "[[10,20,220,90],[250,40,480,140],[40,180,180,320]]" `
  --prefix "Full_" `
  --randomize `
  --recursive `
  --workers 9999
```

If `workers` is set very high, the application should internally limit practical execution to available resources.

---

## Output files

The output folder contains:

- Anonymized image files.
- `mapping.csv`, linking original names to exported names.

Example:

```text
outputs\cli_test_full\
├── Full_0001.png
├── Full_0002.png
└── mapping.csv
```

---

## Safety notes

- Always verify exported images before sharing.
- Do not assume metadata removal alone is sufficient if visible identifiers remain in the image.
- Use rectangles to censor visible identifiers.
- Keep original clinical data in secure, approved locations.
- Do not commit images, datasets, outputs, models, or private data to Git.
