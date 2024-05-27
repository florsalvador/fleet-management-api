"""Model for table users"""

from api.db.db import db


class Users(db.Model):
    """Class for table users"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def create(self):
        """Adds new user to table"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates table"""
        db.session.commit()

    def delete(self):
        """Deletes user from table"""
        db.session.delete(self)
        db.session.commit()
