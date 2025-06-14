from pydantic import BaseModel
from typing import List
from enum import Enum
from typing import Optional

class BookingStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class BookingPersonSchema(BaseModel):
    name: str
    gothram: str
    rasi: str
    nakshatra: str

    class Config:
        from_attributes = True

class BookingSchema(BaseModel):
    temple_id: int
    services: List[int]
    video_type: str
    persons: List[BookingPersonSchema]

class BookingResponseSchema(BaseModel):
    id: int
    temple_id: int
    user_id: Optional[int] = None
    total_price: int
    video_type: str
    status: BookingStatusEnum
    persons: List[BookingPersonSchema]

    class Config:
        from_attributes = True
