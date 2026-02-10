from datetime import datetime
from uuid import uuid4

def map_frigate_event(frigate_event: dict) -> dict:
    after = frigate_event.get("after", {})

    return {
        "event_id": str(uuid4()),
        "event_type": after.get("label"),
        "timestamp": datetime.utcfromtimestamp(
            after.get("start_time", datetime.utcnow().timestamp())
        ),
        "source": "frigate",
        "site_id": "site_001",
        "camera_id": after.get("camera"),
        "severity": "critical" if after.get("label") in ["fire", "smoke"] else "medium",
        "confidence": float(after.get("score", 0.0)),
        "status": "open",
        "evidence": {
            "snapshot_url": after.get("snapshot"),
            "clip_url": None
        },
        "metadata": {
            "frigate_event_id": after.get("id")
        }
    }
