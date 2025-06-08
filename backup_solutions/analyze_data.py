#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict

def analyze_public_cases():
    """Analyze the public cases to understand patterns"""
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print(f'Total cases: {len(data)}')
    print('=' * 50)
    
    # Extract all values
    durations = [case['input']['trip_duration_days'] for case in data]
    miles = [case['input']['miles_traveled'] for case in data]
    receipts = [case['input']['total_receipts_amount'] for case in data]
    outputs = [case['expected_output'] for case in data]
    
    # Basic statistics
    print(f'Trip duration: {min(durations)} to {max(durations)} days')
    print(f'Duration distribution: {sorted(set(durations))}')
    print(f'Miles: {min(miles)} to {max(miles)}')
    print(f'Receipts: ${min(receipts):.2f} to ${max(receipts):.2f}')
    print(f'Reimbursements: ${min(outputs):.2f} to ${max(outputs):.2f}')
    print()
    
    # Analyze patterns by duration
    print("Reimbursement patterns by trip duration:")
    duration_groups = defaultdict(list)
    for case in data:
        duration = case['input']['trip_duration_days']
        duration_groups[duration].append(case['expected_output'])
    
    for duration in sorted(duration_groups.keys()):
        outputs_for_duration = duration_groups[duration]
        avg = statistics.mean(outputs_for_duration)
        print(f'  {duration} days: {len(outputs_for_duration)} cases, avg ${avg:.2f}')
    print()
    
    # Look for base per diem patterns
    print("Analyzing base rates (low mileage, low receipts):")
    base_cases = []
    for case in data:
        if (case['input']['miles_traveled'] < 50 and 
            case['input']['total_receipts_amount'] < 25):
            per_day = case['expected_output'] / case['input']['trip_duration_days']
            base_cases.append((case['input']['trip_duration_days'], per_day, case))
    
    print(f"Found {len(base_cases)} base cases:")
    for duration, per_day, case in sorted(base_cases)[:10]:
        inp = case['input']
        print(f"  {duration} days, {inp['miles_traveled']} miles, ${inp['total_receipts_amount']:.2f} → ${case['expected_output']:.2f} (${per_day:.2f}/day)")
    print()
    
    # Analyze mileage patterns
    print("Sample mileage analysis:")
    mileage_cases = []
    for case in data:
        if case['input']['total_receipts_amount'] < 25:  # Focus on low receipt cases
            miles_per_dollar = case['input']['miles_traveled'] / max(case['expected_output'], 1)
            mileage_cases.append((case['input']['miles_traveled'], case['expected_output'], case))
    
    mileage_cases.sort(key=lambda x: x[0])  # Sort by miles
    print("Low receipt cases by mileage:")
    for miles, reimbursement, case in mileage_cases[:15]:
        inp = case['input']
        print(f"  {miles} miles, {inp['trip_duration_days']} days, ${inp['total_receipts_amount']:.2f} → ${reimbursement:.2f}")
    print()
    
    # Look for the 5-day bonus pattern mentioned in interviews
    print("5-day trip analysis (checking for bonuses):")
    five_day_cases = [case for case in data if case['input']['trip_duration_days'] == 5]
    print(f"Found {len(five_day_cases)} 5-day cases")
    
    if five_day_cases:
        five_day_avg = statistics.mean([case['expected_output'] for case in five_day_cases])
        five_day_per_day = five_day_avg / 5
        print(f"5-day trips average: ${five_day_avg:.2f} (${five_day_per_day:.2f}/day)")
        
        # Compare with other durations
        for duration in [4, 6]:
            other_cases = [case for case in data if case['input']['trip_duration_days'] == duration]
            if other_cases:
                other_avg = statistics.mean([case['expected_output'] for case in other_cases])
                other_per_day = other_avg / duration
                print(f"{duration}-day trips average: ${other_avg:.2f} (${other_per_day:.2f}/day)")
    
    print()
    
    # Sample of interesting cases
    print("Sample interesting cases:")
    for i in [0, 21, 50, 100, 500, 900]:
        if i < len(data):
            case = data[i]
            inp = case['input']
            out = case['expected_output']
            efficiency = inp['miles_traveled'] / inp['trip_duration_days'] if inp['trip_duration_days'] > 0 else 0
            print(f"  Case {i}: {inp['trip_duration_days']} days, {inp['miles_traveled']} miles, ${inp['total_receipts_amount']:.2f} → ${out:.2f} (eff: {efficiency:.1f} mi/day)")

if __name__ == "__main__":
    analyze_public_cases() 