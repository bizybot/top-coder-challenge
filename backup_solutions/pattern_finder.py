#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict
import math

def analyze_patterns():
    """Advanced pattern analysis to reverse engineer the exact formula"""
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("ADVANCED PATTERN ANALYSIS")
    print("=" * 50)
    
    # Test various formula hypotheses
    formulas = [
        # Simple linear combinations
        ("days*100 + miles*0.5 + receipts", lambda d, m, r: d * 100 + m * 0.5 + r),
        ("days*110 + miles*0.6 + receipts*0.8", lambda d, m, r: d * 110 + m * 0.6 + r * 0.8),
        ("days*120 + miles*0.4 + receipts*1.2", lambda d, m, r: d * 120 + m * 0.4 + r * 1.2),
        
        # With efficiency factors
        ("days*100 + miles*0.5 + receipts + (miles/days)*2", lambda d, m, r: d * 100 + m * 0.5 + r + (m/d if d > 0 else 0) * 2),
        ("days*110 + miles*0.6 + receipts*0.9 + (miles/days)*1.5", lambda d, m, r: d * 110 + m * 0.6 + r * 0.9 + (m/d if d > 0 else 0) * 1.5),
        
        # Non-linear combinations
        ("days*100 + sqrt(miles)*20 + receipts", lambda d, m, r: d * 100 + math.sqrt(max(m, 0)) * 20 + r),
        ("days*110 + miles*0.5 + sqrt(receipts)*10", lambda d, m, r: d * 110 + m * 0.5 + math.sqrt(max(r, 0)) * 10),
        
        # Complex interactions
        ("days*100 + miles*0.5 + receipts + days*miles*0.01", lambda d, m, r: d * 100 + m * 0.5 + r + d * m * 0.01),
        ("days*110 + miles*0.6 + receipts*0.8 + days*receipts*0.02", lambda d, m, r: d * 110 + m * 0.6 + r * 0.8 + d * r * 0.02),
    ]
    
    best_formula = None
    best_error = float('inf')
    
    for formula_name, formula_func in formulas:
        errors = []
        for case in data:
            duration = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            actual = case['expected_output']
            
            try:
                predicted = formula_func(duration, miles, receipts)
                error = abs(actual - predicted)
                errors.append(error)
            except:
                errors.append(1000)  # Large error for failed calculations
        
        avg_error = statistics.mean(errors)
        print(f"{formula_name}: avg error ${avg_error:.2f}")
        
        if avg_error < best_error:
            best_error = avg_error
            best_formula = (formula_name, formula_func)
    
    print(f"\nBest formula: {best_formula[0]} (avg error: ${best_error:.2f})")
    
    # Analyze residuals for the best formula
    print("\nAnalyzing residuals for best formula...")
    residuals = []
    for case in data[:50]:  # First 50 cases
        duration = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = best_formula[1](duration, miles, receipts)
        residual = actual - predicted
        residuals.append((residual, case))
    
    # Sort by residual to find patterns
    residuals.sort(key=lambda x: x[0])
    
    print("Cases with largest negative residuals (underestimated):")
    for residual, case in residuals[:5]:
        inp = case['input']
        print(f"  Residual: {residual:.2f}, Case: {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f} → ${case['expected_output']:.2f}")
    
    print("\nCases with largest positive residuals (overestimated):")
    for residual, case in residuals[-5:]:
        inp = case['input']
        print(f"  Residual: {residual:.2f}, Case: {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f} → ${case['expected_output']:.2f}")
    
    # Look for specific patterns in the data
    print("\nLooking for specific patterns...")
    
    # Analyze by trip duration
    duration_analysis = defaultdict(list)
    for case in data:
        duration = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        # Calculate per-day rate
        per_day_rate = actual / duration if duration > 0 else 0
        duration_analysis[duration].append((per_day_rate, miles, receipts, actual))
    
    print("\nPer-day rates by trip duration:")
    for duration in sorted(duration_analysis.keys())[:10]:
        rates = [x[0] for x in duration_analysis[duration]]
        avg_rate = statistics.mean(rates)
        min_rate = min(rates)
        max_rate = max(rates)
        print(f"  {duration} days: avg ${avg_rate:.2f}/day, range ${min_rate:.2f}-${max_rate:.2f}")
    
    # Look for mileage patterns
    print("\nMileage analysis:")
    low_receipt_cases = [case for case in data if case['input']['total_receipts_amount'] < 50]
    
    mileage_groups = defaultdict(list)
    for case in low_receipt_cases:
        miles = case['input']['miles_traveled']
        duration = case['input']['trip_duration_days']
        actual = case['expected_output']
        
        # Group by mileage ranges
        mileage_range = (miles // 50) * 50  # Group in 50-mile buckets
        mileage_groups[mileage_range].append((actual, duration, miles))
    
    for mileage_range in sorted(mileage_groups.keys())[:10]:
        if len(mileage_groups[mileage_range]) >= 3:  # Only show ranges with enough data
            cases = mileage_groups[mileage_range]
            avg_reimbursement = statistics.mean([x[0] for x in cases])
            avg_duration = statistics.mean([x[1] for x in cases])
            avg_miles = statistics.mean([x[2] for x in cases])
            print(f"  {mileage_range}-{mileage_range+49} miles: avg ${avg_reimbursement:.2f} ({len(cases)} cases)")
    
    # Try to find the exact pattern by looking at simple cases
    print("\nAnalyzing simple cases for base patterns:")
    simple_cases = []
    for case in data:
        duration = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        # Look for cases with round numbers or simple patterns
        if (miles % 10 == 0 or miles < 100) and receipts < 50:
            simple_cases.append(case)
    
    simple_cases.sort(key=lambda x: (x['input']['trip_duration_days'], x['input']['miles_traveled']))
    
    print("Simple cases (round miles, low receipts):")
    for case in simple_cases[:15]:
        inp = case['input']
        out = case['expected_output']
        
        # Try to reverse engineer the calculation
        base_estimate = inp['trip_duration_days'] * 100
        mileage_estimate = inp['miles_traveled'] * 0.5
        receipt_estimate = inp['total_receipts_amount']
        total_estimate = base_estimate + mileage_estimate + receipt_estimate
        
        print(f"  {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f} → ${out:.2f} (est: ${total_estimate:.2f}, diff: ${out - total_estimate:.2f})")

if __name__ == "__main__":
    analyze_patterns() 