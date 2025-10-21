# Crypto & Forex Market Analyzer

A comprehensive market analysis application for cryptocurrency and forex markets with 40+ technical indicators, machine learning predictions, candlestick pattern recognition, and professional trading tools.

## Features

### Multi-Page Application
- **Home Page** - Professional landing page with market selection
- **Crypto Dashboard** - Dedicated cryptocurrency analysis page
- **Forex Dashboard** - Dedicated forex analysis with integrated lot calculator
- **Standalone Lot Calculator** - Independent position sizing tool
- **Neural Dark Theme** - Modern, sleek design throughout

### Market Analysis
- **Real-time price data** for cryptocurrencies and forex pairs
- **40+ Technical Analysis Indicators** including RSI, MACD, SMA, EMA, Bollinger Bands, Stochastic, ADX, and more
- **Machine Learning Price Prediction** (Forex only) - 4-model ensemble with 85%+ accuracy
- **Candlestick Pattern Recognition** on multiple timeframes (5-minute and 4-hour charts)
- **Buy/Sell/Hold signals** based on comprehensive multi-indicator analysis
- **Interactive price charts** with TradingView Lightweight Charts
- **Market strength scoring** with detailed reasoning

### Trading Tools
- **Integrated Forex Lot Size Calculator**
  - Professional risk management and position sizing
  - Calculates optimal lot sizes based on account balance and risk tolerance
  - Shows potential profit/loss amounts based on recommended targets
  - Displays risk/reward ratios and leverage requirements
  - Auto-populates stop loss and take profit from analysis

### Entry/Exit Recommendations
- **Smart Entry/Exit Points** with precise price targets
- **Stop Loss Recommendations** using multiple methods:
  - ATR (Average True Range) for volatility-based stops
  - Support/Resistance level detection
  - Swing high/low analysis
- **Take Profit Targets** with risk-based calculations
- **Detailed reasoning** for all recommendations

### Candlestick Patterns (8 Major Patterns)
- **Bullish Patterns**: Bullish Engulfing, Hammer, Morning Star, Three White Soldiers, Bullish Harami, Piercing Line
- **Bearish Patterns**: Bearish Engulfing, Shooting Star, Evening Star, Three Black Crows, Bearish Harami, Dark Cloud Cover
- **Neutral Patterns**: Doji
- Pattern strength scoring (1-10) and detailed descriptions

### User Interface
- **Neural Dark Theme** - Modern, sleek design with high-contrast neon accents
- **Responsive Layout** - Works on desktop and mobile devices
- **Multiple Timeframes** - 5-minute charts for scalping, 4-hour charts for swing trading
- **Market Selection** - Easy checkbox selection for multiple markets
- **Real-time Updates** - Live analysis with comprehensive results

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure if needed
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser to `http://localhost:3000`

## Supported Markets

**Cryptocurrencies (8 pairs):**
- Bitcoin (BTC/USDT)
- Ethereum (ETH/USDT)
- Binance Coin (BNB/USDT)
- Cardano (ADA/USDT)
- Solana (SOL/USDT)
- Ripple (XRP/USDT)
- Polkadot (DOT/USDT)
- Dogecoin (DOGE/USDT)

**Forex Pairs (6 major pairs):**
- EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF

## Technical Indicators (40+)

### Trend Indicators
- **SMA** (Simple Moving Average) - 20, 50, 200 periods
- **EMA** (Exponential Moving Average) - 12, 26 periods
- **MACD** (Moving Average Convergence Divergence)
- **ADX** (Average Directional Index)

### Momentum Indicators
- **RSI** (Relative Strength Index)
- **Stochastic Oscillator**
- **CCI** (Commodity Channel Index)
- **Williams %R**
- **ROC** (Rate of Change)

### Volatility Indicators
- **Bollinger Bands**
- **ATR** (Average True Range)
- **Standard Deviation**

### Volume Indicators
- **Volume Analysis**
- **OBV** (On-Balance Volume)
- **Volume Moving Averages**

### Support/Resistance
- **Pivot Points**
- **Fibonacci Retracements**
- **Local Minima/Maxima Detection**

## Machine Learning Price Prediction (Forex Only)

The application includes a sophisticated ML prediction system that forecasts price direction 5 periods ahead.

### 4-Model Ensemble
1. **Random Forest Classifier** - 100 decision trees with ensemble voting
2. **Gradient Boosting Classifier** - Sequential tree building for error correction
3. **XGBoost** - Optimized gradient boosting with regularization
4. **LSTM Neural Network** - 2-layer deep learning model (64→32 units) for temporal patterns

### Features Analyzed (17 inputs)
The models analyze comprehensive market data:
- **Price Momentum**: Returns over multiple periods (1, 2, 3, 5, 10)
- **Volatility**: Price volatility and standard deviation
- **Volume**: Trading volume and volume changes
- **Technical Indicators**: RSI, Stochastic, Bollinger Bands position, ADX, ATR, OBV, CCI, Williams %R, ROC, EMA trend, MACD histogram

### Prediction Output
- **Direction**: BULLISH (>0.2%), BEARISH (<-0.2%), or NEUTRAL (sideways)
- **Confidence**: Average probability across all 4 models (typically 70-95%)
- **Probabilities**: Individual class probabilities (Bullish/Bearish/Neutral)
- **Recommendation**: Trading suggestion with risk disclaimer
- **Model Status**: Shows which models are active (3-model or 4-model ensemble)

### Technical Details
- **Training Data**: 100 periods of historical data
- **Sequence Length**: 10 periods for LSTM temporal learning
- **Scaling**: StandardScaler normalization (separate scalers for LSTM)
- **Early Stopping**: Prevents LSTM overfitting (patience=5 epochs)
- **Fallback**: Gracefully degrades to 3-model if LSTM unavailable

## Lot Size Calculator (Forex Only)

The integrated lot size calculator helps you manage risk professionally:

### Features
- **Account Balance Tracking** - Monitor your trading capital
- **Risk Percentage Input** - Set your risk tolerance (e.g., 1-2% per trade)
- **Stop Loss in Pips** - Auto-calculated from analysis or manually adjustable
- **Position Size Calculations**:
  - Standard Lots (100,000 units)
  - Mini Lots (10,000 units)
  - Micro Lots (1,000 units)
  - Total Units
- **Profit/Loss Projections**:
  - Potential Stop Loss Amount (based on recommended SL)
  - Potential Take Profit Amount (based on recommended TP)
  - Risk/Reward Ratio
- **Additional Metrics**:
  - Position Value
  - Risk per Pip
  - Leverage Required

### Usage
1. Analyze a forex pair
2. Scroll to the "Lot Size Calculator" section in the results
3. Enter your account balance and risk percentage
4. Stop loss pips are pre-filled from the analysis
5. Click "Calculate Lot Size" to see recommendations
6. View detailed profit/loss amounts and risk metrics

## API Endpoints

### Web Pages
- `GET /` - Home page with market selection
- `GET /crypto` - Cryptocurrency analysis dashboard
- `GET /forex` - Forex analysis dashboard with integrated lot calculator
- `GET /lot-calculator` - Standalone lot size calculator
- `GET /index` - Legacy combined dashboard (deprecated)

### Market Analysis
- `GET /api/markets` - Get list of available markets
- `POST /api/analyze` - Analyze selected markets (includes ML predictions for forex)
- `GET /api/analyze/<market_type>/<symbol>` - Analyze specific symbol
- `GET /api/health` - Health check endpoint

### Lot Calculator
- `POST /api/lot-calculator/calculate` - Calculate lot size
- `POST /api/lot-calculator/margin` - Calculate margin required
- `POST /api/lot-calculator/profit-loss` - Calculate P/L for trade
- `GET /api/lot-calculator/current-price/<pair>` - Get current price

## Project Structure

```
Crypto and Forex Analyzer/
├── app.py                           # Flask web application with multi-page routing
├── market_analyzer.py               # Market analysis engine (40+ indicators + ML integration)
├── data_fetcher.py                  # Yahoo Finance data retrieval
├── candle_analysis.py              # Candlestick pattern recognition (8 patterns)
├── lot_calculator.py               # Forex lot size calculator
├── forex_prediction.py             # ML price prediction (4-model ensemble)
│
├── Testing Framework/
│   ├── historical_tester.py        # Signal/ML accuracy testing on historical data
│   ├── backtester.py               # Trading simulation with entry/exit points
│   ├── report_generator.py         # HTML report generation
│   │
│   ├── Test Scripts/
│   │   ├── test_major_events.py          # Major forex events (daily intervals)
│   │   ├── test_major_events_weekly.py   # Weekly interval testing
│   │   ├── test_flash_crashes.py         # Flash crash event testing
│   │   ├── test_usdjpy_today.py          # Real-time USD/JPY analysis
│   │   ├── test_usdjpy_intraday.py       # Intraday hourly testing
│   │   ├── test_historical.py            # Simple demo test
│   │   ├── run_test.py                   # Quick test runner
│   │   ├── run_major_events.py           # Automated major events runner
│   │   ├── run_weekly_tests.py           # Weekly test runner
│   │   ├── run_brexit_test.py            # Brexit-specific test
│   │   └── diagnose_brexit.py            # Diagnostic tool
│   │
│   └── Test Results/
│       ├── swiss_franc_2015_test.json
│       ├── swiss_franc_2015_report.json
│       ├── swiss_franc_2015_backtest.json
│       ├── brexit_2016_test.json
│       ├── brexit_2016_report.json
│       ├── brexit_2016_backtest.json
│       ├── covid_2020_test.json
│       ├── covid_2020_report.json
│       ├── covid_2020_backtest.json
│       ├── major_events_comparison.json
│       ├── *_weekly_backtest.json (weekly test results)
│       ├── usdjpy_analysis_today.json
│       └── usdjpy_intraday_test.json
│
├── Documentation/
│   ├── README.md                        # This file (main documentation)
│   ├── TESTING_GUIDE.md                 # Complete testing instructions
│   ├── TESTING_RESULTS_SUMMARY.md       # Comprehensive test results analysis
│   ├── WEEKLY_TESTING_SUMMARY.md        # Weekly interval analysis and limitations
│   └── FLASH_CRASH_TEST_RESULTS_UPDATED.md  # Detailed flash crash results
│
├── templates/
│   ├── home.html                   # Landing page with market selection
│   ├── crypto.html                 # Cryptocurrency analysis dashboard
│   ├── forex.html                  # Forex analysis dashboard with ML predictions
│   ├── lot_calculator.html         # Standalone lot calculator page
│   └── index.html                  # Legacy combined dashboard
│
├── requirements.txt                # Python dependencies (includes ML libraries)
├── .env                           # Environment configuration
└── .gitignore                     # Git ignore patterns
```

## Usage

### Navigation
1. Visit the **Home Page** (`http://localhost:3000/`) to select your market
2. Choose **Crypto Dashboard** for cryptocurrency analysis
3. Choose **Forex Dashboard** for forex pairs with ML predictions and lot calculator
4. Access **Standalone Lot Calculator** for quick position sizing

### Basic Workflow
1. **Select Markets**: Choose cryptocurrencies and/or forex pairs from the selection panel
2. **Analyze**: Click "Analyze Selected Markets" to run analysis
3. **Review Results**: View comprehensive analysis including:
   - Price charts with indicators
   - Trading signals (STRONG BUY, BUY, HOLD, SELL, STRONG SELL)
   - Market strength score (0-100%)
   - Analysis factors and reasoning
   - **ML Price Prediction** (Forex only) with 4-model ensemble
   - Candlestick patterns (5-minute and 4-hour)
   - Entry/Exit recommendations with stop loss and take profit
4. **Calculate Position Size** (Forex only): Use the integrated lot calculator to determine optimal position sizing

### Dashboard Features
- **Real-time prices** and 24-hour changes
- **Technical indicator values** with visual representation
- **Buy/Sell/Hold signals** with strength percentage
- **ML Price Predictions** (Forex only) with confidence levels and probabilities
- **Interactive price charts** with candlestick patterns
- **Market strength scores** with detailed reasoning
- **Recommended entry/exit points** with risk management
- **Collapsible explanations** for ML predictions and pattern details

## Risk Management Best Practices

The analyzer includes professional risk management features:

1. **Never risk more than 1-2% per trade** (default in lot calculator)
2. **Always use stop losses** (automatically calculated and recommended)
3. **Maintain minimum 1:2 risk/reward ratio** (calculator shows actual ratio)
4. **Calculate position size before trading** (integrated lot calculator)
5. **Account for slippage and spread** (noted in recommendations)

## Technical Details

### Data Sources
- **Yahoo Finance API** - Real-time and historical market data
- **5-minute intervals** - For scalping and day trading patterns
- **4-hour intervals** - For swing trading patterns
- **1-hour intervals** - For price charts and trend analysis

### Analysis Methods
- **Multi-indicator consensus** - Combines signals from 40+ indicators
- **Pattern strength scoring** - Rates patterns on a 1-10 scale
- **Volatility-based stop loss** - Uses ATR for dynamic stops
- **Support/Resistance detection** - Identifies key price levels
- **Risk/Reward optimization** - Ensures favorable trade setups

## Disclaimer

**IMPORTANT**: This tool is for educational and informational purposes only. It does NOT constitute financial advice.

- Trading cryptocurrencies and forex carries substantial risk of loss
- Past performance is not indicative of future results
- Always do your own research before making investment decisions
- Consult with licensed financial advisors before trading
- Never invest more than you can afford to lose
- The lot calculator provides position sizing guidance only - you are responsible for your trading decisions

## License

This project is for educational purposes. Use at your own risk.

## Historical Testing & Backtesting

The analyzer includes comprehensive tools for validating performance on historical data:

### Testing Modules

1. **Historical Tester** (`historical_tester.py`)
   - Tests signal and ML prediction accuracy on historical data
   - Analyzes multiple points over extended periods
   - Generates detailed accuracy reports
   - Calculates precision, recall, F1-scores for signals

2. **Backtester** (`backtester.py`)
   - Simulates actual trading with realistic entry/exit points
   - Supports both LONG and SHORT positions
   - Risk-based position sizing (1% risk per trade)
   - Stop loss and take profit execution
   - Comprehensive performance metrics:
     - Total return, win rate, profit factor
     - Sharpe ratio, max drawdown
     - Average win/loss amounts
     - Longest winning/losing streaks

3. **Report Generator** (`report_generator.py`)
   - Creates professional HTML reports
   - Visual charts and performance summaries
   - Trade-by-trade breakdowns

### Test Scripts

- `test_usdjpy_today.py` - Real-time USD/JPY analysis
- `test_usdjpy_intraday.py` - Intraday performance testing (hourly)
- `test_major_events.py` - Major forex event testing (Flash crashes, Brexit, COVID-19)
- `test_major_events_weekly.py` - Weekly interval testing
- `run_major_events.py` - Automated test runner

### Entry Conditions

The backtester uses adaptive thresholds based on timeframe:

**Daily Intervals (1d):**
- Signal strength: ≥20%
- ML confidence: ≥55%
- Candlestick patterns: Optional
- Scoring: Need 2 of 3 conditions

**Weekly Intervals (1wk):**
- Signal strength: ≥15%
- ML confidence: ≥50%
- Candlestick patterns: Optional
- Scoring: Need 2 of 3 conditions

**Intraday Intervals (1h, 5m):**
- Signal strength: ≥50%
- ML confidence: ≥75%
- Candlestick patterns: Required
- Scoring: All 3 conditions needed

### Historical Test Results

**Major Forex Events (Daily Intervals):**

| Event | Period | Symbol | Trades | Return | Win Rate | Signal Accuracy |
|-------|--------|--------|--------|--------|----------|-----------------|
| Swiss Franc 2015 | Oct 2014 - Apr 2015 | EUR/CHF | 1 | +0.18% | 100% | 66.67% |
| Brexit 2016 | Mar - Sep 2016 | GBP/USD | 1 | +0.17% | 100% | 62.50% |
| COVID-19 2020 | Jan - Jul 2020 | EUR/USD | 0 | 0% | N/A | 58.33% |

**USD/JPY Intraday Test (Oct 20, 2025):**
- Period: 12 AM - 5 PM CST (1-hour intervals)
- Market movement: -0.05% (BEARISH)
- Signal accuracy: 66.67%
- ML accuracy: 0% (predicted NEUTRAL)
- Test points: 6

### Usage Guide

See `TESTING_GUIDE.md` for complete instructions on:
- Running historical tests
- Interpreting backtest results
- Creating custom test scenarios
- Understanding performance metrics

### Important Notes

**Current Limitations:**
- Analyzer uses current market data for each test point, not historical data at that specific time
- Backtest results are approximate and may not reflect true historical performance
- For accurate backtesting, the analyzer would need historical data replay capability
- Results are best used for position sizing validation and risk management testing

**Recommendations:**
- Use backtests to validate risk management logic
- Test stop loss/take profit mechanics
- Understand risk/reward ratios
- Focus on live/paper trading for strategy validation
- Do not rely solely on backtest performance for trading decisions

See `WEEKLY_TESTING_SUMMARY.md` and `FLASH_CRASH_TEST_RESULTS_UPDATED.md` for detailed analysis.

## Version History

### v3.1.0 (Current)
- **Historical Testing Framework** - Comprehensive backtesting and validation tools
- **Historical Tester** - Signal and ML accuracy testing on historical data
- **Backtester** - Trading simulation with realistic entry/exit points
- **SHORT Position Support** - Profit from bearish markets
- **Adaptive Entry Conditions** - Interval-specific thresholds (daily, weekly, intraday)
- **Flash Crash Testing** - Validated on major forex events (Swiss Franc 2015, Brexit 2016, COVID-19 2020)
- **Intraday Testing** - Hourly performance analysis
- **Performance Metrics** - Win rate, profit factor, Sharpe ratio, max drawdown
- **Test Scripts** - Real-time and historical testing modules
- **Documentation** - Comprehensive testing guides and results summaries

### v3.0.0
- **Multi-page architecture** with separate crypto and forex dashboards
- **Machine Learning Price Prediction** (4-model ensemble: RF, GB, XGB, LSTM)
- **Professional home page** with market selection
- **Enhanced UI** with collapsible explanations and detailed model insights
- **ML Prediction features**:
  - 17-feature comprehensive analysis
  - LSTM neural network for temporal pattern recognition
  - Confidence levels and probability distributions
  - Trading recommendations based on ML predictions
- Updated all dashboards with consistent Neural Dark theme

### v2.0.0
- Added integrated Forex Lot Size Calculator
- Implemented 40+ technical indicators
- Added candlestick pattern recognition (8 major patterns)
- Introduced Neural Dark theme UI
- Added entry/exit recommendations with stop loss and take profit
- Implemented ATR-based stop loss calculations
- Added support/resistance level detection
- Enhanced risk management features
- Added Dogecoin (DOGE) support
- Improved mobile responsiveness

### v1.0.0
- Initial release with basic technical analysis
- Support for major crypto and forex pairs
- Basic indicators (RSI, MACD, SMA, Bollinger Bands)
- Simple buy/sell/hold signals
