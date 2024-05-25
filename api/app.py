"""Imports"""
from flask import Flask, request, jsonify
from api.db.db import db
from api.controllers.taxis_controller import select_taxis
from api.controllers.trajectories_controller import select_trajectories, select_last_location
from api.controllers.users_controller import new_user, select_users, modify_user
from .config import Config


def main():
    """Creates routes"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

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
        return new_user(name, email, password)

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

    return app


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
