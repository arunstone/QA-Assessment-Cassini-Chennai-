import pytest
from utils.api_client import ApiClient


@pytest.mark.regression
def test_tc_error_001_resource_not_found_jsonplaceholder(base_urls, session):
    """
    TC_ERROR_001: Resource Not Found - JSONPlaceholder
    Endpoint: GET https://jsonplaceholder.typicode.com/posts/99999
    Expected Response: 404 Not Found
    Validation Points:
        - Empty response body: {}
        - HTTP status code 404
        - No sensitive information exposed
    """
    client = ApiClient(base_urls["jsonplaceholder"], session=session)
    resp = client.get("/posts/99999")

    # ✅ Status code must be 404
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"

    # ✅ Response should be empty JSON
    try:
        body = resp.json()
    except ValueError:
        body = None
    assert body == {}, f"Expected empty JSON body, got {body}"

    # ✅ Check that no sensitive info is leaked
    assert not any(keyword in resp.text.lower() for keyword in ["error", "stack", "trace", "debug"]), \
        "Sensitive debug info found in response"


@pytest.mark.regression
def test_tc_error_002_method_not_allowed_httpbin(base_urls, session):
    """
    TC_ERROR_002: Method Not Allowed - HTTPBin
    Endpoint: DELETE https://httpbin.org/get
    Expected Response: 405 Method Not Allowed
    Validation Points:
        - Method not allowed error
        - Allowed methods may be listed in response
        - Consistent error format
    """
    client = ApiClient(base_urls["httpbin"], session=session)
    resp = client.delete("/get")

    # ✅ Status code validation
    assert resp.status_code == 405, f"Expected 405, got {resp.status_code}"

    # ✅ Response content validation
    body = resp.json()
    body_text = str(body).lower()
    assert "method" in body_text or "allow" in body_text, "Expected method not allowed info in response"

    # ✅ Optional: check consistent structure
    assert isinstance(body, dict), "Expected JSON object response format"


@pytest.mark.regression
def test_tc_error_003_invalid_url_path_jsonplaceholder(base_urls, session):
    """
    TC_ERROR_003: Invalid URL Path - JSONPlaceholder
    Endpoint: GET https://jsonplaceholder.typicode.com/invalidendpoint
    Expected Response: 404 Not Found
    Validation Points:
        - Empty response body: {}
        - 404 status code for invalid endpoints
        - Consistent error handling
    """
    client = ApiClient(base_urls["jsonplaceholder"], session=session)
    resp = client.get("/invalidendpoint")

    # ✅ Status code validation
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"

    # ✅ Body validation (empty JSON)
    try:
        body = resp.json()
    except ValueError:
        body = None
    assert body == {}, f"Expected empty JSON body, got {body}"

    # ✅ No sensitive data or HTML in error response
    assert "<html" not in resp.text.lower(), "Unexpected HTML found in error response"
