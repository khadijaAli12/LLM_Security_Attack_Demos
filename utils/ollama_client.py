import requests
import json
import time

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate_response(self, prompt, model="llama3.1:latest"):
        """
        Generate response using Ollama API with better error handling
        """
        try:
            # First, ensure model is loaded
            self._ensure_model_loaded(model)
            
            # Now make the actual request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model, 
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 100,  # Limit response length
                        "temperature": 0.7
                    }
                },
                timeout=300  # 5 minutes timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'response' in data:
                return data['response']
            else:
                return f"Unexpected response format: {data}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timeout - Model not responding"
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama - Check if server is running"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _ensure_model_loaded(self, model):
        """
        Ensure the model is loaded and ready before making requests
        """
        try:
            # Check if model exists
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            models = response.json().get('models', [])
            model_exists = any(m.get('name') == model for m in models)
            
            if not model_exists:
                print(f"Model {model} not found. Please pull it first.")
                return False
                
            # Try to load model with a simple request
            test_response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": "test",
                    "stream": False
                },
                timeout=60  # Increased to 60 seconds
            )
            return test_response.status_code == 200
            
        except Exception as e:
            print(f"Model loading check failed: {e}")
            return False
    
    def chat_response(self, prompt, model="llama3.1:latest"):
        """
        Alternative method using chat endpoint
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {
                        "num_predict": 100,
                        "temperature": 0.7
                    }
                },
                timeout=300  # 5 minutes timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get('message', {}).get('content', 'No content found')
            
        except requests.exceptions.Timeout:
            return "Error: Chat request timeout"
        except Exception as e:
            return f"Error: {str(e)}"