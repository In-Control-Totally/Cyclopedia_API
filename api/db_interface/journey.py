from haversine import haversine

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

    @property
    def distance_travelled(self):
        """Return the distance of the entire journey in Kilometers"""
        # Set starting distance at 0
        distance = 0.0
        # Make sure that there is enough points to calculate a distance between
        if len(self.location.features.geometry.coordinates) > 1:
            # Range - 1 is because we are always calculating between two points.
            # Prevents a out of range exception
            for point_idx in range(0, len(self.location.features.geometry.coordinates) - 1):
                # Build a tuple of the two points that we need to measure
                two_points = (self._invert_coords(self.location.features.geometry.coordinates[point_idx]),
                              self._invert_coords(self.location.features.geometry.coordinates[point_idx + 1])
                              )
                # Calculate the distance between the two points and add it to the total distance
                # Using the * unpacks the lat/lon tuple into the two arguments for us automatically
                distance += haversine(*two_points)
        return distance

    def _invert_coords(self, points):
        """Quick and dirty invert the order of the two points because I recorded as lon/lat instead of lat/lon

        I am not proud of this.  A better approach would have been to adjust everything to conform to the accepted order
        """
        return points[1], points[0]

    class Config:
        orm_mode = True
