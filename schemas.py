from typing import List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    city: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    state: Optional[str]


class Checkpoint(BaseModel):
    description: str
    location: Location


class TrackingResponse(BaseModel):
    carrier: str
    checkpoints: List[Checkpoint]
    description: str
    status: str
    time: str
    tracking_stage: str
    delivered: bool
    delivery_date: str
    estimated_delivery: str
    tracking_number: str
