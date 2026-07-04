from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from src.api.app import create_app


def _create_test_image(path: Path) -> None:
    image = Image.new("RGB", (32, 32), color="white")
    image.save(path)


def test_api_health() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "clinical-image-anonymizer-api",
    }


def test_api_version() -> None:
    client = TestClient(create_app())

    response = client.get("/version")

    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "Clinical Image Anonymizer"
    assert payload["version"] == "1.0.0"
    assert payload["author"] == "Ricardo Eugenio Gonzalez Valenzuela"
    assert payload["organization"] == "ACTA AI Lab"
    assert payload["repository"] == "https://github.com/RKronoXR/clinical-image-anonymizer"


def test_api_anonymize_batch_exports_images_and_mapping(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    _create_test_image(input_dir / "image_1.png")
    _create_test_image(input_dir / "image_2.png")

    client = TestClient(create_app())

    response = client.post(
        "/anonymize-batch",
        json={
            "input_dir": str(input_dir),
            "output_dir": str(output_dir),
            "rectangles": [[1, 1, 10, 10], [12, 12, 8, 8]],
            "prefix": "Api_",
            "randomize": True,
            "recursive": False,
            "workers": 9999,
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "success"
    assert payload["processed"] == 2
    assert Path(payload["mapping_csv"]).exists()
    assert len(payload["exported_files"]) == 2
    assert (output_dir / "mapping.csv").exists()
    assert len(list(output_dir.glob("Api_*.png"))) == 2


def test_api_anonymize_batch_rejects_missing_input(tmp_path: Path) -> None:
    client = TestClient(create_app())

    response = client.post(
        "/anonymize-batch",
        json={
            "input_dir": str(tmp_path / "missing"),
            "output_dir": str(tmp_path / "output"),
        },
    )

    assert response.status_code == 404
