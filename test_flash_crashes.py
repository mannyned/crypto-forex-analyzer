"""
Flash Crash Historical Testing
Tests the analyzer's performance during major market crashes and extreme volatility events
"""
from historical_tester import HistoricalTester, custom_test
from backtester import Backtester, run_backtest
import json
from datetime import datetime


class FlashCrashTester:
    """Test analyzer performance during major market crashes"""

    def __init__(self):
        self.events = {
            'swiss_franc_2015': {
                'name': '2015 Swiss Franc Flash Crash',
                'symbol': 'CHFUSD=X',  # Or EURCHF=X
                'market_type': 'forex',
                'start_date': '2014-12-01',
                'end_date': '2015-03-01',
                'crash_date': '2015-01-15',
                'description': 'Swiss National Bank removed EUR/CHF floor, causing 30%+ move in minutes'
            },
            'brexit_2016': {
                'name': '2016 Brexit Vote',
                'symbol': 'GBPUSD=X',
                'market_type': 'forex',
                'start_date': '2016-05-01',
                'end_date': '2016-08-01',
                'crash_date': '2016-06-24',
                'description': 'GBP crashed 10%+ overnight after Brexit referendum'
            },
            'covid_march_2020': {
                'name': '2020 COVID-19 Market Crash',
                'symbol': 'EURUSD=X',
                'market_type': 'forex',
                'start_date': '2020-02-01',
                'end_date': '2020-05-01',
                'crash_date': '2020-03-12',
                'description': 'Global market crash, extreme volatility across all markets'
            },
            'crypto_crash_2022': {
                'name': '2022 Crypto Winter / Luna Collapse',
                'symbol': 'BTC-USD',  # Bitcoin
                'market_type': 'crypto',
                'start_date': '2022-04-01',
                'end_date': '2022-07-01',
                'crash_date': '2022-05-09',
                'description': 'Terra Luna collapse triggered crypto market crash, BTC down 50%+'
            },
            'ftx_collapse_2022': {
                'name': '2022 FTX Collapse',
                'symbol': 'BTC-USD',
                'market_type': 'crypto',
                'start_date': '2022-10-01',
                'end_date': '2023-01-01',
                'crash_date': '2022-11-08',
                'description': 'FTX exchange collapse, Bitcoin dropped 25% in days'
            },
        }

        self.results = {}

    def test_event(self, event_key):
        """Test a specific flash crash event"""
        event = self.events[event_key]

        print("\n" + "="*70)
        print(f"TESTING: {event['name']}")
        print("="*70)
        print(f"Symbol: {event['symbol']}")
        print(f"Period: {event['start_date']} to {event['end_date']}")
        print(f"Crash Date: {event['crash_date']}")
        print(f"Description: {event['description']}")
        print("="*70 + "\n")

        # Run historical accuracy test
        print("1. Running Historical Accuracy Test...")
        print("-" * 70)

        tester = HistoricalTester()
        test_results = tester.test_symbol_over_period(
            symbol=event['symbol'],
            market_type=event['market_type'],
            start_date=event['start_date'],
            end_date=event['end_date'],
            interval='1d'
        )

        if test_results:
            report = tester.generate_report(test_results)
            tester.print_report(report)

            # Save results
            filename = f"{event_key}_historical_test.json"
            tester.results = test_results
            tester.save_results(filename)
            tester.save_report(report, filename.replace('test', 'report'))

        # Run backtest simulation
        print("\n2. Running Backtest Simulation...")
        print("-" * 70)

        backtester = Backtester(initial_capital=10000, risk_per_trade=0.01)
        trades, equity = backtester.backtest_symbol(
            symbol=event['symbol'],
            market_type=event['market_type'],
            start_date=event['start_date'],
            end_date=event['end_date'],
            interval='1d'
        )

        if trades or equity:
            metrics = backtester.analyze_results(trades, equity)
            backtester.print_results(metrics, trades)

            # Save backtest results
            bt_filename = f"{event_key}_backtest.json"
            backtester.save_results(trades, metrics, bt_filename)

            self.results[event_key] = {
                'historical_test': report if test_results else None,
                'backtest': metrics,
                'trades': len(trades),
                'event_info': event
            }

        return self.results.get(event_key)

    def test_all_events(self):
        """Test all flash crash events"""
        print("\n" + "="*70)
        print("FLASH CRASH HISTORICAL TESTING SUITE")
        print("="*70)
        print(f"Testing {len(self.events)} major market crash events")
        print("="*70 + "\n")

        for event_key in self.events.keys():
            try:
                self.test_event(event_key)
            except Exception as e:
                print(f"ERROR testing {event_key}: {e}\n")
                continue

        # Generate comparison report
        self.generate_comparison_report()

    def generate_comparison_report(self):
        """Generate comparison report across all events"""
        print("\n" + "="*70)
        print("FLASH CRASH COMPARISON REPORT")
        print("="*70 + "\n")

        if not self.results:
            print("No results to compare")
            return

        print(f"{'Event':<30} | {'Trades':<7} | {'Return':<10} | {'Win Rate':<10} | {'Max DD':<10}")
        print("-" * 70)

        for event_key, data in self.results.items():
            if data and data.get('backtest'):
                bt = data['backtest']
                event_name = self.events[event_key]['name'][:28]

                print(f"{event_name:<30} | "
                      f"{bt.get('total_trades', 0):<7} | "
                      f"{bt.get('total_return', 0):>+9.2f}% | "
                      f"{bt.get('win_rate', 0):>9.2f}% | "
                      f"{bt.get('max_drawdown', 0):>9.2f}%")

        print("\n" + "="*70)

        # Save comparison
        with open('flash_crash_comparison.json', 'w') as f:
            json.dump({
                'test_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'events_tested': list(self.results.keys()),
                'results': self.results
            }, f, indent=2, default=str)

        print("\nSUCCESS: Comparison saved to flash_crash_comparison.json")


def test_swiss_franc_2015():
    """Test 2015 Swiss Franc crash specifically"""
    tester = FlashCrashTester()
    result = tester.test_event('swiss_franc_2015')
    return result


def test_brexit_2016():
    """Test 2016 Brexit crash specifically"""
    tester = FlashCrashTester()
    result = tester.test_event('brexit_2016')
    return result


def test_covid_2020():
    """Test 2020 COVID crash"""
    tester = FlashCrashTester()
    result = tester.test_event('covid_march_2020')
    return result


def test_all_crashes():
    """Test all major crashes"""
    tester = FlashCrashTester()
    tester.test_all_events()
    return tester.results


if __name__ == '__main__':
    print("""
======================================================================
         FLASH CRASH & EXTREME VOLATILITY TESTING
======================================================================

This module tests the analyzer's performance during major market crashes:

1. 2015 Swiss Franc Flash Crash (30%+ move in minutes)
2. 2016 Brexit Vote (GBP crashed 10%+ overnight)
3. 2020 COVID-19 Market Crash (Global market meltdown)
4. 2022 Crypto Winter / Luna Collapse (BTC down 50%+)
5. 2022 FTX Collapse (Bitcoin dropped 25%)

Testing will show:
- Signal accuracy during extreme volatility
- ML prediction performance in crashes
- Backtest results (would you have survived?)
- Entry/exit behavior during panic selling
- Maximum drawdown during crashes

WARNING: These tests may take several minutes to complete.
Each event downloads historical data and runs full analysis.

""")

    print("Options:")
    print("1. Test Swiss Franc 2015 only")
    print("2. Test Brexit 2016 only")
    print("3. Test COVID-19 2020 only")
    print("4. Test ALL events (recommended)")
    print()

    choice = input("Enter choice (1-4) or press Enter for option 4: ").strip()

    if choice == '1':
        print("\nTesting Swiss Franc 2015 crash...\n")
        test_swiss_franc_2015()
    elif choice == '2':
        print("\nTesting Brexit 2016 crash...\n")
        test_brexit_2016()
    elif choice == '3':
        print("\nTesting COVID-19 2020 crash...\n")
        test_covid_2020()
    else:
        print("\nTesting ALL crash events...\n")
        test_all_crashes()

    print("\n" + "="*70)
    print("TESTING COMPLETE!")
    print("="*70)
    print("\nCheck the generated JSON files for detailed results:")
    print("  - *_historical_test.json - Accuracy test results")
    print("  - *_backtest.json - Trading simulation results")
    print("  - flash_crash_comparison.json - Comparison across all events")
