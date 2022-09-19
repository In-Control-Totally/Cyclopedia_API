from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class POI(BaseModel):
    poi_type: str
    poi_desc: str
    poi_id: int = None

    class Config:
        orm_mode = True
