import pytest

from demo_app.app import app
from demo_app.importer import parse_import_payload
from demo_app.jobs import fetch_status


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_greet(client):
    response = client.get("/greet/Ada")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Hello Ada!"


def test_import_counts_mapping_keys(client):
    response = client.post("/import", data="name: demo\ncount: 2\n")
    assert response.status_code == 200
    assert response.get_json() == {"imported": 2}


def test_parse_import_payload_rejects_list():
    with pytest.raises(ValueError):
        parse_import_payload("- a\n- b\n")


def test_parse_import_payload_without_loader_breaks_after_pyyaml_6():
    # Passes on PyYAML 5.3.1. Breaks after upgrading to PyYAML 6, which requires a Loader argument.
    assert parse_import_payload("name: demo") == {"name": "demo"}


def test_fetch_status_returns_code(monkeypatch):
    class FakeResponse:
        status_code = 204

    monkeypatch.setattr("demo_app.jobs.requests.get", lambda url, timeout: FakeResponse())
    assert fetch_status("https://example.com/status") == 204
