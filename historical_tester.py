"""
Historical Data Testing Module
Tests the market analyzer with historical data and generates performance reports
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from market_analyzer import MarketAnalyzer
from data_fetcher import CRYPTO_PAIRS, FOREX_PAIRS, CRYPTO_NAMES, FOREX_NAMES
import json


class HistoricalTester:
    def __init__(self):
        self.analyzer = MarketAnalyzer()
        self.results = []

    def test_symbol_over_period(self, symbol, market_type, start_date, end_date, interval='1d'):
        """
        Test analysis on a symbol over a historical period

        Args:
            symbol: Trading symbol
            market_type: 'crypto' or 'forex'
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval (1d, 1h, etc.)

        Returns:
            List of test results with predictions and actual outcomes
        """
        print(f"\n{'='*60}")
        print(f"Testing {symbol} ({market_type})")
        print(f"Period: {start_date} to {end_date}")
        print(f"Interval: {interval}")
        print(f"{'='*60}\n")

        test_results = []

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
                return []

            print(f"SUCCESS: Downloaded {len(data)} data points")

            # Test at multiple points in time
            # Skip first 100 periods to have enough history for indicators
            test_points = range(100, len(data) - 10, 10)  # Test every 10th period

            for i, test_idx in enumerate(test_points):
                # Get data up to this point
                historical_data = data.iloc[:test_idx]

                # Get the analysis at this point
                analysis = self.analyzer.analyze_symbol(symbol, market_type, timeframe=interval, limit=100)

                if not analysis:
                    continue

                # Get actual future price movement (next 5 periods for ML comparison)
                future_idx = min(test_idx + 5, len(data) - 1)
                current_price = float(data.iloc[test_idx]['Close'])
                future_price = float(data.iloc[future_idx]['Close'])
                actual_return = ((future_price - current_price) / current_price) * 100

                # Determine actual direction
                if actual_return > 0.2:
                    actual_direction = 'BULLISH'
                elif actual_return < -0.2:
                    actual_direction = 'BEARISH'
                else:
                    actual_direction = 'NEUTRAL'

                # Get the prediction
                signal = analysis.get('signal', 'HOLD')
                strength = analysis.get('strength', 0)
                ml_prediction = analysis.get('ml_prediction')

                # Record result
                result = {
                    'date': str(data.index[test_idx])[:10],  # Get YYYY-MM-DD part
                    'symbol': symbol,
                    'market_type': market_type,
                    'current_price': current_price,
                    'future_price': future_price,
                    'actual_return': actual_return,
                    'actual_direction': actual_direction,
                    'signal': signal,
                    'signal_strength': float(strength),
                    'ml_prediction': ml_prediction.get('direction') if ml_prediction else None,
                    'ml_confidence': ml_prediction.get('confidence') if ml_prediction else None,
                }

                # Check if predictions were correct
                if signal in ['STRONG BUY', 'BUY']:
                    result['signal_correct'] = actual_direction == 'BULLISH'
                elif signal in ['STRONG SELL', 'SELL']:
                    result['signal_correct'] = actual_direction == 'BEARISH'
                else:
                    result['signal_correct'] = actual_direction == 'NEUTRAL'

                if ml_prediction:
                    result['ml_correct'] = ml_prediction.get('direction') == actual_direction
                else:
                    result['ml_correct'] = None

                test_results.append(result)

                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(test_points)} test points...")

            print(f"SUCCESS: Completed {len(test_results)} tests for {symbol}\n")

        except Exception as e:
            print(f"ERROR: Error testing {symbol}: {e}\n")

        return test_results

    def test_all_markets(self, start_date, end_date, interval='1d'):
        """
        Test all crypto and forex markets over a period

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval

        Returns:
            Complete test results for all markets
        """
        all_results = []

        print("\n" + "="*60)
        print("HISTORICAL TESTING - ALL MARKETS")
        print("="*60)

        # Test crypto markets
        print("\nTesting Cryptocurrency Markets...")
        for symbol in CRYPTO_PAIRS[:3]:  # Test first 3 for speed
            results = self.test_symbol_over_period(symbol, 'crypto', start_date, end_date, interval)
            all_results.extend(results)

        # Test forex markets
        print("\nTesting Forex Markets...")
        for symbol in FOREX_PAIRS[:3]:  # Test first 3 for speed
            results = self.test_symbol_over_period(symbol, 'forex', start_date, end_date, interval)
            all_results.extend(results)

        self.results = all_results
        return all_results

    def generate_report(self, results=None):
        """
        Generate a performance report from test results

        Args:
            results: List of test results (uses self.results if None)

        Returns:
            Dictionary with performance metrics
        """
        if results is None:
            results = self.results

        if not results:
            print("ERROR: No results to analyze")
            return None

        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(results)

        report = {
            'summary': {
                'total_tests': len(df),
                'date_range': f"{df['date'].min()} to {df['date'].max()}",
                'markets_tested': df['symbol'].nunique(),
            },
            'signal_accuracy': {},
            'ml_accuracy': {},
            'by_market_type': {},
            'by_symbol': {},
        }

        # Overall signal accuracy
        signal_correct = df['signal_correct'].sum()
        signal_total = len(df)
        report['signal_accuracy']['overall'] = {
            'correct': int(signal_correct),
            'total': int(signal_total),
            'accuracy': float(signal_correct / signal_total * 100) if signal_total > 0 else 0
        }

        # Signal accuracy by type
        for signal_type in ['STRONG BUY', 'BUY', 'HOLD', 'SELL', 'STRONG SELL']:
            signal_df = df[df['signal'] == signal_type]
            if len(signal_df) > 0:
                correct = signal_df['signal_correct'].sum()
                total = len(signal_df)
                report['signal_accuracy'][signal_type] = {
                    'correct': int(correct),
                    'total': int(total),
                    'accuracy': float(correct / total * 100)
                }

        # ML accuracy (forex only)
        ml_df = df[df['ml_correct'].notna()]
        if len(ml_df) > 0:
            ml_correct = ml_df['ml_correct'].sum()
            ml_total = len(ml_df)
            report['ml_accuracy']['overall'] = {
                'correct': int(ml_correct),
                'total': int(ml_total),
                'accuracy': float(ml_correct / ml_total * 100)
            }

            # ML accuracy by direction
            for direction in ['BULLISH', 'BEARISH', 'NEUTRAL']:
                dir_df = ml_df[ml_df['ml_prediction'] == direction]
                if len(dir_df) > 0:
                    correct = dir_df['ml_correct'].sum()
                    total = len(dir_df)
                    report['ml_accuracy'][direction] = {
                        'correct': int(correct),
                        'total': int(total),
                        'accuracy': float(correct / total * 100)
                    }

        # Performance by market type
        for market_type in ['crypto', 'forex']:
            market_df = df[df['market_type'] == market_type]
            if len(market_df) > 0:
                signal_correct = market_df['signal_correct'].sum()
                total = len(market_df)

                report['by_market_type'][market_type] = {
                    'signal_accuracy': float(signal_correct / total * 100),
                    'total_tests': int(total),
                    'avg_return': float(market_df['actual_return'].mean()),
                }

        # Performance by symbol
        for symbol in df['symbol'].unique():
            symbol_df = df[df['symbol'] == symbol]
            signal_correct = symbol_df['signal_correct'].sum()
            total = len(symbol_df)

            symbol_data = {
                'signal_accuracy': float(signal_correct / total * 100),
                'total_tests': int(total),
                'avg_return': float(symbol_df['actual_return'].mean()),
            }

            # Add ML accuracy if available
            symbol_ml_df = symbol_df[symbol_df['ml_correct'].notna()]
            if len(symbol_ml_df) > 0:
                ml_correct = symbol_ml_df['ml_correct'].sum()
                ml_total = len(symbol_ml_df)
                symbol_data['ml_accuracy'] = float(ml_correct / ml_total * 100)

            report['by_symbol'][symbol] = symbol_data

        return report

    def print_report(self, report):
        """
        Print a formatted report

        Args:
            report: Report dictionary from generate_report()
        """
        print("\n" + "="*60)
        print("HISTORICAL TESTING REPORT")
        print("="*60)

        # Summary
        print("\nSUMMARY")
        print("-" * 60)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Date Range: {report['summary']['date_range']}")
        print(f"Markets Tested: {report['summary']['markets_tested']}")

        # Overall Signal Accuracy
        print("\nSIGNAL ACCURACY")
        print("-" * 60)
        overall = report['signal_accuracy']['overall']
        print(f"Overall: {overall['correct']}/{overall['total']} ({overall['accuracy']:.2f}%)")

        print("\nBy Signal Type:")
        for signal_type in ['STRONG BUY', 'BUY', 'HOLD', 'SELL', 'STRONG SELL']:
            if signal_type in report['signal_accuracy']:
                data = report['signal_accuracy'][signal_type]
                print(f"  {signal_type:12s}: {data['correct']:3d}/{data['total']:3d} ({data['accuracy']:5.2f}%)")

        # ML Accuracy
        if report['ml_accuracy']:
            print("\nML PREDICTION ACCURACY (Forex Only)")
            print("-" * 60)
            if 'overall' in report['ml_accuracy']:
                ml_overall = report['ml_accuracy']['overall']
                print(f"Overall: {ml_overall['correct']}/{ml_overall['total']} ({ml_overall['accuracy']:.2f}%)")

                print("\nBy Direction:")
                for direction in ['BULLISH', 'BEARISH', 'NEUTRAL']:
                    if direction in report['ml_accuracy']:
                        data = report['ml_accuracy'][direction]
                        print(f"  {direction:8s}: {data['correct']:3d}/{data['total']:3d} ({data['accuracy']:5.2f}%)")

        # By Market Type
        print("\nPERFORMANCE BY MARKET TYPE")
        print("-" * 60)
        for market_type, data in report['by_market_type'].items():
            print(f"\n{market_type.upper()}:")
            print(f"  Signal Accuracy: {data['signal_accuracy']:.2f}%")
            print(f"  Total Tests: {data['total_tests']}")
            print(f"  Avg Return: {data['avg_return']:.2f}%")

        # By Symbol
        print("\nPERFORMANCE BY SYMBOL")
        print("-" * 60)
        for symbol, data in report['by_symbol'].items():
            print(f"\n{symbol}:")
            print(f"  Signal Accuracy: {data['signal_accuracy']:.2f}%")
            if 'ml_accuracy' in data:
                print(f"  ML Accuracy: {data['ml_accuracy']:.2f}%")
            print(f"  Total Tests: {data['total_tests']}")
            print(f"  Avg Return: {data['avg_return']:.2f}%")

        print("\n" + "="*60 + "\n")

    def save_results(self, filename='historical_test_results.json'):
        """
        Save test results to JSON file

        Args:
            filename: Output filename
        """
        if not self.results:
            print("ERROR: No results to save")
            return

        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"SUCCESS: Results saved to {filename}")

    def save_report(self, report, filename='historical_test_report.json'):
        """
        Save report to JSON file

        Args:
            report: Report dictionary
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"SUCCESS: Report saved to {filename}")


def quick_test():
    """
    Quick test with recent data (last 3 months)
    """
    tester = HistoricalTester()

    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Test
    print("\nQUICK TEST - Last 3 Months")
    results = tester.test_all_markets(
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        interval='1d'
    )

    # Generate and print report
    report = tester.generate_report(results)
    tester.print_report(report)

    # Save results
    tester.save_results('quick_test_results.json')
    tester.save_report(report, 'quick_test_report.json')

    return tester, report


def extended_test():
    """
    Extended test with more historical data (last 1 year)
    """
    tester = HistoricalTester()

    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Test ALL markets
    print("\nEXTENDED TEST - Last 1 Year - ALL MARKETS")

    all_results = []

    # Test all crypto
    print("\nTesting All Cryptocurrency Markets...")
    for symbol in CRYPTO_PAIRS:
        results = tester.test_symbol_over_period(
            symbol, 'crypto',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            interval='1d'
        )
        all_results.extend(results)

    # Test all forex
    print("\nTesting All Forex Markets...")
    for symbol in FOREX_PAIRS:
        results = tester.test_symbol_over_period(
            symbol, 'forex',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            interval='1d'
        )
        all_results.extend(results)

    tester.results = all_results

    # Generate and print report
    report = tester.generate_report(all_results)
    tester.print_report(report)

    # Save results
    tester.save_results('extended_test_results.json')
    tester.save_report(report, 'extended_test_report.json')

    return tester, report


def custom_test(symbol, market_type, start_date, end_date, interval='1d'):
    """
    Custom test for specific symbol and date range

    Args:
        symbol: Trading symbol
        market_type: 'crypto' or 'forex'
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        interval: Data interval
    """
    tester = HistoricalTester()

    print(f"\nCUSTOM TEST")
    results = tester.test_symbol_over_period(symbol, market_type, start_date, end_date, interval)

    # Generate and print report
    report = tester.generate_report(results)
    tester.print_report(report)

    # Save results
    filename = f"{symbol.replace('/', '_')}_test_results.json"
    tester.save_results(filename)
    tester.save_report(report, filename.replace('results', 'report'))

    return tester, report


if __name__ == '__main__':
    print("\n" + "="*60)
    print("HISTORICAL DATA TESTER")
    print("="*60)
    print("\nOptions:")
    print("1. Quick Test (Last 3 months, 3 crypto + 3 forex)")
    print("2. Extended Test (Last 1 year, ALL markets)")
    print("3. Custom Test (Specify symbol and dates)")
    print("\nRunning Quick Test by default...\n")

    # Run quick test by default
    tester, report = quick_test()

    print("\nTIP: To run other tests:")
    print("   Extended: python historical_tester.py extended")
    print("   Custom: Use custom_test() function in Python")
