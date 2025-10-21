"""
Diagnostic script to understand why no trades are being executed during Brexit
"""
import yfinance as yf
from market_analyzer import MarketAnalyzer

print("Diagnosing Brexit 2016 period...")
print("="*70)

# Download Brexit period data
symbol = 'GBPUSD=X'
data = yf.download(symbol, start='2016-03-01', end='2016-09-30', interval='1d', progress=False)

print(f"\nDownloaded {len(data)} days of data for {symbol}")
print(f"Period: {data.index[0]} to {data.index[-1]}\n")

# Analyze at key dates
analyzer = MarketAnalyzer()

test_dates_indices = [50, 75, 100, 120, 140]  # Sample various points

print("Analyzing key dates:")
print("-"*70)

for idx in test_dates_indices:
    if idx >= len(data):
        continue

    date = data.index[idx]
    close_price = float(data.iloc[idx]['Close'])

    print(f"\nDate: {str(date)[:10]} | Price: ${close_price:.4f}")

    # Get analysis
    analysis = analyzer.analyze_symbol(symbol, 'forex', timeframe='1d', limit=100)

    if analysis:
        signal = analysis.get('signal', 'N/A')
        strength = analysis.get('strength', 0)
        patterns_4h = analysis.get('patterns_4h', [])
        ml_pred = analysis.get('ml_prediction')

        print(f"  Signal: {signal} (Strength: {strength:.1f}%)")
        print(f"  4H Patterns: {len(patterns_4h)} found")
        if patterns_4h:
            print(f"    Patterns: {[p['pattern'] for p in patterns_4h[:3]]}")

        if ml_pred:
            print(f"  ML Prediction: {ml_pred['direction']} (Confidence: {ml_pred['confidence']:.1f}%)")
        else:
            print(f"  ML Prediction: None")

        # Check entry conditions
        would_enter = False
        reason = ""

        if signal in ['STRONG BUY', 'BUY'] and strength >= 50:
            if patterns_4h:
                if ml_pred and ml_pred['direction'] == 'BULLISH' and ml_pred['confidence'] >= 75:
                    would_enter = True
                    reason = "All conditions met!"
                else:
                    reason = f"ML not strong enough (conf: {ml_pred['confidence']:.1f}% < 75%)" if ml_pred else "No ML prediction"
            else:
                reason = "No candlestick patterns found"
        elif signal in ['STRONG SELL', 'SELL'] and strength >= 50:
            if patterns_4h:
                if ml_pred and ml_pred['direction'] == 'BEARISH' and ml_pred['confidence'] >= 75:
                    would_enter = True
                    reason = "All conditions met!"
                else:
                    reason = f"ML not strong enough (conf: {ml_pred['confidence']:.1f}% < 75%)" if ml_pred else "No ML prediction"
            else:
                reason = "No candlestick patterns found"
        else:
            reason = f"Signal not strong enough ({signal}, {strength:.1f}%)"

        print(f"  WOULD ENTER TRADE: {would_enter}")
        print(f"  Reason: {reason}")
    else:
        print("  ERROR: No analysis available")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("\nLikely reasons for zero trades:")
print("1. ML confidence threshold too high (>=75%)")
print("2. Signal strength threshold too high (>=50%)")
print("3. Candlestick pattern detection might not be working on daily data")
print("4. Combination of all 3 conditions is too restrictive")
