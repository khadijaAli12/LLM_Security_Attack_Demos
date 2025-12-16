import requests
import json

def test_ollama_connection():
    try:
        print("Testing Ollama connection...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:latest",
                "prompt": "Hello, this is a test. Please respond with 'Test successful'",
                "stream": False
            },
            timeout=300  # 5 minutes timeout
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(data.get('response', 'No response field found'))
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    test_ollama_connection()