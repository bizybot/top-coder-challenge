#!/usr/bin/env python3

import json
import subprocess
import sys
from statistics import mean

def test_hybrid_solution():
    """Test the hybrid solution on public cases"""
    
    # Load test data
    with open('public_cases.json', 'r') as f:
        cases = json.load(f)
    
    errors = []
    exact_matches = 0
    high_errors = []  # Errors > $500
    extreme_flagged = 0
    
    print(f"Testing hybrid solution on {len(cases)} cases...")
    
    for i, case in enumerate(cases):
        if i % 100 == 0:
            print(f"Progress: {i}/{len(cases)}")
        
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        try:
            # Run the hybrid solution
            result = subprocess.run([
                'python3', 'solution_v3_hybrid.py',
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
            
            # Check if this would be flagged as extreme
            miles_per_day = miles / days if days > 0 else 0
            receipts_per_day = receipts / days if days > 0 else 0
            
            if (miles_per_day > 1000 or receipts_per_day > 500 or 
                (days == 1 and miles > 800) or
                (miles > 1200 and receipts > 2000)):
                extreme_flagged += 1
                
        except Exception as e:
            print(f"Exception in case {i}: {e}")
            continue
    
    # Calculate statistics
    avg_error = mean(errors) if errors else 0
    max_error = max(errors) if errors else 0
    success_rate = (len(cases) - len([e for e in errors if e > 1000])) / len(cases) * 100
    
    print(f"\nHYBRID SOLUTION RESULTS:")
    print(f"=" * 40)
    print(f"Total cases: {len(cases)}")
    print(f"Successfully processed: {len(errors)}")
    print(f"Average error: ${avg_error:.2f}")
    print(f"Maximum error: ${max_error:.2f}")
    print(f"Exact matches: {exact_matches}")
    print(f"Success rate (error < $1000): {success_rate:.1f}%")
    print(f"Cases flagged as extreme: {extreme_flagged}")
    print(f"High error cases (>$500): {len(high_errors)}")
    
    # Show the worst cases
    if high_errors:
        print(f"\nTOP 5 HIGH ERROR CASES:")
        high_errors.sort(key=lambda x: x['error'], reverse=True)
        for case in high_errors[:5]:
            print(f"Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.2f}")
            print(f"  Expected: ${case['expected']:.2f}, Predicted: ${case['predicted']:.2f}, Error: ${case['error']:.2f}")
    
    return {
        'avg_error': avg_error,
        'max_error': max_error,
        'exact_matches': exact_matches,
        'success_rate': success_rate,
        'extreme_flagged': extreme_flagged,
        'high_errors': len(high_errors)
    }

if __name__ == "__main__":
    results = test_hybrid_solution() 