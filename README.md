# Crypto & Forex Market Analyzer

A comprehensive market analysis application for cryptocurrency and forex markets with technical indicators and investment signals.

## Features

- Real-time price data for cryptocurrencies and forex pairs
- Technical analysis indicators (RSI, MACD, SMA, EMA, Bollinger Bands)
- Buy/Sell/Hold signals based on multiple indicators
- Interactive web dashboard with charts
- Market trend analysis and recommendations
- Support for multiple crypto and forex pairs

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
5. Open your browser to `http://localhost:5000`

## Supported Markets

**Cryptocurrencies:**
- BTC/USDT, ETH/USDT, BNB/USDT, ADA/USDT, SOL/USDT, XRP/USDT, DOT/USDT

**Forex Pairs:**
- EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF

## Technical Indicators

- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Trend following momentum indicator
- **SMA/EMA (Simple/Exponential Moving Averages)**: Trend identification
- **Bollinger Bands**: Volatility and price level indicator
- **Volume Analysis**: Trading volume trends

## Usage

The dashboard displays:
- Current prices and 24h changes
- Technical indicator values
- Buy/Sell/Hold signals
- Price charts with indicators
- Market strength scores

## Disclaimer

This tool is for educational and informational purposes only. It does not constitute financial advice. Always do your own research and consult with financial advisors before making investment decisions.
