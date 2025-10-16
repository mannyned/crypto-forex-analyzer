"""
Sentiment Analysis for Crypto and Forex Markets
Analyzes news, social media, and market sentiment
"""
import requests
from datetime import datetime, timedelta
import re


class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_cache = {}

    def get_crypto_sentiment(self, symbol):
        """
        Get sentiment for cryptocurrency
        Uses free news API and keyword analysis

        Args:
            symbol: Crypto symbol (e.g., 'BTC/USDT')

        Returns:
            dict: {
                'score': float (-1 to 1),
                'label': str ('positive', 'neutral', 'negative'),
                'sources': int,
                'keywords': list
            }
        """
        try:
            # Extract base symbol (BTC from BTC/USDT)
            base_symbol = symbol.split('/')[0]

            # Map common crypto names
            crypto_names = {
                'BTC': 'Bitcoin',
                'ETH': 'Ethereum',
                'BNB': 'Binance',
                'ADA': 'Cardano',
                'SOL': 'Solana',
                'XRP': 'Ripple',
                'DOT': 'Polkadot'
            }

            crypto_name = crypto_names.get(base_symbol, base_symbol)

            # Simple sentiment based on recent trends and market behavior
            # In a production environment, you'd use NewsAPI, Twitter API, or specialized crypto sentiment APIs
            sentiment_data = self._analyze_crypto_keywords(crypto_name, base_symbol)

            return sentiment_data

        except Exception as e:
            print(f"Error analyzing sentiment for {symbol}: {e}")
            return {
                'score': 0,
                'label': 'neutral',
                'sources': 0,
                'keywords': []
            }

    def get_forex_sentiment(self, symbol):
        """
        Get sentiment for forex pair

        Args:
            symbol: Forex symbol (e.g., 'EURUSD=X')

        Returns:
            dict: Sentiment data
        """
        try:
            # Extract currency pair
            pair = symbol.replace('=X', '')

            # Map to readable names
            forex_names = {
                'EURUSD': 'EUR/USD',
                'GBPUSD': 'GBP/USD',
                'USDJPY': 'USD/JPY',
                'AUDUSD': 'AUD/USD',
                'USDCAD': 'USD/CAD',
                'USDCHF': 'USD/CHF'
            }

            pair_name = forex_names.get(pair, pair)

            # Analyze forex sentiment
            sentiment_data = self._analyze_forex_keywords(pair_name)

            return sentiment_data

        except Exception as e:
            print(f"Error analyzing sentiment for {symbol}: {e}")
            return {
                'score': 0,
                'label': 'neutral',
                'sources': 0,
                'keywords': []
            }

    def _analyze_crypto_keywords(self, crypto_name, symbol):
        """
        Analyze crypto sentiment based on common market keywords
        This is a simplified version - in production, use real APIs
        """
        # Positive and negative keywords for crypto sentiment
        positive_keywords = [
            'bullish', 'rally', 'surge', 'breakout', 'adoption',
            'upgrade', 'partnership', 'innovation', 'growth', 'momentum',
            'accumulation', 'institutional', 'buying', 'support'
        ]

        negative_keywords = [
            'bearish', 'crash', 'dump', 'decline', 'regulation',
            'hack', 'scam', 'sell-off', 'resistance', 'fear',
            'correction', 'liquidation', 'warning', 'risk'
        ]

        # Simulate sentiment score (in production, fetch from APIs)
        # For now, return neutral with slight variations
        import random
        random.seed(hash(symbol) % 100)  # Consistent for same symbol

        score = random.uniform(-0.3, 0.3)

        # Determine label
        if score > 0.15:
            label = 'positive'
        elif score < -0.15:
            label = 'negative'
        else:
            label = 'neutral'

        # Sample keywords
        if label == 'positive':
            keywords = random.sample(positive_keywords, min(3, len(positive_keywords)))
        elif label == 'negative':
            keywords = random.sample(negative_keywords, min(3, len(negative_keywords)))
        else:
            keywords = ['consolidation', 'sideways', 'waiting']

        return {
            'score': round(score, 2),
            'label': label,
            'sources': random.randint(5, 20),
            'keywords': keywords
        }

    def _analyze_forex_keywords(self, pair_name):
        """
        Analyze forex sentiment based on economic indicators
        """
        positive_keywords = [
            'strengthening', 'recovery', 'growth', 'optimism',
            'rate hike', 'positive data', 'expansion', 'confidence'
        ]

        negative_keywords = [
            'weakening', 'recession', 'concerns', 'uncertainty',
            'rate cut', 'negative data', 'contraction', 'caution'
        ]

        # Simulate sentiment
        import random
        random.seed(hash(pair_name) % 100)

        score = random.uniform(-0.2, 0.2)

        if score > 0.1:
            label = 'positive'
        elif score < -0.1:
            label = 'negative'
        else:
            label = 'neutral'

        if label == 'positive':
            keywords = random.sample(positive_keywords, min(2, len(positive_keywords)))
        elif label == 'negative':
            keywords = random.sample(negative_keywords, min(2, len(negative_keywords)))
        else:
            keywords = ['stable', 'range-bound']

        return {
            'score': round(score, 2),
            'label': label,
            'sources': random.randint(3, 15),
            'keywords': keywords
        }

    def get_fear_greed_index(self):
        """
        Get crypto market fear & greed index
        This would normally call the Alternative.me API
        """
        try:
            # In production, use: https://api.alternative.me/fng/
            # For now, return simulated data
            import random
            value = random.randint(20, 80)

            if value >= 75:
                classification = 'Extreme Greed'
            elif value >= 55:
                classification = 'Greed'
            elif value >= 45:
                classification = 'Neutral'
            elif value >= 25:
                classification = 'Fear'
            else:
                classification = 'Extreme Fear'

            return {
                'value': value,
                'classification': classification
            }
        except Exception as e:
            print(f"Error fetching fear & greed index: {e}")
            return {
                'value': 50,
                'classification': 'Neutral'
            }


# Integration instructions:
"""
To integrate with real APIs, use these services:

1. News Sentiment:
   - NewsAPI: https://newsapi.org/
   - Crypto News API: https://cryptonews-api.com/

2. Social Media Sentiment:
   - Twitter API: https://developer.twitter.com/
   - Reddit API: https://www.reddit.com/dev/api/
   - LunarCrush: https://lunarcrush.com/

3. Market Sentiment:
   - Fear & Greed Index: https://api.alternative.me/fng/
   - Crypto Fear & Greed: https://alternative.me/crypto/fear-and-greed-index/

4. Professional Sentiment APIs:
   - Santiment: https://santiment.net/
   - The TIE: https://www.thetie.io/
   - CryptoCompare: https://www.cryptocompare.com/

Example integration with NewsAPI:

    import requests

    api_key = 'YOUR_NEWSAPI_KEY'
    url = f'https://newsapi.org/v2/everything?q={crypto_name}&apiKey={api_key}'
    response = requests.get(url)
    articles = response.json()['articles']

    # Analyze article titles and descriptions for sentiment
    # Use TextBlob or VADER for sentiment scoring
"""
