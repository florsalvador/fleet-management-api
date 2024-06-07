"""Functions for Excel files and sending emails"""

import io
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_mail import Message
from openpyxl import Workbook
from .extensions import mail


def token_required(fn):
    """Decorator to verify a valid token is present in the request"""
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return jsonify({"error": "Token is missing"}), 401
        # pylint: disable=bare-except
        except:
            return jsonify({"error": "Token is invalid or expired"}), 401
        return fn(*args, **kwargs)
    return decorator


def list_to_excel(lst):
    """Converts list to xlsx file"""
    excel = Workbook()
    active_sheet = excel.active
    row_title = list(lst[0].keys()) # ["taxi_id", "plate", "latitude", "longitude", "date"]
    active_sheet.append(row_title)
    for element in lst:
        row = list(element.values())
        active_sheet.append(row)
    buffer = io.BytesIO() # object in-memory buffer
    excel.save(buffer) # saves the excel to the buffer
    buffer.seek(0) # sets buffer's position to the beginning
    return buffer


def send_excel_email(recipient, file, file_name):
    """Sends email with excel file attached"""
    msg = Message(subject="Your Excel file", recipients=[recipient])
    msg.body = "The requested file is attached."
    msg.attach(
        f"{file_name}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        file.read(),
    )
    mail.send(msg)
    return jsonify({"msg": "The file requested has been sent"})
