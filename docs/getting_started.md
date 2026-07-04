# Getting Started

This page gives a quick overview of the main ways to use Clinical Image Anonymizer.

---

## For normal users

Install the Windows application using the installer:

```text
ClinicalImageAnonymizerSetup_v1.0.0.exe
```

Then open:

```text
Clinical Image Anonymizer
```

from the Start Menu.

For details, see:

```text
docs/installer_and_executables.md
```

---

## For command-line users

After installation, open a new PowerShell terminal:

```powershell
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

---

## For REST API users

Start the API locally:

```powershell
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

For details, see:

```text
docs/rest_api.md
```

---

## For developers

Clone the repository:

```powershell
git clone https://github.com/RKronoXR/clinical-image-anonymizer.git
cd clinical-image-anonymizer
```

Create environment:

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

For details, see:

```text
docs/developer_guide.md
```
