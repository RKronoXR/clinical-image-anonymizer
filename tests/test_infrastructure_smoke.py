"""Infrastructure smoke test."""

from src.common.config import load_settings
from src.common.io import ensure_directory
from src.common.logging import get_logger
from src.common.paths import paths


def main() -> None:
    settings = load_settings()

    logger = get_logger("smoke")

    paths.create_directories()

    ensure_directory(paths.outputs)

    logger.info("Infrastructure smoke test passed.")

    print(f"Project      : {settings.project_name}")
    print(f"Environment  : {settings.environment}")
    print(f"Output folder: {paths.outputs}")


if __name__ == "__main__":
    main()