import pandas as pd
import yfinance as yf
import requests
from requests.exceptions import HTTPError

def process_ticker(ticker, log_callback=None):
    try:
        stock = yf.Ticker(ticker)
        info = stock.get_info() 
        company_name = info.get("shortName", "") if info else ""

        has_valid_data = any([
            info.get("currentPrice"),
            info.get("trailingPE"),
            info.get("priceToBook"),
            info.get("trailingEps"),
            info.get("dividendYield"),
            info.get("debtToEquity"),
            info.get("currentRatio"),
            info.get("marketCap")
        ])
        
        if not has_valid_data:
            print(f"[ERROR] {ticker}: Ticker is not supported in Yahoo Finance API")
            
        elif log_callback:
            log_callback(ticker, company_name)
        else:
            print(f"[INFO] Processing {ticker}")
        
        return {
            "Ticker": ticker,
            "Name": company_name,
            "Price": info.get("currentPrice"),
            "PE": info.get("trailingPE"),
            "PB": info.get("priceToBook"),
            "EPS": info.get("trailingEps"),
            "DividendYield": info.get("dividendYield"),
            "DebtToEquity": info.get("debtToEquity"),
            "CurrentRatio": info.get("currentRatio"),
            "MarketCap": info.get("marketCap"),
            "LastUpdated": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"[ERROR] {ticker}: Ticker is not supported in Yahoo Finance API")
        else:
            print(f"[ERROR] {ticker}: HTTP error {e.response.status_code} - {e}")
        return None
    except Exception as e:
        print(f"[ERROR] {ticker}: {type(e).__name__} - {e}")
        return None

def process_data(file_path, market, log_callback=None):
    df = pd.read_csv(file_path)

    if 'Ticker' not in df.columns:
        raise ValueError("CSV must contain a 'Ticker' column.")

    results = []
    total_tickers = len(df)
    processed_tickers = 0

    for index, ticker in enumerate(df['Ticker'], 1):
        result = process_ticker(ticker, log_callback=lambda t, cn=None: log_callback(t, cn, index, total_tickers) if log_callback else None)
        if result:
            results.append(result)
            if result['Price'] is not None:
                processed_tickers += 1

    result_df = pd.DataFrame(results)
    result_df.to_csv(f'data/processed/{market}_tickers.csv', index=False)
    success_rate = (processed_tickers / total_tickers) * 100
    print(f"Successfully processed {processed_tickers}/{total_tickers} tickers ({success_rate:.2f}% for {market})")
    return result_df 