import io
import sys
from datetime import datetime
from contextlib import contextmanager


def get_log_html(log_messages):
    header = "<h4 style='margin-bottom:0.5rem;'>Live Log Output</h4>"
    if log_messages:
        log_html = '<div class="log-section" id="log-section">' + "<br>".join(
            [line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") for line in log_messages]
        ) + '</div>'
    else:
        log_html = '<div class="log-section" id="log-section"></div>'
    return header + log_html

# Context manager to redirect stdout/stderr to Streamlit log
@contextmanager
def streamlit_log_redirect(log_messages, log_placeholder):
    class StreamlitLogStream(io.StringIO):
        def write(self, s):
            if s.strip():
                if "HTTP Error 404:" in s.strip():
                    return super().write(s) 
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_messages.append(f"[{timestamp}] {s.rstrip()}")
                log_placeholder.markdown(get_log_html(log_messages), unsafe_allow_html=True)
            return super().write(s)
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = sys.stderr = StreamlitLogStream()
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# Generic log helper

def log_message(log_messages, log_placeholder, msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_messages.append(f"[{timestamp}] {msg}")
    log_placeholder.markdown(get_log_html(log_messages), unsafe_allow_html=True)

def log_ticker_progress(log_messages, log_placeholder, ticker, company_name=None, current=None, total=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    progress_info = ""
    if current is not None and total is not None:
        percentage = (current / total) * 100
        progress_info = f" ({current}/{total}, {percentage:.1f}%)"
    
    if company_name:
        log_messages.append(f"[{timestamp}] Processing {ticker} ({company_name}){progress_info}")
    else:
        log_messages.append(f"[{timestamp}] Processing {ticker}{progress_info}")
    log_placeholder.markdown(get_log_html(log_messages), unsafe_allow_html=True)

def log_ticker_loading_complete(log_messages, log_placeholder, ticker_count, market_name):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_messages.append(f"[{timestamp}] Successfully loaded {ticker_count} tickers for {market_name}")
    log_placeholder.markdown(get_log_html(log_messages), unsafe_allow_html=True)
