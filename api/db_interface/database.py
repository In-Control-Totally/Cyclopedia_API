import os
from . import temp_configs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"""mysql+pymysql://{os.environ.get("sql_user")}:{os.environ.get('sql_pass')}""" \
                          f"""@{os.environ.get('sql_host')}:{os.environ.get('sql_port')}/{os.environ.get('sql_db')}"""

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

