#!/usr/bin/env python3

import sys
import math
import json

class EnhancedACMEReimbursementSystem:
    """
    Enhanced ACME Corp legacy reimbursement system replica
    Now includes fraud detection patterns discovered from outlier analysis
    """
    
    def __init__(self):
        # Load training data for analysis
        with open('public_cases.json', 'r') as f:
            self.training_data = json.load(f)
        
        # Original known parameters
        self.known_parameters = {
            'trip_duration_days': {'confidence': 1.0, 'weight': 0.85},
            'miles_traveled': {'confidence': 1.0, 'weight': 0.75},
            'total_receipts_amount': {'confidence': 1.0, 'weight': 0.65}
        }
        
        # Enhanced unknown parameters with fraud detection
        self.unknown_parameters = {
            # Original parameters
            'efficiency_bonus': {'confidence': 0.95, 'weight': 0.40},
            'trip_length_modifier': {'confidence': 0.90, 'weight': 0.60},
            'receipt_processing_curve': {'confidence': 0.85, 'weight': 0.50},
            'five_day_special_bonus': {'confidence': 0.80, 'weight': 0.25},
            
            # NEW: Fraud detection parameters
            'physical_impossibility_penalty': {'confidence': 0.90, 'weight': 0.80},
            'excessive_spending_penalty': {'confidence': 0.85, 'weight': 0.70},
            'vacation_pattern_penalty': {'confidence': 0.80, 'weight': 0.60},
            'extreme_combination_penalty': {'confidence': 0.75, 'weight': 0.65},
            'fraud_threshold_matrix': {'confidence': 0.70, 'weight': 0.55}
        }
        
        # Fraud detection thresholds
        self.fraud_thresholds = {
            'max_miles_per_day': 800,      # Physically impossible above this
            'max_daily_spending': 300,     # Excessive spending above this
            'min_efficiency_long_trip': 25, # Vacation pattern below this for 8+ days
            'extreme_mileage': 1000,       # Extreme mileage threshold
            'extreme_receipts': 1500       # Extreme receipts threshold
        }
        
        # Base formula (unchanged - still the best)
        self.base_formula = {
            'days_multiplier': 110,
            'miles_multiplier': 0.5,
            'receipts_sqrt_multiplier': 10
        }
    
    def detect_fraud_indicators(self, days, miles, receipts):
        """Detect potential fraud indicators and return penalty factors"""
        fraud_score = 0.0
        fraud_reasons = []
        
        # Calculate derived metrics
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        # 1. Physical impossibility check
        if miles_per_day > self.fraud_thresholds['max_miles_per_day']:
            severity = min((miles_per_day - self.fraud_thresholds['max_miles_per_day']) / 200, 2.0)
            fraud_score += 0.6 * severity
            fraud_reasons.append(f"Physical impossibility: {miles_per_day:.1f} mi/day")
        
        # 2. Excessive spending check
        if receipts_per_day > self.fraud_thresholds['max_daily_spending']:
            severity = min((receipts_per_day - self.fraud_thresholds['max_daily_spending']) / 100, 1.5)
            fraud_score += 0.4 * severity
            fraud_reasons.append(f"Excessive spending: ${receipts_per_day:.2f}/day")
        
        # 3. Vacation pattern (long trip, minimal travel)
        if days >= 8 and miles_per_day < self.fraud_thresholds['min_efficiency_long_trip']:
            fraud_score += 0.3
            fraud_reasons.append(f"Vacation pattern: {days} days, {miles_per_day:.1f} mi/day")
        
        # 4. Extreme combination penalties
        if (miles > self.fraud_thresholds['extreme_mileage'] and 
            receipts > self.fraud_thresholds['extreme_receipts']):
            fraud_score += 0.5
            fraud_reasons.append(f"Extreme combination: {miles} mi, ${receipts:.2f}")
        
        # 5. Single-day impossibility (special case)
        if days == 1 and miles > 600:
            fraud_score += 0.4
            fraud_reasons.append(f"Single-day high mileage: {miles} mi")
        
        # 6. Luxury spending patterns
        if receipts_per_day > 200 and days <= 3:
            fraud_score += 0.3
            fraud_reasons.append(f"Luxury spending: ${receipts_per_day:.2f}/day on short trip")
        
        return fraud_score, fraud_reasons
    
    def apply_fraud_penalties(self, base_amount, fraud_score, fraud_reasons):
        """Apply fraud penalties based on detected patterns"""
        
        if fraud_score <= 0.1:
            return base_amount  # No fraud detected
        
        # Progressive penalty system
        if fraud_score >= 1.5:
            # Severe fraud: 60-80% reduction
            penalty_factor = 0.2 + (0.2 * max(0, (2.0 - fraud_score)))
        elif fraud_score >= 1.0:
            # Moderate fraud: 40-60% reduction  
            penalty_factor = 0.4 + (0.2 * (1.5 - fraud_score))
        elif fraud_score >= 0.5:
            # Light fraud: 20-40% reduction
            penalty_factor = 0.6 + (0.2 * (1.0 - fraud_score))
        else:
            # Minor flags: 5-20% reduction
            penalty_factor = 0.8 + (0.2 * (0.5 - fraud_score))
        
        penalized_amount = base_amount * penalty_factor
        
        return penalized_amount
    
    def calculate_reimbursement(self, days, miles, receipts, show_debug=False):
        """
        Enhanced calculation with fraud detection
        """
        
        # Base calculation (our proven formula)
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # Apply original business logic modifiers
        
        # 1. Trip length modifier
        if days <= 2:
            base_amount *= 1.6
        elif days <= 7:
            base_amount *= 1.1
        elif days >= 8:
            base_amount *= 0.85
        
        # 2. Efficiency bonus (for legitimate cases)
        efficiency = miles / days if days > 0 else 0
        if 180 <= efficiency <= 220:
            base_amount *= 1.15
        elif 100 <= efficiency <= 180:
            base_amount *= 1.05
        
        # 3. Five-day special bonus
        if days == 5:
            base_amount *= 1.05
        
        # 4. High mileage diminishing returns (for legitimate cases)
        if miles > 500 and efficiency < 400:  # Only if not flagged as impossible
            excess_miles = miles - 500
            penalty = excess_miles * 0.05
            base_amount -= penalty
        
        # NEW: Fraud detection and penalties
        fraud_score, fraud_reasons = self.detect_fraud_indicators(days, miles, receipts)
        
        if fraud_score > 0:
            base_amount = self.apply_fraud_penalties(base_amount, fraud_score, fraud_reasons)
            
            if show_debug:
                print(f"Fraud detected (score: {fraud_score:.2f}): {', '.join(fraud_reasons)}")
        
        # Randomization component (but not for flagged cases)
        if fraud_score < 0.3:
            pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
            base_amount += base_amount * pseudo_random * 0.02
        
        # Ensure minimum reimbursement
        minimum = days * 50
        base_amount = max(base_amount, minimum)
        
        return round(base_amount, 2)
    
    def analyze_outliers(self):
        """Analyze the outlier cases that were causing high errors"""
        
        outlier_cases = [
            (1, 1082, 1809.49, 446.94, "Case 996"),
            (14, 481, 939.99, 877.17, "Case 520"), 
            (2, 384, 495.49, 290.36, "Case 89"),
            (8, 1025, 1031.33, 2214.64, "Case 513"),
            (5, 516, 1878.49, 669.85, "Case 711")
        ]
        
        print("OUTLIER ANALYSIS WITH FRAUD DETECTION")
        print("=" * 50)
        
        for days, miles, receipts, expected, case_name in outlier_cases:
            our_prediction = self.calculate_reimbursement(days, miles, receipts, show_debug=True)
            original_error = abs(expected - our_prediction)
            
            fraud_score, fraud_reasons = self.detect_fraud_indicators(days, miles, receipts)
            
            print(f"\n{case_name}: {days}d, {miles}mi, ${receipts:.2f}")
            print(f"  Expected: ${expected:.2f}")
            print(f"  Our Prediction: ${our_prediction:.2f}")
            print(f"  Error: ${original_error:.2f}")
            print(f"  Fraud Score: {fraud_score:.2f}")
            if fraud_reasons:
                print(f"  Fraud Indicators: {', '.join(fraud_reasons)}")

def main():
    system = EnhancedACMEReimbursementSystem()
    
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
    
    elif len(sys.argv) == 2 and sys.argv[1] == "--analyze-outliers":
        # Analyze outlier cases
        system.analyze_outliers()
    
    else:
        print("Usage:")
        print("  python3 solution_v2_fraud_aware.py <days> <miles> <receipts>")
        print("  python3 solution_v2_fraud_aware.py --analyze-outliers")

if __name__ == "__main__":
    main() 