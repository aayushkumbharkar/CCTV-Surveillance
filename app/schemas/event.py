from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Literal, Optional

class Evidence(BaseModel):
    snapshot_url: Optional[str] = None
    clip_url: Optional[str] = None

class Event(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    timestamp: datetime
    source: Literal["nvr", "ai", "system", "frigate"]
    site_id: str
    camera_id: str
    severity: Literal["low", "medium", "high", "critical"]
    confidence: float
    status: Literal["open", "acknowledged", "closed"]
    evidence: Optional[Evidence] = None
    metadata: Optional[dict] = None

    
    class Config:
        from_attributes = True
