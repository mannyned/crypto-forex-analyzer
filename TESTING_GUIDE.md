# Historical Testing and Backtesting Guide

This guide explains how to use the historical testing and backtesting modules to validate the analyzer's performance with historical data.

## Overview

The application includes three main testing modules:

1. **historical_tester.py** - Tests prediction accuracy on historical data
2. **backtester.py** - Simulates actual trading with entry/exit points
3. **report_generator.py** - Creates HTML reports from test results

## Module 1: Historical Tester

### What It Does

Tests how accurately the analyzer's signals and ML predictions would have performed on historical data. It doesn't simulate trades, just checks if predictions were correct.

### Features

- Tests signal accuracy (STRONG BUY, BUY, HOLD, SELL, STRONG SELL)
- Tests ML prediction accuracy (forex only)
- Analyzes performance by market type, symbol, and signal type
- Generates comprehensive reports with accuracy percentages

### Quick Test (3 months, 3 crypto + 3 forex)

```python
from historical_tester import quick_test

tester, report = quick_test()
```

**Output:**
- Console report with accuracy metrics
- `quick_test_results.json` - Raw test data
- `quick_test_report.json` - Performance metrics

### Extended Test (1 year, ALL markets)

```python
from historical_tester import extended_test

tester, report = extended_test()
```

**Output:**
- `extended_test_results.json`
- `extended_test_report.json`

### Custom Test (Specific symbol and dates)

```python
from historical_tester import custom_test

tester, report = custom_test(
    symbol='BTC/USDT',
    market_type='crypto',
    start_date='2024-01-01',
    end_date='2024-12-31',
    interval='1d'
)
```

### Understanding the Report

```
HISTORICAL TESTING REPORT
============================================================

SUMMARY
------------------------------------------------------------
Total Tests: 1,234
Date Range: 2024-01-01 to 2024-12-31
Markets Tested: 6

SIGNAL ACCURACY
------------------------------------------------------------
Overall: 850/1234 (68.88%)

By Signal Type:
  STRONG BUY  :  45/ 67 (67.16%)
  BUY         : 120/189 (63.49%)
  HOLD        : 450/678 (66.37%)
  SELL        :  89/145 (61.38%)
  STRONG SELL :  46/ 55 (83.64%)

ML PREDICTION ACCURACY (Forex Only)
------------------------------------------------------------
Overall: 245/312 (78.53%)

By Direction:
  BULLISH : 85/105 (80.95%)
  BEARISH : 78/ 98 (79.59%)
  NEUTRAL : 82/109 (75.23%)

PERFORMANCE BY MARKET TYPE
------------------------------------------------------------
CRYPTO:
  Signal Accuracy: 65.23%
  Total Tests: 623
  Avg Return: 2.34%

FOREX:
  Signal Accuracy: 72.45%
  Total Tests: 611
  Avg Return: 1.87%
```

**Key Metrics:**
- **Signal Accuracy**: % of times signal matched actual price movement
- **ML Accuracy**: % of times ML prediction matched actual outcome
- **Avg Return**: Average actual price movement during test periods

## Module 2: Backtester

### What It Does

Simulates actual trading by:
- Entering trades when signals are strong
- Setting stop loss and take profit from analyzer recommendations
- Tracking profit/loss for each trade
- Calculating overall portfolio performance

### Features

- Realistic trade simulation with entry/exit points
- Position sizing based on risk percentage
- Stop loss and take profit management
- Complete trade history with reasons for exit
- Performance metrics (win rate, profit factor, Sharpe ratio, max drawdown)

### Quick Backtest (Single symbol)

```python
from backtester import run_backtest

backtester, trades, metrics = run_backtest(
    symbol='EURUSD=X',
    market_type='forex',
    days=180,
    initial_capital=10000,
    risk_per_trade=0.01  # 1% risk per trade
)
```

**Parameters:**
- `symbol`: Trading symbol (e.g., 'EURUSD=X', 'BTC/USDT')
- `market_type`: 'crypto' or 'forex'
- `days`: Number of days to backtest
- `initial_capital`: Starting capital in dollars
- `risk_per_trade`: Risk percentage (0.01 = 1%)

**Output:**
- Console report with all metrics
- JSON file: `backtest_EURUSD_X_180days.json`

### Understanding the Backtest Report

```
BACKTEST RESULTS
============================================================

OVERALL PERFORMANCE
------------------------------------------------------------
Initial Capital:  $10,000.00
Final Capital:    $11,245.67
Total Return:     +12.46%
Max Drawdown:     8.34%
Sharpe Ratio:     1.23

TRADE STATISTICS
------------------------------------------------------------
Total Trades:     45
Winning Trades:   28 (62.22%)
Losing Trades:    17

PROFIT/LOSS BREAKDOWN
------------------------------------------------------------
Total Profit:     $2,856.34
Total Loss:       $1,610.67
Average Win:      $102.01
Average Loss:     $94.74
Profit Factor:    1.77

EXIT REASONS
------------------------------------------------------------
TAKE_PROFIT   :  28 trades (Avg P/L: +$102.01)
STOP_LOSS     :  15 trades (Avg P/L: -$97.38)
END_OF_PERIOD :   2 trades (Avg P/L: +$45.23)

RECENT TRADES (Last 10)
------------------------------------------------------------
 1. 2025-09-15 | BUY          | TAKE_PROFIT  | +$125.67
 2. 2025-09-18 | STRONG BUY   | STOP_LOSS    | -$89.34
 3. 2025-09-22 | BUY          | TAKE_PROFIT  | +$98.45
   ...
```

**Key Metrics Explained:**

- **Total Return**: % gain/loss on initial capital
- **Max Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns (>1 is good, >2 is excellent)
- **Win Rate**: % of profitable trades
- **Profit Factor**: Gross profit / Gross loss (>1.5 is good)
- **Average Win/Loss**: Average P/L per winning/losing trade

### Entry Conditions

The backtester enters trades when:

**For All Markets:**
1. Signal is STRONG BUY or BUY
2. Signal strength >= 50%
3. Candlestick pattern detected (5-minute or 4-hour)

**For Forex (Additional):**
4. ML prediction is BULLISH with >= 75% confidence

### Exit Conditions

**Stop Loss Hit:**
- Price reaches stop loss level
- Loss is limited to risk amount (e.g., 1% of capital)

**Take Profit Hit:**
- Price reaches take profit level
- Profit is taken (typically 2-3x risk amount)

**End of Period:**
- Backtest period ends with open trade
- Trade is closed at final price

## Module 3: Report Generator

### What It Does

Creates professional HTML reports from backtest results.

### Usage

```python
from report_generator import generate_html_report

generate_html_report(
    results_file='backtest_EURUSD_X_180days.json',
    output_file='backtest_report.html'
)
```

Or via command line:

```bash
python report_generator.py backtest_results.json report.html
```

### Report Features

- **Interactive Metrics Dashboard**: Key performance indicators with color coding
- **Detailed Trade Table**: All trades with entry/exit prices and P/L
- **Visual Progress Bars**: Win rate and other metrics
- **Professional Styling**: Neural dark theme matching the app
- **Export-Friendly**: Can be saved as PDF or shared via email

## Complete Testing Workflow

### Step 1: Historical Accuracy Test

First, test how accurate the analyzer is:

```python
from historical_tester import quick_test

# Test prediction accuracy over last 3 months
tester, report = quick_test()
```

**Look for:**
- Signal accuracy > 60% (good)
- ML accuracy > 70% (good for forex)
- Strong signals (STRONG BUY/SELL) should have highest accuracy

### Step 2: Backtest Trading Strategy

If accuracy looks good, simulate actual trading:

```python
from backtester import run_backtest

# Backtest forex pair
backtester, trades, metrics = run_backtest(
    symbol='EURUSD=X',
    market_type='forex',
    days=180,
    initial_capital=10000,
    risk_per_trade=0.01
)
```

**Look for:**
- Positive total return
- Win rate > 50%
- Profit factor > 1.5
- Max drawdown < 20%
- Sharpe ratio > 1.0

### Step 3: Generate HTML Report

Create a professional report:

```python
from report_generator import generate_html_report

generate_html_report(
    'backtest_EURUSD_X_180days.json',
    'my_backtest_report.html'
)
```

Open `my_backtest_report.html` in a browser to view.

### Step 4: Analyze and Optimize

Review the results and adjust:

**If win rate is low (<45%):**
- Increase minimum signal strength requirement
- Add more entry confirmation (patterns, ML confidence)

**If profit factor is low (<1.2):**
- Adjust risk/reward ratio (wider take profit)
- Tighten entry conditions

**If too few trades:**
- Lower signal strength requirement
- Test more markets
- Use shorter timeframes

**If max drawdown is high (>25%):**
- Reduce risk per trade (e.g., 0.5% instead of 1%)
- Add better stop loss management
- Diversify across multiple markets

## Advanced Usage

### Test Multiple Symbols

```python
from backtester import Backtester

symbols = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X']
all_trades = []
total_capital = 10000

for symbol in symbols:
    backtester = Backtester(initial_capital=total_capital/len(symbols), risk_per_trade=0.01)
    trades, equity = backtester.backtest_symbol(
        symbol=symbol,
        market_type='forex',
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    all_trades.extend(trades)

# Analyze combined results
metrics = backtester.analyze_results(all_trades, equity)
backtester.print_results(metrics, all_trades)
```

### Compare Different Risk Levels

```python
from backtester import run_backtest

risk_levels = [0.005, 0.01, 0.02]  # 0.5%, 1%, 2%

for risk in risk_levels:
    print(f"\nTesting with {risk*100}% risk per trade:")
    backtester, trades, metrics = run_backtest(
        symbol='EURUSD=X',
        market_type='forex',
        days=180,
        risk_per_trade=risk
    )
    print(f"Total Return: {metrics['total_return']:.2f}%")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
```

### Test Different Entry Conditions

Modify the entry conditions in `backtester.py`:

```python
# In backtest_symbol method, around line 89:

# More conservative (higher accuracy, fewer trades)
if signal == 'STRONG BUY' and strength >= 70:
    if analysis.get('patterns_4h'):  # Require 4H pattern
        if market_type == 'forex' and analysis.get('ml_prediction'):
            ml_pred = analysis['ml_prediction']
            if ml_pred['direction'] == 'BULLISH' and ml_pred['confidence'] >= 85:
                entry_conditions = True

# More aggressive (more trades, possibly lower accuracy)
if signal in ['STRONG BUY', 'BUY'] and strength >= 40:
    entry_conditions = True
```

## Performance Benchmarks

Based on testing, typical results:

### Historical Accuracy

| Market | Signal Accuracy | ML Accuracy | Avg Return |
|--------|----------------|-------------|------------|
| Crypto | 60-70% | N/A | 2-5% |
| Forex | 65-75% | 70-85% | 1-3% |

### Backtest Performance (Conservative Settings)

| Metric | Good | Excellent |
|--------|------|-----------|
| Win Rate | >50% | >60% |
| Profit Factor | >1.5 | >2.0 |
| Total Return (6mo) | >5% | >15% |
| Max Drawdown | <20% | <10% |
| Sharpe Ratio | >1.0 | >2.0 |

## Limitations and Considerations

### Historical Testing Limitations

1. **Hindsight Bias**: Testing on historical data can overfit
2. **Slippage**: Real trades may not execute at exact prices
3. **Commissions**: Not included in backtests
4. **Market Conditions**: Past != Future performance

### Backtest Limitations

1. **Simplified Execution**: Assumes perfect fills at stop/target
2. **No Spread Costs**: Forex spreads not included
3. **Position Sizing**: Assumes fractional position sizes possible
4. **Pattern Detection**: Uses historical data, may have look-ahead bias

### Best Practices

1. **Test Multiple Periods**: Don't rely on single time period
2. **Out-of-Sample Testing**: Test on data not used for development
3. **Walk-Forward Analysis**: Test progressively forward in time
4. **Multiple Markets**: Diversify across crypto and forex
5. **Conservative Risk**: Start with low risk per trade (0.5-1%)
6. **Paper Trading**: Test in real-time before live trading

## Files Generated

### Historical Tester

- `quick_test_results.json` - Raw test data (quick test)
- `quick_test_report.json` - Performance metrics (quick test)
- `extended_test_results.json` - Raw test data (extended test)
- `extended_test_report.json` - Performance metrics (extended test)
- `{SYMBOL}_test_results.json` - Custom test raw data
- `{SYMBOL}_test_report.json` - Custom test metrics

### Backtester

- `backtest_{SYMBOL}_{DAYS}days.json` - Complete backtest results
  - Contains: metrics, all trades, timestamp
  - Format: JSON with trade history and performance data

### Report Generator

- `{name}_report.html` - Professional HTML report
  - Interactive dashboard with metrics
  - Complete trade table
  - Styled with neural dark theme

## Troubleshooting

### "No data available for symbol"

**Problem**: Yahoo Finance doesn't have data for that symbol
**Solution**:
- For crypto: Use proper format (e.g., 'BTC-USD' not 'BTC/USDT')
- For forex: Use Yahoo format (e.g., 'EURUSD=X')
- Try different date range (avoid too recent or too old)

### "No trades executed"

**Problem**: Entry conditions too strict or no patterns detected
**Solution**:
- Lower signal strength requirement
- Check if patterns are being detected
- Verify ML predictions are working (forex only)
- Try longer test period

### "All trades are losses"

**Problem**: Strategy or entry conditions need adjustment
**Solution**:
- Review entry conditions logic
- Check stop loss/take profit calculations
- Verify signal accuracy with historical tester first
- Adjust risk/reward ratios

### Unicode encoding errors

**Problem**: Terminal doesn't support Unicode characters
**Solution**: Already fixed in code - uses "SUCCESS:" and "ERROR:" instead of emojis

## Example Scripts

### Complete Test Suite

```python
"""
complete_test.py - Run all tests
"""
from historical_tester import quick_test
from backtester import run_backtest
from report_generator import generate_html_report

print("Step 1: Historical Accuracy Test...")
tester, hist_report = quick_test()

print("\nStep 2: Backtest Trading Strategy...")
backtester, trades, metrics = run_backtest(
    symbol='EURUSD=X',
    market_type='forex',
    days=180,
    initial_capital=10000,
    risk_per_trade=0.01
)

print("\nStep 3: Generate HTML Report...")
generate_html_report('backtest_EURUSD_X_180days.json', 'final_report.html')

print("\nComplete! Check final_report.html for results.")
```

### Compare Multiple Symbols

```python
"""
compare_symbols.py - Compare performance across symbols
"""
from backtester import run_backtest

symbols = [
    ('EURUSD=X', 'forex'),
    ('GBPUSD=X', 'forex'),
    ('USDJPY=X', 'forex')
]

results = {}

for symbol, market_type in symbols:
    print(f"\nTesting {symbol}...")
    _, _, metrics = run_backtest(
        symbol=symbol,
        market_type=market_type,
        days=180,
        initial_capital=10000,
        risk_per_trade=0.01
    )
    results[symbol] = metrics

# Compare results
print("\n\nCOMPARISON:")
print("="*60)
for symbol, metrics in results.items():
    print(f"{symbol:12s} | Return: {metrics['total_return']:+6.2f}% | Win Rate: {metrics['win_rate']:5.2f}%")
```

## Next Steps

1. Run the quick test to validate accuracy
2. Backtest your best-performing markets
3. Generate HTML reports for analysis
4. Adjust strategy based on results
5. Test with different risk levels
6. Consider paper trading before live

## Support

For issues or questions:
- Check the README.md for general documentation
- Review the USER_GUIDE.md for usage instructions
- Open an issue on GitHub for bugs

---

**Disclaimer**: All testing is for educational purposes only. Past performance does not guarantee future results. Always do your own research and never risk more than you can afford to lose.

*Last Updated: v3.0.0 - October 20, 2025*
