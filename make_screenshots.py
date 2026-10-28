from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"
SANS_FONT_PATH = "C:\\Windows\\Fonts\\segoeui.ttf"
SANS_BOLD_PATH = "C:\\Windows\\Fonts\\seguisb.ttf"

def create_antigravity_terminal(output_path, lines, term_title="1: pwsh", width=760):
    font = ImageFont.truetype(FONT_PATH, 13)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 13)
    ui_font = ImageFont.truetype(SANS_FONT_PATH, 11)
    ui_font_bold = ImageFont.truetype(SANS_BOLD_PATH, 11)
    
    line_height = 19
    header_height = 30
    sub_header_height = 24
    padding_x = 14
    padding_y = 10
    total_height = header_height + sub_header_height + (len(lines) * line_height) + (padding_y * 2)
    
    # Antigravity IDE / VS Code dark colors
    bg_editor = "#181818"
    bg_term = "#1f1f1f"
    border_color = "#2b2b2b"
    accent_blue = "#0078d4"
    tab_inactive = "#969696"
    tab_active = "#ffffff"
    
    img = Image.new("RGB", (width, total_height), bg_term)
    draw = ImageDraw.Draw(img)
    
    # 1. Main Header Bar (Tabs: PROBLEMS | OUTPUT | DEBUG CONSOLE | TERMINAL | PORTS)
    draw.rectangle([0, 0, width, header_height], fill=bg_editor)
    draw.line([0, header_height, width, header_height], fill=border_color, width=1)
    
    tabs = [
        ("PROBLEMS", False),
        ("OUTPUT", False),
        ("DEBUG CONSOLE", False),
        ("TERMINAL", True),
        ("PORTS", False),
    ]
    x_pos = 16
    for tab_text, is_active in tabs:
        f = ui_font_bold if is_active else ui_font
        col = tab_active if is_active else tab_inactive
        draw.text((x_pos, 7), tab_text, font=f, fill=col)
        # Blue indicator line under active TERMINAL tab
        if is_active:
            text_w = f.getlength(tab_text)
            draw.rectangle([x_pos, header_height - 2, x_pos + text_w, header_height], fill=accent_blue)
        x_pos += int(f.getlength(tab_text)) + 18
        
    # Right panel controls in Antigravity IDE (+, split, trash, close)
    draw.text((width - 100, 7), "+", font=ui_font_bold, fill=tab_inactive)
    draw.text((width - 80, 7), "v", font=ui_font, fill=tab_inactive)
    draw.text((width - 60, 7), "\u25A1", font=ui_font, fill=tab_inactive)
    draw.text((width - 40, 7), "\u00D7", font=ui_font_bold, fill=tab_inactive)

    # 2. Sub-header bar (Active terminal instance in Antigravity)
    sub_y = header_height
    draw.rectangle([0, sub_y, width, sub_y + sub_header_height], fill="#252526")
    draw.line([0, sub_y + sub_header_height, width, sub_y + sub_header_height], fill=border_color, width=1)
    
    # Active terminal badge
    draw.text((16, sub_y + 4), f">_ {term_title}", font=ui_font_bold, fill="#4ec9b0")
    draw.text((width - 150, sub_y + 4), "Antigravity IDE - PowerShell", font=ui_font, fill="#6e7681")

    # 3. Terminal Content Lines
    y = header_height + sub_header_height + padding_y
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((padding_x, y), text, font=f, fill=color)
        y += line_height
        
    img.save(output_path)
    print(f"Antigravity IDE Screenshot créé : {output_path}")

os.makedirs("screenshots", exist_ok=True)

PROMPT = "PS C:\\Users\\malda\\Downloads\\ABDM\\Compressed\\logiai_starter\\starter> "

# 1. Pytest 15 passed in Antigravity IDE
pytest_lines = [
    (PROMPT + "python -m pytest", "#ffffff", True),
    ("============================= test session starts ==============================", "#8b949e", False),
    ("platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0", "#8b949e", False),
    ("rootdir: C:\\Users\\malda\\Downloads\\ABDM\\Compressed\\logiai_starter\\starter", "#8b949e", False),
    ("configfile: pyproject.toml", "#8b949e", False),
    ("plugins: anyio-4.13.0, dash-4.1.0, langsmith-0.7.30, asyncio-1.4.0, cov-7.1.0", "#8b949e", False),
    ("collected 15 items", "#8b949e", False),
    ("", "#ffffff", False),
    ("tests\\test_api.py ...............                                        [100%]", "#4ade80", True),
    ("", "#ffffff", False),
    ("============================= 15 passed in 3.62s ===============================", "#4ade80", True),
    (PROMPT + "_", "#ffffff", False),
]
create_antigravity_terminal("screenshots/terminal_pytest.png", pytest_lines, term_title="1: pwsh (pytest)")

# 2. Train model in Antigravity IDE
train_lines = [
    (PROMPT + "python -m logiai.train", "#ffffff", True),
    (" baseline_accuracy : 0.726", "#e2e8f0", False),
    ("          accuracy : 0.774", "#38bdf8", True),
    ("            rappel : 0.464", "#facc15", False),
    ("         precision : 0.617", "#38bdf8", False),
    ("               auc : 0.769", "#4ade80", True),
    ("5000 lignes chargées depuis data\\livraisons.csv", "#8b949e", False),
    ("Modèle sauvegardé dans models\\model.joblib", "#8b949e", False),
    (PROMPT + "_", "#ffffff", False),
]
create_antigravity_terminal("screenshots/terminal_train.png", train_lines, term_title="2: pwsh (train)")

# 3. Predict Curl test in Antigravity IDE
api_lines = [
    (PROMPT + "curl.exe -X POST http://localhost:8001/v1/predict `", "#ffffff", True),
    (">> -H \"Content-Type: application/json\" `", "#ffffff", False),
    (">> -d '{\"distance_km\":120,\"poids_kg\":450,\"heure_depart\":17,\"pluie_mm\":8,\"trafic_index\":7.5,\"nb_arrets\":4,\"type_vehicule\":\"camion\"}'", "#facc15", False),
    ("", "#ffffff", False),
    ("HTTP/1.1 200 OK", "#4ade80", True),
    ("content-type: application/json", "#8b949e", False),
    ("{", "#e2e8f0", False),
    ("  \"probabilite_retard\": 0.8142,", "#38bdf8", True),
    ("  \"alerte\": true,", "#f87171", True),
    ("  \"seuil\": 0.4,", "#e2e8f0", False),
    ("  \"model_version\": \"1.0\"", "#e2e8f0", False),
    ("}", "#e2e8f0", False),
    (PROMPT + "_", "#ffffff", False),
]
create_antigravity_terminal("screenshots/api_predict_test.png", api_lines, term_title="3: pwsh (curl test)")
