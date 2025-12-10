import os
import random

def get_sample_prompts(dataset_file, num_samples=3):
    """Get a few sample prompts from a dataset file"""
    filepath = os.path.join("datasets", dataset_file)
    
    if not os.path.exists(filepath):
        return []
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Split by delimiter (---)
        prompt_blocks = content.split('---')
        prompts = []
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
        
        # Return random samples
        return random.sample(prompts, min(num_samples, len(prompts)))

def main():
    print("🎯 Sample Prompts from Each Dataset")
    print("=" * 60)
    
    datasets = [
        ("Advanced Jailbreaks", "advanced_jailbreaks_reduced.txt"),
        ("Advanced Prompt Injections", "advanced_prompt_injections_reduced.txt"),
        ("Information Extraction", "information_extraction_reduced.txt"),
        ("Obfuscated Attacks", "obfuscated_attacks_reduced.txt"),
        ("Social Engineering", "social_engineering_reduced.txt"),
        ("Payload Injection", "payload_injection_reduced.txt"),
        ("Hallucination Attacks", "hallucination_attacks_reduced.txt"),
        ("Context Manipulation", "context_manipulation_reduced.txt"),
        ("Adversarial Prompts", "adversarial_prompts_reduced.txt"),
        ("Comprehensive Jailbreaks", "jailbreaks_comprehensive_reduced.txt")
    ]
    
    for dataset_name, filename in datasets:
        print(f"\n📁 {dataset_name}:")
        print("-" * 40)
        
        samples = get_sample_prompts(filename, 2)
        for i, prompt in enumerate(samples, 1):
            print(f"{i}. {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    
    print(f"\n📊 Total datasets: {len(datasets)}")
    print(f"📈 Total prompts available: ~551")

if __name__ == "__main__":
    main()