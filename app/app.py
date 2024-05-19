"""..."""
from flask import Flask, request, jsonify
from models import db, Taxis
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/taxis", methods=["GET"])
def get_taxis():
    """..."""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    taxis_query = Taxis.query.paginate(page=page, per_page=limit)
    taxis = []
    for taxi in taxis_query.items:
        taxi_info = {"id": taxi.id, "plate": taxi.plate}
        taxis.append(taxi_info)
    return jsonify(taxis)

if __name__ == '__main__':
    app.run(debug=True)
