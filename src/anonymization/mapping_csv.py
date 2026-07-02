from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from src.anonymization.export import ExportMapping


def write_mapping_csv(
    mappings: Iterable[ExportMapping],
    csv_path: Path,
) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "original_name",
                "new_name",
            ],
        )

        writer.writeheader()

        for item in mappings:
            writer.writerow(
                {
                    "original_name": item.original_name,
                    "new_name": item.new_name,
                }
            )