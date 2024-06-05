"""Tests for upload_data.py"""

from .upload_data import query_taxis, get_queries

def test_query_taxis():
    """Test for query_taxis"""
    query = query_taxis(*["7249", "CNCJ-2997"])
    assert isinstance(query, str)


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
