# Crypto & Forex Market Analyzer - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Features Overview](#features-overview)
4. [How to Use](#how-to-use)
5. [Understanding the Analysis](#understanding-the-analysis)
6. [Trading Recommendations](#trading-recommendations)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## Introduction

### What is Crypto & Forex Market Analyzer?

The Crypto & Forex Market Analyzer is a professional-grade trading analysis tool that helps you make informed trading decisions by analyzing:

- **8 Cryptocurrencies:** BTC, ETH, BNB, ADA, SOL, XRP, DOT, DOGE
- **6 Forex Pairs:** EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD, USD/CHF

### Key Features

✅ **Multi-Page Application** - Separate crypto and forex dashboards with professional home page
✅ **Machine Learning Price Prediction** - 4-model ensemble (RF, GB, XGB, LSTM) for forex pairs
✅ **40+ Technical Indicators** - Comprehensive analysis using industry-standard indicators
✅ **Candlestick Pattern Recognition** - Identifies 8 powerful chart patterns on multiple timeframes
✅ **Dynamic Stop Loss & Take Profit** - Intelligent risk management with ATR and support/resistance
✅ **Integrated Lot Size Calculator** - Professional position sizing for forex trading
✅ **Real-time Analysis** - Up-to-date market data from Yahoo Finance
✅ **Neural Dark Theme** - Modern, sleek UI design throughout

### Who Is This For?

- Day traders looking for technical signals
- Swing traders seeking entry/exit points
- Analysts wanting comprehensive market overview
- Beginners learning technical analysis
- Experienced traders seeking confirmation

---

## Getting Started

### Installation

#### Step 1: Download the Application

**Option A: Clone from GitHub**
```bash
git clone https://github.com/mannyned/crypto-forex-analyzer.git
cd crypto-forex-analyzer
```

**Option B: Download ZIP**
1. Visit https://github.com/mannyned/crypto-forex-analyzer
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in the extracted folder

#### Step 2: Install Dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

#### Step 3: Run the Application

**Windows:**
```bash
python app.py
```

**Mac/Linux:**
```bash
python3 app.py
```

#### Step 4: Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:3000
```

You should see the professional home page with options to choose **Cryptocurrency** or **Forex** analysis!

---

## Features Overview

### 1. Multi-Page Application

The application has been redesigned with separate dashboards for optimal user experience:

#### Home Page (`/`)
- Professional landing page with market selection
- Quick statistics (8 crypto pairs, 6 forex pairs, 40+ indicators)
- Direct navigation to specialized dashboards
- Neural dark theme design

#### Crypto Dashboard (`/crypto`)
- Dedicated cryptocurrency analysis
- All 8 crypto pairs
- 40+ technical indicators
- Candlestick pattern recognition
- Entry/exit recommendations

#### Forex Dashboard (`/forex`)
- Dedicated forex pair analysis
- All 6 major forex pairs
- **Machine Learning Price Predictions** (4-model ensemble)
- **Integrated Lot Size Calculator**
- 40+ technical indicators
- Enhanced risk management tools

#### Standalone Lot Calculator (`/lot-calculator`)
- Independent position sizing tool
- Works without running analysis
- Quick calculations for active trades

### 2. Machine Learning Price Prediction (Forex Only)

Advanced ML system that forecasts price direction 5 periods ahead:

#### 4-Model Ensemble
1. **Random Forest Classifier** - 100 decision trees with ensemble voting
2. **Gradient Boosting Classifier** - Sequential tree building for error correction
3. **XGBoost** - Optimized gradient boosting with regularization
4. **LSTM Neural Network** - 2-layer deep learning (64→32 units) for temporal patterns

#### Prediction Features
- **Direction**: BULLISH (>0.2%), BEARISH (<-0.2%), or NEUTRAL (sideways)
- **Confidence**: Average probability across all 4 models (70-95%)
- **Probabilities**: Individual class probabilities for each direction
- **Recommendation**: Trading suggestions with risk warnings
- **Model Status**: Shows active models (3-model or 4-model ensemble)
- **Collapsible Explanation**: Detailed breakdown of how predictions work

#### 17 Features Analyzed
- Price Momentum (5): Returns over 1, 2, 3, 5, 10 periods
- Volatility (2): Price volatility, standard deviation
- Volume (2): Trading volume, volume changes
- Technical Indicators (8): RSI, Stochastic, Bollinger Bands, ADX, ATR, OBV, CCI, Williams %R, ROC, EMA trend, MACD histogram

### 3. Technical Indicators (40+)

The application analyzes markets using 40+ technical indicators across 5 categories:

#### Momentum Indicators
- **RSI (Relative Strength Index)** - Measures overbought/oversold conditions
- **Williams %R** - Momentum oscillator
- **Stochastic Oscillator** - Compares closing price to price range
- **ROC (Rate of Change)** - Momentum indicator
- **CCI (Commodity Channel Index)** - Identifies cyclical trends
- **MFI (Money Flow Index)** - Volume-weighted RSI
- **Ultimate Oscillator** - Multiple timeframe momentum

#### Trend Indicators
- **SMA (Simple Moving Averages)** - 20, 50, 200 periods
- **EMA (Exponential Moving Averages)** - 12, 26 periods
- **MACD** - Trend-following momentum indicator
- **ADX** - Measures trend strength
- **Parabolic SAR** - Stop and reverse indicator
- **Supertrend** - Trend-following indicator
- **Ichimoku Cloud** - Comprehensive trend indicator
- **Aroon Indicator** - Identifies trend changes

#### Volatility Indicators
- **Bollinger Bands** - Volatility bands
- **ATR (Average True Range)** - Measures volatility
- **Keltner Channels** - Volatility-based channels
- **Donchian Channels** - Price channel indicator
- **Standard Deviation** - Statistical volatility measure

#### Volume Indicators
- **OBV (On-Balance Volume)** - Volume-based momentum
- **CMF (Chaikin Money Flow)** - Money flow indicator
- **A/D Line** - Accumulation/Distribution line
- **VWAP** - Volume-weighted average price
- **Volume Oscillator** - Volume momentum
- **Force Index** - Price and volume combination

#### Support & Resistance
- **Fibonacci Retracement** - Key retracement levels
- **Pivot Points** - Intraday support/resistance
- **Support Levels** - Price floors
- **Resistance Levels** - Price ceilings

### 4. Integrated Lot Size Calculator (Forex Only)

Professional position sizing tool built into the forex dashboard:

#### Features
- **Account Balance Tracking** - Monitor your trading capital
- **Risk Percentage Input** - Set risk tolerance (1-2% recommended)
- **Stop Loss in Pips** - Auto-populated from analysis
- **Position Size Calculations**: Standard, mini, and micro lots
- **Profit/Loss Projections**: Based on recommended targets
- **Risk Metrics**: Risk/reward ratio, leverage requirements, position value

#### Usage
1. Analyze a forex pair
2. Scroll to "Lot Size Calculator" section
3. Enter account balance and risk percentage
4. Review recommended lot size and profit projections

### 5. Candlestick Pattern Recognition

The analyzer detects 8 powerful candlestick patterns on multiple timeframes (5-minute and 4-hour charts):

| Pattern | Type | Strength | Signal |
|---------|------|----------|--------|
| Bullish Engulfing | Bullish | 8/10 | Reversal |
| Bearish Engulfing | Bearish | 8/10 | Reversal |
| Doji | Neutral | 6/10 | Indecision |
| Hammer | Bullish | 7/10 | Reversal |
| Inverted Hammer | Bullish | 6/10 | Reversal |
| Shooting Star | Bearish | 7/10 | Reversal |
| Morning Star | Bullish | 9/10 | Strong Reversal |
| Evening Star | Bearish | 9/10 | Strong Reversal |
| Three White Soldiers | Bullish | 9/10 | Continuation |
| Three Black Crows | Bearish | 9/10 | Continuation |
| Bullish Harami | Bullish | 7/10 | Reversal |
| Bearish Harami | Bearish | 7/10 | Reversal |
| Piercing Line | Bullish | 8/10 | Reversal |
| Dark Cloud Cover | Bearish | 8/10 | Reversal |

### 6. Dynamic Stop Loss & Take Profit

**Stop Loss Calculation (Multiple Methods):**
1. **ATR-Based** - Adapts to market volatility (2× ATR)
2. **Support/Resistance** - Based on key structural levels
3. **Swing Levels** - Recent swing highs/lows
4. **Volatility-Based** - Dynamic 5-10% based on conditions

**Take Profit Calculation (Dynamic Risk/Reward):**
- **Tight Stops (≤5%):** 1:3 Risk/Reward
- **Medium Stops (5-10%):** 1:2.5 Risk/Reward
- **Wide Stops (>10%):** 1:2 Risk/Reward

### 7. Signal Generation

**Trading Signals:**
- **STRONG BUY** - Multiple strong buy indicators (score ≥ 6)
- **BUY** - Several buy indicators (score ≥ 2)
- **HOLD** - Mixed or weak signals
- **SELL** - Several sell indicators (score ≤ -2)
- **STRONG SELL** - Multiple strong sell indicators (score ≤ -6)

**Signal Strength:**
- Percentage from 0% to 100%
- Higher percentage = stronger confidence
- Based on indicator consensus

---

## How to Use

### Dashboard Overview

#### Home Page Navigation

When you open http://localhost:3000, you'll see the professional home page with:

1. **Header** - Application title and feature highlights
2. **Feature Cards** - Key features (40+ indicators, pattern recognition, etc.)
3. **Market Selection** - Two main options:
   - **Cryptocurrency** - Navigate to crypto dashboard
   - **Forex** - Navigate to forex dashboard with ML predictions
4. **Footer** - Quick links and disclaimer

#### Crypto Dashboard (`/crypto`)

1. **Market Selection** - Checkboxes for all 8 crypto pairs
2. **Analyze Button** - Click to run analysis
3. **Results Display** - Comprehensive analysis with:
   - Price charts
   - Technical indicators
   - Candlestick patterns
   - Entry/exit recommendations

#### Forex Dashboard (`/forex`)

1. **Market Selection** - Checkboxes for all 6 forex pairs
2. **Analyze Button** - Click to run analysis
3. **Results Display** - Enhanced analysis including:
   - **ML Price Predictions** (4-model ensemble)
   - Technical indicators
   - Candlestick patterns
   - Entry/exit recommendations
   - **Integrated Lot Size Calculator**

### Running an Analysis

#### Step 1: Click "Analyze Markets"

The button will become disabled and show a loading spinner.

**What happens during analysis:**
1. Fetches latest market data from Yahoo Finance
2. Calculates 42+ technical indicators
3. Analyzes candlestick patterns on 4H charts
4. Generates trading signals
5. Calculates entry/exit points
6. Scores sentiment
7. Ranks all opportunities

**Time:** Usually takes 30-60 seconds

#### Step 2: View Results

Results appear in three organized tabs:

**Top Opportunities Tab:**
- Shows markets with STRONG BUY or STRONG SELL signals
- Minimum 30% signal strength
- Sorted by strength (highest first)
- Best for finding immediate trading opportunities

**Cryptocurrencies Tab:**
- All 7 cryptocurrencies analyzed
- Complete analysis for each coin
- All signals shown (STRONG BUY to STRONG SELL)

**Forex Pairs Tab:**
- All 6 forex pairs analyzed
- Complete analysis for each pair
- All signals shown

### Understanding Market Cards

Each market is displayed in a card with sections:

#### 1. Header Section
```
Bitcoin (BTC)
BTC/USDT
```
- Market name and symbol

#### 2. Price Section
```
$45,000.00    +2.5%
```
- Current price
- 24-hour change (green = up, red = down)

#### 3. Signal Badge
```
STRONG BUY
```
- Color-coded signal:
  - **Green:** STRONG BUY, BUY
  - **Yellow:** HOLD
  - **Red:** SELL, STRONG SELL

#### 4. Signal Strength Bar
```
[████████░░] 53.3%
```
- Visual strength indicator
- Percentage value

#### 5. Analysis Factors
```
Analysis Factors:
• RSI oversold (28.50)
• MACD bullish (MACD: 150.23 > Signal: 120.45)
• Price above SMA50 > SMA200
• Supertrend uptrend (ST: 43500.00)
• Positive market sentiment (0.65)
```
- Top 5 reasons for the signal
- Specific indicator values
- Easy to understand explanations

#### 6. Candlestick Patterns (if detected)
```
📊 Candlestick Patterns (4H Chart)
Bullish Engulfing    Strength: 8/10
Strong reversal signal - buyers overwhelm sellers
```
- Pattern name and type (bullish/bearish)
- Strength rating (1-10)
- Pattern description

#### 7. Trading Setup (if pattern found)
```
💰 Trading Setup
LONG

HIGH confidence LONG setup based on Bullish Engulfing

Stop Loss: Based on 2x ATR ($900.00) | Below support level at $43,500
Take Profit: 1:2.4 Risk/Reward ratio | 9.8% profit target

Entry Price: $45,000.00
Stop Loss: $43,200.00
Take Profit: $49,400.00
Risk/Reward: 1:2.44
Risk Amount: 4.00%
Potential Profit: +9.78%
```

**Components:**
- **Trade Type:** LONG (buy) or SHORT (sell)
- **Confidence:** HIGH, MEDIUM, or LOW
- **Stop Loss Reasoning:** Why this level was chosen
- **Take Profit Reasoning:** Why this target was set
- **Entry Price:** Recommended entry point
- **Stop Loss:** Where to exit if trade goes wrong
- **Take Profit:** Where to take profits
- **Risk/Reward:** Ratio of risk to reward
- **Risk Amount:** Percentage you're risking
- **Potential Profit:** Percentage gain if target hit

---

## Understanding the Analysis

### Reading Technical Signals

#### Momentum Indicators

**RSI (Relative Strength Index):**
```
RSI oversold (28.50) → BUY signal
RSI overbought (72.30) → SELL signal
```
- **< 30:** Oversold (potential buy)
- **30-70:** Neutral zone
- **> 70:** Overbought (potential sell)

**Stochastic Oscillator:**
```
Stochastic oversold (K:18.50, D:15.20) → BUY signal
```
- **< 20:** Oversold
- **> 80:** Overbought
- **K crosses above D:** Bullish signal
- **K crosses below D:** Bearish signal

#### Trend Indicators

**MACD:**
```
MACD bullish (MACD: 150.23 > Signal: 120.45) → BUY signal
```
- **MACD > Signal & MACD > 0:** Strong bullish
- **MACD < Signal & MACD < 0:** Strong bearish

**Moving Average Alignment:**
```
Golden alignment: Price > SMA20 > SMA50 > SMA200 → STRONG BUY
Death alignment: Price < SMA20 < SMA50 < SMA200 → STRONG SELL
```

**Supertrend:**
```
Supertrend uptrend (ST: 43500.00) → BUY signal
Supertrend downtrend (ST: 46500.00) → SELL signal
```
- **Uptrend (green):** Bullish signal
- **Downtrend (red):** Bearish signal

#### Volume Indicators

**MFI (Money Flow Index):**
```
MFI oversold (18.50) - buying pressure → BUY signal
MFI overbought (82.30) - selling pressure → SELL signal
```

**CMF (Chaikin Money Flow):**
```
Positive money flow (CMF: 0.25) → BUY signal
Negative money flow (CMF: -0.30) → SELL signal
```

#### Volatility Indicators

**Bollinger Bands:**
```
Price at lower Bollinger Band ($44,200) → BUY signal
Price at upper Bollinger Band ($48,800) → SELL signal
```
- At lower band: Oversold
- At upper band: Overbought

### Interpreting Candlestick Patterns

#### Reversal Patterns

**Bullish Reversal (Buy Signals):**

1. **Bullish Engulfing**
   - Previous candle: Red (down)
   - Current candle: Large green (up)
   - Current engulfs previous completely
   - **Signal:** Strong reversal to upside

2. **Hammer**
   - Small body at top
   - Long lower shadow (2x body)
   - Short or no upper shadow
   - **Signal:** Rejection of lower prices

3. **Morning Star**
   - First: Large red candle
   - Second: Small body (star)
   - Third: Large green candle
   - **Signal:** Very strong reversal to upside

**Bearish Reversal (Sell Signals):**

1. **Bearish Engulfing**
   - Previous candle: Green (up)
   - Current candle: Large red (down)
   - Current engulfs previous completely
   - **Signal:** Strong reversal to downside

2. **Shooting Star**
   - Small body at bottom
   - Long upper shadow (2x body)
   - Short or no lower shadow
   - **Signal:** Rejection of higher prices

3. **Evening Star**
   - First: Large green candle
   - Second: Small body (star)
   - Third: Large red candle
   - **Signal:** Very strong reversal to downside

#### Continuation Patterns

**Bullish Continuation:**

**Three White Soldiers**
- Three consecutive green candles
- Each closes higher than previous
- **Signal:** Strong uptrend continuation

**Bearish Continuation:**

**Three Black Crows**
- Three consecutive red candles
- Each closes lower than previous
- **Signal:** Strong downtrend continuation

### Understanding Entry/Exit Points

#### Stop Loss Levels

**Example:**
```
Entry: $45,000
Stop Loss: $43,200 (4% risk)
Reasoning: Based on 2x ATR ($900) | Below support at $43,500
```

**What this means:**
- If price drops to $43,200, exit the trade
- You'll lose 4% of your position
- Stop placed below key support level
- Stop accounts for market volatility (ATR)

**Types of Stop Loss:**
1. **ATR-Based:** Adapts to volatility
2. **Support-Based:** At key structural level
3. **Swing Low-Based:** Below recent low
4. **Volatility-Based:** Percentage-based adaptive

#### Take Profit Levels

**Example:**
```
Entry: $45,000
Take Profit: $49,400 (9.78% profit)
Risk/Reward: 1:2.44
Reasoning: 1:2.4 R/R ratio | 9.8% target | Balanced setup
```

**What this means:**
- If price rises to $49,400, take profits
- You'll gain 9.78% on your position
- You're risking $1 to make $2.44 (good ratio)
- Target based on dynamic calculation

**Risk/Reward Explained:**
- **1:2** means risk $1 to make $2 (minimum acceptable)
- **1:2.5** means risk $1 to make $2.50 (good)
- **1:3** means risk $1 to make $3 (excellent)

---

## Trading Recommendations

### Using the Analysis for Trading

#### Step 1: Find Opportunities

**Use Top Opportunities Tab:**
- Pre-filtered for strong signals
- Highest strength shown first
- Look for:
  - STRONG BUY or STRONG SELL signals
  - Signal strength > 50%
  - Multiple supporting factors

#### Step 2: Review the Analysis

**Check these factors:**

1. **Signal Consensus:**
   - Are multiple indicators aligned?
   - Example: RSI oversold + MACD bullish + Supertrend up = Strong consensus

2. **Candlestick Pattern:**
   - Is there a pattern detected?
   - What's the pattern strength? (Prefer 7+ /10)
   - Does pattern align with signal?

3. **Sentiment:**
   - Is sentiment supporting the signal?
   - Positive sentiment + BUY signal = Good
   - Negative sentiment + BUY signal = Be cautious

4. **Trading Setup:**
   - Is there a LONG or SHORT recommendation?
   - What's the confidence level? (HIGH preferred)
   - Is the risk/reward ratio good? (Prefer ≥ 1:2)

#### Step 3: Plan Your Trade

**If Trading Setup Shows:**

```
LONG Setup
Entry: $45,000
Stop Loss: $43,200 (4% risk)
Take Profit: $49,400 (9.78% profit)
Risk/Reward: 1:2.44
```

**Your Trading Plan:**
1. **Entry:** Place buy order at $45,000
2. **Stop Loss:** Place stop loss at $43,200
3. **Take Profit:** Place take profit at $49,400
4. **Position Size:** Calculate based on risk tolerance

**Position Sizing Example:**

If you have $10,000 account and want to risk 1%:
```
Account: $10,000
Risk per trade: 1% = $100
Entry: $45,000
Stop Loss: $43,200
Risk per coin: $45,000 - $43,200 = $1,800

Position size: $100 ÷ $1,800 = 0.0556 BTC

Total position value: 0.0556 × $45,000 = $2,500
```

#### Step 4: Execute and Monitor

**Execution:**
1. Enter position at recommended entry
2. Set stop loss immediately
3. Set take profit order
4. Monitor position

**Monitoring:**
1. Check if price respects support/resistance
2. Watch for new candlestick patterns
3. Re-analyze if conditions change
4. Trail stop loss as profit grows (optional)

### Trading Rules

#### Golden Rules

1. **Never trade without a stop loss**
   - Always use the recommended stop loss
   - Never remove stop loss hoping for reversal

2. **Respect your risk management**
   - Never risk more than 1-2% per trade
   - Use proper position sizing

3. **Don't chase trades**
   - Wait for proper entry point
   - Don't FOMO into trades

4. **Follow your plan**
   - Stick to entry, stop loss, take profit
   - Don't change plans mid-trade

5. **Use multiple confirmations**
   - Don't trade on signal alone
   - Look for pattern + signal + sentiment alignment

#### When to Trade

**High Confidence Trades:**
✅ STRONG BUY/SELL signal
✅ Strength > 50%
✅ Candlestick pattern detected (strength 7+)
✅ Multiple indicator consensus
✅ Sentiment aligned
✅ HIGH confidence trading setup
✅ Risk/Reward ≥ 1:2

**Medium Confidence Trades:**
⚠️ BUY/SELL signal
⚠️ Strength 30-50%
⚠️ Some indicator consensus
⚠️ MEDIUM confidence setup
⚠️ Risk/Reward ≥ 1:2

**Avoid Trading:**
❌ HOLD signal
❌ Strength < 30%
❌ NO TRADE recommendation
❌ Conflicting indicators
❌ Risk/Reward < 1:2
❌ No clear pattern

---

## Best Practices

### Daily Routine

**Morning (Before Market Open):**
1. Run full market analysis
2. Review top opportunities
3. Create watchlist of potential trades
4. Set price alerts for entry levels

**During Market Hours:**
1. Monitor watchlist for entry signals
2. Execute planned trades
3. Manage open positions
4. Update stop losses if needed

**Evening (After Market Close):**
1. Review executed trades
2. Update trading journal
3. Prepare for next day

### Risk Management

**Portfolio Level:**
- Total risk across all trades: Max 5-10%
- Example: $10,000 account
  - Max total risk: $500-$1,000
  - If risking 1% per trade: Max 5-10 open trades

**Position Level:**
- Risk per trade: 1-2% of account
- Position size based on stop loss distance
- Larger account balance = more positions possible

**Trade Level:**
- Always use stop loss
- Minimum 1:2 risk/reward
- Don't move stop loss wider
- Take partial profits at targets

### Combining with Other Analysis

**Fundamental Analysis:**
- Check news before trading
- Avoid trading during major news events
- Be aware of economic calendars

**Sentiment Analysis:**
- Monitor social media trends
- Track institutional activity
- Watch market fear/greed

**Multiple Timeframes:**
- Use 4H charts (provided by app)
- Confirm on daily charts
- Refine entry on 1H charts

---

## FAQ

### General Questions

**Q: How often should I run the analysis?**
A: Run analysis at the start of each trading session. For day trading, run every 2-4 hours. For swing trading, once daily is sufficient.

**Q: Can I use this for day trading?**
A: Yes, but the 4-hour candlestick patterns are better suited for swing trading (holding 1-7 days). For day trading, combine with shorter timeframe analysis.

**Q: Are ML predictions available for cryptocurrencies?**
A: No, ML predictions are currently only available for forex pairs. Cryptocurrency analysis includes technical indicators and candlestick patterns.

**Q: How accurate are the signals?**
A: No technical analysis is 100% accurate. Signals show probability, not certainty. Always use proper risk management. Past performance doesn't guarantee future results.

**Q: Can I customize the indicators?**
A: Yes, you can edit `technical_indicators.py` to adjust indicator parameters or add new indicators.

### Technical Questions

**Q: Why does analysis take 30-60 seconds?**
A: The app fetches data for 13 markets, calculates 42+ indicators per market, analyzes patterns, and generates recommendations. This comprehensive analysis takes time.

**Q: Can I analyze more markets?**
A: Yes, edit `data_fetcher.py` and add symbols to `CRYPTO_PAIRS` or `FOREX_PAIRS` lists.

**Q: What data source does it use?**
A: Yahoo Finance API for all market data. Free, no API key required.

**Q: Can I run this on a schedule?**
A: Yes, you can set up a cron job (Linux/Mac) or Task Scheduler (Windows) to run `run_analysis.py` at specific times.

**Q: Does it support stocks?**
A: Currently crypto and forex only. You can modify `data_fetcher.py` to add stock symbols.

### Trading Questions

**Q: Should I always follow the signals?**
A: No. Signals are recommendations based on technical analysis. Always do your own research and consider:
- Market conditions
- News events
- Your risk tolerance
- Your trading strategy

**Q: What if signal says BUY but pattern says SELL?**
A: This indicates conflicting signals. It's generally better to wait for clearer confirmation. Look for:
- Which has higher strength?
- What do most indicators say?
- What's the sentiment?

**Q: Can I adjust the stop loss?**
A: You can, but it's not recommended to widen stops (increase risk). You can trail stops up (reduce risk) as price moves in your favor.

**Q: What's a good risk/reward ratio?**
A: Minimum 1:2 (risk $1 to make $2). Professional traders often target 1:3 or higher. The app dynamically calculates based on market conditions.

**Q: How do I know when to exit?**
A: Three main exits:
1. **Stop Loss Hit** - Exit immediately, accept loss
2. **Take Profit Hit** - Exit immediately, take profit
3. **Signal Changes** - If strong BUY becomes SELL, consider exiting

### Troubleshooting

**Q: Analysis shows "No markets to display"?**
A: This usually means:
- No markets met the strength threshold
- Network issues fetching data
- Check your internet connection
- Try refreshing the page

**Q: Server won't start?**
A:
```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill the process
taskkill /PID <pid> /F

# Restart
python app.py
```

**Q: Getting import errors?**
A:
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

**Q: Page loads but no data shows?**
A:
- Check browser console for errors (F12)
- Verify Flask server is running
- Check if port 3000 is accessible
- Try different browser

---

## Glossary

**ATR (Average True Range):** Measure of market volatility

**Bollinger Bands:** Volatility bands around price

**Candlestick Pattern:** Price pattern formed by OHLC data

**EMA (Exponential Moving Average):** Trend indicator favoring recent prices

**Fibonacci Levels:** Support/resistance based on Fibonacci sequence

**MACD:** Momentum and trend indicator

**Pivot Points:** Support/resistance levels for day trading

**Risk/Reward Ratio:** Ratio of potential loss to potential gain

**RSI (Relative Strength Index):** Momentum indicator measuring overbought/oversold

**SMA (Simple Moving Average):** Average price over period

**Stop Loss:** Price level to exit losing trade

**Support/Resistance:** Price levels where price tends to reverse

**Take Profit:** Price level to exit winning trade

**VWAP (Volume Weighted Average Price):** Average price weighted by volume

---

## Disclaimer

**IMPORTANT LEGAL NOTICE:**

This tool is for **EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY**.

**This is NOT:**
- Financial advice
- Investment advice
- Trading advice
- Professional recommendation

**Trading involves substantial risk:**
- You can lose your entire investment
- Past performance doesn't guarantee future results
- Technical analysis is not foolproof
- Markets can behave irrationally

**Before Trading:**
- Do your own research (DYOR)
- Understand the risks
- Only invest what you can afford to lose
- Consider consulting licensed financial advisors
- Test strategies with paper trading first

**The creators of this tool:**
- Make no guarantees of profitability
- Are not responsible for trading losses
- Do not provide financial advice
- Recommend consulting professionals

**By using this tool, you acknowledge:**
- You understand the risks
- You are solely responsible for your trades
- You won't hold creators liable for losses
- You'll trade responsibly

---

## Support & Resources

### Documentation
- **README.md** - Project overview
- **QUICKSTART.md** - Quick start guide
- **TECHNICAL_DOCUMENTATION.md** - Technical details
- **STOP_LOSS_TAKE_PROFIT_GUIDE.md** - SL/TP system guide
- **SOCIAL_SENTIMENT_SETUP.md** - API integration guide
- **USER_GUIDE.md** - This document

### Community
- **GitHub:** https://github.com/mannyned/crypto-forex-analyzer
- **Issues:** Report bugs and request features
- **Discussions:** Ask questions and share ideas

### Learning Resources
- **Investopedia** - Learn about technical indicators
- **BabyPips** - Forex trading education
- **TradingView** - Charting and analysis
- **CoinGecko** - Cryptocurrency information

### Trading Platforms
- **Binance** - Cryptocurrency exchange
- **Coinbase** - Cryptocurrency exchange
- **OANDA** - Forex broker
- **Interactive Brokers** - Multi-asset broker

---

## Updates & Changelog

### Version 3.0.0 (Current)
- ✅ Multi-page application architecture
- ✅ Machine Learning Price Prediction (4-model ensemble)
- ✅ LSTM Neural Network for temporal pattern recognition
- ✅ Professional home page with market selection
- ✅ Separate crypto and forex dashboards
- ✅ Integrated lot size calculator for forex
- ✅ Collapsible ML prediction explanations
- ✅ 40+ technical indicators
- ✅ 8 candlestick patterns on multiple timeframes
- ✅ Dynamic stop loss & take profit
- ✅ Neural dark theme UI
- ✅ REST API

### Version 2.0.0
- ✅ 40+ technical indicators
- ✅ 8 candlestick patterns
- ✅ Dynamic stop loss & take profit
- ✅ Integrated lot size calculator
- ✅ ATR-based stop loss calculations
- ✅ Support/resistance level detection

### Version 1.0.0
- ✅ Basic technical analysis
- ✅ Initial release

### Planned Features
- 🔄 More candlestick patterns (20+ total)
- 🔄 ML predictions for cryptocurrencies
- 🔄 Backtesting functionality
- 🔄 Mobile app
- 🔄 More markets (stocks, commodities)
- 🔄 Custom indicator builder
- 🔄 Trading journal integration
- 🔄 Real-time sentiment from social media

---

## Contact

**Developer:** Manny (mannyned)
**Email:** mannyned@icloud.com
**GitHub:** https://github.com/mannyned

**For:**
- Bug reports: Open GitHub issue
- Feature requests: GitHub discussions
- General questions: GitHub discussions
- Professional support: Email

---

**Thank you for using Crypto & Forex Market Analyzer!**

**Happy Trading! 📈**

*Remember: Trade responsibly, manage risk, and never stop learning.*

---

**Document Version:** 3.0.0
**Last Updated:** October 20, 2025
**Author:** Manny (mannyned)
**Application Version:** 3.0.0 (Multi-Page + ML Predictions)
