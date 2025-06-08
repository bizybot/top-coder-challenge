#!/usr/bin/env python3

import sys
import math

def calculate_reimbursement(days, miles, receipts):
    """
    Final ACME Corp legacy reimbursement system replica
    Base formula: days*110 + miles*0.5 + sqrt(receipts)*10
    Plus corrections based on residual analysis
    """
    
    # Base formula (best performing from pattern analysis)
    base_component = days * 110
    mileage_component = miles * 0.5
    receipt_component = math.sqrt(max(receipts, 0)) * 10
    
    total = base_component + mileage_component + receipt_component
    
    # Apply trip duration corrections (from residual analysis)
    duration_corrections = {
        1: 187.62,
        2: 217.65,
        3: 112.39,
        4: 164.86,
        5: 111.62,
        6: 99.75,
        7: 87.86,
        8: -80.72,
        9: -188.89,
        10: -237.93,
        11: -282.68,
        12: -342.96,
        13: -407.47,
        14: -494.81
    }
    
    if days in duration_corrections:
        total += duration_corrections[days]
    elif days > 14:
        # Extrapolate for very long trips
        total += -494.81 - (days - 14) * 50
    
    # Apply efficiency corrections
    if days > 0:
        efficiency = miles / days
        
        if efficiency < 50:
            total += -166.80
        elif efficiency < 100:
            total += -170.18
        elif efficiency < 150:
            total += 66.22
        elif efficiency < 200:
            total += 129.40
        elif efficiency < 250:
            total += 170.36
        elif efficiency < 300:
            total += 74.05
        elif efficiency < 350:
            total += 140.10
        elif efficiency < 400:
            total += 57.07
        elif efficiency < 450:
            total += 77.63
        elif efficiency < 500:
            total += 159.91
        elif efficiency < 600:
            total += 252.59
        else:
            total += 519.34
    
    # Apply receipt amount corrections
    if receipts < 100:
        total += -192.70
    elif receipts < 200:
        total += -343.16
    elif receipts < 300:
        total += -379.32
    elif receipts < 400:
        total += -361.21
    elif receipts < 500:
        total += -334.79
    elif receipts < 600:
        total += -292.59
    elif receipts < 700:
        total += -207.90
    elif receipts < 800:
        total += -88.52
    elif receipts < 900:
        total += -63.56
    elif receipts < 1000:
        total += 13.46
    elif receipts < 1100:
        total += 94.86
    elif receipts < 1200:
        total += 149.47
    elif receipts < 1300:
        total += 153.58
    elif receipts < 1400:
        total += 183.31
    elif receipts < 1500:
        total += 172.09
    else:
        total += 200  # For very high receipts
    
    # Ensure reasonable bounds
    total = max(total, days * 50)  # Minimum reimbursement
    
    return round(total, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement_final.py <days> <miles> <receipts>")
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])
        
        reimbursement = calculate_reimbursement(days, miles, receipts)
        print(f"{reimbursement:.2f}")
        
    except ValueError as e:
        print(f"Error: Invalid input parameters - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 