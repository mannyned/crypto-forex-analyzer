"""
Flask web application for Crypto & Forex Market Analyzer
"""
from flask import Flask, render_template, jsonify, request
from market_analyzer import MarketAnalyzer
from data_fetcher import CRYPTO_PAIRS, FOREX_PAIRS, CRYPTO_NAMES, FOREX_NAMES
from lot_calculator import LotCalculator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize analyzer and lot calculator
analyzer = MarketAnalyzer()
lot_calculator = LotCalculator()


@app.route('/')
def home():
    """Render the home page"""
    return render_template('home.html')


@app.route('/index')
def index():
    """Render the combined dashboard (legacy route)"""
    return render_template('index.html')


@app.route('/crypto')
def crypto():
    """Render the cryptocurrency analysis page"""
    return render_template('crypto.html')


@app.route('/forex')
def forex():
    """Render the forex analysis page"""
    return render_template('forex.html')


@app.route('/lot-calculator')
def lot_calculator_page():
    """Render the lot calculator page"""
    return render_template('lot_calculator.html')


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


@app.route('/api/lot-calculator/calculate', methods=['POST'])
def calculate_lot_size():
    """
    Calculate optimal lot size for forex trading

    Request body:
        {
            "account_balance": 10000,
            "risk_percentage": 1,
            "stop_loss_pips": 50,
            "pair": "EURUSD=X",
            "account_currency": "USD"
        }

    Returns:
        JSON with lot size calculations
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        # Extract parameters
        account_balance = float(data.get('account_balance', 0))
        risk_percentage = float(data.get('risk_percentage', 1))
        stop_loss_pips = float(data.get('stop_loss_pips', 0))
        pair = data.get('pair', '')
        account_currency = data.get('account_currency', 'USD')

        # Validate inputs
        if account_balance <= 0:
            return jsonify({
                'success': False,
                'error': 'Account balance must be greater than 0'
            }), 400

        if risk_percentage <= 0 or risk_percentage > 100:
            return jsonify({
                'success': False,
                'error': 'Risk percentage must be between 0 and 100'
            }), 400

        if stop_loss_pips <= 0:
            return jsonify({
                'success': False,
                'error': 'Stop loss must be greater than 0 pips'
            }), 400

        if not pair:
            return jsonify({
                'success': False,
                'error': 'Currency pair is required'
            }), 400

        # Calculate lot size
        result = lot_calculator.calculate_lot_size(
            account_balance=account_balance,
            risk_percentage=risk_percentage,
            stop_loss_pips=stop_loss_pips,
            pair=pair,
            account_currency=account_currency
        )

        return jsonify({
            'success': True,
            'data': result
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/lot-calculator/margin', methods=['POST'])
def calculate_margin():
    """
    Calculate margin required for a position

    Request body:
        {
            "lot_size": 1.0,
            "pair": "EURUSD=X",
            "leverage": 100
        }

    Returns:
        JSON with margin calculations
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        lot_size = float(data.get('lot_size', 0))
        pair = data.get('pair', '')
        leverage = int(data.get('leverage', 100))

        if lot_size <= 0:
            return jsonify({
                'success': False,
                'error': 'Lot size must be greater than 0'
            }), 400

        if leverage <= 0:
            return jsonify({
                'success': False,
                'error': 'Leverage must be greater than 0'
            }), 400

        result = lot_calculator.calculate_margin_required(
            lot_size=lot_size,
            pair=pair,
            leverage=leverage
        )

        return jsonify({
            'success': True,
            'data': result
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/lot-calculator/profit-loss', methods=['POST'])
def calculate_profit_loss():
    """
    Calculate profit/loss for a trade

    Request body:
        {
            "lot_size": 1.0,
            "entry_price": 1.1000,
            "exit_price": 1.1050,
            "pair": "EURUSD=X",
            "position_type": "long"
        }

    Returns:
        JSON with P/L calculations
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        lot_size = float(data.get('lot_size', 0))
        entry_price = float(data.get('entry_price', 0))
        exit_price = float(data.get('exit_price', 0))
        pair = data.get('pair', '')
        position_type = data.get('position_type', 'long')

        if lot_size <= 0:
            return jsonify({
                'success': False,
                'error': 'Lot size must be greater than 0'
            }), 400

        if entry_price <= 0 or exit_price <= 0:
            return jsonify({
                'success': False,
                'error': 'Prices must be greater than 0'
            }), 400

        result = lot_calculator.calculate_profit_loss(
            lot_size=lot_size,
            entry_price=entry_price,
            exit_price=exit_price,
            pair=pair,
            position_type=position_type
        )

        return jsonify({
            'success': True,
            'data': result
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/lot-calculator/current-price/<pair>', methods=['GET'])
def get_current_price(pair):
    """
    Get current price for a currency pair

    Args:
        pair: Currency pair (e.g., EURUSD=X)

    Returns:
        JSON with current price
    """
    try:
        price = lot_calculator.get_current_price(pair)

        if price is None:
            return jsonify({
                'success': False,
                'error': 'Unable to fetch current price'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'pair': pair,
                'price': round(price, 5)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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
