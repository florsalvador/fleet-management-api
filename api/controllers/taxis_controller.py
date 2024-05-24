"""..."""
from flask import jsonify
from api.models.taxis import Taxis


def select_taxis(page, limit):
    """Returns list of taxis"""
    taxis_query = Taxis.query.paginate(page=page, per_page=limit)
    response = []
    for taxi in taxis_query.items:
        taxi_info = {"id": taxi.id, "plate": taxi.plate}
        response.append(taxi_info)
    return jsonify(response)
