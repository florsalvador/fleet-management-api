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
    file = io.BytesIO() # Save the file to an in-memory buffer
    wb.save(file)
    file.seek(0)
    return file


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
