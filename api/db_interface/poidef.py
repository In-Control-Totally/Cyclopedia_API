from pydantic import BaseModel


class POIDef(BaseModel):
    poi_type: str
    poi_desc: str
    poi_type_id: int = None

    class Config:
        orm_mode = True
