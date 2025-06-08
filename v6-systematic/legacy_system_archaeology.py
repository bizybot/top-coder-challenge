#!/usr/bin/env python3

import json
import statistics
from collections import defaultdict, Counter
import math

def archaeological_analysis():
    """
    Reverse-engineer the business logic and accumulated patches in this 60-year-old legacy system
    Approach: Look for evidence of original rules + accumulated bug fixes and special cases
    """
    
    with open('public_cases.json', 'r') as f:
        data = json.load(f)
    
    print("LEGACY SYSTEM ARCHAEOLOGICAL ANALYSIS")
    print("=" * 60)
    print("Hypothesis: 60-year-old system = Original Logic + Decades of Patches")
    print("Looking for: Business rules, bug fixes, special cases, complaint-driven patches")
    print()
    
    # 1. LOOK FOR ORIGINAL BUSINESS LOGIC PATTERNS
    print("1. SEARCHING FOR ORIGINAL BUSINESS LOGIC")
    print("-" * 50)
    
    # Group cases by "clean" scenarios that might reveal original logic
    clean_cases = []
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Look for "round number" cases that might show original rules
        if (miles % 50 == 0 or miles % 100 == 0) and receipts < 100:
            clean_cases.append({
                'days': days,
                'miles': miles,
                'receipts': receipts,
                'output': output,
                'per_day': output / days,
                'per_mile': output / miles if miles > 0 else 0
            })
    
    print(f"Found {len(clean_cases)} 'clean' cases with round miles and low receipts:")
    clean_cases.sort(key=lambda x: (x['days'], x['miles']))
    
    for case in clean_cases[:15]:
        print(f"  {case['days']}d, {case['miles']:3.0f}mi, ${case['receipts']:5.2f} → "
              f"${case['output']:6.2f} (${case['per_day']:6.2f}/day, ${case['per_mile']:4.2f}/mile)")
    
    # 2. LOOK FOR EVIDENCE OF SPECIAL CASE PATCHES
    print(f"\n2. EVIDENCE OF SPECIAL CASE PATCHES")
    print("-" * 40)
    
    # Check for exact amounts that suggest manual overrides
    output_frequencies = Counter()
    for case in data:
        # Round to nearest $5 to find suspiciously common amounts
        rounded_output = round(case['expected_output'] / 5) * 5
        output_frequencies[rounded_output] += 1
    
    # Look for suspiciously common output amounts
    common_outputs = output_frequencies.most_common(20)
    print("Suspiciously common reimbursement amounts (possible manual overrides):")
    for amount, count in common_outputs:
        if count >= 3:  # Appears 3+ times
            print(f"  ${amount:6.0f}: {count} cases")
    
    # 3. LOOK FOR COMPLAINT-DRIVEN PATCHES
    print(f"\n3. COMPLAINT-DRIVEN PATCHES ANALYSIS")
    print("-" * 45)
    
    # Look for cases where similar inputs give very different outputs (evidence of patches)
    similar_case_groups = defaultdict(list)
    
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Group by similar characteristics (within ranges)
        group_key = (
            days,
            round(miles / 50) * 50,  # 50-mile buckets
            round(receipts / 100) * 100  # $100 buckets
        )
        
        similar_case_groups[group_key].append({
            'case': case,
            'output': output
        })
    
    print("Similar inputs with suspiciously different outputs (evidence of patches):")
    patch_evidence = 0
    for group_key, cases in similar_case_groups.items():
        if len(cases) >= 3:  # At least 3 similar cases
            outputs = [c['output'] for c in cases]
            std_dev = statistics.stdev(outputs) if len(outputs) > 1 else 0
            
            # Look for high variance in similar cases
            if std_dev > 50:  # High variance suggests patches/special cases
                patch_evidence += 1
                if patch_evidence <= 10:  # Show first 10
                    days, miles_bucket, receipts_bucket = group_key
                    avg_output = statistics.mean(outputs)
                    print(f"  {days}d, ~{miles_bucket}mi, ~${receipts_bucket} → "
                          f"${min(outputs):.0f}-${max(outputs):.0f} (avg ${avg_output:.0f}, std ${std_dev:.0f})")
    
    print(f"Found {patch_evidence} groups with high variance (possible patch evidence)")
    
    # 4. LOOK FOR BUSINESS RULE EVIDENCE
    print(f"\n4. BUSINESS RULE ARCHAEOLOGY")
    print("-" * 35)
    
    # Look for evidence of original per-diem structure
    print("A. Per-diem base rates by duration:")
    duration_analysis = defaultdict(list)
    
    # Look at cases with minimal miles and receipts (closest to pure per-diem)
    minimal_cases = [case for case in data 
                    if case['input']['miles_traveled'] < 50 
                    and case['input']['total_receipts_amount'] < 50]
    
    for case in minimal_cases:
        days = case['input']['trip_duration_days']
        output = case['expected_output']
        per_day = output / days
        duration_analysis[days].append(per_day)
    
    for days in sorted(duration_analysis.keys())[:10]:
        rates = duration_analysis[days]
        if len(rates) >= 3:
            avg_rate = statistics.mean(rates)
            min_rate = min(rates)
            max_rate = max(rates)
            print(f"  {days:2d} days: ${avg_rate:6.2f}/day avg, range ${min_rate:.0f}-${max_rate:.0f} ({len(rates)} cases)")
    
    # Look for evidence of mileage reimbursement structure
    print(f"\nB. Mileage reimbursement patterns:")
    
    # Look at cases with minimal receipts but varying mileage
    mileage_cases = [case for case in data 
                    if case['input']['total_receipts_amount'] < 50]
    
    mileage_groups = defaultdict(list)
    for case in mileage_cases:
        miles = case['input']['miles_traveled']
        days = case['input']['trip_duration_days']
        output = case['expected_output']
        
        # Estimate mileage component by subtracting estimated per-diem
        estimated_per_diem = days * 100  # rough estimate
        mileage_contribution = output - estimated_per_diem
        
        if miles > 0:
            rate_per_mile = mileage_contribution / miles
            mileage_bucket = (miles // 100) * 100
            mileage_groups[mileage_bucket].append(rate_per_mile)
    
    for miles_bucket in sorted(mileage_groups.keys())[:8]:
        rates = mileage_groups[miles_bucket]
        if len(rates) >= 3:
            avg_rate = statistics.mean(rates)
            print(f"  {miles_bucket:3.0f}-{miles_bucket+99:3.0f} miles: ${avg_rate:.3f}/mile avg ({len(rates)} cases)")
    
    # 5. LOOK FOR BUG FIX EVIDENCE
    print(f"\n5. BUG FIX ARCHAEOLOGY")
    print("-" * 25)
    
    # Look for cases where the math doesn't add up (evidence of manual corrections)
    weird_cases = []
    
    for case in data:
        days = case['input']['trip_duration_days']
        miles = case['input']['miles_traveled']
        receipts = case['input']['total_receipts_amount']
        output = case['expected_output']
        
        # Check if output is suspiciously low or high compared to inputs
        input_sum = days * 50 + miles * 0.3 + receipts * 0.5  # rough calculation
        ratio = output / input_sum if input_sum > 0 else 0
        
        # Look for extreme ratios (possible bug fixes)
        if ratio < 0.3 or ratio > 3.0:
            weird_cases.append({
                'case': case,
                'ratio': ratio,
                'inputs': (days, miles, receipts),
                'output': output
            })
    
    weird_cases.sort(key=lambda x: abs(x['ratio'] - 1.0), reverse=True)
    
    print("Cases with suspicious input/output ratios (possible bug fixes):")
    for i, wc in enumerate(weird_cases[:10]):
        days, miles, receipts = wc['inputs']
        print(f"  {i+1:2d}. {days}d, {miles:4.0f}mi, ${receipts:6.2f} → ${wc['output']:7.2f} "
              f"(ratio: {wc['ratio']:.2f})")
    
    # 6. RECONSTRUCT LIKELY SYSTEM EVOLUTION
    print(f"\n6. RECONSTRUCTED SYSTEM EVOLUTION")
    print("-" * 40)
    
    print("HYPOTHESIS: Original System (1960s)")
    print("  - Simple per-diem: $X per day")
    print("  - Mileage: $Y per mile") 
    print("  - Receipt reimbursement: $Z per dollar or percentage")
    print()
    
    print("HYPOTHESIS: Accumulated Patches (1960s-2020s)")
    print("  - Efficiency bonuses (complaints about long drives)")
    print("  - Anti-fraud measures (complaints about excessive claims)")
    print("  - Special case handlers (executive complaints)")
    print("  - Bug workarounds (mathematical errors that became 'features')")
    print("  - Seasonal adjustments (inflation, policy changes)")
    print("  - Department-specific rules (different treatment)")
    print()
    
    print("EVIDENCE IN OUR DATA:")
    print("  ✓ Non-linear receipt relationship (sqrt) - likely anti-fraud patch")
    print("  ✓ Duration-specific corrections - complaint-driven patches")
    print("  ✓ Efficiency sweet spots - performance incentive patches")
    print("  ✓ Minimum guarantees - fairness patches")
    print("  ✓ Random variations - possible rounding bugs or hash-based rules")

if __name__ == "__main__":
    archaeological_analysis() 