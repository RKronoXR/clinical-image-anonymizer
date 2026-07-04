# ACTA AI Lab - Clinical Image Anonymizer
# Installer source inspection.
# This script does NOT modify files.

param(
    [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ProjectPath)) {
    Write-Host "Project path not found:"
    Write-Host $ProjectPath
    exit 1
}

Set-Location $ProjectPath

Write-Host "=== Branch ==="
git branch --show-current

Write-Host ""
Write-Host "=== Git status ==="
git status --short

Write-Host ""
Write-Host "=== installer/clinical_image_anonymizer.iss ==="
if (Test-Path .\installer\clinical_image_anonymizer.iss) {
    Get-Content .\installer\clinical_image_anonymizer.iss
} else {
    Write-Host "Missing installer/clinical_image_anonymizer.iss"
}

Write-Host ""
Write-Host "=== docs/build_installer.md ==="
if (Test-Path .\docs\build_installer.md) {
    Get-Content .\docs\build_installer.md
} else {
    Write-Host "Missing docs/build_installer.md"
}

Write-Host ""
Write-Host "=== Existing launcher/build scripts ==="
Get-ChildItem -Path . -Recurse -File |
    Where-Object {
        $_.FullName -match "launcher|build|installer|pyinstaller|inno|cli" -and
        $_.FullName -notmatch "\\.venv\\|\\__pycache__\\|\\dist\\|\\build\\"
    } |
    Select-Object FullName
