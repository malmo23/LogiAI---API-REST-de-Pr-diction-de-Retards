# Compte rendu : TP API LogiAI

**Nom :** Maldani Mostafa  
**Module :** Développement et déploiement d’applications intelligentes  
**Année :** 2026 - 2027  

---

## 1. Environnement et premiers tests

- **Sortie de `python -m pytest` au départ :**
```text
collected 13 items

tests\test_api.py ..FFFF......F                                                            [100%]
================================== 5 failed, 8 passed in 4.07s ==================================
```

- **Résultats de l'entraînement (`python -m logiai.train`) :**
  - **Baseline accuracy :** `0.726` (72.6% si on prédisait toujours « à l'heure »)
  - **Accuracy du modèle :** `0.774` (77.4%)
  - **Rappel du modèle :** `0.464` (sur 100 livraisons réellement en retard, environ 46 sont détectées)
  - **Précision :** `0.617` (61.7%)
  - **AUC :** `0.769`

- **À quoi sert l'API si le rappel est limité ?**  
  Même avec un rappel de 46%, l'API permet au dispatcher de prioriser proactivement près de la moitié des retards critiques avant qu'ils n'arrivent (en réaffectant un livreur ou en prévenant le client), ce qui apporte un gain opérationnel immédiat par rapport à une gestion aveugle sans modèle.

- **Pourquoi certains tests qui attendent un 422 passent-ils déjà, alors que rien n'est écrit ?**  
  Dans le starter, la classe `Livraison` contenait `model_config = ConfigDict(extra="forbid")` et ne déclarait que le champ `distance_km`. Dès qu'une requête de test envoyait des champs supplémentaires (`poids_kg`, `heure_depart`, etc.), Pydantic la rejetait immédiatement avec une erreur `422 Unprocessable Entity` pour champ inconnu. Les tests attendant un 422 passaient donc « par accident » (faux vert), car la requête était refusée avant même d'arriver à la validation métier.

- **Quel test de succès (code 200) les démasque ?**  
  Le test `test_predict_valide_renvoie_200`. Il envoie une livraison valide complète et attend un code 200, mais reçoit un 422 à cause du schéma incomplet.

- **Que révèle cet exemple sur la lecture d'un résultat de test ?**  
  Un test « vert » ne prouve pas à lui seul que la logique métier fonctionne. Il faut toujours vérifier qu'un test réussit pour la bonne raison et non à cause d'une erreur fortuite en amont.

---

## 2. Mon schéma

- **Mes bornes et leur justification physique :**

| Variable | Min | Max | Pourquoi |
|---|---|---|---|
| `distance_km` | 1 | 1000 | Trajet physique de livraison routière (min 1 km, max environ 1000 km). |
| `poids_kg` | 0.1 | 5000 | Du petit paquet léger (100 g) à la charge utile maximale d'un utilitaire / fourgon. |
| `heure_depart` | 0 | 23 | Heures valides d'une journée de 24h (horloge de 0h à 23h). |
| `pluie_mm` | 0 | 100 | Précipitations physiques positives ; 100 mm représente déjà un épisode orageux extrême. |
| `trafic_index` | 0 | 10 | Indice conventionnel d'encombrement routier : 0 = fluide, 10 = saturé. |
| `nb_arrets` | 0 | 30 | Nombre d'arrêts de tournée (minimum 0, max réaliste 30 arrêts par shift). |
| `type_vehicule` | - | - | Restreint à `Literal["moto", "fourgon", "camion"]` selon la flotte autorisée. |

---

## 3. Ma fonction predict()

```python
@app.post("/v1/predict", response_model=PredictionOut)
def predict(livraison: Livraison):
    predictor = state.get("predictor")
    if predictor is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible / non chargé")
    return PredictionOut(**predictor.predict(livraison.model_dump()))
```

- **Pourquoi serait-il catastrophique de charger le modèle à chaque requête ?**  
  Le chargement depuis le disque (`joblib.load`) prend plusieurs centaines de millisecondes et sollicite lourdement les I/O du disque et le CPU. En chargeant le modèle une seule fois au démarrage dans `lifespan`, il reste en mémoire vive (RAM) et chaque inférence ne prend que 2 à 5 ms sans saturer le serveur.

---

## 4. Quatre requêtes

| Requête | Code obtenu | Pourquoi |
|---|---|---|
| Livraison normale | **200** | Données conformes au schéma Pydantic, le modèle est présent en mémoire et renvoie la prédiction. |
| `distance_km = -5` | **422** | Rejeté par Pydantic : violation de la borne minimale `ge=1`. |
| `type_vehicule = "avion"` | **422** | Rejeté par Pydantic : la valeur ne fait pas partie du `Literal["moto", "fourgon", "camion"]`. |
| Modèle absent (sans `models/`) | **503** | `state.get("predictor")` renvoie `None`, l'endpoint lève une `HTTPException(503)`. |

---

## 5. Questions de compréhension

1. **Pourquoi charge-t-on le modèle au démarrage et pas à chaque requête ?**  
   Pour éviter les lectures disque lentes et répétitives. Le modèle reste en mémoire vive (RAM), ce qui permet des temps de réponse ultra-rapides (< 5 ms) et supporte un trafic élevé.

2. **Qui écrit le contrôle « pluie <= 100 », et où est-il écrit ?**  
   C'est le développeur qui l'écrit dans la classe Pydantic `Livraison` dans le fichier `logiai/api/schemas.py`, via le paramètre `le=100` de `Field()`.

3. **Différence entre 422 et 503 ?**  
   - **422 (Unprocessable Entity) :** Erreur côté **client**. La requête est en JSON valide mais contient des données impossibles ou hors bornes.  
   - **503 (Service Unavailable) :** Erreur côté **serveur**. Le serveur web fonctionne mais le service sous-jacent (le modèle ML) n'est temporairement pas disponible / non chargé.

4. **Pourquoi une route `/v1/predict` plutôt que `/predict` ?**  
   Pour le **versionnement** de l'API. Cela permet de déployer une future version `/v2/predict` sans casser les applications existantes (mobiles, Streamlit) qui continuent de tourner sur `/v1`.

5. **Que se passerait-il si la distance était déclarée `int` ?**  
   FastAPI forcerait la conversion en entier ou rejetterait les nombres décimaux. Une distance réelle comme `12.5 km` serait soit tronquée à `12 km` (perte de précision pour le modèle), soit refusée avec une erreur 422.

---

## 6. Décision : modèle absent

**Répondre 503 ou refuser de démarrer ? Qu'est-ce que chaque option fait perdre ?**

- **Option A (Démarrer quand même et répondre 503) :**
  - *Gain :* L'API reste joignable, les sondes de supervision peuvent interroger `/health` et savoir précisément que `model_loaded: false`.
  - *Perte :* L'API reçoit inutilement des requêtes de prédiction des clients pour leur renvoyer une erreur 503 au lieu de laisser un répartiteur de charge (load balancer) rediriger le trafic vers une autre instance saine.
- **Option B (Refuser de démarrer / Fail Fast) :**
  - *Gain :* Dans un environnement conteneurisé (Docker / Kubernetes), le conteneur crash immédiatement ; l'orchestrateur ne lui envoie aucun trafic client et alerte l'administrateur.
  - *Perte :* Impossible d'interroger `/health` ou `/docs` pour inspecter l'instance à distance.

---

## 7. Lien de la pull request & Tests

- **Dépôt GitHub :** https://github.com/malmo23/logiai  
- **Branche :** `tp-api` vers `main`  
- **Lien Pull Request :** https://github.com/malmo23/logiai/pull/1  
- **Résultat final des tests :** 15 tests sur 15 validés avec succès (`15 passed in 3.62s`)
