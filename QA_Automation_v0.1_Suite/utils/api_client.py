import requests
from typing import Optional

class ApiClient:
    def __init__(self, base_url: str, session: Optional[requests.Session] = None, headers: Optional[dict] = None):
        self.base_url = base_url.rstrip('/')
        self.session = session or requests.Session()
        self.headers = headers or {}

    def url(self, path: str) -> str:
        if path.startswith('http'):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs):
        return self.session.get(self.url(path), headers=self.headers, **kwargs)

    def post(self, path: str, json=None, data=None, **kwargs):
        return self.session.post(self.url(path), json=json, data=data, headers=self.headers, **kwargs)

    def put(self, path: str, json=None, **kwargs):
        return self.session.put(self.url(path), json=json, headers=self.headers, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.session.delete(self.url(path), headers=self.headers, **kwargs)
