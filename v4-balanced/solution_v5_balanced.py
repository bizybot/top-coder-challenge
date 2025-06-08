#!/usr/bin/env python3

import sys
import math
import json

class BalancedACMEReimbursementSystem:
    """
    Balanced ACME Corp reimbursement system:
    - Uses slightly adjusted coefficients to reduce extreme errors
    - Keeps most of the proven formula intact
    - Maintains selective fraud detection
    """
    
    def __init__(self):
        # Load training data for analysis
        with open('public_cases.json', 'r') as f:
            self.training_data = json.load(f)
        
        # SLIGHTLY adjusted base formula coefficients
        self.base_formula = {
            'days_multiplier': 100,     # Reduced slightly from 110
            'miles_multiplier': 0.45,   # Reduced slightly from 0.5  
            'receipts_sqrt_multiplier': 9  # Reduced slightly from 10
        }
        
        # Conservative fraud thresholds (only for extreme cases)
        self.extreme_thresholds = {
            'impossible_miles_per_day': 1000,
            'impossible_daily_spending': 500,
            'extreme_single_day_miles': 800,
            'extreme_combination_miles': 1200,
            'extreme_combination_receipts': 2000
        }
    
    def is_extreme_outlier(self, days, miles, receipts):
        """Check if case is an extreme outlier requiring fraud detection"""
        
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        extreme_flags = []
        
        if miles_per_day > self.extreme_thresholds['impossible_miles_per_day']:
            extreme_flags.append('impossible_travel')
        
        if receipts_per_day > self.extreme_thresholds['impossible_daily_spending']:
            extreme_flags.append('impossible_spending')
        
        if days == 1 and miles > self.extreme_thresholds['extreme_single_day_miles']:
            extreme_flags.append('single_day_impossible')
        
        if (miles > self.extreme_thresholds['extreme_combination_miles'] and 
            receipts > self.extreme_thresholds['extreme_combination_receipts']):
            extreme_flags.append('extreme_combination')
        
        return len(extreme_flags) > 0, extreme_flags
    
    def apply_selective_fraud_penalty(self, base_amount, days, miles, receipts, flags):
        """Apply conservative fraud penalties only to extreme outliers"""
        
        penalty_factor = 1.0
        
        if 'impossible_travel' in flags:
            penalty_factor *= 0.7
        
        if 'impossible_spending' in flags:
            penalty_factor *= 0.8
        
        if 'single_day_impossible' in flags:
            penalty_factor *= 0.75
        
        if 'extreme_combination' in flags:
            penalty_factor *= 0.75
        
        return base_amount * penalty_factor
    
    def calculate_reimbursement(self, days, miles, receipts, show_debug=False):
        """
        Balanced calculation with minor adjustments
        """
        
        # Base calculation (SLIGHTLY adjusted coefficients)
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # Apply business logic modifiers (SLIGHTLY adjusted multipliers)
        
        # 1. Trip length modifier (minor adjustments)
        if days <= 2:
            base_amount *= 1.5    # Reduced from 1.6
        elif days <= 7:
            base_amount *= 1.08   # Reduced from 1.1
        elif days >= 8:
            base_amount *= 0.87   # Less penalty from 0.85
        
        # 2. Efficiency bonus (slightly adjusted)
        efficiency = miles / days if days > 0 else 0
        if 180 <= efficiency <= 220:
            base_amount *= 1.12   # Reduced from 1.15
        elif 100 <= efficiency <= 180:
            base_amount *= 1.04   # Reduced from 1.05
        
        # 3. Five-day special bonus (kept)
        if days == 5:
            base_amount *= 1.05
        
        # 4. High mileage diminishing returns (slightly adjusted)
        if miles > 500:
            excess_miles = miles - 500
            penalty = excess_miles * 0.04  # Reduced from 0.05
            base_amount -= penalty
        
        # 5. Randomization component (kept)
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.02
        
        # Selective fraud detection
        is_extreme, fraud_flags = self.is_extreme_outlier(days, miles, receipts)
        
        if is_extreme:
            base_amount = self.apply_selective_fraud_penalty(base_amount, days, miles, receipts, fraud_flags)
            
            if show_debug:
                print(f"Extreme outlier detected: {', '.join(fraud_flags)}")
        
        # Ensure minimum reimbursement
        minimum = days * 50
        base_amount = max(base_amount, minimum)
        
        return round(base_amount, 2)

def main():
    system = BalancedACMEReimbursementSystem()
    
    if len(sys.argv) == 4:
        # Calculate reimbursement
        try:
            days = int(sys.argv[1])
            miles = float(sys.argv[2])
            receipts = float(sys.argv[3])
            
            result = system.calculate_reimbursement(days, miles, receipts)
            print(f"{result:.2f}")
            
        except ValueError as e:
            print(f"Error: Invalid input parameters - {e}")
            sys.exit(1)
    
    else:
        print("Usage:")
        print("  python3 solution_v5_balanced.py <days> <miles> <receipts>")

if __name__ == "__main__":
    main() 