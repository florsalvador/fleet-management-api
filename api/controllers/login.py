"""Module for token creation"""

from flask import jsonify
from flask_jwt_extended import create_access_token
from api.models.users import Users
from api.extensions import bcrypt


def create_token(email, password):
    """Creates authentication token"""
    user = Users.query.filter(Users.email == email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        response = {
            "accessToken": access_token,
            "user": {"id": user.id, "email": user.email}
        }
        return jsonify(response)
    return jsonify({"error": "Email or password incorrect"}), 404
