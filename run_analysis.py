"""
Command-line interface for market analysis
"""
import argparse
import json
from market_analyzer import MarketAnalyzer
from data_fetcher import CRYPTO_PAIRS, FOREX_PAIRS, CRYPTO_NAMES, FOREX_NAMES


def print_analysis(analysis):
    """Print analysis results in a formatted way"""
    if not analysis:
        print("  No data available")
        return

    print(f"\n{'='*60}")
    print(f"  {analysis.get('name', analysis['symbol'])} ({analysis['symbol']})")
    print(f"{'='*60}")
    print(f"  Price: ${analysis['current_price']:.2f}" if analysis['current_price'] else "  Price: N/A")
    print(f"  24h Change: {analysis['change_24h']:.2f}%" if analysis['change_24h'] else "  24h Change: N/A")
    print(f"  Signal: {analysis['signal']}")
    print(f"  Strength: {analysis['strength']}%")
    print(f"  Score: {analysis['score']}")
    print(f"\n  Analysis Factors:")
    for reason in analysis['reasons']:
        print(f"    - {reason}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Crypto & Forex Market Analyzer CLI'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Analyze all markets'
    )

    parser.add_argument(
        '--crypto',
        type=str,
        help='Analyze specific crypto pair (e.g., BTC/USDT)'
    )

    parser.add_argument(
        '--forex',
        type=str,
        help='Analyze specific forex pair (e.g., EURUSD=X)'
    )

    parser.add_argument(
        '--timeframe',
        type=str,
        default='1h',
        choices=['1h', '4h', '1d'],
        help='Timeframe for analysis (default: 1h)'
    )

    parser.add_argument(
        '--export',
        type=str,
        help='Export results to JSON file'
    )

    parser.add_argument(
        '--recommend',
        action='store_true',
        help='Show investment recommendations'
    )

    parser.add_argument(
        '--risk',
        type=str,
        default='medium',
        choices=['low', 'medium', 'high'],
        help='Risk tolerance for recommendations (default: medium)'
    )

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = MarketAnalyzer()

    results = {}

    # Analyze all markets
    if args.all:
        print("\nAnalyzing all markets...\n")
        results = analyzer.analyze_all_markets()

        print("\n" + "="*60)
        print("  TOP OPPORTUNITIES")
        print("="*60)
        for opp in results['top_opportunities']:
            print(f"\n  {opp.get('name', opp['symbol'])} - {opp['signal']}")
            print(f"  Strength: {opp['strength']}% | Score: {opp['score']}")
            print(f"  Top reasons:")
            for reason in opp['reasons'][:3]:
                print(f"    - {reason}")

        print("\n" + "="*60)
        print("  CRYPTOCURRENCY ANALYSIS")
        print("="*60)
        for analysis in results['crypto']:
            print(f"\n  {analysis.get('name', analysis['symbol'])}: {analysis['signal']} (Strength: {analysis['strength']}%)")

        print("\n" + "="*60)
        print("  FOREX ANALYSIS")
        print("="*60)
        for analysis in results['forex']:
            print(f"\n  {analysis.get('name', analysis['symbol'])}: {analysis['signal']} (Strength: {analysis['strength']}%)")

    # Analyze specific crypto
    elif args.crypto:
        print(f"\nAnalyzing {args.crypto}...")
        analysis = analyzer.analyze_symbol(args.crypto, 'crypto', args.timeframe)
        if analysis:
            analysis['name'] = CRYPTO_NAMES.get(args.crypto, args.crypto)
            print_analysis(analysis)
            results = {'analysis': analysis}
        else:
            print("Failed to analyze symbol")

    # Analyze specific forex
    elif args.forex:
        print(f"\nAnalyzing {args.forex}...")
        analysis = analyzer.analyze_symbol(args.forex, 'forex', args.timeframe)
        if analysis:
            analysis['name'] = FOREX_NAMES.get(args.forex, args.forex)
            print_analysis(analysis)
            results = {'analysis': analysis}
        else:
            print("Failed to analyze symbol")

    # Show recommendations
    if args.recommend and results:
        print("\n" + "="*60)
        print("  INVESTMENT RECOMMENDATIONS")
        print("="*60)
        print(f"  Risk Tolerance: {args.risk.upper()}")
        print(f"{'='*60}\n")

        if 'top_opportunities' in results:
            opportunities = results['top_opportunities']
        elif 'analysis' in results:
            opportunities = [results['analysis']]
        else:
            opportunities = []

        for opp in opportunities:
            if args.risk == 'low' and opp['strength'] < 70:
                continue
            elif args.risk == 'medium' and opp['strength'] < 60:
                continue
            # High risk accepts all signals

            print(f"  {opp.get('name', opp['symbol'])}")
            print(f"  Signal: {opp['signal']}")
            print(f"  Confidence: {opp['strength']}%")

            if opp['signal'] in ['STRONG BUY', 'BUY']:
                print(f"  Recommendation: Consider BUYING")
                print(f"  Entry: Around ${opp['current_price']:.2f}" if opp.get('current_price') else "")
                if opp.get('indicators', {}).get('bb_lower'):
                    print(f"  Stop Loss: Below ${opp['indicators']['bb_lower']:.2f}")
                if opp.get('indicators', {}).get('bb_upper'):
                    print(f"  Take Profit: Near ${opp['indicators']['bb_upper']:.2f}")
            elif opp['signal'] in ['STRONG SELL', 'SELL']:
                print(f"  Recommendation: Consider SELLING or avoiding")
                print(f"  Risk: Downtrend likely")

            print(f"\n  Key Factors:")
            for reason in opp['reasons'][:5]:
                print(f"    - {reason}")
            print()

    # Export results
    if args.export and results:
        try:
            with open(args.export, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults exported to {args.export}")
        except Exception as e:
            print(f"\nError exporting results: {e}")

    # Show usage if no arguments
    if not any([args.all, args.crypto, args.forex]):
        parser.print_help()
        print("\nExamples:")
        print("  python run_analysis.py --all")
        print("  python run_analysis.py --crypto BTC/USDT")
        print("  python run_analysis.py --forex EURUSD=X")
        print("  python run_analysis.py --all --recommend --risk medium")
        print("  python run_analysis.py --all --export results.json")


if __name__ == '__main__':
    main()
