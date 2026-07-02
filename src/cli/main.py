from __future__ import annotations

import argparse
import ast
from pathlib import Path
from typing import TypeAlias

from src.cli.file_discovery import discover_input_images
from src.common.export_plan import build_export_plan

from src.cli.runner import run_export_plan

Rect: TypeAlias = tuple[int, int, int, int]


def parse_rects(raw_rects: str | None) -> list[Rect]:
    if raw_rects is None or raw_rects.strip() == "":
        return []

    value = raw_rects.strip()

    if value.startswith("["):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise argparse.ArgumentTypeError(
                '--rects must be "x1,y1,x2,y2" or "[[x1,y1,x2,y2],[...]]".'
            ) from exc

        if not isinstance(parsed, list):
            raise argparse.ArgumentTypeError("--rects list format must be a list.")

        rects = parsed
    else:
        rects = [value.split(",")]

    normalized: list[Rect] = []

    for rect in rects:
        if not isinstance(rect, (list, tuple)) or len(rect) != 4:
            raise argparse.ArgumentTypeError(
                "Each rectangle must contain exactly 4 values: x1,y1,x2,y2."
            )

        try:
            x1, y1, x2, y2 = [int(v) for v in rect]
        except (TypeError, ValueError) as exc:
            raise argparse.ArgumentTypeError("Rectangle values must be integers.") from exc

        if x2 <= x1 or y2 <= y1:
            raise argparse.ArgumentTypeError(
                "Rectangle coordinates must satisfy x2 > x1 and y2 > y1."
            )

        normalized.append((x1, y1, x2, y2))

    return normalized


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anonymize.py",
        description=(
            "Anonymize clinical images locally by removing metadata "
            "and optionally censoring rectangular pixel regions."
        ),
    )

    parser.add_argument("--input", required=True, help="Input image file or folder.")
    parser.add_argument("--output", required=True, help="Output folder.")
    parser.add_argument(
        "--rects",
        default=None,
        help='Rectangle(s): "x1,y1,x2,y2" or "[[x1,y1,x2,y2],[...]]".',
    )
    parser.add_argument("--prefix", default="", help="Optional output filename prefix.")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of workers. Must be positive.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process subfolders and preserve folder structure.",
    )
    parser.add_argument("--randomize", action="store_true", help="Randomize output order.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without writing files.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.workers <= 0:
        parser.error("--workers must be a positive integer.")

    try:
        rects = parse_rects(args.rects)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))

    input_path = Path(args.input)

    try:
        input_images = discover_input_images(input_path, recursive=args.recursive)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    try:
        export_plan = build_export_plan(
            input_images=input_images,
            output_root=Path(args.output),
            prefix=args.prefix,
            randomize=args.randomize,
            overwrite=args.overwrite,
            input_root=input_path if input_path.is_dir() else None,
            preserve_structure=args.recursive,
        )
    except (ValueError, FileExistsError) as exc:
        parser.error(str(exc))

    print("Clinical Image Anonymizer CLI")
    print(f"Input      : {args.input}")
    print(f"Output     : {args.output}")
    print(f"Images     : {len(input_images)}")
    print(f"Outputs    : {len(export_plan)}")
    print(f"Rects      : {rects}")
    print(f"Workers    : {args.workers}")
    print(f"Recursive  : {args.recursive}")
    print(f"Randomize  : {args.randomize}")
    print(f"Overwrite  : {args.overwrite}")
    print(f"Dry run    : {args.dry_run}")

    if args.dry_run:
        print("\nPlanned outputs:")
        for item in export_plan:
            print(f"- {item.input_path} -> {item.output_path}")


    if not args.dry_run:
        summary = run_export_plan(export_plan, rects=rects, overwrite=args.overwrite)

        print("\nRun summary:")
        print(f"Processed  : {summary.processed}")
        print(f"Failed     : {summary.failed}")
        print(f"CSV report : {summary.csv_path}")

        if summary.errors:
            print("\nErrors:")
            for error in summary.errors:
                print(f"- {error}")

        if summary.failed > 0:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())