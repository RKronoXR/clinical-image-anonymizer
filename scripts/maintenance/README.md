# Maintenance Scripts

This folder contains local PowerShell scripts for repository audit, cleanup, and release inspection.

These scripts are intended for maintainers. They should be run from the repository root.

---

## Scripts

| Script | Purpose | Modifies files |
|---|---|---:|
| `repo_audit.ps1` | Prints Git status, branches, recent commits, generated files, and release-related tracked files | No |
| `safe_cleanup.ps1` | Dry-runs or removes untracked generated artifacts | Only with `-Apply` |
| `inspect_installer_sources.ps1` | Prints installer script and build documentation | No |
| `inspect_metadata_sources.ps1` | Prints metadata, version, CLI, API, and spec files | No |

---

## Repository audit

```powershell
.\scripts\maintenance\repo_audit.ps1
```

With explicit project path:

```powershell
.\scripts\maintenance\repo_audit.ps1 -ProjectPath "C:\Users\rga580\KronoX-Projects\clinical-image-anonymizer"
```

---

## Safe cleanup

Dry run:

```powershell
.\scripts\maintenance\safe_cleanup.ps1
```

Apply cleanup:

```powershell
.\scripts\maintenance\safe_cleanup.ps1 -Apply
```

The cleanup script deliberately avoids:

- `.git/`
- `.venv/`
- `data/`
- `outputs/`
- `runs/`
- tracked source files
- tracked documentation
- tracked installer scripts
- tracked icons
- tracked PyInstaller spec files
- tracked version metadata

---

## Installer inspection

```powershell
.\scripts\maintenance\inspect_installer_sources.ps1
```

Use this before rebuilding or troubleshooting the Windows installer.

---

## Metadata inspection

```powershell
.\scripts\maintenance\inspect_metadata_sources.ps1
```

Use this before release checks involving version, authorship, CLI, API, and PyInstaller metadata.

---

## Recommended pre-release maintenance sequence

```powershell
git status
python -m pytest

.\scripts\maintenance\repo_audit.ps1
.\scripts\maintenance\safe_cleanup.ps1

python -m pytest
git status
```

Only use cleanup apply mode after reviewing the dry-run output:

```powershell
.\scripts\maintenance\safe_cleanup.ps1 -Apply
```
