#!/usr/bin/env python3

import sys
import math
import json

class OptimizedACMEReimbursementSystem:
    """
    Optimized ACME Corp reimbursement system:
    - Uses adjusted base formula to reduce over-prediction
    - Keeps proven business logic modifiers
    - Maintains selective fraud detection for extreme cases
    """
    
    def __init__(self):
        # Load training data for analysis
        with open('public_cases.json', 'r') as f:
            self.training_data = json.load(f)
        
        # ADJUSTED base formula coefficients (reduced to prevent over-prediction)
        self.base_formula = {
            'days_multiplier': 85,      # Reduced from 110
            'miles_multiplier': 0.4,    # Reduced from 0.5  
            'receipts_sqrt_multiplier': 8  # Reduced from 10
        }
        
        # Conservative fraud thresholds (unchanged - only for extreme cases)
        self.extreme_thresholds = {
            'impossible_miles_per_day': 1000,      # Truly impossible
            'impossible_daily_spending': 500,      # Extremely excessive
            'extreme_single_day_miles': 800,       # Impossible for 1 day
            'extreme_combination_miles': 1200,     # Impossible mileage
            'extreme_combination_receipts': 2000   # Impossible receipts
        }
    
    def is_extreme_outlier(self, days, miles, receipts):
        """Check if case is an extreme outlier requiring fraud detection"""
        
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        # Only flag truly impossible cases
        extreme_flags = []
        
        # 1. Physically impossible travel
        if miles_per_day > self.extreme_thresholds['impossible_miles_per_day']:
            extreme_flags.append('impossible_travel')
        
        # 2. Impossible daily spending
        if receipts_per_day > self.extreme_thresholds['impossible_daily_spending']:
            extreme_flags.append('impossible_spending')
        
        # 3. Single day impossibility
        if days == 1 and miles > self.extreme_thresholds['extreme_single_day_miles']:
            extreme_flags.append('single_day_impossible')
        
        # 4. Extreme combination
        if (miles > self.extreme_thresholds['extreme_combination_miles'] and 
            receipts > self.extreme_thresholds['extreme_combination_receipts']):
            extreme_flags.append('extreme_combination')
        
        return len(extreme_flags) > 0, extreme_flags
    
    def apply_selective_fraud_penalty(self, base_amount, days, miles, receipts, flags):
        """Apply conservative fraud penalties only to extreme outliers"""
        
        penalty_factor = 1.0
        
        # Light penalties for truly impossible cases
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
        Optimized calculation with adjusted coefficients
        """
        
        # Base calculation (ADJUSTED coefficients)
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # Apply business logic modifiers (ADJUSTED multipliers)
        
        # 1. Trip length modifier (REDUCED impact)
        if days <= 2:
            base_amount *= 1.4    # Reduced from 1.6
        elif days <= 7:
            base_amount *= 1.05   # Reduced from 1.1
        elif days >= 8:
            base_amount *= 0.9    # Less penalty from 0.85
        
        # 2. Efficiency bonus (KEPT - working well)
        efficiency = miles / days if days > 0 else 0
        if 180 <= efficiency <= 220:
            base_amount *= 1.1    # Reduced from 1.15
        elif 100 <= efficiency <= 180:
            base_amount *= 1.03   # Reduced from 1.05
        
        # 3. Five-day special bonus (KEPT)
        if days == 5:
            base_amount *= 1.05
        
        # 4. High mileage diminishing returns (ADJUSTED)
        if miles > 500:
            excess_miles = miles - 500
            penalty = excess_miles * 0.03  # Reduced from 0.05
            base_amount -= penalty
        
        # 5. Randomization component (KEPT)
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.02
        
        # Selective fraud detection (unchanged)
        is_extreme, fraud_flags = self.is_extreme_outlier(days, miles, receipts)
        
        if is_extreme:
            base_amount = self.apply_selective_fraud_penalty(base_amount, days, miles, receipts, fraud_flags)
            
            if show_debug:
                print(f"Extreme outlier detected: {', '.join(fraud_flags)}")
        
        # Ensure minimum reimbursement
        minimum = days * 50
        base_amount = max(base_amount, minimum)
        
        return round(base_amount, 2)
    
    def analyze_approach(self):
        """Analyze the optimized approach on problematic cases"""
        
        print("OPTIMIZED APPROACH ANALYSIS")
        print("=" * 40)
        
        # Test on the high-error cases from eval.sh
        problem_cases = [
            (14, 481, 939.99, 877.17, "Case 520"),
            (2, 384, 495.49, 290.36, "Case 89"),
            (5, 516, 1878.49, 669.85, "Case 711"),
            (2, 1139, 306.43, 726.14, "Case 406"),
            (1, 1041, 1630.25, 1466.95, "Case 921")
        ]
        
        total_error = 0
        for days, miles, receipts, expected, case_name in problem_cases:
            is_extreme, flags = self.is_extreme_outlier(days, miles, receipts)
            our_prediction = self.calculate_reimbursement(days, miles, receipts, show_debug=True)
            error = abs(expected - our_prediction)
            total_error += error
            
            print(f"\n{case_name}: {days}d, {miles}mi, ${receipts:.2f}")
            print(f"  Expected: ${expected:.2f}")
            print(f"  Our Prediction: ${our_prediction:.2f}")
            print(f"  Error: ${error:.2f} (was ${error:.2f})")
            print(f"  Extreme Outlier: {is_extreme}")
            if flags:
                print(f"  Flags: {', '.join(flags)}")
        
        avg_error = total_error / len(problem_cases)
        print(f"\nAverage error on problem cases: ${avg_error:.2f}")

def main():
    system = OptimizedACMEReimbursementSystem()
    
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
    
    elif len(sys.argv) == 2 and sys.argv[1] == "--analyze":
        # Analyze approach
        system.analyze_approach()
    
    else:
        print("Usage:")
        print("  python3 solution_v4_optimized.py <days> <miles> <receipts>")
        print("  python3 solution_v4_optimized.py --analyze")

if __name__ == "__main__":
    main() 