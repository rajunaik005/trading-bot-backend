import yfinance as yf
import pandas_ta as ta
from datetime import datetime

# ===============================
# Trades stored per market
# ===============================
trades = {
    "India": [],
    "Taiwan": []
}

# ===============================
# Capital & risk
# ===============================
CAPITAL = 100000
RISK_PCT = 0.01

# ===============================
# Stock universe
# ===============================
STOCKS = {
    "India": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
    "Taiwan": ["2330.TW", "2317.TW"]
}

# ===============================
# Position sizing
# ===============================
def position_size(capital, entry, stop, risk_pct):
    risk_amount = capital * risk_pct
    return int(risk_amount / max(0.01, abs(entry - stop)))

# ===============================
# Strategy per market
# ===============================
def generate_signal(df, market):
    df["ema20"] = ta.ema(df["Close"], 20)
    df["rsi"] = ta.rsi(df["Close"], 14)
    df["sma50"] = ta.sma(df["Close"], 50)
    df["sma200"] = ta.sma(df["Close"], 200)
    df.dropna(inplace=True)

    last = df.iloc[-1]

    if market == "India":
        if last.Close > last.ema20 and last.sma50 > last.sma200 and last.rsi > 60:
            return "BUY"

    if market == "Taiwan":
        if last.Close > last.ema20 and last.rsi > 50:
            return "BUY"

    return "HOLD"

# ===============================
# Run bot ONCE (called by API)
# ===============================
def run_bot(market):
    for symbol in STOCKS.get(market, []):
        try:
            # Prevent duplicate trades
            existing = {t["symbol"] for t in trades[market]}
            if symbol in existing:
                continue

            df = yf.download(symbol, period="6mo", interval="1d", progress=False)
            if df.empty:
                continue

            signal = generate_signal(df, market)
            if signal != "BUY":
                continue

            price = float(df.iloc[-1]["Close"])
            stop = price * 0.98
            qty = position_size(CAPITAL, price, stop, RISK_PCT)

            trades[market].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
                "price": round(price, 2),
                "qty": qty,
                "status": "OPEN"
            })

        except Exception as e:
            print(f"{symbol} error: {e}")
