from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from src.anonymization.export_plan import ExportMapping


def write_mapping_csv(
    mappings: Iterable[ExportMapping],
    csv_path: Path,
    statuses: dict[Path, tuple[str, str]] | None = None,
) -> None:
    statuses = statuses or {}
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "output_index",
                "original_name",
                "original_path",
                "new_name",
                "output_path",
                "status",
                "error",
            ],
        )
        writer.writeheader()

        for item in mappings:
            status, error = statuses.get(item.source_path, ("success", ""))
            writer.writerow(
                {
                    "output_index": item.output_index,
                    "original_name": item.original_name,
                    "original_path": str(item.source_path),
                    "new_name": item.new_name,
                    "output_path": str(item.output_path),
                    "status": status,
                    "error": error,
                }
            )