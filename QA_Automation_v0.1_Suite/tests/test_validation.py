import pytest
import time
from utils.api_client import ApiClient
from utils.config import get_base_url


@pytest.mark.regression
def test_tc_valid_001_missing_required_fields_gorest(session, headers):
    """
    TC_VALID_001: Missing Required Fields - GoRest
    Endpoint: POST https://gorest.co.in/public/v2/users
    Headers: Authorization: Bearer <your_gorest_token>
    Request Body:
        {
            "name": "John Doe"
            // Missing required email, gender, status fields
        }
    Expected Response: 422 Unprocessable Entity
    Validation Points:
        - Error array with specific field validation messages
        - Each missing field identified separately
        - Proper error code (422) for validation failure
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_VALID_001")

    client = ApiClient(get_base_url("gorest"), session=session, headers=headers)
    payload = {"name": "John Doe"}

    start_time = time.time()
    response = client.post("users", json=payload)
    response_time = time.time() - start_time

    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    body = response.json()
    assert isinstance(body, list), "Expected error list response"

    # --- Validation for missing fields ---
    missing_fields = {"email", "gender", "status"}
    found_fields = {f for e in body for f in str(e).lower().split()}
    for field in missing_fields:
        assert field in str(body).lower(), f"Missing field error for: {field}"


@pytest.mark.regression
def test_tc_valid_002_invalid_email_format_gorest(session, headers):
    """
    TC_VALID_002: Invalid Email Format - GoRest
    Endpoint: POST https://gorest.co.in/public/v2/users
    Headers: Authorization: Bearer <your_gorest_token>
    Request Body:
        {
            "name": "John Doe",
            "email": "invalid-email-format",
            "gender": "male",
            "status": "active"
        }
    Expected Response: 422 Unprocessable Entity
    Validation Points:
        - Email format validation error in response
        - Error message indicates invalid email format
        - Other fields validation passed
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_VALID_002")

    client = ApiClient(get_base_url("gorest"), session=session, headers=headers)
    payload = {
        "name": "John Doe",
        "email": "invalid-email-format",
        "gender": "male",
        "status": "active",
    }

    start_time = time.time()
    response = client.post("users", json=payload)
    response_time = time.time() - start_time

    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    body = response.json()
    assert isinstance(body, list), "Expected list of validation errors"
    assert any("email" in str(e).lower() for e in body), \
        "Expected 'email' validation error in response"
    assert all(
        field not in str(body).lower() for field in ["gender", "status"]
    ), "Unexpected validation errors for valid fields"


@pytest.mark.regression
def test_tc_valid_003_invalid_enum_values_gorest(session, headers):
    """
    TC_VALID_003: Invalid Enum Values - GoRest
    Endpoint: POST https://gorest.co.in/public/v2/users
    Headers: Authorization: Bearer <your_gorest_token>
    Request Body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "gender": "unknown",
            "status": "maybe"
        }
    Expected Response: 422 Unprocessable Entity
    Validation Points:
        - Invalid enum values rejected
        - Error messages for gender and status fields
        - Valid values suggested in error response
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_VALID_003")

    client = ApiClient(get_base_url("gorest"), session=session, headers=headers)
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "gender": "unknown",
        "status": "maybe",
    }

    start_time = time.time()
    response = client.post("users", json=payload)
    response_time = time.time() - start_time

    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    body = response.json()
    assert isinstance(body, list), "Expected error array in response"

    # --- Validation for enum errors ---
    assert any("gender" in str(e).lower() for e in body), \
        "Expected validation error for gender"
    assert any("status" in str(e).lower() for e in body), \
        "Expected validation error for status"

    # --- Optional: Suggest valid values ---
    valid_values = ["male", "female", "active", "inactive"]
    assert any(v in str(body).lower() for v in valid_values), \
        "Expected valid values to be hinted in error message"
