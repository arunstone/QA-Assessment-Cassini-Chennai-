import pytest
import time
import requests
import concurrent.futures
from utils.api_client import ApiClient
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Helper to create a session with retries
def get_retry_session(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = Retry(total=retries, backoff_factor=backoff_factor,
                  status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def test_tc_perf_001_response_time_jsonplaceholder(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)

    # GET single post
    t0 = time.perf_counter()
    r1 = client.get('/posts/1')
    t1 = time.perf_counter()
    duration = t1 - t0
    print(f"GET /posts/1 response time: {duration:.3f}s")
    assert r1.status_code == 200 and duration < 1.0

    # GET all posts
    t0 = time.perf_counter()
    rc = client.get('/posts')
    t1 = time.perf_counter()
    duration = t1 - t0
    print(f"GET /posts response time: {duration:.3f}s")
    assert rc.status_code == 200 and duration < 1.0

    # POST a new post
    t0 = time.perf_counter()
    rp = client.post('/posts', json={"title": "t", "body": "b", "userId": 1})
    t1 = time.perf_counter()
    duration = t1 - t0
    print(f"POST /posts response time: {duration:.3f}s")
    assert rp.status_code in (200, 201) and duration < 1.0


def test_tc_perf_002_concurrent_requests_httpbin(base_urls):
    url = f"{base_urls['httpbin']}/get"
    session = get_retry_session()
    
    def fetch(_):
        return session.get(url, timeout=5)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        t0 = time.perf_counter()
        results = list(ex.map(fetch, range(10)))
        duration = time.perf_counter() - t0

    for i, r in enumerate(results):
        print(f"Request {i} returned status {r.status_code}")
    assert all(r.status_code == 200 for r in results)
    print(f"Concurrent requests duration: {duration:.3f}s")
    assert duration < 10


def test_tc_perf_003_pagination_jsonplaceholder(base_urls, session):
    client = ApiClient(base_urls['jsonplaceholder'], session=session)
    for p in [1, 2, 5]:
        resp = client.get(f'/posts?_page={p}&_limit=20')
        print(f"GET page {p} status: {resp.status_code}")
        assert resp.status_code == 200


def test_tc_perf_004_stress_httpbin_echo(base_urls, session):
    client = ApiClient(base_urls['httpbin'], session=session)
    payload = {"data": "x" * 1024}
    successes = 0

    def post_payload():
        try:
            r = client.post('/post', json=payload)
            return r.status_code == 200
        except Exception:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(post_payload) for _ in range(50)]
        for i, f in enumerate(futures):
            if f.result():
                successes += 1

    success_rate = successes / 50
    print(f"Stress test success rate: {success_rate:.2%}")
    assert success_rate >= 0.95
