#!/usr/bin/env python3
"""
Script to run LLM security tests category by category
This prevents memory issues when dealing with large datasets
"""

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("   Success")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print("   Failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"   Exception: {e}")
        return False

def main():
    print("LLM Security Evaluation - Category-wise Testing")
    print("=" * 50)
    
    # Available categories
    categories = [
        "Advanced Jailbreaks",
        "Advanced Prompt Injections", 
        "Information Extraction",
        "Obfuscated Attacks",
        "Social Engineering",
        "Payload Injection",
        "Hallucination Attacks",
        "Context Manipulation",
        "Adversarial Prompts",
        "Comprehensive Jailbreaks"
    ]
    
    # Check if user wants to run a specific category
    if len(sys.argv) > 1:
        category_name = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
        test_suffix = sys.argv[-1] if len(sys.argv) > 1 else ""
        
        if category_name in categories:
            print(f"\nRunning test for category: {category_name}")
            cmd = f"python attacks_test.py \"{category_name}\" {test_suffix}".strip()
            run_command(cmd, f"Testing {category_name}")
        else:
            print(f"Unknown category: {category_name}")
            print("Available categories:")
            for cat in categories:
                print(f"  - {cat}")
    else:
        print("Available categories:")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        print("\nUsage:")
        print("  python run_category_test.py \"Category Name\" [before|after]")
        print("  python run_category_test.py before  # Run all categories with 'before' suffix")
        print("  python run_category_test.py after   # Run all categories with 'after' suffix")

if __name__ == "__main__":
    main()