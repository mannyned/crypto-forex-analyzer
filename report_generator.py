"""
HTML Report Generator for Backtest and Historical Test Results
"""
import json
from datetime import datetime


def generate_html_report(results_file, output_file='test_report.html'):
    """
    Generate HTML report from test results JSON

    Args:
        results_file: Path to JSON results file
        output_file: Output HTML file path
    """
    # Load results
    with open(results_file, 'r') as f:
        data = json.load(f)

    # Check if it's backtest or historical test
    is_backtest = 'metrics' in data

    if is_backtest:
        html = generate_backtest_report(data)
    else:
        html = generate_historical_test_report(data)

    # Save HTML
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✅ HTML report generated: {output_file}")


def generate_backtest_report(data):
    """Generate HTML report for backtest results"""
    metrics = data['metrics']
    trades = data.get('trades', [])
    timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Calculate additional stats
    winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
    losing_trades = [t for t in trades if t.get('pnl', 0) < 0]

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backtest Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0d0d0d;
            color: #e8e8e8;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%);
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: #0d0d0d;
        }}

        .timestamp {{
            color: rgba(13, 13, 13, 0.8);
            font-size: 0.9rem;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .metric-card {{
            background: #171717;
            border: 1px solid #2d2d2d;
            border-radius: 12px;
            padding: 25px;
            transition: transform 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-4px);
            border-color: #00d4ff;
        }}

        .metric-label {{
            color: #b0b0b0;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }}

        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }}

        .metric-value.positive {{
            color: #00ff88;
        }}

        .metric-value.negative {{
            color: #ff3366;
        }}

        .metric-value.neutral {{
            color: #00d4ff;
        }}

        .section {{
            background: #171717;
            border: 1px solid #2d2d2d;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
        }}

        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            color: #00d4ff;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #2d2d2d;
        }}

        th {{
            background: #232323;
            color: #00d4ff;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.875rem;
            letter-spacing: 0.05em;
        }}

        tr:hover {{
            background: #1f1f1f;
        }}

        .profit {{
            color: #00ff88;
        }}

        .loss {{
            color: #ff3366;
        }}

        .stat-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid #2d2d2d;
        }}

        .stat-bar:last-child {{
            border-bottom: none;
        }}

        .stat-name {{
            color: #b0b0b0;
            font-size: 0.9rem;
        }}

        .stat-value {{
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #2d2d2d;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
            border-radius: 4px;
            transition: width 0.3s;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .badge-profit {{
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
        }}

        .badge-loss {{
            background: rgba(255, 51, 102, 0.2);
            color: #ff3366;
        }}

        .badge-neutral {{
            background: rgba(0, 212, 255, 0.2);
            color: #00d4ff;
        }}

        footer {{
            text-align: center;
            padding: 20px;
            color: #707070;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Backtest Report</h1>
            <div class="timestamp">Generated: {timestamp}</div>
        </header>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Initial Capital</div>
                <div class="metric-value neutral">${metrics['initial_capital']:,.2f}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Final Capital</div>
                <div class="metric-value {'positive' if metrics['final_capital'] > metrics['initial_capital'] else 'negative'}">${metrics['final_capital']:,.2f}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Total Return</div>
                <div class="metric-value {'positive' if metrics['total_return'] > 0 else 'negative'}">{metrics['total_return']:+.2f}%</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Win Rate</div>
                <div class="metric-value neutral">{metrics['win_rate']:.2f}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {metrics['win_rate']}%"></div>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Total Trades</div>
                <div class="metric-value neutral">{metrics['total_trades']}</div>
                <div style="font-size: 0.875rem; color: #b0b0b0; margin-top: 5px;">
                    {metrics['winning_trades']} wins / {metrics['losing_trades']} losses
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Profit Factor</div>
                <div class="metric-value {'positive' if metrics.get('profit_factor', 0) and metrics['profit_factor'] > 1 else 'negative'}">
                    {metrics['profit_factor']:.2f if metrics.get('profit_factor') else '∞'}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Max Drawdown</div>
                <div class="metric-value negative">{metrics['max_drawdown']:.2f}%</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Sharpe Ratio</div>
                <div class="metric-value neutral">{metrics['sharpe_ratio']:.2f}</div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">💰 Profit/Loss Breakdown</div>

            <div class="stat-bar">
                <span class="stat-name">Total Profit</span>
                <span class="stat-value profit">${metrics['total_profit']:,.2f}</span>
            </div>

            <div class="stat-bar">
                <span class="stat-name">Total Loss</span>
                <span class="stat-value loss">${metrics['total_loss']:,.2f}</span>
            </div>

            <div class="stat-bar">
                <span class="stat-name">Average Win</span>
                <span class="stat-value profit">${metrics['avg_win']:,.2f}</span>
            </div>

            <div class="stat-bar">
                <span class="stat-name">Average Loss</span>
                <span class="stat-value loss">${metrics['avg_loss']:,.2f}</span>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🚪 Exit Reasons</div>

            {''.join([f'''
            <div class="stat-bar">
                <span class="stat-name">{reason}</span>
                <span class="stat-value">{data['count']} trades (Avg: ${data['avg_pnl']:+,.2f})</span>
            </div>
            ''' for reason, data in metrics.get('by_exit_reason', {}).items()])}
        </div>

        <div class="section">
            <div class="section-title">📝 All Trades</div>

            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Entry Date</th>
                        <th>Exit Date</th>
                        <th>Signal</th>
                        <th>Entry Price</th>
                        <th>Exit Price</th>
                        <th>Exit Reason</th>
                        <th>P/L</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        <td>{i+1}</td>
                        <td>{trade.get('entry_date', 'N/A')}</td>
                        <td>{trade.get('exit_date', 'N/A')}</td>
                        <td><span class="badge badge-neutral">{trade.get('signal', 'N/A')}</span></td>
                        <td>${trade.get('entry_price', 0):.2f}</td>
                        <td>${trade.get('exit_price', 0):.2f}</td>
                        <td>{trade.get('exit_reason', 'N/A')}</td>
                        <td class="{'profit' if trade.get('pnl', 0) > 0 else 'loss'}">${trade.get('pnl', 0):+,.2f}</td>
                    </tr>
                    ''' for i, trade in enumerate(trades)])}
                </tbody>
            </table>
        </div>

        <footer>
            <p>Crypto & Forex Market Analyzer v3.0.0</p>
            <p>This report is for educational purposes only. Past performance does not guarantee future results.</p>
        </footer>
    </div>
</body>
</html>
"""

    return html


def generate_historical_test_report(results):
    """Generate HTML report for historical test results"""
    # This would be similar but focused on prediction accuracy
    # Simplified version for now
    return "<html><body><h1>Historical Test Report</h1><p>Use historical_tester.py report format</p></body></html>"


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        results_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'test_report.html'
        generate_html_report(results_file, output_file)
    else:
        print("Usage: python report_generator.py <results_file.json> [output_file.html]")
        print("Example: python report_generator.py backtest_results.json report.html")
