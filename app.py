import threading
import time
import socket

import psutil
import requests
from flask import Flask, render_template, request

# ── Innstillinger ───────────────────────────────────────────────
TEACHER_URL = "http://10.2.0.58:5000/data"     # ← IP-adressen til lærer-Pi-en
NAME = "Artem"                          # ← Ditt eget navn
SEND_INTERVAL = 30                             # Antall sekunder mellom hver sending
FORRIGE_URL = "http://10.2.0.XX:8080"   # ← Pi til forrige elev
NESTE_URL = "http://10.2.0.YY:8080"     # ← Pi til neste elev
KATALOG_URL = "http://10.2.0.58:5000"   # ← klassens katalog
# ──────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)
# Svar lagres her mens programmet kjører (tømmes ved omstart)
svar_liste = []

def get_status():
    """Henter systeminfo fra denne Pi-en og pakker det i en dict."""
    # Prøv å finne IP-adressen. Hvis det feiler, bruk teksten "unknown".
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "unknown"

    # Hvor lenge maskinen har vært på, regnet om til timer og minutter.
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    return {
        "name":     NAME,
        "hostname": socket.gethostname(),
        "ip":       ip,
        "cpu":      psutil.cpu_percent(interval=1),   # CPU-bruk i prosent
        "ram":      psutil.virtual_memory().percent,  # RAM-bruk i prosent
        "disk":     psutil.disk_usage("/").percent,   # Diskbruk i prosent
        "uptime":   f"{hours}h {minutes}m",
    }


@app.route("/")
def index():
    # Viser statussiden til eleven i nettleseren.
    return render_template(
        "status.html",
        s=get_status(),
        forrige=FORRIGE_URL,
        neste=NESTE_URL,
        katalog=KATALOG_URL,
    )

@app.route("/skjema", methods=["GET", "POST"])
def skjema():
    if request.method == "POST":
        svar = {
            "question1": request.form.get("question1"),
            "question2": request.form.get("question2"),
            "question3": request.form.get("question3"),
        }
        svar_liste.append(svar)
        return render_template("resultat.html", svar_liste=svar_liste)

    return render_template("skjema.html")

@app.route("/resultat")
def resultat():
    return render_template("resultat.html", svar_liste=svar_liste)

def send_loop():
    # Kjører hele tiden i bakgrunnen og sender status til lærer-serveren.
    while True:
        try:
            requests.post(TEACHER_URL, json=get_status(), timeout=5)
        except Exception:
            # Får vi ikke kontakt (server nede, feil IP, e.l.) hopper vi bare over
            # og prøver igjen ved neste runde.
            pass
        time.sleep(SEND_INTERVAL)


# daemon=True gjør at tråden stopper automatisk når hovedprogrammet avsluttes.
threading.Thread(target=send_loop, daemon=True).start()

if __name__ == "__main__":
    # Port 8080: åpne http://<din-ip>:8080 for å se din egen side.
    app.run(host="0.0.0.0", port=8080)
