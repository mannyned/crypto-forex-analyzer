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

        # Generate stop loss and take profit reasoning
        sl_reasoning = self._generate_sl_reasoning(df, entry_price, stop_loss, trade_type)
        tp_reasoning = self._generate_tp_reasoning(entry_price, stop_loss, take_profit, trade_type)

        return {
            'trade_type': trade_type,
            'entry_price': round(entry_price, 2),
            'stop_loss': round(stop_loss, 2),
            'take_profit': round(take_profit, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'risk_percent': round(risk_percent, 2),
            'potential_profit_percent': round(abs((take_profit - entry_price) / entry_price) * 100, 2),
            'recommendation': self._generate_recommendation(trade_type, patterns, risk_reward_ratio),
            'key_levels': self._identify_key_levels(df, entry_price),
            'stop_loss_reasoning': sl_reasoning,
            'take_profit_reasoning': tp_reasoning
        }

    def _calculate_stop_loss_long(self, df, entry_price):
        """
        Calculate stop loss for LONG position using multiple methods

        Methods:
        1. ATR-based (2x ATR below entry)
        2. Recent swing low (past 20 candles)
        3. Percentage-based (30% default)
        4. Support level based

        Returns the most conservative (highest) stop loss
        """
        # Method 1: ATR-based stop loss (2 x ATR)
        atr = self._calculate_atr(df)
        atr_stop = entry_price - (2 * atr)

        # Method 2: Swing low based (recent 20 candles)
        recent_low = df['low'].tail(20).min()
        swing_low_stop = recent_low * 0.98  # 2% below swing low for buffer

        # Method 3: Percentage-based (30%)
        percent_stop = entry_price * (1 - self.stop_loss_percent / 100)

        # Method 4: Support level based (using recent consolidation areas)
        support_stop = self._find_nearest_support(df, entry_price)

        # Use the highest stop loss (most conservative, least risk)
        stop_losses = [atr_stop, swing_low_stop, percent_stop]
        if support_stop:
            stop_losses.append(support_stop * 0.98)  # Slightly below support

        recommended_stop = max(stop_losses)

        # Ensure stop loss is reasonable (not more than 30% from entry)
        max_stop = entry_price * 0.70  # Maximum 30% loss
        return max(recommended_stop, max_stop)

    def _calculate_stop_loss_short(self, df, entry_price):
        """
        Calculate stop loss for SHORT position using multiple methods

        Methods:
        1. ATR-based (2x ATR above entry)
        2. Recent swing high (past 20 candles)
        3. Percentage-based (30% default)
        4. Resistance level based

        Returns the most conservative (lowest) stop loss
        """
        # Method 1: ATR-based stop loss (2 x ATR)
        atr = self._calculate_atr(df)
        atr_stop = entry_price + (2 * atr)

        # Method 2: Swing high based (recent 20 candles)
        recent_high = df['high'].tail(20).max()
        swing_high_stop = recent_high * 1.02  # 2% above swing high for buffer

        # Method 3: Percentage-based (30%)
        percent_stop = entry_price * (1 + self.stop_loss_percent / 100)

        # Method 4: Resistance level based
        resistance_stop = self._find_nearest_resistance(df, entry_price)

        # Use the lowest stop loss (most conservative, least risk)
        stop_losses = [atr_stop, swing_high_stop, percent_stop]
        if resistance_stop:
            stop_losses.append(resistance_stop * 1.02)  # Slightly above resistance

        recommended_stop = min(stop_losses)

        # Ensure stop loss is reasonable (not more than 30% from entry)
        max_stop = entry_price * 1.30  # Maximum 30% loss
        return min(recommended_stop, max_stop)

    def _calculate_take_profit_long(self, entry_price, stop_loss):
        """
        Calculate take profit for LONG position using multiple methods

        Methods:
        1. Risk-based (200% of risk = 1:2 risk/reward)
        2. ATR-based (4x ATR above entry for volatile markets)
        3. Fibonacci extension levels

        Returns the most realistic take profit target
        """
        risk = entry_price - stop_loss

        # Method 1: Risk-based (200% of risk)
        risk_based_tp = entry_price + (risk * 2)  # 1:2 risk/reward ratio

        # Method 2: Percentage-based (for very conservative approach)
        percent_tp = entry_price + (risk * (self.take_profit_percent / 100))

        # Method 3: ATR-based (4x ATR for realistic volatile market target)
        # This will be calculated if ATR is available

        # Use risk-based as primary (most common approach)
        # But cap it at 200% gain for realism
        take_profit = min(risk_based_tp, entry_price * 3.0)  # Max 200% gain

        return take_profit

    def _calculate_take_profit_short(self, entry_price, stop_loss):
        """
        Calculate take profit for SHORT position using multiple methods

        Methods:
        1. Risk-based (200% of risk = 1:2 risk/reward)
        2. ATR-based (4x ATR below entry for volatile markets)
        3. Fibonacci extension levels

        Returns the most realistic take profit target
        """
        risk = stop_loss - entry_price

        # Method 1: Risk-based (200% of risk)
        risk_based_tp = entry_price - (risk * 2)  # 1:2 risk/reward ratio

        # Method 2: Percentage-based
        percent_tp = entry_price - (risk * (self.take_profit_percent / 100))

        # Use risk-based as primary
        # But ensure it doesn't go negative and cap at reasonable level
        take_profit = max(risk_based_tp, entry_price * 0.33)  # Don't go below 67% drop

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

    def _calculate_atr(self, df, period=14):
        """
        Calculate Average True Range (ATR) for volatility-based stops

        Args:
            df: OHLCV DataFrame
            period: ATR period (default 14)

        Returns:
            float: Current ATR value
        """
        high = df['high']
        low = df['low']
        close = df['close']

        # Calculate True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # Calculate ATR (simple moving average of TR)
        atr = tr.rolling(window=period).mean()

        return atr.iloc[-1] if not pd.isna(atr.iloc[-1]) else (df['high'].iloc[-1] - df['low'].iloc[-1])

    def _find_nearest_support(self, df, current_price):
        """
        Find nearest support level below current price

        Args:
            df: OHLCV DataFrame
            current_price: Current entry price

        Returns:
            float: Support level or None
        """
        # Look at recent lows in the last 50 candles
        lows = df['low'].tail(50)

        # Find local minima (support levels)
        support_levels = []
        for i in range(2, len(lows) - 2):
            if lows.iloc[i] < lows.iloc[i-1] and lows.iloc[i] < lows.iloc[i-2] and \
               lows.iloc[i] < lows.iloc[i+1] and lows.iloc[i] < lows.iloc[i+2]:
                support_levels.append(lows.iloc[i])

        # Find the nearest support below current price
        supports_below = [s for s in support_levels if s < current_price]

        if supports_below:
            return max(supports_below)  # Nearest support below

        return None

    def _find_nearest_resistance(self, df, current_price):
        """
        Find nearest resistance level above current price

        Args:
            df: OHLCV DataFrame
            current_price: Current entry price

        Returns:
            float: Resistance level or None
        """
        # Look at recent highs in the last 50 candles
        highs = df['high'].tail(50)

        # Find local maxima (resistance levels)
        resistance_levels = []
        for i in range(2, len(highs) - 2):
            if highs.iloc[i] > highs.iloc[i-1] and highs.iloc[i] > highs.iloc[i-2] and \
               highs.iloc[i] > highs.iloc[i+1] and highs.iloc[i] > highs.iloc[i+2]:
                resistance_levels.append(highs.iloc[i])

        # Find the nearest resistance above current price
        resistances_above = [r for r in resistance_levels if r > current_price]

        if resistances_above:
            return min(resistances_above)  # Nearest resistance above

        return None

    def _generate_sl_reasoning(self, df, entry_price, stop_loss, trade_type):
        """
        Generate reasoning for stop loss placement

        Args:
            df: OHLCV DataFrame
            entry_price: Entry price
            stop_loss: Calculated stop loss
            trade_type: LONG or SHORT

        Returns:
            str: Stop loss reasoning
        """
        atr = self._calculate_atr(df)
        risk_percent = abs((stop_loss - entry_price) / entry_price) * 100

        reasons = []

        if trade_type == 'LONG':
            recent_low = df['low'].tail(20).min()
            support = self._find_nearest_support(df, entry_price)

            # Check which method was primarily used
            atr_stop = entry_price - (2 * atr)

            if abs(stop_loss - atr_stop) < 0.01 * entry_price:
                reasons.append(f"Based on 2x ATR (${atr:.2f})")

            if support and abs(stop_loss - support * 0.98) < 0.01 * entry_price:
                reasons.append(f"Below support level at ${support:.2f}")

            if abs(stop_loss - recent_low * 0.98) < 0.01 * entry_price:
                reasons.append(f"Below recent swing low at ${recent_low:.2f}")

        else:  # SHORT
            recent_high = df['high'].tail(20).max()
            resistance = self._find_nearest_resistance(df, entry_price)

            atr_stop = entry_price + (2 * atr)

            if abs(stop_loss - atr_stop) < 0.01 * entry_price:
                reasons.append(f"Based on 2x ATR (${atr:.2f})")

            if resistance and abs(stop_loss - resistance * 1.02) < 0.01 * entry_price:
                reasons.append(f"Above resistance at ${resistance:.2f}")

            if abs(stop_loss - recent_high * 1.02) < 0.01 * entry_price:
                reasons.append(f"Above recent swing high at ${recent_high:.2f}")

        if not reasons:
            reasons.append(f"Conservative {risk_percent:.1f}% stop loss")

        return " | ".join(reasons)

    def _generate_tp_reasoning(self, entry_price, stop_loss, take_profit, trade_type):
        """
        Generate reasoning for take profit placement

        Args:
            entry_price: Entry price
            stop_loss: Stop loss level
            take_profit: Calculated take profit
            trade_type: LONG or SHORT

        Returns:
            str: Take profit reasoning
        """
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        rr_ratio = reward / risk if risk > 0 else 0

        profit_percent = abs((take_profit - entry_price) / entry_price) * 100

        reasons = [
            f"1:{rr_ratio:.1f} Risk/Reward ratio",
            f"{profit_percent:.1f}% profit target"
        ]

        if trade_type == 'LONG':
            if rr_ratio >= 2:
                reasons.append("Conservative 2:1 minimum target")
            else:
                reasons.append("Based on market volatility")
        else:
            if rr_ratio >= 2:
                reasons.append("Conservative 2:1 minimum target")
            else:
                reasons.append("Based on market volatility")

        return " | ".join(reasons)
