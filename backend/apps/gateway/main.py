from fastapi import FastAPI
import time

app = FastAPI(title="Stock Platform Gateway API", version="0.1.0")

START_TIME = time.time()

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "gateway"}

@app.get("/ready")
async def readiness_check():
    # Placeholder: verify connections to DBs, message queues, etc.
    return {"status": "ready"}

@app.get("/metrics")
async def metrics():
    # Placeholder: would normally return prometheus metrics
    uptime = time.time() - START_TIME
    return {"uptime_seconds": uptime}
