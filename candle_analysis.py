"""
Candlestick Pattern Analysis and Entry/Exit Point Calculator
Analyzes 4-hour charts for trading signals with stop loss and take profit levels
"""
import pandas as pd
import numpy as np


class CandlePatternAnalyzer:
    def __init__(self):
        self.patterns = {
            'bullish': [],
            'bearish': [],
            'neutral': []
        }

    def analyze_patterns(self, df):
        """
        Analyze candlestick patterns from OHLCV data

        Args:
            df: DataFrame with OHLC data

        Returns:
            dict: Detected patterns and their strength
        """
        patterns_found = []

        if len(df) < 10:
            return patterns_found

        # Get last 10 candles for pattern recognition
        recent = df.tail(10)

        # Check for various patterns
        patterns_found.extend(self._check_engulfing(recent))
        patterns_found.extend(self._check_doji(recent))
        patterns_found.extend(self._check_hammer(recent))
        patterns_found.extend(self._check_shooting_star(recent))
        patterns_found.extend(self._check_morning_evening_star(recent))
        patterns_found.extend(self._check_three_soldiers_crows(recent))
        patterns_found.extend(self._check_harami(recent))
        patterns_found.extend(self._check_piercing_dark_cloud(recent))

        return patterns_found

    def _check_engulfing(self, df):
        """Check for bullish/bearish engulfing patterns"""
        patterns = []

        if len(df) < 2:
            return patterns

        prev = df.iloc[-2]
        curr = df.iloc[-1]

        prev_body = abs(prev['close'] - prev['open'])
        curr_body = abs(curr['close'] - curr['open'])

        # Bullish Engulfing
        if (prev['close'] < prev['open'] and  # Previous red candle
            curr['close'] > curr['open'] and  # Current green candle
            curr['open'] < prev['close'] and  # Opens below previous close
            curr['close'] > prev['open'] and  # Closes above previous open
            curr_body > prev_body * 1.2):     # Current body larger

            patterns.append({
                'name': 'Bullish Engulfing',
                'type': 'bullish',
                'strength': 8,
                'description': 'Strong reversal signal - buyers overwhelm sellers'
            })

        # Bearish Engulfing
        if (prev['close'] > prev['open'] and  # Previous green candle
            curr['close'] < curr['open'] and  # Current red candle
            curr['open'] > prev['close'] and  # Opens above previous close
            curr['close'] < prev['open'] and  # Closes below previous open
            curr_body > prev_body * 1.2):     # Current body larger

            patterns.append({
                'name': 'Bearish Engulfing',
                'type': 'bearish',
                'strength': 8,
                'description': 'Strong reversal signal - sellers overwhelm buyers'
            })

        return patterns

    def _check_doji(self, df):
        """Check for Doji patterns"""
        patterns = []

        curr = df.iloc[-1]
        body = abs(curr['close'] - curr['open'])
        range_size = curr['high'] - curr['low']

        if range_size == 0:
            return patterns

        body_percentage = (body / range_size) * 100

        # Doji (body is very small compared to range)
        if body_percentage < 5:
            patterns.append({
                'name': 'Doji',
                'type': 'neutral',
                'strength': 6,
                'description': 'Indecision in market - potential reversal'
            })

        return patterns

    def _check_hammer(self, df):
        """Check for Hammer and Inverted Hammer patterns"""
        patterns = []

        curr = df.iloc[-1]
        body = abs(curr['close'] - curr['open'])
        upper_shadow = curr['high'] - max(curr['open'], curr['close'])
        lower_shadow = min(curr['open'], curr['close']) - curr['low']

        # Hammer (bullish)
        if (lower_shadow > body * 2 and
            upper_shadow < body * 0.3 and
            body > 0):

            patterns.append({
                'name': 'Hammer',
                'type': 'bullish',
                'strength': 7,
                'description': 'Bullish reversal - rejection of lower prices'
            })

        # Inverted Hammer
        if (upper_shadow > body * 2 and
            lower_shadow < body * 0.3 and
            body > 0):

            patterns.append({
                'name': 'Inverted Hammer',
                'type': 'bullish',
                'strength': 6,
                'description': 'Potential bullish reversal - needs confirmation'
            })

        return patterns

    def _check_shooting_star(self, df):
        """Check for Shooting Star pattern"""
        patterns = []

        curr = df.iloc[-1]
        body = abs(curr['close'] - curr['open'])
        upper_shadow = curr['high'] - max(curr['open'], curr['close'])
        lower_shadow = min(curr['open'], curr['close']) - curr['low']

        # Shooting Star (bearish)
        if (upper_shadow > body * 2 and
            lower_shadow < body * 0.3 and
            curr['close'] < curr['open']):  # Red candle

            patterns.append({
                'name': 'Shooting Star',
                'type': 'bearish',
                'strength': 7,
                'description': 'Bearish reversal - rejection of higher prices'
            })

        return patterns

    def _check_morning_evening_star(self, df):
        """Check for Morning Star and Evening Star patterns"""
        patterns = []

        if len(df) < 3:
            return patterns

        first = df.iloc[-3]
        second = df.iloc[-2]
        third = df.iloc[-1]

        first_body = abs(first['close'] - first['open'])
        second_body = abs(second['close'] - second['open'])
        third_body = abs(third['close'] - third['open'])

        # Morning Star (bullish)
        if (first['close'] < first['open'] and  # First: red candle
            second_body < first_body * 0.3 and  # Second: small body (star)
            third['close'] > third['open'] and  # Third: green candle
            third['close'] > first['open'] / 2 + first['close'] / 2):  # Closes above midpoint

            patterns.append({
                'name': 'Morning Star',
                'type': 'bullish',
                'strength': 9,
                'description': 'Very strong bullish reversal pattern'
            })

        # Evening Star (bearish)
        if (first['close'] > first['open'] and  # First: green candle
            second_body < first_body * 0.3 and  # Second: small body (star)
            third['close'] < third['open'] and  # Third: red candle
            third['close'] < first['open'] / 2 + first['close'] / 2):  # Closes below midpoint

            patterns.append({
                'name': 'Evening Star',
                'type': 'bearish',
                'strength': 9,
                'description': 'Very strong bearish reversal pattern'
            })

        return patterns

    def _check_three_soldiers_crows(self, df):
        """Check for Three White Soldiers and Three Black Crows"""
        patterns = []

        if len(df) < 3:
            return patterns

        last_three = df.tail(3)

        # Three White Soldiers (bullish)
        all_green = all(candle['close'] > candle['open'] for _, candle in last_three.iterrows())
        ascending = all(last_three.iloc[i]['close'] > last_three.iloc[i-1]['close']
                       for i in range(1, 3))

        if all_green and ascending:
            patterns.append({
                'name': 'Three White Soldiers',
                'type': 'bullish',
                'strength': 9,
                'description': 'Strong bullish continuation pattern'
            })

        # Three Black Crows (bearish)
        all_red = all(candle['close'] < candle['open'] for _, candle in last_three.iterrows())
        descending = all(last_three.iloc[i]['close'] < last_three.iloc[i-1]['close']
                        for i in range(1, 3))

        if all_red and descending:
            patterns.append({
                'name': 'Three Black Crows',
                'type': 'bearish',
                'strength': 9,
                'description': 'Strong bearish continuation pattern'
            })

        return patterns

    def _check_harami(self, df):
        """Check for Bullish/Bearish Harami patterns"""
        patterns = []

        if len(df) < 2:
            return patterns

        prev = df.iloc[-2]
        curr = df.iloc[-1]

        # Bullish Harami
        if (prev['close'] < prev['open'] and  # Previous red candle
            curr['close'] > curr['open'] and  # Current green candle
            curr['open'] > prev['close'] and  # Opens above previous close
            curr['close'] < prev['open']):    # Closes below previous open

            patterns.append({
                'name': 'Bullish Harami',
                'type': 'bullish',
                'strength': 7,
                'description': 'Bullish reversal - momentum slowing'
            })

        # Bearish Harami
        if (prev['close'] > prev['open'] and  # Previous green candle
            curr['close'] < curr['open'] and  # Current red candle
            curr['open'] < prev['close'] and  # Opens below previous close
            curr['close'] > prev['open']):    # Closes above previous open

            patterns.append({
                'name': 'Bearish Harami',
                'type': 'bearish',
                'strength': 7,
                'description': 'Bearish reversal - momentum slowing'
            })

        return patterns

    def _check_piercing_dark_cloud(self, df):
        """Check for Piercing Line and Dark Cloud Cover"""
        patterns = []

        if len(df) < 2:
            return patterns

        prev = df.iloc[-2]
        curr = df.iloc[-1]

        prev_midpoint = (prev['open'] + prev['close']) / 2

        # Piercing Line (bullish)
        if (prev['close'] < prev['open'] and  # Previous red candle
            curr['close'] > curr['open'] and  # Current green candle
            curr['open'] < prev['low'] and    # Gaps down
            curr['close'] > prev_midpoint and # Closes above midpoint
            curr['close'] < prev['open']):    # But below previous open

            patterns.append({
                'name': 'Piercing Line',
                'type': 'bullish',
                'strength': 8,
                'description': 'Strong bullish reversal signal'
            })

        # Dark Cloud Cover (bearish)
        if (prev['close'] > prev['open'] and  # Previous green candle
            curr['close'] < curr['open'] and  # Current red candle
            curr['open'] > prev['high'] and   # Gaps up
            curr['close'] < prev_midpoint and # Closes below midpoint
            curr['close'] > prev['open']):    # But above previous open

            patterns.append({
                'name': 'Dark Cloud Cover',
                'type': 'bearish',
                'strength': 8,
                'description': 'Strong bearish reversal signal'
            })

        return patterns


class EntryExitCalculator:
    def __init__(self, stop_loss_percent=30, take_profit_percent=200):
        """
        Initialize with stop loss and take profit percentages

        Args:
            stop_loss_percent: Stop loss percentage (default 30%)
            take_profit_percent: Take profit percentage (default 200%)
        """
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent

    def calculate_entry_points(self, df, patterns, indicators):
        """
        Calculate optimal entry, stop loss, and take profit levels

        Args:
            df: OHLCV DataFrame
            patterns: Detected candlestick patterns
            indicators: Technical indicators

        Returns:
            dict: Entry points with stop loss and take profit levels
        """
        current_price = df['close'].iloc[-1]

        # Determine trade direction based on patterns
        bullish_strength = sum(p['strength'] for p in patterns if p['type'] == 'bullish')
        bearish_strength = sum(p['strength'] for p in patterns if p['type'] == 'bearish')

        if bullish_strength > bearish_strength and bullish_strength >= 7:
            trade_type = 'LONG'
            entry_price = current_price
            stop_loss = self._calculate_stop_loss_long(df, entry_price)
            take_profit = self._calculate_take_profit_long(entry_price, stop_loss)

        elif bearish_strength > bullish_strength and bearish_strength >= 7:
            trade_type = 'SHORT'
            entry_price = current_price
            stop_loss = self._calculate_stop_loss_short(df, entry_price)
            take_profit = self._calculate_take_profit_short(entry_price, stop_loss)

        else:
            return {
                'trade_type': 'NO TRADE',
                'recommendation': 'Insufficient pattern strength - wait for clearer signal',
                'entry_price': None,
                'stop_loss': None,
                'take_profit': None
            }

        # Calculate risk/reward ratio
        if trade_type == 'LONG':
            risk = entry_price - stop_loss
            reward = take_profit - entry_price
        else:  # SHORT
            risk = stop_loss - entry_price
            reward = entry_price - take_profit

        risk_reward_ratio = reward / risk if risk > 0 else 0

        # Calculate position size suggestion (1% risk rule)
        risk_percent = abs((stop_loss - entry_price) / entry_price) * 100

        return {
            'trade_type': trade_type,
            'entry_price': round(entry_price, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'risk_percent': round(risk_percent, 2),
            'potential_profit_percent': round(abs((take_profit - entry_price) / entry_price) * 100, 2),
            'recommendation': self._generate_recommendation(trade_type, patterns, risk_reward_ratio),
            'key_levels': self._identify_key_levels(df, entry_price)
        }

    def _calculate_stop_loss_long(self, df, entry_price):
        """Calculate stop loss for LONG position"""
        # Use recent swing low or 30% stop loss, whichever is closer
        recent_low = df['low'].tail(20).min()

        percent_stop = entry_price * (1 - self.stop_loss_percent / 100)
        swing_low_stop = recent_low * 0.98  # Slightly below swing low

        # Use the higher stop loss (less risk)
        return max(percent_stop, swing_low_stop)

    def _calculate_stop_loss_short(self, df, entry_price):
        """Calculate stop loss for SHORT position"""
        # Use recent swing high or 30% stop loss, whichever is closer
        recent_high = df['high'].tail(20).max()

        percent_stop = entry_price * (1 + self.stop_loss_percent / 100)
        swing_high_stop = recent_high * 1.02  # Slightly above swing high

        # Use the lower stop loss (less risk)
        return min(percent_stop, swing_high_stop)

    def _calculate_take_profit_long(self, entry_price, stop_loss):
        """Calculate take profit for LONG position (200% of risk)"""
        risk = entry_price - stop_loss
        take_profit = entry_price + (risk * (self.take_profit_percent / 100) * 2)
        return take_profit

    def _calculate_take_profit_short(self, entry_price, stop_loss):
        """Calculate take profit for SHORT position (200% of risk)"""
        risk = stop_loss - entry_price
        take_profit = entry_price - (risk * (self.take_profit_percent / 100) * 2)
        return take_profit

    def _identify_key_levels(self, df, current_price):
        """Identify support and resistance levels"""
        # Calculate pivot points
        high = df['high'].tail(20).max()
        low = df['low'].tail(20).min()
        close = df['close'].tail(20).mean()

        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)

        return {
            'pivot': round(pivot, 2),
            'resistance_1': round(r1, 2),
            'resistance_2': round(r2, 2),
            'support_1': round(s1, 2),
            'support_2': round(s2, 2)
        }

    def _generate_recommendation(self, trade_type, patterns, risk_reward):
        """Generate trading recommendation"""
        pattern_names = [p['name'] for p in patterns]

        if risk_reward >= 2:
            confidence = "HIGH"
        elif risk_reward >= 1.5:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        recommendation = f"{confidence} confidence {trade_type} setup"

        if patterns:
            recommendation += f" based on {', '.join(pattern_names[:2])}"

        return recommendation
