""""..."""
import json
# from unittest.mock import patch
from .mock_data import taxis_response


def test_get_taxis(client):
    """Test for get_taxis to verify status"""
    response = client.get("/taxis")
    assert response.status == "200 OK"


def test_get_taxis_response(client):
    """Test for get_taxis to verify that the response is correct"""
    response = client.get("/taxis")
    assert response.status == "200 OK"
    assert json.loads(response.get_data()) == taxis_response


def test_get_trajectories_by_taxi(client):
    """Test for get_trajectories(taxi_id) without date"""
    response = client.get("/trajectories/7088")
    assert response.status == "200 OK"


def test_get_trajectories_with_date(client):
    """Test for get_trajectories(taxi_id) with date to verify status and length of data"""
    response = client.get("/trajectories/7088?date=2008-02-02")
    assert response.status == "200 OK"
    assert len(json.loads(response.get_data())) == 135


def test_get_last_location(client):
    """Test for get_last_location to verify status, length of data and the existence of plate"""
    response = client.get("/trajectories/latest")
    data = json.loads(response.get_data())
    assert response.status == "200 OK"
    assert len(data) == 10
    for element in data:
        assert "plate" in element


