import os
import pandas as pd
from typing import List, Dict

# Define malicious prompts by category
malicious_prompts = {
    "Advanced Jailbreaks": "advanced_jailbreaks_reduced.txt",
    "Advanced Prompt Injections": "advanced_prompt_injections_reduced.txt",
    "Information Extraction": "information_extraction_reduced.txt",
    "Obfuscated Attacks": "obfuscated_attacks_reduced.txt",
    "Social Engineering": "social_engineering_reduced.txt",
    "Payload Injection": "payload_injection_reduced.txt",
    "Hallucination Attacks": "hallucination_attacks_reduced.txt",
    "Context Manipulation": "context_manipulation_reduced.txt",
    "Adversarial Prompts": "adversarial_prompts_reduced.txt",
    "Comprehensive Jailbreaks": "jailbreaks_comprehensive_reduced.txt"
}

def load_prompts_from_file(filename: str) -> List[str]:
    """Load prompts from a dataset file"""
    prompts = []
    filepath = os.path.join("datasets", filename)
    
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} not found")
        return prompts
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Split by delimiter (---)
        prompt_blocks = content.split('---')
        for block in prompt_blocks:
            block = block.strip()
            if block and not block.startswith('#'):
                # Remove numbering if present
                lines = block.split('\n')
                prompt_lines = [line for line in lines if not line.strip().startswith('#')]
                if prompt_lines:
                    prompt = '\n'.join(prompt_lines).strip()
                    if prompt:
                        prompts.append(prompt)
    return prompts

def get_all_prompts() -> List[Dict[str, str]]:
    """Get all prompts with their categories"""
    all_prompts = []
    
    for category, filename in malicious_prompts.items():
        prompts = load_prompts_from_file(filename)
        for prompt in prompts:
            all_prompts.append({
                'category': category,
                'prompt': prompt
            })
    
    return all_prompts

def save_dataset_to_csv() -> pd.DataFrame:
    """Save all prompts to a CSV file"""
    prompts_data = get_all_prompts()
    df = pd.DataFrame(prompts_data)
    df.to_csv('malicious_prompts_dataset.csv', index=False)
    return df

if __name__ == "__main__":
    # Create dataset CSV
    df = save_dataset_to_csv()
    print(f"Dataset created with {len(df)} prompts across {len(malicious_prompts)} categories")
    print("Categories:", list(malicious_prompts.keys()))