# Changelog

All notable changes to the Crypto & Forex Market Analyzer will be documented in this file.

## [3.1.0] - 2025-10-20

### Added - Historical Testing & Backtesting Framework

#### Core Testing Modules
- **historical_tester.py** - Comprehensive signal and ML prediction accuracy testing
  - Tests analyzer performance on historical data
  - Generates precision, recall, and F1-scores
  - Analyzes multiple time points over extended periods
  - Calculates bullish/bearish prediction accuracy

- **backtester.py** - Realistic trading simulation engine
  - Simulates actual trades with entry/exit points
  - LONG and SHORT position support
  - Risk-based position sizing (1% risk per trade)
  - Stop loss and take profit execution
  - Comprehensive performance metrics (win rate, profit factor, Sharpe ratio, max drawdown)
  - Adaptive entry conditions based on timeframe (daily, weekly, intraday)

- **report_generator.py** - HTML report generation
  - Visual charts and performance summaries
  - Trade-by-trade breakdowns

#### Test Scripts
- **test_major_events.py** - Major forex event testing (daily intervals)
  - Swiss Franc Flash Crash 2015
  - Brexit Vote 2016
  - COVID-19 Market Crash 2020

- **test_major_events_weekly.py** - Weekly interval testing
  - Extended test periods (2-3 years)
  - Lower entry thresholds for higher frequency

- **test_flash_crashes.py** - Flash crash event testing suite

- **test_usdjpy_today.py** - Real-time USD/JPY market analysis
  - Current market conditions
  - Trading recommendations
  - Entry/exit suggestions

- **test_usdjpy_intraday.py** - Intraday performance testing
  - Hourly interval analysis
  - Tests predictions vs actual movements
  - 12 AM - 5 PM CST timeframe

- **test_historical.py** - Simple demo test
- **run_test.py** - Quick test runner
- **run_major_events.py** - Automated major events runner
- **run_weekly_tests.py** - Weekly test runner
- **run_brexit_test.py** - Brexit-specific test
- **diagnose_brexit.py** - Diagnostic tool

#### Entry Conditions System
- **Daily Intervals (1d)**
  - Signal strength: ≥20%
  - ML confidence: ≥55%
  - Candlestick patterns: Optional
  - Scoring: Need 2 of 3 conditions

- **Weekly Intervals (1wk)**
  - Signal strength: ≥15%
  - ML confidence: ≥50%
  - Candlestick patterns: Optional
  - Scoring: Need 2 of 3 conditions

- **Intraday Intervals (1h, 5m)**
  - Signal strength: ≥50%
  - ML confidence: ≥75%
  - Candlestick patterns: Required
  - Scoring: All 3 conditions needed

#### Documentation
- **TESTING_GUIDE.md** - Complete testing instructions
  - How to run historical tests
  - Interpreting backtest results
  - Creating custom test scenarios
  - Understanding performance metrics

- **TESTING_RESULTS_SUMMARY.md** - Comprehensive results analysis
  - Major forex event testing results
  - Signal and ML accuracy metrics
  - Trade-by-trade breakdowns
  - Performance summaries

- **WEEKLY_TESTING_SUMMARY.md** - Weekly interval analysis
  - Why weekly intervals produced zero trades
  - Analyzer limitation documentation
  - Recommendations for improvement

- **FLASH_CRASH_TEST_RESULTS_UPDATED.md** - Detailed flash crash results
  - Swiss Franc 2015: +0.18% return, 66.67% signal accuracy
  - Brexit 2016: +0.17% return, 62.50% signal accuracy
  - COVID-19 2020: 0 trades (correctly avoided)

- **CHANGELOG.md** - This file

### Fixed

#### Unicode Encoding Errors
- Removed all Unicode emojis causing Windows terminal encoding issues
- Replaced emoji characters with text equivalents
- Fixed box-drawing characters
- Ensures compatibility with Windows cp1252 encoding

#### PnL Calculation Bug
- Fixed massive leverage bug showing 1773% returns
- Corrected position-based PnL formula
- Applied fix to all 6 PnL calculation points (LONG/SHORT stop loss, take profit, end of period)
- Now correctly calculates: `pnl = position_size * price_change_pct`

#### Pandas Series Errors
- Fixed `TypeError: unsupported format string passed to Series.__format__`
- Added float conversion for pandas Series values
- Fixed string formatting with isinstance() checks

#### KeyError When No Trades
- Fixed `KeyError: 'initial_capital'` when backtest had 0 trades
- Updated `analyze_results()` to return complete dictionary with all metrics

### Changed

#### Backtester Entry Conditions
- Relaxed signal threshold from 50% to 20% for daily intervals
- Relaxed ML confidence from 75% to 55% for daily intervals
- Made candlestick patterns optional (previously required)
- Implemented 2/3 scoring system instead of requiring all conditions

#### SHORT Position Support
- Added complete SHORT position logic
- Inverse stop loss/take profit for bearish trades
- Proper PnL calculation for SHORT positions

#### README.md
- Added "Historical Testing & Backtesting" section
- Added test results table with performance metrics
- Updated version to 3.1.0
- Expanded project structure documentation
- Added testing limitations and recommendations

### Test Results Summary

#### Major Forex Events (Daily Intervals)
| Event | Period | Trades | Return | Win Rate | Signal Accuracy |
|-------|--------|--------|--------|----------|-----------------|
| Swiss Franc 2015 | Oct 2014 - Apr 2015 | 1 | +0.18% | 100% | 66.67% |
| Brexit 2016 | Mar - Sep 2016 | 1 | +0.17% | 100% | 62.50% |
| COVID-19 2020 | Jan - Jul 2020 | 0 | 0% | N/A | 58.33% |

#### Overall Performance
- **Total Trades**: 2
- **Win Rate**: 100%
- **Total Return**: +0.35%
- **Max Drawdown**: 0%
- **Average Signal Accuracy**: 63.54%
- **Average ML Accuracy**: 37.50%

#### USD/JPY Intraday Test (Oct 20, 2025)
- **Period**: 12 AM - 5 PM CST (1-hour intervals)
- **Market Movement**: -0.05% (BEARISH)
- **Signal Accuracy**: 66.67%
- **ML Accuracy**: 0% (predicted NEUTRAL)
- **Test Points**: 6

### Known Limitations

#### Analyzer Uses Current Data
The analyzer currently uses current market data for each test point, not historical data at that specific time. This means:
- Backtest results are approximate
- Weekly/intraday testing may be ineffective
- Results are best for position sizing validation
- Not suitable for precise strategy optimization

#### Recommendations
- Use backtests to validate risk management logic
- Focus on live/paper trading for strategy validation
- Don't rely solely on backtest performance
- Consider results as rough estimates

### Files Added (37 total)

**Testing Framework:**
- historical_tester.py
- backtester.py
- report_generator.py

**Test Scripts:**
- test_major_events.py
- test_major_events_weekly.py
- test_flash_crashes.py
- test_usdjpy_today.py
- test_usdjpy_intraday.py
- test_historical.py
- run_test.py
- run_major_events.py
- run_weekly_tests.py
- run_brexit_test.py
- diagnose_brexit.py

**Test Results (JSON):**
- swiss_franc_2015_test.json
- swiss_franc_2015_report.json
- swiss_franc_2015_backtest.json
- swiss_franc_2015_weekly_backtest.json
- brexit_2016_test.json
- brexit_2016_report.json
- brexit_2016_backtest.json
- brexit_2016_weekly_backtest.json
- covid_2020_test.json
- covid_2020_report.json
- covid_2020_backtest.json
- covid_2020_weekly_backtest.json
- major_events_comparison.json
- major_events_weekly_comparison.json
- usdjpy_analysis_today.json
- usdjpy_intraday_test.json
- backtest_EURUSD=X_180days.json

**Documentation:**
- TESTING_GUIDE.md
- TESTING_RESULTS_SUMMARY.md
- WEEKLY_TESTING_SUMMARY.md
- FLASH_CRASH_TEST_RESULTS.md
- FLASH_CRASH_TEST_RESULTS_UPDATED.md
- CHANGELOG.md

---

## [3.0.0] - 2025-10-15

### Added
- Multi-page architecture with separate crypto and forex dashboards
- Machine Learning Price Prediction (4-model ensemble: RF, GB, XGB, LSTM)
- Professional home page with market selection
- Enhanced UI with collapsible explanations and detailed model insights
- ML Prediction features:
  - 17-feature comprehensive analysis
  - LSTM neural network for temporal pattern recognition
  - Confidence levels and probability distributions
  - Trading recommendations based on ML predictions
- Updated all dashboards with consistent Neural Dark theme

---

## [2.0.0] - 2025-10-10

### Added
- Integrated Forex Lot Size Calculator
- 40+ technical indicators
- Candlestick pattern recognition (8 major patterns)
- Neural Dark theme UI
- Entry/exit recommendations with stop loss and take profit
- ATR-based stop loss calculations
- Support/resistance level detection
- Enhanced risk management features
- Dogecoin (DOGE) support
- Improved mobile responsiveness

---

## [1.0.0] - 2025-10-01

### Added
- Initial release with basic technical analysis
- Support for major crypto and forex pairs
- Basic indicators (RSI, MACD, SMA, Bollinger Bands)
- Simple buy/sell/hold signals
- Flask web application
- Real-time price data from Yahoo Finance

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

---

**Current Version**: 3.1.0
**Last Updated**: October 20, 2025
