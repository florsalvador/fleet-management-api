"""..."""
from datetime import datetime
from flask import jsonify
from sqlalchemy import func
from .db import db
from .models import Taxis, Trajectories


def select_taxis(page, limit):
    """Returns list of taxis"""
    taxis_query = Taxis.query.paginate(page=page, per_page=limit)
    response = []
    for taxi in taxis_query.items:
        taxi_info = {"id": taxi.id, "plate": taxi.plate}
        response.append(taxi_info)
    return jsonify(response)


def select_trajectories(taxi_id, date):
    """Returns all the locations of a taxi for a specific date"""
    if date:
        date_to_use = datetime.strptime(date, "%Y-%m-%d").date()
        trajectories_query = Trajectories.query.filter(Trajectories.taxi_id == taxi_id, func.date(Trajectories.date) == date_to_use).all()
    else:
        trajectories_query = Trajectories.query.filter(Trajectories.taxi_id == taxi_id).all()
    response = []
    for t in trajectories_query:
        trajectory = {
            "id": t.id,
            "taxi_id": t.taxi_id,
            "date": t.date,
            "latitude": t.latitude,
            "longitude": t.longitude,
        }
        response.append(trajectory)
    return jsonify(response)


def select_last_location():
    """Returns the last location of each taxi"""
    last_date_subquery = db.session.query(Trajectories.taxi_id, db.func.max(Trajectories.id).label("max_id")).group_by(Trajectories.taxi_id).subquery()
    last_location_query = db.session.query(Trajectories, Taxis).join(last_date_subquery, Trajectories.id == last_date_subquery.c.max_id).join(Taxis, Trajectories.taxi_id == Taxis.id).all()
    response = []
    for element in last_location_query: # element = (Trajectories(id=3, taxi_id=101, date=datetime(2008, 2, 2), latitude=40.7306, longitude=-73.9352), Taxis(id=101, plate='ABC-123'))
        trajectory = element[0]  # Trajectories object
        taxi = element[1]  # Taxis object
        last_location = {
            "taxi_id": trajectory.taxi_id,
            "plate": taxi.plate,
            "date": trajectory.date,
            "latitude": trajectory.latitude,
            "longitude": trajectory.longitude,
        }
        response.append(last_location)
    return jsonify(response)
