"""Reusable project path management."""

from __future__ import annotations

from pathlib import Path


class ProjectPaths:
    """Centralized access to project directories."""

    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[3]

        self.src = self.project_root / "src"
        self.configs = self.project_root / "configs"
        self.data = self.project_root / "data"
        self.docs = self.project_root / "docs"
        self.tests = self.project_root / "tests"
        self.runs = self.project_root / "runs"
        self.outputs = self.project_root / "outputs"
        self.scripts = self.project_root / "scripts"

    def create_directories(self) -> None:
        """Create required project directories if missing."""

        for directory in (
            self.configs,
            self.data,
            self.docs,
            self.tests,
            self.runs,
            self.outputs,
            self.scripts,
        ):
            directory.mkdir(parents=True, exist_ok=True)


paths = ProjectPaths()