from fastapi import FastAPI
from pydantic import BaseModel
import aiohttp, uvicorn

app = FastAPI()
HUB_NAME = "ALPHA" # Для второго файла поставь "BETA"

class Data(BaseModel):
    source: str
    payload: dict
    timestamp: float

@app.post("/relay")
async def relay(data: Data):
    async with aiohttp.ClientSession() as ses:
        msg = {"source": data.source, "hub_relay": HUB_NAME, "data": data.payload, "timestamp": data.timestamp}
        try:
            await ses.post("http://127.0.0.1:8000/receive", json=msg)
            return {"s": "ok"}
        except: return {"s": "err"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) # Для BETA поставь 8002