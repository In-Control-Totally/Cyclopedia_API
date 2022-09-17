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
    crud.create_user(Depends(get_db), user)
    return {"new_user_id": user.user_id}

@app.get("/user/{user_id}")
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    return db_user