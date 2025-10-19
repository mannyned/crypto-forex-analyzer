"""
Forex Lot Size Calculator
Calculates optimal lot sizes based on risk management parameters
"""
import yfinance as yf
from typing import Dict, Optional


class LotCalculator:
    """
    Calculate forex lot sizes based on risk management

    Standard lot sizes:
    - Standard lot: 100,000 units
    - Mini lot: 10,000 units
    - Micro lot: 1,000 units
    - Nano lot: 100 units
    """

    # Pip values for different lot sizes (in USD)
    STANDARD_LOT = 100000
    MINI_LOT = 10000
    MICRO_LOT = 1000
    NANO_LOT = 100

    # Standard pip values (for pairs quoted to 4 decimal places)
    # These are approximate and may vary by broker
    PIP_VALUES = {
        'standard': 10.0,   # $10 per pip for standard lot
        'mini': 1.0,        # $1 per pip for mini lot
        'micro': 0.1,       # $0.10 per pip for micro lot
        'nano': 0.01        # $0.01 per pip for nano lot
    }

    # Japanese Yen pairs (quoted to 2 decimal places)
    JPY_PAIRS = ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY', 'NZDJPY', 'CADJPY', 'CHFJPY']

    def __init__(self):
        self.pip_multiplier = 0.0001  # Default for 4 decimal pairs

    def calculate_pip_value(self, pair: str, lot_size: float, account_currency: str = 'USD') -> float:
        """
        Calculate pip value for a given pair and lot size

        Args:
            pair: Currency pair (e.g., 'EURUSD')
            lot_size: Size in units (e.g., 100000 for 1 standard lot)
            account_currency: Account denomination currency

        Returns:
            Pip value in account currency
        """
        # Remove '=X' suffix if present
        clean_pair = pair.replace('=X', '')

        # Determine pip size based on pair
        if any(jpy in clean_pair for jpy in self.JPY_PAIRS):
            pip_size = 0.01  # JPY pairs use 2 decimal places
        else:
            pip_size = 0.0001  # Most pairs use 4 decimal places

        # Calculate base pip value
        pip_value = lot_size * pip_size

        # For pairs where quote currency is not account currency,
        # we need to convert. For simplicity, we'll use standard approximations
        # In production, you'd fetch live conversion rates

        return pip_value

    def calculate_lot_size(
        self,
        account_balance: float,
        risk_percentage: float,
        stop_loss_pips: float,
        pair: str,
        account_currency: str = 'USD'
    ) -> Dict:
        """
        Calculate optimal lot size based on risk management

        Args:
            account_balance: Trading account balance
            risk_percentage: Percentage of account to risk (e.g., 1.0 for 1%)
            stop_loss_pips: Stop loss distance in pips
            pair: Currency pair
            account_currency: Account currency

        Returns:
            Dictionary with lot size calculations
        """
        # Calculate risk amount in account currency
        risk_amount = account_balance * (risk_percentage / 100)

        # Remove '=X' suffix if present
        clean_pair = pair.replace('=X', '')

        # Determine if this is a JPY pair
        is_jpy_pair = any(jpy in clean_pair for jpy in self.JPY_PAIRS)

        # Get approximate pip value per standard lot
        # For USD account and most pairs, standard lot = $10/pip
        # For JPY pairs, it's different
        if is_jpy_pair:
            # For JPY pairs, pip value calculation is different
            # Approximate: $9-10 per pip for USDJPY
            pip_value_per_standard_lot = 9.0
        else:
            # For most pairs with USD as quote currency
            pip_value_per_standard_lot = 10.0

        # Calculate lot size in standard lots
        # Risk Amount = Lot Size × Pip Value × Stop Loss Pips
        # Lot Size = Risk Amount / (Pip Value × Stop Loss Pips)

        if stop_loss_pips <= 0:
            return {
                'error': 'Stop loss must be greater than 0 pips',
                'lot_size': 0,
                'risk_amount': risk_amount
            }

        standard_lots = risk_amount / (pip_value_per_standard_lot * stop_loss_pips)

        # Convert to different lot types
        mini_lots = standard_lots * 10
        micro_lots = standard_lots * 100
        units = standard_lots * self.STANDARD_LOT

        # Calculate position value
        position_value = standard_lots * self.STANDARD_LOT

        # Calculate leverage required
        leverage_required = position_value / account_balance if account_balance > 0 else 0

        # Calculate actual risk per pip
        risk_per_pip = risk_amount / stop_loss_pips if stop_loss_pips > 0 else 0

        return {
            'account_balance': account_balance,
            'risk_percentage': risk_percentage,
            'risk_amount': round(risk_amount, 2),
            'stop_loss_pips': stop_loss_pips,
            'pair': pair,
            'lot_sizes': {
                'standard_lots': round(standard_lots, 2),
                'mini_lots': round(mini_lots, 2),
                'micro_lots': round(micro_lots, 2),
                'units': round(units, 0)
            },
            'position_value': round(position_value, 2),
            'leverage_required': round(leverage_required, 2),
            'risk_per_pip': round(risk_per_pip, 2),
            'pip_value_per_standard_lot': pip_value_per_standard_lot
        }

    def calculate_position_value(self, lot_size: float, pair: str) -> float:
        """
        Calculate the total position value in base currency

        Args:
            lot_size: Size in standard lots
            pair: Currency pair

        Returns:
            Position value in base currency
        """
        return lot_size * self.STANDARD_LOT

    def calculate_margin_required(
        self,
        lot_size: float,
        pair: str,
        leverage: int = 100
    ) -> Dict:
        """
        Calculate margin required for a position

        Args:
            lot_size: Size in standard lots
            pair: Currency pair
            leverage: Account leverage (e.g., 100 for 1:100)

        Returns:
            Dictionary with margin calculations
        """
        position_value = self.calculate_position_value(lot_size, pair)
        margin_required = position_value / leverage

        return {
            'lot_size': lot_size,
            'position_value': round(position_value, 2),
            'leverage': leverage,
            'margin_required': round(margin_required, 2),
            'free_margin_needed': round(margin_required * 1.2, 2)  # 20% buffer
        }

    def calculate_profit_loss(
        self,
        lot_size: float,
        entry_price: float,
        exit_price: float,
        pair: str,
        position_type: str = 'long'
    ) -> Dict:
        """
        Calculate profit/loss for a trade

        Args:
            lot_size: Size in standard lots
            entry_price: Entry price
            exit_price: Exit/current price
            pair: Currency pair
            position_type: 'long' or 'short'

        Returns:
            Dictionary with P/L calculations
        """
        # Remove '=X' suffix if present
        clean_pair = pair.replace('=X', '')

        # Determine if this is a JPY pair
        is_jpy_pair = any(jpy in clean_pair for jpy in self.JPY_PAIRS)
        pip_size = 0.01 if is_jpy_pair else 0.0001

        # Calculate pip difference
        if position_type.lower() == 'long':
            pip_difference = (exit_price - entry_price) / pip_size
        else:
            pip_difference = (entry_price - exit_price) / pip_size

        # Calculate P/L
        pip_value = 10.0 if not is_jpy_pair else 9.0  # Approximate
        profit_loss = lot_size * pip_difference * pip_value

        # Calculate percentage return
        position_value = lot_size * self.STANDARD_LOT
        percentage_return = (profit_loss / position_value) * 100 if position_value > 0 else 0

        return {
            'lot_size': lot_size,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'position_type': position_type,
            'pip_difference': round(pip_difference, 1),
            'profit_loss': round(profit_loss, 2),
            'percentage_return': round(percentage_return, 2)
        }

    def get_current_price(self, pair: str) -> Optional[float]:
        """
        Get current price for a currency pair

        Args:
            pair: Currency pair symbol

        Returns:
            Current price or None if not available
        """
        try:
            ticker = yf.Ticker(pair)
            data = ticker.history(period='1d', interval='1m')

            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"Error fetching price for {pair}: {e}")
            return None


def format_lot_size_recommendation(calculation: Dict) -> str:
    """
    Format lot size calculation into readable recommendation

    Args:
        calculation: Result from calculate_lot_size

    Returns:
        Formatted string with recommendation
    """
    if 'error' in calculation:
        return calculation['error']

    recommendation = f"""
    POSITION SIZING RECOMMENDATION
    {'='*50}

    Account Balance: ${calculation['account_balance']:,.2f}
    Risk: {calculation['risk_percentage']}% (${calculation['risk_amount']:,.2f})
    Stop Loss: {calculation['stop_loss_pips']} pips
    Pair: {calculation['pair']}

    RECOMMENDED LOT SIZES:
    • Standard Lots: {calculation['lot_sizes']['standard_lots']:.2f}
    • Mini Lots: {calculation['lot_sizes']['mini_lots']:.2f}
    • Micro Lots: {calculation['lot_sizes']['micro_lots']:.2f}
    • Units: {calculation['lot_sizes']['units']:,.0f}

    POSITION DETAILS:
    • Position Value: ${calculation['position_value']:,.2f}
    • Leverage Required: {calculation['leverage_required']:.2f}:1
    • Risk per Pip: ${calculation['risk_per_pip']:.2f}
    • Pip Value (Standard Lot): ${calculation['pip_value_per_standard_lot']:.2f}

    {'='*50}
    """

    return recommendation
