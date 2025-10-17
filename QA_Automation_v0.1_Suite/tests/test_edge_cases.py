from utils.api_client import ApiClient
import pytest

def test_tc_edge_001_empty_request_body(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    resp = client.post('/posts', json={})
    assert resp.status_code in (201, 400)

def test_tc_edge_002_maximum_string_lengths(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    long_str = 'x' * 10000
    resp = client.post('/posts', json={"title": long_str, "body": long_str, "userId": 1})
    assert resp.status_code in (201, 200)

def test_tc_edge_003_unicode_and_special_characters(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    payload = {"name": "José María González-Pérez £$%^", "email": "josé@müller.com"}
    resp = client.post('/posts', json={"title": payload['name'], "body": payload['email'], "userId": 1})
    assert resp.status_code in (201, 200)
