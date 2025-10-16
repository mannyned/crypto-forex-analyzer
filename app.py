"""
Flask web application for Crypto & Forex Market Analyzer
"""
from flask import Flask, render_template, jsonify
from market_analyzer import MarketAnalyzer
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


@app.route('/api/analyze', methods=['GET'])
def analyze_markets():
    """
    Analyze all markets and return results

    Returns:
        JSON with crypto, forex, and top opportunities
    """
    try:
        results = analyzer.analyze_all_markets()
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
