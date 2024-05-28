"""Module controller for table users"""

from flask import jsonify
from api.models.users import Users


def new_user(name, email, password, role):
    """"Adds new user to table users and returns user's information"""
    if not email or not password:
        return jsonify({"error": "Email or password not provided"}), 400
    if Users.query.filter(Users.email == email).first():
        return jsonify({"error": "Email already exists"}), 409
    user = Users(name, email, password, role)
    user.create()
    response = {"id": user.id, "name": user.name, "email": user.email}
    return jsonify(response)


def select_users(page, limit):
    """Returns list of users"""
    users_query = Users.query.paginate(page=page, per_page=limit)
    response = []
    for user in users_query.items:
        user_info = {"id": user.id, "name": user.name, "email": user.email}
        response.append(user_info)
    return jsonify(response)


def modify_user(uid, data):
    """Modifies user's information and returns the new data"""
    if "@" in uid:
        user = Users.query.filter(Users.email == uid).first()
    else:
        user = Users.query.filter(Users.id == uid).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]
    user.update()
    response = {"id": user.id, "name": user.name, "email": user.email}
    return jsonify(response)


def delete_user(uid):
    """Deletes user and returns deleted user's information"""
    if "@" in uid:
        user = Users.query.filter(Users.email == uid).first()
    else:
        user = Users.query.filter(Users.id == uid).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404
    response = {"id": user.id, "name": user.name, "email": user.email}
    user.delete()
    return jsonify(response)
