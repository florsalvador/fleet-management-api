""""..."""
import json
from unittest.mock import patch
from .mock_data import taxis_response, locations_response, last_location_response


@patch("app.app.select_taxis",
       name="mock_select_taxis",
       return_value=taxis_response)
def test_get_taxis_response(mock_select_taxis, client):
    """Test for get_taxis using a mock to verify the response"""
    response = client.get("/taxis")
    assert response.status_code == 200
    assert mock_select_taxis.called
    assert json.loads(response.get_data()) == taxis_response


@patch("app.app.select_trajectories",
       name="mock_select_trajectories",
       return_value=locations_response)
def test_get_trajectories_by_taxi(mock_select_trajectories, client):
    """Test for get_trajectories(taxi_id) without date"""
    response = client.get("/trajectories?taxiId=6418")
    assert response.status_code == 200
    assert mock_select_trajectories.call_args.args == ("6418", None)
    assert json.loads(response.get_data()) == locations_response


@patch("app.app.select_trajectories",
       name="mock_select_trajectories",
       return_value=locations_response)
def test_get_trajectories_with_date(mock_select_trajectories, client):
    """Test for get_trajectories(taxi_id) with date to verify status and length of data"""
    response = client.get("/trajectories?taxiId=6418&date=2008-02-02")
    assert response.status_code == 200
    assert mock_select_trajectories.call_args.args == ("6418", "2008-02-02")
    assert len(json.loads(response.get_data())) == 3


@patch("app.app.select_last_location",
       name="mock_select_last_location",
       return_value=last_location_response)
def test_get_last_location(mock_select_last_location, client):
    """Test for get_last_location to verify status, length of data and the existence of plate"""
    response = client.get("/trajectories/latest")
    data = json.loads(response.get_data())
    assert response.status_code == 200
    assert mock_select_last_location.called
    assert len(data) == 2
    for element in data:
        assert "plate" in element
