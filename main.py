from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bot import run_bot, trades, CAPITIAL, RISK_PCT

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

bot_running = False
selected_market = "India"

@app.get("/")
def home():
    return {"status": "Bot is running", "running": bot_running}

@app.post("/start/{market}")
def start(market: str):
    global bot_running, selected_market
    bot_running = True
    selected_market = market
    run_bot(selected_market)  # run immediately for demo
    return {"status": f"Bot started for {market}"}

@app.post("/stop")
def stop():
    global bot_running
    bot_running = False
    return {"status": "Bot stopped"}

@app.get("/trades")
def get_trades():
    return trades
