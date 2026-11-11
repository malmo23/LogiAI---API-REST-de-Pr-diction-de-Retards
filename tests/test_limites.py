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

CAS_LIMITES = [
    # distance_km (bornes : 1.0 à 1000.0)
    ("distance limite basse", "distance_km", 1.0, 200),
    ("distance trop basse", "distance_km", 0.0, 422),
    ("distance limite haute", "distance_km", 1000.0, 200),
    ("distance trop haute", "distance_km", 1001.0, 422),

    # poids_kg (bornes : 1.0 à 5000.0)
    ("poids limite bas", "poids_kg", 1.0, 200),
    ("poids trop bas", "poids_kg", 0.0, 422),
    ("poids limite haut", "poids_kg", 5000.0, 200),
    ("poids trop haut", "poids_kg", 5001.0, 422),

    # heure_depart (bornes : 0 à 23, supporte les décimales)
    ("heure limite basse", "heure_depart", 0, 200),
    ("heure trop basse", "heure_depart", -1, 422),
    ("heure limite haute", "heure_depart", 23, 200),
    ("heure trop haute", "heure_depart", 24, 422),
    ("heure décimale", "heure_depart", 11.5, 200),

    # pluie_mm (bornes : 0.0 à 100.0)
    ("pluie limite basse", "pluie_mm", 0.0, 200),
    ("pluie trop basse", "pluie_mm", -0.1, 422),
    ("pluie limite haute", "pluie_mm", 100.0, 200),
    ("pluie trop haute", "pluie_mm", 100.1, 422),

    # trafic_index (bornes : 0.0 à 10.0)
    ("trafic limite bas", "trafic_index", 0.0, 200),
    ("trafic trop bas", "trafic_index", -0.1, 422),
    ("trafic limite haut", "trafic_index", 10.0, 200),
    ("trafic trop haut", "trafic_index", 10.1, 422),

    # nb_arrets (bornes : 0 à 20)
    ("arrêts limite bas", "nb_arrets", 0, 200),
    ("arrêts trop bas", "nb_arrets", -1, 422),
    ("arrêts limite haute", "nb_arrets", 20, 200),
    ("arrêts trop haut", "nb_arrets", 21, 422),
]

@pytest.mark.parametrize("description, champ, valeur, attendu", CAS_LIMITES)
def test_limites(client, description, champ, valeur, attendu):
    """Vérifie le comportement de l'API aux frontières des plages de valeurs."""
    corps = {**VALID, champ: valeur}
    response = client.post("/v1/predict", json=corps)
    assert response.status_code == attendu