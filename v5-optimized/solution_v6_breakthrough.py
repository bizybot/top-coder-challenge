#!/usr/bin/env python3

import sys
import math
import json

class BreakthroughACMEReimbursementSystem:
    """
    Breakthrough ACME Corp reimbursement system:
    - Uses discovered better coefficients: days*90 + miles*0.4 + sqrt(receipts)*15
    - Keeps essential business logic but reduced
    - Maintains minimal fraud detection
    """
    
    def __init__(self):
        # Load training data for analysis
        with open('public_cases.json', 'r') as f:
            self.training_data = json.load(f)
        
        # BREAKTHROUGH base formula coefficients (discovered from deep analysis)
        self.base_formula = {
            'days_multiplier': 90,      # Reduced from 110 to 90
            'miles_multiplier': 0.4,    # Reduced from 0.5 to 0.4
            'receipts_sqrt_multiplier': 15  # Increased from 10 to 15
        }
        
        # Minimal fraud thresholds (very lenient)
        self.extreme_thresholds = {
            'impossible_miles_per_day': 2000,      # Very high threshold
            'impossible_daily_spending': 1000,     # Very high threshold
            'extreme_single_day_miles': 1500,      # Very high threshold
            'extreme_combination_miles': 2000,     # Very high threshold
            'extreme_combination_receipts': 4000   # Very high threshold
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
        """Apply very light fraud penalties only to truly impossible cases"""
        
        penalty_factor = 1.0
        
        if 'impossible_travel' in flags:
            penalty_factor *= 0.8  # Lighter penalty
        
        if 'impossible_spending' in flags:
            penalty_factor *= 0.85  # Lighter penalty
        
        if 'single_day_impossible' in flags:
            penalty_factor *= 0.85  # Lighter penalty
        
        if 'extreme_combination' in flags:
            penalty_factor *= 0.8  # Lighter penalty
        
        return base_amount * penalty_factor
    
    def calculate_reimbursement(self, days, miles, receipts, show_debug=False):
        """
        Breakthrough calculation with discovered coefficients
        """
        
        # Base calculation (BREAKTHROUGH coefficients)
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # Minimal business logic modifiers (heavily reduced)
        
        # 1. Trip length modifier (MUCH lighter)
        if days <= 2:
            base_amount *= 1.2    # Much reduced from 1.5
        elif days <= 7:
            base_amount *= 1.02   # Much reduced from 1.08
        elif days >= 8:
            base_amount *= 0.95   # Much reduced penalty
        
        # 2. Efficiency bonus (very light)
        efficiency = miles / days if days > 0 else 0
        if 180 <= efficiency <= 220:
            base_amount *= 1.05   # Much reduced from 1.12
        elif 100 <= efficiency <= 180:
            base_amount *= 1.02   # Much reduced from 1.04
        
        # 3. Five-day special bonus (kept but smaller)
        if days == 5:
            base_amount *= 1.02   # Reduced from 1.05
        
        # 4. High mileage diminishing returns (much lighter)
        if miles > 600:  # Increased threshold
            excess_miles = miles - 600
            penalty = excess_miles * 0.02  # Much reduced penalty
            base_amount -= penalty
        
        # 5. Randomization component (kept minimal)
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.01  # Reduced randomization
        
        # Minimal fraud detection
        is_extreme, fraud_flags = self.is_extreme_outlier(days, miles, receipts)
        
        if is_extreme:
            base_amount = self.apply_selective_fraud_penalty(base_amount, days, miles, receipts, fraud_flags)
            
            if show_debug:
                print(f"Extreme outlier detected: {', '.join(fraud_flags)}")
        
        # Ensure minimum reimbursement
        minimum = days * 40  # Reduced minimum
        base_amount = max(base_amount, minimum)
        
        return round(base_amount, 2)

def main():
    system = BreakthroughACMEReimbursementSystem()
    
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
        print("  python3 solution_v6_breakthrough.py <days> <miles> <receipts>")

if __name__ == "__main__":
    main() 