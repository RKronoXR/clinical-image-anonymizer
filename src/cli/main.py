from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
from typing import TypeAlias

from src.anonymization.export import export_anonymized_images
from src.anonymization.rectangle_filter import ALL_IMAGES_FILENAME
from src.cli.file_discovery import discover_input_images

Rect: TypeAlias = tuple[int, int, int, int]


def parse_rects(raw_rects: str | None) -> list[Rect]:
    if raw_rects is None or raw_rects.strip() == "":
        return []

    value = raw_rects.strip()

    if value.startswith("["):
        parsed = ast.literal_eval(value)
        rects = parsed
    else:
        rects = [value.split(",")]

    normalized: list[Rect] = []
    for rect in rects:
        if not isinstance(rect, (list, tuple)) or len(rect) != 4:
            raise argparse.ArgumentTypeError("Each rectangle must have 4 values.")

        x1, y1, x2, y2 = [int(v) for v in rect]

        if x2 <= x1 or y2 <= y1:
            raise argparse.ArgumentTypeError("Rectangle must satisfy x2 > x1 and y2 > y1.")

        normalized.append((x1, y1, x2, y2))

    return normalized


def rects_to_export_dicts(rects: list[Rect]) -> list[dict]:
    return [
        {
            "filename": ALL_IMAGES_FILENAME,
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1,
        }
        for x1, y1, x2, y2 in rects
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anonymize.py",
        description="Anonymize clinical images locally.",
    )

    parser.add_argument("--input", required=True, help="Input image file or folder.")
    parser.add_argument("--output", required=True, help="Output folder.")
    parser.add_argument("--rects", default=None, help='Example: "10,20,200,80" or "[[10,20,200,80],[30,40,100,120]]".')
    parser.add_argument("--prefix", default="", help="Optional output filename prefix.")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers. Must be positive.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument("--recursive", action="store_true", help="Process subfolders.")
    parser.add_argument("--randomize", action="store_true", help="Randomize output order.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without writing files.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.workers <= 0:
        parser.error("--workers must be a positive integer.")

    cpu_count = os.cpu_count() or 1
    if args.workers > cpu_count:
        print(f"Warning: --workers={args.workers} exceeds available CPUs. Using {cpu_count}.")
        args.workers = cpu_count

    try:
        rects = parse_rects(args.rects)
    except Exception as exc:
        parser.error(str(exc))

    input_path = Path(args.input)

    try:
        image_paths = discover_input_images(input_path, recursive=args.recursive)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    print("Clinical Image Anonymizer CLI")
    print(f"Input      : {args.input}")
    print(f"Output     : {args.output}")
    print(f"Images     : {len(image_paths)}")
    print(f"Rects      : {rects}")
    print(f"Workers    : {args.workers}")
    print(f"Recursive  : {args.recursive}")
    print(f"Randomize  : {args.randomize}")
    print(f"Overwrite  : {args.overwrite}")
    print(f"Dry run    : {args.dry_run}")

    if args.dry_run:
        print("\nDry run completed. No files were written.")
        return 0

    try:
        exported = export_anonymized_images(
            image_paths=image_paths,
            output_dir=Path(args.output),
            rectangles=rects_to_export_dicts(rects),
            prefix=args.prefix,
            randomize=args.randomize,
            overwrite=args.overwrite,
            workers=args.workers,
            input_root=input_path if input_path.is_dir() else None,
            preserve_structure=args.recursive,
            progress_callback=lambda current, total, item: print(
                f"Processing {current}/{total}: {item.original_name}"
            ),
        )
    except Exception as exc:
        parser.error(str(exc))

    print("\nRun summary:")
    print(f"Exported   : {len(exported)}")
    print(f"CSV report : {Path(args.output) / 'mapping.csv'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())