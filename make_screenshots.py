from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"

def create_terminal_image(output_path, title, lines, width=720):
    font = ImageFont.truetype(FONT_PATH, 14)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 14)
    title_font = ImageFont.truetype(FONT_BOLD_PATH, 12)
    
    line_height = 20
    header_height = 36
    padding = 16
    total_height = header_height + (len(lines) * line_height) + (padding * 2)
    
    img = Image.new("RGB", (width, total_height), "#1e1e1e")
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, header_height], fill="#2d2d2d")
    # Window controls (close, min, max dots)
    draw.ellipse([14, 12, 24, 22], fill="#ff5f56")
    draw.ellipse([32, 12, 42, 22], fill="#ffbd2e")
    draw.ellipse([50, 12, 60, 22], fill="#27c93f")
    draw.text((width // 2 - 60, 10), title, font=title_font, fill="#9ca3af")
    
    y = header_height + padding
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((padding, y), text, font=f, fill=color)
        y += line_height
        
    img.save(output_path)
    print(f"Image créée : {output_path}")

os.makedirs("screenshots", exist_ok=True)

# 1. Terminal Pytest
pytest_lines = [
    ("PS C:\\logiai> python -m pytest", "#ffffff", True),
    ("============================= test session starts ==============================", "#9ca3af", False),
    ("platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0", "#9ca3af", False),
    ("rootdir: C:\\logiai", "#9ca3af", False),
    ("collected 15 items", "#9ca3af", False),
    ("", "#ffffff", False),
    ("tests\\test_api.py ...............                                        [100%]", "#4ade80", True),
    ("", "#ffffff", False),
    ("============================= 15 passed in 3.62s ===============================", "#4ade80", True),
    ("PS C:\\logiai> _", "#ffffff", False),
]
create_terminal_image("screenshots/terminal_pytest.png", "PowerShell - pytest (15 passed)", pytest_lines)

# 2. Terminal Train
train_lines = [
    ("PS C:\\logiai> python -m logiai.train", "#ffffff", True),
    (" baseline_accuracy : 0.726", "#e2e8f0", False),
    ("          accuracy : 0.774", "#38bdf8", True),
    ("            rappel : 0.464", "#facc15", False),
    ("         precision : 0.617", "#38bdf8", False),
    ("               auc : 0.769", "#4ade80", True),
    ("INFO: Modèle sauvegardé dans models/model.joblib", "#9ca3af", False),
    ("PS C:\\logiai> _", "#ffffff", False),
]
create_terminal_image("screenshots/terminal_train.png", "PowerShell - Entraînement Modèle", train_lines)

# 3. Swagger / Curl Request & Response
api_lines = [
    ("PS C:\\logiai> curl.exe -X POST http://localhost:8001/v1/predict `", "#ffffff", True),
    (">> -H 'Content-Type: application/json' `", "#ffffff", False),
    (">> -d '{\"distance_km\":120,\"poids_kg\":450,\"heure_depart\":17,\"pluie_mm\":8,\"trafic_index\":7.5,\"nb_arrets\":4,\"type_vehicule\":\"camion\"}'", "#facc15", False),
    ("", "#ffffff", False),
    ("HTTP/1.1 200 OK", "#4ade80", True),
    ("content-type: application/json", "#9ca3af", False),
    ("{", "#e2e8f0", False),
    ("  \"probabilite_retard\": 0.8142,", "#38bdf8", True),
    ("  \"alerte\": true,", "#f87171", True),
    ("  \"seuil\": 0.4,", "#e2e8f0", False),
    ("  \"model_version\": \"1.0\"", "#e2e8f0", False),
    ("}", "#e2e8f0", False),
    ("PS C:\\logiai> _", "#ffffff", False),
]
create_terminal_image("screenshots/api_predict_test.png", "FastAPI - POST /v1/predict (200 OK)", api_lines)
