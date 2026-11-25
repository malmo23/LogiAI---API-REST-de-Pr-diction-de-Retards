"""Génère COMPTE_RENDU.pdf pour l'Atelier 6 - Packaging logiai."""
import os
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable, Image, PageBreak, Paragraph, Preformatted,
    SimpleDocTemplate, Spacer, Table, TableStyle
)
from reportlab.pdfgen import canvas

W, H = A4

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pages = []

    def showPage(self):
        self._pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._pages)
        for state in self._pages:
            self.__dict__.update(state)
            self._draw_footer(n)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_footer(self, total):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.4)
        self.line(36, 28, W - 36, 28)
        self.drawString(36, 17, "Atelier 6 — Faire de LogiAI un package Python installable | Réalisé par : Maldani Mostafa")
        self.drawRightString(W - 36, 17, f"Page {self._pageNumber} / {total}")
        self.restoreState()


def scaled_image(path, target_width=480):
    with PILImage.open(path) as im:
        w, h = im.size
    return Image(path, width=target_width, height=target_width * h / w)


def build():
    doc = SimpleDocTemplate(
        "COMPTE_RENDU.pdf",
        pagesize=A4,
        leftMargin=36, rightMargin=36,
        topMargin=26, bottomMargin=42,
    )

    s = getSampleStyleSheet()

    def ps(name, **kw):
        p = ParagraphStyle(name, parent=s["Normal"], **kw)
        return p

    h1 = ps("H1", fontName="Helvetica-Bold", fontSize=14, leading=17,
             textColor=colors.HexColor("#1e3a8a"), spaceAfter=2)
    meta = ps("Meta", fontName="Helvetica-Bold", fontSize=8, leading=11,
              textColor=colors.HexColor("#334155"), spaceAfter=4)
    h2 = ps("H2", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
            textColor=colors.HexColor("#1e40af"), spaceBefore=6, spaceAfter=3)
    body = ps("Body", fontName="Helvetica", fontSize=8, leading=11,
              textColor=colors.HexColor("#1e293b"), spaceAfter=3)
    bullet = ps("Bullet", fontName="Helvetica", fontSize=8, leading=11,
                textColor=colors.HexColor("#1e293b"), leftIndent=10, spaceAfter=2)
    code = ps("Code", fontName="Courier", fontSize=7.2, leading=9.5,
              textColor=colors.HexColor("#0f172a"),
              backColor=colors.HexColor("#f8fafc"),
              borderColor=colors.HexColor("#cbd5e1"),
              borderWidth=0.4, borderPadding=4,
              spaceBefore=2, spaceAfter=3)
    th = ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=colors.white)
    td = ParagraphStyle("TD", fontName="Helvetica", fontSize=7.2, leading=9.2, textColor=colors.HexColor("#1e293b"))
    tdb = ParagraphStyle("TDB", fontName="Helvetica-Bold", fontSize=7.2, leading=9.2, textColor=colors.HexColor("#0f172a"))

    BLUE = colors.HexColor("#1e3a8a")

    def tbl(headers, rows, widths):
        t = Table([[Paragraph(h, th) for h in headers]] +
                  [[Paragraph(c, td if i else tdb) for i, c in enumerate(r)] for r in rows],
                  colWidths=widths)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ]))
        return t

    story = []

    # ── ENTÊTE ──────────────────────────────────────────────────────────────────
    story.append(Paragraph("Compte Rendu : Atelier 6 — Faire de LogiAI un package Python installable", h1))
    story.append(Paragraph(
        "<b>Réalisé par :</b> Maldani Mostafa &nbsp;|&nbsp; "
        "<b>Professeur :</b> Pr. Soukaina Gouraguine &nbsp;|&nbsp; "
        "<b>Module :</b> Déploiement d'Applications Intelligentes (2026-2027)", meta))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceBefore=2, spaceAfter=6))

    # ── 1. CONSTAT DE DÉPART ────────────────────────────────────────────────────
    story.append(Paragraph("1. Constat de départ : logiai ne marche que dans son propre dossier", h2))
    story.append(Paragraph(
        "Sans <code>pyproject.toml</code>, Python ne connaît le dossier "
        "<code>logiai/</code> que si on l'appelle depuis <code>C:\\…\\atelier5</code>. "
        "Dès qu'on change de répertoire ou qu'on installe dans un autre venv, "
        "<b>ModuleNotFoundError</b> apparaît. L'atelier transforme ce dossier en "
        "package installable via <code>pip</code>.", body))
    story.append(tbl(
        ["Étape", "Avant l'atelier", "Après l'atelier"],
        [
            ["Importer logiai depuis /tmp", "ModuleNotFoundError", "✅ fonctionne"],
            ["Commande CLI", "aucune", "✅ logiai-predict <fichier.json>"],
            ["Distribution", "copier-coller le dossier", "✅ pip install logiai-0.1.0-py3-none-any.whl"],
            ["Tests portables", "dépendent du cwd", "✅ 48 passed partout"],
        ],
        [120, 180, 220]))
    story.append(Spacer(1, 4))

    # ── 2. STEP 1 : TESTS DE DÉPART ─────────────────────────────────────────────
    story.append(Paragraph("2. Étape 1 — Tests de départ & constat (python -m pytest)", h2))
    story.append(Paragraph(
        "Avant toute modification, on vérifie que les 45 tests de l'Atelier 4/5 passent, "
        "puis on ajoute <code>tests/test_package.py</code> qui échoue intentionnellement "
        "(2 tests FAILED) car le package n'est pas encore installé.", body))
    if os.path.exists("screenshots/01_pytest_48passed.png"):
        story.append(scaled_image("screenshots/01_pytest_48passed.png"))
        story.append(Spacer(1, 4))

    # ── 3. STEP 2-3 : PYPROJECT.TOML + pip install -e ───────────────────────────
    story.append(Paragraph("3. Étapes 2 & 3 — pyproject.toml + pip install -e . + logiai-predict", h2))
    story.append(Preformatted(
        "[build-system]\n"
        'requires = ["setuptools>=68", "wheel"]\n'
        'build-backend = "setuptools.build_meta"\n\n'
        "[project]\n"
        'name = "logiai"\n'
        'version = "0.1.0"\n'
        'requires-python = ">=3.10"\n'
        'dependencies = ["pandas>=2.0", "numpy", "scikit-learn>=1.3", "joblib"]\n\n'
        "[project.optional-dependencies]\n"
        'api = ["fastapi", "uvicorn", "pydantic"]\n'
        'dev = ["pytest", "ruff", "httpx"]\n\n'
        "[project.scripts]\n"
        'logiai-predict = "logiai.cli:main"\n\n'
        "[tool.setuptools.packages.find]\n"
        'include = ["logiai*"]', code))
    story.append(Paragraph(
        "La commande <code>logiai-predict</code> (dans <code>logiai/cli.py</code>) "
        "charge le modèle via <code>Predictor()</code> et affiche : "
        "<b>Probabilité de retard : 73 % (ALERTE)</b> pour le fichier "
        "<code>livraison.json</code> de référence.", body))
    if os.path.exists("screenshots/02_pip_install_e_cli.png"):
        story.append(scaled_image("screenshots/02_pip_install_e_cli.png"))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ── 4. STEP 4 : WHEEL ───────────────────────────────────────────────────────
    story.append(Paragraph("4. Étape 4 — Construction du wheel (python -m build)", h2))
    story.append(Paragraph(
        "<code>python -m build</code> produit deux artefacts dans <code>dist/</code> : "
        "un sdist (<code>.tar.gz</code>) et un wheel universel (<code>-py3-none-any.whl</code>). "
        "Le wheel contient <code>logiai-0.1.0.dist-info/entry_points.txt</code> qui déclare "
        "la commande <code>logiai-predict</code> pour pip.", body))
    if os.path.exists("screenshots/03_build_wheel.png"):
        story.append(scaled_image("screenshots/03_build_wheel.png"))
        story.append(Spacer(1, 4))

    # ── 5. TEST COLLÈGUE ─────────────────────────────────────────────────────────
    story.append(Paragraph("5. Test du collègue — Installation dans un venv isolé", h2))
    story.append(Paragraph(
        "On crée un venv temporaire vierge dans <code>%TEMP%\\essai</code> et on installe "
        "uniquement le wheel. Sans <code>LOGIAI_HOME</code>, le modèle n'est pas trouvé "
        "(comportement attendu et documenté). En fixant la variable, la prédiction fonctionne.", body))
    if os.path.exists("screenshots/06_test_collegue.png"):
        story.append(scaled_image("screenshots/06_test_collegue.png"))
        story.append(Spacer(1, 4))

    # ── 6. DOCKER ───────────────────────────────────────────────────────────────
    story.append(Paragraph("6. Adaptation Docker — Dockerfile installe le package via pip", h2))
    story.append(Preformatted(
        "FROM python:3.11-slim\n"
        "WORKDIR /app\n"
        "COPY requirements.txt ./\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "# installe logiai comme vrai package (entry_points.txt inclus)\n"
        "COPY pyproject.toml /tmp/build/\n"
        "COPY logiai/ /tmp/build/logiai/\n"
        "RUN pip install --no-cache-dir --no-deps /tmp/build && rm -rf /tmp/build\n"
        "COPY data/ ./data/\n"
        "COPY models/ ./models/\n"
        "ENV LOGIAI_HOME=/app\n"
        "EXPOSE 8000\n"
        'CMD ["uvicorn", "logiai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]',
        code))
    if os.path.exists("screenshots/04_docker_compose_up.png"):
        story.append(scaled_image("screenshots/04_docker_compose_up.png"))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ── 7. TESTS CURL ───────────────────────────────────────────────────────────
    story.append(Paragraph("7. Vérification end-to-end — Appels curl via Nginx (port 8080)", h2))
    story.append(tbl(
        ["Requête", "Code HTTP", "Corps de réponse"],
        [
            ["GET /api/health", "200 OK", '{"status":"ok","model_loaded":true,"auth_configured":true}'],
            ["POST /api/v1/predict + clé valide", "200 OK", '{"probabilite_retard":0.732,"alerte":true}'],
            ["POST /api/v1/predict + mauvaise clé", "401 Unauthorized", '{"detail":"Clé API invalide."}'],
            ["POST /api/v1/predict sans clé", "401 Unauthorized", '{"detail":"Clé API manquante."}'],
        ],
        [130, 100, 300]))
    story.append(Spacer(1, 4))
    if os.path.exists("screenshots/05_curl_nginx.png"):
        story.append(scaled_image("screenshots/05_curl_nginx.png"))
        story.append(Spacer(1, 4))

    # ── 8. QUESTIONS & RÉPONSES CLÉS DU TP ──────────────────────────────────────
    story.append(Paragraph("8. Réponses clés du TP & ADR 005", h2_style if False else h2))
    questions = [
        ("Étape 1 — Constat hors du dossier du projet :",
         "« Pour utiliser LogiAI, mon collègue doit obligatoirement se placer dans le dossier du projet ou modifier son PYTHONPATH, car le code n'est pas installé dans l'environnement Python. »"),
        ("Étape 4 — Que répond logiai-predict vs l'API avec pluie_mm = 500 ?",
         "logiai-predict répond « Probabilité de retard : 73 % (ALERTE) » (aucune validation), tandis que l'API renvoie HTTP 422 Unprocessable Entity car le schéma Pydantic Livraison impose pluie_mm <= 100.0."),
        ("Étape 5 — Les deux messages du test collègue (%TEMP%\\essai) :",
         "1) Sans LOGIAI_HOME : FileNotFoundError sur ...\\essai\\models\\model.joblib (normal : le modèle n'est pas dans le wheel). 2) Avec LOGIAI_HOME : « Probabilité de retard : 73 % (ALERTE) »."),
        ("Étape 6 — Chemin de logiai dans le conteneur Docker :",
         "docker compose exec api python -c \"import logiai; print(logiai.__file__)\" affiche /usr/local/lib/python3.11/site-packages/logiai/__init__.py, et /app contient uniquement data, models et requirements.txt."),
        ("ADR 005 — >= dans pyproject.toml vs == dans requirements.txt ; modèle hors wheel :",
         ">= garde la compatibilité chez les collègues ; == fige l'image Docker. Le modèle reste hors du wheel (LOGIAI_HOME) pour éviter de rebuilder le package à chaque ré-entraînement."),
    ]
    for q, a in questions:
        story.append(Paragraph(f"<b>{q}</b> {a}", bullet))
        story.append(Spacer(1, 2))

    # ── 9. TICKET DE SORTIE ─────────────────────────────────────────────────────
    story.append(Paragraph("9. Ticket de sortie", h2))
    story.append(tbl(
        ["Question", "Réponse"],
        [
            ["1. Docker et le package : quelle différence ?",
             "Le package (.whl) distribue le code Python ; Docker empaquette tout l'environnement isolé (OS, Python, dépendances figées, services)."],
            ["2. pip install -e . ou wheel : développer vs livrer ?",
             "pip install -e . pour développer (code modifié immédiatement actif) ; wheel (.whl) pour livrer une version figée."],
            ["3. Qu'est-ce qui n'est pas dans le wheel, et que livrer avec ?",
             "models/, data/, .env et tests/ sont exclus. Il faut livrer le modèle (models/) et la config (LOGIAI_HOME, .env) à côté."],
            ["4. Qu'est-ce qui reste flou pour vous ?",
             "L'utilisation du multi-stage build Docker pour réduire encore la taille de l'image finale avec les extras."],
        ],
        [185, 345]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF généré : COMPTE_RENDU.pdf")


if __name__ == "__main__":
    build()
