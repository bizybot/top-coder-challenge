#!/bin/bash

# Black Box Challenge - ACME Corp Legacy Reimbursement System Replica
# This script replicates the behavior of a 60-year-old travel reimbursement system
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Validate input parameters
if [ $# -ne 3 ]; then
    echo "Error: Exactly 3 parameters required"
    echo "Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>"
    exit 1
fi

# Call the reverse-engineered legacy system solution
python3 v7-reverse-engineering/solution_legacy_patches.py "$1" "$2" "$3" 