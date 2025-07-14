from analysis import analyze_stock
from predictor import predict_next_close

print("🔍 Stock Analyzer AI + ML Predictor\n")
tickers = input("Enter stock symbols separated by commas (e.g., AAPL, TSLA, INFY): ")

tickers = [t.strip().upper() for t in tickers.split(',')]

for ticker in tickers:
    print(analyze_stock(ticker))         # 🔎 Technical Analysis
    print(predict_next_close(ticker))    # 🤖 ML Prediction
