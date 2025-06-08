#!/usr/bin/env python3

import math

def debug_case(days, miles, receipts, expected, case_name):
    print(f"\n=== {case_name} ===")
    print(f"Input: {days}d, {miles}mi, ${receipts:.2f}")
    print(f"Expected: ${expected:.2f}")
    
    # Base calculation
    base_amount = (days * 110 + miles * 0.5 + math.sqrt(max(receipts, 0)) * 10)
    print(f"Base formula: {days}*110 + {miles}*0.5 + sqrt({receipts:.2f})*10 = ${base_amount:.2f}")
    
    # Trip length modifier
    original_base = base_amount
    if days <= 2:
        base_amount *= 1.6
        print(f"Short trip boost (1.6x): ${original_base:.2f} -> ${base_amount:.2f}")
    elif days <= 7:
        base_amount *= 1.1
        print(f"Medium trip boost (1.1x): ${original_base:.2f} -> ${base_amount:.2f}")
    elif days >= 8:
        base_amount *= 0.85
        print(f"Long trip penalty (0.85x): ${original_base:.2f} -> ${base_amount:.2f}")
    
    # Efficiency bonus
    efficiency = miles / days if days > 0 else 0
    print(f"Efficiency: {efficiency:.1f} mi/day")
    original_after_trip = base_amount
    if 180 <= efficiency <= 220:
        base_amount *= 1.15
        print(f"Efficiency bonus (1.15x): ${original_after_trip:.2f} -> ${base_amount:.2f}")
    elif 100 <= efficiency <= 180:
        base_amount *= 1.05
        print(f"Efficiency bonus (1.05x): ${original_after_trip:.2f} -> ${base_amount:.2f}")
    
    # Five-day special bonus
    if days == 5:
        original_after_eff = base_amount
        base_amount *= 1.05
        print(f"Five-day bonus (1.05x): ${original_after_eff:.2f} -> ${base_amount:.2f}")
    
    # High mileage diminishing returns
    if miles > 500:
        excess_miles = miles - 500
        penalty = excess_miles * 0.05
        original_before_penalty = base_amount
        base_amount -= penalty
        print(f"High mileage penalty: -{excess_miles}*0.05 = -${penalty:.2f}")
        print(f"After penalty: ${original_before_penalty:.2f} -> ${base_amount:.2f}")
    
    # Randomization component
    pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
    random_amount = base_amount * pseudo_random * 0.02
    original_before_random = base_amount
    base_amount += random_amount
    print(f"Randomization: +${random_amount:.2f}")
    print(f"After randomization: ${original_before_random:.2f} -> ${base_amount:.2f}")
    
    # Minimum reimbursement
    minimum = days * 50
    if base_amount < minimum:
        print(f"Minimum adjustment: ${base_amount:.2f} -> ${minimum:.2f}")
        base_amount = minimum
    
    final_prediction = round(base_amount, 2)
    error = abs(expected - final_prediction)
    
    print(f"Final prediction: ${final_prediction:.2f}")
    print(f"Error: ${error:.2f}")
    print(f"Error ratio: {final_prediction/expected:.2f}x")

# Test the problematic cases
debug_case(14, 481, 939.99, 877.17, "Case 520")
debug_case(2, 384, 495.49, 290.36, "Case 89")
debug_case(5, 516, 1878.49, 669.85, "Case 711") 