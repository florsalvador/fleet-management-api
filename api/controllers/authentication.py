"""Module for token creation"""

from flask import jsonify
from flask_jwt_extended import create_access_token
from api.models.users import Users


def create_token(email, password):
    """Creates authentication token"""
    admin = Users.query.filter(Users.email == "flor@email.com").first()
    if admin.email == email and admin.password == password:
        access_token = create_access_token(identity=admin.id)
        response = {
            "accessToken": access_token,
            "user": {"id": admin.id, "email": admin.email, "role": "admin"}
        }
        return jsonify(response)
    return jsonify({"error": "Email or password incorrect"}), 404
