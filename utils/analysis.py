#!/usr/bin/env python3
"""
Analysis utilities for evaluating LLM security test results
"""

import json
from collections import defaultdict


def load_results(file_path):
    """Load test results from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Results file {file_path} not found")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in {file_path}")
        return []


def analyze_results(results):
    """Analyze test results for security vulnerabilities"""
    if not results:
        print("No results to analyze")
        return
    
    total_tests = len(results)
    successful_attacks = sum(1 for r in results if r.get('success', False))
    failed_attacks = total_tests - successful_attacks
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful Attacks: {successful_attacks}")
    print(f"Failed Attacks: {failed_attacks}")
    print(f"Success Rate: {(successful_attacks/total_tests)*100:.2f}%")
    
    # Categorize by prompt type (would need to extract from prompt content)
    categories = defaultdict(int)
    for result in results:
        prompt = result.get('prompt', '')
        if 'ignore' in prompt.lower() or 'disregard' in prompt.lower():
            categories['Injection'] += 1
        elif 'developer mode' in prompt.lower() or 'fictional' in prompt.lower():
            categories['Jailbreak'] += 1
        elif 'database' in prompt.lower() or 'api' in prompt.lower():
            categories['Info_Extract'] += 1
        else:
            categories['Other'] += 1
    
    print("\nAttack Categories:")
    for category, count in categories.items():
        print(f"  {category}: {count}")


def compare_results(baseline_file, secured_file):
    """Compare baseline results with secured results"""
    baseline = load_results(baseline_file)
    secured = load_results(secured_file)
    
    if not baseline or not secured:
        return
    
    baseline_success = sum(1 for r in baseline if r.get('success', False))
    secured_success = sum(1 for r in secured if r.get('success', False))
    
    print("=== Security Improvement Analysis ===")
    print(f"Baseline Successful Attacks: {baseline_success}/{len(baseline)} ({(baseline_success/len(baseline))*100:.2f}%)")
    print(f"Secured Successful Attacks: {secured_success}/{len(secured)} ({(secured_success/len(secured))*100:.2f}%)")
    
    improvement = ((baseline_success - secured_success) / baseline_success * 100) if baseline_success > 0 else 0
    print(f"Security Improvement: {improvement:.2f}% reduction in successful attacks")