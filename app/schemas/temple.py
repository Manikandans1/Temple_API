from pydantic import BaseModel
from typing import Optional

class TempleBase(BaseModel):
    name: str
    location: str
    image_url: Optional[str] = None
    about: Optional[str] = None
    history: Optional[str] = None
    attraction: Optional[str] = None
    significance: Optional[str] = None

class TempleCreate(TempleBase):
    pass

class TempleSchema(TempleBase):
    id: int

    class Config:
        orm_mode = True

