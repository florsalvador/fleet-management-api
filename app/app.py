"""..."""
from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy import func, desc
from .models import db, Taxis, Trajectories
from .config import Config


def main():
    """..."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    # app.app_context().push()

    @app.route("/taxis", methods=["GET"])
    def get_taxis():
        """Get list of taxis"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        taxis_query = Taxis.query.paginate(page=page, per_page=limit)
        response = []
        for taxi in taxis_query.items:
            taxi_info = {"id": taxi.id, "plate": taxi.plate}
            response.append(taxi_info)
        return jsonify(response)

    @app.route("/trajectories/<int:taxi_id>", methods=["GET"])
    def get_trajectories(taxi_id):
        """Get trajectories of a taxi for a specific date"""
        date = request.args.get("date")
        date_to_use = datetime.strptime(date, "%Y-%m-%d").date()
        trajectories_query = Trajectories.query.filter(
            Trajectories.taxi_id == taxi_id, func.date(Trajectories.date) == date_to_use
        ).order_by(desc(Trajectories.id)).first()
        response = {
                "id": trajectories_query.id,
                "taxi_id": trajectories_query.taxi_id,
                "date": trajectories_query.date,
                "latitude": trajectories_query.latitude,
                "longitude": trajectories_query.longitude,
            }
        return jsonify(response)

    return app


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
