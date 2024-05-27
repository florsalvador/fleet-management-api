"""Model for table trajectories"""

from api.db.db import db


class Trajectories(db.Model):
    """Class for table trajectories"""
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
