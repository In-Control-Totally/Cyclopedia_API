from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models
from . import user, poidef, poiactual, journey, geojson


def create_user(db: Session, user_int: user):
    db_user = models.User(f_name=user_int.f_name, l_name=user_int.l_name, email=user_int.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_all_poi_def(db: Session):
    result = db.query(models.POIType).all()
    return result


def create_poi_type(db: Session, poi_data: poidef):
    poi_definition = models.POIType(poi_type_name=poi_data.poi_type,
                                    poi_type_description=poi_data.poi_desc
                                    )
    db.add(poi_definition)
    db.commit()
    db.refresh(poi_definition)
    return poi_definition


def create_poi(db: Session, poi_actual_info: poiactual):
    poi_act = models.POI(poi_type_id=poi_actual_info.poi_type_id,
                         latitude=poi_actual_info.latitude,
                         longitude=poi_actual_info.longitude,
                         altitude=poi_actual_info.altitude,
                         timestamp=poi_actual_info.timestamp,
                         comments=poi_actual_info.comments
                         )
    db.add(poi_act)
    db.commit()
    db.refresh(poi_act)
    return poi_act


def list_all_poi(db: Session):
    return db.query(models.POI).all()


def create_journey(db: Session, new_journey: journey.JourneyUpload):
    journey_master = models.Journey(journey_start_time=new_journey.journey.journey_start_time,
                                    journey_end_time=new_journey.journey.journey_end_time,
                                    user_id=new_journey.journey.user_id
                                    )
    db.add(journey_master)
    db.commit()
    db.refresh(journey_master)
    for point in new_journey.points:
        new_point = models.JourneyPoint(journey_id=journey_master.journey_id,
                                        latitude=point.latitude,
                                        longitude=point.longitude,
                                        timestamp=point.timestamp,
                                        altitude=point.altitude
                                        )
        db.add(new_point)
    db.commit()
    return journey_master


def get_journey_by_id(db: Session, journey_id: int):
    """Instantiate a bunch of pydantic objects and then wrap them up into the master JourneyRecall object"""
    # Get the journey by its ID number from the Journey table.
    newjourney = db.query(models.Journey).filter(models.Journey.journey_id == journey_id).first()
    # Migrate the query object into the pydantic model.  the from_orm is the key part
    journey_data = journey.Journey.from_orm(newjourney)
    # Using the Journey ID, get all the data from the DB relating to the specific journey
    journey_points_db = db.query(models.JourneyPoint).filter(models.JourneyPoint.journey_id == journey_id).all()
    # Create a linestring object
    points = geojson.LineString()
    # The journey_points_db object returns lat, lon, altitude, timestamp.
    # We only need long and lat.  Iterate over each record returned and return a list of lists containing lat lon.
    # It will look like [[153.05, 27.45], [153.12, 27.35]]
    # Assign it to the coordinates attribute of the points object
    points.coordinates = [[point.longitude, point.latitude] for point in journey_points_db].copy()
    # An experiment.  I was not entirely sure what I was up to here.
    # Basically create the features object and add the points to it.
    features = geojson.Features(geometry=points)
    # Create the location object and add the features to it.  Features now includes points
    location = geojson.Location()
    location.features = features
    # Get the user data for the user who created the journey.
    usr = get_user(db, journey_data.user_id)
    # Create the JourneyRecall object that will be returned at the endpoint.
    # add the location, start, end, and user objects to it
    journey_recall = journey.JourneyRecall()
    journey_recall.journey_end_time = journey_data.journey_end_time
    journey_recall.journey_start_time = journey_data.journey_start_time
    journey_recall.location = location
    journey_recall.user = usr
    return journey_recall


def get_all_journeys(db: Session):
    """Return a list of Journey IDs"""
    return [key["journey_id"] for key in db.query(models.Journey.journey_id).all()]


def save_journey_as_track(db: Session, journey_id: int, trackname: str, rating: int, comments: str):
    saved_journey = get_journey_by_id(db, journey_id)
    new_track = models.TrackName(track_name=trackname)
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    for long, lat in saved_journey.location.features.geometry.coordinates:
        point = models.TrackData(track_id=new_track.track_id,
                                 latitude=lat,
                                 longitude=long,
                                 altitude=0,
                                 timestamp=0
                                 )
        db.add(point)
    db.commit()
    new_rating = models.TrackRating(rating=rating,
                                    comments=comments,
                                    track_id=new_track.track_id,
                                    user_id=saved_journey.user.user_id
                                    )
    db.add(new_rating)
    db.commit()


def get_all_tracks(db):
    return [key["track_id"] for key in db.query(models.TrackName.track_id).all()]


def get_tracks_in_area(db, latitude: float, longitude: float):
    """TODO: The title of this is for tracks, but it is currently set to get journeys just to get a bunch of data out.
             This is a bad idea.
             Fix this.
    """
    # First, identify all track_id's with a point +- 0.1 of a degree in lat/lon from the datum
    # 0.1 of a degree gives us a window of 22.2km in lat and lon to view on the map.
    track_ids = [key["journey_id"] for key in db.query(models.JourneyPoint.journey_id)
        .filter(models.JourneyPoint.latitude.between(latitude - 0.1, latitude + 0.1))
        .filter(models.JourneyPoint.longitude.between(longitude - 0.1, longitude + 0.1))
        .distinct()]
    # For all track_ids identified, get the geoJSON object and return it.
    # Leveraging the journey code from earlier.
    return_list = [get_journey_by_id(db, x) for x in track_ids]
    return return_list
