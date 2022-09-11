from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    f_name: str
    l_name: str
    email: str
    user_id: int = None
