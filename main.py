import random

# ===== SAFE INPUT =====
def safe_input(prompt, default=""):
    try:
        return input(prompt)
    except:
        return default


# ===== GUARD LAYER =====
def classify_input(text):
    text = text.lower().strip()

    if any(p in text for p in ["kill me", "suicide", "end my life", "want to die"]):
        return "critical"

    if any(p in text for p in ["kill someone", "hurt someone", "attack"]):
        return "harmful"

    if text in ["hi", "hello", "hey", "test"]:
        return "invalid"

    return "valid"


def handle_invalid():
    return "Tell me what decision you're trying to make."


def handle_critical():
    return "This seems serious. Please talk to someone you trust."


def handle_harmful():
    return "I can't support harming others."


# ===== HYBRID AI LOGIC (FIXED) =====
def extract_features(user_input):
    text = user_input.lower()

    importance = 0.5
    emotion = 0.5
    risk = 0.5
    impact = "medium"

    # ===== HANDLE CONFLICT (KEY FIX) =====
    if "but" in text:
        parts = text.split("but")

        action_part = parts[0]            # what user wants
        responsibility_part = parts[1]    # real duty

        # ===== RESPONSIBILITY =====
        if any(word in responsibility_part for word in ["exam", "study", "career", "future"]):
            importance += 0.5
            impact = "high"

        # ===== ACTION (RISKY BEHAVIOR) =====
        if any(word in action_part for word in ["play", "cricket", "game", "movie", "scroll"]):
            risk += 0.5   # 🔥 penalize doing this action

    else:
        # ===== NORMAL CASE =====
        if any(word in text for word in ["exam", "study", "career", "future"]):
            importance += 0.3
            impact = "high"

        if any(word in text for word in ["play", "cricket", "game"]):
            emotion += 0.2

        if any(word in text for word in ["risk", "danger", "loss", "money"]):
            risk += 0.3

    # ===== NORMALIZE =====
    importance = min(1, max(0, importance))
    emotion = min(1, max(0, emotion))
    risk = min(1, max(0, risk))

    return {
        "importance": importance,
        "emotion": emotion,
        "risk": risk,
        "impact": impact
    }


# ===== DECISION ENGINE (FIXED) =====
def calculate_score(d):
    impact_map = {"low": 1, "medium": 2, "high": 3}

    score = (
        d["importance"] * 20 +
        impact_map[d["impact"]] * 20 +
        d["emotion"] * 10 -
        d["risk"] * 50   # 🔥 strong penalty for bad action
    )

    return max(0, min(score, 100))


# ===== RESPONSE =====
def decision_text(score):
    if score < 30:
        return "LOW REGRET", random.choice([
            "You probably won’t regret doing this.",
            "This doesn’t seem like a bad choice."
        ])

    elif score < 60:
        return "UNCERTAIN", random.choice([
            "This could go either way.",
            "Think carefully before deciding."
        ])

    else:
        return "HIGH REGRET", random.choice([
            "You might regret doing this.",
            "This decision could negatively affect you."
        ])


def explain(d):
    reasons = []

    if d["importance"] > 0.7:
        reasons.append("it is very important")

    if d["impact"] == "high":
        reasons.append("it affects your future")

    if d["risk"] > 0.6:
        reasons.append("there is high risk in doing this")

    if d["emotion"] > 0.7:
        reasons.append("it feels emotionally appealing")

    if not reasons:
        reasons.append("there are no strong factors")

    return "This is because " + ", ".join(reasons) + "."


# ===== MAIN PROCESS FUNCTION =====
def process_decision(user_input):

    intent = classify_input(user_input)

    if intent == "invalid":
        return handle_invalid()

    if intent == "critical":
        return handle_critical()

    if intent == "harmful":
        return handle_harmful()

    data = extract_features(user_input)

    score = calculate_score(data)
    dec, msg = decision_text(score)
    exp = explain(data)

    return f"{dec} (Score: {round(score,2)})\n{msg}\n{exp}"


# ===== CLI RUN =====
if __name__ == "__main__":
    print("🧠 HYBRID REGRET AI\n")

    user_input = safe_input("👉 Describe your situation:\n", "test")

    result = process_decision(user_input)

    print("\n📊 RESULT")
    print(result)