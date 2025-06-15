from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)

# Konfigurasi CORS yang lebih eksplisit
CORS(app, resources={
    r"/chat": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

API_KEY = "AIzaSyArYniv9dh8w_iG0PxGzxrRB211HSI-gps"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

HEADERS = {
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = (
    "Kamu adalah Bewan AI untuk keluarga B1. "
    "Keluarga B1 terdiri dari Agus Susanto (Papa), Nurul Hidayati (Mama Ida), "
    "Fadhra Dzaki (anak & penciptamu), Aldan Dzaki (anak kedua), dan Azalia Dzaki (anak ketiga). "
    "Tugasmu adalah membantu seluruh keluarga B1 dengan sikap ramah dan lemah lembut."
)

def tanya_ai(pesan_user):
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": pesan_user}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        }
    }

    response = requests.post(GEMINI_URL, headers=HEADERS, data=json.dumps(payload))
    result = response.json()
    
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "Terjadi kesalahan:\n" + json.dumps(result, indent=2)

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        # Handle preflight request
        response = jsonify({"status": "success"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    data = request.get_json()
    if not data or "pesan" not in data:
        return jsonify({"error": "Request harus berisi field 'pesan'"}), 400

    pesan_user = data["pesan"]
    jawaban = tanya_ai(pesan_user)

    response = jsonify({"balasan": jawaban})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)
