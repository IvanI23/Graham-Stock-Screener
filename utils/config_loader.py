import json
from typing import Dict, Any

def load_markets() -> Dict[str, str]:
    """Load markets from JSON file with proper display names and codes"""
    try:
        with open('data/configs/markets_config.json', 'r') as f:
            config = json.load(f)
            return config['markets']
    except FileNotFoundError:
        # Default markets if file doesn't exist
        return {
            "NYSE": "NYSE",
            "NASDAQ": "NASDAQ",
            "US OTC": "US_OTC",
            "London Stock Exchange": "LON",
            "Toronto Stock Exchange": "TSX",
            "Australian Securities Exchange": "ASX"
        }

def get_market_code(display_name: str) -> str:
    """Get the market code from display name"""
    markets = load_markets()
    return markets.get(display_name, display_name)

def load_graham_criteria() -> Dict[str, Any]:
    """Load Graham criteria from JSON file"""
    try:
        with open('data/configs/graham_criteria.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default Graham criteria if file doesn't exist
        return {
            "pe_max": 15.0,
            "pb_max": 1.5,
            "pe_pb_max": 22.5,
            "debt_to_equity_max": 0.5,
            "current_ratio_min": 1.5,
            "dividend_yield_min": 2.0,
            "eps_min": 0.0,
            "market_cap_min": 500.0
        } 