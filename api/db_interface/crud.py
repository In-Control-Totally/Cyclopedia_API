from sqlalchemy.orm import Session

from . import models
from . import user, poidef, poiactual, journey


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
