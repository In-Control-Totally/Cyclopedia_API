from datetime import datetime
from pydantic import BaseModel


class POIActual(BaseModel):
    # use "= None" to mark this as optional for instantiation
    poi_id: int = None
    latitude: float
    longitude: float
    altitude: int
    timestamp: int = int(datetime.timestamp(datetime.now()))
    comments: str
    poi_type_id: int

    class Config:
        orm_mode = True
