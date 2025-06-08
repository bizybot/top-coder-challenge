#!/usr/bin/env python3

import json
import subprocess
import sys
from statistics import mean

def compare_solutions():
    """Compare original and enhanced solutions"""
    
    # Load test data
    with open('public_cases.json', 'r') as f:
        cases = json.load(f)
    
    original_errors = []
    enhanced_errors = []
    
    print(f"Comparing solutions on {len(cases)} cases...")
    
    for i, case in enumerate(cases):
        if i % 200 == 0:
            print(f"Progress: {i}/{len(cases)}")
        
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        try:
            # Test original solution
            result_orig = subprocess.run([
                'python3', 'solution.py',
                str(days), str(miles), str(receipts)
            ], capture_output=True, text=True, timeout=5)
            
            # Test enhanced solution
            result_enh = subprocess.run([
                'python3', 'solution_v2_fraud_aware.py',
                str(days), str(miles), str(receipts)
            ], capture_output=True, text=True, timeout=5)
            
            if result_orig.returncode == 0 and result_enh.returncode == 0:
                pred_orig = float(result_orig.stdout.strip())
                pred_enh = float(result_enh.stdout.strip())
                
                error_orig = abs(expected - pred_orig)
                error_enh = abs(expected - pred_enh)
                
                original_errors.append(error_orig)
                enhanced_errors.append(error_enh)
                
        except Exception as e:
            print(f"Exception in case {i}: {e}")
            continue
    
    # Calculate statistics
    orig_avg = mean(original_errors) if original_errors else 0
    enh_avg = mean(enhanced_errors) if enhanced_errors else 0
    
    orig_max = max(original_errors) if original_errors else 0
    enh_max = max(enhanced_errors) if enhanced_errors else 0
    
    orig_success = len([e for e in original_errors if e < 1000]) / len(original_errors) * 100
    enh_success = len([e for e in enhanced_errors if e < 1000]) / len(enhanced_errors) * 100
    
    print(f"\nSOLUTION COMPARISON:")
    print(f"=" * 50)
    print(f"Original Solution:")
    print(f"  Average error: ${orig_avg:.2f}")
    print(f"  Maximum error: ${orig_max:.2f}")
    print(f"  Success rate: {orig_success:.1f}%")
    
    print(f"\nEnhanced Solution (Fraud-Aware):")
    print(f"  Average error: ${enh_avg:.2f}")
    print(f"  Maximum error: ${enh_max:.2f}")
    print(f"  Success rate: {enh_success:.1f}%")
    
    print(f"\nIMPROVEMENT:")
    print(f"  Average error change: ${enh_avg - orig_avg:.2f} ({'better' if enh_avg < orig_avg else 'worse'})")
    print(f"  Max error change: ${enh_max - orig_max:.2f} ({'better' if enh_max < orig_max else 'worse'})")
    print(f"  Success rate change: {enh_success - orig_success:.1f}% ({'better' if enh_success > orig_success else 'worse'})")
    
    # Analyze specific fraud cases
    fraud_improvements = 0
    fraud_worsenings = 0
    
    print(f"\nFRAUD CASE ANALYSIS:")
    fraud_cases_analyzed = 0
    
    for i, case in enumerate(cases[:100]):  # Just analyze first 100 for speed
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        
        # Check if this is a potential fraud case
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        is_fraud = (miles_per_day > 500 or receipts_per_day > 250 or 
                   (days == 1 and miles > 800) or
                   (days >= 8 and miles_per_day < 30))
        
        if is_fraud and i < len(original_errors) and i < len(enhanced_errors):
            fraud_cases_analyzed += 1
            if enhanced_errors[i] < original_errors[i]:
                fraud_improvements += 1
            elif enhanced_errors[i] > original_errors[i]:
                fraud_worsenings += 1
    
    print(f"  Fraud cases analyzed: {fraud_cases_analyzed}")
    print(f"  Improved: {fraud_improvements}")
    print(f"  Worsened: {fraud_worsenings}")
    print(f"  No change: {fraud_cases_analyzed - fraud_improvements - fraud_worsenings}")

if __name__ == "__main__":
    compare_solutions() 