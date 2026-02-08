import time
import uuid
import random
import requests
from datetime import datetime, timezone

API_URL = "http://127.0.0.1:8000/events/"

EVENT_TYPES = [
    "motion_detected",
    "camera_offline",
    "camera_online",
    "storage_warning",
    "intrusion_detected"
]

SOURCES = ["nvr", "ai", "system"]
SEVERITIES = ["low", "medium", "high"]
STATUSES = ["open", "acknowledged"]
SITES = ["site_101", "site_204"]
CAMERAS = ["cam_01", "cam_07", "cam_12", "cam_21"]

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": random.choice(EVENT_TYPES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": random.choice(SOURCES),
        "site_id": random.choice(SITES),
        "camera_id": random.choice(CAMERAS),
        "severity": random.choice(SEVERITIES),
        "confidence": round(random.uniform(0.6, 0.99), 2),
        "status": random.choice(STATUSES),
        "evidence": {
            "snapshot_url": "https://example.com/snap.jpg",
            "clip_url": None
        },
        "metadata": {
            "simulated": True
        }
    }

def send_event():
    event = generate_event()
    response = requests.post(API_URL, json=event)

    if response.status_code == 200:
        print(f"✅ Sent event {event['event_id']}")
    else:
        print(f"❌ Failed ({response.status_code}): {response.text}")

if __name__ == "__main__":
    print("🚀 Event simulator started (CTRL+C to stop)")
    while True:
        send_event()
        time.sleep(5)  # send every 5 seconds
