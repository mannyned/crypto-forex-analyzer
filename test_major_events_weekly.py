"""
Test major forex events with WEEKLY intervals for higher trade frequency
"""
from historical_tester import HistoricalTester
from backtester import Backtester
import json


def test_swiss_franc_2015_weekly():
    """
    2015 Swiss Franc Flash Crash - WEEKLY INTERVAL
    """
    print("\n" + "="*70)
    print("2015 SWISS FRANC FLASH CRASH TEST (WEEKLY)")
    print("="*70)
    print("Event: SNB removed EUR/CHF 1.20 floor")
    print("Date: January 15, 2015")
    print("Impact: CHF surged 30%+ vs EUR in minutes")
    print("Testing period: 3 years (2013-2015) - Extended for weekly data")
    print("Interval: WEEKLY (1wk) - More trade opportunities")
    print("="*70 + "\n")

    # Extended period for enough data
    tester = HistoricalTester()

    print("Running Historical Test on EUR/CHF...")
    results = tester.test_symbol_over_period(
        symbol='EURCHF=X',
        market_type='forex',
        start_date='2013-01-01',  # Extended: 2+ years for weekly data
        end_date='2015-12-31',
        interval='1wk'  # WEEKLY
    )

    if results:
        report = tester.generate_report(results)
        tester.print_report(report)
        tester.results = results
        tester.save_results('swiss_franc_2015_weekly_test.json')
        tester.save_report(report, 'swiss_franc_2015_weekly_report.json')

    # Backtest
    print("\nRunning Backtest Simulation (WEEKLY)...")
    backtester = Backtester(initial_capital=10000, risk_per_trade=0.01)
    trades, equity = backtester.backtest_symbol(
        symbol='EURCHF=X',
        market_type='forex',
        start_date='2013-01-01',  # Extended: 2+ years
        end_date='2015-12-31',
        interval='1wk'  # WEEKLY
    )

    metrics = backtester.analyze_results(trades, equity)
    backtester.print_results(metrics, trades)
    backtester.save_results(trades, metrics, 'swiss_franc_2015_weekly_backtest.json')

    return {'test': report, 'backtest': metrics, 'trades': trades}


def test_brexit_2016_weekly():
    """
    2016 Brexit Vote - WEEKLY INTERVAL
    """
    print("\n" + "="*70)
    print("2016 BREXIT FLASH CRASH TEST (WEEKLY)")
    print("="*70)
    print("Event: UK voted to leave European Union")
    print("Date: June 24, 2016")
    print("Impact: GBP crashed 10%+ overnight, continued falling")
    print("Testing period: 6 months (3 months before + 3 months after)")
    print("Interval: WEEKLY (1wk) - More trade opportunities")
    print("="*70 + "\n")

    tester = HistoricalTester()

    print("Running Historical Test on GBP/USD...")
    results = tester.test_symbol_over_period(
        symbol='GBPUSD=X',
        market_type='forex',
        start_date='2015-01-01',  # Extended: 2+ years
        end_date='2017-12-31',
        interval='1wk'  # WEEKLY
    )

    if results:
        report = tester.generate_report(results)
        tester.print_report(report)
        tester.results = results
        tester.save_results('brexit_2016_weekly_test.json')
        tester.save_report(report, 'brexit_2016_weekly_report.json')

    # Backtest
    print("\nRunning Backtest Simulation (WEEKLY)...")
    backtester = Backtester(initial_capital=10000, risk_per_trade=0.01)
    trades, equity = backtester.backtest_symbol(
        symbol='GBPUSD=X',
        market_type='forex',
        start_date='2015-01-01',  # Extended: 2+ years
        end_date='2017-12-31',
        interval='1wk'  # WEEKLY
    )

    metrics = backtester.analyze_results(trades, equity)
    backtester.print_results(metrics, trades)
    backtester.save_results(trades, metrics, 'brexit_2016_weekly_backtest.json')

    return {'test': report, 'backtest': metrics, 'trades': trades}


def test_covid_crash_2020_weekly():
    """
    2020 COVID-19 Market Crash - WEEKLY INTERVAL
    """
    print("\n" + "="*70)
    print("2020 COVID-19 MARKET CRASH TEST (WEEKLY)")
    print("="*70)
    print("Event: Global pandemic triggered market crash")
    print("Date: March 2020")
    print("Impact: Extreme volatility across all markets")
    print("Testing period: 6 months (Jan - July 2020)")
    print("Interval: WEEKLY (1wk) - More trade opportunities")
    print("="*70 + "\n")

    tester = HistoricalTester()

    print("Running Historical Test on EUR/USD...")
    results = tester.test_symbol_over_period(
        symbol='EURUSD=X',
        market_type='forex',
        start_date='2019-01-01',  # Extended: 2+ years
        end_date='2021-12-31',
        interval='1wk'  # WEEKLY
    )

    if results:
        report = tester.generate_report(results)
        tester.print_report(report)
        tester.results = results
        tester.save_results('covid_2020_weekly_test.json')
        tester.save_report(report, 'covid_2020_weekly_report.json')

    # Backtest
    print("\nRunning Backtest Simulation (WEEKLY)...")
    backtester = Backtester(initial_capital=10000, risk_per_trade=0.01)
    trades, equity = backtester.backtest_symbol(
        symbol='EURUSD=X',
        market_type='forex',
        start_date='2019-01-01',  # Extended: 2+ years
        end_date='2021-12-31',
        interval='1wk'  # WEEKLY
    )

    metrics = backtester.analyze_results(trades, equity)
    backtester.print_results(metrics, trades)
    backtester.save_results(trades, metrics, 'covid_2020_weekly_backtest.json')

    return {'test': report, 'backtest': metrics, 'trades': trades}


def compare_all_events_weekly():
    """Run all tests with WEEKLY intervals and compare results"""
    print("\n" + "="*70)
    print("MAJOR FOREX EVENTS COMPARISON TEST (WEEKLY INTERVALS)")
    print("="*70)
    print("Testing 3 major forex market events with WEEKLY data:")
    print("1. 2015 Swiss Franc Flash Crash")
    print("2. 2016 Brexit Vote")
    print("3. 2020 COVID-19 Crash")
    print("\nWeekly intervals provide:")
    print("  - More trading opportunities")
    print("  - Lower signal thresholds (15% vs 20%)")
    print("  - Lower ML confidence required (50% vs 55%)")
    print("="*70 + "\n")

    results = {}

    # Test all events
    print("\nTEST 1/3: Swiss Franc 2015 (WEEKLY)")
    print("-" * 70)
    try:
        results['swiss_franc_2015'] = test_swiss_franc_2015_weekly()
    except Exception as e:
        print(f"ERROR in Swiss Franc test: {e}")
        results['swiss_franc_2015'] = None

    print("\n\nTEST 2/3: Brexit 2016 (WEEKLY)")
    print("-" * 70)
    try:
        results['brexit_2016'] = test_brexit_2016_weekly()
    except Exception as e:
        print(f"ERROR in Brexit test: {e}")
        results['brexit_2016'] = None

    print("\n\nTEST 3/3: COVID-19 2020 (WEEKLY)")
    print("-" * 70)
    try:
        results['covid_2020'] = test_covid_crash_2020_weekly()
    except Exception as e:
        print(f"ERROR in COVID test: {e}")
        results['covid_2020'] = None

    # Generate comparison
    print("\n\n" + "="*70)
    print("WEEKLY INTERVALS - COMPARISON SUMMARY")
    print("="*70 + "\n")

    print(f"{'Event':<25} | {'Signal Acc':<12} | {'ML Acc':<12} | {'Trades':<8} | {'Return':<10} | {'Max DD':<10}")
    print("-" * 70)

    for event_name, data in results.items():
        if data and data.get('test') and data.get('backtest'):
            test_report = data['test']
            backtest = data['backtest']

            signal_acc = test_report.get('signal_accuracy', {}).get('overall', {}).get('accuracy', 0)
            ml_acc = test_report.get('ml_accuracy', {}).get('overall', {}).get('accuracy', 0) if test_report.get('ml_accuracy') else 0
            trades_count = backtest.get('total_trades', 0)
            total_return = backtest.get('total_return', 0)
            max_dd = backtest.get('max_drawdown', 0)

            print(f"{event_name:<25} | {signal_acc:>11.2f}% | {ml_acc:>11.2f}% | {trades_count:>8} | {total_return:>+9.2f}% | {max_dd:>9.2f}%")

    print("\n" + "="*70)

    # Save comparison
    with open('major_events_weekly_comparison.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("\nSUCCESS: All results saved to major_events_weekly_comparison.json")
    print("\nKey Differences from Daily Intervals:")
    print("- Signal Threshold: 15% (vs 20% daily)")
    print("- ML Threshold: 50% (vs 55% daily)")
    print("- More data points = More trading opportunities")
    print("- Better for capturing multi-week trends")

    return results


if __name__ == '__main__':
    print("\n" + "="*70)
    print("MAJOR FOREX EVENT TESTING - WEEKLY INTERVALS")
    print("="*70)
    print("\nTest Options:")
    print("1. Swiss Franc 2015 Flash Crash (Weekly)")
    print("2. Brexit 2016 Vote (Weekly)")
    print("3. COVID-19 2020 Crash (Weekly)")
    print("4. ALL EVENTS - WEEKLY (recommended)")
    print()

    choice = input("Enter choice (1-4) or press Enter for ALL: ").strip()

    if choice == '1':
        test_swiss_franc_2015_weekly()
    elif choice == '2':
        test_brexit_2016_weekly()
    elif choice == '3':
        test_covid_crash_2020_weekly()
    else:
        compare_all_events_weekly()

    print("\n" + "="*70)
    print("TESTING COMPLETE!")
    print("="*70)
