import os
import pytest
import requests
from dotenv import load_dotenv
from utils.validators import validate_schema

load_dotenv()

@pytest.fixture(scope="session")
def headers():
    token = os.getenv("GOREST_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}

@pytest.fixture(scope="function")
def session():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture(scope="session")
def jsonschema_validator():
    return validate_schema
