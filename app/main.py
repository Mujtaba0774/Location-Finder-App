from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import sessionmaker
from models import Location, engine

app = FastAPI()

Session = sessionmaker(bind=engine)

class LocationRequest(BaseModel):
    name: str
    latitude: float
    longitude: float

@app.post("/locations/")
async def create_location(location: LocationRequest):
    session = Session()
    new_location = Location(name=location.name, latitude=location.latitude, longitude=location.longitude, geometry=f'SRID=4326;POINT({location.longitude} {location.latitude})')
    session.add(new_location)
    session.commit()
    return JSONResponse(content={"message": "Location created successfully"}, media_type="application/json")

@app.get("/locations/")
async def read_locations():
    session = Session()
    locations = session.query(Location).all()
    return JSONResponse(content=[location.dict() for location in locations], media_type="application/json")

@app.get("/locations/{location_id}")
async def read_location(location_id: int):
    session = Session()
    location = session.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return JSONResponse(content=location.dict(), media_type="application/json")

@app.get("/locations/nearby/")
async def read_locations_nearby(latitude: float, longitude: float):
    session = Session()
    locations = session.query(Location).filter(Location.geometry.distance(f'SRID=4326;POINT({longitude} {latitude})') < 1000).all()
    return JSONResponse(content=[location.dict() for location in locations], media_type="application/json")

@app.get("/locations/bbox/")
async def read_locations_bbox(sw_latitude: float, sw_longitude: float, ne_latitude: float, ne_longitude: float):
    session = Session()
    locations = session.query(Location).filter(Location.geometry.within(f'SRID=4326;BOX2D({sw_longitude} {sw_latitude}, {ne_longitude} {ne_latitude})')).all()
    return JSONResponse(content=[location.dict() for location in locations], media_type="application/json")

@app.put("/locations/{location_id}")
async def update_location(location_id: int, location: LocationRequest):
    session = Session()
    location_db = session.query(Location).filter(Location.id == location_id).first()
    if location_db is None:
        raise HTTPException(status_code=404, detail="Location not found")
    location_db.name = location.name
    location_db.latitude = location.latitude
    location_db.longitude = location.longitude
    location_db.geometry = f'SRID=4326;POINT({location.longitude} {location.latitude})'
    session.commit()
    return JSONResponse(content={"message": "Location updated successfully"}, media_type="application/json")

@app.delete("/locations/{location_id}")
async def delete_location(location_id: int):
    session = Session()
    location_db = session.query(Location).filter(Location.id == location_id).first()
    if location_db is None:
        raise HTTPException(status_code=404, detail="Location not found")
    session.delete(location_db)
    session.commit()
    return JSONResponse(content={"message": "Location deleted successfully"}, media_type="application/json")