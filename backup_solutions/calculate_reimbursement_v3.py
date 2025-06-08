#!/usr/bin/env python3

import sys
import math

def calculate_reimbursement(days, miles, receipts):
    """
    Use the exact best formula discovered: days*110 + miles*0.5 + sqrt(receipts)*10
    """
    
    # The best performing formula from pattern analysis
    base_component = days * 110
    mileage_component = miles * 0.5
    receipt_component = math.sqrt(max(receipts, 0)) * 10
    
    total = base_component + mileage_component + receipt_component
    
    return round(total, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement_v3.py <days> <miles> <receipts>")
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