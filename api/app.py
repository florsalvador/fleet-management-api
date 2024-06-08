"""Routes"""

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity
from api.db.db import db
from api.controllers.taxis_controller import select_taxis
from api.controllers.trajectories_controller import (
    select_trajectories,
    select_last_location,
    trajectories_with_plate
)
from api.controllers.users_controller import new_user, select_users, modify_user, delete_user
from api.controllers.login import create_token
from .config import Config
from .extensions import bcrypt, mail
from .utils import token_required, list_to_excel, send_excel_email


def main():
    """Creates routes"""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app) # Initializes bcrypt (before: bcrypt = Bcrypt(app))
    mail.init_app(app) # Initializes flask-mail
    # pylint: disable=unused-variable
    jwt = JWTManager(app)

    @app.route("/taxis", methods=["GET"])
    @token_required
    def get_taxis():
        """Gets list of taxis"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_taxis(page, limit)

    @app.route("/trajectories", methods=["GET"])
    @token_required
    def get_trajectories():
        """Gets all the locations of a taxi for a specific date"""
        taxi_id = request.args.get("taxiId")
        date = request.args.get("date")
        return select_trajectories(taxi_id, date)

    @app.route("/trajectories/latest", methods=["GET"])
    @token_required
    def get_last_location():
        """Gets the last location of each taxi"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_last_location(page, limit)

    @app.route("/users", methods=["POST"])
    @token_required
    def create_user():
        """Creates a new user"""
        data = request.get_json()
        try:
            name = data["name"]
            email = data["email"]
            password = data["password"]
        except KeyError:
            return jsonify({"error": "Missing information"}), 400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        return new_user(name, email, hashed_password)

    @app.route("/users", methods=["GET"])
    @token_required
    def get_users():
        """Gets list of users"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_users(page, limit)

    @app.route("/users/<uid>", methods=["PATCH"])
    @token_required
    def update_user(uid):
        """Updates user's information"""
        current_user = get_jwt_identity()
        data = request.get_json()
        return modify_user(uid, current_user, data)

    @app.route("/users/<uid>", methods=["DELETE"])
    @token_required
    def delete_by_id(uid):
        """Deletes user"""
        current_user = get_jwt_identity()
        return delete_user(uid, current_user)

    @app.route("/auth/login", methods=["POST"])
    def get_token():
        """Gets authentication token"""
        data = request.get_json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            return jsonify({"error": "Missing information"}), 400
        return create_token(email, password)

    @app.route("/trajectories/export", methods=["GET"])
    @token_required
    def export_trajectories():
        """Gets excel file with the locations of a taxi and sends it via email"""
        taxi_id = request.args.get("taxiId")
        date = request.args.get("date")
        email = request.args.get("email")
        if not taxi_id or not date or not email:
            return jsonify({"error": "Missing parameters"}), 400
        query_list = trajectories_with_plate(taxi_id, date)
        excel_file = list_to_excel(query_list)
        return send_excel_email(email, excel_file, f"locations-{taxi_id}-{date}")

    return app


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
