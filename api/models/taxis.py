"""..."""
from api.db.db import db


class Taxis(db.Model):
    """Class for table Taxis"""
    __tablename__ = "taxis"

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String())

    def __init__(self, plate):
        self.plate = plate
