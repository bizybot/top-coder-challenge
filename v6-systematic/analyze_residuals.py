#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict
import math

def analyze_systematic_residuals():
    """
    Analyze the systematic residual patterns to find remaining corrections
    """
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("SYSTEMATIC RESIDUAL ANALYSIS")
    print("=" * 40)
    
    def current_breakthrough_formula(days, miles, receipts):
        """Current breakthrough formula"""
        base_amount = (days * 90 + miles * 0.4 + math.sqrt(max(receipts, 0)) * 15)
        
        # Light modifiers
        if days <= 2:
            base_amount *= 1.2
        elif days <= 7:
            base_amount *= 1.02
        elif days >= 8:
            base_amount *= 0.95
        
        efficiency = miles / days if days > 0 else 0
        if 180 <= efficiency <= 220:
            base_amount *= 1.05
        elif 100 <= efficiency <= 180:
            base_amount *= 1.02
        
        if days == 5:
            base_amount *= 1.02
        
        if miles > 600:
            excess_miles = miles - 600
            penalty = excess_miles * 0.02
            base_amount -= penalty
        
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.01
        
        minimum = days * 40
        base_amount = max(base_amount, minimum)
        
        return base_amount
    
    # Calculate residuals
    residuals = []
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = current_breakthrough_formula(days, miles, receipts)
        residual = actual - predicted
        residuals.append({
            'case': case,
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'actual': actual,
            'predicted': predicted,
            'residual': residual,
            'abs_residual': abs(residual)
        })
    
    # Sort by residual magnitude
    residuals.sort(key=lambda x: x['abs_residual'], reverse=True)
    
    print("Top 10 worst residuals:")
    for i, r in enumerate(residuals[:10]):
        print(f"  {i+1:2d}. {r['days']}d, {r['miles']:4.0f}mi, ${r['receipts']:6.2f} → "
              f"actual=${r['actual']:7.2f}, predicted=${r['predicted']:7.2f}, residual=${r['residual']:7.2f}")
    
    # Analyze patterns in worst cases
    print("\n" + "="*50)
    print("PATTERN ANALYSIS OF WORST RESIDUALS")
    print("="*50)
    
    # Look at top 100 worst cases
    worst_cases = residuals[:100]
    
    # Pattern 1: High receipts
    high_receipt_cases = [r for r in worst_cases if r['receipts'] > 1000]
    print(f"\nHigh receipt cases (>$1000) in worst 100: {len(high_receipt_cases)}")
    if high_receipt_cases:
        avg_residual = statistics.mean([r['residual'] for r in high_receipt_cases])
        print(f"  Average residual: ${avg_residual:.2f}")
        print("  → We're OVER-predicting high receipt cases")
    
    # Pattern 2: Long trips
    long_trip_cases = [r for r in worst_cases if r['days'] >= 8]
    print(f"\nLong trip cases (8+ days) in worst 100: {len(long_trip_cases)}")
    if long_trip_cases:
        avg_residual = statistics.mean([r['residual'] for r in long_trip_cases])
        print(f"  Average residual: ${avg_residual:.2f}")
        if avg_residual > 0:
            print("  → We're UNDER-predicting long trips")
        else:
            print("  → We're OVER-predicting long trips")
    
    # Pattern 3: High mileage
    high_mile_cases = [r for r in worst_cases if r['miles'] > 500]
    print(f"\nHigh mileage cases (>500 miles) in worst 100: {len(high_mile_cases)}")
    if high_mile_cases:
        avg_residual = statistics.mean([r['residual'] for r in high_mile_cases])
        print(f"  Average residual: ${avg_residual:.2f}")
        if avg_residual > 0:
            print("  → We're UNDER-predicting high mileage")
        else:
            print("  → We're OVER-predicting high mileage")
    
    # Pattern 4: Short trips
    short_trip_cases = [r for r in worst_cases if r['days'] <= 2]
    print(f"\nShort trip cases (1-2 days) in worst 100: {len(short_trip_cases)}")
    if short_trip_cases:
        avg_residual = statistics.mean([r['residual'] for r in short_trip_cases])
        print(f"  Average residual: ${avg_residual:.2f}")
        if avg_residual > 0:
            print("  → We're UNDER-predicting short trips")
        else:
            print("  → We're OVER-predicting short trips")
    
    # CORRECTION ANALYSIS
    print("\n" + "="*50)
    print("SYSTEMATIC CORRECTION ANALYSIS")
    print("="*50)
    
    # Group all residuals by different characteristics
    duration_residuals = defaultdict(list)
    receipt_bracket_residuals = defaultdict(list)
    mileage_bracket_residuals = defaultdict(list)
    
    for r in residuals:
        # By duration
        duration_residuals[r['days']].append(r['residual'])
        
        # By receipt brackets
        receipt_bracket = (r['receipts'] // 500) * 500
        receipt_bracket_residuals[receipt_bracket].append(r['residual'])
        
        # By mileage brackets
        mileage_bracket = (r['miles'] // 200) * 200
        mileage_bracket_residuals[mileage_bracket].append(r['residual'])
    
    print("\nAverage residual by trip duration:")
    corrections_by_duration = {}
    for days in sorted(duration_residuals.keys())[:15]:
        residuals_list = duration_residuals[days]
        if len(residuals_list) >= 5:
            avg_residual = statistics.mean(residuals_list)
            corrections_by_duration[days] = avg_residual
            print(f"  {days:2d} days: avg residual = ${avg_residual:6.2f} ({len(residuals_list)} cases)")
    
    print("\nAverage residual by receipt brackets:")
    corrections_by_receipts = {}
    for bracket in sorted(receipt_bracket_residuals.keys())[:10]:
        residuals_list = receipt_bracket_residuals[bracket]
        if len(residuals_list) >= 10:
            avg_residual = statistics.mean(residuals_list)
            corrections_by_receipts[bracket] = avg_residual
            print(f"  ${bracket:4.0f}-${bracket+499:4.0f}: avg residual = ${avg_residual:6.2f} ({len(residuals_list)} cases)")
    
    print("\nAverage residual by mileage brackets:")
    corrections_by_mileage = {}
    for bracket in sorted(mileage_bracket_residuals.keys())[:10]:
        residuals_list = mileage_bracket_residuals[bracket]
        if len(residuals_list) >= 10:
            avg_residual = statistics.mean(residuals_list)
            corrections_by_mileage[bracket] = avg_residual
            print(f"  {bracket:3.0f}-{bracket+199:3.0f} miles: avg residual = ${avg_residual:6.2f} ({len(residuals_list)} cases)")
    
    # PROPOSED CORRECTIONS
    print("\n" + "="*50)
    print("PROPOSED SYSTEMATIC CORRECTIONS")
    print("="*50)
    
    print("\nDuration-based corrections (add these amounts):")
    for days, correction in corrections_by_duration.items():
        if abs(correction) > 20:  # Only show significant corrections
            print(f"  {days:2d} days: {correction:+6.2f}")
    
    print("\nReceipt-based corrections (add these amounts):")
    for bracket, correction in corrections_by_receipts.items():
        if abs(correction) > 15:  # Only show significant corrections
            print(f"  ${bracket:4.0f}+ receipts: {correction:+6.2f}")
    
    print("\nMileage-based corrections (add these amounts):")
    for bracket, correction in corrections_by_mileage.items():
        if abs(correction) > 15:  # Only show significant corrections
            print(f"  {bracket:3.0f}+ miles: {correction:+6.2f}")

if __name__ == "__main__":
    analyze_systematic_residuals() 