"""Routes"""

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
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

    @app.route("/users", methods=["GET"])
    def get_users():
        """Gets list of users"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_users(page, limit)

    @app.route("/users/<int:user_id>", methods=["PATCH"])
    def update_user(user_id):
        """Updates user's information"""
        data = request.get_json()
        return modify_user(user_id, data)

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_by_id(user_id):
        """Deletes user"""
        return delete_user(user_id)

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
