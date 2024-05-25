"""..."""
from api.db.db import db


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

    def update(self):
        """Updates table"""
        db.session.commit()
