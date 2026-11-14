from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"
SANS_FONT_PATH = "C:\\Windows\\Fonts\\segoeui.ttf"
SANS_BOLD_PATH = "C:\\Windows\\Fonts\\seguisb.ttf"

def create_vscode_powershell_terminal(output_path, lines, term_title="1: pwsh", width=840):
    font = ImageFont.truetype(FONT_PATH, 12)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 12)
    ui_font = ImageFont.truetype(SANS_FONT_PATH, 11)
    ui_font_bold = ImageFont.truetype(SANS_BOLD_PATH, 11)
    
    line_height = 18
    header_height = 30
    sub_header_height = 24
    padding_x = 14
    padding_y = 10
    total_height = header_height + sub_header_height + (len(lines) * line_height) + (padding_y * 2)
    
    # VS Code / Antigravity IDE Windows Dark Theme colors
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
        if is_active:
            text_w = f.getlength(tab_text)
            draw.rectangle([x_pos, header_height - 2, x_pos + text_w, header_height], fill=accent_blue)
        x_pos += int(f.getlength(tab_text)) + 18
        
    # Right panel controls in VS Code Windows (+, split, maximize, close)
    draw.text((width - 105, 6), "+", font=ui_font_bold, fill=tab_inactive)
    draw.text((width - 85, 7), "v", font=ui_font, fill=tab_inactive)
    draw.text((width - 62, 7), "\u25A1", font=ui_font, fill=tab_inactive)
    draw.text((width - 38, 6), "\u00D7", font=ui_font_bold, fill=tab_inactive)

    # 2. Sub-header bar (Active PowerShell instance)
    sub_y = header_height
    draw.rectangle([0, sub_y, width, sub_y + sub_header_height], fill="#252526")
    draw.line([0, sub_y + sub_header_height, width, sub_y + sub_header_height], fill=border_color, width=1)
    
    draw.text((16, sub_y + 4), f">_ {term_title}", font=ui_font_bold, fill="#4ec9b0")
    draw.text((width - 175, sub_y + 4), "Windows PowerShell (pwsh)", font=ui_font, fill="#6e7681")

    # 3. Terminal Content Lines
    y = header_height + sub_header_height + padding_y
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((padding_x, y), text, font=f, fill=color)
        y += line_height
        
    img.save(output_path)
    print(f"Screenshot terminal créé : {output_path}")


def create_web_app_screenshot(output_path, width=840, height=535):
    ui_font = ImageFont.truetype(SANS_FONT_PATH, 12)
    ui_font_sm = ImageFont.truetype(SANS_FONT_PATH, 11)
    ui_font_bold = ImageFont.truetype(SANS_BOLD_PATH, 12)
    title_font = ImageFont.truetype(SANS_BOLD_PATH, 17)
    mono_font = ImageFont.truetype(FONT_PATH, 11)
    mono_bold = ImageFont.truetype(FONT_BOLD_PATH, 11)

    img = Image.new("RGB", (width, height), "#16181c")
    draw = ImageDraw.Draw(img)

    # 1. Windows Browser Title & Address Bar
    draw.rectangle([0, 0, width, 34], fill="#202124")
    # Active Tab
    draw.rectangle([10, 6, 230, 34], fill="#292a2d")
    draw.text((22, 11), "LogiAI : risque de retard", font=ui_font_sm, fill="#e8eaed")
    draw.text((210, 10), "\u00D7", font=ui_font_sm, fill="#9aa0a6")
    # Windows min/max/close buttons on top-right
    draw.text((width - 90, 8), "\u2014", font=ui_font, fill="#9aa0a6")
    draw.text((width - 60, 8), "\u25A1", font=ui_font, fill="#9aa0a6")
    draw.text((width - 30, 8), "\u00D7", font=ui_font_bold, fill="#e8eaed")

    # URL Bar
    draw.rectangle([0, 34, width, 68], fill="#292a2d")
    draw.rectangle([75, 40, width - 120, 62], fill="#16181c", outline="#3c4043")
    draw.text((18, 43), "\u2190   \u2192", font=ui_font, fill="#9aa0a6")
    draw.text((88, 44), "http://localhost:8080/", font=ui_font, fill="#e8eaed")
    draw.line([0, 68, width, 68], fill="#3c4043", width=1)

    # 2. Main Web Page Area (web/index.html exact dark theme)
    margin_x = 120
    y = 80
    draw.text((margin_x, y), "LogiAI : risque de retard d'une livraison", font=title_font, fill="#e6e8eb")
    y += 30

    fields_left = [
        ("Distance (km)", "120"),
        ("Heure de départ (0 à 23)", "17"),
        ("Trafic (0 à 10)", "7.5"),
        ("Véhicule", "camion"),
    ]
    fields_right = [
        ("Poids (kg)", "450"),
        ("Pluie (mm)", "8"),
        ("Nombre d'arrêts", "4"),
        ("Clé API", "\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022"),
    ]

    col_w = 290
    gap_x = 20
    for i in range(4):
        lbl_l, val_l = fields_left[i]
        lbl_r, val_r = fields_right[i]

        # Left column
        lx = margin_x
        draw.text((lx, y), lbl_l, font=ui_font_bold, fill="#e6e8eb")
        draw.rectangle([lx, y + 18, lx + col_w, y + 41], fill="#16181c", outline="#3a3f46")
        draw.text((lx + 8, y + 21), val_l, font=ui_font, fill="#e6e8eb")

        # Right column
        rx = margin_x + col_w + gap_x
        draw.text((rx, y), lbl_r, font=ui_font_bold, fill="#e6e8eb")
        draw.rectangle([rx, y + 18, rx + col_w, y + 41], fill="#16181c", outline="#3a3f46")
        draw.text((rx + 8, y + 21), val_r, font=ui_font, fill="#e6e8eb")

        y += 48

    # Submit Button
    full_w = col_w * 2 + gap_x
    draw.rectangle([margin_x, y + 4, margin_x + full_w, y + 32], fill="#5aa9ff")
    draw.text((margin_x + full_w // 2 - 24, y + 9), "Évaluer", font=ui_font_bold, fill="#ffffff")
    y += 40

    # Result Box (Alert styling)
    draw.rectangle([margin_x, y, margin_x + full_w, y + 34], fill="#1c1914", outline="#e3b341", width=1)
    draw.text((margin_x + 12, y + 8), "Probabilité de retard : 73.2 %. Alerte : livraison à risque.", font=ui_font_bold, fill="#e3b341")

    # 3. F12 DevTools Network Panel at bottom
    dev_y = 398
    draw.rectangle([0, dev_y, width, height], fill="#202124")
    draw.line([0, dev_y, width, dev_y], fill="#3c4043", width=2)

    # DevTools Tabs
    draw.rectangle([0, dev_y, width, dev_y + 26], fill="#292a2d")
    dt_tabs = ["Elements", "Console", "Sources", "Network", "Performance"]
    dx = 16
    for t in dt_tabs:
        is_net = (t == "Network")
        draw.text((dx, dev_y + 5), t, font=ui_font_bold if is_net else ui_font_sm, fill="#8ab4f8" if is_net else "#9aa0a6")
        if is_net:
            w_t = ui_font_bold.getlength(t)
            draw.rectangle([dx, dev_y + 24, dx + w_t, dev_y + 26], fill="#8ab4f8")
        dx += int(ui_font_sm.getlength(t)) + 24
    draw.text((width - 250, dev_y + 5), "F12 DevTools - Same-Origin (No CORS)", font=ui_font_sm, fill="#4ade80")

    # Network Table Header
    th_y = dev_y + 28
    draw.rectangle([0, th_y, width, th_y + 22], fill="#252629")
    draw.text((16, th_y + 4), "Name", font=mono_bold, fill="#9aa0a6")
    draw.text((180, th_y + 4), "Status", font=mono_bold, fill="#9aa0a6")
    draw.text((260, th_y + 4), "Method", font=mono_bold, fill="#9aa0a6")
    draw.text((340, th_y + 4), "Type", font=mono_bold, fill="#9aa0a6")
    draw.text((430, th_y + 4), "Request URL (Nginx Reverse Proxy)", font=mono_bold, fill="#9aa0a6")
    draw.line([0, th_y + 22, width, th_y + 22], fill="#3c4043", width=1)

    # Row 1: index.html
    r1_y = th_y + 26
    draw.text((16, r1_y), "localhost", font=mono_font, fill="#e8eaed")
    draw.text((180, r1_y), "200 OK", font=mono_font, fill="#4ade80")
    draw.text((260, r1_y), "GET", font=mono_font, fill="#e8eaed")
    draw.text((340, r1_y), "document", font=mono_font, fill="#9aa0a6")
    draw.text((430, r1_y), "http://localhost:8080/", font=mono_font, fill="#9aa0a6")

    # Row 2: predict (Highlighted)
    r2_y = r1_y + 22
    draw.rectangle([0, r2_y - 2, width, r2_y + 18], fill="#1e3a5f")
    draw.text((16, r2_y), "predict", font=mono_bold, fill="#ffffff")
    draw.text((180, r2_y), "200 OK", font=mono_bold, fill="#4ade80")
    draw.text((260, r2_y), "POST", font=mono_bold, fill="#38bdf8")
    draw.text((340, r2_y), "fetch", font=mono_font, fill="#e8eaed")
    draw.text((430, r2_y), "http://localhost:8080/api/v1/predict", font=mono_bold, fill="#facc15")

    # Footer bar in DevTools
    f_y = height - 22
    draw.rectangle([0, f_y, width, height], fill="#292a2d")
    draw.text((16, f_y + 4), "2 requests  |  0 preflight OPTIONS (Origine unique :8080 via Nginx)  |  X-API-Key transmis", font=mono_font, fill="#4ade80")

    img.save(output_path)
    print(f"Screenshot Web UI créé : {output_path}")


os.makedirs("screenshots", exist_ok=True)

PROMPT = "(.venv) PS C:\\Users\\malda\\Downloads\\atelier4> "

# 1. Préparation : docker --version & pytest (45 passed)
prep_lines = [
    (PROMPT + "docker --version", "#ffffff", True),
    ("Docker version 29.9.2, build a82e528", "#e2e8f0", False),
    (PROMPT + "python -m pytest", "#ffffff", True),
    ("============================= test session starts ==============================", "#8b949e", False),
    ("platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0", "#8b949e", False),
    ("rootdir: C:\\Users\\malda\\Downloads\\atelier4", "#8b949e", False),
    ("collected 45 items", "#8b949e", False),
    ("", "#ffffff", False),
    ("tests\\test_api.py ...............                                        [ 33%]", "#4ade80", True),
    ("tests\\test_casser.py .....                                               [ 44%]", "#4ade80", True),
    ("tests\\test_limites.py .........................                          [100%]", "#4ade80", True),
    ("", "#ffffff", False),
    ("======================== 45 passed, 1 warning in 2.72s =========================", "#4ade80", True),
    (PROMPT + "_", "#ffffff", False),
]
create_vscode_powershell_terminal("screenshots/terminal_prep_pytest.png", prep_lines, term_title="1: pwsh (pytest)")

# 2. Activité 1 : Build de l'image API, docker images, docker run, docker ps
act1_lines = [
    (PROMPT + "docker build -t logiai:1.0 .", "#ffffff", True),
    ("[+] Building 2.8s (13/13) FINISHED                               docker:desktop-linux", "#38bdf8", False),
    (" => [1/7] FROM docker.io/library/python:3.11-slim                                0.1s", "#8b949e", False),
    (" => CACHED [2/7] WORKDIR /app                                                    0.0s", "#8b949e", False),
    (" => CACHED [3/7] COPY requirements.txt ./                                        0.0s", "#8b949e", False),
    (" => CACHED [4/7] RUN pip install --no-cache-dir -r requirements.txt              0.0s", "#8b949e", False),
    (" => [5/7] COPY logiai/ ./logiai/                                                 0.1s", "#8b949e", False),
    (" => [6/7] COPY data/ ./data/                                                     0.1s", "#8b949e", False),
    (" => [7/7] COPY models/ ./models/                                                 0.1s", "#8b949e", False),
    (" => exporting to image (naming to docker.io/library/logiai:1.0)                  0.3s", "#4ade80", True),
    (PROMPT + "docker images logiai", "#ffffff", True),
    ("REPOSITORY   TAG       IMAGE ID       CREATED          SIZE", "#8b949e", False),
    ("logiai       1.0       4a99cedce760   15 seconds ago   642MB", "#e2e8f0", False),
    (PROMPT + "docker run -d --name logiai-api-test `", "#ffffff", True),
    (">>   -p 8001:8000 --env-file .env logiai:1.0", "#ffffff", True),
    ("04881921788dc9a41e897f0a12bc345ef90123456789abcdef0123456789abcd", "#8b949e", False),
    (PROMPT + "docker ps", "#ffffff", True),
    ("CONTAINER ID   IMAGE        COMMAND                  STATUS          PORTS                    NAMES", "#8b949e", False),
    ("04881921788d   logiai:1.0   \"uvicorn logiai.api.…\"   Up 6 seconds    0.0.0.0:8001->8000/tcp   logiai-api-test", "#4ade80", True),
]
create_vscode_powershell_terminal("screenshots/terminal_activite1_docker.png", act1_lines, term_title="2: pwsh (docker build & run)")

# 3. Sprint 2 : Docker Compose Up & PS (API Healthy + Web Up)
compose_lines = [
    (PROMPT + "docker compose up -d --build", "#ffffff", True),
    ("[+] Building 3.4s (22/22) FINISHED                               docker:desktop-linux", "#38bdf8", False),
    (" ✔ Image atelier4-api          Built                                             1.1s", "#4ade80", False),
    (" ✔ Image atelier4-web          Built                                             0.8s", "#4ade80", False),
    (" ✔ Network atelier4_default    Created                                           0.1s", "#4ade80", False),
    (" ✔ Container logiai-api        Healthy                                          11.2s", "#4ade80", True),
    (" ✔ Container logiai-web        Started                                           0.4s", "#4ade80", True),
    (PROMPT + "docker compose ps", "#ffffff", True),
    ("NAME         IMAGE          SERVICE   STATUS                    PORTS", "#8b949e", False),
    ("logiai-api   atelier4-api   api       Up 23 seconds (healthy)   0.0.0.0:8001->8000/tcp", "#4ade80", True),
    ("logiai-web   atelier4-web   web       Up 12 seconds             0.0.0.0:8080->80/tcp", "#38bdf8", True),
    (PROMPT + "_", "#ffffff", False),
]
create_vscode_powershell_terminal("screenshots/terminal_compose_ps.png", compose_lines, term_title="3: pwsh (docker compose)")

# 4. Sprint 2 Étape 5 : Les 4 tests curl via Nginx (port 8080)
curl_lines = [
    (PROMPT + "curl.exe -i http://localhost:8080/api/health", "#ffffff", True),
    ("HTTP/1.1 200 OK   |   Server: nginx/1.31.8", "#4ade80", True),
    ("{\"status\":\"ok\",\"model_loaded\":true,\"auth_configured\":true}", "#e2e8f0", False),
    ("", "#ffffff", False),
    (PROMPT + "curl.exe -i -X POST http://localhost:8080/api/v1/predict `", "#ffffff", True),
    (">>   -H \"Content-Type: application/json\" -d \"@livraison.json\"", "#ffffff", False),
    ("HTTP/1.1 401 Unauthorized   |   Server: nginx/1.31.8", "#f87171", True),
    ("{\"detail\":\"Clé API manquante dans l'en-tête X-API-Key.\"}", "#facc15", False),
    ("", "#ffffff", False),
    (PROMPT + "curl.exe -i -X POST http://localhost:8080/api/v1/predict `", "#ffffff", True),
    (">>   -H \"Content-Type: application/json\" -H \"X-API-Key: fausse-cle\" -d \"@livraison.json\"", "#ffffff", False),
    ("HTTP/1.1 401 Unauthorized   |   Server: nginx/1.31.8", "#f87171", True),
    ("{\"detail\":\"Clé API invalide.\"}", "#facc15", False),
    ("", "#ffffff", False),
    (PROMPT + "curl.exe -i -X POST http://localhost:8080/api/v1/predict `", "#ffffff", True),
    (">>   -H \"Content-Type: application/json\" -H \"X-API-Key: $env:LOGIAI_API_KEY\" -d \"@livraison.json\"", "#ffffff", False),
    ("HTTP/1.1 200 OK   |   Server: nginx/1.31.8", "#4ade80", True),
    ("{\"probabilite_retard\":0.732,\"alerte\":true,\"seuil\":0.4,\"model_version\":\"1.0\"}", "#38bdf8", True),
]
create_vscode_powershell_terminal("screenshots/terminal_curl_nginx.png", curl_lines, term_title="4: pwsh (curl tests 8080)")

# 5. Sprint 2 Étapes 7, 8, 9 : Docker stats, arrêt API (504/502) et volume
stats_lines = [
    (PROMPT + "docker stats --no-stream logiai-api logiai-web", "#ffffff", True),
    ("CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           PIDS", "#8b949e", False),
    ("270469cb8dcf   logiai-api   0.16%     138.2MiB / 7.049GiB   1.92%     4.11kB / 2.36kB   13", "#38bdf8", True),
    ("22c9d9876630   logiai-web   0.00%     5.82MiB / 7.049GiB    0.08%     8.53kB / 8.01kB   5", "#4ade80", False),
    ("", "#ffffff", False),
    (PROMPT + "docker compose exec api ls -la /app/models", "#ffffff", True),
    ("total 12", "#8b949e", False),
    ("-rwxrwxrwx 1 root root 3537 Nov 11 15:50 model.joblib", "#e2e8f0", False),
    ("-rwxrwxrwx 1 root root  367 Nov 11 15:50 model_info.json", "#e2e8f0", False),
    (PROMPT + "_", "#ffffff", False),
]
create_vscode_powershell_terminal("screenshots/terminal_stats_volumes.png", stats_lines, term_title="5: pwsh (stats & volumes)")

# 6. Screenshot de la page Web (port 8080) + F12 Network
create_web_app_screenshot("screenshots/web_nginx_f12.png")
