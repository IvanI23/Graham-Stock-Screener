import json
from data_processing.fetch_all_tickers import fetch_tickers_and_companies, save_tickers_and_companies
from utils.config_loader import get_market_code

def update_single_market(market_name: str, log_callback=None):

    print(f"Attempting to update market: {market_name}")
    
    try:
        market_code = get_market_code(market_name)
        
        with open("data/configs/markets.json", "r", encoding="utf-8") as f:
            markets_data = json.load(f)
            
        if market_code not in markets_data:
            message = f"Market code '{market_code}' for '{market_name}' not found in markets.json."
            print(f"[ERROR] {message}")
            return False, message
        
        url, suffix = markets_data[market_code]
        
        if log_callback:
            log_callback(f"Scraping {market_name} from {url}...")
        else:
            print(f"Scraping {market_name} from {url}...")
        all_data = fetch_tickers_and_companies(market_code, url, suffix, log_callback)
        
        if all_data:
            save_tickers_and_companies(all_data, market_code)
            message = f"Successfully updated market: {market_name}. Found {len(all_data)} tickers."
            print(f"[SUCCESS] {message}")
            return True, message
        else:
            message = f"No data found for market: {market_name}. The raw file was not updated."
            print(f"[WARNING] {message}")
            return False, message
            
    except Exception as e:
        message = f"An error occurred while updating {market_name}: {e}"
        print(f"[ERROR] {message}")
        return False, message 