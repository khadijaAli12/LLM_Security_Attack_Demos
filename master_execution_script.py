"""
Master Execution Script - LLM Security Testing
Run this script to execute the complete security testing workflow
"""

import sys
import time
from datetime import datetime

def print_banner():
    """Display project banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         LLM SECURITY TESTING FRAMEWORK v1.0             ║
║                                                          ║
║    Testing Leading LLMs Against Jailbreak Attacks       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def check_dependencies():
    """Check if all required libraries are installed"""
    print("Checking dependencies...")
    required = [
        'selenium', 'pandas', 'matplotlib', 
        'seaborn', 'webdriver_manager'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✓ All dependencies satisfied\n")
    return True


def step1_generate_dataset():
    """Step 1: Generate malicious prompts dataset"""
    print("="*60)
    print("STEP 1: Generating Malicious Prompts Dataset")
    print("="*60 + "\n")
    
    from malicious_prompts_dataset import save_dataset_to_csv, malicious_prompts
    
    df = save_dataset_to_csv()
    print(f"\n✓ Generated {len(df)} prompts across {len(malicious_prompts)} categories")
    
    return df


def step2_configure_testing():
    """Step 2: Configure which LLMs and prompts to test"""
    print("\n" + "="*60)
    print("STEP 2: Configure Testing Parameters")
    print("="*60 + "\n")
    
    # Ask user for configuration
    print("Which LLMs do you want to test?")
    print("1. ChatGPT (requires login)")
    print("2. Google Gemini (requires login)")
    print("3. DeepSeek")
    print("4. QWEN (HuggingFace)")
    print("5. Llama (HuggingFace)")
    print("6. All (default)")
    
    choice = input("\nEnter numbers separated by commas (e.g., 1,2,3) or press Enter for all: ").strip()
    
    models_map = {
        '1': {'type': 'chatgpt', 'name': 'ChatGPT'},
        '2': {'type': 'gemini', 'name': 'Gemini'},
        '3': {'type': 'deepseek', 'name': 'DeepSeek'},
        '4': {
            'type': 'huggingface', 
            'name': 'QWEN',
            'url': 'https://huggingface.co/spaces/Qwen/Qwen2.5-72B-Instruct'
        },
        '5': {
            'type': 'huggingface',
            'name': 'Llama',
            'url': 'https://huggingface.co/spaces/meta-llama/Llama-3.2-90B-Vision-Instruct'
        }
    }
    
    if choice:
        selected = [models_map[c.strip()] for c in choice.split(',') if c.strip() in models_map]
    else:
        selected = list(models_map.values())
    
    print(f"\n✓ Selected {len(selected)} models: {', '.join([m['name'] for m in selected])}")
    
    # Ask for prompt limit
    num_prompts = input("\nHow many prompts per category to test? (default: 3, max: all): ").strip()
    try:
        num_prompts = int(num_prompts) if num_prompts else 3
    except:
        num_prompts = 3
    
    print(f"✓ Will test {num_prompts} prompts per category")
    
    return selected, num_prompts


def step3_run_tests(models, num_prompts):
    """Step 3: Execute security tests"""
    print("\n" + "="*60)
    print("STEP 3: Running Security Tests")
    print("="*60 + "\n")
    
    from llm_security_tester import LLMSecurityTester
    from malicious_prompts_dataset import get_all_prompts, malicious_prompts
    
    # Prepare prompts
    all_prompts = get_all_prompts()
    
    # Sample prompts per category
    import pandas as pd
    df_prompts = pd.DataFrame(all_prompts)
    sampled = df_prompts.groupby('category').head(num_prompts)
    test_prompts = sampled.to_dict('records')
    
    print(f"Testing {len(test_prompts)} prompts across {len(models)} models")
    print(f"Estimated time: {len(test_prompts) * len(models) * 0.5} minutes\n")
    
    proceed = input("Proceed with testing? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Testing cancelled.")
        return None
    
    # Initialize tester
    tester = LLMSecurityTester(headless=False)
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("  - ChatGPT and Gemini require you to be logged in")
    print("  - Browser windows will open automatically")
    print("  - Do not close browser windows during testing")
    print("  - Tests may take 15-30 seconds per prompt\n")
    
    time.sleep(3)
    
    # Run tests
    results = tester.run_test_suite(test_prompts, models)
    
    # Save results
    df_results = tester.save_results()
    
    print(f"\n✓ Testing complete! {len(results)} tests executed")
    
    return df_results


def step4_generate_report():
    """Step 4: Generate analysis report"""
    print("\n" + "="*60)
    print("STEP 4: Generating Security Report")
    print("="*60 + "\n")
    
    from security_report_generator import SecurityReportGenerator
    
    try:
        generator = SecurityReportGenerator('security_test_results.csv')
        generator.generate_full_report()
        
        print("\n✓ Report generation complete!")
        print("\nGenerated files:")
        print("  - security_test_results.csv (raw data)")
        print("  - security_report_*.md (detailed report)")
        print("  - security_analysis_*.png (visualizations)")
        print("  - security_summary_*.json (JSON summary)")
        
        return True
        
    except FileNotFoundError:
        print("✗ No results file found. Please run tests first.")
        return False


def main():
    """Main execution flow"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🎯 What would you like to do?")
    print("1. Full workflow (dataset → testing → report)")
    print("2. Generate dataset only")
    print("3. Run tests only (requires existing dataset)")
    print("4. Generate report only (requires test results)")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        # Full workflow
        df = step1_generate_dataset()
        models, num_prompts = step2_configure_testing()
        results = step3_run_tests(models, num_prompts)
        if results is not None:
            step4_generate_report()
    
    elif choice == '2':
        step1_generate_dataset()
    
    elif choice == '3':
        models, num_prompts = step2_configure_testing()
        step3_run_tests(models, num_prompts)
    
    elif choice == '4':
        step4_generate_report()
    
    else:
        print("Invalid option selected.")
        return
    
    print("\n" + "="*60)
    print("🎉 WORKFLOW COMPLETE!")
    print("="*60)
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThank you for using LLM Security Testing Framework!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)