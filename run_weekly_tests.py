"""
Run all major event tests with WEEKLY intervals automatically
"""
from test_major_events_weekly import compare_all_events_weekly

print("\n" + "="*70)
print("RUNNING ALL MAJOR EVENT TESTS - WEEKLY INTERVALS")
print("="*70)
print("\nThis will test with WEEKLY data for higher trade frequency:")
print("1. 2015 Swiss Franc Flash Crash")
print("2. 2016 Brexit Vote")
print("3. 2020 COVID-19 Crash")
print("\nWeekly intervals = More trading opportunities!")
print("\nPlease wait, this may take several minutes...\n")

# Run all tests
results = compare_all_events_weekly()

print("\n" + "="*70)
print("ALL WEEKLY TESTS COMPLETE!")
print("="*70)
print("\nResults saved to major_events_weekly_comparison.json")
print("\nCheck individual JSON files for detailed results:")
print("  - swiss_franc_2015_weekly_test.json / _report.json / _backtest.json")
print("  - brexit_2016_weekly_test.json / _report.json / _backtest.json")
print("  - covid_2020_weekly_test.json / _report.json / _backtest.json")
