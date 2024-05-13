"""Imports flask"""
from flask import Flask, jsonify, request
from models import Taxis, session

app = Flask(__name__)

@app.route("/taxis", methods=["GET"])
def get_taxis():
    """..."""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)
    taxis = session.query(Taxis).limit(limit).offset(page*limit).all()
    alltaxis = []
    for taxi in taxis:
        taxi_info = {"id": taxi.id, "plate": taxi.plate}
        alltaxis.append(taxi_info)
    return jsonify(alltaxis)

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





