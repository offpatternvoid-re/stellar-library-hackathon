from fastapi import FastAPI
from pydantic import BaseModel
import aiohttp
import uvicorn

app = FastAPI()
GROUND_URL = "http://127.0.0.1:8000/receive"
HUB_NAME = "HUB-BETA"

class SatelliteData(BaseModel):
    source: str
    payload: dict
    timestamp: float

@app.post("/relay")
async def relay_to_earth(data: SatelliteData):
    async with aiohttp.ClientSession() as session:
        payload = {
            "source": data.source,
            "hub_relay": HUB_NAME,
            "data": data.payload,
            "timestamp": data.timestamp
        }
        try:
            await session.post(GROUND_URL, json=payload)
            print(f"🛰️ [{HUB_NAME}] Beaming data from {data.source} to Earth...")
            return {"status": "relayed"}
        except:
            return {"status": "error", "message": "Ground Link Down"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)