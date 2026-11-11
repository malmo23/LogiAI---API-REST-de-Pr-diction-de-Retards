import pytest
from fastapi.testclient import TestClient
from logiai.api.main import app
from logiai import config

CLE_USER = "test-user-key"
CLE_ADMIN = "test-admin-key"

@pytest.fixture(autouse=True)
def cles_de_test(monkeypatch):
    """Les tests utilisent des clés configurées."""
    monkeypatch.setattr(config, "API_KEY", CLE_USER)
    monkeypatch.setattr(config, "ADMIN_KEY", CLE_ADMIN)

@pytest.fixture
def client():
    """Client de test qui inclut par défaut la clé utilisateur valide."""
    with TestClient(app, headers={"X-API-Key": CLE_USER}) as c:
        yield c

@pytest.fixture
def headers_user():
    return {"X-API-Key": CLE_USER}

@pytest.fixture
def headers_admin():
    return {"X-API-Key": CLE_ADMIN}
