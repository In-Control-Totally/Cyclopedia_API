from typing import Union
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel


class LineString(BaseModel):
    type: str = "LineString"
    coordinates: list = []


class Features(BaseModel):
    type: str = "Feature"
    properties: dict = {}
    geometry: LineString = LineString()


class Location(BaseModel):
    type: str = "FeatureCollection"
    features: List[Features] = [Features()]
