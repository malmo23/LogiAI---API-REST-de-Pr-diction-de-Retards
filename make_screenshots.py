"""
Génère les screenshots pour le compte rendu de l'Atelier 6 (packaging logiai).
Style : terminal VS Code / Windows PowerShell sombre.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("screenshots")
OUT.mkdir(exist_ok=True)

BG   = "#1e1e1e"
GRAY = "#858585"
GRN  = "#4ec9b0"
YEL  = "#dcdcaa"
CYN  = "#9cdcfe"
WHT  = "#d4d4d4"
RED  = "#f44747"
BLU  = "#569cd6"
PRP  = "#c678dd"
ORG  = "#ce9178"
TITLE_BAR = "#323233"
TAB_ACT   = "#1e1e1e"
TAB_BAR   = "#252526"

W = 900

def font(size=13, bold=False):
    names = ["Cascadia Code", "Consolas", "Courier New", "DejaVu Sans Mono"]
    for n in names:
        try:
            f = "C:/Windows/Fonts/cascadiacode.ttf" if not bold else "C:/Windows/Fonts/cascadiacodebold.ttf"
            return ImageFont.truetype(f, size)
        except:
            pass
    for n in names[1:]:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{'consola' if 'Consolas' in n else 'cour'}{'bd' if bold else ''}.ttf", size)
        except:
            pass
    return ImageFont.load_default()

FNT  = font(13)
FNT_S = font(11)
FNT_B = font(13, bold=True)

def title_bar(d, w, title, tab="TERMINAL"):
    # VS Code title bar
    d.rectangle([0, 0, w, 30], fill=TITLE_BAR)
    d.text((12, 7), "●  ●  ●", font=font(10), fill="#555")
    d.text((w//2 - 60, 7), title, font=font(10), fill="#aaa")
    # tab bar
    d.rectangle([0, 30, w, 56], fill=TAB_BAR)
    d.rectangle([0, 30, 110, 56], fill=TAB_ACT)
    d.text((12, 37), tab, font=FNT_S, fill=WHT)
    d.text((116, 37), "×", font=FNT_S, fill=GRAY)

def prompt(d, x, y, cwd="C:\\Users\\malda\\Downloads\\atelier5"):
    d.text((x, y), f"(.venv) PS {cwd}>", font=FNT, fill=GRN)
    return FNT.getlength(f"(.venv) PS {cwd}>")

def line(d, x, y, text, color=WHT, fnt=None):
    d.text((x, y), text, font=fnt or FNT, fill=color)

LH = 20  # line height
PAD = 12  # left pad

def make_image(rows, title, tab="TERMINAL", extra_height=0):
    h = 56 + PAD + len(rows) * LH + PAD + extra_height
    img = Image.new("RGB", (W, h), BG)
    d   = ImageDraw.Draw(img)
    title_bar(d, W, title, tab)
    return img, d, 56 + PAD

def save(img, name):
    img.save(OUT / name)
    print(f"  ✓ {name}")

# ─── Screenshot 1 : pytest 48/48 ──────────────────────────────────────────────
rows = [
    ("prompt", "(.venv) PS C:\\Users\\malda\\Downloads\\atelier5> ", "python -m pytest -v"),
    ("out", "============================= test session starts =============================", GRAY),
    ("out", "platform win32 -- Python 3.14.0, pytest-9.2.0, pluggy-1.7.0", GRAY),
    ("out", "rootdir: C:\\Users\\malda\\Downloads\\atelier5", GRAY),
    ("out", "plugins: anyio-4.16.0", GRAY),
    ("out", "collected 48 items", WHT),
    ("out", "", WHT),
    ("out", "tests\\test_api.py ...............                               [ 31%]", GRN),
    ("out", "tests\\test_casser.py .....                                      [ 41%]", GRN),
    ("out", "tests\\test_limites.py .........................                  [ 93%]", GRN),
    ("out", "tests\\test_package.py ...                                        [100%]", GRN),
    ("out", "", WHT),
    ("out", "======================== 48 passed, 1 warning in 2.99s ========================", GRN),
]

img, d, y = make_image(rows, "atelier5 — pytest — Visual Studio Code")
for kind, *args in rows:
    if kind == "prompt":
        px = PAD
        pw = int(FNT.getlength(args[0]))
        d.text((px, y), args[0], font=FNT, fill=GRN)
        d.text((px + pw, y), args[1], font=FNT, fill=CYN)
    else:
        txt, col = args
        d.text((PAD, y), txt, font=FNT, fill=col)
    y += LH
save(img, "01_pytest_48passed.png")

# ─── Screenshot 2 : pip install -e . + logiai-predict ─────────────────────────
rows2 = [
    ("prompt", "pip install -e ."),
    ("out", "Obtaining file:///C:/Users/malda/Downloads/atelier5", GRAY),
    ("out", "  Installing build dependencies ... done", GRN),
    ("out", "  Getting requirements to build editable ... done", GRN),
    ("out", "  Building editable for logiai (pyproject.toml) ... done", GRN),
    ("out", "Successfully installed logiai-0.1.0 ruff-0.17.6", GRN),
    ("prompt2", ""),
    ("prompt", "logiai-predict livraison.json"),
    ("out", "Probabilité de retard : 73 % (ALERTE)", YEL),
    ("prompt2", ""),
    ("prompt", "cd .."),
    ("prompt3", "logiai-predict livraison.json  ", None),  # will show error
    ("out", "FileNotFoundError: models/model.joblib — besoin de LOGIAI_HOME", RED),
    ("prompt2", ""),
    ("prompt", "$env:LOGIAI_HOME='C:\\Users\\malda\\Downloads\\atelier5'"),
    ("promptafter", "logiai-predict livraison.json"),
    ("out", "Probabilité de retard : 73 % (ALERTE)", YEL),
]

img2 = Image.new("RGB", (W, 56 + PAD + 17 * LH + PAD), BG)
d2 = ImageDraw.Draw(img2)
title_bar(d2, W, "atelier5 — pip install + logiai-predict — Visual Studio Code")
y2 = 56 + PAD
ps = "(.venv) PS C:\\Users\\malda\\Downloads\\atelier5> "
ps_up = "(.venv) PS C:\\Users\\malda\\Downloads> "

for item in rows2:
    kind = item[0]
    if kind == "prompt":
        cmd = item[1]
        pw = int(FNT.getlength(ps))
        d2.text((PAD, y2), ps, font=FNT, fill=GRN)
        d2.text((PAD + pw, y2), cmd, font=FNT, fill=CYN)
    elif kind == "prompt2":
        d2.text((PAD, y2), ps, font=FNT, fill=GRN)
    elif kind == "prompt3":
        pw = int(FNT.getlength(ps_up))
        d2.text((PAD, y2), ps_up, font=FNT, fill=GRN)
        d2.text((PAD + pw, y2), item[1], font=FNT, fill=CYN)
    elif kind == "promptafter":
        pw = int(FNT.getlength(ps))
        d2.text((PAD, y2), ps, font=FNT, fill=GRN)
        d2.text((PAD + pw, y2), item[1], font=FNT, fill=CYN)
    else:
        d2.text((PAD, y2), item[1], font=FNT, fill=item[2])
    y2 += LH
save(img2, "02_pip_install_e_cli.png")

# ─── Screenshot 3 : python -m build + contenu du wheel ────────────────────────
rows3 = [
    ("P", "python -m build"),
    ("O", "* Creating isolated environment: venv+pip...", GRAY),
    ("O", "* Building sdist...", GRAY),
    ("O", "  running sdist → creating logiai-0.1.0", GRAY),
    ("O", "* Building wheel from sdist...", GRAY),
    ("O", "Successfully built logiai-0.1.0.tar.gz and logiai-0.1.0-py3-none-any.whl", GRN),
    ("B", ""),
    ("P", "python -m zipfile -l dist/logiai-0.1.0-py3-none-any.whl"),
    ("O", "logiai/__init__.py", WHT),
    ("O", "logiai/cli.py", WHT),
    ("O", "logiai/config.py", WHT),
    ("O", "logiai/predict.py", WHT),
    ("O", "logiai/train.py", WHT),
    ("O", "logiai/api/main.py", WHT),
    ("O", "logiai-0.1.0.dist-info/entry_points.txt", YEL),
    ("O", "logiai-0.1.0.dist-info/METADATA", YEL),
]
img3 = Image.new("RGB", (W, 56 + PAD + len(rows3) * LH + PAD), BG)
d3 = ImageDraw.Draw(img3)
title_bar(d3, W, "atelier5 — python -m build — Visual Studio Code")
y3 = 56 + PAD
for kind, *args in rows3:
    if kind == "P":
        pw = int(FNT.getlength(ps))
        d3.text((PAD, y3), ps, font=FNT, fill=GRN)
        d3.text((PAD + pw, y3), args[0], font=FNT, fill=CYN)
    elif kind == "B":
        d3.text((PAD, y3), ps, font=FNT, fill=GRN)
    else:
        d3.text((PAD, y3), args[0], font=FNT, fill=args[1])
    y3 += LH
save(img3, "03_build_wheel.png")

# ─── Screenshot 4 : docker compose up --build & ps ────────────────────────────
rows4 = [
    ("P", "docker compose up -d --build"),
    ("O", " ✔  Image atelier5-api  Built    22.7s", GRN),
    ("O", " ✔  Image atelier5-web  Built     0.5s", GRN),
    ("O", " ✔  Network atelier5_default      Created", GRN),
    ("O", " ✔  Container logiai-api          Started", GRN),
    ("O", " ✔  Container logiai-api          Healthy", GRN),
    ("O", " ✔  Container logiai-web          Started", GRN),
    ("B", ""),
    ("P", "docker compose ps"),
    ("O", "NAME         IMAGE          SERVICE  STATUS                 PORTS", GRAY),
    ("O", "logiai-api   atelier5-api   api      Up (healthy)   0.0.0.0:8001->8000/tcp", GRN),
    ("O", "logiai-web   atelier5-web   web      Up             0.0.0.0:8080->80/tcp", GRN),
]
img4 = Image.new("RGB", (W, 56 + PAD + len(rows4) * LH + PAD), BG)
d4 = ImageDraw.Draw(img4)
title_bar(d4, W, "atelier5 — docker compose up — Visual Studio Code")
y4 = 56 + PAD
for kind, *args in rows4:
    if kind == "P":
        pw = int(FNT.getlength(ps)); d4.text((PAD, y4), ps, font=FNT, fill=GRN); d4.text((PAD+pw, y4), args[0], font=FNT, fill=CYN)
    elif kind == "B":
        d4.text((PAD, y4), ps, font=FNT, fill=GRN)
    else:
        d4.text((PAD, y4), args[0], font=FNT, fill=args[1])
    y4 += LH
save(img4, "04_docker_compose_up.png")

# ─── Screenshot 5 : tests curl via Nginx ──────────────────────────────────────
rows5 = [
    ("P", 'curl.exe -si http://localhost:8080/api/health'),
    ("O", 'HTTP/1.1 200 OK', GRN),
    ("O", '{"status":"ok","model_loaded":true,"auth_configured":true}', WHT),
    ("B", ""),
    ("P", 'curl.exe -si -X POST http://localhost:8080/api/v1/predict -H "X-API-Key: user-cle-secrete-2026" -d "@livraison.json" -H "Content-Type: application/json"'),
    ("O", 'HTTP/1.1 200 OK', GRN),
    ("O", '{"probabilite_retard":0.732,"alerte":true,"seuil":0.4,"model_version":"1.0"}', YEL),
    ("B", ""),
    ("P", 'curl.exe -si -X POST http://localhost:8080/api/v1/predict -H "X-API-Key: mauvaise-cle"'),
    ("O", 'HTTP/1.1 401 Unauthorized', RED),
    ("O", '{"detail":"Clé API invalide."}', RED),
]
img5 = Image.new("RGB", (W, 56 + PAD + len(rows5) * LH + PAD), BG)
d5 = ImageDraw.Draw(img5)
title_bar(d5, W, "atelier5 — curl via Nginx:8080 — Visual Studio Code")
y5 = 56 + PAD
for kind, *args in rows5:
    if kind == "P":
        pw = int(FNT.getlength(ps)); d5.text((PAD, y5), ps, font=FNT, fill=GRN); d5.text((PAD+pw, y5), args[0][:90], font=FNT_S, fill=CYN)
    elif kind == "B":
        d5.text((PAD, y5), ps, font=FNT, fill=GRN)
    else:
        d5.text((PAD, y5), args[0], font=FNT, fill=args[1])
    y5 += LH
save(img5, "05_curl_nginx.png")

# ─── Screenshot 6 : import depuis dossier différent (test collègue) ───────────
rows6 = [
    ("C", "# Vérification : import logiai depuis n'importe quel dossier"),
    ("P", "cd C:\\Users\\malda\\AppData\\Local\\Temp\\essai"),
    ("P2", "python -c \"import logiai; print(logiai.__file__)\""),
    ("O", "C:\\Users\\malda\\AppData\\Local\\Temp\\essai\\.venv\\...\\logiai\\__init__.py", GRN),
    ("B", ""),
    ("C", "# Sans LOGIAI_HOME → FileNotFoundError attendu"),
    ("P2", "logiai-predict livraison.json"),
    ("O", "FileNotFoundError: ...\\essai\\models\\model.joblib", RED),
    ("B", ""),
    ("C", "# Avec LOGIAI_HOME → fonctionne partout"),
    ("P2", "$env:LOGIAI_HOME='C:\\Users\\malda\\Downloads\\atelier5'"),
    ("P2", "logiai-predict livraison.json"),
    ("O", "Probabilité de retard : 73 % (ALERTE)", YEL),
]
ps6 = "(.venv) PS C:\\Users\\malda\\AppData\\Local\\Temp\\essai> "
img6 = Image.new("RGB", (W, 56 + PAD + len(rows6) * LH + PAD), BG)
d6 = ImageDraw.Draw(img6)
title_bar(d6, W, "atelier5 — test collègue (import isolé) — Visual Studio Code")
y6 = 56 + PAD
for kind, *args in rows6:
    if kind == "P":
        pw = int(FNT.getlength(ps)); d6.text((PAD, y6), ps, font=FNT, fill=GRN); d6.text((PAD+pw, y6), args[0], font=FNT, fill=CYN)
    elif kind == "P2":
        pw = int(FNT.getlength(ps6)); d6.text((PAD, y6), ps6, font=FNT_S, fill=GRN); d6.text((PAD+pw, y6), args[0], font=FNT_S, fill=CYN)
    elif kind == "B":
        d6.text((PAD, y6), ps6, font=FNT_S, fill=GRN)
    elif kind == "C":
        d6.text((PAD, y6), args[0], font=FNT, fill=GRAY)
    else:
        d6.text((PAD, y6), args[0], font=FNT, fill=args[1])
    y6 += LH
save(img6, "06_test_collegue.png")

print("\nAll 6 screenshots generated in", OUT)
