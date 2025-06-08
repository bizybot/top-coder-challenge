#!/usr/bin/env python3

import sys
import math
import json

class HybridACMEReimbursementSystem:
    """
    Hybrid ACME Corp reimbursement system:
    - Uses proven base formula for most cases
    - Applies selective fraud detection only for extreme outliers
    - Maintains high accuracy while handling suspicious patterns
    """
    
    def __init__(self):
        # Load training data for analysis
        with open('public_cases.json', 'r') as f:
            self.training_data = json.load(f)
        
        # Known parameters (unchanged)
        self.known_parameters = {
            'trip_duration_days': {'confidence': 1.0, 'weight': 0.85},
            'miles_traveled': {'confidence': 1.0, 'weight': 0.75},
            'total_receipts_amount': {'confidence': 1.0, 'weight': 0.65}
        }
        
        # Enhanced unknown parameters
        self.unknown_parameters = {
            # Original business logic
            'efficiency_bonus': {'confidence': 0.95, 'weight': 0.40},
            'trip_length_modifier': {'confidence': 0.90, 'weight': 0.60},
            'receipt_processing_curve': {'confidence': 0.85, 'weight': 0.50},
            'five_day_special_bonus': {'confidence': 0.80, 'weight': 0.25},
            
            # Selective fraud detection (only for extreme cases)
            'extreme_outlier_penalty': {'confidence': 0.85, 'weight': 0.70},
            'physical_impossibility_cap': {'confidence': 0.90, 'weight': 0.80},
        }
        
        # Base formula coefficients
        self.base_formula = {
            'days_multiplier': 110,
            'miles_multiplier': 0.5,
            'receipts_sqrt_multiplier': 10
        }
        
        # Conservative fraud thresholds (only for extreme cases)
        self.extreme_thresholds = {
            'impossible_miles_per_day': 1500,      # Increased from 1000 - more lenient
            'impossible_daily_spending': 800,      # Increased from 500 - more lenient
            'extreme_single_day_miles': 1200,      # Increased from 800 - more lenient
            'extreme_combination_miles': 1500,     # Increased from 1200 - more lenient
            'extreme_combination_receipts': 3000   # Increased from 2000 - more lenient
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
        
        # Calculate severity based on how extreme the case is
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        penalty_factor = 1.0
        
        # Light penalties for truly impossible cases
        if 'impossible_travel' in flags:
            # Cap at reasonable travel amount
            penalty_factor *= 0.7
        
        if 'impossible_spending' in flags:
            # Moderate penalty for excessive spending
            penalty_factor *= 0.8
        
        if 'single_day_impossible' in flags:
            # Light penalty for single-day impossibility
            penalty_factor *= 0.75
        
        if 'extreme_combination' in flags:
            # Moderate penalty for extreme combinations
            penalty_factor *= 0.75
        
        return base_amount * penalty_factor
    
    def calculate_reimbursement(self, days, miles, receipts, show_debug=False):
        """
        Hybrid calculation: proven formula + selective fraud detection
        """
        
        # Base calculation (our proven formula)
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # Apply business logic modifiers (unchanged)
        
        # 1. Trip length modifier
        if days <= 2:
            base_amount *= 1.6
        elif days <= 7:
            base_amount *= 1.1
        elif days >= 8:
            base_amount *= 0.85
        
        # 2. Efficiency bonus
        efficiency = miles / days if days > 0 else 0
        if 180 <= efficiency <= 220:
            base_amount *= 1.15
        elif 100 <= efficiency <= 180:
            base_amount *= 1.05
        
        # 3. Five-day special bonus
        if days == 5:
            base_amount *= 1.05
        
        # 4. High mileage diminishing returns
        if miles > 500:
            excess_miles = miles - 500
            penalty = excess_miles * 0.05
            base_amount -= penalty
        
        # 5. Randomization component
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.02
        
        # NEW: Selective fraud detection (only for extreme outliers)
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
        """Analyze the hybrid approach"""
        
        print("HYBRID APPROACH ANALYSIS")
        print("=" * 40)
        
        # Test on the outlier cases
        outlier_cases = [
            (1, 1082, 1809.49, 446.94, "Case 996"),
            (14, 481, 939.99, 877.17, "Case 520"), 
            (2, 384, 495.49, 290.36, "Case 89"),
            (8, 1025, 1031.33, 2214.64, "Case 513"),
            (5, 516, 1878.49, 669.85, "Case 711")
        ]
        
        for days, miles, receipts, expected, case_name in outlier_cases:
            is_extreme, flags = self.is_extreme_outlier(days, miles, receipts)
            our_prediction = self.calculate_reimbursement(days, miles, receipts, show_debug=True)
            error = abs(expected - our_prediction)
            
            print(f"\n{case_name}: {days}d, {miles}mi, ${receipts:.2f}")
            print(f"  Expected: ${expected:.2f}")
            print(f"  Our Prediction: ${our_prediction:.2f}")
            print(f"  Error: ${error:.2f}")
            print(f"  Extreme Outlier: {is_extreme}")
            if flags:
                print(f"  Flags: {', '.join(flags)}")
        
        # Count how many cases would be flagged
        flagged_count = 0
        total_cases = len(self.training_data)
        
        for case in self.training_data:
            days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            
            is_extreme, _ = self.is_extreme_outlier(days, miles, receipts)
            if is_extreme:
                flagged_count += 1
        
        print(f"\nSTATISTICS:")
        print(f"Total cases: {total_cases}")
        print(f"Flagged as extreme outliers: {flagged_count} ({flagged_count/total_cases*100:.1f}%)")
        print(f"Regular cases (use base formula): {total_cases - flagged_count} ({(total_cases-flagged_count)/total_cases*100:.1f}%)")

def main():
    system = HybridACMEReimbursementSystem()
    
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
        print("  python3 solution_v3_hybrid.py <days> <miles> <receipts>")
        print("  python3 solution_v3_hybrid.py --analyze")

if __name__ == "__main__":
    main() 