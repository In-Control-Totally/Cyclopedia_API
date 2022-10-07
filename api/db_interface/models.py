from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "USER_INFO"

    user_id = Column(Integer, primary_key=True)
    f_name = Column(String)
    l_name = Column(String)
    email = Column(String)
    # FetchedValue allows the class to instantiate without that value.  You need this for the INSERT operation
    # In the database, the creation_dt is generated automatically on INSERT
    creation_dt = Column(String, server_default=FetchedValue())


class POIType(Base):
    __tablename__ = "POINT_OF_INTEREST_TYPE"

    poi_type_id = Column(Integer, primary_key=True)
    poi_type_name = Column(String)
    poi_type_description = Column(String)


class POI(Base):
    __tablename__ = "POINT_OF_INTEREST"

    poi_id = Column(Integer, primary_key=True)
    poi_type_id = Column(Integer, ForeignKey("POINT_OF_INTEREST_TYPE.poi_type_id"))
    latitude = Column(String)
    longitude = Column(String)
    altitude = Column(String)
    timestamp = Column(String, server_default=FetchedValue())
    comments = Column(String)


class Journey(Base):
    __tablename__ = "JOURNEY"

    journey_id = Column(Integer, primary_key=True)
    journey_start_time = Column(Integer)
    journey_end_time = Column(Integer)
    user_id = Column(Integer, ForeignKey("USER_INFO.user_id"))


class JourneyPoint(Base):
    __tablename__ = "JOURNEY_POINT"

    point_id = Column(Integer, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)
    timestamp = Column(String)
    altitude = Column(String)
    journey_id = Column(Integer, ForeignKey("JOURNEY.journey_id"))


class TrackName(Base):
    # Relates to the actual table name in the database
    __tablename__ = "TRACK_NAME"
    # define the track_id attribute in this class as a Column object that contains Integers and is the Primary Key
    track_id = Column(Integer, primary_key=True)
    # Track names are recorded as a string type
    track_name = Column(String)


class TrackData(Base):
    __tablename__ = "TRACK_DATA"

    point_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey("TRACK_NAME.track_id"))
    timestamp = Column(Integer)
    # Experiment with float types
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Integer)


class TrackRating(Base):
    __tablename__ = "TRACK_RATING"
    rating_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey("TRACK_NAME.track_id"))
    user_id = Column(Integer, ForeignKey("USER_INFO.user_id"))
    rating = Column(Integer)
    comments = Column(String)
