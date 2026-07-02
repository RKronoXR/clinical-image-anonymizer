from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Iterable

from PIL import Image, ImageOps

from src.anonymization.export_plan import ExportMapping, build_export_plan
from src.anonymization.image_writer import safe_output_format, save_without_metadata
from src.anonymization.mapping_csv import write_mapping_csv
from src.anonymization.rectangle_draw import apply_black_rectangles
from src.anonymization.rectangle_filter import rectangles_for_source


ProgressCallback = Callable[[int, int, ExportMapping], None]


def _check_existing_outputs(plan: Iterable[ExportMapping], csv_path: Path) -> None:
    existing = [item.output_path for item in plan if item.output_path.exists()]
    if csv_path.exists():
        existing.append(csv_path)

    if existing:
        names = ", ".join(path.name for path in existing[:5])
        raise FileExistsError(f"Export stopped. Existing output files found: {names}")


def _export_one_image(
    item: ExportMapping,
    rectangles: list[dict] | None,
) -> None:
    with Image.open(item.source_path) as image:
        image = ImageOps.exif_transpose(image)
        image.load()

        image_rectangles = rectangles_for_source(rectangles, item.source_path)
        anonymized = apply_black_rectangles(image, image_rectangles)
        output_format = safe_output_format(item.source_path, image.format)

        save_without_metadata(
            anonymized,
            item.output_path,
            output_format,
        )


def export_anonymized_images(
    image_paths: list[str | Path],
    output_dir: str | Path,
    rectangles: list[dict] | None,
    prefix: str = "",
    randomize: bool = False,
    csv_name: str = "mapping.csv",
    overwrite: bool = False,
    workers: int = 1,
    input_root: str | Path | None = None,
    preserve_structure: bool = False,
    progress_callback: ProgressCallback | None = None,
) -> list[ExportMapping]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    plan = build_export_plan(
        image_paths=image_paths,
        output_dir=output,
        prefix=prefix,
        randomize=randomize,
        input_root=input_root,
        preserve_structure=preserve_structure,
    )

    csv_path = output / csv_name

    if not overwrite:
        _check_existing_outputs(plan, csv_path)

    total = len(plan)
    completed = 0
    statuses: dict[Path, tuple[str, str]] = {}

    max_workers = max(1, workers)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {
            executor.submit(_export_one_image, item, rectangles): item
            for item in plan
        }

        for future in as_completed(future_to_item):
            item = future_to_item[future]

            try:
                future.result()
                statuses[item.source_path] = ("success", "")
            except Exception as exc:
                statuses[item.source_path] = ("failed", str(exc))

            completed += 1

            if progress_callback is not None:
                progress_callback(completed, total, item)

    write_mapping_csv(plan, csv_path, statuses=statuses)

    failed = [status for status, _ in statuses.values() if status == "failed"]
    if failed:
        raise RuntimeError(f"Export completed with {len(failed)} failed image(s). See {csv_path}.")

    return plan