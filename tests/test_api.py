from fastapi.testclient import TestClient

from api.auth import API_KEY_ENV_NAME
from api.data import SNEAKER_CATALOG
from api.index import app


client = TestClient(app)
TEST_API_KEY = "test-only-api-key"


def test_all_twenty_sneakers_are_validated_at_startup() -> None:
    assert len(SNEAKER_CATALOG) == 20
    assert all(sneaker.id > 0 for sneaker in SNEAKER_CATALOG)


def test_health_endpoint_returns_utc_timestamp() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "SOLE Sneaker API"
    assert payload["timestamp"].endswith("+00:00")


def test_public_catalog_remains_available_to_the_website() -> None:
    response = client.get("/sneakers")

    assert response.status_code == 200
    assert response.json()["count"] == 20


def test_protected_catalog_rejects_a_missing_key() -> None:
    response = client.get("/api/v1/sneakers")

    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required."}


def test_protected_catalog_rejects_an_invalid_key(monkeypatch) -> None:
    monkeypatch.setenv(API_KEY_ENV_NAME, TEST_API_KEY)

    response = client.get(
        "/api/v1/sneakers",
        headers={"x-api-key": "wrong-key"},
    )

    assert response.status_code == 401


def test_protected_search_uses_new_metadata(monkeypatch) -> None:
    monkeypatch.setenv(API_KEY_ENV_NAME, TEST_API_KEY)

    response = client.get(
        "/api/v1/sneakers/search",
        params={"q": "China"},
        headers={"x-api-key": TEST_API_KEY},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert {item["brand"] for item in payload["results"]} == {"Anta"}
