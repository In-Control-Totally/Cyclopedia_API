from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "USER_INFO"

    user_id = Column(Integer, primary_key=True)
    f_name = Column(String)
    l_name = Column(String)
    email = Column(String)
    creation_dt = Column(String, server_default=FetchedValue())

