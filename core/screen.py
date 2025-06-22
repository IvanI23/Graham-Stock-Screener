import pandas as pd

def filter(df):
    return df[
        (df["PE"] < 15) &                          
        (df["PB"] < 1.5) &                         
        ((df["PE"] * df["PB"]) < 22.5) &           
        (df["DebtToEquity"] < 0.5) &               
        (df["CurrentRatio"] > 1.5) &               
        (df["DividendYield"] > 0.02) &             
        (df["EPS"] > 0) &                          
        (df["MarketCap"] > 500_000_000)            
    ]

def apply_filter(file_path, market):
    df = pd.read_csv(file_path)
    filtered_df = filter(df)
    filtered_df.to_csv(f"results/filtered_{market}.csv", index=False)
    print(f"Filtered stocks saved to 'results/filtered_{market}.csv'")
    return filtered_df 