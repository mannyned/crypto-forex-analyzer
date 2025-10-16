# Stop Loss and Take Profit Recommendation System

## Overview

The Crypto & Forex Market Analyzer uses an advanced multi-method approach to calculate optimal stop loss and take profit levels for every trading opportunity.

## Stop Loss Calculation Methods

### 1. **ATR-Based Stop Loss (Primary Method)**
- Uses Average True Range (ATR) to measure market volatility
- Stop Loss = Entry Price ± (2 × ATR)
- Automatically adapts to market conditions
- More volatile markets get wider stops, calmer markets get tighter stops

**Example:**
- Entry: $50,000
- ATR: $1,000
- Stop Loss: $50,000 - (2 × $1,000) = $48,000

### 2. **Swing Level Stop Loss**
- Analyzes the last 20 candlesticks for swing highs/lows
- LONG: Places stop below recent swing low (98% of swing low)
- SHORT: Places stop above recent swing high (102% of swing high)
- Prevents premature stop-outs from normal market fluctuations

**Example:**
- Entry: $50,000
- Recent Swing Low: $48,500
- Stop Loss: $48,500 × 0.98 = $47,530

### 3. **Support/Resistance Stop Loss**
- Identifies key support and resistance levels using local minima/maxima
- Analyzes last 50 candles for consolidation areas
- LONG: Places stop below nearest support
- SHORT: Places stop above nearest resistance
- Provides structural market-based protection

**Example:**
- Entry: $50,000
- Support Level: $49,000
- Stop Loss: $49,000 × 0.98 = $48,020

### 4. **Percentage-Based Stop Loss (Safety Net)**
- Default: 30% maximum loss
- Acts as a safety cap to prevent excessive risk
- Overrides other methods if they're too aggressive

**Example:**
- Entry: $50,000
- Stop Loss: $50,000 × 0.70 = $35,000 (30% max loss)

### Stop Loss Selection Logic

The system calculates all four methods and selects the **most conservative** (lowest risk):

```
For LONG positions:
- Use the HIGHEST stop loss (closest to entry)
- Ensures minimum risk exposure

For SHORT positions:
- Use the LOWEST stop loss (closest to entry)
- Ensures minimum risk exposure
```

## Take Profit Calculation Methods

### 1. **Risk-Based Take Profit (Primary)**
- Maintains a minimum 1:2 risk/reward ratio
- Take Profit = Entry + (2 × Risk)
- Professional traders' standard approach

**Example:**
- Entry: $50,000
- Stop Loss: $48,000
- Risk: $2,000
- Take Profit: $50,000 + (2 × $2,000) = $54,000
- Risk/Reward: 1:2

### 2. **Volatility-Adjusted Take Profit**
- Uses ATR to set realistic targets
- More volatile markets get larger profit targets
- Take Profit = Entry ± (4 × ATR)

**Example:**
- Entry: $50,000
- ATR: $1,000
- Take Profit: $50,000 + (4 × $1,000) = $54,000

### 3. **Maximum Gain Cap**
- LONG: Capped at 200% gain (3x entry price)
- SHORT: Capped at 67% drop (0.33x entry price)
- Ensures realistic profit targets

## Reasoning Display

The system provides clear reasoning for each stop loss and take profit recommendation:

### Stop Loss Reasoning Examples:
- "Based on 2x ATR ($1,234.56)"
- "Below support level at $48,500"
- "Below recent swing low at $47,800"
- "Conservative 15.5% stop loss"

### Take Profit Reasoning Examples:
- "1:2.0 Risk/Reward ratio | 8.0% profit target | Conservative 2:1 minimum target"
- "1:3.5 Risk/Reward ratio | 14.0% profit target | Based on market volatility"

## Risk Management Features

### 1. **Position Sizing Suggestion**
- Calculates risk percentage per trade
- Helps determine appropriate position size
- Example: "Risk Amount: 5.2%"

### 2. **Potential Profit Display**
- Shows expected profit percentage if take profit is hit
- Example: "Potential Profit: +10.4%"

### 3. **Confidence Levels**
- **HIGH**: Risk/Reward ≥ 2.0 (excellent setup)
- **MEDIUM**: Risk/Reward ≥ 1.5 (good setup)
- **LOW**: Risk/Reward < 1.5 (marginal setup)

## Practical Example

**Bitcoin LONG Setup:**

```
Entry Price: $45,000
Stop Loss: $42,500 (5.5% risk)
Take Profit: $50,000 (11.1% profit)
Risk/Reward: 1:2.0

Stop Loss Reasoning:
"Based on 2x ATR ($1,250.00) | Below support level at $43,000"

Take Profit Reasoning:
"1:2.0 Risk/Reward ratio | 11.1% profit target | Conservative 2:1 minimum target"
```

**Interpretation:**
- Stop loss placed using ATR method near support
- Risk: $2,500 (5.5%)
- Reward: $5,000 (11.1%)
- If Bitcoin drops 5.5%, you lose $2,500
- If Bitcoin rises 11.1%, you gain $5,000
- 2:1 reward-to-risk ratio = professional setup

## Integration with Candlestick Patterns

Stop loss and take profit levels are calculated based on:
1. **Candlestick pattern detected** (e.g., Bullish Engulfing)
2. **Pattern strength** (rated 1-10)
3. **Market volatility** (ATR)
4. **Key support/resistance levels**

**Pattern-Based Adjustments:**
- Strong patterns (9-10 strength): More aggressive targets
- Medium patterns (7-8 strength): Balanced approach
- Weak patterns (< 7): No trade recommendation

## Best Practices

### For Conservative Traders:
- Only take trades with HIGH confidence
- Use maximum 30% stop loss
- Target minimum 1:2 risk/reward
- Watch for stop loss reasoning mentioning support levels

### For Aggressive Traders:
- Accept MEDIUM confidence setups
- May use tighter stops (ATR-based)
- Target 1:3+ risk/reward when possible
- Monitor volatility (ATR) for opportunities

### Universal Rules:
1. Never risk more than 1-2% of capital per trade
2. Always set stop loss immediately after entry
3. Use limit orders for take profit levels
4. Trail stop loss as price moves in your favor
5. Review reasoning to understand the trade setup

## Technical Implementation

The system uses:
- **pandas** for data analysis
- **numpy** for mathematical calculations
- 4-hour candlestick charts for pattern detection
- 14-period ATR for volatility measurement
- 20-candle lookback for swing levels
- 50-candle lookback for support/resistance

## API Response Format

```json
{
  "entry_exit": {
    "trade_type": "LONG",
    "entry_price": 45000.00,
    "stop_loss": 42500.00,
    "take_profit": 50000.00,
    "risk_reward_ratio": 2.0,
    "risk_percent": 5.56,
    "potential_profit_percent": 11.11,
    "recommendation": "HIGH confidence LONG setup based on Bullish Engulfing",
    "stop_loss_reasoning": "Based on 2x ATR ($1,250.00) | Below support level at $43,000",
    "take_profit_reasoning": "1:2.0 Risk/Reward ratio | 11.1% profit target | Conservative 2:1 minimum target",
    "key_levels": {
      "pivot": 44500.00,
      "resistance_1": 46000.00,
      "resistance_2": 47500.00,
      "support_1": 43000.00,
      "support_2": 41500.00
    }
  }
}
```

## Disclaimer

**IMPORTANT:** These are automated recommendations based on technical analysis. Always:
- Do your own research
- Consider fundamental factors
- Use proper position sizing
- Never risk more than you can afford to lose
- Consult with licensed financial advisors

Trading involves substantial risk of loss. Past performance does not guarantee future results.
