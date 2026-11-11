import pytest
from fastapi.testclient import TestClient
from logiai.api.main import app
from logiai import config

@pytest.fixture
def client():
    """Fournit un TestClient FastAPI pour tester l'application sans lancer uvicorn."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def headers_user():
    """Fournit des en-têtes valides avec la clé utilisateur pour les tests."""
    api_key = config.API_KEY if hasattr(config, "API_KEY") and config.API_KEY else "test-user-key"
    return {"X-API-Key": api_key}

@pytest.fixture
def headers_admin():
    """Fournit des en-têtes valides avec la clé administrateur pour les tests."""
    admin_key = config.ADMIN_KEY if hasattr(config, "ADMIN_KEY") and config.ADMIN_KEY else "test-admin-key"
    return {"X-API-Key": admin_key}
