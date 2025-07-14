import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from indicators import calculate_rsi

def analyze_stock(ticker):
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=180)

    try:
        stock_data = yf.download(ticker, start=start, end=end, progress=False)
        if stock_data.empty:
            return f"\n❌ {ticker} - No data found or invalid symbol."
    except:
        return f"\n❌ {ticker} - Failed to fetch data (maybe no internet or wrong symbol)."

    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['RSI'] = calculate_rsi(stock_data)
    stock_data.dropna(inplace=True)

    latest = stock_data.iloc[-1]
    latest_close = float(latest['Close'])
    latest_ma50 = float(latest['MA50'])
    latest_rsi = float(latest['RSI'])

    result = f"\n📈 Stock: {ticker}\n"
    result += f"Last Close: ₹{latest_close:.2f}\n"
    result += f"MA50: ₹{latest_ma50:.2f}\n"
    result += f"RSI: {latest_rsi:.2f}\n"

    if latest_rsi < 30 and latest_close > latest_ma50:
        result += "✅ Recommendation: BUY"
    elif latest_rsi > 70:
        result += "⚠️ Recommendation: SELL"
    else:
        result += "📊 Recommendation: HOLD"

    # 📊 Plotting
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
    plt.plot(stock_data.index, stock_data['MA50'], label='MA50', color='orange')
    plt.title(f'{ticker} Price & MA50')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(stock_data.index, stock_data['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()

    plt.tight_layout()
    plt.show()

    return result
