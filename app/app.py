"""Imports flask"""
from flask import Flask

app = Flask(__name__)

@app.route("/taxis", methods=["GET"])
def hello_world():
    """"..."""
    return "<p>Hello, World!</p>"
