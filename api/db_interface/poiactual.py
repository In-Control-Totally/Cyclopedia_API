from pydantic import BaseModel


class POIActual(BaseModel):
    # use "= None" to mark this as optional for instantiation
    poi_id: int = None
    latitude: float
    longitude: float
    altitude: int
    # TODO: transmit timestamp of transaction
    timestamp: int = 1
    comments: str
    poi_type_id: int

    class Config:
        orm_mode = True
