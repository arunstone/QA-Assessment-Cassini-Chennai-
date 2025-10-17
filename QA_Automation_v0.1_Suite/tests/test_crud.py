import pytest
from utils.api_client import ApiClient

def test_tc_crud_001_create_post_jsonplaceholder(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    payload = {"title": "Test Post Title", "body": "This is a test post body content for automation testing", "userId": 1}
    resp = client.post('/posts', json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert 'id' in body
    assert body['title'] == payload['title']

def test_tc_crud_002_create_user_gorest(base_urls, session, headers):
    if not headers:
        pytest.skip('GOREST_TOKEN not configured; skipping TC_CRUD_002')
    import uuid
    client = ApiClient(base_urls['gorest'], session=session, headers=headers)
    unique_email = f"john.doe.{uuid.uuid4().hex[:6]}@example.com"
    payload = {"name": "John Doe", "email": unique_email, "gender": "male", "status": "active"}
    resp = client.post('/users', json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert 'id' in body
    assert body['email'] == unique_email

def test_tc_crud_003_read_single_post_jsonplaceholder(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    resp = client.get('/posts/1')
    assert resp.status_code == 200
    body = resp.json()
    assert all(k in body for k in ('id', 'title', 'body', 'userId'))
