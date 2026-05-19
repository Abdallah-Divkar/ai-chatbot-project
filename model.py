from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ChatModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

    def get_response(self, user_input):
        new_input_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token,
            return_tensors="pt"
        )

        bot_output = self.model.generate(
            new_input_ids,
            max_length=200,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95
        )

        response = self.tokenizer.decode(
            bot_output[:, new_input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )

        return response