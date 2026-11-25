# ADR 005 — Packaging de LogiAI

1. **`>=` dans `pyproject.toml` et `==` dans `requirements.txt` :**
   `pyproject.toml` déclare des bornes minimales (`>=`) pour rester compatible avec l'environnement de l'utilisateur qui installe le package. `requirements.txt` fige les versions exactes (`==`) pour garantir la reproductibilité stricte de l'image Docker. Faire l'inverse bloquerait l'installation chez les collègues (`==` partout) ou casserait la reproductibilité en production (`>=` partout).

2. **Le modèle (`models/`) reste hors du package :**
   Le wheel contient uniquement le code (`logiai/`), tandis que `models/` reste à côté (localisé via `LOGIAI_HOME`). Inclure le modèle dans le wheel imposerait de reconstruire et redistribuer tout le package à chaque ré-entraînement et alourdirait l'archive.
