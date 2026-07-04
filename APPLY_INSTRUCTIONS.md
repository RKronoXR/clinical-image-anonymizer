# Apply Instructions

Replace:

```text
src/webapp/event_registry.py
```

Then run:

```powershell
cd C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer

python -m pytest
python -m src.webapp.app
```

Manual check:

1. Load images.
2. Add a rectangle.
3. Remove one image using the `x` in the upload list.
4. Confirm the UI does not enter an infinite reload loop.

Commit:

```powershell
git add src/webapp/event_registry.py
git commit -m "fix(webapp): prevent file list update loop"
```
