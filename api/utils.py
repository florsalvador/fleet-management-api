"""Functions for Excel files and sending emails"""

import io
from flask import jsonify
from flask_mail import Message
from openpyxl import Workbook
from .extensions import mail


def list_to_excel(lst):
    """Converts list to xlsx file"""
    wb = Workbook()
    ws = wb.active
    row_title = list(lst[0].keys()) # ["taxi_id", "plate", "latitude", "longitude", "date"]
    ws.append(row_title)
    for element in lst:
        row = list(element.values())
        ws.append(row)
    # Save the file to an in-memory buffer
    file = io.BytesIO()
    wb.save(file)
    file.seek(0)
    return file


def send_excel_email(recipient, file, file_name):
    """Sends email with excel file attached"""
    msg = Message("Your Excel file", recipients=[recipient])
    msg.body = "Please find the attached Excel file."
    msg.attach(
        f"{file_name}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        file.read(),
    )
    mail.send(msg)
    return jsonify({"msg": "The file requested has been sent"})
