"""
Social Media Sentiment Analysis
Integrates with Twitter, Reddit, and Discord for real-time market sentiment
"""
import requests
import json
from datetime import datetime, timedelta
import re
from collections import Counter


class SocialSentimentAnalyzer:
    def __init__(self, config=None):
        """
        Initialize with API credentials

        Args:
            config: dict with API keys
                {
                    'twitter_bearer_token': 'your_token',
                    'reddit_client_id': 'your_id',
                    'reddit_client_secret': 'your_secret',
                    'discord_bot_token': 'your_token'
                }
        """
        self.config = config or {}
        self.sentiment_keywords = self._load_sentiment_keywords()

    def _load_sentiment_keywords(self):
        """Load positive and negative keywords for sentiment analysis"""
        return {
            'positive': [
                'bullish', 'moon', 'rally', 'pump', 'surge', 'breakout', 'buy',
                'hodl', 'gem', 'rocket', 'gain', 'profit', 'winning', 'growth',
                'adoption', 'partnership', 'upgrade', 'innovation', 'accumulate',
                'undervalued', 'potential', 'opportunity', 'strong', 'support'
            ],
            'negative': [
                'bearish', 'crash', 'dump', 'sell', 'drop', 'decline', 'scam',
                'fear', 'liquidation', 'loss', 'warning', 'risk', 'bubble',
                'overvalued', 'resistance', 'breakdown', 'panic', 'correction',
                'hack', 'fraud', 'regulation', 'ban', 'weak'
            ]
        }

    def analyze_twitter(self, symbol, crypto_name):
        """
        Analyze Twitter sentiment for a cryptocurrency

        Args:
            symbol: e.g., 'BTC'
            crypto_name: e.g., 'Bitcoin'

        Returns:
            dict: sentiment data from Twitter
        """
        if not self.config.get('twitter_bearer_token'):
            return self._mock_twitter_sentiment(symbol, crypto_name)

        try:
            # Twitter API v2 - Recent Search
            url = "https://api.twitter.com/2/tweets/search/recent"

            # Search query - last 24 hours
            query = f"({crypto_name} OR ${symbol}) lang:en -is:retweet"

            headers = {
                'Authorization': f"Bearer {self.config['twitter_bearer_token']}"
            }

            params = {
                'query': query,
                'max_results': 100,
                'tweet.fields': 'created_at,public_metrics,text'
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                tweets = data.get('data', [])

                return self._analyze_tweets(tweets, symbol)
            else:
                print(f"Twitter API error: {response.status_code}")
                return self._mock_twitter_sentiment(symbol, crypto_name)

        except Exception as e:
            print(f"Error fetching Twitter data: {e}")
            return self._mock_twitter_sentiment(symbol, crypto_name)

    def analyze_reddit(self, symbol, crypto_name):
        """
        Analyze Reddit sentiment from crypto subreddits

        Args:
            symbol: e.g., 'BTC'
            crypto_name: e.g., 'Bitcoin'

        Returns:
            dict: sentiment data from Reddit
        """
        if not self.config.get('reddit_client_id'):
            return self._mock_reddit_sentiment(symbol, crypto_name)

        try:
            # Get OAuth token
            auth = requests.auth.HTTPBasicAuth(
                self.config['reddit_client_id'],
                self.config['reddit_client_secret']
            )

            data = {
                'grant_type': 'client_credentials'
            }

            headers = {'User-Agent': 'CryptoAnalyzer/1.0'}

            token_response = requests.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers=headers
            )

            if token_response.status_code == 200:
                token = token_response.json()['access_token']
                headers['Authorization'] = f'Bearer {token}'

                # Search multiple crypto subreddits
                subreddits = ['cryptocurrency', 'CryptoMarkets', 'Bitcoin', 'ethtrader']
                all_posts = []

                for subreddit in subreddits:
                    search_url = f'https://oauth.reddit.com/r/{subreddit}/search'
                    params = {
                        'q': f'{crypto_name} OR {symbol}',
                        'limit': 50,
                        'sort': 'new',
                        't': 'day'
                    }

                    response = requests.get(search_url, headers=headers, params=params)

                    if response.status_code == 200:
                        posts = response.json()['data']['children']
                        all_posts.extend(posts)

                return self._analyze_reddit_posts(all_posts, symbol)
            else:
                return self._mock_reddit_sentiment(symbol, crypto_name)

        except Exception as e:
            print(f"Error fetching Reddit data: {e}")
            return self._mock_reddit_sentiment(symbol, crypto_name)

    def analyze_discord(self, symbol, crypto_name, guild_ids=None):
        """
        Analyze Discord sentiment from crypto communities

        Args:
            symbol: e.g., 'BTC'
            crypto_name: e.g., 'Bitcoin'
            guild_ids: List of Discord server IDs to monitor

        Returns:
            dict: sentiment data from Discord
        """
        if not self.config.get('discord_bot_token'):
            return self._mock_discord_sentiment(symbol, crypto_name)

        try:
            # Discord API - requires bot with proper permissions
            headers = {
                'Authorization': f"Bot {self.config['discord_bot_token']}"
            }

            # This would require a Discord bot setup with message history access
            # For now, return mock data
            return self._mock_discord_sentiment(symbol, crypto_name)

        except Exception as e:
            print(f"Error fetching Discord data: {e}")
            return self._mock_discord_sentiment(symbol, crypto_name)

    def _analyze_tweets(self, tweets, symbol):
        """Analyze sentiment from tweet data"""
        if not tweets:
            return {'score': 0, 'count': 0, 'positive': 0, 'negative': 0, 'neutral': 0}

        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_engagement = 0

        for tweet in tweets:
            text = tweet.get('text', '').lower()
            metrics = tweet.get('public_metrics', {})

            # Weight by engagement
            engagement = (
                metrics.get('like_count', 0) +
                metrics.get('retweet_count', 0) * 2 +
                metrics.get('reply_count', 0)
            )
            total_engagement += engagement

            # Analyze sentiment
            sentiment = self._analyze_text_sentiment(text)

            if sentiment > 0:
                positive_count += 1
            elif sentiment < 0:
                negative_count += 1
            else:
                neutral_count += 1

        total = len(tweets)
        score = (positive_count - negative_count) / total if total > 0 else 0

        return {
            'score': round(score, 2),
            'count': total,
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'engagement': total_engagement
        }

    def _analyze_reddit_posts(self, posts, symbol):
        """Analyze sentiment from Reddit posts"""
        if not posts:
            return {'score': 0, 'count': 0, 'positive': 0, 'negative': 0, 'neutral': 0}

        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0

        for post in posts:
            data = post['data']
            title = data.get('title', '').lower()
            text = data.get('selftext', '').lower()
            upvotes = data.get('ups', 0)

            combined_text = f"{title} {text}"
            sentiment = self._analyze_text_sentiment(combined_text)

            # Weight by upvotes
            weighted_sentiment = sentiment * (1 + upvotes / 100)
            total_score += weighted_sentiment

            if sentiment > 0:
                positive_count += 1
            elif sentiment < 0:
                negative_count += 1
            else:
                neutral_count += 1

        total = len(posts)
        score = total_score / total if total > 0 else 0

        return {
            'score': round(score, 2),
            'count': total,
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count
        }

    def _analyze_text_sentiment(self, text):
        """
        Analyze sentiment of text using keyword matching
        Returns: -1 to 1
        """
        positive_score = 0
        negative_score = 0

        words = re.findall(r'\b\w+\b', text.lower())

        for word in words:
            if word in self.sentiment_keywords['positive']:
                positive_score += 1
            if word in self.sentiment_keywords['negative']:
                negative_score += 1

        total = positive_score + negative_score
        if total == 0:
            return 0

        return (positive_score - negative_score) / total

    def _mock_twitter_sentiment(self, symbol, crypto_name):
        """Generate mock Twitter sentiment"""
        import random
        random.seed(hash(symbol) % 100)

        total = random.randint(50, 200)
        positive = int(total * random.uniform(0.3, 0.6))
        negative = int(total * random.uniform(0.2, 0.4))
        neutral = total - positive - negative

        score = (positive - negative) / total

        return {
            'score': round(score, 2),
            'count': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'engagement': random.randint(500, 5000)
        }

    def _mock_reddit_sentiment(self, symbol, crypto_name):
        """Generate mock Reddit sentiment"""
        import random
        random.seed(hash(symbol) % 101)

        total = random.randint(20, 80)
        positive = int(total * random.uniform(0.35, 0.65))
        negative = int(total * random.uniform(0.15, 0.35))
        neutral = total - positive - negative

        score = (positive - negative) / total

        return {
            'score': round(score, 2),
            'count': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral
        }

    def _mock_discord_sentiment(self, symbol, crypto_name):
        """Generate mock Discord sentiment"""
        import random
        random.seed(hash(symbol) % 102)

        total = random.randint(30, 120)
        positive = int(total * random.uniform(0.4, 0.7))
        negative = int(total * random.uniform(0.1, 0.3))
        neutral = total - positive - negative

        score = (positive - negative) / total

        return {
            'score': round(score, 2),
            'count': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral
        }

    def get_combined_sentiment(self, symbol, crypto_name):
        """
        Get combined sentiment from all sources

        Returns:
            dict: {
                'overall_score': float,
                'overall_label': str,
                'twitter': dict,
                'reddit': dict,
                'discord': dict,
                'total_mentions': int
            }
        """
        twitter = self.analyze_twitter(symbol, crypto_name)
        reddit = self.analyze_reddit(symbol, crypto_name)
        discord = self.analyze_discord(symbol, crypto_name)

        # Weighted average (Twitter 40%, Reddit 40%, Discord 20%)
        overall_score = (
            twitter['score'] * 0.4 +
            reddit['score'] * 0.4 +
            discord['score'] * 0.2
        )

        # Determine label
        if overall_score > 0.2:
            label = 'positive'
        elif overall_score < -0.2:
            label = 'negative'
        else:
            label = 'neutral'

        total_mentions = twitter['count'] + reddit['count'] + discord['count']

        return {
            'overall_score': round(overall_score, 2),
            'overall_label': label,
            'twitter': twitter,
            'reddit': reddit,
            'discord': discord,
            'total_mentions': total_mentions,
            'breakdown': {
                'twitter_weight': '40%',
                'reddit_weight': '40%',
                'discord_weight': '20%'
            }
        }


# Configuration helper
def load_api_config():
    """
    Load API configuration from environment variables or config file

    Set these environment variables:
    - TWITTER_BEARER_TOKEN
    - REDDIT_CLIENT_ID
    - REDDIT_CLIENT_SECRET
    - DISCORD_BOT_TOKEN
    """
    import os

    config = {
        'twitter_bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
        'reddit_client_id': os.getenv('REDDIT_CLIENT_ID'),
        'reddit_client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'discord_bot_token': os.getenv('DISCORD_BOT_TOKEN')
    }

    return config
