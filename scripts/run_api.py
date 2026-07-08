from __future__ import annotations

import argparse

import uvicorn

from src.api.app import create_app


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Clinical Image Anonymizer REST API."
    )
    parser.add_argument("--host", default="127.0.0.1", help="API host.")
    parser.add_argument("--port", default=8000, type=int, help="API port.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable reload mode for development. Not recommended for packaged use.",
    )
    args = parser.parse_args()

    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
