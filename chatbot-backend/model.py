import os
import requests

class ChatModel:
    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

    def get_response(self, user_input):
        payload = {"inputs": user_input}

        response = requests.post(
            self.API_URL,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        # DEBUG (temporarily)
        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        try:
            data = response.json()
        except:
            return f"Invalid JSON: {response.text}"

        # Handle HF error format
        if isinstance(data, dict) and "error" in data:
            return f"HF Error: {data['error']}"

        # Handle empty response
        if not data:
            return "Empty response (model still loading or failed)"

        # Handle list format
        if isinstance(data, list):
            if "generated_text" in data[0]:
                return data[0]["generated_text"]
            return str(data)

        # Handle dict format
        if isinstance(data, dict):
            return data.get("generated_text", str(data))

        return str(data)
    '''def get_response(self, user_input):
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

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)'''
