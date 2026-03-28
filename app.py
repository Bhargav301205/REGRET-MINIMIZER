from flask import Flask, request, jsonify
from flask_cors import CORS
from main import classify_input, extract_features, calculate_score, decision_text, explain

app = Flask(__name__)
CORS(app)   # ✅ FIX FOR FRONTEND CONNECTION

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_input = data.get("input", "")

    intent = classify_input(user_input)

    # 🔒 Guard layer
    if intent == "invalid":
        return jsonify({"reply": "🤖 Tell me a proper decision."})

    if intent == "critical":
        return jsonify({"reply": "⚠️ This seems serious. Talk to someone you trust."})

    if intent == "harmful":
        return jsonify({"reply": "⚠️ I can't support harming others."})

    # 🤖 AI logic
    features = extract_features(user_input)

    if features is None:
        return jsonify({"reply": "⚠️ Could not analyze properly."})

    score = calculate_score(features)
    dec, msg = decision_text(score)
    exp = explain(features)

    return jsonify({
        "reply": f"{dec} (Score: {round(score,2)})\n{msg}\n{exp}"
    })


# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(port=3000, debug=True)