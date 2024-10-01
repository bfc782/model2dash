from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model import *
from config import models_to_load

engine = create_engine("sqlite:///intendif.db", echo=True,
                       connect_args={'check_same_thread': False})
session = Session(engine)

Base.metadata.create_all(engine)

tbl_cls_cols = {cls.__tablename__: {'object': cls, 'cols': cls.__table__.columns.keys()} \
                for cls in models_to_load}

tbl_cls_col_type = {cls.__tablename__: {'object': cls, 'cols': cls.__table__.columns.keys()} \
                for cls in models_to_load}