"""..."""
from .db import db

class Taxis(db.Model):
    """..."""
    __tablename__ = "taxis"
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String())
    def __init__(self, plate):
        self.plate = plate

class Trajectories(db.Model):
    """..."""
    __tablename__ = "trajectories"
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    def __init__(self, taxi_id, date, latitude, longitude):
        self.taxi_id = taxi_id
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
