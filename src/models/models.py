from sqlalchemy import Column, Integer, DateTime
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GPSData(Base):
    """
    Модель данных для хранения информации о GPS-данных в базе данных.
    """
    __tablename__ = 'GPS'

    id = Column(Integer, primary_key=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    speed = Column(Integer)
    gps_time = Column(DateTime)
    vehicle_id = Column(Integer)
