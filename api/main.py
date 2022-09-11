from typing import Union

from fastapi import FastAPI

from objects.user import User

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user/create")
def create_user(user: User):
    """Collect data to create a user"""
    return {"new_user_id": user.user_id}
