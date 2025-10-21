"""
Simple historical test demo using EUR/USD
"""
from historical_tester import custom_test
from datetime import datetime, timedelta

# Calculate dates for last 3 months
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

print("Running Historical Test on EUR/USD (Last 3 months)...")
print("This will test signal and ML prediction accuracy\n")

# Run custom test on EURUSD
tester, report = custom_test(
    symbol='EURUSD=X',
    market_type='forex',
    start_date=start_date.strftime('%Y-%m-%d'),
    end_date=end_date.strftime('%Y-%m-%d'),
    interval='1d'
)

print("\n" + "="*60)
print("TEST COMPLETE!")
print("="*60)
print("\nResults saved to:")
print("  - EURUSD_X_test_results.json")
print("  - EURUSD_X_test_report.json")
print("\nCheck the report above for accuracy metrics!")
