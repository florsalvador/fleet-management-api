""""..."""
import json
from .mock_data import taxis_response


def test_get_taxis(client):
    """..."""
    response = client.get("/taxis")
    assert response.status == "200 OK"


def test_get_taxis_response(client):
    """..."""
    response = client.get("/taxis")
    print(response.data)
    assert response.status == "200 OK"
    assert json.loads(response.get_data()) == taxis_response



# NO FUNCIONA EL PATCH PARA SIMULAR LA RESPUESTA DE QUERY.PAGINATE:
# from unittest.mock import patch
# @patch("app.app.Taxis.query.paginate", name="mock_get_taxis")
# def test_get_taxis_response(mock_get_taxis, client):
#     """..."""
#     mock_get_taxis.return_value.items = taxis_response
#     response = client.get("/taxis")
#     print(response.data)
#     assert response.status == "200 OK"
#     assert json.loads(response.get_data()) == taxis_response


# --------IVY TEST:
# @patch("fleet_api.app.taxis.get",
#        name="mock_get_taxis",
#        return_value=TAXIS_RESPONSE)
# def test_get_taxis(mock_get_taxis, client):
#     response = client.get("/taxis")
#     assert response.status == "200 OK"
#     assert json.loads(response.get_data()) == TAXIS_RESPONSE
#     assert mock_get_taxis.call_args.args == (DEFAULT_PAGE, ROWS_PER_PAGE)

# @patch("fleet_api.app.taxis.get",
#        name="mock_get_taxis",
#        return_value=TAXIS_RESPONSE)
# def test_get_taxis_paged(mock_get_taxis, client):
#     client.get("/taxis?page=2&limit=20")
#     assert mock_get_taxis.call_args.args == (2, 20)

# VER VIDEO IVY MIN 36 TESTS TRAJECTORIES


# --------CHAT GPT v2:

# import json
# from unittest.mock import patch, MagicMock
# from .mock_data import taxis_response
# from flask_sqlalchemy import Pagination

# def test_get_taxis(client):
#     """..."""
#     response = client.get("/taxis")
#     assert response.status == "200 OK"

# @patch("app.models.Taxis.query.paginate", name="mock_paginate")
# def test_get_taxis_response(mock_paginate, client):
#     """..."""
#     # Crear un mock de Pagination
#     mock_pagination = MagicMock(spec=Pagination)
#     mock_pagination.items = taxis_response
#     mock_paginate.return_value = mock_pagination

#     response = client.get("/taxis")
#     assert response.status == "200 OK"
#     assert json.loads(response.get_data()) == taxis_response


# --------CHAT GPT v1:

# from app import app, db
# from models import Taxis

# def test_get_taxis(client):
#     # Insertar datos de prueba
#     taxi1 = Taxis(plate="ABC123")
#     taxi2 = Taxis(plate="XYZ789")
#     db.session.add(taxi1)
#     db.session.add(taxi2)
#     db.session.commit()
    
#     # Hacer la solicitud GET
#     response = client.get("/taxis?page=1&limit=2")
#     assert response.status_code == 200
    
#     data = response.get_json()
#     assert len(data) == 2
#     assert data[0]["id"] == taxi1.id
#     assert data[0]["plate"] == "ABC123"
#     assert data[1]["id"] == taxi2.id
#     assert data[1]["plate"] == "XYZ789"
