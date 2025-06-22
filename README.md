# 📈 Graham Stock Screener

A modern Streamlit application for finding undervalued stocks using Benjamin Graham's value investing principles.

## 🚀 Features

- **Real-time Stock Screening**: Screen stocks across 100+ global markets
- **Graham Criteria**: Built-in filters based on Benjamin Graham's original criteria
- **Customizable Filters**: Adjust all screening parameters with intuitive sliders
- **Export Results**: Download screening results as CSV files
- **Responsive Design**: Clean, modern UI that works on all devices
- **Live Logging**: Real-time progress updates during screening

## 📁 Project Structure

```
Graham_Screen/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── core/                           # Core business logic
│   ├── screener.py                 # Main screening orchestration
│   └── screen.py                   # Graham filtering logic
│
├── data_processing/                # Data fetching and processing
│   ├── processer.py                # Stock data processing with yfinance
│   ├── update_market.py            # Market data updates
│   └── fetch_all_tickers.py        # Web scraping for ticker lists
│
├── ui/                             # User interface components
│   └── ui_components.py            # Streamlit UI components
│
├── utils/                          # Utility modules
│   ├── config_loader.py            # Configuration loading
│   └── logger.py                   # Logging utilities
│
├── data/                           # Data files
│   ├── configs/                    # Configuration files
│   │   ├── markets_config.json     # Market definitions
│   │   ├── graham_criteria.json    # Graham's original criteria
│   │   └── markets.json            # Backend market data
│   ├── raw/                        # Raw ticker data
│   └── processed/                  # Processed stock data
│
├── results/                        # Screening results
└── logs/                          # Application logs
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Graham_Screen
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🎯 How to Use

### 1. Select Market
Choose from 100+ global markets including:
- **US Markets**: NYSE, NASDAQ, US OTC
- **European Markets**: London, Frankfurt, Paris, Amsterdam
- **Asian Markets**: Tokyo, Hong Kong, Shanghai, Singapore
- **Emerging Markets**: India, Brazil, South Africa, and more

### 2. Update Market Data (Optional)
- Click "Update Selected Market" to fetch the latest ticker lists
- Recommended to do this periodically for accurate results

### 3. Adjust Filters
All filters default to Graham's original criteria:
- **P/E Ratio**: ≤ 15 (Maximum Price-to-Earnings)
- **P/B Ratio**: ≤ 1.5 (Maximum Price-to-Book)
- **P/E × P/B**: ≤ 22.5 (Maximum product)
- **Debt/Equity**: ≤ 0.5 (Maximum Debt-to-Equity ratio)
- **Current Ratio**: ≥ 1.5 (Minimum Current Ratio)
- **Dividend Yield**: ≥ 2% (Minimum dividend yield)
- **EPS**: > 0 (Positive Earnings Per Share)
- **Market Cap**: ≥ $500M (Minimum Market Capitalization)

### 4. Run Screening
Click "🚀 Run Screener" to start the process:
1. **Load Tickers**: Reads stock symbols for selected market
2. **Process Data**: Downloads financial data using yfinance
3. **Apply Filters**: Filters stocks based on Graham criteria
4. **Display Results**: Shows matching stocks in a formatted table

### 5. View Results
- **Results Table**: View filtered stocks with key metrics
- **Download**: Export results as CSV for further analysis

## 🔧 Configuration

### Adding New Markets
Edit `data/configs/markets_config.json` to add new markets:
```json
{
  "markets": {
    "Market Name": "MARKET_CODE"
  }
}
```

### Modifying Graham Criteria
Edit `data/configs/graham_criteria.json` to adjust default values:
```json
{
  "graham_criteria": {
    "pe_max": 15.0,
    "pb_max": 1.5,
    "pe_pb_max": 22.5
  }
}
```

## 📊 Graham's Investment Criteria

Benjamin Graham's original criteria for defensive investors:

1. **Size**: Market cap ≥ $500M (large companies)
2. **Financial Strength**: Current ratio ≥ 1.5
3. **Earnings Stability**: Positive earnings for past 10 years
4. **Dividend Record**: Uninterrupted dividends for past 20 years
5. **Earnings Growth**: 33% increase in per-share earnings over 10 years
6. **Moderate P/E**: P/E ratio ≤ 15
7. **Moderate P/B**: P/B ratio ≤ 1.5
8. **Price Safety**: P/E × P/B ≤ 22.5

## 🚀 Performance

- **Real-time Processing**: Live updates during screening
- **Scalable**: Handles thousands of stocks efficiently
- **Fast**: Optimized data processing and filtering
- **Modular Design**: Clean separation of concerns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Benjamin Graham**: For the original value investing principles
- **Streamlit**: For the amazing web app framework
- **yfinance**: For reliable financial data
- **Pandas**: For powerful data manipulation

---

**Built with ❤️ for value investors everywhere**
