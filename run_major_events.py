"""
Run all major event tests automatically (no user input required)
"""
from test_major_events import compare_all_events

print("\n" + "="*70)
print("RUNNING ALL MAJOR EVENT TESTS")
print("="*70)
print("\nThis will test:")
print("1. 2015 Swiss Franc Flash Crash")
print("2. 2016 Brexit Vote")
print("3. 2020 COVID-19 Crash")
print("\nPlease wait, this may take several minutes...\n")

# Run all tests
results = compare_all_events()

print("\n" + "="*70)
print("ALL TESTS COMPLETE!")
print("="*70)
print("\nResults saved to major_events_comparison.json")
print("\nCheck individual JSON files for detailed results:")
print("  - swiss_franc_2015_test.json / swiss_franc_2015_report.json")
print("  - brexit_2016_test.json / brexit_2016_report.json")
print("  - covid_2020_test.json / covid_2020_report.json")
