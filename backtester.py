"""
Advanced Backtesting Module
Simulates actual trading with entry/exit points, stop loss, and take profit
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from market_analyzer import MarketAnalyzer
from data_fetcher import CRYPTO_PAIRS, FOREX_PAIRS, CRYPTO_NAMES, FOREX_NAMES
import json


class Backtester:
    def __init__(self, initial_capital=10000, risk_per_trade=0.01):
        """
        Initialize backtester

        Args:
            initial_capital: Starting capital
            risk_per_trade: Risk percentage per trade (0.01 = 1%)
        """
        self.analyzer = MarketAnalyzer()
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.trades = []
        self.equity_curve = []

    def backtest_symbol(self, symbol, market_type, start_date, end_date, interval='1d'):
        """
        Backtest trading strategy on a symbol

        Args:
            symbol: Trading symbol
            market_type: 'crypto' or 'forex'
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval

        Returns:
            List of trades executed
        """
        print(f"\n{'='*60}")
        print(f"Backtesting {symbol} ({market_type})")
        print(f"Period: {start_date} to {end_date}")
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"Risk per Trade: {self.risk_per_trade*100}%")
        print(f"{'='*60}\n")

        trades = []
        capital = self.initial_capital
        equity_history = [(start_date, capital)]

        try:
            # Fetch historical data
            import yfinance as yf

            # Convert symbol for yfinance
            if market_type == 'crypto':
                yf_symbol = symbol.replace('/', '-')
            else:
                yf_symbol = symbol

            # Download data
            data = yf.download(yf_symbol, start=start_date, end=end_date, interval=interval, progress=False)

            if data.empty:
                print(f"ERROR: No data available for {symbol}")
                return [], []

            print(f"SUCCESS: Downloaded {len(data)} data points")

            # Variables to track active trade
            active_trade = None

            # Determine starting point based on interval
            # Need enough history for indicators
            if interval == '1wk':
                start_idx = 20  # 20 weeks (~5 months) for weekly
            elif interval == '1d':
                start_idx = 100  # 100 days for daily
            else:
                start_idx = 200  # 200 periods for intraday

            # Iterate through data
            for i in range(start_idx, len(data)):
                current_date = data.index[i].strftime('%Y-%m-%d')
                current_price = float(data.iloc[i]['Close'])
                high_price = float(data.iloc[i]['High'])
                low_price = float(data.iloc[i]['Low'])

                # Check if we have an active trade
                if active_trade:
                    direction = active_trade.get('direction', 'LONG')

                    # Check stop loss and take profit based on direction
                    if direction == 'LONG':
                        # Long position: stop loss below, take profit above
                        if low_price <= active_trade['stop_loss']:
                            # Stop loss hit
                            exit_price = active_trade['stop_loss']
                            # PnL = position_size * (price_change / entry_price)
                            price_change_pct = (exit_price - active_trade['entry_price']) / active_trade['entry_price']
                            pnl = active_trade['position_size'] * price_change_pct
                            capital += pnl

                            active_trade['exit_date'] = current_date
                            active_trade['exit_price'] = exit_price
                            active_trade['exit_reason'] = 'STOP_LOSS'
                            active_trade['pnl'] = pnl
                            active_trade['pnl_percent'] = (pnl / capital) * 100
                            active_trade['final_capital'] = capital

                            trades.append(active_trade)
                            equity_history.append((current_date, capital))
                            active_trade = None
                            continue

                        # Check take profit
                        if high_price >= active_trade['take_profit']:
                            # Take profit hit
                            exit_price = active_trade['take_profit']
                            price_change_pct = (exit_price - active_trade['entry_price']) / active_trade['entry_price']
                            pnl = active_trade['position_size'] * price_change_pct
                            capital += pnl

                            active_trade['exit_date'] = current_date
                            active_trade['exit_price'] = exit_price
                            active_trade['exit_reason'] = 'TAKE_PROFIT'
                            active_trade['pnl'] = pnl
                            active_trade['pnl_percent'] = (pnl / capital) * 100
                            active_trade['final_capital'] = capital

                            trades.append(active_trade)
                            equity_history.append((current_date, capital))
                            active_trade = None
                            continue

                    else:  # SHORT position
                        # Short position: stop loss above, take profit below
                        if high_price >= active_trade['stop_loss']:
                            # Stop loss hit (price went up)
                            exit_price = active_trade['stop_loss']
                            price_change_pct = (active_trade['entry_price'] - exit_price) / active_trade['entry_price']
                            pnl = active_trade['position_size'] * price_change_pct
                            capital += pnl

                            active_trade['exit_date'] = current_date
                            active_trade['exit_price'] = exit_price
                            active_trade['exit_reason'] = 'STOP_LOSS'
                            active_trade['pnl'] = pnl
                            active_trade['pnl_percent'] = (pnl / capital) * 100
                            active_trade['final_capital'] = capital

                            trades.append(active_trade)
                            equity_history.append((current_date, capital))
                            active_trade = None
                            continue

                        # Check take profit (price went down)
                        if low_price <= active_trade['take_profit']:
                            # Take profit hit
                            exit_price = active_trade['take_profit']
                            price_change_pct = (active_trade['entry_price'] - exit_price) / active_trade['entry_price']
                            pnl = active_trade['position_size'] * price_change_pct
                            capital += pnl

                            active_trade['exit_date'] = current_date
                            active_trade['exit_price'] = exit_price
                            active_trade['exit_reason'] = 'TAKE_PROFIT'
                            active_trade['pnl'] = pnl
                            active_trade['pnl_percent'] = (pnl / capital) * 100
                            active_trade['final_capital'] = capital

                            trades.append(active_trade)
                            equity_history.append((current_date, capital))
                            active_trade = None
                            continue

                # If no active trade, look for entry signals
                if not active_trade:
                    # Get analysis at this point
                    analysis = self.analyzer.analyze_symbol(symbol, market_type, timeframe=interval, limit=100)

                    if not analysis:
                        continue

                    signal = analysis.get('signal', 'HOLD')
                    strength = analysis.get('strength', 0)

                    # Determine thresholds based on interval
                    if interval in ['1d', '1wk']:
                        # Relaxed conditions for daily/weekly intervals
                        if interval == '1wk':
                            # Even more relaxed for weekly (more trade opportunities)
                            signal_threshold = 15
                            ml_threshold = 50
                        else:  # 1d
                            signal_threshold = 20
                            ml_threshold = 55
                        require_patterns = False  # Optional instead of required
                    else:
                        # Stricter conditions for intraday (4h, 1h, etc.)
                        signal_threshold = 50
                        ml_threshold = 75
                        require_patterns = True

                    # Scoring system: need 2 of 3 conditions
                    score = 0
                    trade_direction = None

                    # Condition 1: Signal strength
                    signal_valid = False
                    if signal in ['STRONG BUY', 'BUY'] and strength >= signal_threshold:
                        score += 1
                        signal_valid = True
                        trade_direction = 'LONG'
                    elif signal in ['STRONG SELL', 'SELL'] and strength >= signal_threshold:
                        score += 1
                        signal_valid = True
                        trade_direction = 'SHORT'

                    # Condition 2: Candlestick patterns (if required or if found)
                    has_patterns = bool(analysis.get('patterns_5m') or analysis.get('patterns_4h'))
                    if has_patterns or not require_patterns:
                        if has_patterns:
                            score += 1

                    # Condition 3: ML prediction (for forex)
                    ml_valid = False
                    if market_type == 'forex' and analysis.get('ml_prediction'):
                        ml_pred = analysis['ml_prediction']
                        if ml_pred['direction'] == 'BULLISH' and ml_pred['confidence'] >= ml_threshold:
                            score += 1
                            ml_valid = True
                            if not trade_direction:
                                trade_direction = 'LONG'
                        elif ml_pred['direction'] == 'BEARISH' and ml_pred['confidence'] >= ml_threshold:
                            score += 1
                            ml_valid = True
                            if not trade_direction:
                                trade_direction = 'SHORT'

                    # Enter trade if score >= 2 (at least 2 conditions met)
                    entry_conditions = score >= 2 and trade_direction is not None

                    # Enter trade if conditions met
                    if entry_conditions:
                        # Get entry/exit recommendations
                        patterns_4h = analysis.get('patterns_4h', [])
                        entry_exit = patterns_4h[0].get('entry_exit') if patterns_4h else None

                        entry_price = current_price

                        # Set stop loss and take profit based on direction and available data
                        if entry_exit:
                            stop_loss = entry_exit.get('stop_loss', entry_price * 0.97)
                            take_profit = entry_exit.get('take_profit', entry_price * 1.06)
                        else:
                            # Default risk/reward for daily intervals without patterns
                            if trade_direction == 'LONG':
                                stop_loss = entry_price * 0.97   # 3% stop loss
                                take_profit = entry_price * 1.06  # 6% take profit (1:2 risk/reward)
                            else:  # SHORT
                                stop_loss = entry_price * 1.03   # 3% stop loss (price goes up)
                                take_profit = entry_price * 0.94  # 6% take profit (price goes down)

                        # Calculate position size based on risk
                        risk_amount = capital * self.risk_per_trade
                        price_risk = abs(entry_price - stop_loss)
                        position_size = risk_amount / price_risk if price_risk > 0 else capital * 0.10

                        # Don't risk more than 10% of capital per trade
                        position_size = min(position_size, capital * 0.10)

                        active_trade = {
                            'symbol': symbol,
                            'market_type': market_type,
                            'entry_date': current_date,
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'direction': trade_direction,
                            'signal': signal,
                            'signal_strength': strength,
                            'ml_prediction': analysis.get('ml_prediction', {}).get('direction'),
                            'ml_confidence': analysis.get('ml_prediction', {}).get('confidence'),
                            'position_size': position_size,
                            'risk_amount': risk_amount,
                            'capital_at_entry': capital,
                            'score': score,  # Track entry score
                        }

                # Progress
                if i % 50 == 0:
                    progress = (i / len(data)) * 100
                    print(f"Progress: {progress:.1f}% | Trades: {len(trades)} | Capital: ${capital:,.2f}")

            # Close any remaining open trade
            if active_trade:
                exit_price = float(data.iloc[-1]['Close'])
                direction = active_trade.get('direction', 'LONG')

                # Calculate PnL based on direction
                if direction == 'LONG':
                    price_change_pct = (exit_price - active_trade['entry_price']) / active_trade['entry_price']
                    pnl = active_trade['position_size'] * price_change_pct
                else:  # SHORT
                    price_change_pct = (active_trade['entry_price'] - exit_price) / active_trade['entry_price']
                    pnl = active_trade['position_size'] * price_change_pct

                capital += pnl

                active_trade['exit_date'] = data.index[-1].strftime('%Y-%m-%d')
                active_trade['exit_price'] = exit_price
                active_trade['exit_reason'] = 'END_OF_PERIOD'
                active_trade['pnl'] = pnl
                active_trade['pnl_percent'] = (pnl / capital) * 100
                active_trade['final_capital'] = capital

                trades.append(active_trade)
                equity_history.append((data.index[-1].strftime('%Y-%m-%d'), capital))

            print(f"\nSUCCESS: Backtest complete!")
            print(f"Total Trades: {len(trades)}")
            print(f"Final Capital: ${capital:,.2f}")
            print(f"Total Return: {((capital - self.initial_capital) / self.initial_capital * 100):.2f}%\n")

        except Exception as e:
            print(f"ERROR: Error backtesting {symbol}: {e}\n")

        return trades, equity_history

    def analyze_results(self, trades, equity_history):
        """
        Analyze backtest results and calculate metrics

        Args:
            trades: List of executed trades
            equity_history: List of (date, capital) tuples

        Returns:
            Dictionary with performance metrics
        """
        if not trades:
            return {
                'error': 'No trades executed',
                'initial_capital': self.initial_capital,
                'final_capital': self.initial_capital,
                'total_return': 0.0,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_profit': 0.0,
                'total_loss': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': None,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'by_exit_reason': {},
            }

        df = pd.DataFrame(trades)

        # Calculate metrics
        winning_trades = df[df['pnl'] > 0]
        losing_trades = df[df['pnl'] < 0]

        total_trades = len(df)
        winning_count = len(winning_trades)
        losing_count = len(losing_trades)

        win_rate = (winning_count / total_trades * 100) if total_trades > 0 else 0

        total_profit = winning_trades['pnl'].sum() if winning_count > 0 else 0
        total_loss = abs(losing_trades['pnl'].sum()) if losing_count > 0 else 0

        avg_win = winning_trades['pnl'].mean() if winning_count > 0 else 0
        avg_loss = abs(losing_trades['pnl'].mean()) if losing_count > 0 else 0

        profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')

        # Calculate equity curve metrics
        equity_df = pd.DataFrame(equity_history, columns=['date', 'capital'])
        returns = equity_df['capital'].pct_change().dropna()

        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if len(returns) > 1 and returns.std() > 0 else 0

        # Max drawdown
        cumulative = equity_df['capital']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = abs(drawdown.min()) * 100 if len(drawdown) > 0 else 0

        # Final metrics
        final_capital = equity_df.iloc[-1]['capital']
        total_return = ((final_capital - self.initial_capital) / self.initial_capital * 100)

        metrics = {
            'initial_capital': self.initial_capital,
            'final_capital': float(final_capital),
            'total_return': float(total_return),
            'total_trades': int(total_trades),
            'winning_trades': int(winning_count),
            'losing_trades': int(losing_count),
            'win_rate': float(win_rate),
            'total_profit': float(total_profit),
            'total_loss': float(total_loss),
            'avg_win': float(avg_win),
            'avg_loss': float(avg_loss),
            'profit_factor': float(profit_factor) if profit_factor != float('inf') else None,
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown': float(max_drawdown),
        }

        # Breakdown by exit reason
        metrics['by_exit_reason'] = {}
        for reason in df['exit_reason'].unique():
            reason_df = df[df['exit_reason'] == reason]
            metrics['by_exit_reason'][reason] = {
                'count': int(len(reason_df)),
                'avg_pnl': float(reason_df['pnl'].mean()),
            }

        return metrics

    def print_results(self, metrics, trades):
        """
        Print formatted backtest results

        Args:
            metrics: Metrics dictionary from analyze_results()
            trades: List of trades
        """
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)

        # Overall Performance
        print("\nOVERALL PERFORMANCE")
        print("-" * 60)
        print(f"Initial Capital:  ${metrics['initial_capital']:,.2f}")
        print(f"Final Capital:    ${metrics['final_capital']:,.2f}")
        print(f"Total Return:     {metrics['total_return']:+.2f}%")
        print(f"Max Drawdown:     {metrics['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio:     {metrics['sharpe_ratio']:.2f}")

        # Trade Statistics
        print("\nTRADE STATISTICS")
        print("-" * 60)
        print(f"Total Trades:     {metrics['total_trades']}")
        print(f"Winning Trades:   {metrics['winning_trades']} ({metrics['win_rate']:.2f}%)")
        print(f"Losing Trades:    {metrics['losing_trades']}")

        # Profit/Loss
        print("\nPROFIT/LOSS BREAKDOWN")
        print("-" * 60)
        print(f"Total Profit:     ${metrics['total_profit']:,.2f}")
        print(f"Total Loss:       ${metrics['total_loss']:,.2f}")
        print(f"Average Win:      ${metrics['avg_win']:,.2f}")
        print(f"Average Loss:     ${metrics['avg_loss']:,.2f}")
        if metrics['profit_factor']:
            print(f"Profit Factor:    {metrics['profit_factor']:.2f}")
        else:
            print(f"Profit Factor:    Infinity (no losses)")

        # Exit Reasons
        print("\nEXIT REASONS")
        print("-" * 60)
        for reason, data in metrics['by_exit_reason'].items():
            print(f"{reason:15s}: {data['count']:3d} trades (Avg P/L: ${data['avg_pnl']:+,.2f})")

        # Recent Trades (last 10)
        if trades:
            print("\nRECENT TRADES (Last 10)")
            print("-" * 60)
            recent = trades[-10:]
            for i, trade in enumerate(recent, 1):
                pnl_str = f"${trade['pnl']:+,.2f}" if trade['pnl'] else "Open"
                print(f"{i:2d}. {trade['entry_date']} | {trade['signal']:12s} | {trade['exit_reason']:12s} | {pnl_str}")

        print("\n" + "="*60 + "\n")

    def save_results(self, trades, metrics, filename='backtest_results.json'):
        """
        Save backtest results to JSON

        Args:
            trades: List of trades
            metrics: Metrics dictionary
            filename: Output filename
        """
        results = {
            'metrics': metrics,
            'trades': trades,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"SUCCESS: Results saved to {filename}")


def run_backtest(symbol='BTC/USDT', market_type='crypto', days=90, initial_capital=10000, risk_per_trade=0.01):
    """
    Run a backtest on a single symbol

    Args:
        symbol: Trading symbol
        market_type: 'crypto' or 'forex'
        days: Number of days to backtest
        initial_capital: Starting capital
        risk_per_trade: Risk percentage per trade

    Returns:
        Backtester instance with results
    """
    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Create backtester
    backtester = Backtester(initial_capital=initial_capital, risk_per_trade=risk_per_trade)

    # Run backtest
    trades, equity_history = backtester.backtest_symbol(
        symbol=symbol,
        market_type=market_type,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        interval='1d'
    )

    # Analyze results
    metrics = backtester.analyze_results(trades, equity_history)

    # Print results
    backtester.print_results(metrics, trades)

    # Save results
    filename = f"backtest_{symbol.replace('/', '_')}_{days}days.json"
    backtester.save_results(trades, metrics, filename)

    return backtester, trades, metrics


if __name__ == '__main__':
    print("\n" + "="*60)
    print("BACKTESTING MODULE")
    print("="*60)
    print("\nRunning default backtest: BTC/USDT - Last 90 days\n")

    # Run default backtest
    backtester, trades, metrics = run_backtest(
        symbol='BTC/USDT',
        market_type='crypto',
        days=90,
        initial_capital=10000,
        risk_per_trade=0.01
    )

    print("\n💡 To run custom backtests:")
    print("   run_backtest('EURUSD=X', 'forex', days=180, initial_capital=50000)")
