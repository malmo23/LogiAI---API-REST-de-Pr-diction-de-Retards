import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, HRFlowable
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
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 38, 576, 38)
        self.drawString(36, 26, "Atelier 3 - API REST avec FastAPI : LogiAI | Compte Rendu")
        page_text = f"Page {self._pageNumber} / {page_count}"
        self.drawRightString(576, 26, page_text)
        self.restoreState()

def build_pdf(filename="COMPTE_RENDU.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=28,
        bottomMargin=46,
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=3,
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#475569"),
        spaceAfter=6,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=7,
        spaceAfter=3,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=3,
    )

    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=body_style,
        leftIndent=10,
        spaceAfter=2,
    )

    code_block_style = ParagraphStyle(
        "CodeBlock",
        fontName="Courier",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.8,
        borderPadding=4,
        spaceBefore=2,
        spaceAfter=3,
    )

    th_style = ParagraphStyle(
        "TH",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )

    td_style = ParagraphStyle(
        "TD",
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
    )

    story = []

    # En-tête
    story.append(Paragraph("Compte Rendu : TP API REST avec FastAPI (LogiAI)", title_style))
    story.append(Paragraph("<b>Module :</b> Développement et déploiement d’applications intelligentes &nbsp;|&nbsp; <b>Année :</b> 2026-2027 &nbsp;|&nbsp; <b>Groupe :</b> ................", subtitle_style))
    story.append(Paragraph("<b>Noms des étudiants :</b> .......................................................................................................................................", body_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1e3a8a"), spaceBefore=3, spaceAfter=5))

    # Section 1
    story.append(Paragraph("1. Environnement et premiers tests", h2_style))
    story.append(Paragraph("<b>Sortie de <code>python -m pytest</code> au départ :</b>", body_style))
    test_output = (
        "collected 13 items\n"
        "tests\\test_api.py ..FFFF......F                                          [100%]\n"
        "============================= 5 failed, 8 passed in 4.07s ============================="
    )
    story.append(Preformatted(test_output, code_block_style))
    story.append(Paragraph(
        "<b>Pourquoi certains tests attendant un code 422 passaient-ils déjà alors que rien n'était écrit ?</b>",
        body_style
    ))
    story.append(Paragraph(
        "Dans le code starter, la classe Pydantic <code>Livraison</code> était configurée avec <code>model_config = ConfigDict(extra=\"forbid\")</code> et ne contenait initialement que le champ <code>distance_km</code>. Dès qu'une requête de test envoyait les autres variables (<code>poids_kg</code>, <code>heure_depart</code>, etc.), Pydantic la rejetait immédiatement avec une erreur HTTP <b>422 Unprocessable Entity</b> pour champs inconnus interdits. Ainsi, les tests attendant un code 422 passaient par « faux vert » sans tester la validation métier des variables.",
        bullet_style
    ))

    # Section 2
    story.append(Paragraph("2. Schéma Pydantic (Livraison) et justification physique", h2_style))
    
    headers = [
        Paragraph("Variable", th_style),
        Paragraph("Min", th_style),
        Paragraph("Max", th_style),
        Paragraph("Justification physique", th_style),
    ]
    rows = [
        [Paragraph("<b>distance_km</b>", td_style), Paragraph("1", td_style), Paragraph("1000", td_style), Paragraph("Distance réelle en km d'une livraison routière (min 1 km, max environ 1000 km).", td_style)],
        [Paragraph("<b>poids_kg</b>", td_style), Paragraph("0.1", td_style), Paragraph("5000", td_style), Paragraph("D'un petit paquet léger (100 g) à la charge utile maximale d'un utilitaire / camionnette.", td_style)],
        [Paragraph("<b>heure_depart</b>", td_style), Paragraph("0", td_style), Paragraph("23", td_style), Paragraph("Heures valides d'une journée (horloge de 0h à 23h).", td_style)],
        [Paragraph("<b>pluie_mm</b>", td_style), Paragraph("0", td_style), Paragraph("100", td_style), Paragraph("Précipitations physiques positives ; 100 mm représente déjà un épisode pluvieux extrême.", td_style)],
        [Paragraph("<b>trafic_index</b>", td_style), Paragraph("0", td_style), Paragraph("10", td_style), Paragraph("Indice d'encombrement routier conventionnel : 0 = fluide, 10 = axe complètement saturé.", td_style)],
        [Paragraph("<b>nb_arrets</b>", td_style), Paragraph("0", td_style), Paragraph("30", td_style), Paragraph("Nombre d'arrêts intermédiaires sur la tournée (au moins 0, max réaliste 30 par tournée).", td_style)],
        [Paragraph("<b>type_vehicule</b>", td_style), Paragraph("-", td_style), Paragraph("-", td_style), Paragraph("Restreint à <code>Literal[\"moto\", \"fourgon\", \"camion\"]</code> correspondant à la flotte disponible.", td_style)],
    ]
    
    t1 = Table([headers] + rows, colWidths=[90, 30, 35, 385])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t1)

    # Section 3
    story.append(Paragraph("3. Implémentation de la fonction predict()", h2_style))
    code_predict = (
        "@app.post(\"/v1/predict\", response_model=PredictionOut)\n"
        "def predict(livraison: Livraison):\n"
        "    predictor = state.get(\"predictor\")\n"
        "    if predictor is None:\n"
        "        raise HTTPException(status_code=503, detail=\"Modèle non disponible / non chargé\")\n"
        "    return PredictionOut(**predictor.predict(livraison.model_dump()))"
    )
    story.append(Preformatted(code_predict, code_block_style))

    # Section 4
    story.append(Paragraph("4. Réponses observées sur quatre requêtes types", h2_style))
    q_headers = [
        Paragraph("Requête testée", th_style),
        Paragraph("Code", th_style),
        Paragraph("Explication technique", th_style),
    ]
    q_rows = [
        [Paragraph("<b>Livraison normale</b>", td_style), Paragraph("<b>200</b>", td_style), Paragraph("Payload conforme au schéma Pydantic, le modèle est présent en mémoire et renvoie la prédiction.", td_style)],
        [Paragraph("<b>distance_km = -5</b>", td_style), Paragraph("<b>422</b>", td_style), Paragraph("Rejeté par Pydantic : violation de la borne minimale <code>ge=1</code> sur <code>distance_km</code>.", td_style)],
        [Paragraph("<b>type_vehicule = \"avion\"</b>", td_style), Paragraph("<b>422</b>", td_style), Paragraph("Rejeté par Pydantic : la valeur ne fait pas partie du <code>Literal[\"moto\", \"fourgon\", \"camion\"]</code>.", td_style)],
        [Paragraph("<b>Modèle absent (sans models/)</b>", td_style), Paragraph("<b>503</b>", td_style), Paragraph("<code>state.get(\"predictor\")</code> renvoie <code>None</code>, l'endpoint lève une <code>HTTPException(503)</code>.", td_style)],
    ]
    t2 = Table([q_headers] + q_rows, colWidths=[150, 40, 350])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t2)

    # Section 5
    story.append(Paragraph("5. Questions de compréhension", h2_style))
    questions = [
        ("1. Pourquoi charge-t-on le modèle au démarrage et pas à chaque requête ?",
         "La lecture du fichier sur le disque (<code>joblib.load</code>) et la désérialisation prennent plusieurs centaines de millisecondes. En le chargeant au démarrage via <code>lifespan</code>, le modèle reste résident en RAM et chaque inférence s'exécute en quelques millisecondes sans surcharger le processeur."),
        ("2. Qui écrit le contrôle « pluie <= 100 », et où est-il écrit ?",
         "C'est le développeur qui l'exprime de manière déclarative dans la classe Pydantic <code>Livraison</code> du fichier <code>logiai/api/schemas.py</code>, à l'aide de l'argument <code>le=100</code> dans <code>Field()</code>."),
        ("3. Quelle est la différence fondamentale entre les statuts 422 et 503 ?",
         "Le code <b>422 (Unprocessable Entity)</b> signale une erreur côté <b>client</b> (requête JSON valide mais données hors bornes). Le code <b>503 (Service Unavailable)</b> signale un état côté <b>serveur</b> (le serveur HTTP tourne, mais la dépendance modèle ML n'est temporairement pas disponible)."),
        ("4. Pourquoi utilise-t-on la route versionnée /v1/predict plutôt que simplement /predict ?",
         "Le versionnement (<code>/v1</code>) permet de faire évoluer le contrat d'API (ex: une future <code>/v2</code>) sans casser le fonctionnement des clients existants (applications mobiles, partenaires, web)."),
        ("5. Que se passerait-il si la variable distance_km était déclarée de type int ?",
         "FastAPI tenterait de forcer la conversion en entier ou rejetterait les nombres décimaux. Une distance réelle comme <code>12.5 km</code> serait tronquée à <code>12 km</code> ou refusée avec un code 422."),
    ]
    for q, a in questions:
        story.append(Paragraph(f"<b>{q}</b>", body_style))
        story.append(Paragraph(a, bullet_style))

    # Section 6
    story.append(Paragraph("6. Décision de conception : comportement en cas de modèle absent", h2_style))
    story.append(Paragraph(
        "• <b>Option A (Démarrer et répondre 503) :</b> Permet de conserver l'API accessible aux outils de diagnostic et supervision. Le endpoint <code>/health</code> peut renvoyer <code>{\"status\": \"ok\", \"model_loaded\": false}</code>, ce qui permet à un opérateur de comprendre la cause de la panne. En revanche, le serveur reçoit du trafic client qu'il ne peut honorer.<br/>"
        "• <b>Option B (Crash au démarrage / Fail Fast) :</b> Très adaptée aux orchestrateurs (Kubernetes/Docker). Si le modèle est absent, le conteneur ne passe jamais en état <i>Ready</i> ; aucun trafic client ne lui est envoyé et les équipes SRE sont immédiatement alertées.",
        bullet_style
    ))

    # Section 7
    story.append(Paragraph("7. Lien de la Pull Request & Tests", h2_style))
    story.append(Paragraph(
        "• <b>Dépôt GitHub :</b> <font color=\"#2563eb\">https://github.com/malmo23/logiai</font> &nbsp;|&nbsp; <b>Branche :</b> <code>tp-api</code> vers <code>main</code><br/>"
        "• <b>Lien Pull Request :</b> https://github.com/malmo23/logiai/pull/1<br/>"
        "• <b>Validation pytest :</b> <code>15 passed in 3.62s</code> (13 tests initiaux + 2 tests personnels ajoutés)",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF généré avec succès : {filename}")

if __name__ == "__main__":
    build_pdf()
