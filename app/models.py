"""..."""
from .db import db


class Taxis(db.Model):
    """Class for table Taxis"""
    __tablename__ = "taxis"
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String())
    def __init__(self, plate):
        self.plate = plate


class Trajectories(db.Model):
    """Class for table Trajectories"""
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


class Users(db.Model):
    """Class for table Users"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    def create(self):
        """Adds new user to table"""
        db.session.add(self)
        db.session.commit()
