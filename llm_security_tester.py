import time
import random
import pandas as pd
from datetime import datetime
import os

class LLMSecurityTester:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.results = []
    
    def setup_driver(self):
        """Setup web driver for testing"""
        # Placeholder for actual implementation
        pass
    
    def close_driver(self):
        """Close web driver"""
        # Placeholder for actual implementation
        pass
    
    def test_chatgpt(self, prompt):
        """Test ChatGPT with a prompt"""
        # Simulate API call delay
        time.sleep(1)
        return {
            'llm': 'ChatGPT',
            'prompt': prompt,
            'response': self._generate_mock_response(prompt),
            'success': True,
            'refused': random.choice([True, False]),
            'error': None
        }
    
    def test_gemini(self, prompt):
        """Test Gemini with a prompt"""
        # Simulate API call delay
        time.sleep(1)
        return {
            'llm': 'Gemini',
            'prompt': prompt,
            'response': self._generate_mock_response(prompt),
            'success': True,
            'refused': random.choice([True, False]),
            'error': None
        }
    
    def test_deepseek(self, prompt):
        """Test DeepSeek with a prompt"""
        # Simulate API call delay
        time.sleep(1)
        return {
            'llm': 'DeepSeek',
            'prompt': prompt,
            'response': self._generate_mock_response(prompt),
            'success': True,
            'refused': random.choice([True, False]),
            'error': None
        }
    
    def test_huggingface_model(self, prompt, url, model_name):
        """Test HuggingFace model with a prompt"""
        # Simulate API call delay
        time.sleep(1)
        return {
            'llm': model_name,
            'prompt': prompt,
            'response': self._generate_mock_response(prompt),
            'success': True,
            'refused': random.choice([True, False]),
            'error': None
        }
    
    def _generate_mock_response(self, prompt):
        """Generate a mock response for testing"""
        responses = [
            "I cannot comply with that request as it violates my ethical guidelines.",
            "I'm sorry, but I can't assist with that.",
            "That request is outside my programming parameters.",
            "I'm designed to be helpful, harmless, and honest.",
            "I don't have access to that information.",
            "I cannot provide that information as it may be harmful.",
            "As an AI assistant, I must follow strict safety protocols.",
            "I'm unable to fulfill this request due to security restrictions."
        ]
        return random.choice(responses)
    
    def save_results(self, suffix=""):
        """Save test results to CSV with optional suffix for before/after comparison"""
        import pandas as pd
        from datetime import datetime
        
        df = pd.DataFrame(self.results)
        
        # If suffix is provided, save with timestamp for comparison
        if suffix:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'security_test_results_{suffix}_{timestamp}.csv'
            df.to_csv(filename, index=False)
            print(f"Results saved to {filename}")
        
        # Always save to main file for dashboard
        df.to_csv('security_test_results.csv', index=False)
        print("Results saved to security_test_results.csv")
        
        # Also save results to a backup file to ensure persistence
        try:
            backup_filename = f'security_test_results_backup_{datetime.now().strftime("%Y%m%d")}.csv'
            df.to_csv(backup_filename, index=False)
            print(f"Backup results saved to {backup_filename}")
        except Exception as e:
            print(f"Warning: Could not save backup results: {e}")