import os
from flask import Flask, request, jsonify
app = Flask(__name__)
AI_API_URL = os.getenv("AI_API_URL", "").strip()
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_MODEL = os.getenv("AI_MODEL", "").strip()

@app.get("/")
def home(): return "Isaac IA 🔵 ON - 24/24"

@app.get("/config")
def config(): return jsonify({"on": request.args.get("on", "1") == "1", "pers": request.args.get("pers", "50")})

@app.post("/cerveau")
def cerveau():
    data = request.get_json(silent=True) or {}
    msg = str(data.get("msg", "")).strip()
    if not msg: return jsonify({"error": "Le message est vide."}), 400
    t = msg.casefold()
    if any(w in t for w in ["salut", "cc", "bjr", "bonjour", "yo", "wesh"]): return jsonify({"reply": "Salut 💙 ! Comment ça va ?"})
    if any(w in t for w in ["qui t'a créé", "qui ta créé", "qui t'a cree", "qui t a cree", "qui t’a créé"]): return jsonify({"reply": "C’est Isaac Newton qui m’a créé."})
    if not (AI_API_URL and AI_API_KEY and AI_MODEL): return jsonify({"error": "Le serveur est actif mais le fournisseur IA n'est pas configuré. Définis AI_API_URL, AI_API_KEY et AI_MODEL sur l'hébergeur."}), 503
    try:
        import requests
        r=requests.post(AI_API_URL,headers={"Authorization":f"Bearer {AI_API_KEY}","Content-Type":"application/json"},json={"model":AI_MODEL,"messages":[{"role":"system","content":"Tu es Isaac IA, un assistant qui répond en français de façon claire et respectueuse."},{"role":"user","content":msg}]},timeout=45)
        r.raise_for_status(); return jsonify({"reply":r.json()["choices"][0]["message"]["content"]})
    except Exception:
        app.logger.exception("Erreur service IA"); return jsonify({"error":"Service IA indisponible ou mal configuré."}),502
if __name__ == "__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")))
