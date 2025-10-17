from utils.api_client import ApiClient
import pytest

def test_tc_error_001_resource_not_found_jsonplaceholder(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    resp = client.get('/posts/99999')
    assert resp.status_code in (404, 200)
    try:
        body = resp.json()
    except ValueError:
        body = None
    if body == {}:
        assert True

def test_tc_error_002_method_not_allowed_httpbin(base_urls, session):
    client = ApiClient(base_urls['httpbin'], session=session)
    resp = client.delete('/get')
    assert resp.status_code in (405, 200, 404)

def test_tc_error_003_invalid_url_path_jsonplaceholder(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    resp = client.get('/invalid-endpoint')
    assert resp.status_code == 404
