# Social Media Sentiment Analysis Setup

This guide explains how to set up real-time sentiment analysis from Twitter, Reddit, and Discord.

## Overview

The application now includes **social sentiment analysis** that aggregates data from:
- **Twitter** (40% weight) - Real-time tweets and engagement
- **Reddit** (40% weight) - Posts from crypto subreddits
- **Discord** (20% weight) - Community discussions

## Current Status

✅ **Mock Mode Active** - Currently using simulated sentiment data
🔧 **API Integration Ready** - Code is prepared for real API connections

## How to Enable Real APIs

### 1. Twitter API Setup

**Get API Access:**
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a Developer Account
3. Create a new App
4. Get your **Bearer Token** from the "Keys and Tokens" tab

**Set Environment Variable:**
```bash
# Windows
set TWITTER_BEARER_TOKEN=your_bearer_token_here

# Linux/Mac
export TWITTER_BEARER_TOKEN=your_bearer_token_here
```

**Or add to `.env` file:**
```
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

### 2. Reddit API Setup

**Get API Access:**
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Note your **Client ID** and **Client Secret**

**Set Environment Variables:**
```bash
# Windows
set REDDIT_CLIENT_ID=your_client_id_here
set REDDIT_CLIENT_SECRET=your_client_secret_here

# Linux/Mac
export REDDIT_CLIENT_ID=your_client_id_here
export REDDIT_CLIENT_SECRET=your_client_secret_here
```

**Or add to `.env` file:**
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

### 3. Discord Bot Setup (Optional)

**Create Discord Bot:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" tab and click "Add Bot"
4. Copy the **Bot Token**
5. Enable "Message Content Intent"
6. Invite bot to your servers

**Set Environment Variable:**
```bash
# Windows
set DISCORD_BOT_TOKEN=your_bot_token_here

# Linux/Mac
export DISCORD_BOT_TOKEN=your_bot_token_here
```

**Or add to `.env` file:**
```
DISCORD_BOT_TOKEN=your_bot_token_here
```

## Features

### Sentiment Metrics

Each platform provides:
- **Score**: -1 (very negative) to +1 (very positive)
- **Count**: Total mentions analyzed
- **Positive/Negative/Neutral**: Breakdown of sentiment
- **Engagement**: Social engagement metrics (likes, retweets, upvotes)

### Combined Sentiment

The overall sentiment is calculated as:
```
Overall Score = (Twitter × 0.4) + (Reddit × 0.4) + (Discord × 0.2)
```

### Sentiment Labels

- **Positive**: Overall score > 0.2
- **Neutral**: Score between -0.2 and 0.2
- **Negative**: Overall score < -0.2

## API Rate Limits

### Twitter
- **Free Tier**: 500,000 tweets/month
- **Basic**: $100/month - 10M tweets
- **Pro**: Custom pricing

### Reddit
- **Free**: 60 requests/minute
- No paid tiers needed for this use case

### Discord
- **Free**: Unlimited messages (with bot)
- Requires bot setup and server invites

## Testing

To test with mock data (no APIs needed):
```bash
python app.py
```

The app will use simulated sentiment data that mimics real patterns.

## Troubleshooting

**"No API key found" errors:**
- Make sure environment variables are set
- Restart your terminal/IDE after setting variables
- Check `.env` file exists and has correct format

**Twitter API errors:**
- Verify your Bearer Token is correct
- Check you have "Read" permissions
- Ensure you're within rate limits

**Reddit API errors:**
- Verify Client ID and Secret are correct
- Check your app type is "script"
- Ensure user agent is set correctly

**Discord Bot not working:**
- Verify bot token is correct
- Check "Message Content Intent" is enabled
- Ensure bot is invited to servers

## Advanced: Sentiment Keywords

You can customize sentiment keywords in `social_sentiment.py`:

```python
'positive': [
    'bullish', 'moon', 'rally', 'pump', ...
],
'negative': [
    'bearish', 'crash', 'dump', 'sell', ...
]
```

## Monitoring Sentiment

Sentiment data is included in market analysis results:

```json
{
  "sentiment": {
    "score": 0.35,
    "label": "positive",
    "sources": 142,
    "social": {
      "twitter": {"positive": 45, "negative": 23, ...},
      "reddit": {"positive": 38, "negative": 19, ...},
      "discord": {"positive": 12, "negative": 5, ...}
    }
  }
}
```

## Cost Estimate

**Free Setup (Mock Mode):**
- Cost: $0/month
- Good for: Testing, development

**Basic Setup (Twitter + Reddit):**
- Cost: $0/month (free tiers)
- Good for: Personal use, small projects

**Professional Setup (All APIs):**
- Twitter Basic: $100/month
- Reddit: Free
- Discord: Free
- Total: ~$100/month
- Good for: Production, high-volume analysis

## Next Steps

1. Start with mock mode to test the system
2. Add Twitter API for real-time tweets
3. Add Reddit API for community sentiment
4. Optionally add Discord for targeted communities
5. Monitor sentiment trends in your dashboard

## Support

For API-specific issues:
- Twitter: [Twitter API Docs](https://developer.twitter.com/en/docs)
- Reddit: [Reddit API Docs](https://www.reddit.com/dev/api)
- Discord: [Discord Developer Docs](https://discord.com/developers/docs)

For application issues:
- Check GitHub: https://github.com/mannyned/crypto-forex-analyzer
- Review logs in terminal
