after pip install -r requirements.txt

# Run all tests with logging and HTML report
pytest -v --log-file=logs/test_run.log --html=reports/test_report.html --self-contained-html

# Run specific test file
pytest tests/test_auth.py -v --log-file=logs/auth_test.log --html=reports/auth_report.html

# Run with markers
pytest -m smoke -v --log-file=logs/smoke_test.log --html=reports/smoke_report.html

# JSONPlaceholder tests
locust -f performance/locust_performance.py --host=https://jsonplaceholder.typicode.com --users 10 --spawn-rate 2

# HTTPBin tests
locust -f performance/locust_performance.py --host=https://httpbin.org --users 10 --spawn-rate 2

# Run headless and save HTML
locust -f performance/locust_performance.py --host=https://httpbin.org --users 10 --spawn-rate 2 --run-time 1m --headless --html=reports/locust_report.html