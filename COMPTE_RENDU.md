# Compte Rendu : Atelier 5 - Conteneuriser et déployer LogiAI avec Docker

**Nom :** Maldani Mostafa  
**Module :** Développement et déploiement d’applications intelligentes  
**Professeur :** Pr. Soukaina Gouraguine  
**Année Universitaire :** 2026 - 2027  

---

## 1. Premier constat : « Ça ne marche que chez vous »

### Tableau récapitulatif

| Ce que le projet suppose | Qui le garantit aujourd’hui |
| :--- | :--- |
| Une version de Python et des bibliothèques compatibles avec `model.joblib` | **Vous**, avec `.venv` et `requirements.txt` |
| Le fichier `.env` avec les deux clés secrètes | **Vous**, manuellement |
| Un modèle entraîné dans `models/` | **Vous**, avec `python -m logiai.train` |
| Deux terminaux : uvicorn (API), puis `python -m http.server 5500` (page web) | **Vous**, manuellement |

### Phrase explicative
> *« Si je donne mon dossier à un camarade, il doit installer la bonne version de Python, créer et activer un environnement virtuel, installer toutes les dépendances sans conflits de système d'exploitation, entraîner le modèle en local, créer manuellement son propre fichier `.env` et jongler avec deux terminaux ouverts en permanence (un pour l'API Uvicorn et un pour le serveur HTTP de la page). Cela entraîne des problèmes d'incompatibilité d'environnement, des conflits de ports, et aucune garantie de reproductibilité. Docker résout cela en figeant tout dans des conteneurs isolés et portables. »*

---

## 2. Activité 1 : L’API dans un conteneur

### Fichier `.dockerignore`
```dockerignore
.venv/
.venv_test/
venv/
.git/
.gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
build/
dist/
*.egg-info/
.env
.vscode/
.idea/
docs/
tests/
```
*Note : `data/` et `models/` ne sont pas exclus car l'image en a besoin au build. `.env` est impérativement exclu pour protéger les clés secrètes.*

### `Dockerfile` de l'API
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 1. Dépendances d'abord (mise en cache efficace)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Code, données et modèle
COPY logiai/ ./logiai/
COPY data/ ./data/
COPY models/ ./models/

ENV LOGIAI_HOME=/app
EXPOSE 8000

CMD ["uvicorn", "logiai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Commandes exécutées
```powershell
docker build -t logiai:1.0 .
docker run -d --name logiai-api-test -p 8001:8000 --env-file .env logiai:1.0
curl.exe http://localhost:8001/health
```

### Trois expériences pour casser le conteneur

| Expérience | Prévu | Obtenu | Explication en une phrase |
| :--- | :--- | :--- | :--- |
| **1. Sans `--env-file`** | Le conteneur démarre mais `/health` indique `auth_configured: false`, et `/v1/predict` refuse toute clé (401). | `/health` renvoie `auth_configured: false` et toute requête de prédiction donne 401. | Le conteneur est un environnement totalement isolé et `.dockerignore` exclut `.env` ; sans `--env-file`, aucune variable secrète n'est injectée dans le conteneur. |
| **2. Sans publier le port (`-p`)** | Le conteneur est `Up`, mais `curl` vers `localhost:8001` échoue immédiatement. | `curl: (7) Failed to connect to localhost port 8001: Connection refused`. | L'instruction `EXPOSE 8000` n'est qu'une documentation ; sans l'option `-p 8001:8000`, aucune redirection réseau n'est créée entre l'hôte Windows et le conteneur. |
| **3. Écoute sur `127.0.0.1`** | Le port est mappé mais la connexion est rejetée ou retourne une réponse vide. | `curl: (52) Empty reply from server` ou fermeture de connexion. | `127.0.0.1` restreint l'écoute à la seule interface loopback interne du conteneur, ignorant les requêtes arrivant sur l'interface virtuelle eth0 via le pont Docker. |

---

## 3. Sprint 1 : La page web dans un conteneur Nginx

### Modification dans `web/index.html`
```javascript
const API_URL = '/api/v1/predict';
```

### Fichier `nginx/default.conf`
```nginx
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        # TODO 1 : Le slash final retire le préfixe /api/ : /api/v1/predict -> /v1/predict
        proxy_pass http://api:8000/;

        # TODO 2 : En-têtes pour transmettre l'identité du client d'origine
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Fichier `web/Dockerfile`
```dockerfile
FROM nginx:alpine
COPY web/index.html /usr/share/nginx/html/index.html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### Cheminement d'une requête `/api/v1/predict`
1. Le navigateur charge la page depuis `http://localhost:8080/`.
2. Lors du clic sur « Évaluer », le script JavaScript appelle l'URL relative `/api/v1/predict`, qui cible donc `http://localhost:8080/api/v1/predict` (même origine, donc **aucun preflight CORS OPTIONS** requis).
3. Le conteneur `logiai-web` (Nginx) reçoit la requête sur le port 80.
4. La directive `location /api/` intercepte la requête et l'envoie à `http://api:8000/`. Grâce au slash final de `proxy_pass`, Nginx retire le préfixe `/api/` et transmet `/v1/predict`.
5. Le DNS interne de Docker résout le nom de service `api` vers l'IP interne du conteneur `logiai-api`.
6. Uvicorn/FastAPI reçoit la requête sur `/v1/predict`, valide la clé d'en-tête `X-API-Key`, calcule la prédiction avec le modèle en mémoire et renvoie la réponse JSON à Nginx, qui la retransmet au navigateur.

---

## 4. Sprint 2 : Docker Compose

### Fichier `docker-compose.yml`
```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: logiai-api
    ports:
      - '8001:8000'
    env_file:
      - .env
    environment:
      LOGIAI_HOME: /app
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  web:
    build:
      context: .
      dockerfile: web/Dockerfile
    container_name: logiai-web
    ports:
      - '8080:80'
    depends_on:
      api:
        condition: service_healthy
```

### État des services (`docker compose ps`)
```text
NAME         IMAGE          COMMAND                  SERVICE   CREATED         STATUS                    PORTS
logiai-api   atelier4-api   "uvicorn logiai.api.…"   api       1 minute ago    Up 1 minute (healthy)     0.0.0.0:8001->8000/tcp
logiai-web   atelier4-web   "/docker-entrypoint.…"   web       1 minute ago    Up 1 minute               0.0.0.0:8080->80/tcp
```

### Codes HTTP observés à l'étape 5 (via Nginx sur le port 8080)
1. `/api/health` : **`200 OK`** (`{"status":"ok","model_loaded":true,"auth_configured":true}`)
2. `/api/v1/predict` sans clé : **`401 Unauthorized`** (`{"detail":"Clé API manquante dans l'en-tête X-API-Key."}`)
3. `/api/v1/predict` avec une fausse clé : **`401 Unauthorized`** (`{"detail":"Clé API invalide."}`)
4. `/api/v1/predict` avec la bonne clé : **`200 OK`** (`{"probabilite_retard":0.732,"alerte":true,"seuil":0.4,"model_version":"1.0"}`)

### Inspection réseau F12 (Étape 6)
- **Adresse cible :** `http://localhost:8080/api/v1/predict`
- **Présence d'une requête préliminaire `OPTIONS` :** **Non**, aucune requête `OPTIONS` n'apparaît.
- **Pourquoi ?** Parce que la page web et l'API partagent désormais la même origine (`http://localhost:8080`). Les requêtes sont considérées comme *same-origin*, ce qui élimine totalement le mécanisme de preflight CORS.

### Relevé des ressources (`docker stats`)
```text
CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O     PIDS
270469cb8dcf   logiai-api   0.16%     138.2MiB / 7.049GiB   1.92%     4.11kB / 2.36kB   0B / 0B       13
22c9d9876630   logiai-web   0.00%     5.82MiB / 7.049GiB    0.08%     8.53kB / 8.01kB   0B / 8.19kB   5
```

### Test de panne et résilience (Étape 8)
- Commande exécutée : `docker compose stop api`
- Résultat sur la page web : La requête AJAX échoue car Nginx ne peut plus joindre le conteneur API. Nginx renvoie un code d'erreur **`504 Gateway Time-out`** (ou `502 Bad Gateway`).
- Affichage sur la page : Message d'erreur utilisateur indiquant que le serveur est indisponible.
- Relance : `docker compose start api` $\rightarrow$ Le service redevient opérationnel immédiatement.

### Observation des volumes (Étape 9)
- `docker compose exec api ls /app/models` liste `model.joblib` et `model_info.json`.
- **Pourquoi un nouveau modèle entraîné sur Windows est-il vu sans rebuild ?**  
  Parce que le bind mount `./models:/app/models` fait pointer le répertoire du conteneur directement vers le système de fichiers hôte de Windows en temps réel.
- **Et un changement dans `logiai/` ?**  
  Le code de `logiai/` n'étant pas monté en volume mais copié à la construction (`COPY`), il est figé dans l'image. Tout changement dans le code nécessite une reconstruction : `docker compose up -d --build`.

---

## 5. Questions de compréhension

1. **Pourquoi l'ordre des instructions dans le Dockerfile est-il capital pour le cache ?**  
   Docker met en cache chaque couche de construction. Lorsqu'une instruction change, toutes les suivantes doivent être réexécutées. En plaçant l'installation des dépendances (`requirements.txt` puis `pip install`) avant la copie du code source, Docker ne réinstalle pas les paquets tant que `requirements.txt` ne change pas, réduisant le temps de build de plusieurs minutes à quelques secondes.

2. **Quelle est la différence entre `EXPOSE 8000` et `-p 8001:8000` ?**  
   `EXPOSE 8000` est une instruction purement documentaire destinée aux administrateurs ; elle n'ouvre ni ne mappe aucun port sur la machine hôte. L'option `-p 8001:8000` (ou la directive `ports:` de Compose) configure la redirection réseau effective au niveau du noyau de l'hôte vers le conteneur.

3. **Pourquoi Uvicorn doit-il écouter sur `0.0.0.0` et non `127.0.0.1` dans un conteneur ?**  
   `127.0.0.1` correspond à la boucle locale interne du conteneur. Les requêtes réseau provenant de l'hôte ou d'autres conteneurs arrivent sur l'interface réseau virtuelle (`eth0`). Écouter sur `0.0.0.0` permet à Uvicorn d'accepter les connexions sur toutes les interfaces réseau du conteneur.

4. **Pourquoi le reverse proxy Nginx évite-t-il les problèmes de CORS ?**  
   Le CORS (*Cross-Origin Resource Sharing*) est une politique de sécurité imposée par les navigateurs lorsque deux serveurs ont des origines distinctes (différence de protocole, de domaine ou de port). Nginx servant à la fois la page web (`/`) et relayant l'API (`/api/`) sur le port unique 8080, le navigateur considère l'ensemble comme provenant de la même origine (*same-origin*).

5. **Pourquoi `depends_on` seul ne garantit-il pas que l'application fonctionne au démarrage ?**  
   `depends_on` sans condition s'assure uniquement que le conteneur cible est lancé (processus démarré), mais ignore si le service à l'intérieur est réellement prêt à recevoir du trafic (par exemple si Uvicorn charge encore un modèle ML volumineux). L'utilisation de `condition: service_healthy` couplée à un `healthcheck` garantit que l'API a répondu positivement avec un code 200 avant que les services dépendants ne démarrent.

---

## 6. Ticket de sortie (individuel)

1. **Quelle différence entre une image et un conteneur ?**  
   Une **image** est un plan statique, immuable et composé de couches en lecture seule. Un **conteneur** est une instance vivante et isolée de cette image en cours d'exécution, disposant de ses propres processus, de son espace mémoire et d'une fine couche inscriptible éphémère.

2. **Pourquoi le navigateur appelle-t-il `/api/v1/predict` et non `api:8000` ?**  
   Le navigateur s'exécute sur le système d'exploitation de la machine hôte (Windows). Le nom d'hôte `api` n'est résolu que par le serveur DNS interne de Docker pour les conteneurs connectés au même réseau bridge. L'hôte ne peut pas résoudre `http://api:8000`. De plus, l'URL relative permet de conserver une origine unique.

3. **Pourquoi `depends_on` seul ne suffit-il pas, et que change `service_healthy` ?**  
   `depends_on` seul vérifie seulement que le conteneur a démarré (`Up`). `service_healthy` force Docker Compose à interroger la route `/health` à intervalles réguliers et à attendre que le conteneur soit déclaré en état `healthy` avant de lancer le conteneur Nginx.

4. **Qu’est-ce qui reste flou pour vous ?**  
   La gestion des utilisateurs non-root (`USER appuser`) dans les images de production pour restreindre les privilèges de sécurité du conteneur, ainsi que la configuration fine du cache de build multi-étapes (*multi-stage build*).
