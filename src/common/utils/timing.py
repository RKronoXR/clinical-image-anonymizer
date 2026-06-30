"""Reusable timing utilities."""

from __future__ import annotations

from time import perf_counter


class Timer:
    """Simple reusable execution timer."""

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, *_):
        self.end = perf_counter()
        self.elapsed = self.end - self.start