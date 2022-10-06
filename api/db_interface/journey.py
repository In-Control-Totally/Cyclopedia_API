from typing import Union
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .user import User
from .geojson import Location


class Journey(BaseModel):
    journey_id: int = None
    user_id: int
    journey_start_time: int
    journey_end_time: int

    class Config:
        orm_mode = True


class JourneyPoint(BaseModel):
    point_id: int = None
    journey_id: int = None
    latitude: float
    longitude: float
    timestamp: int
    altitude: int

    class Config:
        orm_mode = True


class JourneyUpload(BaseModel):
    journey: Journey
    points: List[JourneyPoint]

    class Config:
        orm_mode = True


class JourneyRecall(BaseModel):
    user: User = None
    location: Location = Location()
    journey_start_time: int = 0
    journey_end_time: int = 0

    class Config:
        orm_mode = True
