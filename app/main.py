from fastapi import FastAPI
from app.routes import events,frigate,cameras

app = FastAPI(
    title="Event Ingestion Service",
    version="1.0.0"
)

app.include_router(events.router)
app.include_router(frigate.router)
app.include_router(cameras.router)

@app.get("/")
def health():
    return {"status": "ok"}
