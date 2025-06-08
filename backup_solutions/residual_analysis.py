#!/usr/bin/env python3

import json
import statistics
import math
from collections import defaultdict

def analyze_residuals():
    """Analyze residuals from the best formula to find remaining patterns"""
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("RESIDUAL ANALYSIS FOR BEST FORMULA")
    print("=" * 50)
    print("Formula: days*110 + miles*0.5 + sqrt(receipts)*10")
    print()
    
    # Calculate residuals for all cases
    residuals = []
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        # Best formula
        predicted = days * 110 + miles * 0.5 + math.sqrt(max(receipts, 0)) * 10
        residual = actual - predicted
        
        residuals.append({
            'residual': residual,
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'actual': actual,
            'predicted': predicted,
            'case': case
        })
    
    # Sort by residual
    residuals.sort(key=lambda x: x['residual'])
    
    print("LARGEST NEGATIVE RESIDUALS (underestimated):")
    for i, r in enumerate(residuals[:10]):
        print(f"  {i+1}. Residual: {r['residual']:.2f}")
        print(f"     {r['days']}d, {r['miles']}mi, ${r['receipts']:.2f} → ${r['actual']:.2f} (pred: ${r['predicted']:.2f})")
        
        # Look for patterns
        efficiency = r['miles'] / r['days'] if r['days'] > 0 else 0
        receipts_per_day = r['receipts'] / r['days'] if r['days'] > 0 else 0
        print(f"     Efficiency: {efficiency:.1f} mi/day, Receipts: ${receipts_per_day:.2f}/day")
        print()
    
    print("LARGEST POSITIVE RESIDUALS (overestimated):")
    for i, r in enumerate(residuals[-10:]):
        print(f"  {i+1}. Residual: {r['residual']:.2f}")
        print(f"     {r['days']}d, {r['miles']}mi, ${r['receipts']:.2f} → ${r['actual']:.2f} (pred: ${r['predicted']:.2f})")
        
        # Look for patterns
        efficiency = r['miles'] / r['days'] if r['days'] > 0 else 0
        receipts_per_day = r['receipts'] / r['days'] if r['days'] > 0 else 0
        print(f"     Efficiency: {efficiency:.1f} mi/day, Receipts: ${receipts_per_day:.2f}/day")
        print()
    
    # Analyze residuals by trip duration
    print("RESIDUAL PATTERNS BY TRIP DURATION:")
    duration_residuals = defaultdict(list)
    for r in residuals:
        duration_residuals[r['days']].append(r['residual'])
    
    for days in sorted(duration_residuals.keys()):
        res_list = duration_residuals[days]
        avg_residual = statistics.mean(res_list)
        print(f"  {days} days: avg residual {avg_residual:.2f} ({len(res_list)} cases)")
    
    print()
    
    # Analyze residuals by efficiency (miles per day)
    print("RESIDUAL PATTERNS BY EFFICIENCY:")
    efficiency_residuals = defaultdict(list)
    for r in residuals:
        efficiency = r['miles'] / r['days'] if r['days'] > 0 else 0
        efficiency_bucket = int(efficiency // 50) * 50  # Group by 50 mi/day buckets
        efficiency_residuals[efficiency_bucket].append(r['residual'])
    
    for efficiency in sorted(efficiency_residuals.keys())[:15]:
        if len(efficiency_residuals[efficiency]) >= 5:  # Only show buckets with enough data
            res_list = efficiency_residuals[efficiency]
            avg_residual = statistics.mean(res_list)
            print(f"  {efficiency}-{efficiency+49} mi/day: avg residual {avg_residual:.2f} ({len(res_list)} cases)")
    
    print()
    
    # Analyze residuals by receipt amount
    print("RESIDUAL PATTERNS BY RECEIPT AMOUNT:")
    receipt_residuals = defaultdict(list)
    for r in residuals:
        receipt_bucket = int(r['receipts'] // 100) * 100  # Group by $100 buckets
        receipt_residuals[receipt_bucket].append(r['residual'])
    
    for receipts in sorted(receipt_residuals.keys())[:15]:
        if len(receipt_residuals[receipts]) >= 5:
            res_list = receipt_residuals[receipts]
            avg_residual = statistics.mean(res_list)
            print(f"  ${receipts}-${receipts+99}: avg residual {avg_residual:.2f} ({len(res_list)} cases)")
    
    print()
    
    # Look for interaction patterns
    print("INTERACTION PATTERN ANALYSIS:")
    
    # High efficiency + low receipts
    high_eff_low_rec = [r for r in residuals if (r['miles']/r['days'] > 200 if r['days'] > 0 else False) and r['receipts'] < 100]
    if high_eff_low_rec:
        avg_residual = statistics.mean([r['residual'] for r in high_eff_low_rec])
        print(f"  High efficiency (>200 mi/day) + low receipts (<$100): avg residual {avg_residual:.2f} ({len(high_eff_low_rec)} cases)")
    
    # Long trips + high receipts
    long_high_rec = [r for r in residuals if r['days'] >= 8 and r['receipts'] > 500]
    if long_high_rec:
        avg_residual = statistics.mean([r['residual'] for r in long_high_rec])
        print(f"  Long trips (8+ days) + high receipts (>$500): avg residual {avg_residual:.2f} ({len(long_high_rec)} cases)")
    
    # 5-day trips (special case mentioned in interviews)
    five_day_trips = [r for r in residuals if r['days'] == 5]
    if five_day_trips:
        avg_residual = statistics.mean([r['residual'] for r in five_day_trips])
        print(f"  5-day trips: avg residual {avg_residual:.2f} ({len(five_day_trips)} cases)")
        
        # Analyze 5-day trips by efficiency
        five_day_high_eff = [r for r in five_day_trips if r['miles']/r['days'] > 180]
        five_day_low_eff = [r for r in five_day_trips if r['miles']/r['days'] <= 180]
        
        if five_day_high_eff:
            avg_residual_high = statistics.mean([r['residual'] for r in five_day_high_eff])
            print(f"    5-day high efficiency (>180 mi/day): avg residual {avg_residual_high:.2f} ({len(five_day_high_eff)} cases)")
        
        if five_day_low_eff:
            avg_residual_low = statistics.mean([r['residual'] for r in five_day_low_eff])
            print(f"    5-day low efficiency (≤180 mi/day): avg residual {avg_residual_low:.2f} ({len(five_day_low_eff)} cases)")
    
    print()
    
    # Try to find a correction formula
    print("CORRECTION FORMULA ANALYSIS:")
    
    # Test if residuals correlate with specific factors
    print("Testing correction factors...")
    
    # Test days-based correction
    days_corrections = {}
    for days in sorted(duration_residuals.keys()):
        if len(duration_residuals[days]) >= 5:
            avg_residual = statistics.mean(duration_residuals[days])
            days_corrections[days] = avg_residual
    
    print("Days-based corrections needed:")
    for days, correction in days_corrections.items():
        print(f"  {days} days: {correction:+.2f}")
    
    # Test efficiency-based correction
    print("\nEfficiency-based corrections needed:")
    for efficiency in sorted(efficiency_residuals.keys())[:10]:
        if len(efficiency_residuals[efficiency]) >= 5:
            avg_residual = statistics.mean(efficiency_residuals[efficiency])
            print(f"  {efficiency}-{efficiency+49} mi/day: {avg_residual:+.2f}")

if __name__ == "__main__":
    analyze_residuals() 