"""
Test USD/JPY intraday performance: 12 AM CST to 5 PM CST today
"""
from datetime import datetime, timedelta
import yfinance as yf
from market_analyzer import MarketAnalyzer
import json

print("\n" + "="*70)
print("USD/JPY INTRADAY BACKTEST")
print("="*70)
print("Period: 12 AM CST to 5 PM CST (Today)")
print("Symbol: USDJPY=X")
print("="*70 + "\n")

# Get today's date
today = datetime.now().date()

# CST is UTC-6, so:
# 12 AM CST = 6 AM UTC
# 5 PM CST = 11 PM UTC
start_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=6)  # 6 AM UTC
end_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=23)   # 11 PM UTC

print(f"Start: {start_time} UTC (12 AM CST)")
print(f"End:   {end_time} UTC (5 PM CST)")
print()

# Download intraday data
print("Downloading 1-hour interval data for today...")

try:
    # Get 1-hour data for today
    data = yf.download('USDJPY=X', start=today, end=today + timedelta(days=1), interval='1h', progress=False)

    if data.empty:
        print("ERROR: No intraday data available")
        print("Note: Forex market may be closed or data not available for today")
        exit()

    print(f"SUCCESS: Downloaded {len(data)} hourly candles")
    print()

    # Filter to 12 AM - 5 PM CST (6 AM - 11 PM UTC)
    data_filtered = data.between_time('06:00', '23:00')

    if len(data_filtered) == 0:
        print("WARNING: No data in the specified time range")
        print("Using all available data for today:")
        data_filtered = data

    print("="*70)
    print(f"PRICE MOVEMENT ANALYSIS ({len(data_filtered)} hours)")
    print("="*70)
    print()

    # Get opening and closing prices
    if len(data_filtered) > 0:
        open_price = float(data_filtered.iloc[0]['Open'])
        close_price = float(data_filtered.iloc[-1]['Close'])
        high_price = float(data_filtered['High'].max())
        low_price = float(data_filtered['Low'].min())

        price_change = close_price - open_price
        price_change_pct = (price_change / open_price) * 100

        print(f"Opening Price (12 AM CST): {open_price:.4f}")
        print(f"Closing Price (5 PM CST):  {close_price:.4f}")
        print(f"High:                       {high_price:.4f}")
        print(f"Low:                        {low_price:.4f}")
        print()
        print(f"Price Change:               {price_change:+.4f} ({price_change_pct:+.2f}%)")

        if price_change_pct > 0:
            actual_direction = "BULLISH (UP)"
        elif price_change_pct < 0:
            actual_direction = "BEARISH (DOWN)"
        else:
            actual_direction = "NEUTRAL (FLAT)"

        print(f"Actual Direction:           {actual_direction}")
        print()

    # Analyze at key points throughout the day
    print("="*70)
    print("SIGNAL ANALYSIS AT KEY TIMES")
    print("="*70)
    print()

    analyzer = MarketAnalyzer()

    # Test at different hours
    test_points = []

    for i in range(0, len(data_filtered), max(1, len(data_filtered)//6)):  # Sample ~6 points
        if i >= len(data_filtered):
            break

        timestamp = data_filtered.index[i]
        current_price = float(data_filtered.iloc[i]['Close'])

        # Get analysis (Note: this uses current data, not historical)
        analysis = analyzer.analyze_symbol('USDJPY=X', 'forex', timeframe='1h', limit=100)

        if analysis:
            signal = analysis.get('signal', 'HOLD')
            strength = analysis.get('strength', 0)
            ml_pred = analysis.get('ml_prediction')

            # Calculate what happened after this point (next 4 hours)
            future_idx = min(i + 4, len(data_filtered) - 1)
            future_price = float(data_filtered.iloc[future_idx]['Close'])
            actual_move = ((future_price - current_price) / current_price) * 100

            test_point = {
                'time': str(timestamp),
                'price': current_price,
                'signal': signal,
                'strength': strength,
                'ml_direction': ml_pred.get('direction') if ml_pred else None,
                'ml_confidence': ml_pred.get('confidence') if ml_pred else None,
                'actual_4h_move': actual_move,
                'prediction_correct': None
            }

            # Check if prediction was correct
            if signal in ['STRONG BUY', 'BUY']:
                test_point['prediction_correct'] = actual_move > 0
            elif signal in ['STRONG SELL', 'SELL']:
                test_point['prediction_correct'] = actual_move < 0
            else:
                test_point['prediction_correct'] = abs(actual_move) < 0.1

            test_points.append(test_point)

            print(f"Time: {str(timestamp)[:16]} | Price: {current_price:.4f}")
            print(f"  Signal: {signal} ({strength:.1f}%)")
            if ml_pred:
                print(f"  ML: {ml_pred.get('direction')} ({ml_pred.get('confidence'):.1f}%)")
            print(f"  Next 4H Move: {actual_move:+.2f}%")
            print(f"  Correct: {test_point['prediction_correct']}")
            print()

    # Summary
    print("="*70)
    print("ACCURACY SUMMARY")
    print("="*70)
    print()

    correct_signals = sum(1 for tp in test_points if tp['prediction_correct'])
    total_signals = len(test_points)
    accuracy = (correct_signals / total_signals * 100) if total_signals > 0 else 0

    print(f"Test Points: {total_signals}")
    print(f"Correct Predictions: {correct_signals}")
    print(f"Signal Accuracy: {accuracy:.2f}%")
    print()

    # ML accuracy
    ml_points = [tp for tp in test_points if tp['ml_direction']]
    if ml_points:
        ml_correct = sum(1 for tp in ml_points
                        if (tp['ml_direction'] == 'BULLISH' and tp['actual_4h_move'] > 0) or
                           (tp['ml_direction'] == 'BEARISH' and tp['actual_4h_move'] < 0))
        ml_accuracy = (ml_correct / len(ml_points) * 100) if len(ml_points) > 0 else 0
        print(f"ML Predictions: {len(ml_points)}")
        print(f"ML Correct: {ml_correct}")
        print(f"ML Accuracy: {ml_accuracy:.2f}%")

    # Save results
    results = {
        'test_date': str(today),
        'period': '12 AM CST to 5 PM CST',
        'symbol': 'USDJPY=X',
        'price_stats': {
            'open': open_price,
            'close': close_price,
            'high': high_price,
            'low': low_price,
            'change': price_change,
            'change_pct': price_change_pct,
            'direction': actual_direction
        },
        'test_points': test_points,
        'accuracy': {
            'signal_accuracy': accuracy,
            'ml_accuracy': ml_accuracy if ml_points else 0,
            'total_tests': total_signals
        }
    }

    with open('usdjpy_intraday_test.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print()
    print("SUCCESS: Results saved to usdjpy_intraday_test.json")

    # Trading recommendation based on today's performance
    print()
    print("="*70)
    print("ANALYSIS INTERPRETATION")
    print("="*70)
    print()

    print("ACTUAL MARKET MOVEMENT:")
    print(f"  USD/JPY moved {price_change_pct:+.2f}% from 12 AM to 5 PM CST")
    print()

    print("MODEL PERFORMANCE:")
    print(f"  Signal accuracy: {accuracy:.1f}%")
    if ml_points:
        print(f"  ML accuracy: {ml_accuracy:.1f}%")
    print()

    if accuracy >= 60:
        print("VERDICT: Good performance - Signals were mostly accurate")
    elif accuracy >= 40:
        print("VERDICT: Mixed performance - Signals had moderate accuracy")
    else:
        print("VERDICT: Poor performance - Signals struggled today")

    print()
    print("NOTE: This test uses CURRENT market analysis applied to historical")
    print("      points, so accuracy may not reflect true historical performance.")
    print("      For accurate backtesting, the analyzer would need to use")
    print("      historical data at each point in time.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
print("TEST COMPLETE")
print("="*70)
