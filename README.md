# LogiAI · API REST de Prédiction de Retard de Livraison

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063?logo=pydantic)](https://docs.pydantic.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/pytest-15%2F15%20passed-brightgreen?logo=pytest)](https://docs.pytest.org/)

**LogiAI** est un service intelligent conçu pour une société de transport logistique. Il transforme un modèle de Machine Learning entraîné sur des données de tournées en un service web accessible via une **API REST (FastAPI)**, consommable par un tableau de bord, une application mobile ou une interface interactive (**Streamlit**).

---

## 🚀 Fonctionnalités

- **API REST robuste & typée (FastAPI + Pydantic v2) :**
  - Validation stricte des données d'entrée (`distance_km`, `poids_kg`, `heure_depart`, `pluie_mm`, `trafic_index`, `nb_arrets`, `type_vehicule`).
  - Rejet automatique des valeurs aberrantes (`422 Unprocessable Entity`).
  - Gestion de l'état du service et résilience si le modèle est indisponible (`503 Service Unavailable`).
- **Performance & Inférence ultra-rapide :**
  - Chargement du modèle en mémoire une seule fois au démarrage via le cycle de vie `lifespan`.
  - Inférence ML exécutée en moins de 5 ms par requête.
- **Client Web Interactif (Streamlit) :**
  - Tableau de bord pour les dispatchers avec réglages dynamiques (sliders, sélecteurs) et alerte visuelle de retard.
- **Tests unitaires et d'intégration :**
  - Suite de 15 tests automatisés avec `pytest` (`TestClient`).

---

## 🛠️ Architecture du Projet

```text
logiai/
├── logiai/
│   ├── api/
│   │   ├── main.py          # Routes FastAPI (/health, /v1/predict, /docs)
│   │   └── schemas.py       # Schémas de validation Pydantic (Livraison, PredictionOut)
│   ├── config.py            # Paramètres du projet et chemins
│   ├── dataset.py           # Génération du jeu de données synthétique
│   ├── predict.py           # Classe Predictor pour charger et inférer
│   └── train.py             # Pipeline scikit-learn & entraînement
├── tests/
│   └── test_api.py          # Suite complète des 15 tests automatisés
├── streamlit_app.py         # Application frontend Streamlit pour les dispatchers
├── demo_api.py              # Exemple minimal FastAPI autonome (Bloc 4)
├── COMPTE_RENDU.md          # Compte rendu textuel complet du TP
├── COMPTE_RENDU.pdf         # Rapport PDF avec captures d'écran
├── requirements.txt         # Dépendances Python
└── README.md
```

---

## ⚙️ Installation & Prérequis

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/malmo23/logiai.git
   cd logiai
   ```

2. **Créer et activer l'environnement virtuel :**
   - **Windows (PowerShell) :**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux :**
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📊 Données et Entraînement du Modèle

1. **Générer les données synthétiques (5 000 trajets) :**
   ```bash
   python -m logiai.dataset
   ```
   *Génère le fichier `data/livraisons.csv`.*

2. **Entraîner le modèle de Machine Learning :**
   ```bash
   python -m logiai.train
   ```
   *Sauvegarde le pipeline scikit-learn dans `models/model.joblib` et ses métriques dans `models/model_info.json`.*

---

## 🖥️ Démarrage des Services

### 1. Lancer l'API FastAPI
```powershell
python -m uvicorn logiai.api.main:app --reload --port 8001
```
* **Documentation Swagger interactive :** [http://localhost:8001/docs](http://localhost:8001/docs)
* **Documentation ReDoc :** [http://localhost:8001/redoc](http://localhost:8001/redoc)
* **Health Check :** [http://localhost:8001/health](http://localhost:8001/health)

*(Note : le port `8001` est recommandé sur Windows pour éviter les conflits de ports réservés).*

### 2. Lancer l'interface Web Streamlit (dans un 2e terminal)
```powershell
python -m streamlit run streamlit_app.py
```
* **Accès à l'application :** [http://localhost:8501](http://localhost:8501)

---

## 🧪 Tests de Robustesse

Pour exécuter la suite de tests unitaires et d'intégration :

```bash
python -m pytest
```

**Résultat attendu :**
```text
collected 15 items
tests\test_api.py ...............                                        [100%]
============================= 15 passed in 3.62s ==============================
```

---

## 📑 Spécifications de l'API

### `POST /v1/predict`
Prédit le risque de retard pour une livraison donnée.

**Exemple de requête :**
```json
{
  "distance_km": 120.0,
  "poids_kg": 450.0,
  "heure_depart": 17,
  "pluie_mm": 8.0,
  "trafic_index": 7.5,
  "nb_arrets": 4,
  "type_vehicule": "camion"
}
```

**Exemple de réponse (`200 OK`) :**
```json
{
  "probabilite_retard": 0.8142,
  "alerte": true,
  "seuil": 0.4,
  "model_version": "1.0"
}
```

---

## 👤 Auteur

* **Maldani Mostafa**  
  *Module : Développement et déploiement d’applications intelligentes*  
  *Année universitaire : 2026 - 2027*  
  *Compte rendu complet disponible dans [`COMPTE_RENDU.pdf`](COMPTE_RENDU.pdf) et [`COMPTE_RENDU.md`](COMPTE_RENDU.md).*
