import pytest
from utils.api_client import ApiClient

valid_login_payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
invalid_payload = {"email": "eve.holt@reqres.in", "password": "wrongpassword"}
missing_password = {"email": "eve.holt@reqres.in"}

def test_tc_auth_001_valid_auth(base_urls, session):
    """Simulated valid authentication (HTTPBin mock)."""
    client = ApiClient(base_urls['httpbin'], session=session)
    resp = client.post('/post', json=valid_login_payload)
    assert resp.status_code == 200
    body = resp.json()
    assert 'json' in body
    assert body['json']['email'] == valid_login_payload['email']

def test_tc_auth_002_invalid_credentials(base_urls, session):
    """Invalid credentials mock"""
    client = ApiClient(base_urls['httpbin'], session=session)
    resp = client.post('/post', json=invalid_payload)
    assert resp.status_code == 200
    body = resp.json()
    assert 'json' in body
    assert body['json']['password'] == invalid_payload['password']

def test_tc_auth_003_missing_password(base_urls, session):
    """Missing password mock"""
    client = ApiClient(base_urls['httpbin'], session=session)
    resp = client.post('/post', json=missing_password)
    assert resp.status_code == 200
    body = resp.json()
    assert 'json' in body
    assert 'password' not in body['json']
