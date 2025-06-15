import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ---------- Flask basic ----------
app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/chat": {"origins": "*"}})

# ---------- Konfigurasi ----------
API_KEY = "AIzaSyArYniv9dh8w_iG0PxGzxrRB211HSI-gps"            # ← ambil dari ENV!
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.0-flash:generateContent?key={API_KEY}"
)
HEADERS = {"Content-Type": "application/json"}

SYSTEM_PROMPT = (
    "Kamu adalah Bewan AI untuk keluarga B1. "
    "Keluarga B1 terdiri dari Agus Susanto (Papa), Nurul Hidayati (Mama Ida), "
    "Fadhra Dzaki (anak & penciptamu), Aldan Dzaki (anak kedua), dan Azalia Dzaki (anak ketiga). "
    "Tugasmu adalah membantu seluruh keluarga B1 dengan sikap ramah dan lemah lembut."
)

# ---------- Helper ----------
def tanya_ai(pesan_user: str) -> str:
    payload = {
        "contents": [{"role": "user", "parts": [{"text": pesan_user}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
    }
    try:
        r = requests.post(GEMINI_URL, headers=HEADERS, data=json.dumps(payload), timeout=25)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# ---------- Routes ----------
@app.route("/")
@app.route("/index.html")
def index():
    # Akan mencari static/index.html
    return send_from_directory(app.static_folder, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    pesan = data.get("pesan")
    if not pesan:
        return jsonify({"error": "Field 'pesan' wajib ada"}), 400
    balasan = tanya_ai(pesan)
    return jsonify({"balasan": balasan})

# ---------- Entrypoint ----------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))            # Railway set PORT otomatis
    app.run(host="0.0.0.0", port=port, debug=False)
