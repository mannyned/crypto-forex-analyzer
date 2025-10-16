"""
Market analyzer with advanced signal generation
"""
from data_fetcher import DataFetcher
from technical_indicators import calculate_all_indicators
from sentiment_analyzer import SentimentAnalyzer
from candle_analysis import CandlePatternAnalyzer, EntryExitCalculator


class MarketAnalyzer:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.candle_analyzer = CandlePatternAnalyzer()
        self.entry_exit_calculator = EntryExitCalculator()  # Now uses dynamic analysis

    def generate_signal(self, indicators, sentiment_score=0):
        """
        Generate trading signal based on multiple technical indicators

        Returns:
            dict: {
                'signal': 'STRONG BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG SELL',
                'score': int (-15 to +15),
                'strength': float (0-100),
                'reasons': list of strings
            }
        """
        if not indicators:
            return {
                'signal': 'HOLD',
                'score': 0,
                'strength': 0,
                'reasons': ['Insufficient data']
            }

        score = 0
        buy_signals = 0
        sell_signals = 0
        reasons = []

        close = indicators['close']

        # === MOMENTUM INDICATORS ===

        # RSI Analysis
        if indicators.get('rsi'):
            rsi = indicators['rsi']
            if rsi < 30:
                score += 2
                buy_signals += 1
                reasons.append(f"RSI oversold ({rsi:.2f})")
            elif rsi < 40:
                score += 1
                buy_signals += 1
                reasons.append(f"RSI near oversold ({rsi:.2f})")
            elif rsi > 70:
                score -= 2
                sell_signals += 1
                reasons.append(f"RSI overbought ({rsi:.2f})")
            elif rsi > 60:
                score -= 1
                sell_signals += 1
                reasons.append(f"RSI near overbought ({rsi:.2f})")

        # Williams %R
        if indicators.get('williams_r'):
            wr = indicators['williams_r']
            if wr < -80:
                score += 1
                buy_signals += 1
                reasons.append(f"Williams %R oversold ({wr:.2f})")
            elif wr > -20:
                score -= 1
                sell_signals += 1
                reasons.append(f"Williams %R overbought ({wr:.2f})")

        # Stochastic Oscillator
        if indicators.get('stoch_k') and indicators.get('stoch_d'):
            stoch_k = indicators['stoch_k']
            stoch_d = indicators['stoch_d']
            if stoch_k < 20 and stoch_d < 20:
                score += 2
                buy_signals += 1
                reasons.append(f"Stochastic oversold (K:{stoch_k:.2f}, D:{stoch_d:.2f})")
            elif stoch_k > 80 and stoch_d > 80:
                score -= 2
                sell_signals += 1
                reasons.append(f"Stochastic overbought (K:{stoch_k:.2f}, D:{stoch_d:.2f})")
            elif stoch_k > stoch_d and stoch_k < 50:
                score += 1
                buy_signals += 1
                reasons.append("Stochastic bullish crossover")
            elif stoch_k < stoch_d and stoch_k > 50:
                score -= 1
                sell_signals += 1
                reasons.append("Stochastic bearish crossover")

        # ROC (Rate of Change)
        if indicators.get('roc'):
            roc = indicators['roc']
            if roc > 5:
                score += 1
                buy_signals += 1
                reasons.append(f"Strong positive momentum (ROC: {roc:.2f}%)")
            elif roc < -5:
                score -= 1
                sell_signals += 1
                reasons.append(f"Strong negative momentum (ROC: {roc:.2f}%)")

        # === TREND INDICATORS ===

        # MACD
        if indicators.get('macd') and indicators.get('macd_signal'):
            macd = indicators['macd']
            macd_signal = indicators['macd_signal']
            if macd > macd_signal and macd > 0:
                score += 2
                buy_signals += 1
                reasons.append(f"MACD bullish (MACD: {macd:.2f} > Signal: {macd_signal:.2f})")
            elif macd < macd_signal and macd < 0:
                score -= 2
                sell_signals += 1
                reasons.append(f"MACD bearish (MACD: {macd:.2f} < Signal: {macd_signal:.2f})")

        # ADX (Trend Strength)
        if indicators.get('adx') and indicators.get('plus_di') and indicators.get('minus_di'):
            adx = indicators['adx']
            plus_di = indicators['plus_di']
            minus_di = indicators['minus_di']

            if adx > 25:  # Strong trend
                if plus_di > minus_di:
                    score += 2
                    buy_signals += 1
                    reasons.append(f"Strong uptrend (ADX: {adx:.2f}, +DI > -DI)")
                else:
                    score -= 2
                    sell_signals += 1
                    reasons.append(f"Strong downtrend (ADX: {adx:.2f}, -DI > +DI)")

        # Moving Average Analysis
        sma_20 = indicators.get('sma_20')
        sma_50 = indicators.get('sma_50')
        sma_200 = indicators.get('sma_200')

        if sma_20 and sma_50 and sma_200:
            # Golden alignment (bullish)
            if close > sma_20 > sma_50 > sma_200:
                score += 3
                buy_signals += 1
                reasons.append("Golden alignment: Price > SMA20 > SMA50 > SMA200")
            # Death alignment (bearish)
            elif close < sma_20 < sma_50 < sma_200:
                score -= 3
                sell_signals += 1
                reasons.append("Death alignment: Price < SMA20 < SMA50 < SMA200")
            # Golden Cross (SMA50 > SMA200)
            elif sma_50 > sma_200 and close > sma_50:
                score += 2
                buy_signals += 1
                reasons.append("Price above golden cross (SMA50 > SMA200)")
            # Death Cross (SMA50 < SMA200)
            elif sma_50 < sma_200 and close < sma_50:
                score -= 2
                sell_signals += 1
                reasons.append("Price below death cross (SMA50 < SMA200)")

        # Parabolic SAR
        if indicators.get('psar'):
            psar = indicators['psar']
            if close > psar:
                score += 1
                buy_signals += 1
                reasons.append(f"Price above Parabolic SAR ({psar:.2f})")
            else:
                score -= 1
                sell_signals += 1
                reasons.append(f"Price below Parabolic SAR ({psar:.2f})")

        # Supertrend
        if indicators.get('supertrend') and indicators.get('supertrend_direction'):
            supertrend = indicators['supertrend']
            direction = indicators['supertrend_direction']
            
            if direction == 1:  # Uptrend
                score += 2
                buy_signals += 1
                reasons.append(f"Supertrend uptrend (ST: {supertrend:.2f})")
            elif direction == -1:  # Downtrend
                score -= 2
                sell_signals += 1
                reasons.append(f"Supertrend downtrend (ST: {supertrend:.2f})")

        # Ichimoku Cloud
        if indicators.get('ichimoku_span_a') and indicators.get('ichimoku_span_b'):
            span_a = indicators['ichimoku_span_a']
            span_b = indicators['ichimoku_span_b']
            cloud_top = max(span_a, span_b)
            cloud_bottom = min(span_a, span_b)

            if close > cloud_top:
                score += 2
                buy_signals += 1
                reasons.append("Price above Ichimoku cloud (bullish)")
            elif close < cloud_bottom:
                score -= 2
                sell_signals += 1
                reasons.append("Price below Ichimoku cloud (bearish)")

        # === VOLUME INDICATORS ===

        # MFI (Money Flow Index)
        if indicators.get('mfi'):
            mfi = indicators['mfi']
            if mfi < 20:
                score += 2
                buy_signals += 1
                reasons.append(f"MFI oversold ({mfi:.2f}) - buying pressure")
            elif mfi > 80:
                score -= 2
                sell_signals += 1
                reasons.append(f"MFI overbought ({mfi:.2f}) - selling pressure")

        # Chaikin Money Flow
        if indicators.get('cmf'):
            cmf = indicators['cmf']
            if cmf > 0.1:
                score += 1
                buy_signals += 1
                reasons.append(f"Positive money flow (CMF: {cmf:.2f})")
            elif cmf < -0.1:
                score -= 1
                sell_signals += 1
                reasons.append(f"Negative money flow (CMF: {cmf:.2f})")

        # VWAP
        if indicators.get('vwap'):
            vwap = indicators['vwap']
            if close > vwap:
                score += 1
                buy_signals += 1
                reasons.append(f"Price above VWAP ({vwap:.2f})")
            else:
                score -= 1
                sell_signals += 1
                reasons.append(f"Price below VWAP ({vwap:.2f})")

        # === VOLATILITY INDICATORS ===

        # Bollinger Bands
        if indicators.get('bb_upper') and indicators.get('bb_lower') and indicators.get('bb_middle'):
            bb_upper = indicators['bb_upper']
            bb_lower = indicators['bb_lower']
            bb_middle = indicators['bb_middle']

            if close <= bb_lower:
                score += 2
                buy_signals += 1
                reasons.append(f"Price at lower Bollinger Band ({bb_lower:.2f})")
            elif close >= bb_upper:
                score -= 2
                sell_signals += 1
                reasons.append(f"Price at upper Bollinger Band ({bb_upper:.2f})")
            elif close > bb_middle:
                score += 1
                reasons.append("Price above BB middle")
            else:
                score -= 1
                reasons.append("Price below BB middle")

        # === FIBONACCI LEVELS ===
        if indicators.get('fib_618') and indicators.get('fib_382'):
            fib_618 = indicators['fib_618']
            fib_382 = indicators['fib_382']

            # Near golden ratio support
            if abs(close - fib_618) / close < 0.01:
                score += 1
                reasons.append(f"Near Fibonacci 61.8% support ({fib_618:.2f})")

        # === SENTIMENT ANALYSIS ===
        # Add sentiment score to overall score
        if sentiment_score > 0.5:
            score += 2
            buy_signals += 1
            reasons.append(f"Positive market sentiment ({sentiment_score:.2f})")
        elif sentiment_score < -0.5:
            score -= 2
            sell_signals += 1
            reasons.append(f"Negative market sentiment ({sentiment_score:.2f})")
        elif abs(sentiment_score) > 0.2:
            if sentiment_score > 0:
                score += 1
                buy_signals += 1
                reasons.append(f"Slightly positive sentiment ({sentiment_score:.2f})")
            else:
                score -= 1
                sell_signals += 1
                reasons.append(f"Slightly negative sentiment ({sentiment_score:.2f})")

        # === GENERATE FINAL SIGNAL ===

        # Calculate strength percentage
        max_score = 15
        strength = min(100, max(0, (abs(score) / max_score) * 100))

        # Determine signal
        if score >= 6 and buy_signals > sell_signals:
            signal = 'STRONG BUY'
        elif score >= 2 and buy_signals > sell_signals:
            signal = 'BUY'
        elif score <= -6 and sell_signals > buy_signals:
            signal = 'STRONG SELL'
        elif score <= -2 and sell_signals > buy_signals:
            signal = 'SELL'
        else:
            signal = 'HOLD'

        return {
            'signal': signal,
            'score': score,
            'strength': round(strength, 2),
            'reasons': reasons[:10]  # Limit to top 10 reasons
        }

    def analyze_symbol(self, symbol, market_type='crypto', timeframe='1h', limit=100):
        """
        Analyze a single symbol

        Args:
            symbol: Trading symbol
            market_type: 'crypto' or 'forex'
            timeframe: Timeframe for analysis
            limit: Number of candles to analyze

        Returns:
            dict: Complete analysis with indicators and signals
        """
        try:
            # Fetch data
            if market_type == 'crypto':
                df = self.fetcher.fetch_crypto_data(symbol, timeframe, limit)
            else:
                period_map = {'1h': '60d', '4h': '120d', '1d': '2y'}
                period = period_map.get(timeframe, '60d')
                df = self.fetcher.fetch_forex_data(symbol, period=period, interval=timeframe)

            if df is None or len(df) < 52:
                return None

            # Calculate indicators
            indicators = calculate_all_indicators(df)

            if not indicators:
                return None

            # Get sentiment analysis
            if market_type == 'crypto':
                sentiment = self.sentiment_analyzer.get_crypto_sentiment(symbol)
            else:
                sentiment = self.sentiment_analyzer.get_forex_sentiment(symbol)

            # Add sentiment to signal generation
            sentiment_score = sentiment['score'] * 2  # Scale sentiment (-2 to +2)

            # Generate signal
            signal_data = self.generate_signal(indicators, sentiment_score)

            # Fetch 4-hour chart data for candlestick pattern analysis
            if market_type == 'crypto':
                df_4h = self.fetcher.fetch_crypto_data(symbol, '4h', 100)
            else:
                df_4h = self.fetcher.fetch_forex_data(symbol, period='120d', interval='4h')

            # Analyze candlestick patterns on 4-hour chart
            candle_patterns = []
            entry_exit_data = None

            if df_4h is not None and len(df_4h) >= 10:
                candle_patterns = self.candle_analyzer.analyze_patterns(df_4h)

                # Calculate entry/exit points if patterns found
                if candle_patterns:
                    entry_exit_data = self.entry_exit_calculator.calculate_entry_points(
                        df_4h, candle_patterns, indicators
                    )

            # Get current price and change
            current_price = self.fetcher.get_current_price(symbol, market_type)
            change_24h = self.fetcher.get_24h_change(symbol, market_type)

            return {
                'symbol': symbol,
                'market_type': market_type,
                'current_price': current_price,
                'change_24h': change_24h,
                'signal': signal_data['signal'],
                'score': signal_data['score'],
                'strength': signal_data['strength'],
                'reasons': signal_data['reasons'],
                'indicators': indicators,
                'sentiment': sentiment,
                'candle_patterns': candle_patterns,
                'entry_exit': entry_exit_data
            }

        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return None

    def analyze_all_markets(self):
        """
        Analyze all configured crypto and forex markets

        Returns:
            dict: {
                'crypto': [...],
                'forex': [...],
                'top_opportunities': [...]
            }
        """
        from data_fetcher import CRYPTO_PAIRS, FOREX_PAIRS, CRYPTO_NAMES, FOREX_NAMES

        results = {
            'crypto': [],
            'forex': [],
            'top_opportunities': []
        }

        # Analyze crypto
        print("Analyzing cryptocurrencies...")
        for symbol in CRYPTO_PAIRS:
            print(f"  - {symbol}")
            analysis = self.analyze_symbol(symbol, 'crypto')
            if analysis:
                analysis['name'] = CRYPTO_NAMES.get(symbol, symbol)
                results['crypto'].append(analysis)

        # Analyze forex
        print("Analyzing forex pairs...")
        for symbol in FOREX_PAIRS:
            print(f"  - {symbol}")
            analysis = self.analyze_symbol(symbol, 'forex')
            if analysis:
                analysis['name'] = FOREX_NAMES.get(symbol, symbol)
                results['forex'].append(analysis)

        # Find top opportunities (strong buy/sell signals with high strength)
        all_markets = results['crypto'] + results['forex']
        opportunities = [
            m for m in all_markets
            if m['signal'] in ['STRONG BUY', 'STRONG SELL'] and m['strength'] > 30
        ]
        opportunities.sort(key=lambda x: x['strength'], reverse=True)
        results['top_opportunities'] = opportunities[:10]

        return results


if __name__ == '__main__':
    analyzer = MarketAnalyzer()
    results = analyzer.analyze_all_markets()

    print("\n=== TOP OPPORTUNITIES ===")
    for opp in results['top_opportunities']:
        print(f"{opp['name']} ({opp['symbol']}): {opp['signal']} - Strength: {opp['strength']}%")
