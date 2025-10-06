from flask import Flask, render_template, request, jsonify
import json, random, os

app = Flask(__name__)

# Load intents
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

# Ensure feedback file exists
if not os.path.exists("feedback.json"):
    with open("feedback.json", "w") as f:
        json.dump({"feedback": []}, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_message = request.form["message"].lower()

    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern in user_message:
                response = random.choice(intent["responses"])
                return jsonify({"response": response})

    return jsonify({"response": "🤖 I'm sorry, I didn’t understand that. Could you please rephrase?"})

@app.route("/feedback", methods=["POST"])
def feedback():
    rating = request.form["rating"]
    with open("feedback.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["feedback"].append(int(rating))
        f.seek(0)
        json.dump(data, f, indent=2)
    return jsonify({"message": f"Thanks for rating us {rating}/5! 🙏"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
