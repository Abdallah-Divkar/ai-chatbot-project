import os
from flask import Flask, request, jsonify,Response, stream_with_context
from model import ChatModel
from memory import get_history, save_history

app = Flask(__name__)
chatbot = ChatModel()


@app.route("/")
def home():
    return "Chatbot API is running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "message required"}), 400
    if len(user_message) > 1000:
        return jsonify({"error": "message too long"}), 400
    session_id = data.get("session_id") or request.remote_addr

    history = get_history(session_id)
    response, updated_history = chatbot.get_response(user_message, history)
    save_history(session_id, updated_history)

    return jsonify({"response": response})

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    data = request.get_json()
    user_message = data["message"]
    session_id = data.get("session_id", "default")

    history = get_history(session_id)

    def generate():
        final_messages = None

        for chunk in chatbot.stream_response(user_message, history):
            if isinstance(chunk, dict) and "__final_messages__" in chunk:
                final_messages = chunk["__final_messages__"]
            else:
                yield chunk

        if final_messages:
            save_history(session_id, final_messages)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)