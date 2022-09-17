from fastapi import FastAPI, Depends

from db_interface.user import User
from db_interface.database import SessionLocal, engine
from db_interface import models, crud

from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user/create")
def create_user(user: User, db: Session = Depends(get_db)):
    """Collect data to create a user"""
    # rv for return value from the crud operation
    rv = crud.create_user(db, user)
    return rv


@app.get("/user/{user_id}")
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    return db_user