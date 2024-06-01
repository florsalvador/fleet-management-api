"""Module controller for table trajectories"""
# import sys
from datetime import datetime
from flask import jsonify
from sqlalchemy import func
from api.db.db import db
from api.models.taxis import Taxis
from api.models.trajectories import Trajectories


def select_trajectories(taxi_id, date):
    """Returns all the locations of a taxi for a specific date"""
    if date:
        try:
            date_to_use = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return "<h1>Error</h1><p>Date entered does not match format YYYY-MM-DD. Try again.</p>"
        trajectories_query = Trajectories.query.filter(
            Trajectories.taxi_id == taxi_id, func.date(Trajectories.date) == date_to_use
        ).all()
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


def trajectories_with_plate(taxi_id, date):
    """Returns list with all the locations of a taxi for a specific date (including plates)"""
    try:
        date_to_use = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return "<h1>Error</h1><p>Date entered does not match format YYYY-MM-DD. Try again.</p>"
    trajectories_query = (
        db.session.query(Trajectories, Taxis)
        .filter(Trajectories.taxi_id == taxi_id, func.date(Trajectories.date) == date_to_use)
        .join(Taxis, Trajectories.taxi_id == Taxis.id)
        .all()
    )
    response = []
    for element in trajectories_query:
        trajectory = element[0]  # Trajectories object
        taxi = element[1]  # Taxis object
        locations = {
            "taxi_id": trajectory.taxi_id,
            "plate": taxi.plate,
            "latitude": trajectory.latitude,
            "longitude": trajectory.longitude,
            "date": trajectory.date
        }
        response.append(locations)
    return response


#     return send_file(output, download_name="file_ready.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#     file_name = f"locations-{taxi_id}-{date}.xlsx"

#     # print(response, file=sys.stderr)
#     wb = Workbook()
#     ws = wb.active
#     row_1 = ["taxi_id", "plate", "latitude", "longitude", "date"]
#     ws.append(row_1)
#     for r in response:
#         row = list(r.values())
#         ws.append(row)
#     # Save the file to an in-memory buffer
#     output = io.BytesIO()
#     wb.save(output)
#     output.seek(0)
#     file_name = f"locations-{taxi_id}-{date}.xlsx"
#     return send_file(output, as_attachment=True, download_name=file_name, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
