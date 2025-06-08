#!/usr/bin/env python3

import sys
import math
import json

class FinalACMEReimbursementSystem:
    """
    Final ACME Corp reimbursement system:
    - Uses breakthrough coefficients: days*90 + miles*0.4 + sqrt(receipts)*15
    - Applies systematic corrections based on residual analysis
    - Minimal business logic to avoid over-fitting
    """
    
    def __init__(self):
        # BREAKTHROUGH base formula coefficients
        self.base_formula = {
            'days_multiplier': 90,
            'miles_multiplier': 0.4,
            'receipts_sqrt_multiplier': 15
        }
        
        # SYSTEMATIC CORRECTIONS based on residual analysis
        self.duration_corrections = {
            1: -33,     # 1-day trips: reduce by $33
            2: -17,     # 2-day trips: reduce by $17
            3: +67,     # 3-day trips: add $67
            4: +94,     # 4-day trips: add $94
            5: +47,     # 5-day trips: add $47
            6: +80,     # 6-day trips: add $80
            7: +89,     # 7-day trips: add $89
            8: +34,     # 8-day trips: add $34
            9: -32,     # 9-day trips: reduce by $32
            10: -69,    # 10-day trips: reduce by $69
            11: -89,    # 11-day trips: reduce by $89
            12: -135,   # 12-day trips: reduce by $135
            13: -150,   # 13-day trips: reduce by $150
            14: -223    # 14-day trips: reduce by $223
        }
        
        # Receipt bracket corrections
        self.receipt_corrections = [
            (0, 500, -230),      # $0-500: reduce by $230
            (500, 1000, -71),    # $500-1000: reduce by $71
            (1000, 1500, +190),  # $1000-1500: add $190
            (1500, 2000, +111),  # $1500-2000: add $111
        ]
    
    def get_duration_correction(self, days):
        """Get systematic correction for trip duration"""
        if days in self.duration_corrections:
            return self.duration_corrections[days]
        elif days > 14:
            # Extrapolate for very long trips
            return -223 - (days - 14) * 20
        else:
            return 0
    
    def get_receipt_correction(self, receipts):
        """Get systematic correction for receipt amount"""
        for min_amt, max_amt, correction in self.receipt_corrections:
            if min_amt <= receipts < max_amt:
                return correction
        return 0  # No correction for very high receipts
    
    def calculate_reimbursement(self, days, miles, receipts, show_debug=False):
        """
        Final calculation with systematic corrections
        """
        
        # Base calculation (BREAKTHROUGH coefficients)
        base_amount = (days * self.base_formula['days_multiplier'] + 
                      miles * self.base_formula['miles_multiplier'] + 
                      math.sqrt(max(receipts, 0)) * self.base_formula['receipts_sqrt_multiplier'])
        
        # SYSTEMATIC CORRECTIONS (the key insight!)
        duration_correction = self.get_duration_correction(days)
        receipt_correction = self.get_receipt_correction(receipts)
        
        base_amount += duration_correction
        base_amount += receipt_correction
        
        if show_debug:
            print(f"Base: ${base_amount - duration_correction - receipt_correction:.2f}")
            print(f"Duration correction ({days}d): {duration_correction:+.0f}")
            print(f"Receipt correction (${receipts:.0f}): {receipt_correction:+.0f}")
        
        # MINIMAL business logic (much reduced to avoid over-fitting)
        
        # Light efficiency bonus (only for extreme efficiency)
        efficiency = miles / days if days > 0 else 0
        if 200 <= efficiency <= 250:  # Very narrow sweet spot
            base_amount += 25  # Small additive bonus
        
        # Very light randomization (reduced impact)
        pseudo_random = ((days * 7 + int(miles) * 3 + int(receipts * 100)) % 100) / 1000
        base_amount += pseudo_random * 5  # Much smaller random component
        
        # Ensure reasonable minimum
        minimum = days * 35
        base_amount = max(base_amount, minimum)
        
        return round(base_amount, 2)

def main():
    system = FinalACMEReimbursementSystem()
    
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
        print("  python3 solution_v7_final.py <days> <miles> <receipts>")

if __name__ == "__main__":
    main() 