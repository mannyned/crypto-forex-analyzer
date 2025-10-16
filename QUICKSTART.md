# Quick Start Guide

## Installation

1. Navigate to the project directory:
```bash
cd C:\Users\Manny\market-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file if you want to customize settings:
```bash
copy .env.example .env
```

## Running the Application

### Option 1: Web Dashboard (Recommended)

Start the web dashboard:
```bash
python app.py
```

Then open your browser to: http://localhost:5000

Click "Analyze Markets" to get real-time analysis of crypto and forex markets!

### Option 2: Command Line Interface

Analyze all markets:
```bash
python run_analysis.py --all
```

Analyze specific cryptocurrency:
```bash
python run_analysis.py --crypto BTC/USDT
```

Analyze specific forex pair:
```bash
python run_analysis.py --forex EURUSD=X
```

Get investment recommendations:
```bash
python run_analysis.py --recommend --risk medium
```

Export results to JSON:
```bash
python run_analysis.py --all --export results.json
```

## What You'll Get

### Technical Indicators
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
- **MACD**: Trend following and momentum indicator
- **Moving Averages**: SMA and EMA for trend identification
- **Bollinger Bands**: Volatility and price level analysis
- **Stochastic Oscillator**: Momentum indicator
- **ATR**: Volatility measurement

### Trading Signals
- **STRONG BUY**: Multiple bullish indicators aligned
- **BUY**: Positive trend with good entry opportunity
- **HOLD**: No clear direction, wait for better signal
- **SELL**: Bearish indicators suggest exit
- **STRONG SELL**: Multiple bearish indicators aligned

### Markets Analyzed

**Cryptocurrencies:**
- BTC/USDT (Bitcoin)
- ETH/USDT (Ethereum)
- BNB/USDT (Binance Coin)
- ADA/USDT (Cardano)
- SOL/USDT (Solana)
- XRP/USDT (Ripple)
- DOT/USDT (Polkadot)

**Forex Pairs:**
- EURUSD (Euro/US Dollar)
- GBPUSD (British Pound/US Dollar)
- USDJPY (US Dollar/Japanese Yen)
- AUDUSD (Australian Dollar/US Dollar)
- USDCAD (US Dollar/Canadian Dollar)
- USDCHF (US Dollar/Swiss Franc)

## Understanding the Dashboard

### Top Opportunities Tab
Shows the best potential investments ranked by signal strength and multiple technical indicators.

### Cryptocurrencies Tab
Detailed analysis of all tracked crypto pairs with:
- Current price and 24h change
- Trading signal (Buy/Sell/Hold)
- Key technical indicators
- Analysis reasons

### Forex Tab
Same comprehensive analysis for forex pairs.

## Tips for Using the App

1. **Check Multiple Timeframes**: The default analysis uses 1-hour data. For longer-term investments, you may want to modify the timeframe in the code.

2. **Don't Rely on Single Indicators**: The app combines multiple indicators to give you a holistic view. Pay attention to the "Analysis Factors" section.

3. **Consider the Strength Score**: Higher strength scores (70+) indicate stronger conviction in the signal.

4. **Risk Management**: Always use stop-losses and take-profits. The app provides suggestions in the recommendations.

5. **Market Conditions**: Technical analysis works best in trending markets. In highly volatile or news-driven conditions, use additional caution.

## Troubleshooting

### "Module not found" errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### API Rate Limits
If you're getting rate limit errors, add delays between requests or use API keys in the `.env` file.

### No data returned
Check your internet connection. The app requires connectivity to fetch market data from Binance and Yahoo Finance.

## Disclaimer

**IMPORTANT**: This tool is for educational and informational purposes only. It does NOT constitute financial advice. Trading cryptocurrencies and forex carries substantial risk of loss. Always:

- Do your own research
- Never invest more than you can afford to lose
- Consult with licensed financial advisors
- Understand that past performance doesn't guarantee future results
- Be aware of the high volatility in crypto markets

## Next Steps

- Customize the watched symbols in `data_fetcher.py`
- Adjust indicator parameters in `technical_indicators.py`
- Modify signal generation logic in `market_analyzer.py`
- Add portfolio tracking features using `portfolio.py`

Happy analyzing! 📊
