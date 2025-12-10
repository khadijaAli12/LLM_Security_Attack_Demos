import os

def count_prompts_in_file(filename):
    """Count the number of prompts in a dataset file"""
    filepath = os.path.join("datasets", filename)
    
    if not os.path.exists(filepath):
        return 0
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Count prompts by counting the delimiter (---)
        prompt_count = content.count('---') + 1
        # Subtract 1 if the file ends with delimiter
        if content.strip().endswith('---'):
            prompt_count -= 1
        return prompt_count

def main():
    print("🔍 Dataset Validation Script")
    print("=" * 50)
    
    datasets = [
        "advanced_jailbreaks_reduced.txt",
        "advanced_prompt_injections_reduced.txt",
        "information_extraction_reduced.txt",
        "obfuscated_attacks_reduced.txt",
        "social_engineering_reduced.txt",
        "payload_injection_reduced.txt",
        "hallucination_attacks_reduced.txt",
        "context_manipulation_reduced.txt",
        "adversarial_prompts_reduced.txt",
        "jailbreaks_comprehensive_reduced.txt"
    ]
    
    total_prompts = 0
    
    for dataset in datasets:
        prompt_count = count_prompts_in_file(dataset)
        print(f"{dataset:30} : {prompt_count:3} prompts")
        total_prompts += prompt_count
    
    print("=" * 50)
    print(f"{'Total':30} : {total_prompts:3} prompts")
    print(f"Datasets directory exists: {os.path.exists('datasets')}")
    
    # Check if all files exist
    missing_files = []
    for dataset in datasets:
        if not os.path.exists(os.path.join("datasets", dataset)):
            missing_files.append(dataset)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
    else:
        print(f"\n✅ All dataset files are present")

if __name__ == "__main__":
    main()