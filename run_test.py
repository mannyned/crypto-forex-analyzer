"""
Quick test script for backtester
"""
from backtester import run_backtest

# Test with EUR/USD (forex) - should have good historical data
print("Testing EUR/USD Forex Pair...")
backtester, trades, metrics = run_backtest(
    symbol='EURUSD=X',
    market_type='forex',
    days=180,  # 6 months
    initial_capital=10000,
    risk_per_trade=0.01  # 1% risk per trade
)

print("\nBacktest completed successfully!")
print(f"Check the JSON file for detailed results")
