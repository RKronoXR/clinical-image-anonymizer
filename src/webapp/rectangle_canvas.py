from __future__ import annotations

import base64
import html
import io
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

from src.webapp.callbacks import get_uploaded_file_path
from src.webapp.rectangle_state import format_rectangles


def _image_to_data_url(file_path: str | Path | None) -> tuple[str | None, int, int]:
    if file_path is None:
        return None, 0, 0

    with Image.open(file_path) as image:
        image = ImageOps.exif_transpose(image)
        image.load()
        rgb_image = image.convert("RGB")

    buffer = io.BytesIO()
    rgb_image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}", rgb_image.width, rgb_image.height


def render_rectangle_canvas(file: Any, rectangles: list[dict] | None) -> str:
    file_path = get_uploaded_file_path(file)
    data_url, image_width, image_height = _image_to_data_url(file_path)

    if data_url is None:
        return "<p>Upload an image to draw rectangles.</p>"

    rectangles_json = html.escape(json.dumps(rectangles or []), quote=True)

    return f"""
<div>
  <p style="margin: 0 0 8px 0;">
    Draw mode: click and drag on the image, then release.
  </p>

  <canvas
    id="rectangle-canvas"
    width="{image_width}"
    height="{image_height}"
    data-rectangles="{rectangles_json}"
    style="
      max-width: 100%;
      height: auto;
      border: 1px solid #ccc;
      cursor: crosshair;
      display: block;
    "
  ></canvas>
</div>

<script>
(function() {{
  const canvas = document.getElementById("rectangle-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const image = new Image();
  image.src = "{data_url}";

  let rectangles = JSON.parse(canvas.dataset.rectangles || "[]");
  let isDrawing = false;
  let startX = 0;
  let startY = 0;
  let currentX = 0;
  let currentY = 0;

  function getPoint(event) {{
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    return {{
      x: Math.round((event.clientX - rect.left) * scaleX),
      y: Math.round((event.clientY - rect.top) * scaleY)
    }};
  }}

  function drawRectangle(rectangle, preview) {{
    ctx.lineWidth = preview ? 2 : 4;
    ctx.strokeStyle = preview ? "orange" : "red";
    ctx.strokeRect(
      rectangle.x,
      rectangle.y,
      rectangle.width,
      rectangle.height
    );
  }}

  function redraw(previewRectangle) {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0);

    rectangles.forEach(function(rectangle) {{
      drawRectangle(rectangle, false);
    }});

    if (previewRectangle) {{
      drawRectangle(previewRectangle, true);
    }}
  }}

  function syncRectangles() {{
    const target = document.querySelector("#rectangle_canvas_payload textarea");
    if (!target) return;

    target.value = JSON.stringify(rectangles);
    target.dispatchEvent(new Event("input", {{ bubbles: true }}));
    target.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}

  image.onload = function() {{
    redraw(null);
  }};

  canvas.addEventListener("mousedown", function(event) {{
    const point = getPoint(event);
    isDrawing = true;
    startX = point.x;
    startY = point.y;
    currentX = point.x;
    currentY = point.y;
  }});

  canvas.addEventListener("mousemove", function(event) {{
    if (!isDrawing) return;

    const point = getPoint(event);
    currentX = point.x;
    currentY = point.y;

    const previewRectangle = {{
      x: Math.min(startX, currentX),
      y: Math.min(startY, currentY),
      width: Math.max(1, Math.abs(currentX - startX)),
      height: Math.max(1, Math.abs(currentY - startY))
    }};

    redraw(previewRectangle);
  }});

  canvas.addEventListener("mouseup", function(event) {{
    if (!isDrawing) return;
    isDrawing = false;

    const point = getPoint(event);
    currentX = point.x;
    currentY = point.y;

    const rectangle = {{
      x: Math.min(startX, currentX),
      y: Math.min(startY, currentY),
      width: Math.max(1, Math.abs(currentX - startX)),
      height: Math.max(1, Math.abs(currentY - startY))
    }};

    rectangles.push(rectangle);
    redraw(null);
    syncRectangles();
  }});

  canvas.addEventListener("mouseleave", function() {{
    if (!isDrawing) return;
    isDrawing = false;
    redraw(null);
  }});
}})();
</script>
"""


def sync_canvas_rectangles(
    payload: str | None,
    rectangles: list[dict] | None,
) -> tuple[list[dict], str]:
    if not payload:
        return rectangles or [], format_rectangles(rectangles)

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return rectangles or [], format_rectangles(rectangles)

    if not isinstance(parsed, list):
        return rectangles or [], format_rectangles(rectangles)

    cleaned: list[dict] = []

    for item in parsed:
        if not isinstance(item, dict):
            continue

        cleaned.append(
            {
                "x": max(0, int(item.get("x", 0))),
                "y": max(0, int(item.get("y", 0))),
                "width": max(1, int(item.get("width", 1))),
                "height": max(1, int(item.get("height", 1))),
            }
        )

    return cleaned, format_rectangles(cleaned)