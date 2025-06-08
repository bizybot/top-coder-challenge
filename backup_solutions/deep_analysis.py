#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict
import math

def deep_analysis():
    """Deep analysis to reverse engineer the reimbursement formula"""
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("DEEP ANALYSIS OF REIMBURSEMENT PATTERNS")
    print("=" * 60)
    
    # Let's look for base per diem rates
    print("1. BASE PER DIEM ANALYSIS")
    print("-" * 30)
    
    # Group by duration and find minimum reimbursements (likely base rates)
    duration_mins = defaultdict(list)
    for case in data:
        duration = case['input']['trip_duration_days']
        reimbursement = case['expected_output']
        duration_mins[duration].append(reimbursement)
    
    base_rates = {}
    for duration in sorted(duration_mins.keys()):
        min_reimbursement = min(duration_mins[duration])
        base_per_day = min_reimbursement / duration
        base_rates[duration] = base_per_day
        print(f"  {duration} days: min ${min_reimbursement:.2f} → ${base_per_day:.2f}/day")
    
    # Check if there's a consistent base rate
    base_values = list(base_rates.values())
    if len(set([round(x, 0) for x in base_values])) <= 2:
        avg_base = statistics.mean(base_values)
        print(f"  → Consistent base rate: ~${avg_base:.2f}/day")
    else:
        print(f"  → Variable base rates: {[round(x, 2) for x in base_values]}")
    
    print()
    
    # 2. MILEAGE ANALYSIS
    print("2. MILEAGE REIMBURSEMENT ANALYSIS")
    print("-" * 35)
    
    # Look for mileage patterns by examining cases with similar duration/receipts
    mileage_rates = []
    for case in data:
        duration = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        reimbursement = case['expected_output']
        
        # Estimate base cost (assuming ~$100-120/day base)
        estimated_base = duration * 110  # rough estimate
        excess_reimbursement = reimbursement - estimated_base
        
        if miles > 0 and excess_reimbursement > 0:
            rate_per_mile = excess_reimbursement / miles
            mileage_rates.append((miles, rate_per_mile, case))
    
    # Analyze mileage rates
    rates = [rate for _, rate, _ in mileage_rates]
    print(f"  Mileage rate estimates: ${min(rates):.3f} to ${max(rates):.3f} per mile")
    print(f"  Average mileage rate: ${statistics.mean(rates):.3f} per mile")
    print(f"  Median mileage rate: ${statistics.median(rates):.3f} per mile")
    
    # Look for common rates
    rounded_rates = [round(rate, 2) for rate in rates]
    rate_counts = defaultdict(int)
    for rate in rounded_rates:
        rate_counts[rate] += 1
    
    common_rates = sorted(rate_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"  Most common rates: {common_rates}")
    
    print()
    
    # 3. RECEIPT ANALYSIS
    print("3. RECEIPT REIMBURSEMENT ANALYSIS")
    print("-" * 35)
    
    # Look for receipt reimbursement patterns
    receipt_patterns = []
    for case in data:
        duration = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        reimbursement = case['expected_output']
        
        # Try to isolate receipt contribution
        estimated_base = duration * 110
        estimated_mileage = miles * 0.5  # rough estimate
        estimated_receipt_reimbursement = reimbursement - estimated_base - estimated_mileage
        
        if receipts > 0:
            receipt_rate = estimated_receipt_reimbursement / receipts
            receipt_patterns.append((receipts, receipt_rate, case))
    
    receipt_rates = [rate for _, rate, _ in receipt_patterns if rate > 0]
    if receipt_rates:
        print(f"  Receipt rate estimates: {min(receipt_rates):.3f} to {max(receipt_rates):.3f}")
        print(f"  Average receipt rate: {statistics.mean(receipt_rates):.3f}")
        print(f"  Median receipt rate: {statistics.median(receipt_rates):.3f}")
    
    print()
    
    # 4. FORMULA TESTING
    print("4. FORMULA HYPOTHESIS TESTING")
    print("-" * 35)
    
    # Test different formulas
    formulas = [
        ("Base + 0.5*miles + receipts", lambda d, m, r: d * 110 + m * 0.5 + r),
        ("Base + 0.6*miles + receipts", lambda d, m, r: d * 110 + m * 0.6 + r),
        ("Base + 0.4*miles + receipts", lambda d, m, r: d * 110 + m * 0.4 + r),
        ("Base + 0.5*miles + 0.8*receipts", lambda d, m, r: d * 110 + m * 0.5 + r * 0.8),
        ("Base + 0.5*miles + 1.2*receipts", lambda d, m, r: d * 110 + m * 0.5 + r * 1.2),
    ]
    
    for formula_name, formula_func in formulas:
        errors = []
        for case in data[:100]:  # Test on first 100 cases
            duration = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            actual = case['expected_output']
            
            predicted = formula_func(duration, miles, receipts)
            error = abs(actual - predicted)
            errors.append(error)
        
        avg_error = statistics.mean(errors)
        print(f"  {formula_name}: avg error ${avg_error:.2f}")
    
    print()
    
    # 5. SPECIAL CASES ANALYSIS
    print("5. SPECIAL CASES & BONUSES")
    print("-" * 30)
    
    # Look for 5-day bonus pattern
    five_day_cases = [case for case in data if case['input']['trip_duration_days'] == 5]
    four_day_cases = [case for case in data if case['input']['trip_duration_days'] == 4]
    six_day_cases = [case for case in data if case['input']['trip_duration_days'] == 6]
    
    if five_day_cases and four_day_cases:
        five_day_per_day = statistics.mean([case['expected_output'] for case in five_day_cases]) / 5
        four_day_per_day = statistics.mean([case['expected_output'] for case in four_day_cases]) / 4
        
        print(f"  5-day trips: ${five_day_per_day:.2f}/day")
        print(f"  4-day trips: ${four_day_per_day:.2f}/day")
        
        if five_day_per_day < four_day_per_day * 0.9:
            print("  → 5-day trips appear to have LOWER per-day rates (efficiency bonus?)")
        elif five_day_per_day > four_day_per_day * 1.1:
            print("  → 5-day trips appear to have HIGHER per-day rates (bonus?)")
    
    # Look for high mileage patterns
    high_mileage_cases = [case for case in data if case['input']['miles_traveled'] > 500]
    if high_mileage_cases:
        print(f"  High mileage cases (>500 miles): {len(high_mileage_cases)}")
        avg_per_mile = statistics.mean([
            case['expected_output'] / case['input']['miles_traveled'] 
            for case in high_mileage_cases
        ])
        print(f"  Average reimbursement per mile for high mileage: ${avg_per_mile:.3f}")
    
    print()
    
    # 6. DETAILED CASE STUDY
    print("6. DETAILED CASE STUDIES")
    print("-" * 30)
    
    interesting_cases = [
        ("Low everything", lambda c: c['input']['trip_duration_days'] <= 2 and c['input']['miles_traveled'] < 50 and c['input']['total_receipts_amount'] < 25),
        ("High mileage", lambda c: c['input']['miles_traveled'] > 300),
        ("High receipts", lambda c: c['input']['total_receipts_amount'] > 500),
        ("Long duration", lambda c: c['input']['trip_duration_days'] >= 10),
    ]
    
    for case_type, condition in interesting_cases:
        matching_cases = [case for case in data if condition(case)][:3]
        print(f"  {case_type} cases:")
        for case in matching_cases:
            inp = case['input']
            out = case['expected_output']
            print(f"    {inp['trip_duration_days']}d, {inp['miles_traveled']}mi, ${inp['total_receipts_amount']:.2f} → ${out:.2f}")

if __name__ == "__main__":
    deep_analysis() 