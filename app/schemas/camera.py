from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Literal, Optional


class CameraCreate(BaseModel):
    """Schema for creating a new camera"""
    site_id: str
    name: str
    location: Optional[str] = None
    stream_url: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None


class Camera(BaseModel):
    camera_id: UUID = Field(default_factory=uuid4)
    site_id: str
    name: str
    location: Optional[str] = None

    status: Literal["online", "offline", "maintenance"] = "offline"
    stream_url: Optional[str] = None

    vendor: Optional[str] = None
    model: Optional[str] = None

    last_heartbeat: Optional[datetime] = None
    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
