# ACTA AI Lab - Clinical Image Anonymizer
# Safe local repository audit.
# This script does NOT delete, move, stage, or commit files.

param(
    [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Clinical Image Anonymizer Repository Audit ==="
Write-Host ""

if (-not (Test-Path $ProjectPath)) {
    Write-Host "Project path not found:"
    Write-Host $ProjectPath
    exit 1
}

Set-Location $ProjectPath

Write-Host ""
Write-Host "=== Current path ==="
Get-Location

Write-Host ""
Write-Host "=== Current Git branch ==="
git branch --show-current

Write-Host ""
Write-Host "=== Git status short ==="
git status --short

Write-Host ""
Write-Host "=== Git status ignored short ==="
git status --ignored --short

Write-Host ""
Write-Host "=== Local and remote branches ==="
git branch -a

Write-Host ""
Write-Host "=== Last 10 commits ==="
git log --oneline -10

Write-Host ""
Write-Host "=== Generated or disposable folders to review manually ==="
Get-ChildItem -Path . -Recurse -Force -Directory |
    Where-Object {
        $_.FullName -notmatch "\\.git\\|\\.venv\\|\\data\\|\\outputs\\|\\runs\\" -and
        (
            $_.Name -in @("build", "dist", "__pycache__", ".pytest_cache", ".ruff_cache") -or
            $_.Name -like "*.egg-info"
        )
    } |
    Select-Object FullName

Write-Host ""
Write-Host "=== Potential generated files to review manually ==="
Get-ChildItem -Path . -Recurse -Force -File |
    Where-Object {
        $_.FullName -notmatch "\\.git\\|\\.venv\\|\\data\\|\\outputs\\|\\runs\\" -and
        (
            $_.Name -like "*.pyc" -or
            $_.Name -like "*.pyo" -or
            $_.Name -like "*.log" -or
            $_.Name -like "*.tmp" -or
            $_.Name -like "*.bak"
        )
    } |
    Select-Object FullName, Length

Write-Host ""
Write-Host "=== Important tracked files related to release/docs ==="
git ls-files |
    Select-String -Pattern "installer|pyinstaller|version_info|icon|README|CHANGELOG|LICENSE|CITATION|DISCLAIMER|docs/|TESTING" |
    ForEach-Object { $_.Line }

Write-Host ""
Write-Host "=== Audit completed. No files were modified. ==="
