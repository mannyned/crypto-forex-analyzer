"""
Test USD/JPY on today's market - Real-time analysis
"""
from market_analyzer import MarketAnalyzer
import json
from datetime import datetime

print("\n" + "="*70)
print("USD/JPY REAL-TIME MARKET ANALYSIS")
print("="*70)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Symbol: USDJPY=X (US Dollar / Japanese Yen)")
print("Market Type: Forex")
print("="*70 + "\n")

# Initialize analyzer
analyzer = MarketAnalyzer()

# Analyze USD/JPY
print("Fetching current market data and running analysis...")
print("This includes:")
print("  - Technical indicators (RSI, MACD, Bollinger Bands, etc.)")
print("  - Candlestick pattern detection (5m and 4H)")
print("  - ML predictions (4-model ensemble)")
print("  - Entry/exit recommendations")
print("\nPlease wait...\n")

# Run analysis
analysis = analyzer.analyze_symbol('USDJPY=X', 'forex', timeframe='1d', limit=100)

if analysis:
    print("="*70)
    print("ANALYSIS RESULTS")
    print("="*70 + "\n")

    # Current Price
    print(f"CURRENT PRICE: {analysis.get('current_price', 'N/A')}")
    print()

    # Signal
    signal = analysis.get('signal', 'HOLD')
    strength = analysis.get('strength', 0)
    print(f"SIGNAL: {signal} (Strength: {strength:.2f}%)")
    print()

    # Technical Indicators
    print("TECHNICAL INDICATORS:")
    print("-" * 70)
    indicators = analysis.get('indicators', {})
    if indicators:
        rsi = indicators.get('rsi', 'N/A')
        print(f"  RSI (14):           {rsi:.2f}" if isinstance(rsi, (int, float)) else f"  RSI (14):           {rsi}")

        macd = indicators.get('macd', 'N/A')
        print(f"  MACD:               {macd:.4f}" if isinstance(macd, (int, float)) else f"  MACD:               {macd}")

        macd_sig = indicators.get('macd_signal', 'N/A')
        print(f"  MACD Signal:        {macd_sig:.4f}" if isinstance(macd_sig, (int, float)) else f"  MACD Signal:        {macd_sig}")

        macd_hist = indicators.get('macd_hist', 'N/A')
        print(f"  MACD Histogram:     {macd_hist:.4f}" if isinstance(macd_hist, (int, float)) else f"  MACD Histogram:     {macd_hist}")

        bb = indicators.get('bollinger_bands', {})
        if bb:
            bb_upper = bb.get('upper', 'N/A')
            bb_mid = bb.get('middle', 'N/A')
            bb_lower = bb.get('lower', 'N/A')
            print(f"  Bollinger Upper:    {bb_upper:.4f}" if isinstance(bb_upper, (int, float)) else f"  Bollinger Upper:    {bb_upper}")
            print(f"  Bollinger Middle:   {bb_mid:.4f}" if isinstance(bb_mid, (int, float)) else f"  Bollinger Middle:   {bb_mid}")
            print(f"  Bollinger Lower:    {bb_lower:.4f}" if isinstance(bb_lower, (int, float)) else f"  Bollinger Lower:    {bb_lower}")

        atr = indicators.get('atr', 'N/A')
        print(f"  ATR (14):           {atr:.4f}" if isinstance(atr, (int, float)) else f"  ATR (14):           {atr}")

        adx = indicators.get('adx', 'N/A')
        print(f"  ADX (14):           {adx:.2f}" if isinstance(adx, (int, float)) else f"  ADX (14):           {adx}")

        sma = indicators.get('sma', {})
        if sma:
            sma20 = sma.get('sma_20', 'N/A')
            sma50 = sma.get('sma_50', 'N/A')
            print(f"  SMA 20:             {sma20:.4f}" if isinstance(sma20, (int, float)) else f"  SMA 20:             {sma20}")
            print(f"  SMA 50:             {sma50:.4f}" if isinstance(sma50, (int, float)) else f"  SMA 50:             {sma50}")

        ema = indicators.get('ema', {})
        if ema:
            ema12 = ema.get('ema_12', 'N/A')
            ema26 = ema.get('ema_26', 'N/A')
            print(f"  EMA 12:             {ema12:.4f}" if isinstance(ema12, (int, float)) else f"  EMA 12:             {ema12}")
            print(f"  EMA 26:             {ema26:.4f}" if isinstance(ema26, (int, float)) else f"  EMA 26:             {ema26}")
    print()

    # ML Prediction
    ml_pred = analysis.get('ml_prediction')
    if ml_pred:
        print("ML PREDICTION (4-Model Ensemble):")
        print("-" * 70)
        print(f"  Direction:          {ml_pred.get('direction', 'N/A')}")
        print(f"  Confidence:         {ml_pred.get('confidence', 0):.2f}%")
        print(f"  Expected Return:    {ml_pred.get('expected_return', 0):.2f}%")

        models = ml_pred.get('model_predictions', {})
        if models:
            print(f"\n  Individual Models:")
            print(f"    Random Forest:    {models.get('random_forest', 'N/A')}")
            print(f"    Gradient Boost:   {models.get('gradient_boost', 'N/A')}")
            print(f"    XGBoost:          {models.get('xgboost', 'N/A')}")
            print(f"    LSTM:             {models.get('lstm', 'N/A')}")
    print()

    # Candlestick Patterns
    patterns_5m = analysis.get('patterns_5m', [])
    patterns_4h = analysis.get('patterns_4h', [])

    print("CANDLESTICK PATTERNS:")
    print("-" * 70)

    if patterns_5m:
        print(f"  5-Minute Patterns ({len(patterns_5m)} found):")
        for i, pattern in enumerate(patterns_5m[:3], 1):
            print(f"    {i}. {pattern.get('pattern', 'N/A')} - {pattern.get('signal', 'N/A')}")
    else:
        print("  5-Minute Patterns: None detected")

    if patterns_4h:
        print(f"\n  4-Hour Patterns ({len(patterns_4h)} found):")
        for i, pattern in enumerate(patterns_4h[:3], 1):
            print(f"    {i}. {pattern.get('pattern', 'N/A')} - {pattern.get('signal', 'N/A')}")
            entry_exit = pattern.get('entry_exit')
            if entry_exit and i == 1:  # Show details for first pattern
                print(f"       Entry: {entry_exit.get('entry_price', 'N/A'):.4f}")
                print(f"       Stop Loss: {entry_exit.get('stop_loss', 'N/A'):.4f}")
                print(f"       Take Profit: {entry_exit.get('take_profit', 'N/A'):.4f}")
                print(f"       Risk/Reward: 1:{entry_exit.get('risk_reward_ratio', 'N/A'):.2f}")
    else:
        print("  4-Hour Patterns: None detected")
    print()

    # Trading Recommendation
    print("="*70)
    print("TRADING RECOMMENDATION")
    print("="*70)

    # Determine recommendation based on scoring system
    score = 0
    reasons = []

    # Signal strength
    if signal in ['STRONG BUY', 'BUY'] and strength >= 20:
        score += 1
        reasons.append(f"Signal: {signal} ({strength:.1f}%)")
    elif signal in ['STRONG SELL', 'SELL'] and strength >= 20:
        score += 1
        reasons.append(f"Signal: {signal} ({strength:.1f}%)")

    # Patterns
    if patterns_4h or patterns_5m:
        score += 1
        reasons.append(f"Patterns: {len(patterns_4h)} on 4H, {len(patterns_5m)} on 5m")

    # ML
    if ml_pred and ml_pred.get('confidence', 0) >= 50:
        score += 1
        reasons.append(f"ML: {ml_pred['direction']} ({ml_pred['confidence']:.1f}%)")

    print(f"\nEntry Score: {score}/3 conditions met")
    print(f"Minimum required: 2/3 for entry\n")

    if score >= 2:
        print("RECOMMENDATION: ENTER TRADE")
        direction = "LONG" if signal in ['STRONG BUY', 'BUY'] else "SHORT"
        print(f"Direction: {direction}")
        print(f"\nReasons:")
        for reason in reasons:
            print(f"  - {reason}")

        # Show entry/exit if available
        if patterns_4h and patterns_4h[0].get('entry_exit'):
            ee = patterns_4h[0]['entry_exit']
            print(f"\nSuggested Entry/Exit:")
            print(f"  Entry Price: {ee.get('entry_price', 'N/A'):.4f}")
            print(f"  Stop Loss: {ee.get('stop_loss', 'N/A'):.4f} ({ee.get('stop_loss_reasoning', 'N/A')})")
            print(f"  Take Profit: {ee.get('take_profit', 'N/A'):.4f} ({ee.get('take_profit_reasoning', 'N/A')})")
            print(f"  Risk/Reward: 1:{ee.get('risk_reward_ratio', 'N/A'):.2f}")
            print(f"  Potential Profit: {ee.get('potential_profit_pct', 'N/A'):.2f}%")
    else:
        print("RECOMMENDATION: WAIT / NO TRADE")
        print(f"Not enough conditions met ({score}/3)")
        print(f"\nReasons to wait:")
        if score == 0:
            print("  - No strong signals detected")
        else:
            for reason in reasons:
                print(f"  - {reason}")
            print(f"  - Need at least 2/3 conditions for entry")

    print("\n" + "="*70)

    # Save results
    with open('usdjpy_analysis_today.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)

    print("\nSUCCESS: Full analysis saved to usdjpy_analysis_today.json")

else:
    print("ERROR: Could not analyze USD/JPY")
    print("Possible reasons:")
    print("  - Market is closed")
    print("  - Network connection issue")
    print("  - Symbol not available")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
