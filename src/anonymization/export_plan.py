
from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExportMapping:
    original_name: str
    new_name: str
    source_path: Path
    output_path: Path


def build_export_plan(
    image_paths: list[str | Path],
    output_dir: str | Path,
    prefix: str = "",
    randomize: bool = False,
) -> list[ExportMapping]:
    paths = [Path(path) for path in image_paths]

    if randomize:
        paths = paths.copy()
        random.shuffle(paths)

    output = Path(output_dir)
    plan: list[ExportMapping] = []

    for index, source in enumerate(paths, start=1):
        new_name = f"{prefix}{index:04d}{source.suffix.lower()}"
        destination = output / new_name

        plan.append(
            ExportMapping(
                original_name=source.name,
                new_name=new_name,
                source_path=source,
                output_path=destination,
            )
        )

    return plan