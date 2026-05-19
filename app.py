from flask import Flask, request, jsonify
from model import ChatModel

app = Flask(__name__)
chatbot = ChatModel()

@app.route("/")
def home():
    return "Chatbot API is running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    response = chatbot.get_response(user_message)

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)