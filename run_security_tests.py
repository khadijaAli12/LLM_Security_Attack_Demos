"""
Complete LLM Security Testing Script
Tests all prompts against all LLMs and generates comprehensive report
"""

from malicious_prompts_dataset import get_all_prompts, get_categories
from llm_security_tester import LLMSecurityTester
from security_report_generator import SecurityReportGenerator
import pandas as pd

def main():
    print("\n" + "="*70)
    print("🛡️  LLM Security Testing Framework")
    print("="*70)
    
    # Load prompts
    print("\n📊 Loading malicious prompts dataset...")
    all_prompts = get_all_prompts()
    categories = get_categories()
    
    print(f"   ✓ Loaded {len(all_prompts)} prompts across {len(categories)} categories:")
    for cat in categories:
        count = len([p for p in all_prompts if p['category'] == cat])
        print(f"      - {cat}: {count} prompts")
    
    # Configure models - Updated with working URLs
    all_models = {
        'chatgpt': {'type': 'chatgpt', 'name': 'ChatGPT', 'requires_login': True},
        'gemini': {'type': 'gemini', 'name': 'Gemini', 'requires_login': True},
        'deepseek': {'type': 'deepseek', 'name': 'DeepSeek', 'requires_login': True},
        'qwen': {
            'type': 'huggingface', 
            'name': 'QWEN',
            'url': 'https://huggingface.co/spaces/Qwen/Qwen2.5-72B-Instruct',
            'requires_login': False
        },
        'llama': {
            'type': 'huggingface',
            'name': 'Llama',
            'url': 'https://huggingface.co/spaces/meta-llama/Llama-3.2-90B-Vision-Instruct',
            'requires_login': False
        },
        # Alternative working models
        'mistral': {
            'type': 'huggingface',
            'name': 'Mistral',
            'url': 'https://huggingface.co/spaces/mistralai/Mistral-7B-Instruct-v0.2',
            'requires_login': False
        },
        'phi': {
            'type': 'huggingface',
            'name': 'Phi-3',
            'url': 'https://huggingface.co/spaces/microsoft/Phi-3-mini-4k-instruct',
            'requires_login': False
        }
    }
    
    # Ask user which models to test
    print("\n🤖 Available Models:")
    print("   ⚠️  Note: HuggingFace Spaces may have 404 errors. Login models are more reliable.")
    print("\n   Public (No Login) - May have URL issues:")
    for key, model in all_models.items():
        if not model.get('requires_login', False):
            print(f"      [{key}] {model['name']}")
    print("\n   Login Required (More Reliable):")
    for key, model in all_models.items():
        if model.get('requires_login', False):
            print(f"      [{key}] {model['name']} (⚠️ Login once, then works)")
    
    print("\n⚙️  Model Selection:")
    print("   Options:")
    print("   1. Type model keys separated by comma (e.g., deepseek,qwen,llama)")
    print("   2. Type 'public' to test only public models (no login)")
    print("   3. Type 'all' to test all models (including login required)")
    print("   4. Press Enter for default: public models only")
    
    model_choice = input("\n   Your choice (default=public): ").strip().lower()
    
    if model_choice == '' or model_choice == 'public':
        # Default: Only public models (but warn about 404 issues)
        models_to_test = [m for m in all_models.values() if not m.get('requires_login', False)]
        print("\n   ⚠️  Selected: Public models (HuggingFace - may have 404 errors)")
        print("   💡 Tip: Use 'deepseek' or 'chatgpt' for more reliable testing")
    elif model_choice == 'all':
        models_to_test = list(all_models.values())
        print("\n   ⚠️  Selected: All models (some require login)")
    else:
        # User specified models
        selected_keys = [k.strip() for k in model_choice.split(',')]
        models_to_test = [all_models[k] for k in selected_keys if k in all_models]
        if not models_to_test:
            print("\n   ⚠️  No valid models selected. Using public models only.")
            models_to_test = [m for m in all_models.values() if not m.get('requires_login', False)]
        else:
            print(f"\n   ✓ Selected: {len(models_to_test)} model(s)")
    
    # Remove requires_login from model config (not needed for tester)
    for model in models_to_test:
        model.pop('requires_login', None)
    
    print(f"\n🤖 Models to test: {len(models_to_test)}")
    for model in models_to_test:
        print(f"   - {model['name']}")
    
    # Ask user for configuration
    print("\n⚙️  Configuration:")
    prompts_per_category = input("   Prompts per category (1-10, default=2): ").strip()
    prompts_per_category = int(prompts_per_category) if prompts_per_category.isdigit() else 2
    
    # Sample prompts
    df_prompts = pd.DataFrame(all_prompts)
    sampled = df_prompts.groupby('category').head(prompts_per_category)
    test_prompts = sampled.to_dict('records')
    
    print(f"\n📝 Testing {len(test_prompts)} prompts across {len(models_to_test)} models")
    print(f"   Total tests: {len(test_prompts) * len(models_to_test)}")
    
    confirm = input("\n⚠️  Start testing? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Testing cancelled.")
        return
    
    # Initialize tester
    print("\n🚀 Initializing tester...")
    tester = LLMSecurityTester(headless=False)
    
    # Run tests
    print("\n" + "="*70)
    print("🧪 Starting Security Tests")
    print("="*70)
    
    results = tester.run_test_suite(test_prompts, models_to_test)
    
    # Save results
    print("\n💾 Saving results...")
    df_results = tester.save_results('security_test_results.csv')
    
    # Generate report
    print("\n📈 Generating security report...")
    try:
        generator = SecurityReportGenerator('security_test_results.csv')
        generator.generate_full_report()
        print("   ✓ Report generated successfully!")
    except Exception as e:
        print(f"   ✗ Error generating report: {str(e)}")
    
    # Summary
    print("\n" + "="*70)
    print("✅ Testing Complete!")
    print("="*70)
    print(f"\n📊 Results Summary:")
    print(f"   Total tests: {len(results)}")
    successful = len([r for r in results if r.get('success')])
    print(f"   Successful: {successful}")
    refusals = len([r for r in results if r.get('refused') == True])
    compliances = len([r for r in results if r.get('refused') == False and r.get('success')])
    errors = len([r for r in results if not r.get('success')])
    print(f"   Refused (Secure): {refusals}")
    print(f"   Complied (Vulnerable): {compliances}")
    print(f"   Errors: {errors}")
    
    print(f"\n📁 Files generated:")
    print(f"   - security_test_results.csv")
    print(f"   - security_report_*.html")
    print(f"   - security_analysis_*.png")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()

