import asyncio, aiohttp, time, random, numpy as np
from sklearn.ensemble import IsolationForest

class AI:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.history = []
    def is_bad(self, t):
        self.history.append([t])
        if len(self.history) < 20: return False
        if len(self.history) % 10 == 0: self.model.fit(np.array(self.history[-50:]))
        return self.model.predict([[t]])[0] == -1

async def start():
    ai = AI()
    hubs = ["http://127.0.0.1:8001/relay", "http://127.0.0.1:8002/relay"]
    async with aiohttp.ClientSession() as ses:
        print("🛰️ Satellite Active...")
        while True:
            t = random.normalvariate(50, 5)
            if random.random() > 0.9: t += 20 # Генерим аномалию
            if ai.is_bad(t):
                d = {"source": "SAT-1", "payload": {"temp": t, "status": "🚨 ALERT"}, "timestamp": time.time()}
                for h in hubs:
                    try: 
                        await ses.post(h, json=d)
                        print(f"📡 Sent to {h}")
                        break
                    except: continue
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(start())