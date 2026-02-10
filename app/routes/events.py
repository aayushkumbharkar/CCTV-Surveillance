from fastapi import APIRouter, HTTPException, Query
from app.schemas.event import Event
from app.services.event_store import (
    save_event,
    fetch_events,
    update_event_status
)
from typing import Optional

router = APIRouter(prefix="/events", tags=["Events"])

# -------------------------
# POST /events (Create)
# -------------------------
@router.post("/")
def create_event(event: Event):
    try:
        save_event(event)
        return {
            "status": "success",
            "event_id": str(event.event_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# GET /events (Read + Pagination + Filters)
# -------------------------
@router.get("/")
def list_events(
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    site_id: Optional[str] = None,
    camera_id: Optional[str] = None,
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    source: Optional[str] = None,
    from_timestamp: Optional[str] = None,
    to_timestamp: Optional[str] = None
):
    try:
        events = fetch_events(
            limit=limit,
            offset=offset,
            site_id=site_id,
            camera_id=camera_id,
            event_type=event_type,
            severity=severity,
            source=source,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp
        )

        return {
            "limit": limit,
            "offset": offset,
            "count": len(events),
            "filters": {
                "site_id": site_id,
                "camera_id": camera_id,
                "event_type": event_type,
                "severity": severity,
                "source": source,
                "from_timestamp": from_timestamp,
                "to_timestamp": to_timestamp
            },
            "events": events
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# PATCH /events/{event_id}/status (Update)
# -------------------------
@router.patch("/{event_id}/status")
def update_event_status_api(
    event_id: str,
    status: str = Query(..., description="New event status")
):
    try:
        updated = update_event_status(event_id, status)

        if not updated:
            raise HTTPException(status_code=404, detail="Event not found")

        return {
            "status": "success",
            "event_id": event_id,
            "new_status": status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
