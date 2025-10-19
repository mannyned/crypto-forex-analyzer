# Crypto & Forex Market Analyzer

A comprehensive market analysis application for cryptocurrency and forex markets with 40+ technical indicators, candlestick pattern recognition, and professional trading tools.

## Features

### Market Analysis
- **Real-time price data** for cryptocurrencies and forex pairs
- **40+ Technical Analysis Indicators** including RSI, MACD, SMA, EMA, Bollinger Bands, Stochastic, ADX, and more
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

### Market Analysis
- `GET /api/markets` - Get list of available markets
- `POST /api/analyze` - Analyze selected markets
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
├── app.py                      # Flask web application
├── market_analyzer.py          # Market analysis engine (40+ indicators)
├── data_fetcher.py            # Yahoo Finance data retrieval
├── candle_analysis.py         # Candlestick pattern recognition
├── lot_calculator.py          # Forex lot size calculator
├── templates/
│   ├── index.html             # Main dashboard (Neural Dark theme)
│   └── lot_calculator.html    # Standalone lot calculator page
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
└── README.md                  # This file
```

## Usage

### Basic Workflow
1. **Select Markets**: Choose cryptocurrencies and/or forex pairs from the selection panel
2. **Analyze**: Click "Analyze Selected Markets" to run analysis
3. **Review Results**: View comprehensive analysis including:
   - Price charts with indicators
   - Trading signals (STRONG BUY, BUY, HOLD, SELL, STRONG SELL)
   - Market strength score (0-100%)
   - Analysis factors and reasoning
   - Candlestick patterns (5-minute and 4-hour)
   - Entry/Exit recommendations with stop loss and take profit
4. **Calculate Position Size** (Forex only): Use the integrated lot calculator to determine optimal position sizing

### Dashboard Features
- **Real-time prices** and 24-hour changes
- **Technical indicator values** with visual representation
- **Buy/Sell/Hold signals** with strength percentage
- **Interactive price charts** with candlestick patterns
- **Market strength scores** with detailed reasoning
- **Recommended entry/exit points** with risk management

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

## Version History

### v2.0.0 (Current)
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
