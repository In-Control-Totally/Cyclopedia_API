from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from db_interface.user import User
from db_interface.database import SessionLocal, engine
from db_interface.journey import JourneyUpload
from db_interface import models, crud
from db_interface.poidef import POIDef
from db_interface.poiactual import POIActual

from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost",
           "http://127.0.0.1:53657"
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.cyclopedia\.goldenrivet\.xyz",
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
    """This is a simple return to test that the API is available."""
    return {"Hello": "World"}


@app.post("/user/create")
def create_user(user: User, db: Session = Depends(get_db)):
    """Mandatory parameters are f_name, l_name and email.  user_id is created automatically."""
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
    """poi_type_id will be created automatically.  The only required parameters are poi_type and poi_desc.

    poi_type is a short name while poi_desc is a longer description of thje point of interest
    """
    return crud.create_poi_type(db, poi_data)


@app.post("/poi/create")
def create_poi_actual(poi_actual: POIActual, db: Session = Depends(get_db)):
    """When creating a POI, the poi_type_id must relate to a poi_type_id the system knows about.

    Send a GET request to /poi/show_all_types to get the list of Point Of Interest Type definitions.

    Dont supply a poi_id, one will be created for you when the poi is created
    """
    return crud.create_poi(db, poi_actual)


@app.get("/poi/list")
def list_all_poi(db: Session = Depends(get_db)):
    return crud.list_all_poi(db)


@app.post("/poi/bylocation")
def get_all_poi_in_area(lat: float, lon: float, db: Session = Depends(get_db)):
    """Returns a list of points of interest within 11km of the supplied point"""
    return crud.get_all_poi_in_area(db, lat, lon)


@app.post("/journey/create")
def create_journey(journey: JourneyUpload, db: Session = Depends(get_db)):
    """Do not supply a journey ID or a point ID when creating a journey.  The system will create these automatically"""
    return crud.create_journey(db, journey)


@app.get("/journey/{journey_id}")
def get_specific_journey(journey_id: int, db: Session = Depends(get_db)):
    """Pass a specific journey_id number to get the datapoints returned in GEOJSON"""
    return crud.get_journey_by_id(db, journey_id)


@app.get("/journey/list/")
def get_all_journeys(db: Session = Depends(get_db)):
    """Return a list of all valid journey IDs"""
    return crud.get_all_journeys(db)


@app.post("/track/savejourney/")
def save_journey_as_track(journey_id: int, name: str, rating: int, comments: str, db: Session = Depends(get_db)):
    """Pass an existing Journey_ID in, with a name, rating and comments to save as a track

    TODO: Fix so that a journey can only be added once.
    """
    return crud.save_journey_as_track(db, journey_id, name, rating, comments)


@app.get("/track/list/")
def get_all_tracks(db: Session = Depends(get_db)):
    """Return a list of valid track IDs"""
    return crud.get_all_tracks(db)


@app.post("/track/bylocation/")
def get_tracks_in_area(lat: float, lon: float, db: Session = Depends(get_db)):
    """Returns a tracks within a point within a given area in a geoJSON format"""
    return crud.get_tracks_in_area(db, lat, lon)


@app.get("/stats/tracks/ratings/")
def get_track_ratings(db: Session = Depends(get_db)):
    """List average ratings of tracks"""
    return crud.get_track_ratings(db)


@app.get("/stats/distance/")
def get_total_distance_travelled(user_id: int = 0, db: Session = Depends(get_db)):
    """Get the total distance travelled.  Supply an optional user id to get the total travelled by an individual"""
    return crud.get_total_distance_travelled(db, user_id)


@app.get("/stats/distanceranking")
def user_ranking_by_distance(db: Session = Depends(get_db)):
    """Return a list of User IDs in order of distance travelled and the distance"""
    return crud.get_user_ranking_by_distance(db)
