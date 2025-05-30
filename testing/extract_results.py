#!/usr/bin/env python3
import json

# Load the regression results
with open('ucla_regression_results.json', 'r') as f:
    results = json.load(f)

print("=== UCLA WOMEN'S BASKETBALL RAG TEST RESULTS ===")
print(f"Total Queries: {len(results)}")

successful = [r for r in results if r['error'] is None]
failed = [r for r in results if r['error'] is not None]

print(f"Successful: {len(successful)}")
print(f"Failed: {len(failed)}")
print(f"Success Rate: {len(successful)/len(results)*100:.1f}%")

print("\n" + "="*80)
print("SUCCESSFUL QUERY RESULTS")
print("="*80)

for i, result in enumerate(successful, 1):
    print(f"\n{i}. QUESTION: {result['query']}")
    print(f"   SQL: {result['sql'].replace(chr(10), ' ').strip()}")
    
    if result['results']:
        if len(result['results']) == 1 and len(result['results'][0]) == 1:
            # Single value result
            print(f"   ANSWER: {result['results'][0][0]}")
        elif len(result['results']) == 1:
            # Single row with multiple columns
            print(f"   ANSWER: {result['results'][0]}")
        else:
            # Multiple rows
            print(f"   ANSWER: {len(result['results'])} rows returned")
            for j, row in enumerate(result['results'][:3], 1):  # Show first 3 rows
                print(f"           Row {j}: {row}")
            if len(result['results']) > 3:
                print(f"           ... and {len(result['results']) - 3} more rows")
    else:
        print(f"   ANSWER: No data returned")

if failed:
    print("\n" + "="*80)
    print("FAILED QUERIES")
    print("="*80)
    
    for i, result in enumerate(failed, 1):
        print(f"\n{i}. QUESTION: {result['query']}")
        print(f"   ERROR: {result['error']}")
        if result['sql']:
            print(f"   SQL: {result['sql'].replace(chr(10), ' ').strip()[:100]}...")

print(f"\n{'='*80}")
print(f"SUMMARY: {len(successful)}/{len(results)} queries successful ({len(successful)/len(results)*100:.1f}%)")
print(f"{'='*80}") 