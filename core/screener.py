import pandas as pd
from typing import Dict, Any, Callable
from data_processing.processer import process_data
from core.screen import apply_filter
from utils.config_loader import get_market_code
from utils.logger import streamlit_log_redirect, log_message, log_ticker_progress, log_ticker_loading_complete

def run_screener_with_logs(selected_market: str, filters: Dict[str, Any], log_messages: list, log_placeholder) -> pd.DataFrame:
    try:
        with streamlit_log_redirect(log_messages, log_placeholder):
            market_code = get_market_code(selected_market)
            log_message(log_messages, log_placeholder, f"Starting Graham Screener for {selected_market}")
            log_message(log_messages, log_placeholder, f"Loading tickers for {selected_market} ({market_code})...")

            ticker_file = f'data/raw/{market_code}.csv'
            ticker_df = pd.read_csv(ticker_file)
            ticker_count = len(ticker_df)
            log_ticker_loading_complete(log_messages, log_placeholder, ticker_count, selected_market)
            
            log_message(log_messages, log_placeholder, f"Processing market data with yfinance...")
            
            def progress_callback(ticker, company_name=None, current=None, total=None):
                log_ticker_progress(log_messages, log_placeholder, ticker, company_name, current, total)
            
            result_df = process_data(ticker_file, market_code, progress_callback)
            processed_count = len(result_df)
            
            log_message(log_messages, log_placeholder, f"Applying Graham's value investing filters...")
            processed_file = f'data/processed/{market_code}_tickers.csv'
            filtered_df = apply_filter(processed_file, market_code)
            log_message(log_messages, log_placeholder, f"Applied Graham filters - Found {len(filtered_df)} initial matches")
            
            if filters:
                log_message(log_messages, log_placeholder, "Applying custom filter criteria...")
                initial_count = len(filtered_df)
                filtered_df = apply_custom_filters(filtered_df, filters)
                final_count = len(filtered_df)
                log_message(log_messages, log_placeholder, f"Custom filters applied - {initial_count} -> {final_count} stocks")
            
            log_message(log_messages, log_placeholder, f"Screening complete! Found {len(filtered_df)} stocks matching your criteria")
            log_message(log_messages, log_placeholder, "Results ready for review below")
            return filtered_df
    except Exception as e:
        log_message(log_messages, log_placeholder, f"Error during screening: {str(e)}")
        raise e

def apply_custom_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    mask = pd.Series([True] * len(df), index=df.index)
    
    if filters.get('pe_max') is not None:
        mask &= (df['PE'] <= filters['pe_max'])
    
    if filters.get('pb_max') is not None:
        mask &= (df['PB'] <= filters['pb_max'])
    
    if filters.get('pe_pb_max') is not None:
        mask &= ((df['PE'] * df['PB']) <= filters['pe_pb_max'])
    
    if filters.get('debt_to_equity_max') is not None:
        mask &= (df['DebtToEquity'] <= filters['debt_to_equity_max'])
    
    if filters.get('current_ratio_min') is not None:
        mask &= (df['CurrentRatio'] >= filters['current_ratio_min'])
    
    if filters.get('dividend_yield_min') is not None:
        mask &= (df['DividendYield'] >= filters['dividend_yield_min'] / 100)
    
    if filters.get('eps_min') is not None:
        mask &= (df['EPS'] >= filters['eps_min'])
    
    if filters.get('market_cap_min') is not None:
        mask &= (df['MarketCap'] >= filters['market_cap_min'] * 1e6)
    
    return df[mask]

def format_results_for_display(df: pd.DataFrame) -> pd.DataFrame:
    display_df = df.copy()
    
    if 'PE' in display_df.columns:
        display_df['PE'] = display_df['PE'].round(2)
    if 'PB' in display_df.columns:
        display_df['PB'] = display_df['PB'].round(2)
    if 'DividendYield' in display_df.columns:
        display_df['DividendYield'] = (display_df['DividendYield']).round(2)
    if 'CurrentRatio' in display_df.columns:
        display_df['CurrentRatio'] = display_df['CurrentRatio'].round(2)
    if 'DebtToEquity' in display_df.columns:
        display_df['DebtToEquity'] = display_df['DebtToEquity'].round(2)
    if 'MarketCap' in display_df.columns:
        display_df['MarketCap'] = (display_df['MarketCap'] / 1e9).round(2)
    
    column_mapping = {
        'Ticker': 'Symbol',
        'Name': 'Company Name',
        'Price': 'Current Price',
        'PE': 'P/E Ratio',
        'PB': 'P/B Ratio',
        'EPS': 'EPS',
        'DividendYield': 'Dividend Yield (%)',
        'DebtToEquity': 'Debt/Equity',
        'CurrentRatio': 'Current Ratio',
        'MarketCap': 'Market Cap (B)',
        'LastUpdated': 'Last Updated'
    }
    
    return display_df.rename(columns=column_mapping) 