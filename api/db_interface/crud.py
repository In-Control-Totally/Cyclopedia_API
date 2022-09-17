from sqlalchemy.orm import Session

from . import models
from . import user


def create_user(db: Session, user_int: user):
    db_user = models.User(f_name=user_int.f_name, l_name=user_int.l_name, email=user_int.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()
