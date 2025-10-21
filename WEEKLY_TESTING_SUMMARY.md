# Weekly Interval Testing Summary

## Goal
Increase trade frequency by using weekly (1wk) intervals instead of daily (1d) intervals.

## Configuration Changes Made

### 1. Backtester Updates
- Added weekly interval support
- Relaxed signal threshold: 15% (vs 20% daily, 50% intraday)
- Relaxed ML confidence: 50% (vs 55% daily, 75% intraday)
- Patterns remain optional
- Adjusted starting index: 20 weeks for weekly (vs 100 days for daily)

### 2. Extended Test Periods
- Swiss Franc 2015: 3 years (2013-2015) - 157 weeks
- Brexit 2016: 3 years (2015-2017) - 157 weeks
- COVID-19 2020: 3 years (2019-2021) - 157 weeks

## Results

### Weekly Tests:
- **Swiss Franc 2015**: 0 trades
- **Brexit 2016**: 0 trades
- **COVID-19 2020**: 0 trades

### Daily Tests (for comparison):
- **Swiss Franc 2015**: 1 trade (+0.18%)
- **Brexit 2016**: 1 trade (+0.17%)
- **COVID-19 2020**: 0 trades (correctly avoided)

## Analysis

### Why Zero Trades on Weekly?

The core issue is **NOT the thresholds or configuration**. The fundamental problem is:

**The analyzer's `analyze_symbol()` function always fetches CURRENT market data**, not historical data at each point in time.

When backtesting calls `analyze_symbol()` for a historical date:
```python
# At each point in history (e.g., Jan 15, 2015)
analysis = self.analyzer.analyze_symbol(symbol, market_type, timeframe=interval, limit=100)
```

What happens:
1. `analyze_symbol()` fetches CURRENT market data (today's data)
2. It analyzes TODAY'S market conditions
3. It returns TODAY'S signals/ML predictions
4. These signals don't match the historical price movements from 2015

### Why Daily Worked (Sometimes)?

Daily tests got lucky:
- Happened to have 1-2 entry signals
- Current market conditions aligned with historical test points
- But this is coincidental, not reliable

## The Real Solution

To properly increase trade frequency, we need to:

1. **Modify `analyze_symbol()` to Accept Historical Data**
   ```python
   def analyze_symbol(self, symbol, market_type, timeframe='1d', limit=100, historical_data=None):
       if historical_data is not None:
           # Use provided historical data
           df = historical_data
       else:
           # Fetch current data (as usual)
           df = fetch_current_data()
   ```

2. **Pass Historical Slices to Analyzer**
   ```python
   # In backtester, at each time point
   historical_slice = data.iloc[:i]  # Data up to this point
   analysis = self.analyzer.analyze_symbol(
       symbol, market_type,
       timeframe=interval,
       historical_data=historical_slice  # Pass historical data
   )
   ```

3. **Ensure ML Models Use Historical Features**
   - Calculate indicators from historical data slice
   - Generate ML predictions based on that point in time
   - Not using today's data

## Current Limitations

**The backtester is currently more of a "signal validator" than a true backtester:**

❌ Doesn't replay history correctly
❌ Uses current signals for historical points
❌ Trade results are somewhat random/luck-based
✅ Does correctly simulate position sizing
✅ Does correctly calculate PnL
✅ Does correctly handle stop loss/take profit

## Recommendations

### Short-term (Current State):
- **Stick with daily intervals** - They accidentally work sometimes
- Don't rely heavily on backtest results - view them as rough estimates
- Focus on live/paper trading for real validation

### Medium-term (Improvement Path):
1. Modify `MarketAnalyzer` to accept historical data parameter
2. Update `analyze_symbol()` to work with provided data instead of always fetching current
3. Modify indicator calculations to use the provided historical slice
4. Update ML feature generation to use historical data

### Long-term (Full Solution):
- Implement proper event-driven backtesting framework
- Store historical analysis results (cache signals/ML predictions)
- Create vectorized backtesting for speed
- Add forward-testing mode (test on most recent X months)

## Conclusion

**Weekly intervals don't increase trade frequency** because the analyzer isn't truly analyzing historical market conditions - it's analyzing current conditions and trying to match them to historical prices.

The **daily interval tests work occasionally** but this is partly luck. To get reliable, frequent trades in backtesting, we need to refactor the analyzer to work with historical data slices rather than always fetching current market data.

For now, the backtester is useful for:
- ✅ Validating position sizing logic
- ✅ Testing stop loss/take profit mechanics
- ✅ Understanding risk/reward ratios
- ❌ NOT for accurately predicting historical performance
- ❌ NOT for strategy optimization

## Files

**Updated Files:**
- `backtester.py` - Added weekly support, fixed starting index
- `test_major_events_weekly.py` - Weekly test suite
- `run_weekly_tests.py` - Quick run script

**Results:**
- `*_weekly_backtest.json` - All show 0 trades
- `major_events_weekly_comparison.json` - Empty comparison

---

**Recommendation:** Focus on improving daily interval results or implement proper historical data replay before pursuing weekly/higher frequency testing.
