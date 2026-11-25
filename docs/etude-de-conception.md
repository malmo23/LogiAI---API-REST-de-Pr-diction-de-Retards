# Étude de conception — LogiAI

## 1. Besoin
*À compléter.*

## 2. Données
*À compléter.*

## 3. Modèle et métriques
*À compléter.*

## 4. Critères d'acceptation
*À compléter.*

## 5. Cycle de vie
*À compléter.*

## 6. Architecture

```text
[Navigateur :8080] ──► [Conteneur web : Nginx (port 80)]
                              │
                              ├── /       ──► page statique (web/index.html)
                              └── /api/*  ──► [Conteneur api : FastAPI + Uvicorn (port 8000)]
                                                    │
[Terminal CLI] ──► logiai-predict ─────────────────┼──► [Package logiai (site-packages)]
                                                    │          │
                                                    │          ▼
                                                    └──► [Volumes / Disque (LOGIAI_HOME)]
                                                           ├── data/livraisons.csv
                                                           └── models/model.joblib
```

- **Package `logiai`** : code métier (`train`, `predict`, `cli`, `api`) installé dans `site-packages`.
- **Données & Modèle (`data/`, `models/`)** : externes au package, résolus via `LOGIAI_HOME` (`/app` dans Docker).
- **CLI (`logiai-predict`)** : prédiction locale sans API depuis un fichier JSON.
- **Conteneur `api`** : FastAPI exposant `/health` et `/v1/predict` (protégé par `X-API-Key`).
- **Conteneur `web`** : Nginx servant `index.html` et relayant `/api/` vers `http://api:8000/` (origine unique).

## 7. Choix technologiques
*À compléter.*

## 8. Risques et éthique
*À compléter.*

## 9. Limites
*À compléter.*
