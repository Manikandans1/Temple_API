from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    live_video_url: Optional[str] = None
    recorded_video_url: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceSchema(ServiceBase):
    id: int
    temple_id: int

    class Config:
        orm_mode = True
