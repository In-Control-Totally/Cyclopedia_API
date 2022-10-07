from typing import Union
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from .user import User
from .geojson import Location


class TrackData(BaseModel):
    point_id: int = None
    timestamp: int = 0
    latitude: float
    longitude: float
    altitude: float


class Track(BaseModel):
    track_id: int = None
    track_name: str


class TrackRating(BaseModel):
    rating_id: int = None
    track_id: int
    user_id: int
    rating: int
    comments: str
