from fastapi import FastAPI
from app.routes import events

app = FastAPI(
    title="Event Ingestion Service",
    version="1.0.0"
)

app.include_router(events.router)


@app.get("/")
def health():
    return {"status": "ok"}
