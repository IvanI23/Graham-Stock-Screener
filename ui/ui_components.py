import streamlit as st
import pandas as pd
from typing import Dict, Any, Tuple
from core.screener import format_results_for_display

def create_sidebar(markets: Dict[str, str], graham_criteria: Dict[str, Any]) -> Tuple[str, Dict[str, Any], bool]:

    st.sidebar.title("⚙️ Screener Settings")
    

    st.sidebar.subheader("🌍 Select Market")
    selected_market = st.sidebar.selectbox(
        "Choose a market:",
        options=list(markets.keys()),
        index=0
    )


    st.sidebar.subheader("🔄 Update Market Data")
    update_market_button_clicked = st.sidebar.button(
        "Update Selected Market",
        use_container_width=True,
        key="update_market_button"
    )
    
    st.sidebar.subheader("🎯 Graham Filters")
    
    if 'filters' not in st.session_state:
        st.session_state.filters = graham_criteria.copy()
    
    if 'slider_key' not in st.session_state:
        st.session_state.slider_key = 0
    
    pe_max = st.sidebar.slider(
        "P/E Ratio (Max)",
        min_value=0.0,
        max_value=50.0,
        value=float(st.session_state.filters.get('pe_max', 15.0)),
        step=0.5,
        key=f"pe_slider_{st.session_state.slider_key}"
    )
    
    pb_max = st.sidebar.slider(
        "P/B Ratio (Max)",
        min_value=0.0,
        max_value=10.0,
        value=float(st.session_state.filters.get('pb_max', 1.5)),
        step=0.1,
        key=f"pb_slider_{st.session_state.slider_key}"
    )
    
    pe_pb_max = st.sidebar.slider(
        "P/E × P/B (Max)",
        min_value=0.0,
        max_value=50.0,
        value=float(st.session_state.filters.get('pe_pb_max', 22.5)),
        step=0.5,
        key=f"pe_pb_slider_{st.session_state.slider_key}"
    )
    
    debt_to_equity_max = st.sidebar.slider(
        "Debt/Equity (Max)",
        min_value=0.0,
        max_value=2.0,
        value=float(st.session_state.filters.get('debt_to_equity_max', 0.5)),
        step=0.1,
        key=f"debt_equity_slider_{st.session_state.slider_key}"
    )
    
    current_ratio_min = st.sidebar.slider(
        "Current Ratio (Min)",
        min_value=0.0,
        max_value=5.0,
        value=float(st.session_state.filters.get('current_ratio_min', 1.5)),
        step=0.1,
        key=f"current_ratio_slider_{st.session_state.slider_key}"
    )
    
    dividend_yield_min = st.sidebar.slider(
        "Dividend Yield % (Min)",
        min_value=0.0,
        max_value=10.0,
        value=float(st.session_state.filters.get('dividend_yield_min', 2.0)),
        step=0.1,
        key=f"dividend_yield_slider_{st.session_state.slider_key}"
    )
    
    eps_min = st.sidebar.slider(
        "EPS (Min)",
        min_value=-10.0,
        max_value=50.0,
        value=float(st.session_state.filters.get('eps_min', 0.0)),
        step=0.1,
        key=f"eps_slider_{st.session_state.slider_key}"
    )
    
    market_cap_min = st.sidebar.slider(
        "Market Cap (Min, $M)",
        min_value=0.0,
        max_value=10000.0,
        value=float(st.session_state.filters.get('market_cap_min', 500.0)),
        step=50.0,
        key=f"market_cap_slider_{st.session_state.slider_key}"
    )
    
    if st.sidebar.button("🔄 Reset to Graham Defaults", use_container_width=True):
        st.session_state.filters = graham_criteria.copy()
        st.session_state.slider_key += 1
        st.rerun()
    
    filters = {
        'pe_max': pe_max,
        'pb_max': pb_max,
        'pe_pb_max': pe_pb_max,
        'debt_to_equity_max': debt_to_equity_max,
        'current_ratio_min': current_ratio_min,
        'dividend_yield_min': dividend_yield_min,
        'eps_min': eps_min,
        'market_cap_min': market_cap_min
    }
    
    st.session_state.filters = filters
    
    return selected_market, filters, update_market_button_clicked

def display_results(df: pd.DataFrame, market_name: str):
    st.markdown("---")
    st.subheader(f"📊 Screening Results for {market_name}")
    
    if df.empty:
        st.warning("No stocks found matching your criteria.")
        return
    
    display_df = format_results_for_display(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Stocks", len(df))
    with col2:
        avg_pe = df['PE'].mean() if 'PE' in df.columns else 0
        st.metric("Avg P/E", f"{avg_pe:.2f}")
    with col3:
        avg_pb = df['PB'].mean() if 'PB' in df.columns else 0
        st.metric("Avg P/B", f"{avg_pb:.2f}")
    with col4:
        avg_div = (df['DividendYield'].mean() if 'DividendYield' in df.columns else 0)
        st.metric("Avg Dividend Yield", f"{avg_div:.2f}%")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"graham_screener_{market_name.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True
    )

def display_how_to():
    st.markdown("---")
    st.subheader("📖 How to Use the Graham Stock Screener")

    st.markdown("""
    This tool helps you find stocks based on the value investing principles of Benjamin Graham. 
    Here's a step-by-step guide:

    ### 1. Select a Market
    - Use the dropdown in the sidebar to choose the stock market you want to screen (e.g., NYSE, NASDAQ).

    ### 2. Update Market Data (Optional but Recommended)
    - The screener uses pre-downloaded ticker lists for speed. However, this data can become outdated.
    - Click **"Update Selected Market"** to fetch the latest list of tickers for the chosen market. This can take a few moments.
    - It is recommended to do this periodically to ensure you are screening the most current list of available stocks.

    ### 3. Adjust Graham Filters
    - The sidebar contains sliders for various financial metrics based on Graham's criteria:
        - **P/E Ratio:** Price-to-Earnings ratio. Lower is generally better.
        - **P/B Ratio:** Price-to-Book ratio. Graham preferred values under 1.5.
        - **Debt/Equity:** A measure of a company's financial leverage.
        - **Current Ratio:** Measures a company's ability to pay short-term obligations.
        - **Dividend Yield:** The annual dividend per share as a percentage of the stock's price.
        - **EPS (Earnings Per Share):** A measure of a company's profitability.
    - You can adjust these sliders to match your risk tolerance.
    - Click **"Reset to Graham Defaults"** to return to the standard criteria.

    ### 4. Run the Screener
    - Once you've set your criteria, click the **"🚀 Run Graham Screener"** button.
    - The screener will perform the following steps, shown in the log window:
        1. **Load Tickers:** Reads the list of stocks for the selected market.
        2. **Process Data:** Fetches the latest financial data for each stock using yfinance. This is the most time-consuming part.
        3. **Apply Filters:** Screens the stocks against both the core Graham criteria and your custom adjustments.

    ### 5. Review the Results
    - The results will appear in a table.
    - You can sort the table by clicking on the column headers.
    - To save the results, click the **"📥 Download Results as CSV"** button.

    ### Tips
    - **Patience is Key:** The data processing step can be slow, especially for large markets. The log window will show the progress.
    - **No Results?** If you get no results, try relaxing your filter criteria. The default Graham settings can be quite strict for modern markets.
    - **Errors:** If a specific stock fails to load, the screener will note the error in the log and continue with the next one.
    """) 