import yfinance as yf

def get_market_price(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")

    if not data.empty:
        price = data["Close"].iloc[-1]
        return f"{symbol} latest close: {price}"
    
    return "No data found"


