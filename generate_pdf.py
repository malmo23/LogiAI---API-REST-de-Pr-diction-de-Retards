import os
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
        self.line(36, 32, 576, 32)
        self.drawString(36, 22, "Atelier 3 - API REST avec FastAPI : LogiAI | Compte Rendu | Maldani Mostafa")
        page_text = f"Page {self._pageNumber} / {page_count}"
        self.drawRightString(576, 22, page_text)
        self.restoreState()

def build_pdf(filename="COMPTE_RENDU.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=26,
        bottomMargin=40,
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=2,
    )
    
    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=5,
        spaceAfter=2,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=2,
    )

    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=body_style,
        leftIndent=8,
        spaceAfter=2,
    )

    code_style = ParagraphStyle(
        "CodeText",
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=2,
        spaceAfter=2,
    )

    th_style = ParagraphStyle(
        "TH", fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=colors.white
    )
    td_style = ParagraphStyle(
        "TD", fontName="Helvetica", fontSize=7.2, leading=9, textColor=colors.HexColor("#1e293b")
    )

    story = []

    # En-tête
    story.append(Paragraph("Compte Rendu : TP API REST avec FastAPI (LogiAI)", title_style))
    story.append(Paragraph("<b>Étudiant :</b> Maldani Mostafa &nbsp;&nbsp;|&nbsp;&nbsp; <b>Module :</b> Déploiement d'Applications Intelligentes &nbsp;&nbsp;|&nbsp;&nbsp; <b>Année :</b> 2026-2027", meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceBefore=2, spaceAfter=4))

    # --- PARTIE 1 : ENTRAÎNEMENT & PREMIERS TESTS ---
    story.append(Paragraph("1. Entraînement du modèle & premiers tests pytest", h2_style))
    story.append(Paragraph("On commence par générer les données (<code>python -m logiai.dataset</code>) puis entraîner le modèle (<code>python -m logiai.train</code>).", body_style))
    
    # Capture Train
    if os.path.exists("screenshots/terminal_train.png"):
        story.append(Image("screenshots/terminal_train.png", width=420, height=115))
        story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Sortie de pytest au départ (5 failed, 8 passed) :</b>", body_style))
    story.append(Paragraph(
        "• <i>Pourquoi certains tests attendant 422 passaient-ils déjà ?</i><br/>"
        "Parce que la classe <code>Livraison</code> avait <code>extra=\"forbid\"</code> et ne déclarait que <code>distance_km</code>. Quand les tests envoyaient des données complètes (poids, trafic, etc.), FastAPI rejetait la requête immédiatement pour champ inconnu avec un code 422. C'était un faux vert.",
        bullet_style
    ))

    # --- PARTIE 2 : LE SCHÉMA PYDANTIC ---
    story.append(Spacer(1, 2))
    story.append(Paragraph("2. Schéma Pydantic : bornes physiques retenues", h2_style))
    headers = [Paragraph("Variable", th_style), Paragraph("Min", th_style), Paragraph("Max", th_style), Paragraph("Justification physique", th_style)]
    rows = [
        [Paragraph("distance_km", td_style), Paragraph("1", td_style), Paragraph("1000", td_style), Paragraph("Trajet de livraison routier réel (au moins 1 km, max ~1000 km).", td_style)],
        [Paragraph("poids_kg", td_style), Paragraph("0.1", td_style), Paragraph("5000", td_style), Paragraph("D'un petit colis léger (100g) à la charge max d'un camionnette/fourgon.", td_style)],
        [Paragraph("heure_depart", td_style), Paragraph("0", td_style), Paragraph("23", td_style), Paragraph("Heures valides d'une journée (horloge 0h - 23h).", td_style)],
        [Paragraph("pluie_mm", td_style), Paragraph("0", td_style), Paragraph("100", td_style), Paragraph("Pluie positive ; 100 mm correspond déjà à un épisode orageux extrême.", td_style)],
        [Paragraph("trafic_index", td_style), Paragraph("0", td_style), Paragraph("10", td_style), Paragraph("Indice conventionnel de 0 (fluide) à 10 (embouteillage saturé).", td_style)],
        [Paragraph("nb_arrets", td_style), Paragraph("0", td_style), Paragraph("30", td_style), Paragraph("Nombre d'arrêts de tournée (minimum 0, max réaliste 30).", td_style)],
        [Paragraph("type_vehicule", td_style), Paragraph("-", td_style), Paragraph("-", td_style), Paragraph("Restreint à Literal[\"moto\", \"fourgon\", \"camion\"] selon la flotte.", td_style)],
    ]
    t1 = Table([headers] + rows, colWidths=[80, 25, 30, 405])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t1)

    # --- PARTIE 3 : FONCTION PREDICT ---
    story.append(Spacer(1, 2))
    story.append(Paragraph("3. Implémentation de la route predict()", h2_style))
    code_predict = (
        "@app.post(\"/v1/predict\", response_model=PredictionOut)\n"
        "def predict(livraison: Livraison):\n"
        "    predictor = state.get(\"predictor\")\n"
        "    if predictor is None:\n"
        "        raise HTTPException(status_code=503, detail=\"Modèle non disponible\")\n"
        "    return PredictionOut(**predictor.predict(livraison.model_dump()))"
    )
    story.append(Preformatted(code_predict, code_style))

    # --- PARTIE 4 : TEST DES REQUÊTES ---
    story.append(Spacer(1, 2))
    story.append(Paragraph("4. Réponses observées sur les requêtes types & capture d'exécution", h2_style))
    
    q_headers = [Paragraph("Requête testée", th_style), Paragraph("Code", th_style), Paragraph("Explication", th_style)]
    q_rows = [
        [Paragraph("Livraison normale", td_style), Paragraph("200", td_style), Paragraph("Données conformes, modèle interrogé et résultat renvoyé.", td_style)],
        [Paragraph("distance_km = -5", td_style), Paragraph("422", td_style), Paragraph("Rejeté par Pydantic : ge=1 non respecté.", td_style)],
        [Paragraph("type_vehicule = 'avion'", td_style), Paragraph("422", td_style), Paragraph("Rejeté par Pydantic : hors du Literal['moto', 'fourgon', 'camion'].", td_style)],
        [Paragraph("Modèle absent (sans models/)", td_style), Paragraph("503", td_style), Paragraph("predictor est None dans state, renvoie HTTP 503 Service Unavailable.", td_style)],
    ]
    t2 = Table([q_headers] + q_rows, colWidths=[140, 30, 370])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 2))
    
    # Capture Appel API Predict
    if os.path.exists("screenshots/api_predict_test.png"):
        story.append(Image("screenshots/api_predict_test.png", width=420, height=135))

    # SAUT DE PAGE PROPRE
    story.append(PageBreak())

    # --- PARTIE 5 : QUESTIONS DE COMPRÉHENSION ---
    story.append(Paragraph("5. Questions de compréhension (réponses synthétiques)", h2_style))
    questions = [
        ("1. Pourquoi charger le modèle au démarrage et pas à chaque requête ?",
         "Le chargement depuis le disque (<code>joblib.load</code>) prend plusieurs centaines de millisecondes. En le chargeant une fois dans <code>lifespan</code>, il reste en mémoire vive (RAM) et l'inférence ne prend que 2 à 5 ms par requête."),
        ("2. Qui écrit le contrôle « pluie <= 100 », et où ?",
         "C'est le développeur dans <code>logiai/api/schemas.py</code> avec le paramètre <code>le=100</code> de Pydantic <code>Field()</code>."),
        ("3. Différence entre 422 et 503 ?",
         "• <b>422</b> = faute du <b>client</b> (requête bien formée mais valeurs hors bornes).<br/>"
         "• <b>503</b> = problème côté <b>serveur</b> (le serveur tourne mais le modèle ML n'est pas prêt)."),
        ("4. Pourquoi /v1/predict plutôt que /predict ?",
         "Pour le <b>versionnement</b> de l'API : permet de créer une future <code>/v2</code> sans casser les applications mobiles ou web déjà en production."),
        ("5. Que se passerait-il si distance_km était de type int ?",
         "FastAPI rejetterait ou tronquerait les valeurs décimales (ex: 12.5 km -> 12 km), ce qui causerait une perte de précision pour les prédictions."),
    ]
    for q, a in questions:
        story.append(Paragraph(f"<b>{q}</b>", body_style))
        story.append(Paragraph(a, bullet_style))

    # --- PARTIE 6 : DÉCISION DE CONCEPTION ---
    story.append(Spacer(1, 2))
    story.append(Paragraph("6. Décision de conception : modèle absent", h2_style))
    story.append(Paragraph(
        "• <b>Option A (Répondre 503) :</b> L'API démarre et <code>/health</code> répond <code>model_loaded: false</code>, utile pour diagnostiquer. Mais on reçoit des requêtes pour rien.<br/>"
        "• <b>Option B (Crash direct) :</b> Idéal avec Docker/Kubernetes (Fail Fast). Le conteneur redémarre et aucun trafic n'est dirigé vers une instance cassée.",
        bullet_style
    ))

    # --- PARTIE 7 : TESTS PYTEST VALIDES & CLIENT STREAMLIT ---
    story.append(Spacer(1, 2))
    story.append(Paragraph("7. Validation des tests (15/15) & Interface Streamlit", h2_style))
    story.append(Paragraph("Après ajout des deux nouveaux tests (<code>test_heure_24_refusee</code> et <code>test_alerte_coherente_avec_le_seuil</code>), tous les tests passent :", body_style))

    # Capture Pytest 15 passed
    if os.path.exists("screenshots/terminal_pytest.png"):
        story.append(Image("screenshots/terminal_pytest.png", width=420, height=125))
        story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Interface client Streamlit (connectée à l'API) :</b>", body_style))
    # Capture Streamlit
    if os.path.exists("screenshots/streamlit_app.png"):
        story.append(Image("screenshots/streamlit_app.png", width=380, height=160))
        story.append(Spacer(1, 2))

    # --- PARTIE 8 : GIT ---
    story.append(Paragraph("8. Rendu Git", h2_style))
    story.append(Paragraph(
        "• <b>Dépôt GitHub :</b> https://github.com/malmo23/logiai<br/>"
        "• <b>Branche :</b> <code>tp-api</code> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Pull Request :</b> https://github.com/malmo23/logiai/pull/1",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF généré avec succès : {filename}")

if __name__ == "__main__":
    build_pdf()
