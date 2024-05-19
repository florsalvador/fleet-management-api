"""..."""
from flask import Flask, request, jsonify
from models import db, Taxis

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://default:Wd1enjQ2cHyL@ep-steep-paper-a4geq4k9-pooler.us-east-1.aws.neon.tech:5432/verceldb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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



# def get_taxis():
#     """..."""
#     page = request.args.get("page", 1, type=int)
#     limit = request.args.get("limit", 20, type=int)
#     taxis_pagination = session.query(Taxis).paginate(page=page, per_page=limit, error_out=False)
#     alltaxis = []
#     for taxi in taxis_pagination.items:
#         taxi_info = {"id": taxi.id, "plate": taxi.plate}
#         alltaxis.append(taxi_info)
#     return jsonify(alltaxis)





