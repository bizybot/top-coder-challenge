#!/usr/bin/env python3

import json
import subprocess
import sys
from statistics import mean

def test_enhanced_solution():
    """Test the enhanced fraud-aware solution on public cases"""
    
    # Load test data
    with open('public_cases.json', 'r') as f:
        cases = json.load(f)
    
    errors = []
    exact_matches = 0
    high_errors = []  # Errors > $500
    fraud_flagged = 0
    
    print(f"Testing enhanced solution on {len(cases)} cases...")
    
    for i, case in enumerate(cases):
        if i % 100 == 0:
            print(f"Progress: {i}/{len(cases)}")
        
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        try:
            # Run the enhanced solution
            result = subprocess.run([
                'python3', 'solution_v2_fraud_aware.py',
                str(days), str(miles), str(receipts)
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                print(f"Error in case {i}: {result.stderr}")
                continue
                
            predicted = float(result.stdout.strip())
            error = abs(expected - predicted)
            errors.append(error)
            
            if error == 0:
                exact_matches += 1
            
            if error > 500:
                high_errors.append({
                    'case': i,
                    'days': days,
                    'miles': miles,
                    'receipts': receipts,
                    'expected': expected,
                    'predicted': predicted,
                    'error': error
                })
            
            # Check if this case would be flagged by fraud detection
            miles_per_day = miles / days if days > 0 else 0
            receipts_per_day = receipts / days if days > 0 else 0
            
            if (miles_per_day > 800 or receipts_per_day > 300 or 
                (days >= 8 and miles_per_day < 25) or
                (miles > 1000 and receipts > 1500) or
                (days == 1 and miles > 600) or
                (receipts_per_day > 200 and days <= 3)):
                fraud_flagged += 1
                
        except Exception as e:
            print(f"Exception in case {i}: {e}")
            continue
    
    # Calculate statistics
    avg_error = mean(errors) if errors else 0
    max_error = max(errors) if errors else 0
    success_rate = (len(cases) - len([e for e in errors if e > 1000])) / len(cases) * 100
    
    print(f"\nENHANCED SOLUTION RESULTS:")
    print(f"=" * 40)
    print(f"Total cases: {len(cases)}")
    print(f"Successfully processed: {len(errors)}")
    print(f"Average error: ${avg_error:.2f}")
    print(f"Maximum error: ${max_error:.2f}")
    print(f"Exact matches: {exact_matches}")
    print(f"Success rate (error < $1000): {success_rate:.1f}%")
    print(f"Cases flagged for fraud: {fraud_flagged}")
    print(f"High error cases (>$500): {len(high_errors)}")
    
    if high_errors:
        print(f"\nTOP 10 HIGH ERROR CASES:")
        high_errors.sort(key=lambda x: x['error'], reverse=True)
        for case in high_errors[:10]:
            print(f"Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.2f}")
            print(f"  Expected: ${case['expected']:.2f}, Predicted: ${case['predicted']:.2f}, Error: ${case['error']:.2f}")
    
    return {
        'avg_error': avg_error,
        'max_error': max_error,
        'exact_matches': exact_matches,
        'success_rate': success_rate,
        'fraud_flagged': fraud_flagged,
        'high_errors': len(high_errors)
    }

if __name__ == "__main__":
    results = test_enhanced_solution() 