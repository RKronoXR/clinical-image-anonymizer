from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anonymize.py",
        description="Anonymize clinical images locally by removing metadata and optionally censoring rectangular pixel regions.",
    )

    parser.add_argument("--input", required=True, help="Input image file or folder.")
    parser.add_argument("--output", required=True, help="Output folder.")
    parser.add_argument("--rects", default=None, help='Rectangle(s): "x1,y1,x2,y2" or "[[x1,y1,x2,y2],[...]]".')
    parser.add_argument("--prefix", default="", help="Optional output filename prefix.")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers. Must be positive.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files.")
    parser.add_argument("--recursive", action="store_true", help="Process subfolders and preserve folder structure.")
    parser.add_argument("--randomize", action="store_true", help="Randomize output order.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without writing files.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.workers <= 0:
        parser.error("--workers must be a positive integer.")

    print("Clinical Image Anonymizer CLI")
    print(f"Input     : {args.input}")
    print(f"Output    : {args.output}")
    print(f"Rects     : {args.rects}")
    print(f"Workers   : {args.workers}")
    print(f"Recursive : {args.recursive}")
    print(f"Dry run   : {args.dry_run}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())