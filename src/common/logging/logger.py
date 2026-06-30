"""Reusable logging utilities."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger