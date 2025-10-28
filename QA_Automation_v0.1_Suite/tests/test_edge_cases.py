import pytest
from utils.api_client import ApiClient


@pytest.mark.edge
def test_tc_edge_001_empty_request_body_gorest(base_urls, session, headers):
    """
    TC_EDGE_001: Empty Request Body - GoRest
    Endpoint: POST https://gorest.co.in/public/v2/users
    Objective:
        Validate API behavior when request body is completely empty.
    Expected Response:
        400 Bad Request or 422 Unprocessable Entity
    Validation Points:
        - Proper validation error messages returned
        - No internal server error (500)
        - Response in valid JSON structure
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_EDGE_001")

    client = ApiClient(base_urls["gorest"], session=session, headers=headers)
    resp = client.post("/users", json={})
    print(f"Status: {resp.status_code}, Response: {resp.text[:100]}")
    assert resp.status_code in (400, 422)
    body = resp.json()
    assert isinstance(body, list)
    assert any("field" in e and "message" in e for e in body)


@pytest.mark.edge
def test_tc_edge_002_maximum_string_lengths_gorest(base_urls, session, headers):
    """
    TC_EDGE_002: Maximum String Lengths - GoRest
    Endpoint: POST https://gorest.co.in/public/v2/users
    Objective:
        Verify behavior when sending fields with extremely large string lengths.
    Expected Response:
        201 Created
    Validation Points:
        - Data saved correctly
        - No truncation or internal errors
        - Response time acceptable
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_EDGE_002")

    client = ApiClient(base_urls["gorest"], session=session, headers=headers)
    long_str = "x" * 255  # realistic boundary
    payload = {
        "name": long_str,
        "email": f"test_{long_str[:10]}@example.com",
        "gender": "male",
        "status": "active",
    }
    resp = client.post("/users", json=payload)
    print(f"Status: {resp.status_code}, Length Sent: {len(long_str)}")
    assert resp.status_code == 201
    body = resp.json()
    assert "id" in body
    assert body["name"] == long_str


@pytest.mark.edge
def test_tc_edge_003_unicode_and_special_characters_gorest(base_urls, session, headers):
    """
    TC_EDGE_003: Unicode and Special Characters - GoRest
    Endpoint: POST https://gorest.co.in/public/v2/users
    Objective:
        Ensure API handles Unicode, accents, and special characters gracefully.
    Expected Response:
        201 Created
    Validation Points:
        - Unicode characters stored properly
        - No encoding or validation errors
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_EDGE_003")

    client = ApiClient(base_urls["gorest"], session=session, headers=headers)
    payload = {
        "name": "José María González-Pérez £$%^",
        "email": "jose.maria.gp@example.com",
        "gender": "male",
        "status": "active",
    }
    resp = client.post("/users", json=payload)
    print(f"Status: {resp.status_code}, Response: {resp.text[:100]}")
    assert resp.status_code == 201
    body = resp.json()
    assert all(
        key in body for key in ("id", "name", "email", "gender", "status")
    )
    assert "José" in body["name"]
