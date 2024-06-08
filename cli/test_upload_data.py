"""Tests for upload_data.py"""

from .upload_data import query_taxis, query_trajectories, get_queries

def test_query_taxis():
    """Test for query_taxis"""
    line_list = ["7249", "CNCJ-2997"]
    query = query_taxis(*line_list)
    assert query == "INSERT INTO taxis (id, plate) VALUES (7249,'CNCJ-2997');"


def test_query_trajectories():
    """Test for query_trajectories"""
    line_list = ["2749", "2008-02-02 20:40:39", "116.45019", "39.86295"]
    query = query_trajectories(*line_list)
    assert query == "INSERT INTO trajectories (taxi_id, date, latitude, longitude) VALUES (2749,'2008-02-02 20:40:39',116.45019,39.86295);"


def test_get_queries():
    """Test for get_queries"""
    file = ["7249,CNCJ-2997", "6402,HNCJ-5063"]
    queries = get_queries("taxis", file)
    assert len(queries) == 2


def test_get_queries_empty_file():
    """Test for get_queries"""
    file = []
    queries = get_queries("taxis", file)
    assert len(queries) == 0
