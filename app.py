from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Chatbot API is running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = f"You said: {user_message}"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)