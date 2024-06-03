"""Tests for app.py"""

import json
from unittest.mock import patch
from .mock_data import (
    taxis_response,
    locations_response,
    last_location_response,
    new_user_response,
    users_response,
    create_token_response
)


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.select_taxis", name="mock_select_taxis", return_value=taxis_response)
def test_get_taxis(mock_select_taxis, mock_jwt_required, client):
    """Test for get_taxis using a mock to verify the response"""
    response = client.get("/taxis")
    assert response.status_code == 200
    assert mock_select_taxis.called
    assert mock_jwt_required.called
    assert json.loads(response.get_data()) == taxis_response


def test_get_taxis_no_token(client):
    """Test for get_taxis to verify it returns a 401 error when unauthorized"""
    response = client.get("/taxis")
    assert response.status_code == 401


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.select_trajectories",
    name="mock_select_trajectories",
    return_value=locations_response)
def test_get_trajectories_by_taxi(mock_select_trajectories, mock_jwt_required, client):
    """Test for get_trajectories without date"""
    response = client.get("/trajectories?taxiId=6418")
    assert response.status_code == 200
    assert mock_select_trajectories.call_args.args == ("6418", None)
    assert mock_jwt_required.called
    assert json.loads(response.get_data()) == locations_response


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.select_trajectories",
    name="mock_select_trajectories",
    return_value=locations_response)
def test_get_trajectories_with_date(mock_select_trajectories, mock_jwt_required, client):
    """Test for get_trajectories with date to verify status and length of data"""
    response = client.get("/trajectories?taxiId=6418&date=2008-02-02")
    assert response.status_code == 200
    assert mock_select_trajectories.call_args.args == ("6418", "2008-02-02")
    assert mock_jwt_required.called
    assert len(json.loads(response.get_data())) == 3


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.select_last_location",
    name="mock_select_last_location",
    return_value=last_location_response)
def test_get_last_location(mock_select_last_location, mock_jwt_required, client):
    """Test for get_last_location to verify status, length of data and the existence of plate"""
    response = client.get("/trajectories/latest")
    data = json.loads(response.get_data())
    assert response.status_code == 200
    assert mock_select_last_location.called
    assert mock_jwt_required.called
    assert len(data) == 2
    for element in data:
        assert "plate" in element


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.new_user", name="mock_new_user", return_value=new_user_response)
def test_create_user(mock_new_user, mock_jwt_required, client):
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
    assert mock_jwt_required.called
    assert json.loads(response.get_data()) == new_user_response


def test_create_user_no_token(client):
    """Test for create_user to verify it returns a 401 error when unauthorized"""
    response = client.post(
        "/users",
        json={
            "name": "Grace Hopper",
            "email": "grace.hopper@systers.xyz",
            "password": "9XXLqVhq3vw9yjNt"
        }
    )
    assert response.status_code == 401


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
def test_create_user_missing_info(mock_jwt_required, client):
    """Test for create_user to verify it returns a 400 error when missing info"""
    response = client.post(
        "/users",
        json={
            "name": "Grace Hopper",
            "email": "grace.hopper@systers.xyz"
        }
    )
    assert mock_jwt_required.called
    assert response.status_code == 400


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.select_users", name="mock_select_users", return_value=users_response)
def test_get_users(mock_select_users, mock_jwt_required, client):
    """Test for get_users"""
    response = client.get("/users")
    assert response.status_code == 200
    assert mock_select_users.call_args.args == (1, 10)
    assert mock_jwt_required.called


def test_update_user(client):
    """Test for update_user to verify it returns a 401 error when unauthorized"""
    response = client.patch(
        "/users/15254",
        json={
            "email": "grace.hopper@email.com"
        }
    )
    assert response.status_code == 401


def test_delete_by_id(client):
    """Test for delete_by_id to verify it returns a 401 error when unauthorized"""
    response = client.delete("/users/15254")
    assert response.status_code == 401


@patch("api.app.create_token", name="mock_create_token", return_value=create_token_response)
def test_get_token(mock_create_token, client):
    """Test for get_token"""
    response = client.post(
        "/auth/login",
        json={
            "email": "anita.borg@systers.xyz",
            "password": "XLqVhq3vw9yj"
        }
    )
    assert response.status_code == 200
    assert mock_create_token.called
    assert json.loads(response.get_data()) == create_token_response


def test_get_token_missing_info(client):
    """Test for get_token to verify that both email and password are present in the request"""
    response = client.post(
        "/auth/login",
        json={
            "email": "anita.borg@systers.xyz"
        }
    )
    assert response.status_code == 400


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
@patch("api.app.send_excel_email", name="mock_send_excel_email", return_value={"msg": "The file requested has been sent"})
def test_export_trajectories(mock_send_excel_email, mock_jwt_required, client):
    """Test for export_trajectories"""
    response = client.get("/trajectories/export?taxiId=7088&date=2008-02-02&email=example@gmail.com")
    assert mock_send_excel_email.called
    assert mock_jwt_required.called
    assert response.status_code == 200


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", name="mock_jwt_required")
def test_export_trajectories_missing_params(mock_jwt_required, client):
    """Test for export_trajectories to verify that the required parameteres are present"""
    response = client.get("/trajectories/export")
    assert mock_jwt_required.called
    assert response.status_code == 400


def test_export_trajectories_no_token(client):
    """Test for export_trajectories to verify it returns a 401 error when unauthorized"""
    response = client.get("/trajectories/export?taxiId=7088&date=2008-02-02&email=example@gmail.com")
    assert response.status_code == 401
