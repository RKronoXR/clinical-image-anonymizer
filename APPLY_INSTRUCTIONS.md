# Apply Instructions

Copy this file over the repository root:

```text
src/webapp/app.py
```

Then run:

```powershell
cd C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer

python -m pytest

Remove-Item build, dist -Recurse -Force -ErrorAction SilentlyContinue
pyinstaller --noconfirm clinical_image_anonymizer.spec
pyinstaller --noconfirm clinical_image_anonymizer_cli.spec

.\dist\"Clinical Image Anonymizer"\"Clinical Image Anonymizer.exe"
```

If it works:

```powershell
git add src/webapp/app.py
git commit -m "fix(webapp): support PyInstaller without console"
```
