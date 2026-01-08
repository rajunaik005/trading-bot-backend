from flask import Flask, jsonify
from flask_cors import CORS
import random
import time
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

# ===============================
# Bot state per market
# ===============================
bot_running = {
    "India": False,
    "Taiwan": False
}

# Trades per market
trades = {
    "India": [],
    "Taiwan": []
}

india_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
taiwan_stocks = ["TSMC", "UMC", "ASE", "MEDIATEK"]

# ===============================
# Trading loop
# ===============================
def trading_loop(market):
    global bot_running, trades

    stocks = india_stocks if market == "India" else taiwan_stocks

    while bot_running[market]:
        stock = random.choice(stocks)

        # prevent duplicate trades per stock
        existing = {t["symbol"] for t in trades[market]}
        if stock in existing:
            time.sleep(5)
            continue

        trade = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": stock,
            "price": round(random.uniform(100, 2000), 2),
            "qty": random.randint(1, 10),
            "status": "BUY"
        }

        trades[market].append(trade)
        time.sleep(5)

# ===============================
# API endpoints
# ===============================
@app.route("/start/<market>", methods=["GET", "POST"])
def start_bot(market):
    if market not in bot_running:
        return jsonify({"error": "Invalid market"}), 400

    if not bot_running[market]:
        bot_running[market] = True
        threading.Thread(
            target=trading_loop,
            args=(market,),
            daemon=True
        ).start()

    return jsonify({"status": f"Bot started for {market}"})


@app.route("/stop/<market>", methods=["POST"])
def stop_bot(market):
    if market not in bot_running:
        return jsonify({"error": "Invalid market"}), 400

    bot_running[market] = False
    return jsonify({"status": f"Bot stopped for {market}"})


@app.route("/trades/<market>", methods=["GET"])
def get_trades(market):
    if market not in trades:
        return jsonify([])

    return jsonify(trades[market])


@app.route("/")
def home():
    return "Trading Bot Backend Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
