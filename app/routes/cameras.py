from fastapi import APIRouter
from app.schemas.camera import CameraCreate
from app.services.camera_store import create_camera, heartbeat, list_cameras

router = APIRouter(prefix="/cameras", tags=["Cameras"])

@router.post("/")
def register_camera(camera: CameraCreate):
    camera_id = create_camera(camera)
    return {
        "status": "registered",
        "camera_id": camera_id
    }

@router.post("/{camera_id}/heartbeat")
def camera_heartbeat(camera_id: str):
    heartbeat(camera_id)
    return {
        "status": "online",
        "camera_id": camera_id
    }

@router.get("/")
def get_cameras():
    return list_cameras()
