from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from db_interface.user import User
from db_interface.database import SessionLocal, engine
from db_interface import models, crud
from db_interface.poidef import POIDef
from db_interface.poiactual import POIActual

from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost",
           "http://127.0.0.1"
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/poi/show_all_types")
def get_all_poi_def(db: Session = Depends(get_db)):
    return crud.get_all_poi_def(db)


@app.post("/poi/create_def")
def create_poi_def(poi_data: POIDef, db: Session = Depends(get_db)):
    return crud.create_poi_type(db, poi_data)
    # return poi_data


@app.post("/poi/create")
def create_poi_actual(poi_actual: POIActual, db: Session = Depends(get_db)):
    return crud.create_poi(db, poi_actual)


@app.get("/poi/list")
def list_all_poi(db: Session = Depends(get_db)):
    return crud.list_all_poi(db)
