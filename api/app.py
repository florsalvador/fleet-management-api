"""Routes"""

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from api.db.db import db
from api.controllers.taxis_controller import select_taxis
from api.controllers.trajectories_controller import select_trajectories, select_last_location
from api.controllers.users_controller import new_user, select_users, modify_user, delete_user
from api.controllers.authentication import create_token
from .config import Config


def main():
    """Creates routes"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "ansfalfgnlkn4636" # Change
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)

    @app.route("/taxis", methods=["GET"])
    def get_taxis():
        """Gets list of taxis"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_taxis(page, limit)

    @app.route("/trajectories", methods=["GET"])
    def get_trajectories():
        """Gets all the locations of a taxi for a specific date"""
        taxi_id = request.args.get("taxiId")
        date = request.args.get("date")
        return select_trajectories(taxi_id, date)

    @app.route("/trajectories/latest", methods=["GET"])
    def get_last_location():
        """Gets the last location of each taxi"""
        return select_last_location()

    @app.route("/users", methods=["POST"])
    def create_user():
        """Creates a new user"""
        data = request.get_json()
        try:
            name = data["name"]
            email = data["email"]
            password = data["password"]
        except KeyError:
            return jsonify({"error": "Missing information"}), 400
        role = "user" if not "role" in data else data["role"]
        return new_user(name, email, password, role)

    @app.route("/users", methods=["GET"]) # PROTECTED ENDPOINT
    # @jwt_required()
    def get_users():
        """Gets list of users"""
        # current_user = get_jwt_identity()
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_users(page, limit)

    @app.route("/users/<uid>", methods=["PATCH"])
    def update_user(uid):
        """Updates user's information"""
        data = request.get_json()
        return modify_user(uid, data)

    @app.route("/users/<uid>", methods=["DELETE"])
    def delete_by_id(uid):
        """Deletes user"""
        return delete_user(uid)

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

    return app


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
