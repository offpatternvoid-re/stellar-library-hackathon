from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import datetime, uvicorn

app = FastAPI()
db_logs = []

class Message(BaseModel):
    source: str
    hub_relay: str
    data: dict
    timestamp: float

@app.post("/receive")
async def receive(msg: Message):
    log = {"time": datetime.datetime.now().strftime("%H:%M:%S"), 
           "source": msg.source, "hub": msg.hub_relay, 
           "temp": msg.data.get("temp"), "status": msg.data.get("status")}
    db_logs.append(log)
    if len(db_logs) > 15: db_logs.pop(0)
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def home():
    rows = "".join([f"<tr style='color:#00ffcc'><td>{l['time']}</td><td>{l['source']}</td><td>{l['hub']}</td><td>{l['temp']:.2f}</td><td>{l['status']}</td></tr>" for l in reversed(db_logs)])
    return f"<html><body style='background:#0b0e14;color:white;text-align:center;font-family:sans-serif'><h1>🛰️ STELLAR CONTROL CENTER</h1><table border='1' style='margin:auto;width:80%'><tr><th>Time</th><th>Sat</th><th>Hub</th><th>Temp</th><th>Status</th></tr>{rows}</table><script>setTimeout(()=>location.reload(), 2000)</script></body></html>"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)