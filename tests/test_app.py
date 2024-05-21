""""..."""
import json
from unittest.mock import patch
from .mock_data import taxis_response


def test_get_taxis(client):
    """Test for get_taxis to verify status"""
    response = client.get("/taxis")
    assert response.status == "200 OK"


@patch("app.models.Taxis", name="mock_taxis")
def test_get_taxis_response(mock_taxis, client):
    """Test for get_taxis using a mock to verify the response"""
    mock_taxis.query.Paginate.return_value = taxis_response
    response = client.get("/taxis")
    assert response.status == "200 OK"
    assert json.loads(response.get_data()) == taxis_response


def test_get_trajectories_by_taxi(client):
    """Test for get_trajectories(taxi_id) without date"""
    response = client.get("/trajectories/7088")
    assert response.status == "200 OK"


def test_get_trajectories_with_date(client):
    """Test for get_trajectories(taxi_id) with date"""
    response = client.get("/trajectories/7088?date=2008-02-02")
    assert response.status == "200 OK"
    assert len(json.loads(response.get_data())) == 135


def test_get_last_location(client):
    """Test for get_last_location"""
    response = client.get("/trajectories/latest")
    data = json.loads(response.get_data())
    assert response.status == "200 OK"
    assert len(data) == 10
    for element in data:
        assert "plate" in element


# --------TEST_GET_TAXIS SIN MOCK

# def test_get_taxis_response(client):
#     """Test for get_taxis"""
#     response = client.get("/taxis")
#     assert response.status == "200 OK"
#     assert json.loads(response.get_data()) == taxis_response
