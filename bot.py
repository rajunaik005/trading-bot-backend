import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# In-memory trade log
trades = []

# Bot running flag
running = False

# Capital and risk (adjustable)
CAPITAL = 100000
RISK_PCT = 0.01  # 1% risk per trade

# Stock list for India & Taiwan (demo)
STOCKS = {
    "India": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
    "Taiwan": ["2330.TW", "2317.TW"]
}

# Simple position sizing
def position_size(capital, entry, stop, risk_pct=0.01):
    risk_amount = capital * risk_pct
    qty = int(risk_amount / max(0.01, abs(entry - stop)))
    return qty

# Trading strategy: simple breakout
def generate_signal(df):
    df["sma50"] = ta.sma(df["Close"], 50)
    df["sma200"] = ta.sma(df["Close"], 200)
    df["ema20"] = ta.ema(df["Close"], 20)
    df["rsi"] = ta.rsi(df["Close"], 14)
    last = df.iloc[-1]

    # Breakout / Trend logic
    if last.Close > last.ema20 and last.sma50 > last.sma200 and last.rsi > 60:
        return "BUY"
    return "HOLD"

# Paper trading bot
def run_bot(market="India"):
    global trades
    for symbol in STOCKS[market]:
        try:
            df = yf.download(symbol, period="6mo", interval="1d")
            df.dropna(inplace=True)
            signal = generate_signal(df)
            last_price = df.iloc[-1]["Close"]
            stop_price = last_price * 0.98  # example stop loss 2%
            qty = position_size(CAPITAL, last_price, stop_price, RISK_PCT)

            if signal == "BUY":
                trades.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "symbol": symbol,
                    "signal": signal,
                    "price": last_price,
                    "qty": qty,
                    "status": "OPEN"
                })
                print(f"Paper BUY: {symbol} qty {qty} at {last_price}")
        except Exception as e:
            print(f"Error {symbol}: {e}")
