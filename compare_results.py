import pandas as pd
import glob
import os
from datetime import datetime

def find_latest_results(prefix):
    """Find the latest results file with the given prefix"""
    files = glob.glob(f'security_test_results_{prefix}_*.csv')
    if not files:
        return None
    
    # Sort by timestamp in filename
    files.sort(key=lambda x: x.split('_')[-1].split('.')[0], reverse=True)
    return files[0]

def compare_before_after():
    """Compare before and after test results"""
    print("LLM Security Test Results Comparison")
    print("=" * 50)
    
    # Find before and after results
    before_file = find_latest_results("before")
    after_file = find_latest_results("after")
    
    if not before_file:
        print("No 'before' results found. Run tests with 'before' suffix first.")
        return
        
    if not after_file:
        print("No 'after' results found. Run tests with 'after' suffix first.")
        return
    
    print(f"Before: {before_file}")
    print(f"After:  {after_file}")
    print()
    
    # Load results
    try:
        before_df = pd.read_csv(before_file)
        after_df = pd.read_csv(after_file)
    except Exception as e:
        print(f"Error loading results: {e}")
        return
    
    # Calculate metrics
    def calculate_metrics(df):
        total = len(df)
        successful = len(df[df['success'] == True])
        refused = len(df[df['refused'] == True])
        security_score = (refused / successful * 100) if successful > 0 else 0
        return {
            'total': total,
            'successful': successful,
            'refused': refused,
            'security_score': security_score
        }
    
    before_metrics = calculate_metrics(before_df)
    after_metrics = calculate_metrics(after_df)
    
    # Display comparison
    print("Security Score Comparison:")
    print("-" * 30)
    print(f"{'Metric':<20} {'Before':<10} {'After':<10} {'Change':<10}")
    print("-" * 30)
    print(f"{'Total Tests':<20} {before_metrics['total']:<10} {after_metrics['total']:<10} {'-':<10}")
    print(f"{'Successful Tests':<20} {before_metrics['successful']:<10} {after_metrics['successful']:<10} {'-':<10}")
    print(f"{'Refused Requests':<20} {before_metrics['refused']:<10} {after_metrics['refused']:<10} {after_metrics['refused'] - before_metrics['refused']:<10}")
    print(f"{'Security Score %':<20} {before_metrics['security_score']:<10.2f} {after_metrics['security_score']:<10.2f} {after_metrics['security_score'] - before_metrics['security_score']:<10.2f}")
    print()
    
    # Improvement calculation
    improvement = after_metrics['security_score'] - before_metrics['security_score']
    if improvement > 0:
        print(f"IMPROVEMENT: Security score increased by {improvement:.2f}%")
    elif improvement < 0:
        print(f"REGRESSION: Security score decreased by {abs(improvement):.2f}%")
    else:
        print("No change in security score")
    
    # Category-wise comparison
    print("\nCategory-wise Comparison:")
    print("-" * 40)
    
    categories = set(before_df['category'].unique()) | set(after_df['category'].unique())
    
    for category in sorted(categories):
        before_cat = before_df[before_df['category'] == category]
        after_cat = after_df[after_df['category'] == category]
        
        if len(before_cat) > 0 and len(after_cat) > 0:
            before_refused = len(before_cat[before_cat['refused'] == True])
            before_total = len(before_cat)
            before_rate = (before_refused / before_total * 100) if before_total > 0 else 0
            
            after_refused = len(after_cat[after_cat['refused'] == True])
            after_total = len(after_cat)
            after_rate = (after_refused / after_total * 100) if after_total > 0 else 0
            
            change = after_rate - before_rate
            
            print(f"{category:<25} {before_rate:>6.2f}% → {after_rate:>6.2f}% ({'+' if change >= 0 else ''}{change:>6.2f}%)")

if __name__ == "__main__":
    compare_before_after()