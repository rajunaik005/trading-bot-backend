from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
from bot import run_bot, trades

app = Flask(__name__)
CORS(app)

# ===============================
# Bot state per market
# ===============================
bot_running = {
    "India": False,
    "Taiwan": False
}

# ===============================
# Background loop
# ===============================
def bot_loop(market):
    while bot_running[market]:
        run_bot(market)
        time.sleep(300)  # run every 5 minutes

# ===============================
# API routes
# ===============================
@app.route("/start/<market>")
def start_bot(market):
    if market not in bot_running:
        return jsonify({"error": "Invalid market"}), 400

    if not bot_running[market]:
        bot_running[market] = True
        threading.Thread(target=bot_loop, args=(market,), daemon=True).start()

    return jsonify({"status": f"Bot started for {market}"})


@app.route("/stop/<market>", methods=["POST"])
def stop_bot(market):
    if market in bot_running:
        bot_running[market] = False
    return jsonify({"status": f"Bot stopped for {market}"})


@app.route("/trades/<market>")
def get_trades(market):
    return jsonify(trades.get(market, []))


@app.route("/")
def home():
    return "Trading Bot Backend Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
