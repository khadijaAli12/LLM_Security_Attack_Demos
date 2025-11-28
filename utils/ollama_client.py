import requests

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate_response(self, prompt, model="llama3.1:latest"):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            return response.json()['response']
        except Exception as e:
            return f"Error: {str(e)}"