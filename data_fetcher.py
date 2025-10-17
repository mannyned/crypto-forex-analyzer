"""
Data fetcher for cryptocurrency and forex market data
Updated to use Yahoo Finance for crypto (no geo-restrictions)
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

class DataFetcher:
    def __init__(self):
        pass

    def fetch_crypto_data(self, symbol, timeframe='1h', limit=100):
        """
        Fetch cryptocurrency data from Yahoo Finance

        Args:
            symbol: Trading pair (e.g., 'BTC-USD')
            timeframe: Timeframe for candles (e.g., '1h', '4h', '1d')
            limit: Number of candles to fetch

        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Convert symbol format for Yahoo Finance
            if '/' in symbol:
                symbol = symbol.replace('/USDT', '-USD').replace('/', '-')

            # Map timeframe
            interval_map = {'5m': '5m', '15m': '15m', '1h': '1h', '4h': '4h', '1d': '1d'}
            interval = interval_map.get(timeframe, '1h')

            # Calculate period based on limit
            if interval == '5m':
                period = '5d' if limit <= 100 else '7d'
            elif interval == '15m':
                period = '5d' if limit <= 100 else '7d'
            elif interval == '1h':
                period = '1mo' if limit <= 120 else '3mo'
            elif interval == '4h':
                period = '1mo' if limit <= 180 else '3mo'
            else:
                period = '1mo' if limit <= 30 else ('3mo' if limit <= 90 else '1y')

            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                print(f"No data returned for {symbol}")
                return None

            # Rename columns to match expected format
            df.columns = df.columns.str.lower()
            df = df.rename(columns={'dividends': 'dividend', 'stock splits': 'stock_split'})

            # Ensure we have required columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                print(f"Missing required columns for {symbol}")
                return None

            return df.tail(limit)  # Return only requested number of candles

        except Exception as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            return None

    def fetch_forex_data(self, symbol, period='60d', interval='1h'):
        """
        Fetch forex data from Yahoo Finance

        Args:
            symbol: Forex pair (e.g., 'EURUSD=X')
            period: Time period (e.g., '60d', '1y')
            interval: Data interval (e.g., '1h', '1d')

        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                print(f"No data returned for {symbol}")
                return None

            # Rename columns to match crypto format
            df.columns = df.columns.str.lower()

            return df
        except Exception as e:
            print(f"Error fetching forex data for {symbol}: {e}")
            return None

    def get_current_price(self, symbol, market_type='crypto'):
        """
        Get current price for a symbol

        Args:
            symbol: Trading symbol
            market_type: 'crypto' or 'forex'

        Returns:
            Current price or None
        """
        try:
            if market_type == 'crypto':
                # Convert to Yahoo Finance format
                if '/' in symbol:
                    symbol = symbol.replace('/USDT', '-USD').replace('/', '-')

            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            if not data.empty:
                return data['Close'].iloc[-1]
        except Exception as e:
            print(f"Error fetching current price for {symbol}: {e}")
            return None

    def get_24h_change(self, symbol, market_type='crypto'):
        """
        Get 24h price change percentage

        Args:
            symbol: Trading symbol
            market_type: 'crypto' or 'forex'

        Returns:
            24h change percentage or None
        """
        try:
            if market_type == 'crypto':
                # Convert to Yahoo Finance format
                if '/' in symbol:
                    symbol = symbol.replace('/USDT', '-USD').replace('/', '-')

            ticker = yf.Ticker(symbol)
            data = ticker.history(period='5d', interval='1h')
            if len(data) >= 24:
                old_price = data['Close'].iloc[-24]
                new_price = data['Close'].iloc[-1]
                return ((new_price - old_price) / old_price) * 100
        except Exception as e:
            print(f"Error fetching 24h change for {symbol}: {e}")
            return None


# Supported markets (Yahoo Finance format)
CRYPTO_PAIRS = [
    'BTC/USDT',   # Will convert to BTC-USD
    'ETH/USDT',   # Will convert to ETH-USD
    'BNB/USDT',   # Will convert to BNB-USD
    'ADA/USDT',   # Will convert to ADA-USD
    'SOL/USDT',   # Will convert to SOL-USD
    'XRP/USDT',   # Will convert to XRP-USD
    'DOT/USDT'    # Will convert to DOT-USD
]

FOREX_PAIRS = [
    'EURUSD=X',
    'GBPUSD=X',
    'USDJPY=X',
    'AUDUSD=X',
    'USDCAD=X',
    'USDCHF=X'
]

# Friendly names for display
CRYPTO_NAMES = {
    'BTC/USDT': 'Bitcoin',
    'ETH/USDT': 'Ethereum',
    'BNB/USDT': 'Binance Coin',
    'ADA/USDT': 'Cardano',
    'SOL/USDT': 'Solana',
    'XRP/USDT': 'Ripple',
    'DOT/USDT': 'Polkadot'
}

FOREX_NAMES = {
    'EURUSD=X': 'EUR/USD',
    'GBPUSD=X': 'GBP/USD',
    'USDJPY=X': 'USD/JPY',
    'AUDUSD=X': 'AUD/USD',
    'USDCAD=X': 'USD/CAD',
    'USDCHF=X': 'USD/CHF'
}
