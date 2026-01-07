from flask import Flask, jsonify
from flask_cors import CORS
import random
import time
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

bot_running = False
trades = []

india_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
taiwan_stocks = ["TSMC", "UMC", "ASE", "MEDIATEK"]

def trading_loop(market):
    global bot_running, trades
    while bot_running:
        stock = random.choice(india_stocks if market == "India" else taiwan_stocks)
        trade = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": stock,
            "price": round(random.uniform(100, 2000), 2),
            "qty": random.randint(1, 10),
            "status": "BUY"
        }
        trades.append(trade)
        time.sleep(5)

@app.route("/start/<market>", methods=["GET", "POST"])
def start_bot(market):
    global bot_running
    if not bot_running:
        bot_running = True
        threading.Thread(
            target=trading_loop,
            args=(market,),
            daemon=True
        ).start()
    return jsonify({"status": f"Bot started for {market}"})


@app.route("/stop", methods=["POST"])
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"status": "Bot stopped"})


@app.route("/trades", methods=["GET"])
def get_trades():
    return jsonify(trades)


@app.route("/")
def home():
    return "Trading Bot Backend Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
