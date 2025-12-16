#!/usr/bin/env python3
"""
Complete LLM Security Evaluation Workflow

This script demonstrates the complete workflow:
1. Attack the model using categorized prompts (BEFORE hardening)
2. Gather the results
3. Update the system prompts (manual step)
4. Attack again using those same prompts (AFTER hardening)
5. Gather the results again
6. Generate a report comparing before vs after results
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
    print("LLM Security Evaluation Workflow")
    print("=" * 50)
    
    # Step 1: Run tests BEFORE system prompt hardening
    print("\nSTEP 1: Running tests BEFORE system prompt hardening")
    if not run_command("python attacks_test.py before", "Running before tests"):
        print("❌ Failed to run before tests")
        return
    
    # Wait a bit for file system sync
    time.sleep(2)
    
    # Step 2: Manual step - Update system prompts
    print("\nSTEP 2: Manual step required")
    print("   Please update your system prompts now.")
    print("   Once you've hardened your LLM's system prompt, press Enter to continue...")
    input("   Press Enter when ready...")
    
    # Step 3: Run tests AFTER system prompt hardening
    print("\nSTEP 3: Running tests AFTER system prompt hardening")
    if not run_command("python attacks_test.py after", "Running after tests"):
        print("❌ Failed to run after tests")
        return
    
    # Wait a bit for file system sync
    time.sleep(2)
    
    # Step 4: Compare results
    print("\nSTEP 4: Comparing before and after results")
    if not run_command("python compare_results.py", "Comparing results"):
        print("❌ Failed to compare results")
        return
    
    print("\nWorkflow completed successfully!")
    print("   Check the comparison results above to see the impact of your system prompt hardening.")

if __name__ == "__main__":
    main()