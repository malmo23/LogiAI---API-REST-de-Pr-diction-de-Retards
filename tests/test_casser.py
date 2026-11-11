import pytest

VALID = {
    "distance_km": 120.0,
    "poids_kg": 450.0,
    "heure_depart": 17,
    "pluie_mm": 8.0,
    "trafic_index": 7.5,
    "nb_arrets": 4,
    "type_vehicule": "camion"
}

CAS_REFUSES = [
    ("champ manquant", "/v1/predict", {k: v for k, v in VALID.items() if k != "poids_kg"}, 422),
    ("valeur absurde", "/v1/predict", {**VALID, "poids_kg": 99999}, 422),
    ("texte au lieu d'un nombre", "/v1/predict", {**VALID, "poids_kg": "trop_lourd"}, 422),
    ("champ en trop", "/v1/predict", {**VALID, "champ_inconnu": 123}, 422),
    ("mauvaise route", "/v1/route-inexistante", VALID, 404),
]

@pytest.mark.parametrize("description, url, corps, attendu", CAS_REFUSES)
def test_request_refuse(client, description, url, corps, attendu):
    """Vérifie que les requêtes incorrectes sont rejetées avec le bon code HTTP."""
    response = client.post(url, json=corps)
    assert response.status_code == attendu