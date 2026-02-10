from fastapi import APIRouter, HTTPException, Request
from app.utils.frigate_mapper import map_frigate_event
from app.schemas.event import Event
from app.services.event_store import save_event

router = APIRouter(prefix="/frigate", tags=["Frigate"])


@router.post("/webhook")
async def frigate_webhook(request: Request):
    """
    Receives Frigate webhook events,
    maps them to internal Event schema,
    and stores them in DB.
    """
    try:
        payload = await request.json()

        mapped_event = map_frigate_event(payload)
        event = Event(**mapped_event)

        save_event(event)

        return {
            "status": "success",
            "event_id": str(event.event_id)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
