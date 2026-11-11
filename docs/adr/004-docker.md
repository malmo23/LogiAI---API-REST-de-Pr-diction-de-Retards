# ADR 004 : Conteneurisation et Déploiement de LogiAI avec Docker, Nginx et Compose

## Date
2026-11-11

## Statut
Accepté

## Contexte
LogiAI doit devenir une application autonome, transportable et facilement déployable en une seule commande, sans dépendre de l'environnement Python de la machine hôte. L'architecture sépare l'API de calcul (FastAPI) et l'interface utilisateur (page HTML/JS servie par Nginx faisant office de reverse proxy). Deux décisions d'architecture majeures doivent être tranchées : la gestion du modèle de machine learning et la politique d'exposition des ports réseau.

---

## Décision 1 : Gestion du modèle (COPY dans l'image vs Montage en volume)

### Décision retenue
Nous combinons les deux approches :
1. **Dans le `Dockerfile`** : nous copions le modèle (`COPY models/ ./models/`) pour rendre l'image autonome et prête pour la production.
2. **Dans le `docker-compose.yml` (environnement local de développement)** : nous montons le dossier hôte en volume bind mount (`./models:/app/models`).

### Justification et comparaison des alternatives
- **Ce que l'on perdrait avec `COPY` seul (sans volume en dev) :**  
  À chaque ré-entraînement du modèle (`python -m logiai.train`), le fichier `model.joblib` est mis à jour sur la machine hôte. Sans volume, le conteneur en cours d'exécution continuerait d'utiliser l'ancienne version figée dans l'image. Il faudrait systématiquement reconstruire l'image (`docker compose up -d --build`), ce qui ralentit considérablement la boucle d'itération en développement.
- **Ce que l'on perdrait avec le volume seul (sans `COPY` au build) :**  
  L'image Docker ne serait pas auto-suffisante. Si l'image était déployée sur un serveur distant, un environnement cloud ou un orchestrateur sans partage de fichiers local, le conteneur planterait au démarrage faute de trouver le fichier `model.joblib` (erreur 503).
- **Conséquence :** L'approche retenue garantit à la fois la **portabilité totale en production** et la **flexibilité immédiate en développement local**.

---

## Décision 2 : Exposition des ports réseau (8080 seul vs 8080 et 8001)

### Décision retenue
En développement, nous publions :
- Le port **8080** pour le reverse proxy Nginx (`8080:80`).
- Le port **8001** pour l'API FastAPI (`8001:8000`).

En production, seul le port **8080** (ou 80/443) sera publié vers l'extérieur.

### Justification et comparaison des alternatives
- **Ce que l'on perdrait si l'on ne publiait QUE le port 8080 en dev :**  
  Un développeur perdrait l'accès direct aux outils de documentation interactive OpenAPI / Swagger (`http://localhost:8001/docs`) et aux sondes de surveillance individuelles de l'API (`http://localhost:8001/health`). Cela compliquerait le débogage unitaire de l'API sans passer par le proxy Nginx.
- **Ce que l'on perdrait si l'on publiait le port 8001 en production :**  
  Un visiteur extérieur pourrait contourner Nginx et attaquer directement le serveur Uvicorn / FastAPI. On perdrait tous les bénéfices du reverse proxy : point d'entrée unique, masquage de la topologie interne, élimination des failles CORS, protection contre les attaques de déni de service (DDoS) et centralisation des terminaisons TLS / SSL.
- **Conséquence :** Le port 8001 est conservé pour le confort d'inspection et de test en développement local, mais sera retiré de la publication publique en environnement de production.
