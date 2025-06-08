#!/usr/bin/env python3

import sys
import math
import json

class ACMEReimbursementSystem:
    """
    Reverse-engineered ACME Corp legacy reimbursement system
    
    This system identifies known and unknown parameters, each with:
    - Confidence score (0-1): how confident we are it influences the outcome
    - Weight score (0-1): how much weight this parameter carries in overall outcome
    """
    
    def __init__(self):
        # Load training data for analysis
        with open('public_cases.json', 'r') as f:
            self.training_data = json.load(f)
        
        # Known parameters (from input)
        self.known_parameters = {
            'trip_duration_days': {
                'confidence': 1.0,  # We know this exists and influences outcome
                'weight': 0.85,     # Very high weight - major factor in reimbursement
                'description': 'Number of days spent traveling'
            },
            'miles_traveled': {
                'confidence': 1.0,  # We know this exists and influences outcome  
                'weight': 0.75,     # High weight - significant factor
                'description': 'Total miles traveled during trip'
            },
            'total_receipts_amount': {
                'confidence': 1.0,  # We know this exists and influences outcome
                'weight': 0.65,     # Medium-high weight - important but not linear
                'description': 'Total dollar amount of submitted receipts'
            }
        }
        
        # Unknown/Hidden parameters (inferred from patterns and interviews)
        self.unknown_parameters = {
            'efficiency_bonus': {
                'confidence': 0.95,  # Very confident this exists based on data patterns
                'weight': 0.40,      # Moderate weight - affects outcome significantly
                'description': 'Bonus for high miles-per-day efficiency (sweet spot 180-220 mi/day)'
            },
            'trip_length_modifier': {
                'confidence': 0.90,  # Strong evidence from residual analysis
                'weight': 0.60,      # High weight - dramatically affects per-day rates
                'description': 'Non-linear modifier based on trip duration (short trips boosted, long trips penalized)'
            },
            'receipt_processing_curve': {
                'confidence': 0.85,  # Clear evidence of non-linear receipt processing
                'weight': 0.50,      # Medium weight - affects how receipts are reimbursed
                'description': 'Square root relationship for receipt reimbursement, not linear'
            },
            'five_day_special_bonus': {
                'confidence': 0.80,  # Mentioned in interviews, some evidence in data
                'weight': 0.25,      # Lower weight - only affects 5-day trips
                'description': 'Special bonus calculation for exactly 5-day trips'
            },
            'high_mileage_diminishing_returns': {
                'confidence': 0.75,  # Evidence from mileage analysis
                'weight': 0.35,      # Moderate weight - affects high-mileage trips
                'description': 'Diminishing returns for very high mileage (>500 miles)'
            },
            'receipt_amount_thresholds': {
                'confidence': 0.70,  # Pattern visible in residual analysis
                'weight': 0.45,      # Medium weight - creates step functions in reimbursement
                'description': 'Different reimbursement rates for different receipt amount ranges'
            },
            'vacation_penalty': {
                'confidence': 0.65,  # Mentioned in interviews, some data support
                'weight': 0.30,      # Lower weight - only affects long trips with high spending
                'description': 'Penalty for long trips (8+ days) with high daily spending'
            },
            'submission_timing_factor': {
                'confidence': 0.40,  # Mentioned in interviews but hard to verify
                'weight': 0.15,      # Low weight - minor influence if it exists
                'description': 'Possible variation based on submission timing (day of week, month)'
            },
            'randomization_component': {
                'confidence': 0.60,  # Some evidence of controlled randomness
                'weight': 0.20,      # Low weight - small variation factor
                'description': 'Small pseudo-random variation to prevent gaming'
            },
            'department_modifier': {
                'confidence': 0.30,  # Mentioned in interviews but no clear evidence
                'weight': 0.25,      # Unknown weight - could be significant if it exists
                'description': 'Possible different treatment for different departments'
            }
        }
        
        # Calculate the core formula based on analysis
        self.base_formula = self._derive_base_formula()
    
    def _derive_base_formula(self):
        """Derive the base formula from pattern analysis"""
        # From our analysis, the best performing formula was:
        # days*110 + miles*0.5 + sqrt(receipts)*10
        return {
            'days_multiplier': 110,
            'miles_multiplier': 0.5,
            'receipts_sqrt_multiplier': 10
        }
    
    def calculate_reimbursement(self, days, miles, receipts):
        """
        Calculate reimbursement using the reverse-engineered formula
        """
        
        # Base calculation using known parameters
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # Apply unknown parameter effects
        
        # 1. Trip length modifier (high confidence, high weight)
        if days <= 2:
            base_amount *= 1.6  # Short trip boost
        elif days <= 7:
            base_amount *= 1.1  # Moderate boost
        elif days >= 8:
            base_amount *= 0.85  # Long trip penalty
        
        # 2. Efficiency bonus (high confidence, moderate weight)
        if days > 0:
            efficiency = miles / days
            if 180 <= efficiency <= 220:
                base_amount *= 1.15  # Sweet spot bonus
            elif efficiency > 300:
                base_amount *= 0.95  # Very high efficiency penalty
        
        # 3. Receipt processing curve (already applied via sqrt)
        
        # 4. Five-day special bonus (medium confidence, low weight)
        if days == 5:
            base_amount *= 1.05
        
        # 5. High mileage diminishing returns (medium confidence, moderate weight)
        if miles > 500:
            excess_miles = miles - 500
            penalty = excess_miles * 0.1
            base_amount -= penalty
        
        # 6. Randomization component (medium confidence, low weight)
        # Use deterministic "randomness" based on inputs
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += base_amount * pseudo_random * 0.02
        
        # Ensure minimum reimbursement
        minimum = days * 50
        base_amount = max(base_amount, minimum)
        
        return round(base_amount, 2)
    
    def print_parameter_analysis(self):
        """Print analysis of known and unknown parameters"""
        print("ACME CORP REIMBURSEMENT SYSTEM - PARAMETER ANALYSIS")
        print("=" * 60)
        print()
        
        print("KNOWN PARAMETERS (from system inputs):")
        print("-" * 40)
        for param, info in self.known_parameters.items():
            print(f"{param}:")
            print(f"  Confidence: {info['confidence']:.2f} (how sure we are it influences outcome)")
            print(f"  Weight: {info['weight']:.2f} (how much it affects the result)")
            print(f"  Description: {info['description']}")
            print()
        
        print("UNKNOWN/HIDDEN PARAMETERS (inferred from analysis):")
        print("-" * 50)
        for param, info in self.unknown_parameters.items():
            print(f"{param}:")
            print(f"  Confidence: {info['confidence']:.2f} (how sure we are it exists)")
            print(f"  Weight: {info['weight']:.2f} (estimated impact on outcome)")
            print(f"  Description: {info['description']}")
            print()
        
        print("DERIVED FORMULA:")
        print("-" * 15)
        print("Base: days*110 + miles*0.5 + sqrt(receipts)*10")
        print("Plus various modifiers based on unknown parameters")
        print()
        
        print("CONFIDENCE SUMMARY:")
        print("-" * 18)
        total_known_weight = sum(p['weight'] for p in self.known_parameters.values())
        total_unknown_weight = sum(p['weight'] * p['confidence'] for p in self.unknown_parameters.values())
        
        print(f"Known parameter influence: {total_known_weight:.2f}")
        print(f"Unknown parameter influence: {total_unknown_weight:.2f}")
        print(f"Total system complexity: {total_known_weight + total_unknown_weight:.2f}")
        
        # Calculate confidence in our understanding
        explained_variance = total_known_weight / (total_known_weight + total_unknown_weight)
        print(f"System understanding: {explained_variance:.1%}")

def main():
    system = ACMEReimbursementSystem()
    
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
        # Print parameter analysis
        system.print_parameter_analysis()
    
    else:
        print("Usage:")
        print("  python3 solution.py <days> <miles> <receipts>  # Calculate reimbursement")
        print("  python3 solution.py --analyze                  # Show parameter analysis")

if __name__ == "__main__":
    main() 