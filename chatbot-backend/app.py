from flask import Flask, request, jsonify
from flask_cors import CORS
from model import ChatModel

app = Flask(__name__)
CORS(app)

chatbot = ChatModel()

@app.route("/")
def home():
    return "Chatbot API running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    response = chatbot.get_response(data["message"])

    return jsonify({"response": response})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)