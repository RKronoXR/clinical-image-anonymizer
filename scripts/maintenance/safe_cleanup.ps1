# ACTA AI Lab - Clinical Image Anonymizer
# Safe cleanup for generated local artifacts.
#
# Default mode:
#   Lists generated/disposable artifacts that can be safely removed.
#
# Apply mode:
#   Removes only untracked generated/disposable artifacts.
#
# This script deliberately does NOT remove:
#   - .git/
#   - .venv/
#   - data/
#   - outputs/
#   - runs/
#   - tracked source files
#   - tracked documentation
#   - tracked installer scripts
#   - tracked icons
#   - tracked PyInstaller spec files
#   - tracked version metadata

param(
    [switch]$Apply,
    [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$ExcludedRootFolders = @(
    ".git",
    ".venv",
    "data",
    "outputs",
    "runs"
)

$GeneratedDirectoryNames = @(
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".tmp",
    "temp",
    "build",
    "dist"
)

$GeneratedFilePatterns = @(
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.tmp",
    "*.temp",
    "*.bak",
    "*.orig",
    "*.rej",
    ".DS_Store",
    "Thumbs.db"
)

function Get-RelativePath {
    param(
        [string]$BasePath,
        [string]$TargetPath
    )

    $baseUri = New-Object System.Uri(($BasePath.TrimEnd('\') + '\'))
    $targetUri = New-Object System.Uri($TargetPath)
    return [System.Uri]::UnescapeDataString(
        $baseUri.MakeRelativeUri($targetUri).ToString().Replace('/', '\')
    )
}

function Test-IsInsideExcludedRoot {
    param(
        [string]$RelativePath
    )

    foreach ($Root in $ExcludedRootFolders) {
        if ($RelativePath -eq $Root -or $RelativePath.StartsWith("$Root\")) {
            return $true
        }
    }

    return $false
}

function Test-IsTrackedByGit {
    param(
        [string]$RelativePath
    )

    git ls-files --error-unmatch -- "$RelativePath" *> $null
    return ($LASTEXITCODE -eq 0)
}

if (-not (Test-Path $ProjectPath)) {
    Write-Host "Project path not found:"
    Write-Host $ProjectPath
    exit 1
}

Set-Location $ProjectPath

Write-Host ""
Write-Host "=== Clinical Image Anonymizer Safe Cleanup ==="
Write-Host ""

Write-Host "Current path:"
Get-Location

Write-Host ""
Write-Host "Current Git branch:"
git branch --show-current

Write-Host ""
Write-Host "Git status before cleanup:"
git status --short

$Candidates = New-Object System.Collections.Generic.List[string]

Get-ChildItem -Path . -Recurse -Force -Directory |
    ForEach-Object {
        $RelativePath = Get-RelativePath -BasePath (Get-Location).Path -TargetPath $_.FullName

        if (Test-IsInsideExcludedRoot -RelativePath $RelativePath) {
            return
        }

        if ($GeneratedDirectoryNames -contains $_.Name -or $_.Name -like "*.egg-info") {
            if (-not (Test-IsTrackedByGit -RelativePath $RelativePath)) {
                $Candidates.Add($RelativePath)
            }
        }
    }

Get-ChildItem -Path . -Recurse -Force -File |
    ForEach-Object {
        $RelativePath = Get-RelativePath -BasePath (Get-Location).Path -TargetPath $_.FullName

        if (Test-IsInsideExcludedRoot -RelativePath $RelativePath) {
            return
        }

        foreach ($Pattern in $GeneratedFilePatterns) {
            if ($_.Name -like $Pattern) {
                if (-not (Test-IsTrackedByGit -RelativePath $RelativePath)) {
                    $Candidates.Add($RelativePath)
                }
                break
            }
        }
    }

$UniqueCandidates = $Candidates | Sort-Object -Unique

Write-Host ""
if ($Apply) {
    Write-Host "=== Apply mode: removing untracked generated artifacts ==="
} else {
    Write-Host "=== Dry-run mode: candidates only, no files removed ==="
}

foreach ($Candidate in $UniqueCandidates) {
    if ($Apply) {
        if (Test-Path $Candidate) {
            Write-Host "Removing: $Candidate"
            Remove-Item -LiteralPath $Candidate -Recurse -Force
        }
    } else {
        Write-Host "Candidate: $Candidate"
    }
}

Write-Host ""
Write-Host "Git status after cleanup:"
git status --short

Write-Host ""
if ($Apply) {
    Write-Host "Cleanup completed."
} else {
    Write-Host "Dry run completed. Re-run with -Apply to remove candidates."
}
