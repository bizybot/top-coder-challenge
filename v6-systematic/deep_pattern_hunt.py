#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict, Counter
import math

def hunt_for_missing_patterns():
    """
    Deep dive to find the missing patterns that could explain 10x better performance
    """
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("HUNTING FOR MISSING PATTERNS")
    print("=" * 50)
    print(f"Target: ~$20 avg error (score ~2000)")
    print(f"Current: ~$230 avg error (score ~23000)")
    print(f"Gap: 10x improvement needed\n")
    
    # 1. LOOK FOR EXACT MATHEMATICAL RELATIONSHIPS
    print("1. TESTING EXACT MATHEMATICAL RELATIONSHIPS")
    print("-" * 50)
    
    # Test if there are exact ratios or patterns
    exact_patterns = []
    for case in data[:50]:  # Test on subset first
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Test various exact relationships
        ratios = {
            'output/days': output / days if days > 0 else 0,
            'output/miles': output / miles if miles > 0 else 0,
            'output/receipts': output / receipts if receipts > 0 else 0,
            'output/sqrt(receipts)': output / math.sqrt(receipts) if receipts > 0 else 0,
            'output/(days*miles)': output / (days * miles) if days > 0 and miles > 0 else 0,
            'output/(days+miles+receipts)': output / (days + miles + receipts),
            'output/(days*100+miles*0.5)': output / (days * 100 + miles * 0.5) if (days * 100 + miles * 0.5) > 0 else 0,
        }
        
        exact_patterns.append({
            'case': case,
            'ratios': ratios
        })
    
    # Look for consistent ratios
    print("Looking for consistent ratios across cases:")
    ratio_names = ['output/days', 'output/sqrt(receipts)', 'output/(days*100+miles*0.5)']
    
    for ratio_name in ratio_names:
        values = [p['ratios'][ratio_name] for p in exact_patterns if p['ratios'][ratio_name] > 0]
        if values:
            avg_val = statistics.mean(values)
            std_val = statistics.stdev(values) if len(values) > 1 else 0
            min_val = min(values)
            max_val = max(values)
            
            print(f"  {ratio_name}: avg={avg_val:.3f}, std={std_val:.3f}, range={min_val:.3f}-{max_val:.3f}")
    
    # 2. LOOK FOR DISCRETE PATTERNS OR LOOKUP TABLES
    print("\n2. SEARCHING FOR DISCRETE PATTERNS")
    print("-" * 40)
    
    # Check if certain combinations always give same results
    combination_results = defaultdict(list)
    
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Round values to see if there are discrete patterns
        rounded_combo = (
            days,
            round(miles / 10) * 10,  # Round to nearest 10
            round(receipts / 25) * 25  # Round to nearest 25
        )
        
        combination_results[rounded_combo].append(output)
    
    # Find combinations that appear multiple times with same/similar results
    print("Combinations appearing multiple times:")
    consistent_combos = 0
    for combo, outputs in combination_results.items():
        if len(outputs) >= 3:  # At least 3 occurrences
            std_dev = statistics.stdev(outputs) if len(outputs) > 1 else 0
            avg_output = statistics.mean(outputs)
            
            if std_dev < 10:  # Very consistent results
                consistent_combos += 1
                if consistent_combos <= 10:  # Show first 10
                    print(f"  {combo[0]}d, ~{combo[1]}mi, ~${combo[2]} → ${avg_output:.2f} ±{std_dev:.2f} ({len(outputs)} cases)")
    
    print(f"Found {consistent_combos} highly consistent combinations")
    
    # 3. ANALYZE RESIDUALS FROM CURRENT FORMULA
    print("\n3. ANALYZING CURRENT FORMULA RESIDUALS")
    print("-" * 45)
    
    def current_formula(days, miles, receipts):
        """Our current best formula"""
        base_amount = (days * 110 + miles * 0.5 + math.sqrt(max(receipts, 0)) * 10)
        
        # Apply modifiers
        if days <= 2:
            base_amount *= 1.5
        elif days <= 7:
            base_amount *= 1.08
        elif days >= 8:
            base_amount *= 0.87
        
        # Efficiency bonus
        if days > 0:
            efficiency = miles / days
            if 180 <= efficiency <= 220:
                base_amount *= 1.12
            elif 100 <= efficiency <= 180:
                base_amount *= 1.04
        
        # Five-day bonus
        if days == 5:
            base_amount *= 1.05
        
        # High mileage penalty
        if miles > 500:
            excess_miles = miles - 500
            penalty = excess_miles * 0.04
            base_amount -= penalty
        
        # Randomization
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.02
        
        # Minimum
        minimum = days * 50
        base_amount = max(base_amount, minimum)
        
        return base_amount
    
    # Calculate residuals
    residuals = []
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        actual = case['expected_output']
        
        predicted = current_formula(days, miles, receipts)
        residual = actual - predicted
        residuals.append({
            'case': case,
            'predicted': predicted,
            'actual': actual,
            'residual': residual,
            'abs_residual': abs(residual)
        })
    
    # Sort by absolute residual
    residuals.sort(key=lambda x: x['abs_residual'], reverse=True)
    
    print("Worst prediction errors:")
    for i, r in enumerate(residuals[:10]):
        case = r['case']
        inp = case['input']
        print(f"  {i+1:2d}. {inp['trip_duration_days']}d, {inp['miles_traveled']:4.0f}mi, ${inp['total_receipts_amount']:6.2f} → "
              f"actual=${r['actual']:7.2f}, predicted=${r['predicted']:7.2f}, error=${r['abs_residual']:6.2f}")
    
    # 4. LOOK FOR PATTERNS IN RESIDUALS
    print("\n4. PATTERNS IN RESIDUALS")
    print("-" * 25)
    
    # Group residuals by different characteristics
    residual_patterns = {
        'by_days': defaultdict(list),
        'by_miles_range': defaultdict(list),
        'by_receipts_range': defaultdict(list),
        'by_efficiency': defaultdict(list)
    }
    
    for r in residuals:
        case = r['case']
        inp = case['input']
        days = inp['trip_duration_days']
        miles = inp['miles_traveled']
        receipts = inp['total_receipts_amount']
        residual = r['residual']
        
        # Group by characteristics
        residual_patterns['by_days'][days].append(residual)
        
        miles_range = (miles // 100) * 100
        residual_patterns['by_miles_range'][miles_range].append(residual)
        
        receipts_range = (receipts // 200) * 200
        residual_patterns['by_receipts_range'][receipts_range].append(residual)
        
        efficiency = miles / days if days > 0 else 0
        eff_range = (efficiency // 50) * 50
        residual_patterns['by_efficiency'][eff_range].append(residual)
    
    # Analyze patterns
    print("Systematic residual patterns (avg residual by category):")
    
    print("\nBy trip duration:")
    for days in sorted(residual_patterns['by_days'].keys())[:10]:
        residuals_list = residual_patterns['by_days'][days]
        if len(residuals_list) >= 5:
            avg_residual = statistics.mean(residuals_list)
            print(f"  {days:2d} days: avg residual = ${avg_residual:6.2f} ({len(residuals_list)} cases)")
    
    print("\nBy miles range:")
    for miles_range in sorted(residual_patterns['by_miles_range'].keys())[:10]:
        residuals_list = residual_patterns['by_miles_range'][miles_range]
        if len(residuals_list) >= 5:
            avg_residual = statistics.mean(residuals_list)
            print(f"  {miles_range:3.0f}-{miles_range+99:3.0f} miles: avg residual = ${avg_residual:6.2f} ({len(residuals_list)} cases)")
    
    # 5. TEST COMPLETELY DIFFERENT APPROACHES
    print("\n5. TESTING RADICALLY DIFFERENT APPROACHES")
    print("-" * 45)
    
    # Test if it's based on total trip "cost" or "value"
    total_values = []
    for case in data[:100]:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Calculate different "total trip value" metrics
        trip_values = {
            'simple_sum': days + miles + receipts,
            'weighted_sum': days * 100 + miles + receipts,
            'complex_sum': days * 50 + miles * 2 + receipts * 1.5,
            'log_based': days * 100 + math.log(miles + 1) * 50 + math.log(receipts + 1) * 30,
        }
        
        for approach, value in trip_values.items():
            ratio = output / value if value > 0 else 0
            total_values.append((approach, ratio, case))
    
    # Check if any approach gives consistent ratios
    approach_ratios = defaultdict(list)
    for approach, ratio, case in total_values:
        approach_ratios[approach].append(ratio)
    
    print("Testing different 'total trip value' approaches:")
    for approach, ratios in approach_ratios.items():
        std_dev = statistics.stdev(ratios) if len(ratios) > 1 else 0
        avg_ratio = statistics.mean(ratios)
        print(f"  {approach:15s}: avg ratio = {avg_ratio:.4f}, std = {std_dev:.4f}")
    
    # 6. FINAL INSIGHT CHECK
    print("\n6. FINAL INSIGHT CHECK")
    print("-" * 25)
    
    # What if the formula is much simpler than we think?
    simple_tests = []
    for case in data[:50]:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled'] 
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Test very simple relationships
        tests = {
            'pure_linear': days * 75 + miles * 0.3 + receipts * 0.4,
            'receipt_heavy': days * 50 + miles * 0.2 + receipts * 0.8,
            'mile_heavy': days * 80 + miles * 0.8 + receipts * 0.2,
            'sqrt_receipts_v2': days * 90 + miles * 0.4 + math.sqrt(receipts) * 15,
            'log_everything': days * 50 + math.log(miles + 1) * 30 + math.log(receipts + 1) * 40,
        }
        
        for test_name, prediction in tests.items():
            error = abs(output - prediction)
            simple_tests.append((test_name, error))
    
    # Average errors for simple tests
    test_errors = defaultdict(list)
    for test_name, error in simple_tests:
        test_errors[test_name].append(error)
    
    print("Simple formula tests (avg error on 50 cases):")
    for test_name, errors in test_errors.items():
        avg_error = statistics.mean(errors)
        print(f"  {test_name:20s}: ${avg_error:6.2f}")

if __name__ == "__main__":
    hunt_for_missing_patterns() 