# ACTA AI Lab - Clinical Image Anonymizer
# Source inspection for metadata/authorship/release checks.
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
Write-Host "=== pyproject.toml ==="
if (Test-Path .\pyproject.toml) {
    Get-Content .\pyproject.toml
} else {
    Write-Host "Missing pyproject.toml"
}

Write-Host ""
Write-Host "=== version_info.txt ==="
if (Test-Path .\version_info.txt) {
    Get-Content .\version_info.txt
} else {
    Write-Host "Missing version_info.txt"
}

Write-Host ""
Write-Host "=== clinical_image_anonymizer.spec ==="
if (Test-Path .\clinical_image_anonymizer.spec) {
    Get-Content .\clinical_image_anonymizer.spec
} else {
    Write-Host "Missing clinical_image_anonymizer.spec"
}

Write-Host ""
Write-Host "=== clinical_image_anonymizer_cli.spec ==="
if (Test-Path .\clinical_image_anonymizer_cli.spec) {
    Get-Content .\clinical_image_anonymizer_cli.spec
} else {
    Write-Host "Missing clinical_image_anonymizer_cli.spec"
}

Write-Host ""
Write-Host "=== src/api routes and schemas ==="
Get-ChildItem .\src\api -Recurse -File -Include *.py -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host ""
    Write-Host "--- $($_.FullName) ---"
    Get-Content $_.FullName
}

Write-Host ""
Write-Host "=== src/cli files ==="
Get-ChildItem .\src\cli -Recurse -File -Include *.py -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host ""
    Write-Host "--- $($_.FullName) ---"
    Get-Content $_.FullName
}
