"""..."""
from flask import Flask, request, jsonify
from .models import db, Taxis
from .config import Config


def main():
    """..."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    # app.app_context().push()

    @app.route("/taxis", methods=["GET"])
    def get_taxis():
        """..."""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        taxis_query = Taxis.query.paginate(page=page, per_page=limit)
        response = []
        for taxi in taxis_query.items:
            taxi_info = {"id": taxi.id, "plate": taxi.plate}
            response.append(taxi_info)
        return jsonify(response)
    
    return app

    # @app.route("/trajectories/<taxi_id>", methods=["GET"])
    # def get_trajectories(taxi_id):
    #     """..."""
    #     date = datetime(year=datetime.now().year, month=datetime.now().month, day=1)
    #     date = request.args.get("date")
    #     trajectories_query = Trajectories.query.filter(
    #         Trajectories.taxi_id == taxi_id, Trajectories.date == date
    #     ).all()
    #     response = []
    #     for t in trajectories_query.items:
    #         trajectory = {
    #             "id": t.id,
    #             "taxi_id": t.taxi_id,
    #             "date": t.date,
    #             "latitude": t.latitude,
    #             "longitude": t.longitude,
    #         }
    #         response.append(trajectory)
    #     return jsonify(response)


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
