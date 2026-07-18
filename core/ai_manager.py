import ollama


class AIManager:
    def __init__(self, model="qwen3"):
        self.model = model

    def ask(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]