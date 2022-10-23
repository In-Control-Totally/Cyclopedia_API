from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    f_name: str
    l_name: str
    email: str
    user_id: int = None

    class Config:
        orm_mode = True


class UserDistance:
    user_id: str
    distance_travelled: float = 0.0

    def __eq__(self, other):
        return self.user_id < other.user_id

    def __lt__(self, other):
        return self.distance_travelled < other.distance_travelled
