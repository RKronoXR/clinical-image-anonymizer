from fastapi.testclient import TestClient

from src.api.app import create_app


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
