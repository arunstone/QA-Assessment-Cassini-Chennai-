import pytest
from utils.api_client import ApiClient

def test_tc_valid_001_missing_required_fields_gorest(base_urls, session, headers):
    if not headers:
        pytest.skip('GOREST_TOKEN not configured; skipping TC_VALID_001')
    client = ApiClient(base_urls['gorest'], session=session, headers=headers)
    payload = {"name": "John Doe"}
    resp = client.post('/users', json=payload)
    assert resp.status_code == 422
    body = resp.json()
    assert isinstance(body, list)
    assert any('email' in str(e) for e in body)

def test_tc_valid_002_invalid_email_format_gorest(base_urls, session, headers):
    if not headers:
        pytest.skip('GOREST_TOKEN not configured; skipping TC_VALID_002')
    client = ApiClient(base_urls['gorest'], session=session, headers=headers)
    payload = {"name": "John Doe", "email": "invalid-email-format", "gender": "male", "status": "active"}
    resp = client.post('/users', json=payload)
    assert resp.status_code == 422
    body = resp.json()
    assert any('email' in str(e) for e in body)

def test_tc_valid_003_invalid_enum_values_gorest(base_urls, session, headers):
    if not headers:
        pytest.skip('GOREST_TOKEN not configured; skipping TC_VALID_003')
    client = ApiClient(base_urls['gorest'], session=session, headers=headers)
    payload = {"name": "John Doe", "email": "john@example.com", "gender": "unknown", "status": "maybe"}
    resp = client.post('/users', json=payload)
    assert resp.status_code == 422
    body = resp.json()
    assert any('gender' in str(e) or 'status' in str(e) for e in body)
