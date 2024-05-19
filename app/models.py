"""..."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Taxis(db.Model):
    """..."""
    __tablename__ = "taxis"
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String())
    def __init__(self, plate):
        self.plate = plate
