import os
import requests

class ChatModel:
    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

    def get_response(self, user_input):
        payload = {
            "inputs": user_input
        }

        response = requests.post(
            self.API_URL,
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            return "Model error"

        try:
            result = response.json()
        except:
            return "Invalid model response"

        try:
            return result[0]["generated_text"]
        except:
            return "Sorry, I couldn't generate a response."