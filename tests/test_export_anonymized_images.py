from pathlib import Path
import csv

import pytest
from PIL import Image

from src.anonymization.export import (
    apply_black_rectangles,
    build_export_plan,
    export_anonymized_images,
)
from src.anonymization.metadata import inspect_image_metadata


PRIVATE_METADATA_KEYS = {
    "artist",
    "copyright",
    "software",
    "description",
    "documentname",
    "datetime",
    "exif:315",
    "exif:270",
    "exif:305",
    "exif:306",
}


def create_test_image(path: Path) -> None:
    image = Image.new("RGB", (100, 100), (255, 255, 255))
    image.save(path)


def assert_no_private_metadata(metadata: dict[str, str]) -> None:
    keys = {key.lower() for key in metadata.keys()}
    assert PRIVATE_METADATA_KEYS.isdisjoint(keys)


def test_build_export_plan_without_prefix() -> None:
    plan = build_export_plan(["a.png", "b.png"], output_dir="output", prefix="", randomize=False)
    assert plan[0].new_name == "0001.png"
    assert plan[1].new_name == "0002.png"


def test_build_export_plan_with_prefix() -> None:
    plan = build_export_plan(["a.png", "b.png"], output_dir="output", prefix="Anon_", randomize=False)
    assert plan[0].new_name == "Anon_0001.png"
    assert plan[1].new_name == "Anon_0002.png"


def test_apply_black_rectangles() -> None:
    image = Image.new("RGB", (50, 50), (255, 255, 255))
    result = apply_black_rectangles(image, [{"x": 10, "y": 10, "width": 20, "height": 20}])
    assert result.getpixel((15, 15)) == (0, 0, 0)
    assert result.getpixel((5, 5)) == (255, 255, 255)


def test_export_creates_images_and_csv(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    create_test_image(input_dir / "img1.png")
    create_test_image(input_dir / "img2.png")

    export_anonymized_images(
        image_paths=[input_dir / "img1.png", input_dir / "img2.png"],
        output_dir=output_dir,
        rectangles=[],
        prefix="Anon_",
        randomize=False,
    )

    assert (output_dir / "Anon_0001.png").exists()
    assert (output_dir / "Anon_0002.png").exists()

    with (output_dir / "mapping.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["output_index"] == "1"
    assert rows[0]["original_name"] == "img1.png"
    assert rows[0]["new_name"] == "Anon_0001.png"
    assert rows[0]["status"] == "success"
    assert rows[0]["error"] == ""

    assert rows[1]["output_index"] == "2"
    assert rows[1]["original_name"] == "img2.png"
    assert rows[1]["new_name"] == "Anon_0002.png"
    assert rows[1]["status"] == "success"
    assert rows[1]["error"] == ""


def test_export_does_not_overwrite(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    create_test_image(input_dir / "img1.png")
    (output_dir / "0001.png").touch()
    with pytest.raises(FileExistsError):
        export_anonymized_images(
            image_paths=[input_dir / "img1.png"],
            output_dir=output_dir,
            rectangles=[],
            prefix="",
            randomize=False,
        )


def test_exported_png_has_no_private_metadata(tmp_path: Path) -> None:
    input_path = tmp_path / "source.png"
    output_dir = tmp_path / "output"
    Image.new("RGB", (40, 40), (255, 255, 255)).save(input_path, format="PNG")
    export_anonymized_images([input_path], output_dir, [], prefix="Anon_", randomize=False)
    metadata = inspect_image_metadata(output_dir / "Anon_0001.png")
    assert_no_private_metadata(metadata)


def test_exported_jpeg_has_no_private_metadata(tmp_path: Path) -> None:
    input_path = tmp_path / "source.jpg"
    output_dir = tmp_path / "output"
    Image.new("RGB", (40, 40), (255, 255, 255)).save(input_path, format="JPEG", dpi=(300, 300))
    export_anonymized_images([input_path], output_dir, [], prefix="Anon_", randomize=False)
    metadata = inspect_image_metadata(output_dir / "Anon_0001.jpg")
    assert_no_private_metadata(metadata)


def test_exported_tiff_has_no_private_metadata(tmp_path: Path) -> None:
    input_path = tmp_path / "source.tif"
    output_dir = tmp_path / "output"
    Image.new("RGB", (40, 40), (255, 255, 255)).save(input_path, format="TIFF", dpi=(300, 300))
    export_anonymized_images([input_path], output_dir, [], prefix="Anon_", randomize=False)
    metadata = inspect_image_metadata(output_dir / "Anon_0001.tif")
    assert_no_private_metadata(metadata)


def test_export_applies_rectangles_by_filename_and_all_images(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    create_test_image(input_dir / "img1.png")
    create_test_image(input_dir / "img2.png")

    export_anonymized_images(
        image_paths=[input_dir / "img1.png", input_dir / "img2.png"],
        output_dir=output_dir,
        rectangles=[
            {"filename": "img1.png", "x": 10, "y": 10, "width": 5, "height": 5},
            {"filename": "All_images", "x": 20, "y": 20, "width": 5, "height": 5},
        ],
        prefix="Anon_",
        randomize=False,
    )

    with Image.open(output_dir / "Anon_0001.png") as img1:
        assert img1.convert("RGB").getpixel((12, 12)) == (0, 0, 0)
        assert img1.convert("RGB").getpixel((22, 22)) == (0, 0, 0)

    with Image.open(output_dir / "Anon_0002.png") as img2:
        assert img2.convert("RGB").getpixel((12, 12)) == (255, 255, 255)
        assert img2.convert("RGB").getpixel((22, 22)) == (0, 0, 0)
