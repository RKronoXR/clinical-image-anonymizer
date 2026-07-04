# Testing

This document explains how to run automated and manual tests for Clinical Image Anonymizer.

Testing is required before commits, merges, installer builds, and releases.

---

## Quick test command

From the project root:

```powershell
cd C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer

python -m pytest
```

Expected result:

```text
passed
```

Warnings may appear depending on third-party packages. A warning is not automatically a failure, but new warnings should be reviewed.

---

## Recommended pre-commit checklist

Before each commit:

```powershell
git status
python -m pytest
git status
```

Commit only intentional files.

Do not commit:

- Clinical images
- Datasets
- Output folders
- Build folders
- Installer outputs
- Mapping files with private study information
- Secrets
- Temporary instruction files

---

## Run specific test files

API tests:

```powershell
python -m pytest tests/test_api_smoke.py
```

Webapp smoke tests:

```powershell
python -m pytest tests/test_webapp_smoke.py
```

Export tests:

```powershell
python -m pytest tests/test_export_anonymized_images.py
```

Anonymization smoke tests:

```powershell
python -m pytest tests/test_anonymization_smoke.py
```

Infrastructure tests:

```powershell
python -m pytest tests/test_infrastructure_smoke.py
```

---

## Run a single test

Use the `file::test_name` format:

```powershell
python -m pytest tests/test_api_smoke.py::test_api_health
```

---

## Current test coverage overview

| Area | Test file | Purpose |
|---|---|---|
| API | `tests/test_api_smoke.py` | Health, version, and batch anonymization endpoint smoke tests |
| Webapp | `tests/test_webapp_smoke.py` | Confirms the Gradio app can be built |
| Export | `tests/test_export_anonymized_images.py` | Confirms exported images and mapping CSV are created |
| Anonymization | `tests/test_anonymization_smoke.py` | Confirms core anonymization behavior |
| Infrastructure | `tests/test_infrastructure_smoke.py` | Confirms common infrastructure utilities |

---

## REST API manual smoke test

Start the API:

```powershell
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

In another PowerShell terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/version
```

Batch anonymization test:

```powershell
$Body = @{
  input_dir = "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images"
  output_dir = "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\api_manual_test"
  rectangles = @(
    @(10, 20, 220, 90),
    @(250, 40, 480, 140)
  )
  prefix = "Api_"
  randomize = $true
  recursive = $false
  workers = 4
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/anonymize-batch `
  -Method Post `
  -ContentType "application/json" `
  -Body $Body
```

Use a fresh output folder for each manual test unless intentionally testing overwrite behavior.

---

## CLI manual smoke test from source

```powershell
python -m src.cli.main --version
python -m src.cli.main --help
```

Full CLI test:

```powershell
python -m src.cli.main `
  --input "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\data\test_images" `
  --output "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer\outputs\cli_manual_test" `
  --rects "[[10,20,220,90],[250,40,480,140]]" `
  --prefix "Cli_" `
  --randomize `
  --workers 4
```

Verify:

```text
outputs\cli_manual_test\
├── Cli_0001.*
├── Cli_0002.*
└── mapping.csv
```

---

## GUI manual smoke test from source

Start the GUI:

```powershell
python -m src.webapp.app
```

Manual checks:

1. GUI opens in browser.
2. About panel appears on the initial screen.
3. Upload test images.
4. About panel disappears in the workspace.
5. Metadata appears.
6. Add one or more rectangles.
7. Preview updates.
8. Remove one image with the file-list `x`.
9. No reload loop occurs.
10. Export to a fresh output folder.
11. Output images and `mapping.csv` are created.
12. Clear/remove all images.
13. About panel appears again.

---

## Installer smoke test

Before building the installer:

```powershell
python -m pytest
```

Build GUI:

```powershell
pyinstaller --noconfirm clinical_image_anonymizer.spec
```

Build CLI:

```powershell
pyinstaller --noconfirm clinical_image_anonymizer_cli.spec
```

Test built GUI:

```powershell
.\dist\"Clinical Image Anonymizer"\"Clinical Image Anonymizer.exe"
```

Test built CLI:

```powershell
.\dist\clinical-image-anonymizer.exe --version
.\dist\clinical-image-anonymizer.exe --help
```

Build installer:

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\installer\clinical_image_anonymizer.iss
```

After installing:

```powershell
clinical-image-anonymizer --version
clinical-image-anonymizer --help
```

If PATH was not enabled:

```powershell
& "C:\Program Files\Clinical Image Anonymizer\clinical-image-anonymizer.exe" --version
```

---

## Maintenance audit before release

Run the repository audit script:

```powershell
.\scripts\maintenance\repo_audit.ps1
```

Run the cleanup script in dry-run mode:

```powershell
.\scripts\maintenance\safe_cleanup.ps1
```

Apply cleanup only after reviewing the dry-run output:

```powershell
.\scripts\maintenance\safe_cleanup.ps1 -Apply
```

Then run tests again:

```powershell
python -m pytest
```

---

## What to do when a test fails

1. Read the first failing test, not only the final summary.
2. Re-run only that test file.
3. Check whether the failure is due to a stale output folder.
4. Check whether the working tree has unintended files.
5. Fix the smallest possible cause.
6. Run the full suite again.
7. Commit only after the full suite passes.

Useful commands:

```powershell
git status
python -m pytest tests/test_api_smoke.py -vv
python -m pytest -x
```

---

## Release testing checklist

Before a release tag:

- `python -m pytest` passes.
- GUI manual smoke test passes.
- CLI manual smoke test passes.
- REST API manual smoke test passes.
- Installer build succeeds.
- Installed GUI opens.
- Installed CLI works.
- PATH option works from a new terminal.
- Uninstaller works.
- `git status` is clean.
- No datasets or private data are staged.
- Documentation is updated.
