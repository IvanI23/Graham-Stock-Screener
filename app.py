import streamlit as st
from utils.config_loader import load_markets, load_graham_criteria, get_market_code
from ui.ui_components import create_sidebar, display_results, display_how_to
from core.screener import run_screener_with_logs
from utils.logger import get_log_html
from data_processing.update_market import update_single_market


st.set_page_config(
    page_title="Graham Stock Screener",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .log-section {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        max-height: 350px;
        overflow-y: scroll;
        font-family: monospace;
        font-size: 1rem;
        white-space: pre-wrap;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Graham Stock Screener</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Value investing based on Benjamin Graham\'s principles</p>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2 = st.tabs(["Screener", "How To"])

    with tab1:
        # Load configurations
        markets = load_markets()
        graham_criteria = load_graham_criteria()
        
        # Create sidebar
        selected_market, filters, update_market_button_clicked = create_sidebar(markets, graham_criteria)
        

        if 'screening_active' not in st.session_state:
            st.session_state.screening_active = False
        if 'results_df' not in st.session_state:
            st.session_state.results_df = None
        if 'log_messages' not in st.session_state:
            st.session_state.log_messages = []
        if 'market_update_logs' not in st.session_state:
            st.session_state.market_update_logs = []
        
        # Create results placeholder
        results_placeholder = st.empty()
        
        # Handle market update in the main panel to show logs
        if update_market_button_clicked:
            if not selected_market:
                st.sidebar.warning("Please select a market to update.")
            else:
                st.session_state.market_update_logs = [f"Starting update for {selected_market}..."]
                st.session_state.log_messages = []  # Clear previous screener logs
                log_placeholder = st.empty()
                
                def log_to_ui(message):
                    st.session_state.market_update_logs.append(message)
                    log_html = get_log_html(st.session_state.market_update_logs)
                    log_placeholder.markdown(log_html, unsafe_allow_html=True)
                
                with st.spinner(f"Updating {selected_market}... This may take a while."):
                    success, message = update_single_market(selected_market, log_to_ui)
                    if success:
                        st.sidebar.success(message)
                        log_to_ui(f"✅ {message}")
                    else:
                        st.sidebar.error(message)
                        log_to_ui(f"❌ {message}")

        # Display market update logs if they exist
        if st.session_state.market_update_logs and not update_market_button_clicked:
            log_html = get_log_html(st.session_state.market_update_logs)
            st.markdown(log_html, unsafe_allow_html=True)
        
        # Main content area
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Run button
            if st.button("🚀 Run Graham Screener", type="primary", use_container_width=True, disabled=st.session_state.screening_active):
                if selected_market:
                    st.session_state.screening_active = True
                    st.session_state.results_df = None
                    st.session_state.log_messages = []
                    st.session_state.market_update_logs = []
                    # Clear results area immediately
                    results_placeholder.empty()
                    st.rerun()
                else:
                    st.warning("Please select a market from the sidebar.")
        
        # Stop button (only show when screening is active)
        if st.session_state.screening_active:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("⏹️ Stop Screening", type="secondary", use_container_width=True):
                    st.session_state.screening_active = False
                    st.rerun()
        
        # Terminal-style log display
        log_placeholder = st.empty()
        show_log = st.session_state.screening_active or st.session_state.log_messages
        if show_log:
            log_html = get_log_html(st.session_state.log_messages)
            log_placeholder.markdown(log_html, unsafe_allow_html=True)
        
        # Run screening in background if active
        if st.session_state.screening_active:
            try:
                with st.spinner("Running Graham Screener..."):
                    results_df = run_screener_with_logs(selected_market, filters, st.session_state.log_messages, log_placeholder)
                    if results_df is not None:
                        st.session_state.results_df = results_df
                    st.session_state.screening_active = False
                    st.rerun()
            except Exception as e:
                st.error(f"Error running screener: {str(e)}")
                st.session_state.screening_active = False

        # Display results if available and screening is not active
        if not st.session_state.screening_active and st.session_state.results_df is not None:
            with results_placeholder.container():
                display_results(st.session_state.results_df, selected_market)

    with tab2:
        display_how_to()

if __name__ == "__main__":
    main() 