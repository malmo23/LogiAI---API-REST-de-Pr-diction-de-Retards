import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, HRFlowable, Image, PageBreak
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 30, 576, 30)
        self.drawString(36, 19, "Atelier 5 - Conteneuriser et déployer LogiAI avec Docker | Réalisé par : Maldani Mostafa")
        page_text = f"Page {self._pageNumber} / {page_count}"
        self.drawRightString(576, 19, page_text)
        self.restoreState()


def scaled_image(path, target_width=470):
    with PILImage.open(path) as im:
        w, h = im.size
    ratio = h / float(w)
    return Image(path, width=target_width, height=target_width * ratio)


def build_pdf(filename="COMPTE_RENDU.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=26,
        bottomMargin=38,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14.5,
        leading=18,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=2,
    )

    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=3,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=6,
        spaceAfter=3,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=3,
    )

    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=body_style,
        leftIndent=10,
        spaceAfter=2,
    )

    code_style = ParagraphStyle(
        "CodeText",
        fontName="Courier",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=4,
        spaceBefore=2,
        spaceAfter=3,
    )

    th_style = ParagraphStyle(
        "TH", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=colors.white
    )
    td_style = ParagraphStyle(
        "TD", fontName="Helvetica", fontSize=7.2, leading=9.2, textColor=colors.HexColor("#1e293b")
    )
    td_bold = ParagraphStyle(
        "TDBold", fontName="Helvetica-Bold", fontSize=7.2, leading=9.2, textColor=colors.HexColor("#0f172a")
    )

    story = []

    # --- EN-TÊTE ---
    story.append(Paragraph("Compte Rendu : Atelier 5 - Conteneuriser et déployer LogiAI avec Docker", title_style))
    story.append(Paragraph(
        "<b>Réalisé par :</b> Maldani Mostafa &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Professeur :</b> Pr. Soukaina Gouraguine &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Module :</b> Déploiement d'Applications Intelligentes (2026-2027)",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceBefore=2, spaceAfter=5))

    # --- SECTION 1 : PRÉPARATION & PREMIER CONSTAT ---
    story.append(Paragraph("1. Préparation & Premier constat : « Ça ne marche que chez vous »", h2_style))
    story.append(Paragraph(
        "Vérification de Docker Desktop (WSL2), présence du modèle <code>models/model.joblib</code> et validation de la suite de tests de l'Atelier 4 (<b>45/45 tests verts</b>) :",
        body_style
    ))

    if os.path.exists("screenshots/terminal_prep_pytest.png"):
        story.append(scaled_image("screenshots/terminal_prep_pytest.png", target_width=460))
        story.append(Spacer(1, 4))

    c_headers = [Paragraph("Ce que le projet suppose", th_style), Paragraph("Qui le garantit avant Docker", th_style)]
    c_rows = [
        [Paragraph("Une version de Python et des bibliothèques compatibles avec model.joblib", td_style),
         Paragraph("Vous, manuellement avec .venv et requirements.txt", td_style)],
        [Paragraph("Le fichier .env contenant les deux clés (LOGIAI_API_KEY, LOGIAI_ADMIN_KEY)", td_style),
         Paragraph("Vous, créé localement sur votre poste", td_style)],
        [Paragraph("Un modèle entraîné dans models/", td_style),
         Paragraph("Vous, après exécution de python -m logiai.train", td_style)],
        [Paragraph("Deux terminaux ouverts (uvicorn sur 8000/8001 + http.server sur 5500)", td_style),
         Paragraph("Vous, en lançant deux processus manuellement", td_style)],
    ]
    t1 = Table([c_headers] + c_rows, colWidths=[300, 240])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<i>« Si je donne mon dossier à un camarade, il doit installer Python, créer un venv, installer les dépendances, "
        "entraîner le modèle, créer son .env et lancer deux terminaux séparés. Docker élimine ces frictions en empaquetant "
        "chaque service dans un conteneur isolé démarrable en une seule commande. »</i>",
        body_style
    ))

    # --- SECTION 2 : ACTIVITÉ 1 - L'API DANS UN CONTENEUR ---
    story.append(Paragraph("2. Activité 1 : L'API seule dans un conteneur & Expériences", h2_style))
    story.append(Paragraph(
        "Le fichier <code>.dockerignore</code> exclut <code>.venv/</code>, <code>.git/</code>, <code>tests/</code> et surtout <code>.env</code> "
        "(pour qu'aucun secret n'entre dans l'image), tout en conservant <code>data/</code> et <code>models/</code>.",
        body_style
    ))

    dockerfile_api_code = (
        "FROM python:3.11-slim\n"
        "WORKDIR /app\n"
        "COPY requirements.txt ./\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY logiai/ ./logiai/\n"
        "COPY data/ ./data/\n"
        "COPY models/ ./models/\n"
        "ENV LOGIAI_HOME=/app\n"
        "EXPOSE 8000\n"
        "CMD [\"uvicorn\", \"logiai.api.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
    )
    story.append(Preformatted(dockerfile_api_code, code_style))

    if os.path.exists("screenshots/terminal_activite1_docker.png"):
        story.append(scaled_image("screenshots/terminal_activite1_docker.png", target_width=460))
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Trois expériences pour casser le conteneur :</b>", body_style))
    exp_headers = [
        Paragraph("Expérience", th_style),
        Paragraph("Prévu", th_style),
        Paragraph("Obtenu", th_style),
        Paragraph("Explication", th_style),
    ]
    exp_rows = [
        [Paragraph("1. Sans --env-file", td_bold),
         Paragraph("Clés absentes du conteneur.", td_style),
         Paragraph("/health : auth_configured: false ; /v1/predict : 401.", td_style),
         Paragraph(".env est exclu par .dockerignore ; sans --env-file, les clés ne sont pas injectées à l'exécution.", td_style)],
        [Paragraph("2. Sans -p 8001:8000", td_bold),
         Paragraph("Port 8001 inaccessible depuis Windows.", td_style),
         Paragraph("curl: (7) Failed to connect to localhost port 8001.", td_style),
         Paragraph("EXPOSE 8000 documente uniquement le port ; seul -p crée la redirection réseau hôte:conteneur.", td_style)],
        [Paragraph("3. --host 127.0.0.1", td_bold),
         Paragraph("Rejet des requêtes externes au conteneur.", td_style),
         Paragraph("curl: (52) Empty reply from server / connexion fermée.", td_style),
         Paragraph("127.0.0.1 n'écoute que la boucle locale interne du conteneur ; 0.0.0.0 est requis pour écouter sur eth0.", td_style)],
    ]
    t2 = Table([exp_headers] + exp_rows, colWidths=[85, 95, 130, 230])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))

    # --- SECTION 3 : SPRINT 1 - NGINX REVERSE PROXY ---
    story.append(Paragraph("3. Sprint 1 : La page web dans un conteneur Nginx (Reverse Proxy)", h2_style))
    story.append(Paragraph(
        "Dans <code>web/index.html</code>, l'URL devient relative : <code>const API_URL = '/api/v1/predict';</code>. "
        "Nginx sert la page statique sur le port 80 et relaie les appels <code>/api/</code> vers <code>http://api:8000/</code> "
        "(le slash final retire le préfixe <code>/api/</code> pour transmettre <code>/v1/predict</code> à FastAPI).",
        body_style
    ))

    nginx_and_web_code = (
        "# --- nginx/default.conf ---                        # --- web/Dockerfile ---\n"
        "server {                                            FROM nginx:alpine\n"
        "    listen 80;                                      COPY web/index.html /usr/share/nginx/html/index.html\n"
        "    server_name localhost;                          COPY nginx/default.conf /etc/nginx/conf.d/default.conf\n"
        "    root /usr/share/nginx/html;                     EXPOSE 80\n"
        "    index index.html;\n"
        "    location / { try_files $uri $uri/ /index.html; }\n"
        "    location /api/ {\n"
        "        proxy_pass http://api:8000/;\n"
        "        proxy_set_header Host $host;\n"
        "        proxy_set_header X-Real-IP $remote_addr;\n"
        "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
        "    }\n"
        "}"
    )
    story.append(Preformatted(nginx_and_web_code, code_style))

    # --- SECTION 4 : SPRINT 2 - DOCKER COMPOSE & TESTS BOUT EN BOUT ---
    story.append(Paragraph("4. Sprint 2 : Orchestration Docker Compose, Healthcheck & Tests", h2_style))
    compose_code = (
        "services:\n"
        "  api:\n"
        "    build: { context: ., dockerfile: Dockerfile }\n"
        "    container_name: logiai-api\n"
        "    ports: ['8001:8000']\n"
        "    env_file: [.env]\n"
        "    environment: { LOGIAI_HOME: /app }\n"
        "    volumes: ['./models:/app/models', './data:/app/data']\n"
        "    healthcheck:\n"
        "      test: [\"CMD\", \"python\", \"-c\", \"import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')\"]\n"
        "      interval: 30s\n"
        "      timeout: 5s\n"
        "      retries: 3\n"
        "      start_period: 10s\n"
        "  web:\n"
        "    build: { context: ., dockerfile: web/Dockerfile }\n"
        "    container_name: logiai-web\n"
        "    ports: ['8080:80']\n"
        "    depends_on: { api: { condition: service_healthy } }"
    )
    story.append(Preformatted(compose_code, code_style))

    if os.path.exists("screenshots/terminal_compose_ps.png"):
        story.append(scaled_image("screenshots/terminal_compose_ps.png", target_width=440))
        story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Test de bout en bout sur http://localhost:8080 et inspection réseau F12 (Origine unique, 0 requête OPTIONS) :</b>", body_style))
    if os.path.exists("screenshots/web_nginx_f12.png"):
        story.append(scaled_image("screenshots/web_nginx_f12.png", target_width=430))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # --- PAGE 4 : TESTS CURL, STATS, ADR 004 & TICKET DE SORTIE ---
    story.append(Paragraph("5. Vérification des 4 appels curl via Nginx (Port 8080) & Ressources", h2_style))
    if os.path.exists("screenshots/terminal_curl_nginx.png"):
        story.append(scaled_image("screenshots/terminal_curl_nginx.png", target_width=460))
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Observation des ressources (docker stats), test de panne (étape 8) et volumes (étape 9) :</b>", body_style))
    if os.path.exists("screenshots/terminal_stats_volumes.png"):
        story.append(scaled_image("screenshots/terminal_stats_volumes.png", target_width=460))
        story.append(Spacer(1, 3))

    story.append(Paragraph(
        "• <b>Étape 8 (Arrêt de l'API avec <code>docker compose stop api</code>) :</b> Lorsque l'API est arrêtée, Nginx ne parvient plus à joindre "
        "le service <code>api:8000</code> et renvoie une erreur <b>502 Bad Gateway / 504 Gateway Time-out</b> ; la page affiche alors le message d'erreur réseau. "
        "Dès que l'on exécute <code>docker compose start api</code>, les prédictions refonctionnent immédiatement.<br/>"
        "• <b>Étape 9 (Volumes) :</b> Grâce au bind mount <code>./models:/app/models</code>, un nouveau <code>model.joblib</code> entraîné sur Windows "
        "est immédiatement visible dans le conteneur sans reconstruire l'image. En revanche, une modification du code dans <code>logiai/</code> nécessite "
        "<code>docker compose up -d --build</code>.",
        bullet_style
    ))

    # --- SECTION 6 : ADR 004 & QUESTIONS ---
    story.append(Paragraph("6. Décisions d'architecture (ADR 004) & Ticket de sortie", h2_style))
    story.append(Paragraph(
        "• <b>Décision 1 (Modèle COPY + Volume) :</b> <code>COPY models/</code> dans le Dockerfile garantit une image autonome en production (sans volume externe), "
        "tandis que le bind mount <code>./models:/app/models</code> dans Compose évite de reconstruire l'image à chaque ré-entraînement en développement.<br/>"
        "• <b>Décision 2 (Ports 8080 et 8001) :</b> Publier 8001 en développement permet d'accéder directement à Swagger UI (<code>/docs</code>) et <code>/health</code>. "
        "En production, seul le port 8080 (ou 443) de Nginx doit être publié pour empêcher tout contournement du reverse proxy.",
        bullet_style
    ))

    q_headers = [Paragraph("Question (Ticket de sortie & Compte rendu)", th_style), Paragraph("Réponse synthétique", th_style)]
    q_rows = [
        [Paragraph("1. Différence entre une image et un conteneur ?", td_bold),
         Paragraph("L'image est un modèle immuable en lecture seule (couches figées). Le conteneur est une instance isolée en exécution de cette image avec une fine couche inscriptible éphémère.", td_style)],
        [Paragraph("2. Pourquoi appeler /api/v1/predict et non api:8000 ?", td_bold),
         Paragraph("Le navigateur tourne sur Windows (hors du réseau Docker) et ne peut pas résoudre le nom DNS interne 'api'. Le chemin relatif passe par Nginx sur la même origine (:8080), évitant le CORS.", td_style)],
        [Paragraph("3. Pourquoi depends_on seul ne suffit pas (service_healthy) ?", td_bold),
         Paragraph("depends_on attend seulement que le conteneur démarre, pas que FastAPI ait chargé le modèle. service_healthy attend que le healthcheck (/health) renvoie 200 OK avant de lancer Nginx.", td_style)],
        [Paragraph("4. Dépôt Git, Branche et Tag de livraison", td_bold),
         Paragraph("Dépôt : github.com/malmo23/LogiAI---API-REST-de-Pr-diction-de-Retards | Branche : atelier5 | Tag : tp5", td_style)],
    ]
    t3 = Table([q_headers] + q_rows, colWidths=[185, 355])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(Spacer(1, 2))
    story.append(t3)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF généré avec succès : {filename}")


if __name__ == "__main__":
    build_pdf()
