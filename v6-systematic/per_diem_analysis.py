#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict
import math

def analyze_per_diem_patterns():
    """
    Analyze actual per-day reimbursement rates based on trip characteristics
    to find better patterns than fixed coefficients
    """
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("PER-DIEM PATTERN ANALYSIS")
    print("=" * 50)
    
    # Calculate per-day rates for all cases
    cases_with_rates = []
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        total_reimbursement = case['expected_output']
        
        per_day_rate = total_reimbursement / days if days > 0 else 0
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        cases_with_rates.append({
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'total_reimbursement': total_reimbursement,
            'per_day_rate': per_day_rate,
            'miles_per_day': miles_per_day,
            'receipts_per_day': receipts_per_day
        })
    
    print(f"Analyzing {len(cases_with_rates)} cases...")
    
    # 1. BASIC PER-DAY RATE BY DURATION
    print("\n1. PER-DAY RATES BY TRIP DURATION")
    print("-" * 40)
    
    duration_rates = defaultdict(list)
    for case in cases_with_rates:
        duration_rates[case['days']].append(case['per_day_rate'])
    
    for days in sorted(duration_rates.keys())[:15]:
        rates = duration_rates[days]
        avg_rate = statistics.mean(rates)
        median_rate = statistics.median(rates)
        min_rate = min(rates)
        max_rate = max(rates)
        
        print(f"  {days:2d} days: avg ${avg_rate:6.2f}/day, median ${median_rate:6.2f}, range ${min_rate:6.2f}-${max_rate:6.2f} ({len(rates)} cases)")
    
    # 2. PER-DAY RATES BY MILEAGE BRACKETS
    print("\n2. PER-DAY RATES BY MILES-PER-DAY")
    print("-" * 40)
    
    mileage_brackets = [
        (0, 50, "Low mileage"),
        (50, 100, "Medium-low mileage"), 
        (100, 150, "Medium mileage"),
        (150, 200, "Medium-high mileage"),
        (200, 300, "High mileage"),
        (300, 500, "Very high mileage"),
        (500, 1000, "Extreme mileage")
    ]
    
    for min_miles, max_miles, label in mileage_brackets:
        bracket_cases = [c for c in cases_with_rates if min_miles <= c['miles_per_day'] < max_miles]
        if len(bracket_cases) >= 5:  # Only show brackets with enough data
            rates = [c['per_day_rate'] for c in bracket_cases]
            avg_rate = statistics.mean(rates)
            median_rate = statistics.median(rates)
            
            print(f"  {label:20s} ({min_miles:3d}-{max_miles:3d} mi/day): avg ${avg_rate:6.2f}/day, median ${median_rate:6.2f} ({len(bracket_cases)} cases)")
    
    # 3. PER-DAY RATES BY SPENDING BRACKETS  
    print("\n3. PER-DAY RATES BY RECEIPTS-PER-DAY")
    print("-" * 40)
    
    spending_brackets = [
        (0, 25, "Very low spending"),
        (25, 50, "Low spending"),
        (50, 100, "Medium spending"), 
        (100, 200, "High spending"),
        (200, 400, "Very high spending"),
        (400, 1000, "Extreme spending")
    ]
    
    for min_spend, max_spend, label in spending_brackets:
        bracket_cases = [c for c in cases_with_rates if min_spend <= c['receipts_per_day'] < max_spend]
        if len(bracket_cases) >= 5:
            rates = [c['per_day_rate'] for c in bracket_cases]
            avg_rate = statistics.mean(rates)
            median_rate = statistics.median(rates)
            
            print(f"  {label:20s} (${min_spend:3d}-${max_spend:3d}/day): avg ${avg_rate:6.2f}/day, median ${median_rate:6.2f} ({len(bracket_cases)} cases)")
    
    # 4. COMBINED ANALYSIS - Miles AND Spending
    print("\n4. COMBINED MILES + SPENDING PATTERN ANALYSIS")
    print("-" * 50)
    
    # Create buckets for analysis
    mileage_buckets = [(0, 100, "Low miles"), (100, 200, "Med miles"), (200, 500, "High miles")]
    spending_buckets = [(0, 50, "Low spend"), (50, 150, "Med spend"), (150, 500, "High spend")]
    
    for m_min, m_max, m_label in mileage_buckets:
        for s_min, s_max, s_label in spending_buckets:
            bucket_cases = [c for c in cases_with_rates 
                          if m_min <= c['miles_per_day'] < m_max and s_min <= c['receipts_per_day'] < s_max]
            
            if len(bucket_cases) >= 3:  # Need at least 3 cases for meaningful average
                rates = [c['per_day_rate'] for c in bucket_cases]
                avg_rate = statistics.mean(rates)
                
                print(f"  {m_label} + {s_label}: avg ${avg_rate:6.2f}/day ({len(bucket_cases)} cases)")
    
    # 5. EFFICIENCY ANALYSIS - What drives higher per-day rates?
    print("\n5. EFFICIENCY ANALYSIS")
    print("-" * 25)
    
    # Sort by per-day rate to find patterns
    sorted_cases = sorted(cases_with_rates, key=lambda x: x['per_day_rate'])
    
    # Top 10% highest per-day rates
    top_10_pct = int(len(sorted_cases) * 0.9)
    high_rate_cases = sorted_cases[top_10_pct:]
    
    print("Characteristics of HIGH per-day rate trips:")
    avg_days = statistics.mean([c['days'] for c in high_rate_cases])
    avg_miles_per_day = statistics.mean([c['miles_per_day'] for c in high_rate_cases])
    avg_receipts_per_day = statistics.mean([c['receipts_per_day'] for c in high_rate_cases])
    avg_rate = statistics.mean([c['per_day_rate'] for c in high_rate_cases])
    
    print(f"  Avg duration: {avg_days:.1f} days")
    print(f"  Avg miles/day: {avg_miles_per_day:.1f}")
    print(f"  Avg receipts/day: ${avg_receipts_per_day:.2f}")
    print(f"  Avg per-day rate: ${avg_rate:.2f}")
    
    # Bottom 10% lowest per-day rates
    low_rate_cases = sorted_cases[:int(len(sorted_cases) * 0.1)]
    
    print("\nCharacteristics of LOW per-day rate trips:")
    avg_days = statistics.mean([c['days'] for c in low_rate_cases])
    avg_miles_per_day = statistics.mean([c['miles_per_day'] for c in low_rate_cases])
    avg_receipts_per_day = statistics.mean([c['receipts_per_day'] for c in low_rate_cases])
    avg_rate = statistics.mean([c['per_day_rate'] for c in low_rate_cases])
    
    print(f"  Avg duration: {avg_days:.1f} days")
    print(f"  Avg miles/day: {avg_miles_per_day:.1f}")
    print(f"  Avg receipts/day: ${avg_receipts_per_day:.2f}")
    print(f"  Avg per-day rate: ${avg_rate:.2f}")
    
    # 6. PROPOSED DYNAMIC FORMULA
    print("\n6. DYNAMIC PER-DAY RATE FORMULA PROPOSAL")
    print("-" * 45)
    
    # Try to create a formula based on observed patterns
    # Base rate varies by trip duration (we observed this pattern)
    base_rates_by_duration = {}
    for days in range(1, 15):
        if days in duration_rates and len(duration_rates[days]) >= 5:
            median_rate = statistics.median(duration_rates[days])
            base_rates_by_duration[days] = median_rate
    
    print("Observed median per-day rates by duration:")
    for days, rate in sorted(base_rates_by_duration.items()):
        print(f"  {days:2d} days: ${rate:6.2f}/day")
    
    # Test if we can predict better using dynamic rates
    print("\n7. TESTING DYNAMIC APPROACH")
    print("-" * 35)
    
    def get_dynamic_per_day_rate(days, miles_per_day, receipts_per_day):
        """Calculate dynamic per-day rate based on trip characteristics"""
        
        # Base rate from duration pattern
        if days in base_rates_by_duration:
            base_rate = base_rates_by_duration[days]
        elif days <= 14:
            # Interpolate for missing durations
            base_rate = 800 - (days - 1) * 50  # Rough approximation
        else:
            base_rate = 150  # Long trip rate
        
        # Adjust for mileage efficiency (observed pattern)
        if 150 <= miles_per_day <= 250:
            mileage_bonus = 50  # Sweet spot bonus
        elif miles_per_day >= 300:
            mileage_bonus = 100  # High mileage bonus
        else:
            mileage_bonus = 0
        
        # Adjust for spending level
        if receipts_per_day >= 200:
            spending_bonus = 30
        elif receipts_per_day >= 100:
            spending_bonus = 15
        else:
            spending_bonus = 0
        
        return base_rate + mileage_bonus + spending_bonus
    
    # Test the dynamic approach on some cases
    test_errors = []
    for case in cases_with_rates[:100]:  # Test on first 100 cases
        predicted_per_day = get_dynamic_per_day_rate(
            case['days'], 
            case['miles_per_day'], 
            case['receipts_per_day']
        )
        predicted_total = predicted_per_day * case['days']
        actual_total = case['total_reimbursement']
        error = abs(actual_total - predicted_total)
        test_errors.append(error)
    
    avg_error = statistics.mean(test_errors)
    print(f"Dynamic approach average error on 100 test cases: ${avg_error:.2f}")
    
    # Compare with current formula
    current_errors = []
    for case in cases_with_rates[:100]:
        # Current formula: days*110 + miles*0.5 + sqrt(receipts)*10 + modifiers
        days = case['days']
        miles = case['miles']
        receipts = case['receipts']
        
        predicted = (days * 110 + miles * 0.5 + math.sqrt(max(receipts, 0)) * 10)
        
        # Apply basic modifiers
        if days <= 2:
            predicted *= 1.5
        elif days <= 7:
            predicted *= 1.08
        elif days >= 8:
            predicted *= 0.87
            
        actual = case['total_reimbursement']
        error = abs(actual - predicted)
        current_errors.append(error)
    
    current_avg_error = statistics.mean(current_errors)
    print(f"Current formula average error on same 100 cases: ${current_avg_error:.2f}")
    
    if avg_error < current_avg_error:
        print(f"✅ Dynamic approach is BETTER by ${current_avg_error - avg_error:.2f}")
    else:
        print(f"❌ Current approach is better by ${avg_error - current_avg_error:.2f}")

if __name__ == "__main__":
    analyze_per_diem_patterns() 