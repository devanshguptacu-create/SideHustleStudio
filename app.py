from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder=None)
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/<path:filename>")
def assets(filename):
    if filename in {"style.css", "script.js"}:
        return send_from_directory(".", filename)
    return jsonify({"error": "Not found"}), 404

@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    product = (data.get("product") or "").strip()
    if len(product) < 2:
        return jsonify({"error": "Please enter a product or service name."}), 400

    platform = data.get("platform", "Instagram")
    language = data.get("language", "English")
    tone = data.get("tone", "Friendly and persuasive")
    audience = (data.get("audience") or "potential customers").strip()
    details = (data.get("details") or "").strip()
    price = (data.get("price") or "").strip()

    prompt = f"""You are SideHustle Studio, a copywriting assistant for small sellers.
Use only facts supplied by the seller. Never invent specifications, materials, certifications,
guarantees, stock, delivery promises, or product claims.

Product: {product}
Platform: {platform}
Language: {language}
Tone: {tone}
Audience: {audience}
Facts: {details or "No extra facts supplied"}
Price: {price or "Not supplied"}

Write in {language}. Use headings TITLE, DESCRIPTION, KEY BENEFITS, CALL TO ACTION, TAGS.
Make the title clear and searchable for {platform}; write a readable description; give 3-5
benefits grounded in supplied facts; add one natural call to action; and provide 8-12 relevant
comma-separated tags. Mention the price exactly only if provided. Do not make up missing facts.
"""
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=180)
        r.raise_for_status()
        result = (r.json().get("response") or "").strip()
        if not result:
            return jsonify({"error": "The model returned an empty response. Please try again."}), 502
        return jsonify({"result": result, "model": MODEL, "mode": "local"})
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Ollama is not running or is unreachable. Start Ollama and run: ollama pull qwen2.5:3b"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "The local model timed out. Try again or select a smaller model."}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": "The local AI request failed. Check that Ollama is running and the model is installed."}), 502

if __name__ == "__main__":
    app.run(debug=True)
