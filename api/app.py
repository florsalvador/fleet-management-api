"""Routes"""

import io
# import json
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from openpyxl import Workbook
from api.db.db import db
from api.controllers.taxis_controller import select_taxis
from api.controllers.trajectories_controller import select_trajectories, select_last_location, trajectories_with_plate
from api.controllers.users_controller import new_user, select_users, modify_user, delete_user
from api.controllers.login import create_token
from .extensions import bcrypt
from .config import Config


def main():
    """Creates routes"""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app) # Initializes bcrypt with the application (before: bcrypt = Bcrypt(app))
    # pylint: disable=unused-variable
    jwt = JWTManager(app)
    mail = Mail(app)

    @app.route("/taxis", methods=["GET"])
    @jwt_required()
    def get_taxis():
        """Gets list of taxis"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_taxis(page, limit)

    @app.route("/trajectories", methods=["GET"])
    @jwt_required()
    def get_trajectories():
        """Gets all the locations of a taxi for a specific date"""
        taxi_id = request.args.get("taxiId")
        date = request.args.get("date")
        return select_trajectories(taxi_id, date)

    @app.route("/trajectories/latest", methods=["GET"])
    @jwt_required()
    def get_last_location():
        """Gets the last location of each taxi"""
        return select_last_location()

    @app.route("/users", methods=["POST"])
    @jwt_required()
    def create_user():
        """Creates a new user"""
        data = request.get_json()
        try:
            name = data["name"]
            email = data["email"]
            password = data["password"]
        except KeyError:
            return jsonify({"error": "Missing information"}), 400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        return new_user(name, email, hashed_password)

    @app.route("/users", methods=["GET"])
    @jwt_required()
    def get_users():
        """Gets list of users"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_users(page, limit)

    @app.route("/users/<uid>", methods=["PATCH"])
    @jwt_required()
    def update_user(uid):
        """Updates user's information"""
        current_user = get_jwt_identity()
        data = request.get_json()
        return modify_user(uid, current_user, data)

    @app.route("/users/<uid>", methods=["DELETE"])
    @jwt_required()
    def delete_by_id(uid):
        """Deletes user"""
        current_user = get_jwt_identity()
        return delete_user(uid, current_user)

    @app.route("/auth/login", methods=["POST"])
    def get_token():
        """Gets authentication token"""
        data = request.get_json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            return jsonify({"error": "Missing information"}), 400
        return create_token(email, password)

    @app.route("/trajectories/export", methods=["GET"])
    def export_trajectories():
        """Gets excel"""
        taxi_id = request.args.get("taxiId")
        date = request.args.get("date")
        email = request.args.get("email")
        query_list = trajectories_with_plate(taxi_id, date)
        # Convert list to xlsx
        wb = Workbook()
        ws = wb.active
        row_title = list(query_list[0].keys()) # ["taxi_id", "plate", "latitude", "longitude", "date"]
        ws.append(row_title)
        for element in query_list:
            row = list(element.values())
            ws.append(row)
        # Save the file to an in-memory buffer
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        # Send email
        msg = Message("Your Excel file is ready", sender=app.config['MAIL_USERNAME'], recipients=[email])
        # msg.body = "Please find the attached Excel file."
        msg.attach(f"locations-{taxi_id}-{date}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", output.read())
        mail.send(msg)
        return jsonify({"msg": "The file requested has been sent"})

    return app


if __name__ == "__main__":
    taxi_app = main()
    taxi_app.run()
