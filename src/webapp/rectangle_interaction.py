from __future__ import annotations

from typing import Any

import gradio as gr

from src.webapp.callbacks import get_uploaded_file_path
from src.webapp.preview_rendering import (
    load_preview_image,
    render_censored_preview,
    render_overlay_preview,
)
from src.webapp.rectangle_state import (
    create_rectangle,
    format_rectangles,
    rectangle_choices,
)


DEFAULT_DRAW_WIDTH = 100
DEFAULT_DRAW_HEIGHT = 100


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float)


def _rectangle_from_event_index(index: Any) -> dict | None:
    if index is None:
        return None

    if (
        isinstance(index, list | tuple)
        and len(index) == 2
        and all(_is_number(value) for value in index)
    ):
        x, y = index
        return create_rectangle(
            x=int(x),
            y=int(y),
            width=DEFAULT_DRAW_WIDTH,
            height=DEFAULT_DRAW_HEIGHT,
        )

    if (
        isinstance(index, list | tuple)
        and len(index) == 2
        and all(isinstance(point, list | tuple) and len(point) == 2 for point in index)
    ):
        x1, y1 = index[0]
        x2, y2 = index[1]

        left = min(int(x1), int(x2))
        top = min(int(y1), int(y2))
        width = abs(int(x2) - int(x1))
        height = abs(int(y2) - int(y1))

        return create_rectangle(
            x=left,
            y=top,
            width=max(1, width),
            height=max(1, height),
        )

    if (
        isinstance(index, list | tuple)
        and len(index) == 4
        and all(_is_number(value) for value in index)
    ):
        x1, y1, x2, y2 = index

        left = min(int(x1), int(x2))
        top = min(int(y1), int(y2))
        width = abs(int(x2) - int(x1))
        height = abs(int(y2) - int(y1))

        return create_rectangle(
            x=left,
            y=top,
            width=max(1, width),
            height=max(1, height),
        )

    return None


def handle_image_rectangle_draw(
    rectangles: list[dict] | None,
    file: Any,
    event: gr.SelectData,
):
    rectangle = _rectangle_from_event_index(event.index)

    current = rectangles or []
    if rectangle is None:
        file_path = get_uploaded_file_path(file)
        return (
            current,
            gr.update(choices=rectangle_choices(current), value=None),
            0,
            0,
            DEFAULT_DRAW_WIDTH,
            DEFAULT_DRAW_HEIGHT,
            format_rectangles(current),
            load_preview_image(file_path),
            render_overlay_preview(file_path, current),
            render_censored_preview(file_path, current),
        )

    updated = [*current, rectangle]
    choices = rectangle_choices(updated)
    selected = choices[-1] if choices else None
    file_path = get_uploaded_file_path(file)

    return (
        updated,
        gr.update(choices=choices, value=selected),
        rectangle["x"],
        rectangle["y"],
        rectangle["width"],
        rectangle["height"],
        format_rectangles(updated),
        load_preview_image(file_path),
        render_overlay_preview(file_path, updated),
        render_censored_preview(file_path, updated),
    )