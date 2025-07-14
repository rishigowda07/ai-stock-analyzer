import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import requests
from analysis import analyze_stock
from predictor import predict_next_close

# 🧠 Function to fetch crypto news
def get_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": "demo",  # Replace 'demo' with your API key for more requests
        "currencies": "BTC,ETH",
        "filter": "important",
        "public": "true"
    }

    try:
        res = requests.get(url, params=params)
        news_items = res.json().get("results", [])[:5]

        if not news_items:
            return ["No news found."]

        headlines = []
        for item in news_items:
            title = item.get("title", "No title")
            link = item.get("url", "#")
            headlines.append(f"🔹 [{title}]({link})")
        return headlines

    except Exception as e:
        return [f"⚠️ Failed to fetch news: {e}"]

# 🌐 Streamlit UI
st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("📈 AI Stock Analyzer & Predictor")
st.markdown("Enter stock tickers (e.g., `AAPL`, `TSLA`, `INFY.NS`, `BTC-USD`, `ETH-USD`) separated by commas:")

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

        # 🔥 Chart
        with st.spinner("Generating chart..."):
            stock_data = yf.download(ticker, period="90d", interval="1d", progress=False)
            chart_data = stock_data[['Close']].copy().dropna().tail(60)

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(chart_data.index, chart_data['Close'], label='Close Price', color='cyan')
            ax.set_title(f'{ticker.upper()} Close Price - Last 60 Days')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price (₹)')
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

    # 📰 Crypto News (shown once after loop)
    st.subheader("📰 Latest Crypto News")
    news = get_crypto_news()
    for headline in news:
        st.markdown(headline, unsafe_allow_html=True)
