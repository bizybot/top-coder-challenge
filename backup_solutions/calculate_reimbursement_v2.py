#!/usr/bin/env python3

import sys
import math

class ImprovedReimbursementCalculator:
    """
    Improved ACME Corp legacy reimbursement system replica
    Based on advanced pattern analysis of 1000 historical cases
    """
    
    def __init__(self):
        # Per-day rates that decrease with trip length (discovered pattern)
        self.per_day_rates = {
            1: 873.55,
            2: 523.12,
            3: 336.85,
            4: 304.49,
            5: 254.52,
            6: 227.75,
            7: 217.35,
            8: 180.33,
            9: 159.85,
            10: 149.61,
            11: 145.51,
            12: 134.62,
            13: 128.90,
            14: 121.93
        }
        
        # Mileage rate (from pattern analysis)
        self.mileage_rate = 0.5
        
        # Receipt processing uses square root (key discovery!)
        self.receipt_sqrt_multiplier = 10
        
    def get_per_day_rate(self, days):
        """Get the per-day rate based on trip duration"""
        if days in self.per_day_rates:
            return self.per_day_rates[days]
        elif days > 14:
            # Extrapolate for very long trips
            return max(100, 150 - (days - 14) * 2)
        else:
            # Interpolate for missing values
            return 200  # Fallback
    
    def calculate_reimbursement(self, days, miles, receipts):
        """Calculate reimbursement using the discovered formula"""
        
        # Base formula: days*rate + miles*0.5 + sqrt(receipts)*10
        per_day_rate = self.get_per_day_rate(days)
        
        # But the per_day_rate already includes some base amount
        # So we need to adjust the formula
        base_component = days * 110  # Base per diem
        mileage_component = miles * self.mileage_rate
        receipt_component = math.sqrt(max(receipts, 0)) * self.receipt_sqrt_multiplier
        
        total = base_component + mileage_component + receipt_component
        
        # Apply adjustments based on observed patterns
        
        # Adjustment for trip length efficiency
        if days == 1:
            # 1-day trips get a significant boost
            total *= 1.4
        elif days == 2:
            # 2-day trips get moderate boost
            total *= 1.05
        elif days >= 8:
            # Long trips get penalized
            penalty_factor = 1.0 - (days - 7) * 0.05
            total *= max(penalty_factor, 0.7)
        
        # High mileage adjustments
        if miles > 500:
            # High mileage gets bonus but with diminishing returns
            bonus = (miles - 500) * 0.2
            total += bonus
        
        # Receipt amount adjustments
        if receipts > 1000:
            # Very high receipts get diminishing returns
            excess = receipts - 1000
            penalty = math.sqrt(excess) * 5
            total -= penalty
        
        return round(total, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement_v2.py <days> <miles> <receipts>")
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])
        
        calculator = ImprovedReimbursementCalculator()
        reimbursement = calculator.calculate_reimbursement(days, miles, receipts)
        
        print(f"{reimbursement:.2f}")
        
    except ValueError as e:
        print(f"Error: Invalid input parameters - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 