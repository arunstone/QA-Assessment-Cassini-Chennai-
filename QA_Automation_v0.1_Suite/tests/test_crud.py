import pytest
import time
import uuid
from utils.api_client import ApiClient
from utils.config import get_base_url


@pytest.mark.smoke
def test_tc_crud_001_create_resource_jsonplaceholder(session):
    """
    TC_CRUD_001: Create Resource - JSONPlaceholder
    Endpoint: POST https://jsonplaceholder.typicode.com/posts
    Expected: 201 Created
    Validation:
        - Response contains created resource with ID (101)
        - All input fields present in response
        - ID field auto-generated
        - Response time < 1 second
    """
    client = ApiClient(get_base_url("jsonplaceholder"), session=session)
    payload = {
        "title": "Test Post Title",
        "body": "This is a test post body content for automation testing",
        "userId": 1,
    }

    start_time = time.time()
    response = client.post("posts", json=payload)
    response_time = time.time() - start_time

    # --- Response time check ---
    assert response_time < 1, f"Response took too long: {response_time:.2f}s"

    # --- Status code check ---
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    body = response.json()

    # --- Field validations ---
    assert all(key in body for key in ("id", "title", "body", "userId")), \
        "One or more required fields missing in response"
    assert isinstance(body["id"], int), "ID should be integer (auto-generated)"
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]


@pytest.mark.regression
def test_tc_crud_002_create_user_gorest(session, headers):
    """
    TC_CRUD_002: Create User - GoRest (Requires Token)
    Endpoint: POST https://gorest.co.in/public/v2/users
    Expected: 201 Created
    Validation:
        - Response contains created user with ID
        - All input fields properly saved
        - Email uniqueness enforced
    """
    if not headers:
        pytest.skip("GOREST_TOKEN not configured; skipping TC_CRUD_002")

    client = ApiClient(get_base_url("gorest"), session=session, headers=headers)

    unique_email = f"john.doe.{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "John Doe Automation",
        "email": unique_email,
        "gender": "male",
        "status": "active",
    }

    start_time = time.time()
    response = client.post("users", json=payload)
    response_time = time.time() - start_time

    # --- Status code ---
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert response_time < 2, f"Response took too long: {response_time:.2f}s"

    body = response.json()

    # --- Field validations ---
    assert "id" in body, "User ID not present in response"
    assert isinstance(body["id"], int), "User ID should be integer"
    assert body["email"] == unique_email, "Email mismatch"
    assert body["name"] == payload["name"]
    assert body["gender"] == payload["gender"]
    assert body["status"] == payload["status"]

    # --- Email uniqueness check ---
    # Attempt to create same email again -> should fail
    duplicate_resp = client.post("users", json=payload)
    assert duplicate_resp.status_code in (400, 422), \
        "Duplicate email should not be allowed"


@pytest.mark.regression
def test_tc_crud_003_read_single_resource_jsonplaceholder(session):
    """
    TC_CRUD_003: Read Single Resource - JSONPlaceholder
    Endpoint: GET https://jsonplaceholder.typicode.com/posts/1
    Expected: 200 OK
    Validation:
        - Complete resource data returned
        - Fields: id, title, body, userId present
        - Data types: id and userId are integers
        - title and body are strings
    """
    client = ApiClient(get_base_url("jsonplaceholder"), session=session)

    start_time = time.time()
    response = client.get("posts/1")
    response_time = time.time() - start_time

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response_time < 1, f"Response took too long: {response_time:.2f}s"

    body = response.json()

    # --- Field presence ---
    required_fields = ["id", "userId", "title", "body"]
    for field in required_fields:
        assert field in body, f"Missing field: {field}"

    # --- Data types ---
    assert isinstance(body["id"], int), "id must be integer"
    assert isinstance(body["userId"], int), "userId must be integer"
    assert isinstance(body["title"], str), "title must be string"
    assert isinstance(body["body"], str), "body must be string"
