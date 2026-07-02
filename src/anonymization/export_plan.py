from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExportMapping:
    output_index: int
    original_name: str
    new_name: str
    source_path: Path
    output_path: Path


def build_export_plan(
    image_paths: list[str | Path],
    output_dir: str | Path,
    prefix: str = "",
    randomize: bool = False,
    input_root: str | Path | None = None,
    preserve_structure: bool = False,
) -> list[ExportMapping]:
    paths = [Path(path) for path in image_paths]

    if randomize:
        paths = paths.copy()
        random.shuffle(paths)
    else:
        paths = sorted(paths)

    output = Path(output_dir)
    root = Path(input_root).resolve() if input_root else None

    plan: list[ExportMapping] = []

    for index, source in enumerate(paths, start=1):
        source = source.resolve()
        new_name = f"{prefix}{index:04d}{source.suffix.lower()}"

        if preserve_structure and root is not None:
            relative_parent = source.parent.relative_to(root)
            destination = output / relative_parent / new_name
        else:
            destination = output / new_name

        plan.append(
            ExportMapping(
                output_index=index,
                original_name=source.name,
                new_name=new_name,
                source_path=source,
                output_path=destination,
            )
        )

    return plan