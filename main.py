from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot is running"}

@app.post("/start")
def start():
    return {"status": "Bot started"}

@app.post("/stop")
def stop():
    return {"status": "Bot stopped"}
