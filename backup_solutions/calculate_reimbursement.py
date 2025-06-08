#!/usr/bin/env python3

import sys
import math

class ReimbursementCalculator:
    """
    Reverse-engineered ACME Corp legacy reimbursement system
    Based on analysis of 1000 historical cases and employee interviews
    """
    
    def __init__(self):
        # Base per diem rates (discovered from minimum reimbursements)
        self.base_per_diem = {
            1: 117.24,
            2: 101.76, 
            3: 101.07,
            4: 80.50,
            5: 81.34,  # Special 5-day rate
            6: 87.10,
            7: 68.95,
            8: 67.94,
            9: 66.87,
            10: 77.46,
            11: 63.24,
            12: 65.75,
            13: 54.63,
            14: 61.91
        }
        
        # Mileage calculation parameters
        self.mileage_base_rate = 0.565
        self.mileage_tier_1_threshold = 100
        self.mileage_tier_2_threshold = 300
        self.mileage_tier_2_rate = 0.52
        self.mileage_tier_3_rate = 0.48
        
        # Efficiency bonus parameters (miles per day)
        self.efficiency_sweet_spot_min = 180
        self.efficiency_sweet_spot_max = 220
        self.efficiency_bonus_rate = 0.15
        
        # Receipt processing parameters
        self.receipt_penalty_threshold = 25
        self.receipt_optimal_min = 50
        self.receipt_optimal_max = 800
        self.receipt_diminishing_threshold = 600
        
    def calculate_base_reimbursement(self, days):
        """Calculate base per diem reimbursement"""
        if days in self.base_per_diem:
            return days * self.base_per_diem[days]
        else:
            # Interpolate for unusual durations
            avg_rate = sum(self.base_per_diem.values()) / len(self.base_per_diem)
            return days * avg_rate
    
    def calculate_mileage_reimbursement(self, miles, days):
        """Calculate mileage reimbursement with tiered rates and efficiency bonuses"""
        if miles <= 0:
            return 0
            
        # Tiered mileage calculation
        mileage_reimbursement = 0
        
        if miles <= self.mileage_tier_1_threshold:
            mileage_reimbursement = miles * self.mileage_base_rate
        elif miles <= self.mileage_tier_2_threshold:
            mileage_reimbursement = (self.mileage_tier_1_threshold * self.mileage_base_rate + 
                                   (miles - self.mileage_tier_1_threshold) * self.mileage_tier_2_rate)
        else:
            mileage_reimbursement = (self.mileage_tier_1_threshold * self.mileage_base_rate + 
                                   (self.mileage_tier_2_threshold - self.mileage_tier_1_threshold) * self.mileage_tier_2_rate +
                                   (miles - self.mileage_tier_2_threshold) * self.mileage_tier_3_rate)
        
        # Efficiency bonus calculation
        if days > 0:
            miles_per_day = miles / days
            if self.efficiency_sweet_spot_min <= miles_per_day <= self.efficiency_sweet_spot_max:
                efficiency_bonus = mileage_reimbursement * self.efficiency_bonus_rate
                mileage_reimbursement += efficiency_bonus
            elif miles_per_day > 250:  # Very high mileage gets diminishing returns
                penalty = mileage_reimbursement * 0.1
                mileage_reimbursement -= penalty
        
        return mileage_reimbursement
    
    def calculate_receipt_reimbursement(self, receipts, days):
        """Calculate receipt reimbursement with complex penalty/bonus structure"""
        if receipts <= 0:
            return 0
        
        # Very small receipts get penalized
        if receipts < self.receipt_penalty_threshold:
            return receipts * 0.3  # Heavy penalty
        
        # Optimal range gets good treatment
        if self.receipt_optimal_min <= receipts <= self.receipt_optimal_max:
            return receipts * 0.85
        
        # High receipts get diminishing returns
        if receipts > self.receipt_diminishing_threshold:
            base_reimbursement = self.receipt_optimal_max * 0.85
            excess = receipts - self.receipt_optimal_max
            diminished_reimbursement = excess * 0.4  # Diminishing returns
            return base_reimbursement + diminished_reimbursement
        
        # Medium receipts
        return receipts * 0.75
    
    def apply_special_bonuses(self, days, miles, receipts, base_total):
        """Apply special bonuses and penalties based on trip characteristics"""
        bonus = 0
        
        # 5-day trip bonus (mentioned in interviews)
        if days == 5:
            miles_per_day = miles / days if days > 0 else 0
            receipts_per_day = receipts / days if days > 0 else 0
            
            # Kevin's "sweet spot combo": 5 days, 180+ miles/day, <$100/day receipts
            if miles_per_day >= 180 and receipts_per_day < 100:
                bonus += base_total * 0.12  # 12% bonus
            else:
                bonus += base_total * 0.05  # Standard 5-day bonus
        
        # Long trip penalty (vacation penalty)
        if days >= 8:
            receipts_per_day = receipts / days if days > 0 else 0
            if receipts_per_day > 90:  # High spending on long trips
                bonus -= base_total * 0.08  # 8% penalty
        
        # High efficiency bonus
        if days > 0:
            miles_per_day = miles / days
            if miles_per_day > 300:  # Very high mileage
                if receipts / days < 80:  # But low spending
                    bonus += base_total * 0.06  # Efficiency bonus
        
        return bonus
    
    def apply_interaction_effects(self, days, miles, receipts):
        """Apply complex interaction effects between parameters"""
        interaction_bonus = 0
        
        # High mileage + low receipts interaction
        if miles > 200 and receipts < 100:
            interaction_bonus += miles * 0.1
        
        # Medium trip + balanced parameters
        if 3 <= days <= 6:
            miles_per_day = miles / days if days > 0 else 0
            receipts_per_day = receipts / days if days > 0 else 0
            
            if 100 <= miles_per_day <= 200 and 50 <= receipts_per_day <= 120:
                interaction_bonus += days * 15  # Balanced trip bonus
        
        return interaction_bonus
    
    def calculate_reimbursement(self, days, miles, receipts):
        """Main calculation method that combines all components"""
        
        # Base calculations
        base_reimbursement = self.calculate_base_reimbursement(days)
        mileage_reimbursement = self.calculate_mileage_reimbursement(miles, days)
        receipt_reimbursement = self.calculate_receipt_reimbursement(receipts, days)
        
        # Combine base components
        total = base_reimbursement + mileage_reimbursement + receipt_reimbursement
        
        # Apply special bonuses/penalties
        special_bonus = self.apply_special_bonuses(days, miles, receipts, total)
        total += special_bonus
        
        # Apply interaction effects
        interaction_bonus = self.apply_interaction_effects(days, miles, receipts)
        total += interaction_bonus
        
        # Add some controlled randomness (mentioned in interviews)
        # Using a deterministic "random" factor based on input values
        pseudo_random_factor = ((days * 7 + miles * 3 + int(receipts * 100)) % 100) / 1000
        randomness_adjustment = total * pseudo_random_factor * 0.02  # Up to 2% variation
        total += randomness_adjustment
        
        # Ensure minimum reimbursement
        min_reimbursement = days * 50  # Absolute minimum
        total = max(total, min_reimbursement)
        
        return round(total, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <days> <miles> <receipts>")
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])
        
        calculator = ReimbursementCalculator()
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