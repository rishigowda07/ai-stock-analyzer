import streamlit as st
from analysis import analyze_stock
from predictor import predict_next_close

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("📈 AI Stock Analyzer & Predictor")
st.markdown("Enter stock tickers (e.g., `AAPL`, `TSLA`, `INFY.NS`) separated by commas:")

tickers = st.text_input("Stock Tickers", value="AAPL, TSLA")

if st.button("🔍 Analyze & Predict"):
    tickers = [t.strip().upper() for t in tickers.split(',') if t.strip()]
    for ticker in tickers:
        st.subheader(f"📊 {ticker}")
        
        with st.spinner("Running technical analysis..."):
            result1 = analyze_stock(ticker)
            st.text(result1)
        
        with st.spinner("Running ML prediction..."):
            result2 = predict_next_close(ticker)
            st.text(result2)
