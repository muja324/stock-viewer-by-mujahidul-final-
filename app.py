import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import os

# Disable caching to avoid Hugging Face permission issues
os.environ["YFINANCE_NO_CACHE"] = "true"

st.set_page_config(page_title="Stock Viewer by Mujahidul", layout="wide")
st.title("📈 Simple Stock Viewer")

# Sidebar: Stock symbol
ticker_symbol = st.sidebar.selectbox(
    "Select a stock to track:",
    ('AAPL', 'MSFT', 'GOOG', 'META', 'AMZN', 'TSLA', 'OTHER')
)

if ticker_symbol == "OTHER":
    ticker_symbol = st.sidebar.text_input("Enter custom symbol (e.g. TATASTEEL.NS)", "AAPL")

st.sidebar.write("You selected:", ticker_symbol)

# Sidebar: Date input
today = dt.date.today()
year_ago = today - dt.timedelta(days=365)

start_date = st.sidebar.date_input("Start date", value=year_ago)
end_date = st.sidebar.date_input("End date", value=today)

# Validate date range
if end_date <= start_date:
    st.sidebar.error("❌ End date must be after start date.")
else:
    try:
        data = yf.Ticker(ticker_symbol).history(period="1d", start=start_date, end=end_date)

        if data.empty:
            st.warning("No data found for this symbol and date range.")
        else:
            st.success(f"Showing data from {start_date} to {end_date}")
            st.line_chart(data["Close"], height=300)
            st.line_chart(data["Open"], height=200)
            st.line_chart(data["High"], height=200)
            st.line_chart(data["Low"], height=200)
            st.line_chart(data["Volume"], height=200)
    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")
