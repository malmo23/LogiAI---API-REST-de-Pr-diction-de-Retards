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

    # ── 8. QUESTIONS ────────────────────────────────────────────────────────────
    story.append(Paragraph("8. Questions de compréhension", h2))
    questions = [
        ("Quelle différence entre un dossier Python et un package installable ?",
         "Un dossier avec __init__.py est importable seulement si Python est lancé depuis le répertoire parent. "
         "Un package installable (pyproject.toml + pip install) est enregistré dans site-packages et reste "
         "importable depuis n'importe quel répertoire de n'importe quel projet."),
        ("À quoi sert [project.scripts] dans pyproject.toml ?",
         "Il déclare des points d'entrée (entry_points). pip crée un exécutable "
         "(logiai-predict.exe sous Windows) qui appelle la fonction logiai.cli:main, "
         "accessible dans le PATH sans avoir à invoquer python manuellement."),
        ("Pourquoi le mode éditable (-e) est-il pratique en développement ?",
         "pip install -e . crée un lien symbolique vers le code source. Toute modification du code "
         "source est immédiatement visible sans réinstaller le package, ce qui accélère le cycle "
         "édition → test."),
        ("Pourquoi le Dockerfile installe-t-il le package au lieu de faire COPY logiai/ ?",
         "En installant via pip install, le conteneur dispose des entry_points et des métadonnées "
         "dist-info (version, dépendances), exactement comme chez n'importe quel utilisateur. "
         "Cela valide que le packaging est correct et cohérent entre local et production."),
        ("Que manque-t-il pour publier sur PyPI ?",
         "Un compte PyPI, un token d'API, compléter les métadonnées METADATA (description, auteur, "
         "licence, classifiers), puis : python -m twine upload dist/*."),
    ]
    for i, (q, a) in enumerate(questions, 1):
        story.append(Paragraph(f"<b>{i}. {q}</b>", bullet))
        story.append(Paragraph(a, bullet))
        story.append(Spacer(1, 2))

    # ── 9. TICKET DE SORTIE ─────────────────────────────────────────────────────
    story.append(Paragraph("9. Ticket de sortie", h2))
    story.append(tbl(
        ["Question", "Réponse"],
        [
            ["Différence import logiai depuis /tmp avant et après ?",
             "Avant : ModuleNotFoundError. Après pip install -e . : importable partout car enregistré dans site-packages."],
            ["La commande logiai-predict fonctionne-t-elle depuis n'importe où ?",
             "Oui pour l'import Python. Elle a besoin de LOGIAI_HOME pour trouver models/ et data/."],
            ["Qu'est-ce qui reste flou ?",
             "La gestion des dépendances optionnelles extras (fastapi, streamlit) dans le wheel et leur impact sur la taille de l'image Docker."],
        ],
        [170, 360]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF généré : COMPTE_RENDU.pdf")


if __name__ == "__main__":
    build()
