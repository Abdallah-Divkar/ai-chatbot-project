import { useState } from "react";
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // add user message
    const updatedChat = [...chat, { sender: "user", text: message }];
    setChat(updatedChat);

    try {
      const response = await fetch(
        "https://ai-chatbot-project-qgkh.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
          }),
        }
      );

      const data = await response.json();

      setChat([
        ...updatedChat,
        { sender: "bot", text: data.response },
      ]);

    } catch (error) {
      setChat([
        ...updatedChat,
        { sender: "bot", text: "Error connecting to chatbot API." },
      ]);
    }

    setMessage("");
  };

  return (
    <div style={styles.container}>
      <h1>AI Chatbot</h1>

      <div style={styles.chatBox}>
        {chat.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf:
                msg.sender === "user" ? "flex-end" : "flex-start",
              background:
                msg.sender === "user" ? "#007bff" : "#333",
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div style={styles.inputArea}>
        <input
          style={styles.input}
          type="text"
          placeholder="Type a message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />

        <button style={styles.button} onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    padding: "20px",
    fontFamily: "Arial",
  },

  chatBox: {
    height: "500px",
    border: "1px solid #ccc",
    borderRadius: "10px",
    padding: "10px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    marginBottom: "20px",
  },

  message: {
    padding: "12px",
    borderRadius: "10px",
    color: "white",
    maxWidth: "70%",
  },

  inputArea: {
    display: "flex",
    gap: "10px",
  },

  input: {
    flex: 1,
    padding: "12px",
    fontSize: "16px",
  },

  button: {
    padding: "12px 20px",
    cursor: "pointer",
  },
};

export default App;