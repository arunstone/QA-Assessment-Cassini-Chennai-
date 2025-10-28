import pytest
import time
from utils.api_client import ApiClient
from utils.config import get_base_url


@pytest.mark.smoke
def test_tc_auth_001_valid_authentication(session):
    """
    TC_AUTH_001: Valid Authentication (ReqRes)
    Endpoint: POST https://reqres.in/api/login
    Request Body:
        {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    Expected:
        - 200 OK
        - Response contains token field
        - Token is a non-empty string
        - Response time < 2 seconds
    """
    client = ApiClient(get_base_url("reqres"), session=session)
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    start_time = time.time()
    response = client.post("login", json=payload)
    response_time = time.time() - start_time

    # --- Response time ---
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    # --- Status code ---
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    body = response.json()

    # --- Token validations ---
    assert "token" in body, "Token field missing in response"
    assert isinstance(body["token"], str), "Token should be a string"
    assert body["token"].strip(), "Token value should not be empty"


@pytest.mark.regression
def test_tc_auth_002_invalid_credentials(session):
    """
    TC_AUTH_002: Invalid Credentials (ReqRes)
    Endpoint: POST https://reqres.in/api/login
    Request Body:
        {
            "email": "eve.holt@reqres.in",
            "password": "wrongpassword"
        }
    Expected:
        - 400 Bad Request
        - Error field present in response
        - No token returned
        - Consistent JSON error structure
    """
    client = ApiClient(get_base_url("reqres"), session=session)
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "wrongpassword"
    }

    start_time = time.time()
    response = client.post("login", json=payload)
    response_time = time.time() - start_time

    # --- Response code and time ---
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    body = response.json()

    # --- Error structure ---
    assert "error" in body, "Error field missing in response"
    assert "token" not in body, "Token should not be returned for invalid credentials"
    assert isinstance(body["error"], str), "Error message must be string"


@pytest.mark.regression
def test_tc_auth_003_missing_password(session):
    """
    TC_AUTH_003: Missing Password (ReqRes)
    Endpoint: POST https://reqres.in/api/login
    Request Body:
        {
            "email": "eve.holt@reqres.in"
        }
    Expected:
        - 400 Bad Request
        - Error message: "Missing password"
        - Response follows standard error format
    """
    client = ApiClient(get_base_url("reqres"), session=session)
    payload = {
        "email": "eve.holt@reqres.in"
    }

    start_time = time.time()
    response = client.post("login", json=payload)
    response_time = time.time() - start_time

    # --- Response code and time ---
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    body = response.json()

    # --- Error format ---
    assert "error" in body, "Error field missing in response"
    assert body["error"].lower() == "missing password", \
        f"Expected 'Missing password', got: {body['error']}"
    assert "token" not in body, "Token should not be present in error response"
