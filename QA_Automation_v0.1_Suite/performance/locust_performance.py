from locust import HttpUser, task, between, run_single_user
import time
import concurrent.futures
from utils.api_client import ApiClient
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests


# ---------------------------------------
# Helper: Create session with retry logic
# ---------------------------------------
def get_retry_session(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# ---------------------------------------
# Locust User Class
# ---------------------------------------
class PerformanceUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user think-time between requests

    def on_start(self):
        """Setup reusable client and session before test start"""
        print(f"Starting Locust user on: {self.host}")

    # ---------------------------------------
    # TC_PERF_001: Response Time Validation - JSONPlaceholder
    # ---------------------------------------
    @task(2)
    def tc_perf_001_response_time_jsonplaceholder(self):
        """GET/POST latency check within 1 second"""
        jsonplaceholder_client = ApiClient("https://jsonplaceholder.typicode.com", session=self.client)
        endpoints = [
            ("/posts/1", "GET", None),
            ("/posts", "GET", None),
            ("/posts", "POST", {"title": "t", "body": "b", "userId": 1}),
        ]
        for ep, method, payload in endpoints:
            t0 = time.perf_counter()
            if method == "GET":
                resp = jsonplaceholder_client.get(ep)
            else:
                resp = jsonplaceholder_client.post(ep, json=payload)
            duration = time.perf_counter() - t0
            print(f"{method} {ep} -> {resp.status_code}, {duration:.3f}s")
            assert resp.status_code in (200, 201)
            assert duration < 1.0, f"{ep} too slow: {duration:.3f}s"

    # ---------------------------------------
    # TC_PERF_002: Concurrent Request Handling - HTTPBin
    # ---------------------------------------
    @task(1)
    def tc_perf_002_concurrent_requests_httpbin(self):
        """10 parallel GET requests"""
        httpbin_client = ApiClient("https://httpbin.org", session=self.client)
        session = get_retry_session()

        def fetch(_):
            return httpbin_client.get("/get")

        t0 = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(fetch, range(10)))
        duration = time.perf_counter() - t0

        for i, r in enumerate(results):
            print(f"Request {i} -> Status {r.status_code}")
        assert all(r.status_code == 200 for r in results)
        print(f"Concurrent requests done in {duration:.3f}s")
        assert duration < 10, "Concurrent request batch took too long"

    # ---------------------------------------
    # TC_PERF_003: Pagination Performance - JSONPlaceholder
    # ---------------------------------------
    @task(1)
    def tc_perf_003_pagination_jsonplaceholder(self):
        """GET paginated data quickly"""
        jsonplaceholder_client = ApiClient("https://jsonplaceholder.typicode.com", session=self.client)
        for page in [1, 2, 5]:
            t0 = time.perf_counter()
            resp = jsonplaceholder_client.get(f"/posts?_page={page}&_limit=20")
            duration = time.perf_counter() - t0
            print(f"GET page {page} -> {resp.status_code}, {duration:.3f}s")
            assert resp.status_code == 200
            assert duration < 1.5, f"Page {page} too slow: {duration:.3f}s"

    # ---------------------------------------
    # TC_PERF_004: Stress Test (POST) - HTTPBin
    # ---------------------------------------
    @task(1)
    def tc_perf_004_stress_httpbin_echo(self):
        """50 POSTs with 10 concurrent threads, expect 95% success"""
        httpbin_client = ApiClient("https://httpbin.org", session=self.client)
        payload = {"data": "x" * 1024}
        successes = 0

        def post_payload():
            try:
                r = httpbin_client.post("/post", json=payload, timeout=5)
                return r.status_code == 200
            except Exception:
                return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(post_payload) for _ in range(50)]
            for f in futures:
                if f.result():
                    successes += 1

        success_rate = successes / 50
        print(f"Stress test success rate: {success_rate:.2%}")
        assert success_rate >= 0.95, f"Too many failures: {success_rate:.2%}"


# For quick single-run debugging (optional)
if __name__ == "__main__":
    run_single_user(PerformanceUser)