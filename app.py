"""
Flask web application for Crypto & Forex Market Analyzer
"""
from flask import Flask, render_template, jsonify, request
from market_analyzer import MarketAnalyzer
from data_fetcher import CRYPTO_PAIRS, FOREX_PAIRS, CRYPTO_NAMES, FOREX_NAMES
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize analyzer
analyzer = MarketAnalyzer()


@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')


@app.route('/api/markets', methods=['GET'])
def get_markets():
    """
    Get list of available markets

    Returns:
        JSON with available crypto and forex markets
    """
    try:
        markets = {
            'crypto': [
                {'symbol': symbol, 'name': CRYPTO_NAMES.get(symbol, symbol)}
                for symbol in CRYPTO_PAIRS
            ],
            'forex': [
                {'symbol': symbol, 'name': FOREX_NAMES.get(symbol, symbol)}
                for symbol in FOREX_PAIRS
            ]
        }
        return jsonify({
            'success': True,
            'data': markets
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_markets():
    """
    Analyze selected markets and return results

    Request body:
        {
            "crypto": ["BTC/USDT", "ETH/USDT", ...],
            "forex": ["EURUSD=X", "GBPUSD=X", ...]
        }

    Returns:
        JSON with analysis results for selected markets
    """
    try:
        data = request.get_json()

        if not data:
            # If no data provided, return error
            return jsonify({
                'success': False,
                'error': 'No markets selected'
            }), 400

        crypto_symbols = data.get('crypto', [])
        forex_symbols = data.get('forex', [])

        results = {
            'crypto': [],
            'forex': []
        }

        # Analyze selected crypto markets
        for symbol in crypto_symbols:
            print(f"Analyzing {symbol}...")
            analysis = analyzer.analyze_symbol(symbol, 'crypto')
            if analysis:
                analysis['name'] = CRYPTO_NAMES.get(symbol, symbol)
                results['crypto'].append(analysis)

        # Analyze selected forex markets
        for symbol in forex_symbols:
            print(f"Analyzing {symbol}...")
            analysis = analyzer.analyze_symbol(symbol, 'forex')
            if analysis:
                analysis['name'] = FOREX_NAMES.get(symbol, symbol)
                results['forex'].append(analysis)

        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze/<market_type>/<symbol>', methods=['GET'])
def analyze_symbol(market_type, symbol):
    """
    Analyze a specific symbol

    Args:
        market_type: 'crypto' or 'forex'
        symbol: Trading symbol

    Returns:
        JSON with analysis results
    """
    try:
        # For crypto, convert URL format to proper format
        if market_type == 'crypto' and '/' not in symbol:
            symbol = symbol.replace('-', '/')

        analysis = analyzer.analyze_symbol(symbol, market_type)

        if analysis:
            return jsonify({
                'success': True,
                'data': analysis
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Unable to analyze symbol'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Crypto & Forex Market Analyzer'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    print("=" * 60)
    print("  Crypto & Forex Market Analyzer")
    print("=" * 60)
    print(f"\n  Server running on: http://localhost:{port}")
    print(f"  Debug mode: {debug}")
    print("\n  Press CTRL+C to stop\n")
    print("=" * 60)

    app.run(host='0.0.0.0', port=port, debug=debug)
