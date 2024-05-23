"""Imports"""
from flask import Flask, request
from .db import db
from .controllers import select_taxis, select_trajectories, select_last_location
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

    return app


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
