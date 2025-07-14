import yfinance as yf
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from indicators import calculate_rsi  # make sure this file exists

def predict_next_close(ticker):
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=200)

    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty or len(df) < 60:
            return f"\n❌ {ticker} - Not enough data or invalid symbol."
    except:
        return f"\n❌ {ticker} - Failed to fetch data (check symbol or internet)."

    # 📊 Add indicators
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df)
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)

    # 🧠 Features: close, ma50, rsi
    X = df[['Close', 'MA50', 'RSI']]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    latest_data = df[['Close', 'MA50', 'RSI']].iloc[-1].values.reshape(1, -1)
    predicted_price = float(model.predict(latest_data)[0])
    last_price = float(df['Close'].iloc[-1])
    diff = predicted_price - last_price
    direction = "🔼 Up" if diff > 0 else "🔽 Down"

    result = f"\n🤖 Advanced ML Prediction for {ticker}:\n"
    result += f"Last Close: ₹{last_price:.2f}\n"
    result += f"Predicted Next Close: ₹{predicted_price:.2f} ({direction})\n"
    result += f"Change: ₹{diff:.2f}"

    return result
