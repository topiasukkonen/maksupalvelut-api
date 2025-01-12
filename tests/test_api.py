import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_licenses_success(client):
    response = client.get("/licenses/2382421-3")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

    if data:
        assert "law_section" in data[0]
        assert "country" in data[0]


def test_get_licenses_not_found(client):
    response = client.get("/licenses/nonexistent-id")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_get_contacts_success(client):
    response = client.get("/contacts/AS SEB Pank")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "postal_address" in data
    assert "postal_code" in data


def test_get_contacts_not_found(client):
    response = client.get("/contacts/nonexistent-company")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
