import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# ===============================
# In-memory trade log
# ===============================
trades = []

# Bot running flag
running = False

# Capital and risk
CAPITAL = 100000
RISK_PCT = 0.01  # 1% risk per trade

# Stock list for India & Taiwan
STOCKS = {
    "India": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
    "Taiwan": ["2330.TW", "2317.TW"]
}

# ===============================
# Position sizing
# ===============================
def position_size(capital, entry, stop, risk_pct=0.01):
    risk_amount = capital * risk_pct
    qty = int(risk_amount / max(0.01, abs(entry - stop)))
    return qty

# ===============================
# Strategy: Different per market
# ===============================
def generate_signal(df, market):
    df["sma50"] = ta.sma(df["Close"], 50)
    df["sma200"] = ta.sma(df["Close"], 200)
    df["ema20"] = ta.ema(df["Close"], 20)
    df["rsi"] = ta.rsi(df["Close"], 14)

    df.dropna(inplace=True)
    last = df.iloc[-1]

    # INDIA: Strong trend-following
    if market == "India":
        if (
            last.Close > last.ema20 and
            last.sma50 > last.sma200 and
            last.rsi > 60
        ):
            return "BUY"

    # TAIWAN: Softer momentum
    if market == "Taiwan":
        if (
            last.Close > last.ema20 and
            last.rsi > 50
        ):
            return "BUY"

    return "HOLD"

# ===============================
# Paper trading bot
# ===============================
def run_bot(market="India"):
    global trades

    for symbol in STOCKS.get(market, []):
        try:
            df = yf.download(symbol, period="6mo", interval="1d", progress=False)
            if df.empty:
                continue

            signal = generate_signal(df, market)
            last_price = float(df.iloc[-1]["Close"])
            stop_price = last_price * 0.98  # 2% stop loss
            qty = position_size(CAPITAL, last_price, stop_price, RISK_PCT)

            if signal == "BUY":
                trade = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "symbol": symbol,
                    "price": round(last_price, 2),
                    "qty": qty,
                    "status": "OPEN"
                }
                trades.append(trade)
                print(f"BUY {symbol} | Qty {qty} | Price {last_price}")

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
