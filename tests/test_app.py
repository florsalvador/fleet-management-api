"""Tests for app.py"""

import json
from unittest.mock import patch
from .mock_data import (
    taxis_response,
    locations_response,
    last_location_response,
    new_user_response,
    users_response,
    update_user_response
)


@patch("api.app.select_taxis", name="mock_select_taxis", return_value=taxis_response)
def test_get_taxis_response(mock_select_taxis, client):
    """Test for get_taxis using a mock to verify the response"""
    response = client.get("/taxis")
    assert response.status_code == 200
    assert mock_select_taxis.called
    assert json.loads(response.get_data()) == taxis_response


@patch("api.app.select_trajectories",
    name="mock_select_trajectories",
    return_value=locations_response)
def test_get_trajectories_by_taxi(mock_select_trajectories, client):
    """Test for get_trajectories without date"""
    response = client.get("/trajectories?taxiId=6418")
    assert response.status_code == 200
    assert mock_select_trajectories.call_args.args == ("6418", None)
    assert json.loads(response.get_data()) == locations_response


@patch("api.app.select_trajectories",
    name="mock_select_trajectories",
    return_value=locations_response)
def test_get_trajectories_with_date(mock_select_trajectories, client):
    """Test for get_trajectories with date to verify status and length of data"""
    response = client.get("/trajectories?taxiId=6418&date=2008-02-02")
    assert response.status_code == 200
    assert mock_select_trajectories.call_args.args == ("6418", "2008-02-02")
    assert len(json.loads(response.get_data())) == 3


@patch("api.app.select_last_location",
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


@patch("api.app.new_user", name="mock_new_user", return_value=new_user_response)
def test_create_user(mock_new_user, client):
    """Test for create_user"""
    response = client.post(
        "/users",
        json={
            "name": "Grace Hopper",
            "email": "grace.hopper@systers.xyz",
            "password": "9XXLqVhq3vw9yjNt"
        }
    )
    assert response.status_code == 200
    assert mock_new_user.called
    assert json.loads(response.get_data()) == new_user_response


# @patch("api.app.new_user", name="mock_new_user", return_value=new_user_response)
def test_create_user_error(client):
    """Test for create_user to verify name, email and password are present in the request body"""
    response = client.post(
        "/users",
        json={
            "name": "Grace Hopper",
            "email": "grace.hopper@systers.xyz"
        }
    )
    assert response.status_code == 400
    # assert mock_new_user.called


@patch("api.app.select_users", name="mock_select_users", return_value=users_response)
def test_get_users(mock_select_users, client):
    """Test for get_users"""
    response = client.get("/users")
    assert response.status_code == 200
    assert mock_select_users.call_args.args == (1, 10)


@patch("api.app.modify_user", name="mock_modify_user", return_value=update_user_response)
def test_update_user(mock_modify_user, client):
    """Test for update_user"""
    response = client.patch(
        "/users/15254",
        json={
            "email": "grace.hopper@email.com"
        }
    )
    assert response.status_code == 200
    assert mock_modify_user.called
    assert json.loads(response.get_data()) == update_user_response


@patch("api.app.delete_user", name="mock_delete_user", return_value=update_user_response)
def test_delete_by_id(mock_delete_user, client):
    """Test for delete_by_id"""
    response = client.delete("/users/15254")
    assert response.status_code == 200
    assert mock_delete_user.called
