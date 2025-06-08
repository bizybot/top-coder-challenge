#!/usr/bin/env python3

import json
import sys
from solution_legacy_patches import LegacyPatchedReimbursementSystem

def test_solution():
    """Test the legacy patched system solution"""
    
    # Load test cases
    with open('../public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    system = LegacyPatchedReimbursementSystem()
    
    total_error = 0
    max_error = 0
    max_error_case = None
    correct_predictions = 0
    
    print("Testing Legacy Patched Reimbursement System...")
    print("=" * 60)
    
    # Test a sample of cases first
    sample_cases = test_cases[:20]  # Test first 20 cases
    
    for i, case in enumerate(sample_cases):
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        predicted = system.calculate_reimbursement(days, miles, receipts, show_debug=False)
        error = abs(predicted - expected)
        
        print(f"Case {i+1}: {days}d, {miles}mi, ${receipts:.2f}")
        print(f"  Expected: ${expected:.2f}, Got: ${predicted:.2f}, Error: ${error:.2f}")
        
        total_error += error
        
        if error > max_error:
            max_error = error
            max_error_case = case
        
        if error < 0.01:  # Essentially perfect
            correct_predictions += 1
    
    print("\n" + "=" * 60)
    print(f"Sample Results ({len(sample_cases)} cases):")
    print(f"Average Error: ${total_error / len(sample_cases):.2f}")
    print(f"Max Error: ${max_error:.2f}")
    print(f"Perfect Predictions: {correct_predictions}/{len(sample_cases)} ({100*correct_predictions/len(sample_cases):.1f}%)")
    
    if max_error_case:
        case = max_error_case
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        predicted = system.calculate_reimbursement(days, miles, receipts, show_debug=True)
        
        print(f"\nWorst Case Analysis:")
        print(f"Input: {days}d, {miles}mi, ${receipts:.2f}")
        print(f"Expected: ${expected:.2f}, Got: ${predicted:.2f}")
        print(f"Error: ${abs(predicted - expected):.2f}")
    
    # Calculate estimated full score
    estimated_score = (total_error / len(sample_cases)) * len(test_cases)
    print(f"\nEstimated Full Score: {estimated_score:.0f}")
    
    return estimated_score

def run_full_evaluation():
    """Run full evaluation on all test cases"""
    
    with open('../public_cases.json', 'r') as f:
        test_cases = json.load(f)
    
    system = LegacyPatchedReimbursementSystem()
    
    total_error = 0
    errors = []
    
    print(f"Running full evaluation on {len(test_cases)} cases...")
    
    for i, case in enumerate(test_cases):
        if i % 100 == 0:
            print(f"Processing case {i+1}/{len(test_cases)}")
        
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        expected = case['expected_output']
        
        predicted = system.calculate_reimbursement(days, miles, receipts)
        error = abs(predicted - expected)
        
        total_error += error
        errors.append(error)
    
    avg_error = total_error / len(test_cases)
    max_error = max(errors)
    score = total_error
    
    print(f"\nFull Evaluation Results:")
    print(f"Total Score: {score:.2f}")
    print(f"Average Error: ${avg_error:.2f}")
    print(f"Max Error: ${max_error:.2f}")
    
    # Show distribution
    errors.sort(reverse=True)
    print(f"\nTop 10 worst errors:")
    for i in range(min(10, len(errors))):
        print(f"  ${errors[i]:.2f}")
    
    return score

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        run_full_evaluation()
    else:
        test_solution() 