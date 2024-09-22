from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from geoalchemy2 import Geometry

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    geometry = Column(Geometry('POINT', 4326))

engine = create_engine('postgresql://user:password@host:port/location_finder')
Base.metadata.create_all(engine)