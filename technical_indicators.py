"""
Technical indicators calculator with 40+ indicators
"""
import pandas as pd
import numpy as np


def calculate_rsi(df, period=14):
    """Calculate Relative Strength Index"""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(df, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    exp1 = df['close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram


def calculate_sma(df, period):
    """Calculate Simple Moving Average"""
    return df['close'].rolling(window=period).mean()


def calculate_ema(df, period):
    """Calculate Exponential Moving Average"""
    return df['close'].ewm(span=period, adjust=False).mean()


def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    sma = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, sma, lower_band


def calculate_atr(df, period=14):
    """Calculate Average True Range"""
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    return atr

def calculate_supertrend(df, period=10, multiplier=3):
    """
    Calculate Supertrend indicator
    
    Args:
        df: DataFrame with OHLC data
        period: ATR period (default 10)
        multiplier: ATR multiplier (default 3)
    
    Returns:
        supertrend: Supertrend line values
        direction: 1 for uptrend, -1 for downtrend
    """
    # Calculate ATR
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(period).mean()
    
    # Calculate basic upper and lower bands
    hl_avg = (df['high'] + df['low']) / 2
    upper_band = hl_avg + (multiplier * atr)
    lower_band = hl_avg - (multiplier * atr)
    
    # Initialize supertrend and direction
    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=float)
    
    # Calculate supertrend
    for i in range(period, len(df)):
        if i == period:
            supertrend.iloc[i] = upper_band.iloc[i]
            direction.iloc[i] = -1
        else:
            # Adjust bands based on previous values
            if upper_band.iloc[i] < supertrend.iloc[i-1] or df['close'].iloc[i-1] > supertrend.iloc[i-1]:
                upper_band.iloc[i] = upper_band.iloc[i]
            else:
                upper_band.iloc[i] = supertrend.iloc[i-1]
                
            if lower_band.iloc[i] > supertrend.iloc[i-1] or df['close'].iloc[i-1] < supertrend.iloc[i-1]:
                lower_band.iloc[i] = lower_band.iloc[i]
            else:
                lower_band.iloc[i] = supertrend.iloc[i-1]
            
            # Determine trend direction
            if df['close'].iloc[i] <= upper_band.iloc[i]:
                supertrend.iloc[i] = upper_band.iloc[i]
                direction.iloc[i] = -1  # Downtrend
            else:
                supertrend.iloc[i] = lower_band.iloc[i]
                direction.iloc[i] = 1   # Uptrend
    
    return supertrend, direction

def calculate_stochastic(df, period=14, smooth_k=3, smooth_d=3):
    """Calculate Stochastic Oscillator (%K and %D)"""
    low_min = df['low'].rolling(window=period).min()
    high_max = df['high'].rolling(window=period).max()

    k = 100 * ((df['close'] - low_min) / (high_max - low_min))
    k = k.rolling(window=smooth_k).mean()
    d = k.rolling(window=smooth_d).mean()

    return k, d


def calculate_roc(df, period=12):
    """Calculate Rate of Change"""
    roc = ((df['close'] - df['close'].shift(period)) / df['close'].shift(period)) * 100
    return roc


def calculate_williams_r(df, period=14):
    """Calculate Williams %R"""
    high_max = df['high'].rolling(window=period).max()
    low_min = df['low'].rolling(window=period).min()

    williams_r = -100 * ((high_max - df['close']) / (high_max - low_min))
    return williams_r


def calculate_adx(df, period=14):
    """Calculate Average Directional Index (ADX) with +DI and -DI"""
    # Calculate True Range
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)

    # Calculate directional movement
    up_move = df['high'] - df['high'].shift()
    down_move = df['low'].shift() - df['low']

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    # Smooth the values
    atr = true_range.rolling(window=period).mean()
    plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).mean() / atr)
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).mean() / atr)

    # Calculate ADX
    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()

    return adx, plus_di, minus_di


def calculate_parabolic_sar(df, acceleration=0.02, maximum=0.2):
    """Calculate Parabolic SAR"""
    sar = df['close'].copy()
    ep = df['high'].copy()
    af = acceleration
    trend = 1  # 1 for uptrend, -1 for downtrend

    sar_values = [df['close'].iloc[0]]

    for i in range(1, len(df)):
        if trend == 1:  # Uptrend
            sar_values.append(sar_values[-1] + af * (ep.iloc[i-1] - sar_values[-1]))
            if df['low'].iloc[i] < sar_values[-1]:
                trend = -1
                sar_values[-1] = ep.iloc[i-1]
                ep.iloc[i] = df['low'].iloc[i]
                af = acceleration
        else:  # Downtrend
            sar_values.append(sar_values[-1] - af * (sar_values[-1] - ep.iloc[i-1]))
            if df['high'].iloc[i] > sar_values[-1]:
                trend = 1
                sar_values[-1] = ep.iloc[i-1]
                ep.iloc[i] = df['high'].iloc[i]
                af = acceleration

    return pd.Series(sar_values, index=df.index)


def calculate_obv(df):
    """Calculate On-Balance Volume"""
    obv = [0]
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i-1]:
            obv.append(obv[-1] + df['volume'].iloc[i])
        elif df['close'].iloc[i] < df['close'].iloc[i-1]:
            obv.append(obv[-1] - df['volume'].iloc[i])
        else:
            obv.append(obv[-1])

    return pd.Series(obv, index=df.index)


def calculate_vwap(df):
    """Calculate Volume Weighted Average Price"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
    return vwap


def calculate_mfi(df, period=14):
    """Calculate Money Flow Index"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']

    positive_flow = []
    negative_flow = []

    for i in range(1, len(df)):
        if typical_price.iloc[i] > typical_price.iloc[i-1]:
            positive_flow.append(money_flow.iloc[i])
            negative_flow.append(0)
        elif typical_price.iloc[i] < typical_price.iloc[i-1]:
            positive_flow.append(0)
            negative_flow.append(money_flow.iloc[i])
        else:
            positive_flow.append(0)
            negative_flow.append(0)

    positive_flow = [0] + positive_flow
    negative_flow = [0] + negative_flow

    positive_mf = pd.Series(positive_flow).rolling(window=period).sum()
    negative_mf = pd.Series(negative_flow).rolling(window=period).sum()

    mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
    return mfi


def calculate_cmf(df, period=20):
    """Calculate Chaikin Money Flow"""
    mfm = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low'])
    mfv = mfm * df['volume']
    cmf = mfv.rolling(window=period).sum() / df['volume'].rolling(window=period).sum()
    return cmf


def calculate_ichimoku(df):
    """Calculate Ichimoku Cloud components"""
    # Conversion Line (Tenkan-sen): (9-period high + 9-period low)/2
    period9_high = df['high'].rolling(window=9).max()
    period9_low = df['low'].rolling(window=9).min()
    conversion_line = (period9_high + period9_low) / 2

    # Base Line (Kijun-sen): (26-period high + 26-period low)/2
    period26_high = df['high'].rolling(window=26).max()
    period26_low = df['low'].rolling(window=26).min()
    base_line = (period26_high + period26_low) / 2

    # Leading Span A (Senkou Span A): (Conversion Line + Base Line)/2
    leading_span_a = ((conversion_line + base_line) / 2).shift(26)

    # Leading Span B (Senkou Span B): (52-period high + 52-period low)/2
    period52_high = df['high'].rolling(window=52).max()
    period52_low = df['low'].rolling(window=52).min()
    leading_span_b = ((period52_high + period52_low) / 2).shift(26)

    return conversion_line, base_line, leading_span_a, leading_span_b


def calculate_fibonacci_levels(df, period=50):
    """Calculate Fibonacci Retracement levels"""
    high = df['high'].rolling(window=period).max()
    low = df['low'].rolling(window=period).min()
    diff = high - low

    levels = {
        'fib_0': high,
        'fib_236': high - 0.236 * diff,
        'fib_382': high - 0.382 * diff,
        'fib_500': high - 0.500 * diff,
        'fib_618': high - 0.618 * diff,
        'fib_786': high - 0.786 * diff,
        'fib_100': low
    }

    return levels


def calculate_all_indicators(df):
    """
    Calculate all technical indicators for a given DataFrame

    Args:
        df: DataFrame with OHLCV data

    Returns:
        Dictionary with all indicator values
    """
    if df is None or len(df) < 52:  # Need at least 52 periods for Ichimoku
        return None

    try:
        # Momentum indicators
        rsi = calculate_rsi(df)
        macd, macd_signal, macd_hist = calculate_macd(df)
        stoch_k, stoch_d = calculate_stochastic(df)
        roc = calculate_roc(df)
        williams_r = calculate_williams_r(df)

        # Trend indicators
        sma_20 = calculate_sma(df, 20)
        sma_50 = calculate_sma(df, 50)
        sma_200 = calculate_sma(df, 200)
        ema_12 = calculate_ema(df, 12)
        ema_26 = calculate_ema(df, 26)
        ema_50 = calculate_ema(df, 50)
        adx, plus_di, minus_di = calculate_adx(df)
        psar = calculate_parabolic_sar(df)
        supertrend, supertrend_direction = calculate_supertrend(df)

        # Volatility indicators
        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df)
        atr = calculate_atr(df)

        # Volume indicators
        obv = calculate_obv(df)
        vwap = calculate_vwap(df)
        mfi = calculate_mfi(df)
        cmf = calculate_cmf(df)

        # Ichimoku Cloud
        ich_conversion, ich_base, ich_span_a, ich_span_b = calculate_ichimoku(df)

        # Fibonacci levels
        fib_levels = calculate_fibonacci_levels(df)

        # Get latest values
        indicators = {
            # Price data
            'close': float(df['close'].iloc[-1]),
            'high': float(df['high'].iloc[-1]),
            'low': float(df['low'].iloc[-1]),
            'volume': float(df['volume'].iloc[-1]),

            # Momentum
            'rsi': float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
            'macd': float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else None,
            'macd_signal': float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else None,
            'macd_histogram': float(macd_hist.iloc[-1]) if not pd.isna(macd_hist.iloc[-1]) else None,
            'stoch_k': float(stoch_k.iloc[-1]) if not pd.isna(stoch_k.iloc[-1]) else None,
            'stoch_d': float(stoch_d.iloc[-1]) if not pd.isna(stoch_d.iloc[-1]) else None,
            'roc': float(roc.iloc[-1]) if not pd.isna(roc.iloc[-1]) else None,
            'williams_r': float(williams_r.iloc[-1]) if not pd.isna(williams_r.iloc[-1]) else None,

            # Trend
            'sma_20': float(sma_20.iloc[-1]) if not pd.isna(sma_20.iloc[-1]) else None,
            'sma_50': float(sma_50.iloc[-1]) if not pd.isna(sma_50.iloc[-1]) else None,
            'sma_200': float(sma_200.iloc[-1]) if not pd.isna(sma_200.iloc[-1]) else None,
            'ema_12': float(ema_12.iloc[-1]) if not pd.isna(ema_12.iloc[-1]) else None,
            'ema_26': float(ema_26.iloc[-1]) if not pd.isna(ema_26.iloc[-1]) else None,
            'ema_50': float(ema_50.iloc[-1]) if not pd.isna(ema_50.iloc[-1]) else None,
            'adx': float(adx.iloc[-1]) if not pd.isna(adx.iloc[-1]) else None,
            'plus_di': float(plus_di.iloc[-1]) if not pd.isna(plus_di.iloc[-1]) else None,
            'minus_di': float(minus_di.iloc[-1]) if not pd.isna(minus_di.iloc[-1]) else None,
            'psar': float(psar.iloc[-1]) if not pd.isna(psar.iloc[-1]) else None,
            'supertrend': float(supertrend.iloc[-1]) if not pd.isna(supertrend.iloc[-1]) else None,
            'supertrend_direction': float(supertrend_direction.iloc[-1]) if not pd.isna(supertrend_direction.iloc[-1]) else None,

            # Volatility
            'bb_upper': float(bb_upper.iloc[-1]) if not pd.isna(bb_upper.iloc[-1]) else None,
            'bb_middle': float(bb_middle.iloc[-1]) if not pd.isna(bb_middle.iloc[-1]) else None,
            'bb_lower': float(bb_lower.iloc[-1]) if not pd.isna(bb_lower.iloc[-1]) else None,
            'atr': float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else None,

            # Volume
            'obv': float(obv.iloc[-1]) if not pd.isna(obv.iloc[-1]) else None,
            'vwap': float(vwap.iloc[-1]) if not pd.isna(vwap.iloc[-1]) else None,
            'mfi': float(mfi.iloc[-1]) if not pd.isna(mfi.iloc[-1]) else None,
            'cmf': float(cmf.iloc[-1]) if not pd.isna(cmf.iloc[-1]) else None,

            # Ichimoku
            'ichimoku_conversion': float(ich_conversion.iloc[-1]) if not pd.isna(ich_conversion.iloc[-1]) else None,
            'ichimoku_base': float(ich_base.iloc[-1]) if not pd.isna(ich_base.iloc[-1]) else None,
            'ichimoku_span_a': float(ich_span_a.iloc[-1]) if not pd.isna(ich_span_a.iloc[-1]) else None,
            'ichimoku_span_b': float(ich_span_b.iloc[-1]) if not pd.isna(ich_span_b.iloc[-1]) else None,

            # Fibonacci
            'fib_0': float(fib_levels['fib_0'].iloc[-1]) if not pd.isna(fib_levels['fib_0'].iloc[-1]) else None,
            'fib_236': float(fib_levels['fib_236'].iloc[-1]) if not pd.isna(fib_levels['fib_236'].iloc[-1]) else None,
            'fib_382': float(fib_levels['fib_382'].iloc[-1]) if not pd.isna(fib_levels['fib_382'].iloc[-1]) else None,
            'fib_500': float(fib_levels['fib_500'].iloc[-1]) if not pd.isna(fib_levels['fib_500'].iloc[-1]) else None,
            'fib_618': float(fib_levels['fib_618'].iloc[-1]) if not pd.isna(fib_levels['fib_618'].iloc[-1]) else None,
            'fib_786': float(fib_levels['fib_786'].iloc[-1]) if not pd.isna(fib_levels['fib_786'].iloc[-1]) else None,
            'fib_100': float(fib_levels['fib_100'].iloc[-1]) if not pd.isna(fib_levels['fib_100'].iloc[-1]) else None,
        }

        return indicators

    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None
