"""Reusable validation helpers."""

from __future__ import annotations


def ensure_not_none(value: object, name: str) -> None:
    """Ensure a value is not None."""

    if value is None:
        raise ValueError(f"{name} cannot be None")


def ensure_not_empty(text: str, name: str) -> None:
    """Ensure a string is not empty."""

    if not text.strip():
        raise ValueError(f"{name} cannot be empty")