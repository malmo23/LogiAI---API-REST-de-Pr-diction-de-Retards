# Compte rendu : TP API LogiAI

**Noms :** ............................  **Groupe :** ........

## 1. Environnement et premiers tests
- Sortie de `python -m pytest` au départ (collez-la) :
```
collected 13 items

tests\test_api.py ..FFFF......F                                                            [100%]
================================== 5 failed, 8 passed in 4.07s ==================================
```

- Pourquoi certains tests qui attendent un 422 passent-ils déjà, alors que rien n'est écrit ?
  Dans le starter, la classe `Livraison` contenait `model_config = ConfigDict(extra="forbid")` et un seul champ (`distance_km`). Dès qu'une requête envoyait des champs supplémentaires (`poids_kg`, `heure_depart`, etc.), Pydantic la rejetait immédiatement avec une erreur `422 Unprocessable Entity` (champs inconnus interdits). Les tests attendant un code 422 passaient donc "par accident" (faux vert), car la requête était refusée avant même d'arriver à la validation métier de ces variables.

## 2. Mon schéma
- Mes bornes et leur justification physique (une ligne par variable) :

| Variable | Min | Max | Pourquoi |
|---|---|---|---|
| distance_km | 1 | 1000 | Trajet physique de livraison routière (min 1 km, max environ 1000 km). |
| poids_kg | 0.1 | 5000 | Du petit colis (100 g) à la charge utile maximale d'un véhicule utilitaire/camion léger (5 t). |
| heure_depart | 0 | 23 | Heure valide sur une journée de 24 heures (de 0h à 23h). |
| pluie_mm | 0 | 100 | Précipitations physiques positives, 100 mm représentant une pluie torrentielle extrême. |
| trafic_index | 0 | 10 | Échelle d'indice de trafic définie entre 0 (fluide) et 10 (embouteillage saturé). |
| nb_arrets | 0 | 30 | Une tournée comprend au minimum 0 arrêt intermédiaire et rarement plus de 30 arrêts par jour. |
| type_vehicule | - | - | Restreint par `Literal["moto", "fourgon", "camion"]` correspondant à la flotte existante. |

## 3. Ma fonction predict()
```python
@app.post("/v1/predict", response_model=PredictionOut)
def predict(livraison: Livraison):
    predictor = state.get("predictor")
    if predictor is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible / non chargé")
    return PredictionOut(**predictor.predict(livraison.model_dump()))
```

## 4. Quatre requêtes
| Requête | Code obtenu | Pourquoi |
|---|---|---|
| livraison normale | 200 | Requête valide conforme au schéma Pydantic, le modèle calcule et renvoie la prédiction. |
| distance_km = -5 | 422 | Violation de la contrainte `ge=1` définie dans le schéma Pydantic. |
| type_vehicule = "avion" | 422 | Violation du type `Literal["moto", "fourgon", "camion"]` (valeur non autorisée). |
| modèle absent (supprimez models/ et relancez) | 503 | `state.get("predictor")` renvoie `None`, déclenchant l'exception HTTP 503 (Service Unavailable). |

## 5. Questions de compréhension
1. **Pourquoi charge-t-on le modèle au démarrage et pas à chaque requête ?**
   Le chargement d'un modèle depuis le disque (`joblib.load`) implique des opérations d'I/O disque et de désérialisation lentes (plusieurs centaines de millisecondes). En le chargeant une seule fois dans la fonction `lifespan` au démarrage, il reste en mémoire vive (RAM) et chaque inférence s'exécute en quelques millisecondes sans surcharger le processeur.

2. **Qui écrit le contrôle « pluie <= 100 », et où est-il écrit ?**
   C'est le développeur qui l'écrit dans la classe Pydantic `Livraison` dans le fichier `logiai/api/schemas.py`, via le paramètre `le=100` de `Field()`.

3. **Différence entre 422 et 503 ?**
   - **422 (Unprocessable Entity)** : Erreur côté **client**. La requête est un JSON valide mais les données ne respectent pas le contrat de l'API (ex: valeur négative ou hors bornes).
   - **503 (Service Unavailable)** : Erreur côté **serveur**. Le serveur est en ligne mais le service demandé (ici le modèle de prédiction) n'est temporairement pas prêt ou non chargé.

4. **Pourquoi une route `/v1/predict` plutôt que `/predict` ?**
   Pour gérer le **versionnement** de l'API. Cela permet de déployer une future version `/v2/predict` (avec un nouveau contrat ou modèle) sans casser le fonctionnement des clients existants (applications mobiles, web) qui utilisent encore `/v1`.

5. **Que se passerait-il si la distance était déclarée `int` ?**
   Pydantic forcerait la conversion en entier ou rejetterait les valeurs décimales. Une distance comme `12.5 km` serait soit tronquée à `12 km` (perte de précision pour le modèle ML), soit refusée avec une erreur 422 selon le mode de validation stricte.

## 6. Décision : modèle absent
**Répondre 503 ou refuser de démarrer ? Qu'est-ce que chaque option fait perdre ?**
- **Option A (Démarrer quand même et répondre 503)** :
  - *Ce qu'on gagne* : L'API reste joignable, les sondes de supervision peuvent interroger `/health` et savoir précisément que l'API tourne mais que `model_loaded: false`.
  - *Ce qu'on perd* : L'API reçoit inutilement du trafic client qu'elle ne peut pas honorer au lieu de laisser un répartiteur de charge (load balancer) rediriger vers une instance saine.
- **Option B (Refuser de démarrer - Fail Fast)** :
  - *Ce qu'on gagne* : Le gestionnaire de conteneurs (Docker/Kubernetes) détecte immédiatement l'échec au démarrage et évite de diriger des utilisateurs vers une instance invalide.
  - *Ce qu'on perd* : L'accès aux routes de diagnostic comme `/health` ou `/docs` pour inspecter l'instance.

## 7. Lien de la pull request
(À insérer après l'ouverture de la pull request sur GitHub depuis la branche `tp-api` vers `main`)
